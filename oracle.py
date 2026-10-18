#!/usr/bin/env python3
# Grade Math oracle - mirrors engine.js.
import json, math

def _h(x, msg, lo, hi, allow_zero):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < lo or x > hi or (not allow_zero and x == 0):
        raise ValueError(msg)
    return math.floor(x * 100 + 0.5)

def _fmt(h):
    whole, frac = divmod(h, 100)
    if frac == 0:
        return str(whole)
    f = f"{frac:02d}"
    if f[1] == "0":
        f = f[0]
    return f"{whole}.{f}"

def _div(n, d):
    return (2 * n + d) // (2 * d)

def _scores(lst, lo, what):
    if not isinstance(lst, list) or len(lst) < lo or len(lst) > 20:
        raise ValueError(f"need {lo} to 20 {what}")
    return [_h(x, "each score must be between 0 and 1000", 0, 1000, True) for x in lst]

def weighted_truth(scores, weights):
    s = _scores(scores, 1, "scores")
    if not isinstance(weights, list) or len(weights) != len(s):
        raise ValueError("scores and weights need the same count")
    w = [_h(x, "each weight must be above 0 and at most 1000", 0, 1000, False) for x in weights]
    num = sum(a * b for a, b in zip(s, w)); den = sum(w); tot = sum(s)
    return f"Weighted average: {_fmt(_div(num, den))}. The plain average of the same scores is {_fmt(_div(tot, len(s)))}."

def final_truth(current, final_weight, target):
    c = _h(current, "current average must be between 0 and 1000", 0, 1000, True)
    if isinstance(final_weight, bool) or not isinstance(final_weight, (int, float)) or not math.isfinite(final_weight) or math.floor(final_weight) != final_weight or final_weight < 1 or final_weight > 99:
        raise ValueError("final weight must be a whole number from 1 to 99")
    t = _h(target, "target must be between 0 and 1000", 0, 1000, True)
    fw = int(final_weight)
    rest = 100 - fw
    n = t * 100 - c * rest
    lead = f"With {_fmt(c)} on the other {rest}% and the final worth {fw}%, "
    if n < 0:
        return lead + f"the target {_fmt(t)} holds even with a final of 0."
    return lead + f"a final of {_fmt(_div(n, fw))} gives {_fmt(t)}."

def drop_truth(scores, drop):
    s = _scores(scores, 2, "scores")
    if isinstance(drop, bool) or not isinstance(drop, (int, float)) or not math.isfinite(drop) or math.floor(drop) != drop or drop < 1 or drop > len(s) - 1:
        raise ValueError("drop must be a whole number from 1 to one fewer than the scores")
    d = int(drop)
    srt = sorted(s)
    allv = sum(srt); kept = sum(srt[d:])
    what = "score" if d == 1 else f"{d} scores"
    return f"Dropping the lowest {what} of {len(s)}: average goes from {_fmt(_div(allv, len(s)))} to {_fmt(_div(kept, len(s) - d))}."

FNS = {"weightedTruth": weighted_truth, "finalTruth": final_truth, "dropTruth": drop_truth}

CASES = [
    ("weightedTruth", [[90, 80, 70], [50, 30, 20]]), ("weightedTruth", [[85], [10]]), ("weightedTruth", [[100, 0], [1, 1]]),
    ("weightedTruth", [[70, 90], [3, 1]]), ("weightedTruth", [[85.5, 92.25], [0.5, 1.5]]), ("weightedTruth", [[0, 0], [1, 2]]),
    ("weightedTruth", [[1000], [1000]]), ("weightedTruth", [[], []]), ("weightedTruth", [[90, 80], [50]]),
    ("weightedTruth", [[90, 80], [50, 0]]), ("weightedTruth", [[90, -1], [50, 50]]), ("weightedTruth", [[90, 1001], [50, 50]]),
    ("weightedTruth", [[90, 80], [50, 1001]]), ("weightedTruth", [[1] * 21, [1] * 21]), ("weightedTruth", [[1] * 20, [1] * 20]),
    ("finalTruth", [85, 40, 90]), ("finalTruth", [90, 20, 70]), ("finalTruth", [50, 50, 100]), ("finalTruth", [80, 1, 80]),
    ("finalTruth", [80, 99, 80]), ("finalTruth", [0, 25, 60]), ("finalTruth", [72.5, 30, 80]), ("finalTruth", [85, 40, 85]),
    ("finalTruth", [85, 0, 90]), ("finalTruth", [85, 100, 90]), ("finalTruth", [85, 33.5, 90]), ("finalTruth", [-1, 40, 90]),
    ("finalTruth", [85, 40, 1001]), ("finalTruth", [1001, 40, 90]),
    ("dropTruth", [[60, 80, 90, 100], 1]), ("dropTruth", [[60, 80, 90, 100], 2]), ("dropTruth", [[70, 70], 1]),
    ("dropTruth", [[100, 50, 75], 1]), ("dropTruth", [[100, 50, 75], 3]), ("dropTruth", [[100, 50, 75], 0]),
    ("dropTruth", [[100], 1]), ("dropTruth", [[100, 50, 75], 1.5]), ("dropTruth", [[10.5, 20.25, 30], 1]),
    ("dropTruth", [[100, 101, 5], 1]), ("dropTruth", [[1] * 21, 1]), ("dropTruth", [[5, 1, 4, 2, 3], 2]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
