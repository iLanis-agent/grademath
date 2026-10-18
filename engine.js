// Grade Math engine - weighted average, the final score needed, and averages with lowest scores dropped.
// Mirrored by oracle.py; keep the op order identical.
// Numbers are rounded to hundredths on the way in; results come out to hundredths.

function _h(x, msg, min, max, allowZero) {
  if (typeof x !== "number" || !isFinite(x) || x < min || x > max || (!allowZero && x === 0)) throw new Error(msg);
  return Math.floor(x * 100 + 0.5);
}

function _fmt(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  if (frac === 0) return String(whole);
  var f = (frac < 10 ? "0" : "") + frac;
  if (f.charAt(1) === "0") f = f.charAt(0);
  return whole + "." + f;
}

// n/d rounded half up, n >= 0.
function _div(n, d) {
  return Math.floor((2 * n + d) / (2 * d));
}

function _scores(list, lo, what) {
  if (!Array.isArray(list) || list.length < lo || list.length > 20) throw new Error("need " + lo + " to 20 " + what);
  var out = [];
  for (var i = 0; i < list.length; i++) out.push(_h(list[i], "each score must be between 0 and 1000", 0, 1000, true));
  return out;
}

// The weighted truth: weighted average next to the plain average of the same scores.
function weightedTruth(scores, weights) {
  var s = _scores(scores, 1, "scores");
  if (!Array.isArray(weights) || weights.length !== s.length) throw new Error("scores and weights need the same count");
  var w = [];
  for (var i = 0; i < weights.length; i++) w.push(_h(weights[i], "each weight must be above 0 and at most 1000", 0, 1000, false));
  var num = 0, den = 0, sum = 0;
  for (i = 0; i < s.length; i++) { num += s[i] * w[i]; den += w[i]; sum += s[i]; }
  return "Weighted average: " + _fmt(_div(num, den)) + ". The plain average of the same scores is " + _fmt(_div(sum, s.length)) + ".";
}

// The final-score truth: the final that lands a target, given the average so far and the final's weight.
function finalTruth(current, finalWeight, target) {
  var c = _h(current, "current average must be between 0 and 1000", 0, 1000, true);
  if (typeof finalWeight !== "number" || !isFinite(finalWeight) || Math.floor(finalWeight) !== finalWeight || finalWeight < 1 || finalWeight > 99) {
    throw new Error("final weight must be a whole number from 1 to 99");
  }
  var t = _h(target, "target must be between 0 and 1000", 0, 1000, true);
  var rest = 100 - finalWeight;
  var n = t * 100 - c * rest;
  var lead = "With " + _fmt(c) + " on the other " + rest + "% and the final worth " + finalWeight + "%, ";
  if (n < 0) return lead + "the target " + _fmt(t) + " holds even with a final of 0.";
  var need = _div(n, finalWeight);
  return lead + "a final of " + _fmt(need) + " gives " + _fmt(t) + ".";
}

// The drop truth: average before and after the lowest scores are dropped.
function dropTruth(scores, drop) {
  var s = _scores(scores, 2, "scores");
  if (typeof drop !== "number" || !isFinite(drop) || Math.floor(drop) !== drop || drop < 1 || drop > s.length - 1) {
    throw new Error("drop must be a whole number from 1 to one fewer than the scores");
  }
  var sorted = s.slice().sort(function (a, b) { return a - b; });
  var all = 0, kept = 0, i;
  for (i = 0; i < sorted.length; i++) { all += sorted[i]; if (i >= drop) kept += sorted[i]; }
  var what = drop === 1 ? "score" : drop + " scores";
  return "Dropping the lowest " + what + " of " + s.length + ": average goes from " + _fmt(_div(all, s.length)) + " to " + _fmt(_div(kept, s.length - drop)) + ".";
}
