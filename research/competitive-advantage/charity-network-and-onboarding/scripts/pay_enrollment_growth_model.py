#!/usr/bin/env python3
"""Grant-triggered e-payment enrollment growth model (agent PAY, 2026-11-26).

Pure, deterministic expected-value model. Stdlib only. I/O only in main().

Question: if every grant to a not-yet-enrolled charity carries an enrollment
invitation (email + QR/registration code on the check stub) that converts with
probability p, how fast does a sponsor's grant flow (by count and by dollars)
become electronic, and how much does starting with charities already enrolled
at a networked partner (CNV-EXP-002) help?

Closed form per recipient r with grant arrival rate lam_r (grants / year),
pre-enrolled probability e0_r and per-invitation conversion p (Poisson thinning):
    P_r(t) = 1 - (1 - e0_r) * exp(-p * lam_r * t)
Grant-weighted electronic share at time t = sum(lam_r * P_r(t)) / sum(lam_r)
Dollar-weighted share                    = sum(usd_r * P_r(t)) / sum(usd_r)

Inputs: data/workflow-innovation/sponsor-recipient-edges-fy2023.csv in the
daf-landscape repo (IRS Form 990 Schedule I, FY2023, top-50 sponsors; recipients
receiving > $5,000 from a sponsor are itemised). Everything else is an explicit,
labelled ASSUMPTION in PARAMS and is varied in the scenario grid.

Usage:
  python3 -I pay_enrollment_growth_model.py <daf-landscape repo root> > out.csv
"""
from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Mapping, Sequence

EDGES = "data/workflow-innovation/sponsor-recipient-edges-fy2023.csv"

# Sponsors resembling the CNV-ECO-004 entry segment (advisor-distributed / mid-size national).
SPONSORS = (("8", "American Endowment Foundation"),
            ("19", "Raymond James Charitable Endowment Fund"),
            ("46", "T. Rowe Price Program for Charitable Giving"))

# VERIFIED-FACT anchor: AEF reported 109,708 grants for 2024 (AEF DAFs: Impact by State V3.4),
# against 12,491 itemised FY2023 recipients -> 8.78 grants per itemised recipient.
GRANTS_PER_ITEMISED_RECIPIENT = 109_708 / 12_491

PARAMS = {
    # ASSUMPTION: share of a sponsor's grant COUNT going to itemised (> $5k) recipients.
    "share_grants_itemised": (0.4, 0.6, 0.8),
    # ASSUMPTION: grants per un-itemised (tail) recipient per year, and their average size (USD).
    "tail_grants_per_recipient": 1.5,
    "tail_avg_grant_usd": 1_000.0,
    # ASSUMPTION: grant count per itemised recipient proportional to dollars ** beta.
    "beta": (0.3, 0.5, 0.7),
    # ASSUMPTION: probability an invitation attached to one grant results in enrollment before payment.
    "p_convert": (0.10, 0.25, 0.40),
}

# ASSUMPTION: share of recipients already enrolled at a supported networked partner at go-live,
# by how many top-50 sponsors funded them in FY2023 (proxy for institutional DAF exposure).
COVERAGE = {
    "none":            {"n6": 0.00, "n2_5": 0.00, "n1": 0.00, "tail": 0.00},
    "one_partner":     {"n6": 0.20, "n2_5": 0.08, "n1": 0.03, "tail": 0.02},
    "two_partners":    {"n6": 0.45, "n2_5": 0.20, "n1": 0.08, "tail": 0.05},
}

MONTHS = (0, 3, 6, 12, 24, 36)
THRESHOLDS = (0.50, 0.67, 0.80, 0.90)


@dataclass(frozen=True)
class Recipient:
    lam: float      # grants per year
    usd: float      # dollars per year
    tier: str       # n6 | n2_5 | n1 | tail
    count: int = 1  # identical recipients represented by this row (tail is one aggregated row)


def read_edges(path: str) -> list[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def sponsor_counts(edges: Iterable[Mapping]) -> Counter:
    return Counter(e["recipient_key"] for e in edges)


def tier_of(n: int) -> str:
    return "n6" if n >= 6 else ("n2_5" if n >= 2 else "n1")


def build_population(edges: Sequence[Mapping], nspons: Counter, rank: str,
                     share_itemised: float, beta: float) -> tuple[Recipient, ...]:
    mine = [e for e in edges if e["sponsor_rank"] == rank]
    usd = [float(e["amount_usd"]) for e in mine]
    total_grants = len(mine) * GRANTS_PER_ITEMISED_RECIPIENT
    itemised_grants = total_grants * share_itemised
    weights = [u ** beta for u in usd]
    k = itemised_grants / sum(weights)
    itemised = tuple(Recipient(max(1.0, w * k), u, tier_of(nspons[e["recipient_key"]]))
                     for w, u, e in zip(weights, usd, mine))
    tail_grants = total_grants - itemised_grants
    n_tail = max(1, round(tail_grants / PARAMS["tail_grants_per_recipient"]))
    lam_tail = tail_grants / n_tail
    tail = (Recipient(lam_tail, lam_tail * PARAMS["tail_avg_grant_usd"], "tail", n_tail),)
    return itemised + tail


def p_enrolled(r: Recipient, e0: Mapping[str, float], p: float, years: float) -> float:
    return 1.0 - (1.0 - e0[r.tier]) * math.exp(-p * r.lam * years)


def shares(pop: Sequence[Recipient], e0: Mapping[str, float], p: float, years: float) -> tuple[float, float, float]:
    probs = [p_enrolled(r, e0, p, years) for r in pop]
    g = sum(r.count * r.lam * q for r, q in zip(pop, probs)) / sum(r.count * r.lam for r in pop)
    d = sum(r.count * r.usd * q for r, q in zip(pop, probs)) / sum(r.count * r.usd for r in pop)
    n = sum(r.count * q for r, q in zip(pop, probs)) / sum(r.count for r in pop)
    return g, d, n


def months_to(pop, e0, p, target: float, horizon_months: int = 120) -> int | None:
    """Smallest whole month at which the grant-weighted share reaches target (share is monotone in t)."""
    ok = lambda m: shares(pop, e0, p, m / 12)[0] >= target
    if not ok(horizon_months):
        return None
    lo, hi = 0, horizon_months
    while lo < hi:
        mid = (lo + hi) // 2
        lo, hi = (lo, mid) if ok(mid) else (mid + 1, hi)
    return lo


def rows_for(edges, nspons, rank, name) -> list[dict]:
    out = []
    for s_it, beta, p, cov in product(PARAMS["share_grants_itemised"], PARAMS["beta"],
                                      PARAMS["p_convert"], COVERAGE):
        pop = build_population(edges, nspons, rank, s_it, beta)
        grants_yr = sum(r.count * r.lam for r in pop)
        base = dict(sponsor_rank=rank, sponsor=name, share_grants_itemised=s_it, beta=beta,
                    p_convert=p, partner_coverage=cov, recipients_modelled=sum(r.count for r in pop),
                    grants_per_year=round(grants_yr))
        for m in MONTHS:
            g, d, n = shares(pop, COVERAGE[cov], p, m / 12)
            out.append({**base, "row_type": "trajectory", "month": m,
                        "grant_share_electronic": round(g, 4), "dollar_share_electronic": round(d, 4),
                        "recipient_share_enrolled": round(n, 4),
                        "cumulative_grants_processed": round(grants_yr * m / 12),
                        "threshold": "", "months_to_threshold": ""})
        for th in THRESHOLDS:
            mt = months_to(pop, COVERAGE[cov], p, th)
            out.append({**base, "row_type": "threshold", "month": "", "grant_share_electronic": "",
                        "dollar_share_electronic": "", "recipient_share_enrolled": "",
                        "cumulative_grants_processed": "" if mt is None else round(grants_yr * mt / 12),
                        "threshold": th, "months_to_threshold": "" if mt is None else mt})
    return out


def main(argv: list[str]) -> None:
    root = argv[1] if len(argv) > 1 else "."
    edges = read_edges(f"{root}/{EDGES}")
    nspons = sponsor_counts(edges)
    rows = [r for rank, name in SPONSORS for r in rows_for(edges, nspons, rank, name)]
    w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)


if __name__ == "__main__":
    main(sys.argv)
