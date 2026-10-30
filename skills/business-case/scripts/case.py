#!/usr/bin/env python3
"""Work out NPV, payback, ROI and IRR for a business case.

Input (JSON file or stdin):
{"discount_rate": 0.08, "upfront_cost": 100000,
 "yearly_benefits": [40000, 50000, 50000], "yearly_costs": [5000, 5000, 5000]}
Year 0 is the upfront cost. Years 1..n use the lists.
"""
import json
import sys


def cash_flows(case):
    ben, cost = case["yearly_benefits"], case["yearly_costs"]
    if len(ben) != len(cost):
        raise ValueError("yearly_benefits and yearly_costs must be the same length")
    return [-case["upfront_cost"]] + [b - c for b, c in zip(ben, cost)]


def npv(rate, flows):
    return sum(f / (1 + rate) ** t for t, f in enumerate(flows))


def irr(flows):
    """Rate at which NPV is zero, or None if the flows never change sign."""
    if not (any(f < 0 for f in flows) and any(f > 0 for f in flows)):
        return None
    lo, hi = -0.99, 10.0
    if npv(lo, flows) * npv(hi, flows) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(lo, flows) * npv(mid, flows) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def payback_years(flows):
    """Years until the running total turns positive (fractional), or None."""
    total = 0.0
    for t, f in enumerate(flows):
        prev = total
        total += f
        if t > 0 and total >= 0 > prev:
            return t - 1 + (-prev / f)
    return None


def analyse(case):
    flows = cash_flows(case)
    rate = case["discount_rate"]
    spend = case["upfront_cost"] + sum(case["yearly_costs"])
    gain = sum(case["yearly_benefits"])
    return {
        "cash_flows": flows,
        "npv": round(npv(rate, flows), 2),
        "irr": None if irr(flows) is None else round(irr(flows), 4),
        "payback_years": None if payback_years(flows) is None else round(payback_years(flows), 2),
        "roi": round((gain - spend) / spend, 4) if spend else None,
        "total_benefit": gain,
        "total_cost": spend,
    }


def sensitivity(case, swing=0.3):
    """NPV if benefits fall, costs rise, or both by `swing`, and how far benefits
    can fall before the case stops paying (NPV = 0)."""
    rate = case["discount_rate"]

    def run(bf, cf):
        c = dict(case)
        c["upfront_cost"] = case["upfront_cost"] * cf
        c["yearly_benefits"] = [b * bf for b in case["yearly_benefits"]]
        c["yearly_costs"] = [x * cf for x in case["yearly_costs"]]
        return round(npv(rate, cash_flows(c)), 2)

    pv_b = sum(b / (1 + rate) ** t for t, b in enumerate(case["yearly_benefits"], 1))
    pv_c = case["upfront_cost"] + sum(x / (1 + rate) ** t for t, x in enumerate(case["yearly_costs"], 1))
    return {
        "swing": swing,
        "npv_benefits_down": run(1 - swing, 1),
        "npv_costs_up": run(1, 1 + swing),
        "npv_both": run(1 - swing, 1 + swing),
        "benefits_can_fall_by": None if pv_b <= pv_c else round(1 - pv_c / pv_b, 4),  # None: already below break-even
    }


def compare(named_cases):
    """named_cases: {name: case dict}. Returns rows sorted by NPV, best first."""
    rows = []
    for name, c in named_cases.items():
        a = analyse(c)
        rows.append({"option": name, "npv": a["npv"], "payback_years": a["payback_years"], "roi": a["roi"], "total_cost": a["total_cost"]})
    return sorted(rows, key=lambda r: -r["npv"])


if __name__ == "__main__" and "--compare" in sys.argv:
    files = [a for a in sys.argv[1:] if a != "--compare"]
    rows = compare({f.rsplit("/", 1)[-1].removesuffix(".json"): json.load(open(f)) for f in files})
    print(f"{'option'.ljust(24)}{'NPV'.rjust(12)}{'payback (yrs)'.rjust(15)}{'ROI'.rjust(9)}")
    for r in rows:
        pb = "never" if r["payback_years"] is None else f"{r['payback_years']:.1f}"
        print(f"{r['option'].ljust(24)}{r['npv']:>12,.0f}{pb.rjust(15)}{r['roi']:>9.0%}")
    print(f"Best on NPV: {rows[0]['option']}")
    sys.exit(0)

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--sensitivity"]
    src = open(args[0]) if args else sys.stdin
    data = json.load(src)
    out = analyse(data)
    if "--sensitivity" in sys.argv:
        out["sensitivity"] = sensitivity(data)
    print(json.dumps(out, indent=2))
