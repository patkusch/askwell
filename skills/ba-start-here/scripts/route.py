#!/usr/bin/env python3
"""Suggest which askwell skills fit a request, in the order to use them.

  route.py "we need a dashboard for refunds"
Prints up to four skills with the reason. If nothing fits it asks the one question.
It matches words, so treat it as a first guess and read the skill's description.
"""
import re
import sys

# skill -> phrases that suggest it. Order inside a request does not matter.
RULES = {
    "problem-statement": ["we need a", "need a way", "we want", "wants a", "would like a", "need to be able", "build a", "new system", "new tool", "dashboard", "what problem", "problem statement", "why are we doing"],
    "stakeholder-mapping": ["stakeholder", "who should i talk", "who do i need", "raci", "power interest", "register"],
    "stakeholder-interview": ["interview", "one-to-one", "talk to the", "subject matter expert", "sme"],
    "workshop-facilitation": ["workshop", "facilitate", "brainstorm", "session plan", "agenda for a workshop"],
    "current-state-analysis": ["as-is", "as is", "current state", "how it works today", "baseline"],
    "root-cause-analysis": ["root cause", "keeps happening", "keeps going wrong", "5 whys", "five whys", "fishbone", "why does"],
    "gap-analysis": ["gap analysis", "swot", "current versus target", "capability gap", "where we are and where"],
    "requirements-elicitation": ["elicit", "gather requirements", "discover requirements", "what should we build", "requirements gathering"],
    "requirements-writing": ["write requirements", "write the requirements", "requirement statements", "shall statements", "vague requirement", "tidy requirements"],
    "user-stories": ["user stor", "epic", "backlog item", "as a user"],
    "acceptance-criteria": ["acceptance criteria", "given when then", "definition of done", "test scenarios"],
    "use-cases": ["use case", "use-case", "interaction flow", "main flow"],
    "nonfunctional-requirements": ["non-functional", "nonfunctional", "performance requirement", "availability", "security requirement", "accessibility", "service level"],
    "scope-definition": ["scope", "out of scope", "scope creep", "what is in and out"],
    "requirements-conflict-check": ["conflict", "contradict", "review the requirements", "sanity check", "inconsisten"],
    "requirements-traceability": ["traceability", "rtm", "coverage", "everything we promised"],
    "brd-writing": ["brd", "business requirements document", "requirements document", "frd", "srs"],
    "process-mapping": ["process map", "draw the process", "flowchart", "swimlane", "bpmn", "map the process", "as-is process"],
    "data-dictionary": ["data dictionary", "glossary", "definition of", "what does the term", "data requirements", "field definitions"],
    "sql-for-analysis": ["sql", "query the", "pull the numbers", "how many", "database query"],
    "kpi-definition": ["kpi", "metric", "success measure", "measure success", "target for"],
    "business-case": ["business case", "roi", "payback", "npv", "cost-benefit", "cost benefit", "worth doing", "justify", "investment"],
    "options-analysis": ["options", "compare approaches", "build or buy", "build versus buy", "go/no-go", "recommend one"],
    "vendor-selection": ["vendor", "supplier", "rfp", "which product", "scorecard", "procurement"],
    "backlog-prioritisation": ["prioriti", "moscow", "rice", "wsjf", "what goes first", "ranking the backlog"],
    "raid-log": ["raid", "risk register", "risks", "assumptions log", "issue log", "dependencies"],
    "decision-log": ["decision log", "why did we decide", "record the decision", "decisions"],
    "change-impact-assessment": ["impact assessment", "change request", "change management", "who is affected", "training plan", "go-live readiness"],
    "user-acceptance-testing": ["uat", "acceptance test", "go live", "go-live", "sign-off", "defects"],
    "stakeholder-communication": ["status report", "executive summary", "update for", "brief the", "bad news", "write to the sponsor"],
    "meeting-minutes": ["minutes", "action items", "meeting notes", "transcript", "agenda"],
}
DOMAINS = {
    "financial-services": ["bank", "payment", "lending", "loan", "kyc", "aml", "fintech", "investment"],
    "insurance": ["insurance", "claim", "policy holder", "underwriting", "premium"],
    "public-sector": ["council", "government", "citizen", "public sector", "agency"],
    "healthcare": ["patient", "clinical", "hospital", "nhs", "hipaa", "ehr"],
    "saas": ["saas", "subscription", "churn", "multi-tenant"],
    "erp-crm": ["erp", "crm", "sap", "salesforce", "dynamics"],
    "data-bi": ["dashboard", "warehouse", "bi report", "reporting"],
    "privacy": ["personal data", "gdpr", "privacy", "data protection"],
}
QUESTION = "What is the decision or deliverable this has to support, and who will read it?"


def has(text, phrase):
    return re.search(r"(?<![a-z])" + re.escape(phrase), text) is not None


def route(request, limit=4):
    t = request.lower()
    scored = []
    for skill, phrases in RULES.items():
        hits = [p for p in phrases if has(t, p)]
        if hits:
            scored.append((len(hits), skill, hits))
    scored.sort(key=lambda x: (-x[0], list(RULES).index(x[1])))
    picks = [(s, h) for _, s, h in scored[:limit]]
    domains = [d for d, kws in DOMAINS.items() if any(has(t, k) for k in kws)]
    return picks, domains


if __name__ == "__main__":
    request = " ".join(sys.argv[1:]) or sys.stdin.read()
    picks, domains = route(request)
    if not picks:
        print("No skill matches those words.")
        print("Ask: " + QUESTION)
        sys.exit(1)
    for skill, hits in picks:
        print(f"{skill}  (matched: {', '.join(hits)})")
    if domains:
        print("Also read the domain pack(s): " + ", ".join(domains) + "  (domain-packs/references/)")
