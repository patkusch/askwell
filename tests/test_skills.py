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
story = load(SKILLS / "user-stories/scripts/check.py")
gwt = load(SKILLS / "acceptance-criteria/scripts/check.py")
conf = load(SKILLS / "requirements-conflict-check/scripts/conflicts.py")
raid = load(SKILLS / "raid-log/scripts/raid.py")
kpi = load(SKILLS / "kpi-definition/scripts/check.py")
cmp = load(SKILLS / "process-mapping/scripts/compare.py")
flow = load(SKILLS / "process-mapping/scripts/check.py")
agenda = load(SKILLS / "meeting-minutes/scripts/agenda.py")
acts = load(SKILLS / "meeting-minutes/scripts/actions.py")
stake = load(SKILLS / "stakeholder-mapping/scripts/check.py")
router = load(SKILLS / "ba-start-here/scripts/route.py")
sqlc = load(SKILLS / "sql-for-analysis/scripts/check.py")
interview = load(SKILLS / "stakeholder-interview/scripts/check.py")
wshop = load(SKILLS / "workshop-facilitation/scripts/check.py")
brd = load(SKILLS / "brd-writing/scripts/check.py")
elic = load(SKILLS / "requirements-elicitation/scripts/check.py")
comms = load(SKILLS / "stakeholder-communication/scripts/check.py")
impact = load(SKILLS / "change-impact-assessment/scripts/check.py")
gapa = load(SKILLS / "gap-analysis/scripts/check.py")
csa = load(SKILLS / "current-state-analysis/scripts/check.py")
rca = load(SKILLS / "root-cause-analysis/scripts/check.py")
optn = load(SKILLS / "options-analysis/scripts/check.py")
scope = load(SKILLS / "scope-definition/scripts/check.py")
pstate = load(SKILLS / "problem-statement/scripts/check.py")
uat = load(SKILLS / "user-acceptance-testing/scripts/summary.py")
dlog = load(SKILLS / "decision-log/scripts/check.py")
nfr = load(SKILLS / "nonfunctional-requirements/scripts/check.py")
gloss = load(SKILLS / "data-dictionary/scripts/glossary.py")
ddict = load(SKILLS / "data-dictionary/scripts/check.py")
usecase = load(SKILLS / "use-cases/scripts/check.py")
import datetime, subprocess, sys

EX = ROOT / "examples" / "refund-approval"
TODAY = datetime.date(2026, 10, 16)


def read(name, which):
    return (EX / which / name).read_text()


def rows(name, which):
    return list(csv.DictReader(io.StringIO(read(name, which))))


class Repo(unittest.TestCase):
    def test_every_skill_valid(self):
        errs = [e for d in sorted(SKILLS.iterdir()) if d.is_dir() for e in validate.validate(d)]
        self.assertEqual(errs, [])

    def test_cross_references_point_at_real_skills(self):
        names = {d.name for d in SKILLS.iterdir() if d.is_dir()}
        allowed = {"user-friendly", "state-of-the-art", "to-do"}
        for f in SKILLS.glob("*/SKILL.md"):
            for ref in re.findall(r"`([a-z]+(?:-[a-z]+)+)`", f.read_text()):
                if ref in allowed or ref.endswith(".py"):
                    continue
                self.assertIn(ref, names, f"{f.parent.name} mentions `{ref}`, which is not a skill")


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



class Stories(unittest.TestCase):
    def test_good_story(self):
        self.assertEqual(story.check("As a finance manager, I want a list of waiting refunds, so that I can clear them before the audit."), [])

    def test_planted_flaws(self):
        out = {i: story.check(l) for i, l in enumerate(read("stories.txt", "bad").splitlines())}
        self.assertTrue(any("too general" in p for p in out[0]))
        self.assertTrue(any("repeats" in p for p in out[0]))
        self.assertTrue(any("solution" in p for p in out[0]))
        self.assertTrue(any("not in the form" in p for p in out[1]))
        self.assertTrue(any("not a person" in p for p in out[2]))
        self.assertTrue(any("two stories" in p for p in out[3]))


class Criteria(unittest.TestCase):
    def test_good_set_clean(self):
        self.assertEqual(gwt.check(read("criteria.txt", "good")), ([], []))

    def test_bad_set(self):
        per, whole = gwt.check(read("criteria.txt", "bad"))
        text = " ".join(p for _, p in per) + " ".join(whole)
        for bit in ("missing 'When'", "properly", "more than one 'When'", "no scenario tests a failure"):
            self.assertIn(bit, text)

    def test_out_of_order(self):
        per, _ = gwt.check("Then x. When y. Given z.\n\nGiven a, when b, then error c.\n\nGiven a, when b, then d.")
        self.assertTrue(any("out of order" in p for _, p in per))


class Conflicts(unittest.TestCase):
    def test_bad_finds_each_kind(self):
        found = conf.find(rows("conflict.csv", "bad"), json.loads(read("terms.json", "bad")))
        kinds = {f[0] for f in found}
        self.assertEqual(kinds, {"number clash", "duplicate", "opposite", "term drift"})
        self.assertIn(("duplicate", "R1", "R3", "say nearly the same thing: merge"), found)

    def test_unrelated_requirements_not_flagged(self):
        r = [dict(id="A", text="The system shall email a receipt within 5 minutes"),
             dict(id="B", text="Managers shall approve refunds over 500")]
        self.assertEqual(conf.find(r), [])


class Raid(unittest.TestCase):
    def test_good_clean_bad_flagged(self):
        flags, ranked = raid.review(rows("raid.csv", "good"), TODAY)
        self.assertEqual(flags, [])
        self.assertEqual(ranked[0][1], "K1")
        flags, ranked = raid.review(rows("raid.csv", "bad"), TODAY)
        joined = "\n".join(flags)
        for bit in ("K1: no owner", "K1: overdue by 45 days", "K1: score 20", "K3: no due date", "K3: risk without"):
            self.assertIn(bit, joined)
        self.assertNotIn("K4", joined)  # closed items are ignored


class Kpi(unittest.TestCase):
    def test_good(self):
        self.assertEqual(kpi.check(json.loads(read("kpis.json", "good"))), [])

    def test_bad(self):
        out = "\n".join(kpi.check(json.loads(read("kpis.json", "bad"))))
        for bit in ("no source", "no owner", "no guard", "target has no number", "baseline has no number", "formula does not say"):
            self.assertIn(bit, out)


class Flow(unittest.TestCase):
    def test_good(self):
        self.assertEqual(flow.check(read("process.mmd", "good")), [])

    def test_bad(self):
        out = "\n".join(flow.check(read("process.mmd", "bad")))
        for bit in ("2 starting points", "C: decision with 1 exit", "no label", "E: dead end", "F: dead end"):
            self.assertIn(bit, out)

    def test_unreachable_step(self):
        out = flow.check("flowchart TD\n A([s]) --> B{q}\n B -- Yes --> C([e])\n B -- No --> C\n D[loop] --> E[loop2]\n E --> D")
        self.assertTrue(any("cannot be reached" in p for p in out))

    def test_mermaid_inline_label_forms(self):
        self.assertEqual(flow.check("flowchart TD\n A([s]) --> B{q}\n B -->|Yes| C([e])\n B -- No --> C"), [])

    def test_not_a_flowchart(self):
        self.assertTrue(flow.check("hello"))


class Minutes(unittest.TestCase):
    def test_good_all_owned_and_dated(self):
        actions, decisions = acts.extract(read("notes.txt", "good"))
        self.assertEqual(len(decisions), 1)
        self.assertEqual(len(actions), 2)
        self.assertTrue(all(not m for _, _, m in actions))

    def test_bad(self):
        actions, _ = acts.extract(read("notes.txt", "bad"))
        got = {s: m for _, s, m in actions}
        self.assertEqual(got["Someone should chase the provider."], ["owner", "date"])
        self.assertEqual(got["Priya will send the threshold."], ["date"])
        self.assertEqual(got["ACTION: confirm file format"], ["owner", "date"])
        self.assertNotIn("Agreed to launch in November.", got)  # a decision, not an action


class UseCases(unittest.TestCase):
    def test_good(self):
        self.assertEqual(usecase.check(read("usecase.txt", "good")), [])

    def test_bad(self):
        out = "\n".join(usecase.check(read("usecase.txt", "bad")))
        for bit in ("missing 'Trigger'", "missing 'Preconditions'", "'Exceptions' is empty", "verb and an object",
                    "too thin", "('button')", "contains a branch", "9a branches from step 9"):
            self.assertIn(bit, out)

    def test_too_long_and_misnumbered(self):
        base = "Name: Do a thing\nActor: a\nGoal: g\nTrigger: t\nPreconditions: p\nMain flow:\n"
        steps = "".join(f"  {i}. Step {i}.\n" for i in range(1, 14))
        out = usecase.check(base + steps + "Alternative flows:\n  2a. x\nExceptions:\n  3e. y\nPostconditions: z")
        self.assertTrue(any("split it" in p for p in out))
        out = usecase.check(base + "  1. a\n  3. b\n  4. c\nAlternative flows:\n  1a. x\nExceptions:\n  1e. y\nPostconditions: z")
        self.assertTrue(any("not numbered" in p for p in out))


class DataDictionary(unittest.TestCase):
    def test_good(self):
        self.assertEqual(ddict.check(rows("dictionary.csv", "good")), [])

    def test_bad(self):
        out = "\n".join(ddict.check(rows("dictionary.csv", "bad")))
        for bit in ("too short", "refund_amount: no source", "no owner", "no currency", "financial data with no retention",
                    "refund_status: no meaning", "none are given", "no time zone", "free text", "defined twice"):
            self.assertIn(bit, out)

    def test_circular_meaning(self):
        r = [dict(field="customer_name", meaning="The name of the customer", type="text", source="crm", owner="x")]
        self.assertTrue(any("repeats the field name" in p for p in ddict.check(r)))


class Nfr(unittest.TestCase):
    def test_good_covers_all_twelve_areas(self):
        self.assertEqual(nfr.check(rows("nfr.csv", "good")), [])

    def test_bad(self):
        out = "\n".join(nfr.check(rows("nfr.csv", "bad")))
        for bit in ("N1: no measurable number", "N1: no way to test", "N1: priority must be", "N2: a speed with no load",
                    "N3: availability with no percentage", "N4: too vague", "N5: area 'looks-nice'", "not covered yet: capacity"):
            self.assertIn(bit, out)

    def test_dropping_a_row_reports_the_gap(self):
        rs = [r for r in rows("nfr.csv", "good") if r["area"] != "recovery"]
        self.assertEqual(nfr.check(rs), ["not covered yet: recovery (ask, or record that it does not apply)"])

    def test_business_days_count_as_a_number(self):
        r = [dict(id="N", area="support", requirement="Faults fixed within 1 business day", how_tested="log", priority="must")]
        self.assertNotIn("N: no measurable number", " ".join(nfr.check(r)))


class Stakeholders(unittest.TestCase):
    def test_good(self):
        self.assertEqual(stake.check(rows("stakeholders.csv", "good")), [])

    def test_bad(self):
        out = "\n".join(stake.check(rows("stakeholders.csv", "bad")))
        for bit in ("Priya Nair: nobody on the team owns", "Tom Reyes: interest must be", "Tom Reyes: stance must be",
                    "Tom Reyes: no plan", "Dana Whitlock: resistant but the reason", "Priya Nair: listed twice",
                    "no one listed for: people who do the work; customers; finance"):
            self.assertIn(bit, out)

    def test_resistant_high_power_only_flagged_when_not_managed_closely(self):
        base = dict(name="D", role="Compliance officer sponsor", cares_about="Fears repeat audit finding on refunds",
                    power="high", interest="low", stance="resistant", owner="A")
        self.assertTrue(any("biggest stakeholder risk" in p for p in stake.check([dict(base, engagement="Send newsletter")])))
        self.assertFalse(any("biggest stakeholder risk" in p for p in stake.check([dict(base, engagement="Manage closely weekly")])))


class DecisionLog(unittest.TestCase):
    def test_good(self):
        self.assertEqual(dlog.check(rows("decisions.csv", "good"), TODAY), [])

    def test_bad(self):
        out = "\n".join(dlog.check(rows("decisions.csv", "bad"), TODAY))
        for bit in ("D-003: id used twice", "D-001: the decision is a question", "D-001: fewer than two options",
                    "D-001: reason is too short", "D-001: no one named", "D-001: review date 2026-10-01 has passed",
                    "D-002: date missing", "D-002: superseded by D-009, which is not in the log",
                    "D-003: names D-001 as its replacement", "D-003: proposed 26 days ago"):
            self.assertIn(bit, out)

    def test_superseded_by_an_earlier_decision(self):
        r = [dict(id="A", date="2026-05-01", decision="x y", options="a;b", reason="a b c d e f g", decided_by="p",
                  status="superseded", superseded_by="B"),
             dict(id="B", date="2026-04-01", decision="y", options="a;b", reason="a b c d e f g", decided_by="p", status="decided")]
        self.assertTrue(any("dated earlier" in p for p in dlog.check(r, TODAY)))


class Uat(unittest.TestCase):
    def go(self, which):
        reqs = [r["req_id"] for r in rows("uat_requirements.csv", which)]
        return uat.evaluate(rows("uat_scenarios.csv", which), rows("uat_defects.csv", which), reqs)

    def test_good_is_go_and_open_change_request_does_not_block(self):
        r = self.go("good")
        self.assertEqual(r["call"], "GO")
        self.assertTrue(any("change request" in n for n in r["notes"]))

    def test_bad_is_no_go_with_every_problem(self):
        r = self.go("bad")
        self.assertEqual(r["call"], "NO-GO")
        self.assertEqual(r["blocking"], ["D1 (critical)"])
        out = "\n".join(r["problems"])
        for bit in ("U1: failed with no defect", "U2: marked pass but D1", "U3: points at D9", "U4: result must be",
                    "D3: severity must be", "R3: no UAT scenario"):
            self.assertIn(bit, out)

    def test_minor_open_defects_give_conditions(self):
        sc = [dict(id="U1", requirement="R1", scenario="s", result="pass", defect_id="")]
        df = [dict(defect_id="D1", severity="minor", status="open", kind="defect")]
        self.assertEqual(uat.evaluate(sc, df)["call"], "GO WITH CONDITIONS")

    def test_not_run_scenario_is_no_go(self):
        sc = [dict(id="U1", requirement="R1", scenario="s", result="not run", defect_id="")]
        self.assertEqual(uat.evaluate(sc, [])["call"], "NO-GO")


class ProblemStatement(unittest.TestCase):
    def test_good(self):
        self.assertEqual(pstate.check(read("problem.txt", "good")), [])

    def test_bad(self):
        out = "\n".join(pstate.check(read("problem.txt", "bad")))
        for bit in ("too short", "mentions a solution (system, dashboard, ai)", "no number", "no cause", "no impact",
                    "no success measure", "who struggles"):
            self.assertIn(bit, out)

    def test_lack_of_is_a_solution_in_disguise(self):
        t = ("Account managers struggle to find customers who have not ordered for 90 days because there is a lack of a "
             "proper view of orders, which costs about 12 lost sales a month. We will know it is fixed when fewer than 3 are lost.")
        self.assertTrue(any("solution in disguise" in p for p in pstate.check(t)))

    def test_too_long(self):
        self.assertTrue(any("under 120 words" in p for p in pstate.check("staff struggle because it costs 5. fixed when under 3. " * 15)))


class DomainPacks(unittest.TestCase):
    def test_every_pack_has_the_same_shape_and_is_linked(self):
        pack = SKILLS / "domain-packs"
        skill = (pack / "SKILL.md").read_text()
        files = sorted((pack / "references").glob("*.md"))
        self.assertGreaterEqual(len(files), 8)
        for f in files:
            text = f.read_text()
            self.assertIn(f"references/{f.name}", skill, f"{f.name} not listed in domain-packs/SKILL.md")
            self.assertIn("**Questions to add**", text, f.name)
            self.assertIn("**Traps**", text, f.name)
            self.assertTrue("**Rules to confirm" in text or f.name in {"saas.md", "erp-crm.md", "data-bi.md"}, f.name)


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/askwell.py"), *args], capture_output=True, text=True)

    def test_list_names_every_skill_with_a_script(self):
        out = self.run_cli("list").stdout
        for d in SKILLS.iterdir():
            if (d / "scripts").is_dir():
                self.assertIn(d.name, out)

    def test_run_passes_files_and_exit_code_through(self):
        good = self.run_cli("run", "requirements-writing", str(EX / "good/requirements.txt"))
        bad = self.run_cli("run", "requirements-writing", str(EX / "bad/requirements.txt"))
        self.assertEqual(good.returncode, 0)
        self.assertEqual(bad.returncode, 1)
        self.assertIn("vague word", bad.stdout)

    def test_typo_gets_a_suggestion(self):
        r = self.run_cli("run", "requirement-writing")
        self.assertEqual(r.returncode, 2)
        self.assertIn("requirements-writing", r.stderr)

    def test_skills_lists_all(self):
        out = self.run_cli("skills").stdout
        self.assertIn("ba-start-here", out)
        self.assertIn("domain-packs", out)

    def test_unknown_command(self):
        self.assertEqual(self.run_cli("nonsense").returncode, 2)


class Scope(unittest.TestCase):
    def test_good(self):
        self.assertEqual(scope.check(read("scope.txt", "good")), [])

    def test_bad(self):
        out = "\n".join(scope.check(read("scope.txt", "bad")))
        for bit in ("missing 'Assumptions'", "'Constraints' is empty", "an activity, not a deliverable",
                    "vague ('etc')", "they contradict", "deferred with no date or owner",
                    "does not say who approves", "does not say what is assessed"):
            self.assertIn(bit, out)

    def test_single_exclusion_is_not_enough(self):
        t = read("scope.txt", "good").replace("- Changes to the billing system\n", "").replace("- Chargebacks from card providers\n", "").replace("- Mobile app version, deferred to Q2 2027, owner Head of Finance\n", "")
        self.assertTrue(any("one item" in p for p in scope.check(t)))


class Options(unittest.TestCase):
    def test_good(self):
        self.assertEqual(optn.check(json.loads(read("options.json", "good"))), [])

    def test_bad(self):
        out = "\n".join(optn.check(json.loads(read("options.json", "bad"))))
        for bit in ("no decision", "no deadline", "at least 3 real choices", "no 'do nothing' option",
                    "cost_one_off is a single figure", "no cost_running", "no risks listed", "has no figure",
                    "no benefit stated", "is not one of the options", "reason is too short",
                    "no biggest risk", "no mitigation", "no unknowns"):
            self.assertIn(bit, out)

    def test_sales_pitch_detected(self):
        p = json.loads(read("options.json", "good"))
        for o in p["options"]:
            if o["name"] == "Buy product X":
                o["description"] = "word " * 80
        self.assertTrue(any("sales pitch" in x for x in optn.check(p)))

    def test_do_nothing_must_carry_a_figure(self):
        p = json.loads(read("options.json", "good"))
        p["options"][0]["cost_running"] = "none"
        self.assertTrue(any("not free" in x for x in optn.check(p)))


class RootCause(unittest.TestCase):
    def test_good(self):
        self.assertEqual(rca.check(read("rootcause.txt", "good")), [])

    def test_bad(self):
        out = "\n".join(rca.check(read("rootcause.txt", "bad")))
        for bit in ("no Measure", "Problem has no number", "not numbered", "stopped too early", "blames a person ('careless')",
                    "blames a person ('forgot')", "not a 'because' answer", "0 piece(s) of evidence",
                    "just restates the problem", "changes behaviour, not the process"):
            self.assertIn(bit, out)

    def test_unrelated_root_cause_is_caught(self):
        t = read("rootcause.txt", "good").replace("Root cause: The approval and payment screens share no data, so the amount is retyped",
                                                   "Root cause: Understaffed night shift")
        self.assertTrue(any("does not follow" in p for p in rca.check(t)))


class GapAnalysis(unittest.TestCase):
    def test_good(self):
        self.assertEqual(gapa.check(rows("gaps.csv", "good")), [])

    def test_bad(self):
        out = "\n".join(gapa.check(rows("gaps.csv", "bad")))
        for bit in ("row 1 (process): current or target has no number", "effort must be H, M or L", "no action", "no owner",
                    "same, so there is no gap", "gap 20 does not match target - current = 30", "no gaps looked at for: people, policy"):
            self.assertIn(bit, out)

    def test_close_first_puts_high_impact_low_effort_first(self):
        order = [r["area"] for r in gapa.close_first(rows("gaps.csv", "good"))]
        self.assertEqual(order[:2], ["data", "policy"])
        self.assertEqual(order[-1], "people")

    def test_gap_sign_does_not_matter(self):
        r = [dict(area="process", current="71", target="24", gap="47", impact="H", effort="L", action="a", owner="o")]
        self.assertFalse(any("does not match" in p for p in gapa.check(r)))


class ChangeImpact(unittest.TestCase):
    def test_good(self):
        self.assertEqual(impact.check(rows("impact.csv", "good")), [])

    def test_bad(self):
        out = "\n".join(impact.check(rows("impact.csv", "bad")))
        for bit in ("say what actually changes", "no communication planned", "nobody owns", "high impact with no training",
                    "high impact with no support", "high impact and low readiness", "readiness unknown",
                    "listed twice", "rating must be high, medium or low", "readiness must be"):
            self.assertIn(bit, out)

    def test_attention_order(self):
        order = [r["group"] for r in impact.attention_first(rows("impact.csv", "bad"))]
        self.assertEqual(order[0], "Refund agents")

    def test_nobody_rated_high_is_suspicious(self):
        r = [dict(group="A", what_changes="A small tweak to a form", rating="low", communication="x", training="", support="", readiness="high", owner="o")]
        self.assertTrue(any("no group is rated high" in p for p in impact.check(r)))


class Communication(unittest.TestCase):
    def test_good(self):
        self.assertEqual(comms.check(read("summary.txt", "good")), [])

    def test_bad(self):
        out = "\n".join(comms.check(read("summary.txt", "bad")))
        for bit in ("first 60 words", "no numbers", "no cost or risk", "no date", "jargon 'leverage'", "jargon 'robust'",
                    "sentences average", "over 40 words", "hedges", "acronym PRM", "acronym SLA"):
            self.assertIn(bit, out)

    def test_defined_acronym_is_fine(self):
        t = read("summary.txt", "good") + " The service level agreement (SLA) stays at 95%, so SLA reports are unchanged."
        self.assertNotIn("acronym SLA", " ".join(comms.check(t)))

    def test_too_long(self):
        t = read("summary.txt", "good") + " " + "Another short sentence. " * 80
        self.assertTrue(any("fit in 250" in p for p in comms.check(t)))


class Housekeeping(unittest.TestCase):
    def test_every_script_is_exercised_by_the_worked_example(self):
        runner = (ROOT / "examples/run_all.sh").read_text()
        for script in SKILLS.glob("*/scripts/*.py"):
            self.assertIn(f"{script.parent.parent.name}/scripts/{script.name}", runner,
                          f"{script} is not run by examples/run_all.sh")

    def test_every_script_is_listed_by_the_cli(self):
        cli = load(ROOT / "scripts/askwell.py")
        listed = {p.resolve() for p in cli.checks().values()}
        for script in SKILLS.glob("*/scripts/*.py"):
            self.assertIn(script.resolve(), listed)

    def test_contributing_exists_and_names_the_rules(self):
        text = (ROOT / "CONTRIBUTING.md").read_text()
        for bit in ("Exit 0 when clean", "run_all.sh", "validate_skills.py"):
            self.assertIn(bit, text)


class Elicitation(unittest.TestCase):
    def test_good(self):
        self.assertEqual(elic.check(rows("needs.csv", "good")), [])

    def test_bad(self):
        out = "\n".join(elic.check(rows("needs.csv", "bad")))
        for bit in ("names a technology ('dashboard')", "no source", "not a named person", "a Must that is only assumed",
                    "everyone wants this", "date missing", "id used twice", "status must be", "priority must be",
                    "2 of 3 requirements are only assumed"):
            self.assertIn(bit, out)

    def test_technology_in_a_system_need_is_fine(self):
        r = [dict(id="N", need="Expose an API for approvals", type="system", source="IT", who="Tom Reyes",
                  date="2026-09-01", status="confirmed", priority="should")]
        self.assertEqual(elic.check(r), [])


class Brd(unittest.TestCase):
    def test_good(self):
        self.assertEqual(brd.check(read("brd.md", "good")), [])

    def test_bad(self):
        out = "\n".join(brd.check(read("brd.md", "bad")))
        for bit in ("no 'stakeholders' section", "no 'risks' section", "no 'version history' section", "summary should come first",
                    "objectives have no number", "out of scope", "too short", "sign-off needs", "ID used twice: BR-001",
                    "vague wording", "unfinished placeholder"):
            self.assertIn(bit, out)

    def test_title_mentioning_approval_is_not_the_sign_off(self):
        self.assertNotIn("sign-off needs", " ".join(brd.check(read("brd.md", "good"))))

    def test_requirement_without_priority_is_not_counted(self):
        md = read("brd.md", "good").replace("| Must |", "|  |")
        self.assertTrue(any("no numbered requirements" in p for p in brd.check(md)))


class Workshop(unittest.TestCase):
    def test_good(self):
        self.assertEqual(wshop.check(json.loads(read("workshop.json", "good"))), [])

    def test_bad(self):
        out = "\n".join(wshop.check(json.loads(read("workshop.json", "bad"))))
        for bit in ("not something you can hold", "20 attendees", "adds up to 130 minutes but only 120", "no opening block",
                    "no closing block", "'Discussion': no owner", "100 minutes in one block", "more than 90 minutes without a break",
                    "no silent writing", "no parking lot"):
            self.assertIn(bit, out)

    def test_a_break_resets_the_clock(self):
        p = json.loads(read("workshop.json", "good"))
        p["blocks"] = [b for b in p["blocks"] if b["topic"] != "Break"]
        p["blocks"][2]["minutes"] = 45
        self.assertTrue(any("without a break" in x for x in wshop.check(p)))

    def test_underfilled_agenda(self):
        p = json.loads(read("workshop.json", "good"))
        p["end"] = "15:00"
        self.assertTrue(any("fills" in x for x in wshop.check(p)))

    def test_bad_times(self):
        p = json.loads(read("workshop.json", "good"))
        p["start"] = "nine"
        self.assertTrue(any("HH:MM" in x for x in wshop.check(p)))


class Interview(unittest.TestCase):
    def test_good(self):
        self.assertEqual(interview.check(read("interview.txt", "good")), [])

    def test_bad(self):
        out = "\n".join(interview.check(read("interview.txt", "bad")))
        for bit in ("missing 'Next Interviews'", "Date is not YYYY-MM-DD", "Goal is too short", "not labelled",
                    "more of your own reading", "nothing [seen]", "has no detail", "is a solution",
                    "says no one is finding out", "leading question", "sent back"):
            self.assertIn(bit, out)

    def test_pain_point_with_a_number_is_fine(self):
        t = read("interview.txt", "good").replace("- Managers answer by email at different times, so no one knows what is waiting", "- 3 days")
        self.assertFalse(any("has no detail" in p for p in interview.check(t)))


class Sql(unittest.TestCase):
    HEAD = "-- Question: q\n-- Definition: d\n"

    def test_good(self):
        self.assertEqual(sqlc.check(read("analysis.sql", "good")), [])

    def test_bad(self):
        out = "\n".join(sqlc.check(read("analysis.sql", "bad")))
        for bit in ("no '-- Question:'", "no '-- Definition:'", "SELECT * pulls", "join with no ON", "BETWEEN on dates",
                    "'= NULL' is never true", "LEFT JOIN table", "COUNT on a joined result", "SELECT DISTINCT with a join",
                    "division with no NULLIF", "01/02/2026", "changes data", "no GROUP BY"):
            self.assertIn(bit, out)

    def test_cross_join_is_allowed_when_asked_for(self):
        self.assertEqual(sqlc.check(self.HEAD + "SELECT a.id, b.id FROM a CROSS JOIN b;"), [])

    def test_left_join_condition_in_on_is_fine(self):
        q = self.HEAD + "SELECT a.id, b.x FROM a LEFT JOIN b ON b.a_id = a.id AND b.status = 'x' WHERE a.region = 'N';"
        self.assertFalse(any("LEFT JOIN table" in p for p in sqlc.check(q)))

    def test_comments_do_not_trigger_rules(self):
        q = self.HEAD + "SELECT id FROM t; -- SELECT * and = NULL would be wrong here"
        self.assertEqual(sqlc.check(q), [])

    def test_is_null_test_on_left_join_is_the_anti_join_pattern(self):
        q = self.HEAD + "SELECT a.id FROM a LEFT JOIN b ON b.a_id = a.id WHERE b.a_id IS NULL;"
        self.assertFalse(any("LEFT JOIN table" in p for p in sqlc.check(q)))


class Router(unittest.TestCase):
    def picks(self, text):
        return [s for s, _ in router.route(text)[0]]

    def test_solution_led_request_goes_to_the_problem_first(self):
        self.assertEqual(self.picks("we need a new system for refunds")[0], "problem-statement")

    def test_obvious_requests(self):
        cases = {
            "write user stories for checkout": "user-stories",
            "which vendor should we pick for payroll": "vendor-selection",
            "draw the process as a swimlane": "process-mapping",
            "is it worth doing, what is the payback": "business-case",
            "how do we prioritise the backlog with moscow": "backlog-prioritisation",
            "write the minutes from this transcript": "meeting-minutes",
            "we need a UAT plan before go live": "user-acceptance-testing",
        }
        for text, want in cases.items():
            self.assertIn(want, self.picks(text), text)

    def test_domain_detected(self):
        _, d = router.route("claims handling for an insurance company")
        self.assertIn("insurance", d)
        _, d = router.route("patient records and gdpr")
        self.assertIn("healthcare", d)
        self.assertIn("privacy", d)

    def test_unknown_request_asks_the_one_question(self):
        self.assertEqual(router.route("hello there")[0], [])
        r = subprocess.run([sys.executable, str(SKILLS / "ba-start-here/scripts/route.py"), "hello there"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn(router.QUESTION, r.stdout)

    def test_every_skill_can_be_reached(self):
        names = {d.name for d in SKILLS.iterdir() if d.is_dir()} - {"ba-start-here", "domain-packs"}
        self.assertEqual(names - set(router.RULES), set(), "a skill has no routing words")
        self.assertEqual(set(router.RULES) - names, set(), "routing points at a skill that does not exist")

    def test_every_routing_phrase_finds_its_own_skill(self):
        for skill, phrases in router.RULES.items():
            for ph in phrases:
                self.assertIn(skill, self.picks(ph + " please"), f"'{ph}' should route to {skill}")

    def test_word_start_matching_does_not_fire_inside_words(self):
        self.assertNotIn("sql-for-analysis", self.picks("the squirrel scored a goal"))


class Audit(unittest.TestCase):
    def audit(self, folder, *extra):
        return subprocess.run([sys.executable, str(ROOT / "scripts/askwell.py"), "audit", str(EX.parent / folder), "--today", "2026-10-16", *extra],
                              capture_output=True, text=True)

    def test_good_folder_is_clean(self):
        r = self.audit("refund-approval/good")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0 check(s) found something, 34 clean, 1 skipped", r.stdout)

    def test_bad_folder_exit_code_matches_run_all(self):
        r = self.audit("refund-approval/bad")
        self.assertEqual(r.returncode, 33, r.stdout[-800:])
        self.assertIn("== problem-statement", r.stdout)

    def test_verbose_shows_clean_checks_too(self):
        self.assertIn("(clean)", self.audit("claims-triage/good", "-v").stdout)

    def test_missing_folder_and_missing_argument(self):
        self.assertEqual(self.audit("no-such-folder").returncode, 2)
        r = subprocess.run([sys.executable, str(ROOT / "scripts/askwell.py"), "audit"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_a_folder_with_one_file_runs_one_check(self):
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(EX / "good/problem.txt", d)
            out = subprocess.run([sys.executable, str(ROOT / "scripts/askwell.py"), "audit", d], capture_output=True, text=True).stdout
        self.assertIn("1 clean, 34 skipped", out.replace("0 check(s) found something, ", ""))

    def test_every_check_script_is_in_the_audit_table(self):
        cli = load(ROOT / "scripts/askwell.py")
        table = {(skill, stem) for skill, stem, *_ in cli.AUDIT}
        for script in SKILLS.glob("*/scripts/*.py"):
            self.assertIn((script.parent.parent.name, script.stem), table, f"{script} is not in AUDIT")


class CurrentState(unittest.TestCase):
    def test_good(self):
        self.assertEqual(csa.check(rows("currentstate.csv", "good")), [])

    def test_bad(self):
        out = "\n".join(csa.check(rows("currentstate.csv", "bad")))
        for bit in ("Request: no role", "Request: no system", "volume_per_week is missing", "error rate over 100%",
                    "only an estimate: measure it", "touch_minutes is negative", "evidence must be",
                    "happy path only", "2 of 3 rows are only estimates"):
            self.assertIn(bit, out)

    def test_summary_numbers(self):
        s = csa.summary(rows("currentstate.csv", "good"))
        self.assertIn("19 minutes of work, 2670 minutes of waiting", s[0])
        self.assertIn("Manager approves by email reply", s[1])
        self.assertIn("Agent retypes approved amount", s[2])

    def test_exception_rows_are_not_in_the_normal_path_total(self):
        s = csa.summary(rows("currentstate.csv", "good"))
        self.assertNotIn("1440", s[0])

    def test_negative_rows_are_left_out_of_the_summary(self):
        self.assertNotIn("4 minutes of work", csa.summary(rows("currentstate.csv", "bad"))[0])


class Glossary(unittest.TestCase):
    def test_good_sets_are_clean_including_the_scan(self):
        for ex, doc in (("refund-approval", "requirements.txt"), ("claims-triage", "stories.txt")):
            base = ROOT / "examples" / ex / "good"
            problems, avoid = gloss.check(list(csv.DictReader(io.StringIO((base / "glossary.csv").read_text()))))
            self.assertEqual(problems, [], ex)
            self.assertEqual(gloss.scan((base / doc).read_text(), avoid), [], ex)

    def test_bad(self):
        problems, avoid = gloss.check(rows("glossary.csv", "bad"))
        out = "\n".join(problems)
        for bit in ("Customer: definition is too short", "Customer: no example", "Customer: no non-example", "Customer: no owner",
                    "Refund: the definition is open-ended", "Refunds: defined twice", "'user' is on the avoid list for Customer"):
            self.assertIn(bit, out)

    def test_scan_counts_avoided_words(self):
        _, avoid = gloss.check(rows("glossary.csv", "bad"))
        found = gloss.scan("The client and the client's user asked. A client left.", avoid)
        self.assertIn("'client' appears 3 times; the glossary says use 'Customer'", found)

    def test_definition_that_starts_with_the_term(self):
        r = [dict(term="Claim", definition="Claim is something a customer makes after a loss", avoid="", example="e", non_example="n", owner="o")]
        problems, _ = gloss.check(r)
        self.assertTrue(any("starts with the term" in p for p in problems))


class Agenda(unittest.TestCase):
    def test_good_sets(self):
        for ex in ("refund-approval", "claims-triage"):
            a = json.loads((ROOT / "examples" / ex / "good/agenda.json").read_text())
            self.assertEqual(agenda.check(a), [], ex)

    def test_bad(self):
        out = "\n".join(agenda.check(json.loads(read("agenda.json", "bad"))))
        for bit in ("does not name an outcome", "add up to 35 minutes but the meeting is 30", "no owner to lead it",
                    "only 5 minutes set aside to decide", "outcome must be decide, discuss or inform", "one-way information",
                    "first item should review the actions", "14 attendees for a decision", "less than two days ahead"):
            self.assertIn(bit, out)

    def test_all_inform_should_be_an_email(self):
        a = json.loads(read("agenda.json", "good"))
        for i in a["items"]:
            i["outcome"] = "inform"
        self.assertTrue(any("send it as an email" in p for p in agenda.check(a)))

    def test_missing_pre_read_date(self):
        a = json.loads(read("agenda.json", "good"))
        del a["pre_reads_sent"]
        self.assertTrue(any("no pre-read" in p for p in agenda.check(a)))

    def test_too_many_items(self):
        a = json.loads(read("agenda.json", "good"))
        a["items"] = a["items"] * 2
        self.assertTrue(any("seven" in p for p in agenda.check(a)))


class ProcessCompare(unittest.TestCase):
    def pair(self, ex, which):
        base = ROOT / "examples" / ex / which
        return (base / "process_asis.mmd").read_text(), (base / "process_tobe.mmd").read_text()

    def test_good_pairs_are_no_worse(self):
        for ex in ("refund-approval", "claims-triage"):
            a, b, worse, _, _ = cmp.compare(*self.pair(ex, "good"))
            self.assertEqual(worse, [], ex)

    def test_known_numbers(self):
        a, b, worse, removed, added = cmp.compare(*self.pair("refund-approval", "good"))
        self.assertEqual(a, {"steps": 7, "decisions": 1, "handoffs": 4, "loops": 0, "longest path": 9})
        self.assertEqual(b, {"steps": 6, "decisions": 1, "handoffs": 3, "loops": 0, "longest path": 8})
        self.assertIn("phone customer later", removed)
        self.assertIn("send decision email", added)

    def test_bad_pair_is_worse_on_everything(self):
        _, _, worse, _, _ = cmp.compare(*self.pair("refund-approval", "bad"))
        self.assertEqual(worse, ["steps", "decisions", "handoffs", "loops", "longest path"])

    def test_a_loop_is_counted_once_and_does_not_hang(self):
        m, _ = cmp.measures("flowchart TD\n A([s]) --> B[x]\n B --> C{ok}\n C -- No --> B\n C -- Yes --> D([e])")
        self.assertEqual(m["loops"], 1)
        self.assertEqual(m["longest path"], 4)

    def test_handoffs_need_lanes(self):
        m, _ = cmp.measures("flowchart TD\n A([s]) --> B[x]\n B --> C([e])")
        self.assertEqual(m["handoffs"], 0)


class RaidGrid(unittest.TestCase):
    def test_grid_places_each_risk_by_likelihood_and_impact(self):
        g = raid.grid(rows("raid.csv", "bad"))
        lines = g.splitlines()
        row4 = next(l for l in lines if l.startswith("4"))
        row2 = next(l for l in lines if l.startswith("2"))
        self.assertIn("K1", row4)           # likelihood 4
        self.assertIn("K2", row2)           # likelihood 2
        self.assertNotIn("K3", g)           # unrated
        self.assertNotIn("K4", g)           # closed issue
        self.assertEqual(row4.index("K1") > row2.index("K2"), True)  # K1 has the higher impact so sits further right

    def test_two_risks_in_one_square_are_both_shown(self):
        r = [dict(id="A", type="risk", likelihood="3", impact="3", status="open"),
             dict(id="B", type="risk", likelihood="3", impact="3", status="open")]
        self.assertIn("A,B", raid.grid(r))

    def test_empty_high_squares_are_starred(self):
        g = raid.grid([])
        self.assertIn("*", next(l for l in g.splitlines() if l.startswith("5")))
        self.assertNotIn("*", next(l for l in g.splitlines() if l.startswith("1")))

    def test_cli_grid_flag_keeps_the_exit_code(self):
        r = subprocess.run([sys.executable, str(SKILLS / "raid-log/scripts/raid.py"), str(EX / "bad/raid.csv"), "--today", "2026-10-16", "--grid"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Likelihood", r.stdout)
        ok = subprocess.run([sys.executable, str(SKILLS / "raid-log/scripts/raid.py"), str(EX / "good/raid.csv"), "--today", "2026-10-16", "--grid"],
                            capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0)


class Extras(unittest.TestCase):
    def test_sensitivity(self):
        c = json.loads(read("case.json", "good"))
        s = case.sensitivity(c)
        self.assertLess(s["npv_both"], 0)
        self.assertGreater(s["npv_costs_up"], 0)
        # benefits can fall by exactly the share that makes NPV zero
        shrunk = dict(c, yearly_benefits=[b * (1 - s["benefits_can_fall_by"]) for b in c["yearly_benefits"]])
        self.assertAlmostEqual(case.analyse(shrunk)["npv"], 0, delta=10)  # result is rounded to 4 places

    def test_sensitivity_already_failing(self):
        self.assertIsNone(case.sensitivity(json.loads(read("case.json", "bad")))["benefits_can_fall_by"])

    def test_vendor_robustness(self):
        safe = {"criteria": {"A": 50, "B": 50}, "scores": {"X": {"A": 5, "B": 5}, "Y": {"A": 1, "B": 1}}}
        self.assertEqual(vendor.robustness(safe), [])
        close = json.loads(read("scorecard.json", "good"))
        self.assertTrue(vendor.robustness(close))
        self.assertEqual(vendor.margin(close), 0.1)

    def test_moscow(self):
        shares, warns = rank.moscow(rows("moscow.csv", "good"))
        self.assertEqual(warns, [])
        shares, warns = rank.moscow(rows("moscow.csv", "bad"))
        self.assertAlmostEqual(shares["must"], 14 / 18, places=2)
        self.assertEqual(len(warns), 1)
        with self.assertRaises(ValueError):
            rank.moscow([dict(id="x", moscow="maybe", effort="1")])

    def test_trace_with_tests(self):
        tests = [r["test_id"] for r in rows("tests.csv", "bad")]
        out = trace.check(rows("matrix.csv", "bad"), tests)
        self.assertIn("R3: test T9 does not exist", out)
        self.assertIn("T2: tests nothing (no requirement points at it)", out)
        good = trace.check(rows("matrix.csv", "good"), [r["test_id"] for r in rows("tests.csv", "good")])
        self.assertEqual(good, [])

    def test_lint_new_rules(self):
        out = " ".join(lint.lint("It shall be updated as needed. TBD"))
        for bit in ("pronoun", "passive", "as required/needed", "TBD"):
            self.assertIn(bit, out)


class WorkedExample(unittest.TestCase):
    def run_all(self, which):
        return subprocess.run(["sh", str(ROOT / "examples/run_all.sh"), f"refund-approval/{which}"],
                              capture_output=True, text=True)

    def test_good_example_passes_every_check(self):
        r = self.run_all("good")
        self.assertEqual(r.returncode, 0, r.stdout[-1500:])

    def test_second_example_in_another_field_also_passes_every_check(self):
        r = self.run_all("../claims-triage/good")
        self.assertEqual(r.returncode, 0, r.stdout[-1500:])

    def test_both_examples_have_the_same_files(self):
        a = {p.name for p in (ROOT / "examples/refund-approval/good").iterdir()}
        b = {p.name for p in (ROOT / "examples/claims-triage/good").iterdir()}
        self.assertEqual(a - b - {"conflict.csv", "terms.json"}, set(), "claims-triage is missing files refund-approval has")

    def test_bad_example_trips_every_check(self):
        r = self.run_all("bad")
        self.assertEqual(r.returncode, 33, r.stdout[-1500:])  # all thirty-three gated checks find something


if __name__ == "__main__":
    unittest.main()
