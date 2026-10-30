#!/usr/bin/env python3
"""Check an analysis SQL file for the habits that give plausible wrong answers.

A heuristic reader, not a parser: it finds likely mistakes and says why.
The file should start with comments "-- Question:" and "-- Definition:".
"""
import re
import sys

WRITE = re.compile(r"^\s*(insert|update|delete|drop|truncate|alter|create|grant|merge)\b", re.I)


def strip_comments(sql):
    sql = re.sub(r"--[^\n]*", "", sql)
    return re.sub(r"/\*.*?\*/", "", sql, flags=re.S)


def statements(sql):
    return [s.strip() for s in strip_comments(sql).split(";") if s.strip()]


def check(sql):
    out = []
    head = "\n".join(l for l in sql.splitlines() if l.strip().startswith("--"))
    if not re.search(r"--\s*question\s*:", head, re.I):
        out.append("no '-- Question:' comment: say what is being asked")
    if not re.search(r"--\s*definitions?\s*:", head, re.I):
        out.append("no '-- Definition:' comment: say what counts and over which dates")
    stmts = statements(sql)
    if not stmts:
        out.append("no SQL statements found")
    for n, s in enumerate(stmts, 1):
        low = re.sub(r"\s+", " ", s.lower())
        tag = f"statement {n}"
        if WRITE.match(s):
            out.append(f"{tag}: changes data; analysis should only read")
            continue
        if re.search(r"select\s+(distinct\s+)?\*", low) or re.search(r",\s*\*\s*from", low) or re.search(r"\b\w+\.\*", low) and "count(*)" not in low:
            out.append(f"{tag}: SELECT * pulls every column; name the ones you need")
        for m in re.finditer(r"\b(?:inner |left |right |full |outer |cross |natural )*join\b[^;]*?(?=\bjoin\b|\bwhere\b|\bgroup\b|\border\b|\blimit\b|$)", low):
            part = m.group(0)
            if not re.search(r"\bon\b|\busing\b", part) and "cross join" not in part and "natural" not in part:
                out.append(f"{tag}: a join with no ON or USING condition multiplies every row by every row")
                break
        if re.search(r"\bbetween\b\s+\S*\d{4}-\d{2}-\d{2}", low) or re.search(r"\bbetween\b.*\b(date|timestamp)\b", low):
            out.append(f"{tag}: BETWEEN on dates includes the whole end moment or day; use >= start and < next day")
        if re.search(r"(=|!=|<>)\s*null\b", low):
            out.append(f"{tag}: '= NULL' is never true; use IS NULL or IS NOT NULL")
        m = re.search(r"left join\s+(\w+)(?:\s+(?:as\s+)?(\w+))?", low)
        if m:
            alias = m.group(2) if m.group(2) and m.group(2) not in {"on", "where", "left", "inner", "join"} else m.group(1)
            tail = low[m.end():]  # only a WHERE that comes after the join can undo it
            where = tail.split(" where ", 1)[1] if " where " in tail else ""
            if re.search(rf"\b{re.escape(alias)}\.\w+\s*(=|>=|<=|<>|!=|>|<|\blike\b|\bin\b)", where) and not re.search(rf"{re.escape(alias)}\.\w+ is null", where):
                out.append(f"{tag}: filtering the LEFT JOIN table in WHERE turns it into an inner join; move the test into ON")
        has_join = bool(re.search(r"\bjoin\b", low))
        if has_join and re.search(r"count\(\s*(?!distinct|\*)\w+(\.\w+)?\s*\)", low):
            out.append(f"{tag}: COUNT on a joined result can count one thing many times; use COUNT(DISTINCT id) and check the row count after each join")
        if has_join and re.search(r"select\s+distinct", low):
            out.append(f"{tag}: SELECT DISTINCT with a join may be hiding duplicate rows; find out why they appear")
        if re.search(r"/\s*(?!nullif)\(?\s*\w+(\.\w+)?\s*\)?", low) and re.search(r"\bsum\(|\bcount\(|\bavg\(", low) and "nullif" not in low and re.search(r"\)\s*/\s*", low):
            out.append(f"{tag}: division with no NULLIF: a zero will stop the query or give a wrong rate")
        if re.search(r"'\d{1,2}/\d{1,2}/\d{2,4}'", low):
            out.append(f"{tag}: a date like 01/02/2026 reads differently in different places; use 2026-02-01")
        if re.search(r"\bselect\b", low) and re.search(r"\b(sum|avg|count|min|max)\(", low) and not re.search(r"\bgroup by\b", low):
            cols = re.match(r"select (.*?) from", low)
            if cols and re.search(r"\b\w+(\.\w+)?\s*,", re.sub(r"\([^)]*\)", "()", cols.group(1))) and not re.search(r"over\s*\(", low):
                out.append(f"{tag}: mixes totals with plain columns but has no GROUP BY")
    return out


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    found = check(text)
    print("\n".join(found) if found else "SQL OK.")
    sys.exit(1 if found else 0)
