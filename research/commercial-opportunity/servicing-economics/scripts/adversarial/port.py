"""Pure-function Python port of Economics.evaluate (ServicingEconomics F#) for adversarial magnitude checks.
Mirrors Parameters.fs values for archetypes, sponsor activities and Model B. Not a replacement for the F# model."""
import math
from dataclasses import dataclass, replace
from typing import Tuple

APPROACHES = ("conv", "enh", "nat", "elim")
# name, share, balance, minutes(4), external(4), payments(4), decShare
ARCH = (
    ("inactive", 0.2, 20000, (15.8, 7.3, 3, 2.6), (4.97, 5.01, 5.01, 5), (0.72, 0.72, 0.72, 0.39), 0.176),
    ("small_recurring", 0.2, 8000, (168.9, 70.5, 21.5, 16.2), (6.63, 7.02, 6.97, 6.82), (11.08, 11.08, 11.08, 6.57), 0.242),
    ("typical", 0.4, 150000, (220.2, 101, 38, 27.3), (8.16, 9.07, 8.99, 8.67), (25.43, 25.43, 25.43, 15.94), 0.244),
    ("high_frequency", 0.07, 400000, (832.8, 376.4, 133.6, 94.6), (16.76, 20.07, 19.74, 18.36), (91.65, 91.65, 91.65, 50.04), 0.242),
    ("high_value", 0.1, 3e6, (464.3, 232.2, 105, 74.7), (25.7, 28.28, 28.05, 27.53), (54.21, 54.21, 54.21, 38.6), 0.26),
    ("complex_asset", 0.03, 1.5e6, (1010.2, 618.7, 359, 166), (357.26, 358.91, 358.64, 358.29), (40.43, 40.43, 40.43, 30), 0.333),
)
MIX_BAL = sum(a[1] * a[2] for a in ARCH)
SPONSOR_MIN = {"conv": 48000.0, "enh": 33000.0, "nat": 19440.0, "elim": 19440.0}
PH = 1520.0
OPS_H = 99478.0 / PH


@dataclass(frozen=True)
class Org:
    core: Tuple[Tuple[float, float], ...]  # (loaded, servicing share)
    nonpersonnel: float
    steps: Tuple[Tuple[str, float, float, float], ...]  # (driver, free, size, cost)
    min_added: float
    dec_share: float = 0.10
    ph: float = PH
    hourly: float = OPS_H


STEPS_AB = (("fte", 4.0, 6.0, 149810.0), ("sponsors", 4.0, 8.0, 188958.0), ("sponsors", 3.0, 8.0, 127440.0),
            ("accounts", 5000.0, 15000.0, 110662.0), ("assets", 1e9, 1e15, 121848.0))
MODEL_B = Org(core=((200142.0, 0.05), (222482.0, 0.0), (188958.0, 0.0), (183365.0, 0.3), (99478.0, 0.8)),
              nonpersonnel=631048.0 + 115814.0, steps=STEPS_AB, min_added=1.0)


def ceil_steps(v, free, size):
    return 0.0 if size <= 0 else math.ceil(max(0.0, v - free) / size - 1e-9)


def evaluate(org, ap, bps, sponsors, asset_factor=1.0, minutes_factor=1.0, per_acct_floor=0.0,
             payments_pass=False, dec_mode="model"):
    """sponsors: tuple of (accounts, avg_balance). Returns dict. dec_mode 'model' = F# rule; 'none' = no peak cost."""
    i = APPROACHES.index(ap)
    rev = hours = ext = dec = assets = accts = 0.0
    for n, b in sponsors:
        scale = b / MIX_BAL
        for _, sh, bal, mins, ex, pay, ds in ARCH:
            k = n * sh
            fee = max(bal * scale * asset_factor * bps / 1e4, per_acct_floor)
            rev += k * fee
            hours += k * mins[i] * minutes_factor / 60
            dec += k * mins[i] * ds * minutes_factor / 60
            ext += k * (ex[i] + (0 if payments_pass else pay[i]))
            assets += k * bal * scale * asset_factor
        hours += SPONSOR_MIN[ap] * minutes_factor / 60
        dec += SPONSOR_MIN[ap] * org.dec_share * minutes_factor / 60
        accts += n
    core_h = sum(s * org.ph for _, s in org.core)
    added = max(org.min_added, ceil_steps(hours, core_h, org.ph))
    added_cost = added * org.ph * org.hourly
    monthly_cap = (core_h + added * org.ph) / 12
    peak = max(0.0, dec - monthly_cap) * org.hourly if dec_mode == "model" else 0.0
    drv = {"fte": added, "sponsors": len(sponsors), "accounts": accts, "assets": assets}
    step = sum(ceil_steps(drv[d], f, s) * c for d, f, s, c in org.steps)
    core = sum(l for l, _ in org.core)
    sponsor_cost = 12000.0 * len(sponsors)
    total = ext + added_cost + peak + core + org.nonpersonnel + step + sponsor_cost
    return {"rev": rev, "total": total, "profit": rev - total, "margin": (rev - total) / rev if rev else float("nan"),
            "hours": hours, "added": added, "peak": peak, "step": step, "ext": ext, "assets": assets, "accts": accts,
            "dec": dec, "monthly_cap": monthly_cap}


def equal(n, total_assets, b):
    return tuple((total_assets / b / n, b) for _ in range(n))
