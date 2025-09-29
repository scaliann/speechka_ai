from math import log
from typing import Dict, List, Tuple

EPS = 1e-9


def aggregate_diagnosis(
    items: Dict[int, dict],
    use_log_product: bool = True,
) -> Dict[str, str | float]:
    """
    items: {idx: {"filename": str, "probs": {"healthy": float, "burr": float, "lisp": float, "lisp_burr": float}}}
    returns:
      {"top_label": str, "p_healthy": float, "p_lisp": float, "p_burr": float, "confidence": float}
    """

    per_file = []
    for _, rec in items.items():
        p = rec["probs"]
        p_lisp = p.get("lisp", 0.0) + 0.5 * p.get("lisp_burr", 0.0)
        p_burr = p.get("burr", 0.0) + 0.5 * p.get("lisp_burr", 0.0)
        p_healthy = p.get("healthy", 0.0)
        per_file.append({"healthy": p_healthy, "lisp": p_lisp, "burr": p_burr})

    agg = {"healthy": 0.0, "lisp": 0.0, "burr": 0.0}
    if use_log_product:
        for c in agg:
            agg[c] = sum(log(x[c] + EPS) for x in per_file)
        import math

        m = max(agg.values())
        exps = {c: math.exp(agg[c] - m) for c in agg}
        s = sum(exps.values())
        probs = {c: exps[c] / s for c in agg}
    else:
        n = len(per_file) or 1
        probs = {c: sum(x[c] for x in per_file) / n for c in agg}

    p_healthy = probs["healthy"]
    p_lisp = probs["lisp"]
    p_burr = probs["burr"]

    top_label, p_top = max((("lisp", p_lisp), ("burr", p_burr)), key=lambda t: t[1])
    sorted_vals = sorted([p_healthy, p_lisp, p_burr], reverse=True)
    confidence = sorted_vals[0] - sorted_vals[1]

    if p_healthy >= 0.65 and max(p_lisp, p_burr) <= 0.35:
        top_label = "healthy"

    return {
        "top_label": top_label,
        "p_healthy": round(p_healthy, 3),
        "p_lisp": round(p_lisp, 3),
        "p_burr": round(p_burr, 3),
        "confidence": round(confidence, 3),
    }
