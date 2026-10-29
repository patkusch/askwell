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
flow = load(SKILLS / "process-mapping/scripts/check.py")
acts = load(SKILLS / "meeting-minutes/scripts/actions.py")
stake = load(SKILLS / "stakeholder-mapping/scripts/check.py")
optn = load(SKILLS / "options-analysis/scripts/check.py")
scope = load(SKILLS / "scope-definition/scripts/check.py")
pstate = load(SKILLS / "problem-statement/scripts/check.py")
uat = load(SKILLS / "user-acceptance-testing/scripts/summary.py")
dlog = load(SKILLS / "decision-log/scripts/check.py")
nfr = load(SKILLS / "nonfunctional-requirements/scripts/check.py")
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

    def test_bad_example_trips_every_check(self):
        r = self.run_all("bad")
        self.assertEqual(r.returncode, 19, r.stdout[-1500:])  # all nineteen gated checks find something


if __name__ == "__main__":
    unittest.main()
