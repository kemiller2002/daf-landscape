#!/usr/bin/env python3
"""Test the proposed methodology §7a-§7c AI-overlay rules (task b4301-05)
against every existing overlay rating in the quadrant and census data.

Usage: python3 scripts/mission_b4301_05_overlay_rule_test.py . [out_csv]

Inputs are transcribed from the repo documents named in each row's
`source_pointer` (no network access). The census and gap19 labels are read
directly from their CSVs. Functional style, stdlib only.
"""
import csv
import os
import sys
from functools import reduce

RANK = {"None": 0, "GREEN": 1, "AMBER": 2, "RED": 3}
FLAG_TIES = ("T1", "T2", "T3", "T4")  # ties that let an AMBER/RED component count
GREEN_TIES = ("T1",)                  # a GREEN component counts only when live in the scored offering
TIE_TEXT = {
    "T1": "in the scored offering",
    "T2": "shared AI platform or agent channel that reaches the scored offering",
    "T3": "performs the scored offering's own function",
    "T4": "vendor capability tied by a source to the sponsor's program",
    "confined": "source confines it to another product (adjacent)",
    "none": "no source ties it to this entity (entity scope)",
    "not_ai": "not described as AI (automation or navigation)",
    "not_live": "roadmap or announced only (watch)",
    "not_live_in_offering": "configured from the scored offering but not shown live there",
}


def comp(name, level, tie, live=True):
    return {"name": name, "level": level, "tie": tie, "live": live}


def level_of(label):
    head = label.split(" ")[0].split("/")[0].strip().upper().rstrip(".,;")
    return {"GREEN": "GREEN", "AMBER": "AMBER", "RED": "RED"}.get(head, "None")


def counts(c):
    if not c["live"] or c["tie"] in ("not_ai", "not_live"):
        return False
    return c["tie"] in (GREEN_TIES if c["level"] == "GREEN" else FLAG_TIES)


def adjacent(c):
    return c["live"] and c["tie"] == "confined" and c["level"] in ("AMBER", "RED")


def aggregate(components):
    """Rule §7b: most severe counted component; GREEN only if all counted are GREEN."""
    counted = [c for c in components if counts(c)]
    top = reduce(lambda a, c: c["level"] if RANK[c["level"]] > RANK[a] else a, counted, "None")
    levels = sorted({c["level"] for c in counted}, key=lambda l: -RANK[l])
    mixed = len(levels) > 1
    adj = [c["name"] for c in components if adjacent(c)]
    watch = [c["name"] for c in components if c["tie"] == "not_live"]
    return {"level": top, "counted": counted, "mixed": mixed, "adjacent": adj, "watch": watch}


def outcome_label(row, agg):
    gov = row["governing"]
    if row["scope"] in ("product_reading",):
        return row["recorded"]
    qual = row.get("qualifier_if_changed", "")
    base = gov if level_of(gov) == agg["level"] else (agg["level"] + (" " + qual if qual else ""))
    notes = []
    if agg["mixed"]:
        notes.append("mixed: " + "; ".join(c["level"] + " " + c["name"] for c in agg["counted"]))
    if agg["level"] == "None" and agg["adjacent"] and "adjacent" not in base:
        notes.append("adjacent product AMBER: " + "; ".join(agg["adjacent"]))
    return base + (" [" + " | ".join(notes) + "]" if notes else "")


def first_green(row, agg):
    """Rule §7c: returns (eligible, first failing condition)."""
    checks = (
        (row["scope"] == "area_row", "not an A1-A5 area row"),
        (row["version"] >= 1.1, "v1.0 label (no written GREEN test; withdrawn by v1.1)"),
        (len(agg["counted"]) > 0, "no counted AI component ('none' or non-AI automation cannot be GREEN)"),
        (agg["level"] == "GREEN", "a counted component is AMBER or RED" if agg["counted"] else "no GREEN component"),
        (row["two_scorer"], "not reproduced or upheld under the two-scorer rule"),
        ("provisional" not in row["recorded"].lower(), "provisional"),
    )
    failed = [msg for ok, msg in checks if not ok]
    return (not failed, failed[0] if failed else "meets §7c")


def norm(label):
    return "None" if label.strip().lower() in ("none", "none evidenced") else label.strip()


def change(out, ref):
    if norm(out) == norm(ref):
        return "no"
    return "annotation only" if norm(out.split(" [")[0]) == norm(ref) else "yes: " + ref + " -> " + out


def evaluate(row):
    agg = aggregate(row["components"])
    out = outcome_label(row, agg)
    fg_ok, fg_reason = first_green(row, agg)
    ch_rec = change(out, row["recorded"])
    ch_gov = change(out, row["governing"])
    rule_a = {
        "area_row": "area row; components admitted by tie",
        "product_reading": "product-level reading; " + row.get("product_scope", ""),
        "entity_reading": "entity program-level reading; parent or vendor capability enters only on a tie (entity scope)",
    }[row["scope"]]
    single = row["scope"] != "area_row"
    comp_txt = "n/a (single product or entity reading)" if single else "; ".join(
        "%s=%s (%s%s)" % (c["name"], c["level"], TIE_TEXT[c["tie"]], "" if c["live"] else ", not live")
        for c in row["components"]) or "none evidenced"
    counted_txt = "n/a" if row["scope"] != "area_row" else ("; ".join(c["name"] for c in agg["counted"]) or "none")
    rule_b = "own reading kept (§7b(4))" if single else ("level " + agg["level"] + (" (mixed)" if agg["mixed"] else "")
              + ("; adjacent shown" if agg["adjacent"] else "")
              + ("; watch items not counted" if agg["watch"] else ""))
    return {
        "row_id": "", "rating_set": row["set"], "source_pointer": row["src"],
        "area": row["area"], "subject": row["subject"], "recorded_label": row["recorded"],
        "governing_label_now": row["governing"], "scope_class": row["scope"],
        "components_considered": comp_txt, "counted_components": counted_txt,
        "rule_a_scope": rule_a, "rule_b_components": rule_b,
        "rule_c_first_green": ("eligible" if fg_ok else "no: " + fg_reason),
        "proposed_outcome": out, "change_vs_recorded": ch_rec, "change_vs_governing": ch_gov,
        "change_driver": row.get("driver", "none" if ch_gov == "no" else "rule"),
        "note": row.get("note", ""),
    }


# ---------------------------------------------------------------- components
LOUISE = comp("AIP01 TIFIN Louise", "AMBER", "T1")
LOUISE_GC = comp("AIP01 TIFIN Louise", "AMBER", "T4")
DAFFY = [comp("AIP02 Daffy MCP", "AMBER", "T1"), comp("AIP03 Daffy Quick Donate", "AMBER", "T1")]
FID_VA = comp("AIP04 Fidelity Virtual Assistant", "None", "not_ai")
FIA = comp("AIP11 Foundant Fia (beta)", "AMBER", "T2")
SS_FOUNDANT = comp("AIP12 SmartSimple Application Analysis", "GREEN", "not_live_in_offering")
RULES = comp("rule-based instant approval (RCF policy)", "None", "not_ai")
GIFT_AI = comp("AIP06 Chariot Gift Processing AI", "AMBER", "confined")
MCP_CONF = comp("AIP07 Chariot MCP", "AMBER", "confined")
MCP_DAFPAY = comp("AIP07 Chariot MCP (get_dafpay_components)", "AMBER", "T2")
AGENT_API = comp("agent-capable API, no AI product", "None", "not_ai")
CANDID = [comp("AIP22 Candid MCP", "AMBER", "T2"), comp("AIP23 Candid assistant (beta)", "AMBER", "T2")]
BENEVITY = comp("Benevity Match Assurance", "AMBER", "T3")
GOODSTACK = comp("Goodstack 'AI-powered automation' claim", "AMBER", "T1")
BB = [comp("Blackbaud Copilot FE NXT technical preview (2024-10-07)", "AMBER", "T1"),
      comp("AIP17 Blackbaud Development Agent (RE NXT)", "AMBER", "confined"),
      comp("AIP18 Chat for Blackbaud AI etc. (RE NXT)", "AMBER", "confined"),
      comp("AIP16 YourCause summaries (GrantsConnect)", "GREEN", "confined")]
FS_ROADMAP = comp("AIP09 Foundation Source AI roadmap", "None", "not_live")
GIVE_INT = comp("'AI tools' integration claim", "None", "not_ai")
GIVINGA = comp("AIP10 Givinga automation claim (not labelled AI)", "None", "not_ai")
MS_AUTO = comp("MS GIFT 'Automated' vetting (nature undisclosed)", "AMBER", "T1")
NCF_AI = comp("NCF AI search (ncfgiving.com/ai-search, 2026-08-12)", "AMBER", "T1")
SF = comp("AIP24 Salesforce Agentforce Nonprofit", "AMBER", "none")

V10 = "research/mission-2026-11-14/quadrant-calibration.md §5"
V10P = "research/mission-2026-11-14/quadrant-A1-rationale.md (overlay table)"
V11B = "research/mission-2026-11-14/quadrant-v11-blind-and-calibration.md §6 (adjudication table)"
V11C = "research/mission-2026-11-14/quadrant-v11-blind-and-calibration.md §5"
V12 = "research/mission-2026-11-14/quadrant-v12-targeted-rescore.md §4"
CEN = "data/mission-2026-11-14/philanthropy-ai-products-2026.csv"
G19 = "data/mission-2026-11-14/ai-coverage-20-entities-2026-11-19.csv"

CHARIOT_DISB_NOTE = ("Help page (accessed 2026-11-20): connector 'is built for Chariot's Gift Processing platform. "
                     "It also surfaces DAFpay components'; Disbursements not named. No AI in the grant or payment "
                     "decision path (A2-A5 rationale §4). Endaoment precedent (v1.1 §6): an agent-capable API is not AI. "
                     "Downgrade needs adjudication at the next re-score")
NCF_NOTE = ("New evidence after v1.2 (gap19-ai-coverage S18; page re-read 2026-11-20: 'Explore trusted NCF resources "
            "through an AI-powered search experience'). Fidelity's Virtual Assistant is counted on Fidelity's A1 and "
            "A3 rows, so parity puts NCF's own AI search on NCF's rows")


def area(set_, src, area_, subject, recorded, governing, components, version, two_scorer, **kw):
    return dict(set=set_, src=src, area=area_, subject=subject, recorded=recorded, governing=governing,
                components=components, version=version, two_scorer=two_scorer, scope="area_row", **kw)


def v10(area_, subject, recorded, governing, components, **kw):
    return area("v1.0 consensus (superseded)", V10, area_, subject, recorded, governing, components, 1.0, True, **kw)


def v11(area_, subject, label, components, governing=None, **kw):
    return area("v1.1 consensus", V11C, area_, subject, label, governing or label, components, 1.1, True, **kw)


V10_OTHERS = [("A1", "NPact"), ("A1, A4", "Givinga"), ("A3", "NPT"), ("A1, A3", "NCF"), ("A1", "SVCF"),
              ("A3", "Vanguard Charitable"), ("A3, A4", "DAFgiving360"), ("A3", "Goldman Sachs PF"),
              ("A3", "Morgan Stanley GIFT"), ("A3", "BofA Charitable Gift Fund"), ("A2", "PayPal Grant Payments"),
              ("A2", "Fidelity Charitable EFT"), ("A2", "DAF Direct"), ("A2, A4", "Every.org"), ("A5", "IRS baseline")]


def v10_other(a, s):
    special = {
        "Givinga": ([GIVINGA], "None", {}),
        "NCF": ([NCF_AI, SF], "None", {"qualifier_if_changed": "(low)", "driver": "new evidence (gap19 S18) admitted by §7a",
                                         "note": NCF_NOTE}),
        "SVCF": ([SF], "None", {}),
        "Morgan Stanley GIFT": ([MS_AUTO], "AMBER (provisional)", {"note": "Governing label is v1.2. Not labelled AI; "
                                "§7c bars GREEN for non-AI automation. Inconsistent with Givinga's similar claim (None)"}),
        "DAF Direct": ([comp("AIP04 Fidelity Virtual Assistant", "None", "none")], "None", {}),
        "Fidelity Charitable EFT": ([comp("AIP04 Fidelity Virtual Assistant", "None", "none")], "None", {}),
    }
    comps, gov, kw = special.get(s, ([], "None", {}))
    return v10(a, s, "None", gov, comps, **kw)


AREA_ROWS = [
    v10("A1", "TIFIN Give", "AMBER (high)", "AMBER (RED-boundary)", [LOUISE]),
    v10("A3", "GiveClear", "AMBER (high)", "AMBER (RED-boundary)", [LOUISE_GC]),
    v10("A4", "Daffy", "AMBER", "AMBER", DAFFY),
    v10("A5", "Benevity validation", "AMBER / at risk", "AMBER (provisional)", [BENEVITY],
        note="Governing label from wave 21 correction in quadrant-v11-rescore.md"),
    v10("A1", "Foundant CommunitySuite", "AMBER", "AMBER", [FIA, SS_FOUNDANT],
        note="Application Analysis is configured from CommunitySuite but not shown live there (wave 42A), so the GREEN "
             "component is not counted; if shown live the label becomes AMBER (mixed), never GREEN"),
    v10("A1", "Give Interactive", "AMBER-unverified", "None", [GIVE_INT]),
    v10("A1", "Foundation Source", "WATCH", "None", [FS_ROADMAP]),
    v10("A5", "Goodstack", "Unverified; consistent in design", "AMBER", [GOODSTACK]),
    v10("A1, A3, A4", "Fidelity Charitable", "GREEN", "None (inform-only)", [FID_VA],
        note="§7c: v1.0 GREEN withdrawn by v1.1; not a precedent"),
    v10("A1", "Ren", "GREEN / none", "None", [RULES], note="§7c: 'none' cannot be GREEN"),
    v10("A2", "Ren Rapid Disbursement Engine", "GREEN / none", "None", [RULES], note="§7c: 'none' cannot be GREEN"),
    v10("A3", "Renaissance Charitable Foundation", "GREEN / none", "None", [RULES], note="§7c: 'none' cannot be GREEN"),
    v10("A3", "AEF", "GREEN / none", "None", [RULES], note="§7c: 'none' cannot be GREEN"),
    v10("A2", "Chariot Disbursements", "Consistent", "AMBER", [GIFT_AI, MCP_CONF, AGENT_API],
        qualifier_if_changed="(watch: agent-capable API)", note=CHARIOT_DISB_NOTE),
    v10("A2", "Chariot DAFpay", "Consistent", "AMBER", [MCP_DAFPAY, GIFT_AI, AGENT_API]),
    v10("A5", "Chariot verification", "Consistent", "None", [GIFT_AI, MCP_CONF]),
    v10("A4", "Endaoment", "Consistent", "None (watch: agent-capable API)", [AGENT_API]),
    v10("A5", "Candid", "Consistent (read-only)", "AMBER (low)", CANDID),
    v10("A1", "Blackbaud Financial Edge NXT", "None for FE NXT", "AMBER", BB,
        note="Holds only on the FE NXT Copilot technical preview (wave 28); the RE NXT agents are adjacent. "
             "If the preview is not current the row becomes None [adjacent product AMBER]"),
] + [v10_other(a, s) for a, s in V10_OTHERS] + [
    area("v1.0 primary scorer A1 (superseded)", V10P, "A1", "Fidelity Charitable", "GREEN", "None (inform-only)",
         [FID_VA], 1.0, False, note="§7c: single-scorer v1.0 label"),
    area("v1.0 primary scorer A1 (superseded)", V10P, "A1", "Ren", "GREEN/none", "None", [RULES], 1.0, False),
    area("v1.1 blind scorer (adjudicated)", V11B, "A1, A3, A4", "Fidelity Charitable", "GREEN", "None (inform-only)",
         [FID_VA], 1.1, False, note="§7c: blind GREEN not upheld by consensus"),
    area("v1.1 blind scorer (adjudicated)", V11B, "A5", "Candid", "GREEN", "AMBER (low)", CANDID, 1.1, False,
         note="Read-only documented by a third party, not Candid"),
    area("v1.1 blind scorer (adjudicated)", V11B, "A4", "Endaoment", "AMBER", "None (watch: agent-capable API)",
         [AGENT_API], 1.1, False),
    area("v1.1 blind scorer (adjudicated)", V11B, "A1", "Foundant CommunitySuite", "None", "AMBER",
         [FIA, SS_FOUNDANT], 1.1, False),
    # v1.1 consensus, A1
    v11("A1", "Fidelity Charitable (in-house)", "None (inform-only)", [FID_VA]),
    v11("A1", "Ren", "None", [RULES]),
    v11("A1", "NCF (sponsor-built, Salesforce)", "None", [NCF_AI, SF], qualifier_if_changed="(low)",
        driver="new evidence (gap19 S18) admitted by §7a", note=NCF_NOTE),
    v11("A1", "TIFIN Give", "AMBER (RED-boundary)", [LOUISE]),
    v11("A1", "Foundant CommunitySuite", "AMBER", [FIA, SS_FOUNDANT]),
    v11("A1", "Foundation Source", "None", [FS_ROADMAP]),
    v11("A1", "Blackbaud Financial Edge NXT", "AMBER", BB,
        note="Basis should cite the FE NXT Copilot preview, not the adjacent RE NXT agents"),
    v11("A1", "SVCF (sponsor-built, Salesforce)", "None", [SF]),
    v11("A1", "Give Interactive", "None", [GIVE_INT]),
    v11("A1", "Givinga", "None", [GIVINGA]),
    v11("A1", "NPact", "None", []),
    # A2
    v11("A2", "PayPal Grant Payments", "None", []),
    v11("A2", "Fidelity Charitable EFT", "None", [comp("AIP04 Fidelity Virtual Assistant", "None", "none")]),
    v11("A2", "Chariot Disbursements", "AMBER", [GIFT_AI, MCP_CONF, AGENT_API],
        qualifier_if_changed="(watch: agent-capable API)", note=CHARIOT_DISB_NOTE),
    v11("A2", "Chariot DAFpay", "AMBER", [MCP_DAFPAY, GIFT_AI, AGENT_API],
        note="Holds: the MCP 'also surfaces DAFpay components' (get_dafpay_components)"),
    v11("A2", "Every.org", "None", []),
    v11("A2", "Ren Rapid Disbursement Engine", "None", [RULES]),
    v11("A2", "DAF Direct", "None", [comp("AIP04 Fidelity Virtual Assistant", "None", "none")]),
    # A3
    v11("A3", "NPT", "None", []),
    v11("A3", "Renaissance Charitable Foundation", "None", [RULES]),
    v11("A3", "Vanguard Charitable", "None", []),
    v11("A3", "Fidelity Charitable", "None (inform-only)", [FID_VA]),
    v11("A3", "DAFgiving360", "None", []),
    v11("A3", "NCF", "None", [NCF_AI], qualifier_if_changed="(low)",
        driver="new evidence (gap19 S18) admitted by §7a", note=NCF_NOTE),
    v11("A3", "AEF", "None", []),
    v11("A3", "Goldman Sachs Philanthropy Fund", "None", []),
    v11("A3", "Morgan Stanley GIFT", "None", [MS_AUTO], governing="AMBER (provisional)",
        note="Governing label is v1.2"),
    v11("A3", "Charityvest (adviser programs)", "None", [comp("AIP09 Foundation Source AI roadmap (owner)", "None", "none")]),
    v11("A3", "GiveClear", "AMBER (RED-boundary)", [LOUISE_GC]),
    v11("A3", "BofA Charitable Gift Fund", "None", []),
    # A4
    v11("A4", "Fidelity Charitable (direct)", "None (inform-only)", [FID_VA]),
    v11("A4", "DAFgiving360 (direct)", "None", []),
    v11("A4", "Daffy", "AMBER", DAFFY),
    v11("A4", "Charityvest (direct)", "None", []),
    v11("A4", "Endaoment", "None (watch: agent-capable API)", [AGENT_API]),
    v11("A4", "Every.org", "None", []),
    v11("A4", "Givinga consumer accounts", "None", [GIVINGA]),
    # A5
    v11("A5", "IRS BMF / Pub 78 / TEOS", "None", []),
    v11("A5", "Candid", "AMBER (low)", CANDID),
    v11("A5", "Chariot verification", "None", [GIFT_AI, MCP_CONF]),
    v11("A5", "Benevity validation", "RED (provisional)", [BENEVITY], governing="AMBER (provisional)",
        note="v1.1 table not yet corrected; wave 21 correction (quadrant-v11-rescore.md) governs"),
    v11("A5", "Goodstack", "AMBER", [GOODSTACK]),
    # v1.2 targeted
    area("v1.2 targeted", V12, "A3", "BofA Charitable Gift Fund", "none evidenced", "None", [], 1.2, True),
    area("v1.2 targeted", V12, "A3", "Morgan Stanley GIFT", "AMBER (provisional)", "AMBER (provisional)",
         [MS_AUTO], 1.2, True, note="Not labelled AI; §7c bars GREEN; inconsistent with Givinga (None) for a similar claim"),
    area("v1.2 targeted", V12, "A3", "Goldman Sachs PF", "none evidenced", "None", [], 1.2, True),
    area("v1.2 targeted", V12, "A3", "NCF", "none evidenced", "None", [NCF_AI], 1.2, True,
         qualifier_if_changed="(low)", driver="new evidence (gap19 S18) admitted by §7a", note=NCF_NOTE),
    area("v1.2 targeted", V12, "A1", "NCF", "none evidenced", "None", [NCF_AI, SF], 1.2, True,
         qualifier_if_changed="(low)", driver="new evidence (gap19 S18) admitted by §7a", note=NCF_NOTE),
]

# census product rows: (id, expected label, product scope under §7a)
CENSUS_SCOPE = {
    "AIP01": "TIFIN Give product; counted in TIFIN Give A1 (T1) and GiveClear A3 (T4)",
    "AIP02": "Daffy product; counted in Daffy A4 (T1)",
    "AIP03": "Daffy product; counted in Daffy A4 (T1)",
    "AIP04": "Fidelity Charitable; not described as AI, so not a counted component",
    "AIP05": "Endaoment; no AI product",
    "AIP06": "outside A1-A5 (Chariot Gift Processing); adjacent to Chariot Disbursements, DAFpay and verification",
    "AIP07": "outside A1-A5 (built for Gift Processing); counted in Chariot DAFpay A2 via get_dafpay_components (T2); adjacent to Disbursements and verification",
    "AIP08": "Ren; none found",
    "AIP09": "Foundation Source; roadmap only (watch, not counted)",
    "AIP10": "Givinga; automation not labelled AI",
    "AIP11": "Foundant vendor-wide AI platform; counted in Foundant CommunitySuite A1 (T2)",
    "AIP12": "outside A1-A5; configured from CommunitySuite but not shown live there, so not a counted GREEN component; Foundant vendor aggregate would be AMBER (mixed)",
    "AIP13": "outside A1-A5; Fluxx vendor aggregate with AIP14 would be AMBER (mixed); not a first GREEN",
    "AIP14": "outside A1-A5",
    "AIP15": "outside A1-A5",
    "AIP16": "outside A1-A5 (GrantsConnect, not FE NXT); not a counted component of Blackbaud FE NXT A1; not a first GREEN",
    "AIP17": "outside A1-A5 (RE NXT); adjacent to Blackbaud FE NXT A1",
    "AIP18": "outside A1-A5 (RE NXT); adjacent to Blackbaud FE NXT A1",
    "AIP19": "outside A1-A5", "AIP20": "outside A1-A5", "AIP21": "outside A1-A5",
    "AIP22": "Candid product; counted in Candid A5 (T2)",
    "AIP23": "Candid product; counted in Candid A5 (T2)",
    "AIP24": "outside A1-A5; vendor evidence, not tied to NCF or SVCF programs (entity scope)",
    "AIP25": "outside A1-A5", "AIP26": "outside A1-A5", "AIP27": "outside A1-A5",
    "AIP28": "outside A1-A5", "AIP29": "outside A1-A5", "AIP30": "outside A1-A5 (ratings site, not eligibility data)",
}

G19_NOTE = {
    "National Christian Foundation": "Own AI search; feeds NCF A1 and A3 rows under §7a (see NCF rows)",
    "SEI (SEI Charitable Fund)": "TIFIN Louise not tied to SEI's program: entity scope holds",
    "Morgan Stanley (GIFT)": "Differs from v1.2 AMBER (provisional), which rests on non-AI 'Automated' vetting; both stand",
}


def census_rows(root):
    rows = list(csv.DictReader(open(os.path.join(root, CEN), encoding="utf-8")))
    return [dict(set="census (product readings)", src=CEN + " " + r["product_id"], area="outside" if
                 CENSUS_SCOPE[r["product_id"]].startswith("outside") else "product of A1-A5 provider",
                 subject=r["product_id"] + " " + r["vendor"].split(" (")[0] + ": " + r["product_name"][:60],
                 recorded=r["ai_overlay"].replace(" [V wave 42A]", ""), governing=r["ai_overlay"].replace(" [V wave 42A]", ""),
                 components=[], version=1.1, two_scorer=False, scope="product_reading",
                 product_scope=CENSUS_SCOPE[r["product_id"]],
                 note="product row keeps its own reading (§7b)") for r in rows]


def g19_rows(root):
    rows = list(csv.DictReader(open(os.path.join(root, G19), encoding="utf-8")))
    return [dict(set="gap19 AI coverage (entity readings)", src=G19, area="entity", subject=r["entity"],
                 recorded=r["ai_overlay"], governing=r["ai_overlay"], components=[], version=1.1, two_scorer=False,
                 scope="entity_reading", note=G19_NOTE.get(r["entity"], "parent/owner capability not tied (entity scope)"
                                                            if "outside" in r["ai_overlay"] or "Owner" in r["notes"]
                                                            or "Platform" in r["notes"] else "")) for r in rows]


def entity_eval(row):
    """Entity readings keep their recorded label: §7a(4) adds no tie that is not already documented."""
    base = evaluate(dict(row, scope="product_reading", product_scope=""))
    return dict(base, scope_class="entity_reading",
                rule_a_scope="entity program-level reading; parent or vendor capability enters only on a tie (entity scope)",
                rule_c_first_green="no: not an A1-A5 area row")


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    out = argv[2] if len(argv) > 2 else os.path.join(root, "data/mission-2026-11-14/overlay-rule-test-2026-11-20.csv")
    area_eval = [evaluate(r) for r in AREA_ROWS]
    cen_eval = [evaluate(r) for r in census_rows(root)]
    g_eval = [entity_eval(r) for r in g19_rows(root)]
    allrows = [dict(e, row_id="OT%03d" % (i + 1)) for i, e in enumerate(area_eval + cen_eval + g_eval)]
    fields = ["row_id", "rating_set", "source_pointer", "area", "subject", "recorded_label", "governing_label_now",
              "scope_class", "components_considered", "counted_components", "rule_a_scope", "rule_b_components",
              "rule_c_first_green", "proposed_outcome", "change_vs_recorded", "change_vs_governing", "change_driver", "note"]
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        list(map(w.writerow, allrows))
    tally = lambda key, pred: sum(1 for r in allrows if pred(r[key]))
    by_set = reduce(lambda acc, r: dict(acc, **{r["rating_set"]: acc.get(r["rating_set"], 0) + 1}), allrows, {})
    print("rows", len(allrows))
    print("by set", by_set)
    print("first-GREEN eligible", tally("rule_c_first_green", lambda v: v == "eligible"))
    print("GREEN-labelled rows", tally("recorded_label", lambda v: level_of(v) == "GREEN"))
    print("change vs governing: yes", tally("change_vs_governing", lambda v: v.startswith("yes")),
          "annotation", tally("change_vs_governing", lambda v: v == "annotation only"))
    print("change vs recorded: yes", tally("change_vs_recorded", lambda v: v.startswith("yes")),
          "annotation", tally("change_vs_recorded", lambda v: v == "annotation only"))
    list(map(lambda r: print(" ", r["row_id"], r["rating_set"], "|", r["subject"], "|", r["change_vs_governing"],
                             "|", r["change_driver"]),
             [r for r in allrows if r["change_vs_governing"] != "no"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
