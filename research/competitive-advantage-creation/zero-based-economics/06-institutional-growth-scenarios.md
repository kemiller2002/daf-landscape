# 06. Institutional growth: 0 to 100 customers

**Customers differ in size.** Profiles ([`profiles.csv`](data/inputs/profiles.csv)):

| Profile | Accounts (low/base/high) | Assets per account | Grants per account |
|---|---|---|---|
| XS small community foundation | 25/60/120 | $80k–300k | 3–9 |
| S mid-size community foundation | 150/300/600 | $100k–400k | 3–10 |
| M large community foundation or affinity sponsor | 800/1,500/3,000 | $100k–350k | 4–12 |
| L regional or institution-affiliated sponsor | 3,000/6,000/12,000 | $60k–250k | 5–14 |
| XL national sponsor | 15,000/30,000/60,000 | $40k–200k | 6–12.3 |

The XL grant range tops out at 12.3, Fidelity Charitable's 2025 average grants per account. Community-foundation figures are not public, so those ranges are assumptions anchored to Phase II (5.6–18.5 observed across sponsors).

**Mixes:**
- **mixed:** S M S XS M S L S M XS, first customer a 300-account foundation;
- **small:** all S;
- **tiny:** all XS;
- **anchor:** L first, then mixed.

**Independent variation.** Within each count, four factors vary independently: accounts, assets per account, transactions per account and exception intensity (0.5×/1×/2×). That gives 81 combinations × 4 mixes per count ([`scenario-grid.csv`](data/outputs/scenario-grid.csv), 15,552 rows).

## Echelon Foundry annual cash (base mix, typical contracts)
| Model | 0 | 1 | 2 | 5 | 10 | 25 | 50 | 100 |
|---|---|---|---|---|---|---|---|---|
| L Licensing | $7k | $202k | $233k | $387k | $568k | $1.10M | $2.03M | $3.75M |
| W White-label | $7k | $195k | $220k | $342k | $496k | $904k | $1.62M | $2.95M |
| T Limited operations | $7k | $284k | $395k | $615k | $1.14M | $2.37M | $4.71M | $9.07M |
| F Full service | $7k | $325k | $413k | $633k | $1.24M | $2.57M | $5.11M | $9.97M |
| C Charity intelligence | $17k | $145k | $146k | $148k | $156k | $175k | $207k | $268k |
| M Migration (projects per year) | $4k | $29k | $37k | $83k | $247k | $690k | $1.49M | $3.09M |

Other views are in [`results.md`](data/outputs/results.md):
- §1a: cash if the founder were paid;
- §2: fully loaded;
- §3: tiers 0 and 2.

## Sensitivity to size, volume and exceptions (min / median / max over 81 factor combinations × 4 mixes)
| Model, customers | Min | Median | Max |
|---|---|---|---|
| L, 10 | $562k | $565k | $576k |
| L, 100 | $3.69M | $3.72M | $3.82M |
| F, 10 | $792k | $954k | $3.49M |
| F, 100 | $5.71M | $7.37M | $32.7M |
| C, 100 | $208k | $238k | $342k |

**Licensing cost barely depends on customer size.** The sponsor carries account-driven work, so Echelon Foundry's cost is driven by the number of customers.

**Full-service cost spans more than 4× at the same count.** Exception intensity and customer size drive almost all of it. That is why an asset-based fee is fragile when exception rates are unmeasured.

## Sponsor-borne cost (not in Echelon Foundry cost)
| Customers (mixed) | Licensing | Limited operations | Full service |
|---|---|---|---|
| 1 | $42k | $24k | $19k |
| 10 | $911k | $480k | $390k |
| 100 | $9.1M | $4.8M | $3.9M |

The sponsor-borne cost includes:
- reserved decisions;
- payment rails (about $0.50 per transaction);
- the sponsor's own audit;
- sponsor-side migration;
- under licensing, its own exception work and reconciliation.

## Who performs the 180-day deep review (open decision P3-DEC-MOD005 / OD-CDD-06)
| Allocation | L, 10 customers: EF cash | Sponsor cost | F, 10: EF cash |
|---|---|---|---|
| EF performs (change-driven) | $574k | $907k | $1.24M |
| Sponsor performs (change-driven) | $568k | $911k | $1.24M |
| EF performs (manual 180-day reviews) | **$780k** | $907k | $1.39M |
| Sponsor performs (manual reviews) | $568k | **$1.06M** | $1.24M |

**The allocation is not the lever; the change-driven design is.** With change-driven renewal (OD-CDD-02, approved), the residual reviews cost a few thousand dollars a year whoever performs them. If renewals revert to manual 10-minute reviews:
- at 10 customers, about $210k a year falls on whichever party performs them;
- at 100 customers, about $1.8M a year.

Source: [`deep-review-allocation.csv`](data/outputs/deep-review-allocation.csv).
