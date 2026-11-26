"""P-B4013-03-02: validate the draft open DAF grant record test vectors against schema-v0.1.json.

Usage: python3 -I scripts/mission_validate_grant_record.py . [CACHE_LOG ...]
  root       repo root ('.')
  CACHE_LOG  optional log.jsonl files written by the robots-respecting fetcher
             (scratchpad q1303/std/log.jsonl, q1332/web/log.jsonl). Each line maps a URL
             to a cached file. When given, every source_snippet in a vector's
             field_provenance is checked verbatim (whitespace-normalised; HTML reduced to text)
             against the cached copy of its source_url.

What it checks
  1. The schema uses only the JSON Schema 2020-12 keywords this validator implements.
  2. A self-test of the validator on small hand-made cases.
  3. Every standards/daf-grant-record/vectors/*.json validates (expect=valid) or fails
     (expect=invalid) as declared; for invalid vectors each expected (instance_path, keyword)
     error must be among the errors found.
  4. Provenance: exact/renamed values equal the record value; transformed values with a named
     transform are recomputed; not_available paths are absent from the record.
Exit status 0 only if everything passes. Stdlib only, pure functions, no mutable global state.

Draft, unendorsed research output.
"""
import glob
import html
import json
import os
import re
import sys
from decimal import Decimal
from functools import reduce

SCHEMA_PATH = "standards/daf-grant-record/schema-v0.1.json"
VECTOR_GLOB = "standards/daf-grant-record/vectors/*.json"
ANNOTATIONS = frozenset({"$schema", "$id", "$comment", "$defs", "title", "description", "default", "examples"})
APPLICATORS = frozenset({"type", "enum", "const", "pattern", "minLength", "maxLength", "minItems", "maxItems",
                         "uniqueItems", "required", "properties", "additionalProperties", "items",
                         "allOf", "anyOf", "oneOf", "not", "if", "then", "else", "$ref"})
SUPPORTED = ANNOTATIONS | APPLICATORS


# ---------------------------------------------------------------- JSON helpers

def json_type_ok(name, x):
    return {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "boolean": lambda v: isinstance(v, bool),
        "null": lambda v: v is None,
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    }[name](x)


def canon(x):
    """Canonical text form so that equality follows JSON (true != 1, key order ignored)."""
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def json_equal(a, b):
    return canon(a) == canon(b)


def pointer_get(doc, pointer):
    """Resolve a JSON pointer ('' = whole document). Returns (found, value)."""
    parts = [p.replace("~1", "/").replace("~0", "~") for p in pointer.split("/")[1:]] if pointer else []
    def step(acc, key):
        found, node = acc
        if not found:
            return acc
        if isinstance(node, dict):
            return (key in node, node.get(key))
        if isinstance(node, list) and key.isdigit() and int(key) < len(node):
            return (True, node[int(key)])
        return (False, None)
    return reduce(step, parts, (True, doc))


def child(path, key):
    return f"{path}/{key}"


# ---------------------------------------------------------------- validator (keyword subset)

def err(path, keyword, message):
    return ((path, keyword, message),)


def validate(schema, inst, root, path=""):
    """Return a tuple of (instance_path, keyword, message) errors. Empty tuple = valid."""
    if schema is True:
        return ()
    if schema is False:
        return err(path, "false", "schema is false")
    return tuple(e for kw, val in schema.items() if kw in APPLICATORS and kw not in ("then", "else")
                 for e in KEYWORDS[kw](val, schema, inst, root, path))


def k_type(val, _s, inst, _r, path):
    names = val if isinstance(val, list) else [val]
    return () if any(json_type_ok(n, inst) for n in names) else err(path, "type", f"expected {val}")


def k_enum(val, _s, inst, _r, path):
    return () if any(json_equal(inst, v) for v in val) else err(path, "enum", f"{canon(inst)} not in enum")


def k_const(val, _s, inst, _r, path):
    return () if json_equal(inst, val) else err(path, "const", f"{canon(inst)} != {canon(val)}")


def k_pattern(val, _s, inst, _r, path):
    return () if not isinstance(inst, str) or re.search(val, inst) else err(path, "pattern", f"{inst[:40]!r} !~ {val}")


def k_min_length(val, _s, inst, _r, path):
    return () if not isinstance(inst, str) or len(inst) >= val else err(path, "minLength", f"length {len(inst)} < {val}")


def k_max_length(val, _s, inst, _r, path):
    return () if not isinstance(inst, str) or len(inst) <= val else err(path, "maxLength", f"length {len(inst)} > {val}")


def k_min_items(val, _s, inst, _r, path):
    return () if not isinstance(inst, list) or len(inst) >= val else err(path, "minItems", f"{len(inst)} < {val}")


def k_max_items(val, _s, inst, _r, path):
    return () if not isinstance(inst, list) or len(inst) <= val else err(path, "maxItems", f"{len(inst)} > {val}")


def k_unique_items(val, _s, inst, _r, path):
    if not val or not isinstance(inst, list):
        return ()
    forms = [canon(x) for x in inst]
    return () if len(set(forms)) == len(forms) else err(path, "uniqueItems", "duplicate items")


def k_required(val, _s, inst, _r, path):
    missing = [k for k in val if isinstance(inst, dict) and k not in inst]
    return tuple(e for k in missing for e in err(path, "required", f"missing {k!r}"))


def k_properties(val, _s, inst, root, path):
    if not isinstance(inst, dict):
        return ()
    return tuple(e for k, sub in val.items() if k in inst for e in validate(sub, inst[k], root, child(path, k)))


def k_additional(val, schema, inst, root, path):
    if not isinstance(inst, dict):
        return ()
    extra = [k for k in inst if k not in schema.get("properties", {})]
    if val is False:
        return tuple(e for k in extra for e in err(path, "additionalProperties", f"unexpected property {k!r}"))
    return tuple(e for k in extra for e in validate(val, inst[k], root, child(path, k)))


def k_items(val, _s, inst, root, path):
    if not isinstance(inst, list):
        return ()
    return tuple(e for i, x in enumerate(inst) for e in validate(val, x, root, child(path, i)))


def k_all_of(val, _s, inst, root, path):
    return tuple(e for sub in val for e in validate(sub, inst, root, path))


def k_any_of(val, _s, inst, root, path):
    return () if any(not validate(sub, inst, root, path) for sub in val) else err(path, "anyOf", "no subschema matched")


def k_one_of(val, _s, inst, root, path):
    n = sum(1 for sub in val if not validate(sub, inst, root, path))
    return () if n == 1 else err(path, "oneOf", f"{n} subschemas matched (need exactly 1)")


def k_not(val, _s, inst, root, path):
    return err(path, "not", "matched a 'not' subschema") if not validate(val, inst, root, path) else ()


def k_if(val, schema, inst, root, path):
    branch = schema.get("then", True) if not validate(val, inst, root, path) else schema.get("else", True)
    return validate(branch, inst, root, path)


def k_ref(val, _s, inst, root, path):
    if not val.startswith("#"):
        raise ValueError(f"only local $ref supported: {val}")
    found, target = pointer_get(root, val[1:])
    if not found:
        raise ValueError(f"unresolved $ref {val}")
    return validate(target, inst, root, path)


KEYWORDS = {
    "type": k_type, "enum": k_enum, "const": k_const, "pattern": k_pattern,
    "minLength": k_min_length, "maxLength": k_max_length, "minItems": k_min_items, "maxItems": k_max_items,
    "uniqueItems": k_unique_items, "required": k_required, "properties": k_properties,
    "additionalProperties": k_additional, "items": k_items, "allOf": k_all_of, "anyOf": k_any_of,
    "oneOf": k_one_of, "not": k_not, "if": k_if, "$ref": k_ref,
}


def schema_keywords(schema):
    """All keywords used anywhere in a schema (walking subschemas, not property names)."""
    if not isinstance(schema, dict):
        return frozenset()
    subs_map = [v for k in ("properties", "$defs") for v in schema.get(k, {}).values()]
    subs_list = [v for k in ("allOf", "anyOf", "oneOf") for v in schema.get(k, [])]
    subs_one = [schema[k] for k in ("items", "not", "if", "then", "else", "additionalProperties")
                if isinstance(schema.get(k), dict)]
    return reduce(lambda acc, s: acc | schema_keywords(s), subs_map + subs_list + subs_one, frozenset(schema))


# ---------------------------------------------------------------- self-test

SELF_TESTS = (
    ({"enum": [False]}, 0, False),
    ({"enum": [1]}, True, False),
    ({"const": {"a": 1, "b": 2}}, {"b": 2, "a": 1}, True),
    ({"type": "integer"}, True, False),
    ({"type": "string", "maxLength": 2}, "éé", True),
    ({"oneOf": [{"type": "string"}, {"pattern": "^a"}]}, "abc", False),
    ({"if": {"const": 1}, "then": {"type": "integer"}, "else": {"type": "string"}}, "x", True),
    ({"if": {"const": 1}, "then": {"type": "string"}}, 1, False),
    ({"not": {"const": "0.00"}}, "0.00", False),
    ({"uniqueItems": True}, [{"a": 1}, {"a": 1}], False),
    ({"properties": {"a": {"type": "string"}}, "additionalProperties": False}, {"a": "x", "b": 1}, False),
    ({"$defs": {"s": {"type": "string"}}, "$ref": "#/$defs/s"}, 3, False),
)


def self_test():
    return tuple((i, s, x, want) for i, (s, x, want) in enumerate(SELF_TESTS) if (not validate(s, x, s)) != want)


# ---------------------------------------------------------------- provenance

def cents_to_decimal(v):
    return f"{Decimal(int(v)) / 100:.2f}"


def usdc_micro_to_decimal(v):
    d = Decimal(int(v)) / Decimal(1000000)
    if d != d.quantize(Decimal("0.01")):
        raise ValueError(f"{v} micro-units is not a whole number of cents")
    return f"{d:.2f}"


TRANSFORMS = {
    "ein_strip_hyphen": lambda v: v.replace("-", ""),
    "usd_cents_to_decimal": cents_to_decimal,
    "usdc_micro_to_usd_decimal": usdc_micro_to_decimal,
    "after_last_colon_space": lambda v: v.rsplit(": ", 1)[-1],
    "chariot_anonymous_to_level": lambda v: "anonymous" if v is True else "full_contact",
}
CONVERSIONS = ("exact", "renamed", "transformed", "not_available")


def check_provenance_entry(record, p):
    found, value = pointer_get(record, p["record_path"])
    conv, tf = p["conversion"], p.get("transform")
    if conv not in CONVERSIONS:
        return (f"{p['record_path']}: unknown conversion {conv}",)
    if conv == "not_available":
        return () if not found else (f"{p['record_path']}: marked not_available but present",)
    if not found:
        return (f"{p['record_path']}: missing from record",)
    if conv in ("exact", "renamed"):
        return () if json_equal(value, p.get("source_value")) else (f"{p['record_path']}: {value!r} != source {p.get('source_value')!r}",)
    if tf in TRANSFORMS:
        got = TRANSFORMS[tf](p["source_value"])
        return () if json_equal(got, value) else (f"{p['record_path']}: {tf}({p['source_value']!r}) = {got!r} != {value!r}",)
    return () if tf == "manual" else (f"{p['record_path']}: unknown transform {tf}",)


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def html_to_text(raw):
    no_code = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", raw)
    return html.unescape(re.sub(r"<[^>]+>", " ", no_code))


def load_sources(log_paths):
    """URL -> normalised text of the cached file, from fetcher logs (last good entry wins)."""
    def entries(lp):
        base = os.path.dirname(os.path.dirname(os.path.abspath(lp)))
        with open(lp, encoding="utf-8") as f:
            recs = [json.loads(line) for line in f if line.strip()]
        return [(r["url"], os.path.join(base, r["file"]) if not os.path.isabs(r["file"]) else r["file"],
                 r.get("ctype", "")) for r in recs if r.get("status") == 200 and r.get("file")]
    def read(path, ctype):
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
        return norm(html_to_text(raw) if "html" in ctype else raw)
    pairs = [e for lp in log_paths for e in entries(lp)]
    return {url: read(path, ctype) for url, path, ctype in pairs if os.path.exists(path)}


def check_snippets(prov, sources):
    def one(p):
        if p["conversion"] == "not_available" or not p.get("source_snippet"):
            return ()
        text = sources.get(p.get("source_url"))
        if text is None:
            return (f"{p['record_path']}: source not cached ({p.get('source_url')})",)
        return () if norm(p["source_snippet"]) in text else (f"{p['record_path']}: snippet not found in source",)
    return tuple(e for p in prov for e in one(p))


# ---------------------------------------------------------------- vectors

def run_vector(schema, vec, sources):
    errors = validate(schema, vec["record"], schema)
    is_valid = not errors
    want_valid = vec["expect"] == "valid"
    found = {(p, k) for p, k, _ in errors}
    missing = [e for e in vec.get("expected_errors", []) if (e["instance_path"], e["keyword"]) not in found]
    prov = vec.get("field_provenance", [])
    prov_errs = tuple(e for p in prov for e in check_provenance_entry(vec["record"], p))
    snip_errs = check_snippets(prov, sources) if sources else ()
    ok = (is_valid == want_valid) and not missing and not prov_errs and not snip_errs
    counts = {c: sum(1 for p in prov if p["conversion"] == c) for c in CONVERSIONS}
    return {"id": vec["vector_id"], "expect": vec["expect"], "valid": is_valid, "ok": ok, "errors": errors,
            "missing_expected": missing, "prov_errors": prov_errs, "snippet_errors": snip_errs,
            "counts": counts, "snippets_checked": sum(1 for p in prov if p["conversion"] != "not_available" and p.get("source_snippet")) if sources else 0}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def report(results, unsupported, selftest_fail, n_sources):
    lines = [f"schema keywords outside the implemented subset: {sorted(unsupported) or 'none'}",
             f"validator self-test: {len(SELF_TESTS) - len(selftest_fail)}/{len(SELF_TESTS)} passed",
             f"cached sources loaded: {n_sources}", "",
             "vector | expect | result | ok | exact/renamed/transformed/not_available | snippets | first error"]
    rows = [f"{r['id']} | {r['expect']} | {'valid' if r['valid'] else 'invalid'} | {'PASS' if r['ok'] else 'FAIL'} | "
            f"{r['counts']['exact']}/{r['counts']['renamed']}/{r['counts']['transformed']}/{r['counts']['not_available']} | "
            f"{r['snippets_checked']} | {(r['errors'][0][0] or '/') + ' ' + r['errors'][0][1] if r['errors'] else '-'}"
            for r in results]
    problems = [f"  {r['id']}: {x}" for r in results
                for x in list(r["missing_expected"]) + list(r["prov_errors"]) + list(r["snippet_errors"])]
    totals = reduce(lambda a, r: {c: a[c] + r["counts"][c] for c in CONVERSIONS}, results, {c: 0 for c in CONVERSIONS})
    summary = ["",
               f"vectors: {len(results)} ({sum(r['expect'] == 'valid' for r in results)} positive, "
               f"{sum(r['expect'] == 'invalid' for r in results)} negative); passed {sum(r['ok'] for r in results)}",
               f"provenance entries: {sum(totals.values())} " + ", ".join(f"{c} {totals[c]}" for c in CONVERSIONS),
               f"snippets verified against cache: {sum(r['snippets_checked'] for r in results if not r['snippet_errors'])}"]
    return "\n".join(lines + rows + (["", "problems:"] + problems if problems else []) + summary)


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    schema = load_json(os.path.join(root, SCHEMA_PATH))
    unsupported = schema_keywords(schema) - SUPPORTED
    st = self_test()
    sources = load_sources(argv[2:]) if len(argv) > 2 else {}
    vectors = [load_json(p) for p in sorted(glob.glob(os.path.join(root, VECTOR_GLOB)))]
    results = [run_vector(schema, v, sources) for v in vectors]
    print(report(results, unsupported, st, len(sources)))
    ok = not unsupported and not st and results and all(r["ok"] for r in results) \
        and schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
