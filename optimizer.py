"""AI Optimizer - Q15: AI Tutor Safeguards Optimizer | LearnLoop
Scans the one constraint that matters and returns the best setting.
Needs backend.py in the same folder. Run: python optimizer.py
"""
import json
from backend import *  # engine, input models and PRESET


def best_settings():
    opts = [Opt(name=o[0], ceil=o[1], scale=o[2], value=o[3]) for o in PRESET["opts"]]
    best = None
    for pct in range(50, 201, 5):  # total budget from 50% to 200% of the input
        budget = PRESET["bud"] * pct / 100
        r = engine_c(C(budget=budget, options=opts))
        net = r["total_value"] - PRESET["uc"] * budget
        if best is None or net > best[0]:
            best = (net, pct, budget, r)
    net, pct, budget, r = best
    return {"setting": "total budget (" + PRESET["unit"] + ")", "best_value": budget, "percent_of_input": pct,
            "net_value": net, "allocation": r["allocation"],
            "message": "Above this budget the next unit earns less than it costs."}


if __name__ == "__main__":
    print(json.dumps(best_settings(), indent=2, ensure_ascii=False))
