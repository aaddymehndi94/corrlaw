#!/usr/bin/env python3
"""Analytical sanity example only. This is NOT the CorrLaw research experiment."""
import json
import math
import os
from fractions import Fraction
from pathlib import Path


def calculate():
    points = [(math.cos(2*math.pi*i/256), math.sin(2*math.pi*i/256)) for i in range(256)]
    error = max(abs((u*u + 2*v*v) - (1 + v*v)) for u, v in points)
    mean_u = sum(u for u, _ in points)/len(points)
    mean_v = sum(v for _, v in points)/len(points)
    covariance = sum((u-mean_u)*(v-mean_v) for u, v in points)/len(points)
    u, v = Fraction(0), Fraction(1, 2)
    f, g = u*u + 2*v*v, 1 + v*v
    assert error < 1e-12
    assert abs(covariance) < 1e-12
    assert f == Fraction(1, 2) and g == Fraction(5, 4)
    return {"kind": "analytical_sanity_only", "novel_research_result": False,
            "ring_max_disagreement": error, "symmetric_grid_covariance": covariance,
            "off_ring_true": str(f), "off_ring_alternative": str(g),
            "physical_prior": "No additional boundary-value prior supplied to learner.",
            "warning": "The formulas were supplied to this test; it discovers nothing."}


if __name__ == "__main__":
    data = calculate()
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if os.environ.get("CORRLAW_RESULT_DIR"):
        output = Path(os.environ["CORRLAW_RESULT_DIR"]) / "sanity.json"
        output.write_text(text, encoding="utf-8")
    print(text, end="")
