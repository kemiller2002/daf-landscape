#!/usr/bin/env python3
"""Research coverage matrix generator (functional style, stdlib only).

The assessments below are the coordinator's baseline judgements of what the
repository already evidences (2026-11-14). They are NOT independent validation.
"IC" (independently corroborated) is only assigned when the validation register
(data/mission-2026-11-14/validation-register.csv) records a pass for that entity.

Outputs:
  data/mission-2026-11-14/coverage-matrix-entities.csv   (entity x checklist item, long format)
  data/mission-2026-11-14/coverage-summary.json          (proportions by status / segment)
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

STATUS = {
    "NI": "Not investigated",
    "DS": "Discovery started",
    "EC": "Evidence collected",
    "PV": "Partially validated",
    "IC": "Independently corroborated",
    "CE": "Contradictory evidence",
    "IP": "Insufficient public information",
    "RC": "Research completed to current evidence standard",
}

CHECKLIST = (
    ("legal_role", "Legal entity, EIN and role (sponsor / administrator / vendor / distributor)"),
    ("financials", "Latest audited statements or Form 990 reviewed for the relevant period"),
    ("fees", "Published fee schedule / pricing with retrieval date"),
    ("tech_admin", "Technology and administration provider identified with source"),
    ("custody_invest", "Custodian and investment-management arrangement identified"),
    ("distribution", "Distribution partners / channels identified"),
    ("grant_workflow", "Grant approval, vetting and payment workflow documented"),
    ("assurance", "Security assurance (SOC reports) scope documented"),
    ("ownership_funding", "Ownership, funding and acquisitions documented"),
    ("timeline", "Dated historical timeline built"),
    ("ai", "AI claims and evidence of delivery assessed"),
    ("operating_evidence", "Customer / operational performance evidence (turnaround, errors, retention)"),
)

SEGMENT = {
    "national_sponsor": "National / financial-institution-affiliated sponsor",
    "independent_sponsor": "Independent or white-label sponsor",
    "wealth_channel": "Wealth-management distribution channel",
    "tech_admin_vendor": "Technology / administration vendor",
    "infrastructure": "Payments / verification infrastructure",
    "digital_challenger": "Digital-first challenger sponsor/platform",
    "community_faith": "Community / faith / affinity sponsor",
}

# Each tuple: (entity, segment, {item: status}, key evidence files, notes)
# Items not listed default to "NI".
BASELINE = (
    ("Ren (RenPSG)", "tech_admin_vendor",
     dict(legal_role="PV", financials="EC", fees="EC", tech_admin="PV", custody_invest="DS", distribution="PV",
          grant_workflow="EC", assurance="CE", ownership_funding="EC", timeline="DS", ai="DS", operating_evidence="IP"),
     "ren-*.md; audited-revenue-and-client-cohorts; ren-contract-durability-concentration; soc2-assessment",
     "Assurance contradictory: AEF 2025 Type II vs 2026 Type I wording. Ren corporate revenue/ARR not public."),
    ("Renaissance Charitable Foundation (RCF)", "independent_sponsor",
     dict(legal_role="PV", financials="PV", fees="EC", tech_admin="PV", custody_invest="DS", distribution="PV",
          grant_workflow="EC", assurance="NI", ownership_funding="EC", timeline="DS", ai="NI", operating_evidence="IP"),
     "rcf-ren-governance*; ren-five-year-fee-sharing; data/rcf-ren-audited-admin-payments-2020-2024.csv",
     "Audited 2020-2024 payments to Ren documented; signed related-party agreement not public."),
    ("TIFIN Give", "tech_admin_vendor",
     dict(legal_role="EC", financials="IP", fees="EC", tech_admin="EC", custody_invest="DS", distribution="EC",
          grant_workflow="EC", assurance="DS", ownership_funding="DS", timeline="DS", ai="DS", operating_evidence="IP"),
     "ren-tifin-chariot-deep-dive; daf-economics-and-distribution; tax-opportunity-lifecycle",
     "Form ADV 2025 reviewed; AI 'Tax Intelligence' announced, delivery evidence pending."),
    ("GiveClear Foundation", "independent_sponsor",
     dict(legal_role="EC", financials="EC", fees="DS", tech_admin="EC", custody_invest="DS", distribution="EC",
          grant_workflow="DS", assurance="NI", ownership_funding="NI", timeline="DS", ai="NI", operating_evidence="IP"),
     "giveclear-wealth-partner-observations-2025.csv; sponsor-governance-and-fee-transparency",
     "Self-reported partner list; SEI Charitable Fund (Oct 2026) adds a channel."),
    ("Foundation Source", "tech_admin_vendor",
     dict(legal_role="EC", financials="IP", fees="DS", tech_admin="EC", custody_invest="DS", distribution="EC",
          grant_workflow="DS", assurance="NI", ownership_funding="EC", timeline="DS", ai="NI", operating_evidence="IP"),
     "charityvest-foundation-source-tiaa-financial-bridge; expanded-daf-ecosystem",
     "Vennfi (2024) and Giving Place (2025) acquisitions; private company financials not public."),
    ("Charityvest", "digital_challenger",
     dict(legal_role="PV", financials="EC", fees="EC", tech_admin="EC", custody_invest="DS", distribution="EC",
          grant_workflow="EC", assurance="NI", ownership_funding="EC", timeline="DS", ai="NI", operating_evidence="EC"),
     "charityvest-*; challenger-economics; oneascent-onegive",
     "Board overlap with Foundation Source documented; Chariot disbursement transition Aug 2026."),
    ("Chariot", "infrastructure",
     dict(legal_role="EC", financials="IP", fees="EC", tech_admin="EC", custody_invest="NI", distribution="EC",
          grant_workflow="EC", assurance="DS", ownership_funding="DS", timeline="DS", ai="NI", operating_evidence="DS"),
     "ren-tifin-chariot-deep-dive; daf-grant-tracking-payment-rails-comparison; revenue-retention-and-switching",
     "Oct 2026 nonprofit terms 2.9% DAFpay default fee documented."),
    ("Daffy", "digital_challenger",
     dict(legal_role="EC", financials="DS", fees="EC", tech_admin="DS", custody_invest="DS", distribution="DS",
          grant_workflow="DS", assurance="DS", ownership_funding="DS", timeline="NI", ai="NI", operating_evidence="DS"),
     "startups-and-emerging-competitors; challenger-economics",
     "Self-reported $2B assets Sep 2026 (unaudited)."),
    ("Fidelity Charitable", "national_sponsor",
     dict(legal_role="EC", financials="PV", fees="EC", tech_admin="DS", custody_invest="EC", distribution="DS",
          grant_workflow="EC", assurance="DS", ownership_funding="EC", timeline="NI", ai="NI", operating_evidence="DS"),
     "batch-1c-affiliated-provider-fee-tracing; batch-2a; market-demand",
     "Affiliated-provider fee flows traced from audited statements."),
    ("DAFgiving360 (Schwab Charitable)", "national_sponsor",
     dict(legal_role="EC", financials="EC", fees="EC", tech_admin="DS", custody_invest="EC", distribution="DS",
          grant_workflow="EC", assurance="NI", ownership_funding="EC", timeline="DS", ai="NI", operating_evidence="DS"),
     "batch-1d-vanguard-npt-dafgiving360-fee-audit; batch-2a",
     "Disclosure-access gap recorded in batch 1D."),
    ("Vanguard Charitable", "national_sponsor",
     dict(legal_role="EC", financials="PV", fees="EC", tech_admin="DS", custody_invest="EC", distribution="DS",
          grant_workflow="EC", assurance="NI", ownership_funding="EC", timeline="NI", ai="NI", operating_evidence="DS"),
     "vanguard-charitable-economic-and-experience-deep-dive; batch-1d",
     "Embedded investment economics; NPT expense attribution."),
    ("National Philanthropic Trust (NPT)", "independent_sponsor",
     dict(legal_role="EC", financials="EC", fees="DS", tech_admin="PV", custody_invest="DS", distribution="EC",
          grant_workflow="DS", assurance="DS", ownership_funding="EC", timeline="DS", ai="NI", operating_evidence="DS"),
     "national-philanthropic-trust-financial-technology-audit; npt-*.md",
     "Stellar/iPhi and GivingPoint lineage traced; Ren link via primary source."),
    ("American Endowment Foundation (AEF)", "independent_sponsor",
     dict(legal_role="EC", financials="DS", fees="DS", tech_admin="PV", custody_invest="DS", distribution="DS",
          grant_workflow="DS", assurance="CE", ownership_funding="EC", timeline="DS", ai="NI", operating_evidence="EC"),
     "revenue-retention-and-switching; ren-five-year-fee-sharing",
     "Portal migration left two years of directly accessible history; SOC type wording conflict."),
    ("Stellar Technology Solutions / iPhi", "tech_admin_vendor",
     dict(legal_role="EC", financials="IP", fees="DS", tech_admin="EC", custody_invest="NI", distribution="DS",
          grant_workflow="EC", assurance="NI", ownership_funding="DS", timeline="DS", ai="NI", operating_evidence="IP"),
     "ren-iphi-*; npt-givingpoint-iphi-architecture; iphi-175-client-lead",
     "175-client claim is a lead, not verified."),
    ("Givinga", "tech_admin_vendor",
     dict(legal_role="DS", fees="NI", tech_admin="DS", distribution="DS"),
     "expanded-daf-ecosystem", "Thin coverage."),
    ("Edward Jones", "wealth_channel",
     dict(legal_role="EC", financials="NI", fees="EC", tech_admin="EC", custody_invest="DS", distribution="EC",
          grant_workflow="DS", assurance="NI", ownership_funding="NI", timeline="NI", ai="NI", operating_evidence="IP"),
     "edward-jones-ren-*.md",
     "Sponsor RCF + DonorFirstX portal confirmed; private DAF provider unknown; 2021 $2.9B historical only."),
    ("Morgan Stanley (GIFT)", "wealth_channel",
     dict(legal_role="EC", financials="DS", fees="DS", tech_admin="DS", distribution="EC", grant_workflow="NI"),
     "bofa-morgan-stanley-institutional-ren-evidence", "Ren relationship evidence partial."),
    ("Goldman Sachs (two DAF programs)", "wealth_channel",
     dict(legal_role="EC", financials="EC", fees="DS", tech_admin="DS", distribution="EC"),
     "goldman-sachs-two-daf-programs", "Technology provider unresolved."),
    ("Bank of America Charitable Gift Fund", "wealth_channel",
     dict(legal_role="EC", financials="EC", fees="DS", tech_admin="EC", distribution="EC"),
     "bofa-charitable-gift-fund-10k-ren-relationship", "10-K Ren relationship evidence."),
    ("TIAA (Charityvest-sponsored DAF)", "wealth_channel",
     dict(legal_role="EC", fees="EC", tech_admin="EC", distribution="EC", ownership_funding="NI"),
     "charityvest-foundation-source-tiaa-financial-bridge", "Sep 2026 launch; ADV incentive disclosure."),
    ("OneAscent (OneGive)", "wealth_channel",
     dict(legal_role="EC", fees="EC", tech_admin="EC", distribution="EC"),
     "oneascent-onegive-charityvest-disclosed-incentives", "55bps waivable adviser fee."),
    ("SEI (SEI Charitable Fund)", "wealth_channel",
     dict(legal_role="DS", tech_admin="DS", distribution="DS"),
     "startups-and-emerging-competitors", "Announced Oct 28 2026; TIFIN Give + GiveClear."),
    ("Pave Finance", "digital_challenger",
     dict(legal_role="EC", fees="DS", custody_invest="EC", distribution="EC"),
     "pave-*.md", "Market-entry study; investment-management access."),
    ("National Christian Foundation", "community_faith",
     dict(legal_role="DS", financials="DS"), "affinity-dafs-*", "Thin coverage."),
    ("Jewish Communal Fund", "community_faith", dict(legal_role="DS"), "affinity-dafs-*", "Thin coverage."),
    ("Silicon Valley Community Foundation", "community_faith", dict(legal_role="DS"), "expanded-daf-ecosystem",
     "Thin coverage."),
    ("Benevity / workplace processors", "infrastructure", dict(legal_role="DS", tech_admin="DS"),
     "expanded-daf-ecosystem; historical lifecycle", "Processor vs traditional DAF distinction only."),
    ("DAF Direct", "infrastructure", dict(legal_role="DS"), "batch-2b", "Mentioned only."),
    ("Candid / IRS BMF (eligibility data)", "infrastructure",
     dict(legal_role="EC", grant_workflow="EC"), "batch-2b-ren-tifin-chariot-charity-vetting-infrastructure",
     "Eligibility data sources compared; vendor AI not assessed."),
)


# Mission 2026-11-14 research updates (coordinator assessment of the new mission files;
# still not independent validation). Applied on top of BASELINE.
MISSION_UPDATES = {
    "Ren (RenPSG)": dict(timeline="EC", ai="IP", distribution="PV"),
    "Renaissance Charitable Foundation (RCF)": dict(timeline="EC"),
    "TIFIN Give": dict(timeline="EC", ai="EC", ownership_funding="EC"),
    "GiveClear Foundation": dict(timeline="DS", distribution="PV"),
    "Foundation Source": dict(timeline="EC", ownership_funding="PV"),
    "Charityvest": dict(timeline="EC"),
    "Chariot": dict(timeline="EC", ai="EC", ownership_funding="EC", distribution="PV"),
    "Daffy": dict(timeline="EC", ai="EC", ownership_funding="EC", fees="PV"),
    "Fidelity Charitable": dict(timeline="EC", ai="EC", grant_workflow="PV"),
    "DAFgiving360 (Schwab Charitable)": dict(timeline="EC"),
    "Vanguard Charitable": dict(timeline="EC", tech_admin="EC"),
    "National Philanthropic Trust (NPT)": dict(timeline="EC", operating_evidence="EC"),
    "Stellar Technology Solutions / iPhi": dict(timeline="EC", distribution="EC"),
    "Givinga": dict(timeline="DS", legal_role="EC", operating_evidence="EC"),
    "Morgan Stanley (GIFT)": dict(tech_admin="EC", financials="EC"),
    "Bank of America Charitable Gift Fund": dict(fees="EC"),
    "SEI (SEI Charitable Fund)": dict(legal_role="EC", tech_admin="EC", distribution="EC"),
    "National Christian Foundation": dict(legal_role="EC", financials="EC", tech_admin="DS", grant_workflow="DS"),
    "Jewish Communal Fund": dict(financials="EC", grant_workflow="DS"),
    "Silicon Valley Community Foundation": dict(legal_role="EC", financials="EC", tech_admin="DS", grant_workflow="DS"),
    "Benevity / workplace processors": dict(timeline="EC", ai="EC"),
    "Candid / IRS BMF (eligibility data)": dict(ai="DS"),
    "DAF Direct": dict(ownership_funding="DS"),
    "Pave Finance": dict(ownership_funding="IP"),
    "Edward Jones": dict(tech_admin="PV"),
}

MISSION_NEW_ENTITIES = (
    ("Give Interactive", "tech_admin_vendor",
     dict(legal_role="DS", tech_admin="EC", distribution="DS"),
     "mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md",
     "New 2026-11-14: Vanguard Charitable DAF recordkeeping (press release 2025-11-04); Signatry portal; claims $40bn+."),
    ("Endaoment", "independent_sponsor",
     dict(legal_role="EC", tech_admin="DS", distribution="DS"),
     "mission-2026-11-14/ai-native-entrant-simulation.md", "Sponsor-of-record API tiers; custodian list unverified."),
    ("Foundant (CommunitySuite)", "tech_admin_vendor",
     dict(legal_role="EC", distribution="DS", ownership_funding="EC"),
     "mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md", "Claims 700+ community foundations; SmartSimple merger 2024."),
    ("NPact (FIMS / DonorCentral)", "tech_admin_vendor",
     dict(legal_role="DS", ownership_funding="EC"),
     "mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md", "Acquired FIMS/DonorCentral from Blackbaud 2022."),
)


def apply_updates(baseline, updates, new_entities):
    return tuple(
        (e, seg, {**st, **updates.get(e, {})}, files, notes) for e, seg, st, files, notes in baseline
    ) + tuple(new_entities)


def rows(baseline, validated=frozenset()):
    return tuple(
        {
            "entity": entity,
            "segment": SEGMENT[segment],
            "checklist_item": item,
            "checklist_definition": definition,
            "status_code": "IC" if (entity, item) in validated else statuses.get(item, "NI"),
            "status": STATUS["IC" if (entity, item) in validated else statuses.get(item, "NI")],
            "evidence_files": files,
            "notes": notes,
            "assessed_by": "coordinator baseline 2026-11-14 (not independent validation)",
        }
        for entity, segment, statuses, files, notes in baseline
        for item, definition in CHECKLIST
    )


def read_rows(path: Path) -> tuple:
    with path.open(newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def load_validated(directory: Path) -> frozenset:
    """(entity, checklist_item) pairs confirmed by any independent validation register."""
    return frozenset(
        (r.get("entity", ""), r.get("checklist_item", ""))
        for path in sorted(directory.glob("validation-register*.csv"))
        for r in read_rows(path)
        if r.get("validation_result", "").lower() == "confirmed" and r.get("checklist_item")
    )


def summary(records):
    by_status = Counter(r["status_code"] for r in records)
    investigated = sum(v for k, v in by_status.items() if k != "NI")
    advanced = sum(by_status[k] for k in ("PV", "IC", "RC"))
    by_entity = {}
    for r in records:
        by_entity.setdefault(r["entity"], Counter())[r["status_code"]] += 1
    return {
        "entities": len({r["entity"] for r in records}),
        "cells": len(records),
        "status_counts": {STATUS[k]: by_status.get(k, 0) for k in STATUS},
        "share_cells_investigated_any": round(investigated / len(records), 3),
        "share_cells_partially_validated_or_better": round(advanced / len(records), 3),
        "entities_with_majority_not_investigated": sorted(
            e for e, c in by_entity.items() if c["NI"] > len(CHECKLIST) / 2),
        "caveat": "The research universe is incomplete: DAFRC counts ~1,500 sponsors; this matrix covers a "
                  "purposive set of the largest and most strategically relevant entities.",
    }


def write_csv(path: Path, records):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    out = root / "data" / "mission-2026-11-14"
    out.mkdir(parents=True, exist_ok=True)
    records = rows(apply_updates(BASELINE, MISSION_UPDATES, MISSION_NEW_ENTITIES), load_validated(out))
    write_csv(out / "coverage-matrix-entities.csv", records)
    (out / "coverage-summary.json").write_text(json.dumps(summary(records), indent=2))
    print(json.dumps(summary(records), indent=2))
