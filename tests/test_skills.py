import csv
import importlib.util
import io
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


case = load(SKILLS / "business-case/scripts/case.py")
rank = load(SKILLS / "backlog-prioritisation/scripts/score.py")
vendor = load(SKILLS / "vendor-selection/scripts/score.py")
trace = load(SKILLS / "requirements-traceability/scripts/check.py")
lint = load(SKILLS / "requirements-writing/scripts/lint.py")
validate = load(ROOT / "scripts/validate_skills.py")


class Repo(unittest.TestCase):
    def test_every_skill_valid(self):
        errs = [e for d in sorted(SKILLS.iterdir()) if d.is_dir() for e in validate.validate(d)]
        self.assertEqual(errs, [])

    def test_cross_references_point_at_real_skills(self):
        names = {d.name for d in SKILLS.iterdir() if d.is_dir()}
        for f in SKILLS.glob("*/SKILL.md"):
            for ref in re.findall(r"`([a-z]+(?:-[a-z]+)+)`", f.read_text()):
                if ref in {"user-friendly", "state-of-the-art", "go-live", "one-to-many", "end-to-end"}:
                    continue
                if f.parent.name != ref and re.fullmatch(r"[a-z]+(-[a-z]+)+", ref) and ref not in names:
                    # only skill-looking refs inside parentheses or "the `x` skill" are checked
                    ctx = f.read_text()
                    if re.search(r"\(`%s`" % ref, ctx) or "the `%s` skill" % ref in ctx:
                        self.fail(f"{f.parent.name} points at missing skill {ref}")


class BusinessCase(unittest.TestCase):
    def test_known_numbers(self):
        r = case.analyse({"discount_rate": 0.1, "upfront_cost": 100,
                          "yearly_benefits": [60, 60, 60], "yearly_costs": [0, 0, 0]})
        self.assertAlmostEqual(r["npv"], 49.21, places=2)
        self.assertAlmostEqual(r["payback_years"], 1.67, places=2)
        self.assertAlmostEqual(r["roi"], 0.8, places=2)
        self.assertAlmostEqual(r["irr"], 0.3631, places=3)  # 60/1.3631 + 60/1.3631^2 + 60/1.3631^3 = 100

    def test_never_pays_back(self):
        r = case.analyse({"discount_rate": 0.05, "upfront_cost": 100,
                          "yearly_benefits": [10], "yearly_costs": [0]})
        self.assertIsNone(r["payback_years"])
        self.assertLess(r["npv"], 0)

    def test_mismatched_lists(self):
        with self.assertRaises(ValueError):
            case.cash_flows({"upfront_cost": 1, "yearly_benefits": [1, 2], "yearly_costs": [1]})


class Backlog(unittest.TestCase):
    def test_rice_order(self):
        rows = [dict(id="a", name="A", reach="100", impact="1", confidence="1", effort="1"),
                dict(id="b", name="B", reach="1000", impact="2", confidence="0.5", effort="2")]
        self.assertEqual([r["id"] for r in rank.rank("rice", rows)], ["b", "a"])

    def test_wsjf(self):
        rows = [dict(id="a", name="A", business_value="8", time_criticality="5", risk_reduction="2", job_size="5")]
        self.assertEqual(rank.rank("wsjf", rows)[0]["score"], 3.0)

    def test_zero_effort_rejected(self):
        rows = [dict(id="a", name="A", reach="1", impact="1", confidence="1", effort="0")]
        with self.assertRaises(ValueError):
            rank.rank("rice", rows)


class Vendor(unittest.TestCase):
    D = {"criteria": {"Fit": 60, "Cost": 40},
         "scores": {"A": {"Fit": 5, "Cost": 1}, "B": {"Fit": 3, "Cost": 5}}}

    def test_ranking(self):
        self.assertEqual(list(vendor.score(self.D)), ["B", "A"])
        self.assertEqual(vendor.score(self.D)["A"], 3.4)

    def test_bad_weights(self):
        with self.assertRaises(ValueError):
            vendor.score({"criteria": {"Fit": 50}, "scores": {"A": {"Fit": 3}}})

    def test_score_out_of_range(self):
        with self.assertRaises(ValueError):
            vendor.score({"criteria": {"Fit": 100}, "scores": {"A": {"Fit": 9}}})

    def test_missing_score(self):
        with self.assertRaises(ValueError):
            vendor.score({"criteria": {"Fit": 50, "Cost": 50}, "scores": {"A": {"Fit": 3}}})


class Trace(unittest.TestCase):
    def test_gaps(self):
        rows = [dict(req_id="R1", design_ref="D1", test_ref="T1", status="done"),
                dict(req_id="R2", design_ref="", test_ref="", status="done"),
                dict(req_id="R1", design_ref="D1", test_ref="T1", status="open")]
        out = trace.check(rows)
        self.assertIn("R2: no design reference", out)
        self.assertIn("R2: no test", out)
        self.assertIn("R2: marked done but nothing tests it", out)
        self.assertIn("R1: listed twice", out)

    def test_clean(self):
        self.assertEqual(trace.check([dict(req_id="R1", design_ref="D", test_ref="T", status="open")]), [])


class Lint(unittest.TestCase):
    def test_good(self):
        self.assertEqual(lint.lint("The system shall email a receipt within 5 minutes of payment."), [])

    def test_bad(self):
        out = " ".join(lint.lint("The system should be fast and easy to use, etc."))
        for bit in ("should", "fast", "easy", "etc", "no 'shall'"):
            self.assertIn(bit, out)

    def test_limit_without_number(self):
        self.assertTrue(any("no number" in p for p in lint.lint("The system shall respond within a short time.")))

    def test_blank_line(self):
        self.assertEqual(lint.lint("   "), [])


if __name__ == "__main__":
    unittest.main()
