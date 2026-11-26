"""Generate ACT CSV/JSONL outputs (except report) from act_model + act_meta. Run: python3 -I -B gen_outputs.py <out_dir>"""
import csv
import importlib.util
import json
import sys
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HERE = Path(__file__).resolve().parent
M = load("act_model", HERE / "act_model.py")
X = load("act_meta", HERE / "act_meta.py")


def activity_rows():
    typ = M.ARCHETYPES["typical"]
    rows = []
    for act in M.ACTIVITIES:
        md = X.META[act["id"]]
        cat, unit = act["ext"]
        rows.append({
            "activity_id": act["id"], "activity": act["name"], "scope": "per account",
            "why_it_exists": md[0], "trigger": md[1], "frequency_driver": md[2], "frequency_unit": act["freq_unit"],
            "frequency_per_account_year_low": md[3][0], "frequency_per_account_year_base": md[3][1], "frequency_per_account_year_high": md[3][2],
            "frequency_model_typical_conventional": round(act["driver"](typ, "conventional"), 4),
            "frequency_model_typical_ai_native": round(act["driver"](typ, "ai_native"), 4),
            "legally_required": md[4], "legal_basis": md[5], "human_judgment_required": md[6], "preventable": md[7], "eliminable": md[8],
            "deterministic_automation_sufficient": md[9], "ai_adds_value": md[10],
            **{f"minutes_{p}_{l}": act["m"][p][l] for p in M.APPROACHES for l in M.LEVELS},
            "minutes_basis": "expected servicer minutes per occurrence incl. zero-touch occurrences [A]",
            "exception_rate": md[11], "external_cost_per_occurrence_usd": unit, "external_cost_category": cat, "external_cost_note": md[12],
            "sponsor_retained_min_per_occurrence_conv_vs_redesign": f"{act['sponsor'][0]} / {act['sponsor'][1]}",
            "typical_min_per_acct_yr_conventional": round(M.minutes_for(act, typ, "conventional", "base"), 2),
            "typical_min_per_acct_yr_ai_enhanced": round(M.minutes_for(act, typ, "ai_enhanced", "base"), 2),
            "typical_min_per_acct_yr_ai_native": round(M.minutes_for(act, typ, "ai_native", "base"), 2),
            "typical_min_per_acct_yr_elimination": round(M.minutes_for(act, typ, "elimination", "base"), 2),
            "required_controls": md[13], "evidence_ids": ";".join(md[14]), "quality": md[15],
        })
    for s in M.SPONSOR_ACTIVITIES:
        md = X.META[s["id"]]
        rows.append({
            "activity_id": s["id"], "activity": s["name"], "scope": "per sponsor" + (" (one-off)" if s["one_off"] else "-year"),
            "why_it_exists": md[0], "trigger": md[1], "frequency_driver": md[2], "frequency_unit": md[2],
            "frequency_per_account_year_low": md[3][0], "frequency_per_account_year_base": md[3][1], "frequency_per_account_year_high": md[3][2],
            "frequency_model_typical_conventional": "", "frequency_model_typical_ai_native": "",
            "legally_required": md[4], "legal_basis": md[5], "human_judgment_required": md[6], "preventable": md[7], "eliminable": md[8],
            "deterministic_automation_sufficient": md[9], "ai_adds_value": md[10],
            **{f"minutes_{p}_{l}": s["h"][p][l] * 60 for p in M.APPROACHES for l in M.LEVELS},
            "minutes_basis": "minutes per sponsor-year (or per one-off event) [A]" + ("; plus per-account migration minutes " + json.dumps(s.get("per_account_min", {})) if s.get("per_account_min") else ""),
            "exception_rate": md[11], "external_cost_per_occurrence_usd": "", "external_cost_category": "", "external_cost_note": md[12],
            "sponsor_retained_min_per_occurrence_conv_vs_redesign": "",
            "typical_min_per_acct_yr_conventional": "", "typical_min_per_acct_yr_ai_enhanced": "", "typical_min_per_acct_yr_ai_native": "",
            "typical_min_per_acct_yr_elimination": "",
            "required_controls": md[13], "evidence_ids": ";".join(md[14]), "quality": md[15],
        })
    return rows


def approach_rows():
    typ = M.ARCHETYPES["typical"]
    acts = {a["id"]: a for a in M.ACTIVITIES}
    out = []
    for aid, t in X.APPROACH_TEXT.items():
        act = acts[aid]
        mins = {p: round(M.minutes_for(act, typ, p, "base"), 2) for p in M.APPROACHES}
        out.append({"activity_id": aid, "activity": act["name"], "conventional": t[0], "conventional_plus_ai": t[1],
                    "ai_native_redesign": t[2], "elimination": t[3],
                    **{f"typical_min_per_acct_{p}": mins[p] for p in M.APPROACHES},
                    "structural_advantage": t[4], "elimination_legally_financially_sound": t[5],
                    "label": "[A] minutes; approach classification follows repo modal winners (EV-ACT-028, process-economics-summary.md:24-33)"})
    return out


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def write_jsonl(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main(out_dir):
    out = Path(out_dir)
    write_csv(out / "activities.csv", activity_rows())
    write_csv(out / "approaches.csv", approach_rows())
    write_jsonl(out / "evidence.jsonl", [
        {"evidence_id": e[0], "claim": e[1], "value": e[2], "unit": e[3], "source_url_or_path": e[4], "source_type": e[5],
         "filing_period": e[6], "accessed": "2026-11-25", "quality": e[7], "notes": e[8]} for e in X.EVIDENCE])
    write_jsonl(out / "assumptions.jsonl", [
        {"assumption_id": a[0], "statement": a[1], "value": a[2], "unit": a[3], "low": a[4], "high": a[5], "basis": a[6],
         "evidence_ids": a[7], "sensitivity": a[8]} for a in X.ASSUMPTIONS])
    write_jsonl(out / "requirements-candidates.jsonl", X.REQ_CANDIDATES)


if __name__ == "__main__":
    main(sys.argv[1])
