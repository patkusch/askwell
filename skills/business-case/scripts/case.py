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


if __name__ == "__main__":
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    print(json.dumps(analyse(json.load(src)), indent=2))
