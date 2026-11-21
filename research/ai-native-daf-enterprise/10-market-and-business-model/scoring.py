"""Weighted decision matrix for business models A-D (stdlib only, functional style).

Reads model-scores.csv (1-5 scores, higher is better) and weights.csv, prints
weighted totals and ranks per weight set, and a Dirichlet(1,...,1) Monte Carlo of
rank-first probability over random weights. Scores are judgments with stated
rationale, not measurements; this shows how robust the ranking is to weights.
Usage: python3 -I scoring.py [--samples N] [--seed S]
"""
import csv, random, sys
from collections import Counter
from functools import reduce
from pathlib import Path

HERE = Path(__file__).resolve().parent

def read_scores(path):
    rows = list(csv.DictReader(open(path, newline="")))
    return reduce(lambda acc, r: {**acc, r["model"]: {**acc.get(r["model"], {}), r["criterion"]: int(r["score"])}}, rows, {})

def read_weights(path):
    return {r["weight_set"]: {k: float(v) for k, v in r.items() if k != "weight_set"} for r in csv.DictReader(open(path, newline=""))}

def weighted(scores, weights):
    total = sum(weights.values())
    return {m: round(sum(s[c] * w for c, w in weights.items()) / total, 3) for m, s in scores.items()}

def ranking(totals):
    return sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))

def dirichlet(rng, keys):
    draws = [rng.gammavariate(1.0, 1.0) for _ in keys]
    return dict(zip(keys, draws))

def monte_carlo(scores, keys, n, seed):
    rng = random.Random(seed)
    firsts = Counter(ranking(weighted(scores, dirichlet(rng, keys)))[0][0] for _ in range(n))
    return {m: round(firsts.get(m, 0) / n, 3) for m in scores}

def perturb(scores, model, crit, delta):
    return {m: {c: (max(1, min(5, v + delta)) if (m, c) == (model, crit) else v) for c, v in cs.items()} for m, cs in scores.items()}

def flips(scores, weights):
    base = ranking(weighted(scores, weights))[0][0]
    cells = [(m, c, d) for m, cs in scores.items() for c in cs for d in (-1, 1)]
    return base, [(m, c, d, ranking(weighted(perturb(scores, m, c, d), weights))[0][0]) for m, c, d in cells
                  if ranking(weighted(perturb(scores, m, c, d), weights))[0][0] != base]

def main(argv):
    n = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 20000
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 20261120
    scores, weights = read_scores(HERE / "model-scores.csv"), read_weights(HERE / "weights.csv")
    print("weight_set,rank,model,weighted_score")
    for ws, w in weights.items():
        for i, (m, t) in enumerate(ranking(weighted(scores, w)), 1):
            print(f"{ws},{i},{m},{t}")
    print("\nsingle_score_perturbation(+/-1)_that_changes_rank_first")
    for ws, w in weights.items():
        base, fl = flips(scores, w)
        print(f"{ws}: base_first={base}; flips={len(fl)}: " + "; ".join(f"{m}.{c}{d:+d}->{n}" for m, c, d, n in fl))
    keys = list(next(iter(weights.values())).keys())
    print("\nmonte_carlo_rank_first_probability(n=%d,seed=%d)" % (n, seed))
    for m, p in sorted(monte_carlo(scores, keys, n, seed).items(), key=lambda kv: -kv[1]):
        print(f"{m},{p}")

if __name__ == "__main__":
    main(sys.argv)
