# Grade Math

Grade arithmetic. A weighted average is not the plain average.

## What it computes

- **The weighted truth** - weighted average next to the plain average: scores 90, 80, 70 with weights 50, 30, 20 give 83 against 80.
- **The final-score truth** - the final score that lands a target, given the average on the rest and the final's weight: 85 on the other 60% and a final worth 40% needs 97.5 for 90.
- **The drop truth** - the average before and after the lowest scores are dropped.

Numbers are rounded to hundredths.

## Boundary

Arithmetic only. Grade Math does not know your course's real weights, rounding or drop rules. Check those in your syllabus.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (41 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/grademath/
Repo: https://github.com/iLanis-agent/grademath
