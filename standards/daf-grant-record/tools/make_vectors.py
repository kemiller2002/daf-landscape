"""One-off generator for standards/daf-grant-record/vectors/*.json (task P-B4013-03-02).
Usage: python3 -I make_vectors.py REPO_ROOT
Pure data + pure functions; writes one JSON file per vector. Stdlib only."""
import copy
import json
import os
import sys

CHARIOT = "https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md"
ENDAOMENT = "https://docs.endaoment.org/developers/api/transfers/create-an-async-grant-request.md"
CANDID_DEV = "https://developer.candid.org/docs/candids-taxonomy"
CACHED = {
    CHARIOT: {"retrieved": "2026-11-19", "sha256": "8c17df4086c1d89df53e5e05a32df4d0d49455265da2f2a21afce2953b271909",
              "cache": "scratchpad q1303/std/cfc76e7268828bd5"},
    ENDAOMENT: {"retrieved": "2026-11-19", "sha256": "7790bd5227f919ad00541198e56f882f5c66ac5ba6acb06082e0279ae10cf972",
                "cache": "scratchpad q1303/std/9955741ee77ac16b", "openapi_version": "4.88.0"},
    CANDID_DEV: {"retrieved": "2026-11-20", "cache": "scratchpad q1332/web/531a46f6ec870eec"},
}


def prov(path, conversion, source_field=None, url=None, snippet=None, value=None, transform=None, note=""):
    base = {"record_path": path, "conversion": conversion, "source_field": source_field,
            "source_url": url, "source_snippet": snippet, "note": note}
    extra = ({"source_value": value} if value is not None else {})
    extra2 = ({"transform": transform} if transform else {})
    return {**base, **extra, **extra2}


PCS_GENERAL = {"vocabulary": "PCS", "facet": "support_strategy", "code": "UA0000", "label": "General support"}

CHARIOT_RECORD = {
    "schema_version": "0.1",
    "grant_id": "grant_3kd02",
    "fund_id": "fund_a91x",
    "recipient": {"ein": "133441466", "alternative_id": {"scheme": "x-sponsor-org-id", "id": "org_77fq"}},
    "amount": {"value": "250.00", "currency": "USD"},
    "purpose": {"codes": [PCS_GENERAL], "text": "Wherever needed most"},
    "anonymity": "full_contact",
    "status": "pending",
    "external_ids": [{"system": "chariot-dafpay", "id": "grant_req_01jpjenf5q6cawy43yxfcrxhct"}],
    "dates": {"recommended_at": "2026-06-10T14:30:00Z"},
}

CHARIOT_PROV = [
    prov("/grant_id", "renamed", "Create Grant response: id", CHARIOT, '"id": "grant_3kd02"', "grant_3kd02",
         note="Sponsor's own grant id, returned by Create Grant"),
    prov("/fund_id", "exact", "Create Grant request: fund_id", CHARIOT, '"fund_id": "fund_a91x"', "fund_a91x"),
    prov("/recipient/ein", "transformed", "Search Organizations response: organizations[0].ein (resolves organization_id org_77fq)",
         CHARIOT, '"ein": "13-3441466"', "13-3441466", "ein_strip_hyphen",
         "Create Grant sends organization_id; the EIN comes from the documented Search Organizations example for the same org_77fq. Chariot also allows 'an ein field here in place of organization_id'."),
    prov("/recipient/alternative_id/id", "renamed", "Create Grant request: organization_id", CHARIOT,
         '"organization_id": "org_77fq"', "org_77fq"),
    prov("/recipient/alternative_id/scheme", "transformed", "(none: scheme label)", CHARIOT,
         '"organization_id": "org_77fq"', None, "manual",
         "Scheme label 'x-sponsor-org-id' assigned by the converter for the sponsor's internal organization id"),
    prov("/amount/value", "transformed", "Create Grant request: amount", CHARIOT, '"amount": 25000', 25000,
         "usd_cents_to_decimal", "Chariot: 'integer cents in USD (e.g., 25000 = $250.00)'"),
    prov("/amount/currency", "transformed", "Conventions: monetary amounts", CHARIOT,
         "All monetary amounts are **integer cents in USD**", None, "manual",
         "Currency is a documented convention ('unless we agree otherwise during onboarding'), not a payload field"),
    prov("/purpose/text", "renamed", "Create Grant request: purpose", CHARIOT, '"purpose": "Wherever needed most"',
         "Wherever needed most"),
    prov("/purpose/codes/0/code", "transformed", "Create Grant request: purpose (coded by converter)", CANDID_DEV,
         "General support UA0000 or UA", None, "manual",
         "Coded by hand [I]: PCS 'General support' covers 'support which may be applied to any use or to fund any purpose (unrestricted support)'. Chariot sends free text only."),
    prov("/anonymity", "transformed", "Create Grant request: anonymous", CHARIOT, '"anonymous": false', False,
         "chariot_anonymous_to_level",
         "anonymous:true withholds 'the donor's name and contact details'; false is read as full_contact. Chariot's boolean cannot express name_only."),
    prov("/status", "exact", "Create Grant response: status", CHARIOT, '"status": "pending"', "pending"),
    prov("/dates/recommended_at", "renamed", "Create Grant response: created_at", CHARIOT,
         '"created_at": "2026-06-10T14:30:00Z"', "2026-06-10T14:30:00Z"),
    prov("/external_ids/0/id", "transformed", "Create Grant request: note", CHARIOT,
         '"note": "DAFpay Grant Request: grant_req_01jpjenf5q6cawy43yxfcrxhct"',
         "DAFpay Grant Request: grant_req_01jpjenf5q6cawy43yxfcrxhct", "after_last_colon_space",
         "Chariot Grant Request ID; it 'must appear on the grant letter / remittance advice sent to the nonprofit' and is also the Idempotency-Key"),
    prov("/sponsor_id", "not_available", note="The sponsor hosts the API; its EIN is not in any payload"),
    prov("/payment_reference", "not_available", note="Status is pending; Chariot's spec has no rail reference field"),
    prov("/restriction_text", "not_available", note="No restriction field in the recommended shape"),
    prov("/dates/approved_at", "not_available", note="Not in the Create Grant response"),
]

CHARIOT_STATUS_RECORD = {
    **CHARIOT_RECORD,
    "status": "approved",
    "dates": {"recommended_at": "2026-06-10T14:30:00Z", "approved_at": "2026-06-11T09:12:00Z",
              "updated_at": "2026-06-11T09:12:00Z"},
}

CHARIOT_STATUS_PROV = (
    [p for p in CHARIOT_PROV if p["record_path"] not in ("/status", "/dates/approved_at")]
    + [
        prov("/status", "exact", "Get Grant Status response: status", CHARIOT, '"status": "approved"', "approved"),
        prov("/dates/updated_at", "renamed", "Get Grant Status response: updated_at", CHARIOT,
             '"updated_at": "2026-06-11T09:12:00Z"', "2026-06-11T09:12:00Z"),
        prov("/dates/approved_at", "transformed", "Get Grant Status response: updated_at", CHARIOT,
             '"updated_at": "2026-06-11T09:12:00Z"', "2026-06-11T09:12:00Z", "manual",
             "[I] updated_at is taken as the approval time because the same response reports status approved; Chariot has no approved_at field"),
    ]
)

UUID = "123e4567-e89b-12d3-a456-426614174000"
ENDAOMENT_RECORD = {
    "schema_version": "0.1",
    "grant_id": UUID,
    "fund_id": UUID,
    "recipient": {"ein": "530196605", "alternative_id": {"scheme": "x-endaoment-org-uuid", "id": UUID}},
    "amount": {"value": "1.00", "currency": "USD"},
    "purpose": {"text": "Supporting educational programs"},
    "restriction_text": "Funds must be used exclusively for the summer education program",
    "anonymity": "name_only",
    "status": "pending",
    "payment_reference": {"rail": "onchain", "reference": "0x1234567890abcdef"},
    "dates": {"recommended_at": "2024-03-20T10:30:00Z", "updated_at": "2024-03-20T10:30:00Z"},
}

ENDAOMENT_PROV = [
    prov("/grant_id", "renamed", "GrantTransferDto.id", ENDAOMENT,
         "id: type: string description: Unique identifier of the transfer format: uuid example: " + UUID, UUID,
         note="Every uuid example in the OpenAPI is the same placeholder, so grant, fund and org ids coincide here"),
    prov("/fund_id", "renamed", "InitiateAsyncGrantInputDto.originFundId", ENDAOMENT,
         "originFundId: type: string description: ID of the fund that is the origin of the grant format: uuid example: " + UUID, UUID),
    prov("/recipient/alternative_id/id", "renamed", "InitiateAsyncGrantInputDto.destinationOrgId", ENDAOMENT,
         "destinationOrgId: type: string description: ID of the organization that will receive the grant format: uuid example: " + UUID, UUID),
    prov("/recipient/alternative_id/scheme", "transformed", "(none: scheme label)", ENDAOMENT,
         "description: Unique identifier of the organization in Endaoment database", None, "manual",
         "Scheme label 'x-endaoment-org-uuid' assigned by the converter"),
    prov("/recipient/ein", "renamed", "GrantTransferDto.destinationOrg.ein (OrgSimpleListingDto)", ENDAOMENT,
         "description: IRS Employer Identification Number (EIN) without hyphen example: '530196605'", "530196605",
         note="Response-side example; the OpenAPI's per-field examples are independent, so the pairing of this EIN with the uuid is an assembly [I]"),
    prov("/amount/value", "transformed", "InitiateAsyncGrantInputDto.requestedAmount", ENDAOMENT,
         "The amount in USDC to be granted, in the smallest currency unit (1000000 = 1 USD) example: '1000000'",
         "1000000", "usdc_micro_to_usd_decimal", "USDC smallest unit (1000000 = 1 USD) to a two-decimal USD string; non-cent amounts are rejected, not rounded"),
    prov("/amount/currency", "transformed", "requestedAmount description", ENDAOMENT, "(1000000 = 1 USD)", None, "manual",
         "[I] USDC is recorded as USD at the 1:1 rate the OpenAPI states; the record does not model stablecoins"),
    prov("/purpose/text", "renamed", "InitiateAsyncGrantInputDto.purpose", ENDAOMENT,
         "description: Public declaration of the grant purpose maxLength: 511 example: Supporting educational programs",
         "Supporting educational programs"),
    prov("/purpose/codes", "not_available",
         note="Free text only. An education subject code exists in PCS but its code value could not be read first-hand (full code list robots-blocked), so none is assigned"),
    prov("/restriction_text", "renamed", "InitiateAsyncGrantInputDto.specialInstructions", ENDAOMENT,
         "example: Funds must be used exclusively for the summer education program",
         "Funds must be used exclusively for the summer education program"),
    prov("/anonymity", "transformed", "InitiateAsyncGrantInputDto.shareMyEmail (default) + recommender", ENDAOMENT,
         "Set by the user recommending the grant. default: false", False, "manual",
         "[I] shareMyEmail defaults to false (email withheld) while recommender carries a name ('John Doe'), read as name_only"),
    prov("/status", "renamed", "GrantTransferDto.asyncStatus", ENDAOMENT,
         "description: Current status of the async transfer request enum: - PendingLiquidation - Liquidated - Cancelled example: pending",
         "pending", note="The OpenAPI's example 'pending' is not in its own enum; the documented value PendingLiquidation would also map to pending"),
    prov("/dates/recommended_at", "renamed", "GrantTransferDto.createdAtUtc", ENDAOMENT,
         "description: UTC timestamp when the transfer was created format: date-time example: '2024-03-20T10:30:00Z'",
         "2024-03-20T10:30:00Z"),
    prov("/dates/updated_at", "renamed", "GrantTransferDto.updatedAtUtc", ENDAOMENT,
         "description: UTC timestamp when the transfer was last updated format: date-time example: '2024-03-20T10:30:00Z'",
         "2024-03-20T10:30:00Z"),
    prov("/payment_reference/reference", "renamed", "GrantTransferDto.transactionHash", ENDAOMENT,
         "description: Transaction hash of the donation made to the target entity example: '0x1234567890abcdef'",
         "0x1234567890abcdef", note="Nullable in the OpenAPI; kept because the example supplies it"),
    prov("/payment_reference/rail", "transformed", "GrantTransferDto.transactionHash (field type)", ENDAOMENT,
         "Transaction hash of the donation made to the target entity", None, "manual", "Rail 'onchain' inferred from the hash field"),
    prov("/payment_reference/paid_date", "not_available", note="No payment date field"),
    prov("/sponsor_id", "not_available", note="Endaoment is the sponsor; its EIN is not in the payload"),
    prov("/external_ids", "not_available", note="No intermediary id"),
    prov("/dates/approved_at", "not_available",
         note="Approval status is no longer exposed: status (PendingReview/Approved/Rejected) is deprecated (wave 40A)"),
]

ENDAOMENT_NOT_CARRIED = ["idempotencyKey (transaction-API concern, not part of a published record)",
                         "recommendationIds", "destinationSubprojectId", "recommender (the name itself; only its presence drives anonymity)",
                         "netAmount", "fee", "chainId", "type", "status (deprecated)",
                         "destinationOrg.* other than ein (name, address, nteeCode, ...)", "destinationSubproject"]
CHARIOT_NOT_CARRIED = ["Idempotency-Key header (same value as the note id; transaction-API concern)",
                       "status_description (null in the example)", "Search Organizations name/address"]

SYNTHETIC_PAID = {
    "schema_version": "0.1",
    "grant_id": "US-EIN-000000000:G-0001",
    "sponsor_id": "US-EIN-000000000",
    "fund_id": "F-0001",
    "recipient": {"ein": "000000000"},
    "amount": {"value": "100.00", "currency": "USD"},
    "purpose": {"codes": [{"vocabulary": "PCS", "facet": "subject", "code": "SC020000", "label": "Climate change"},
                          PCS_GENERAL]},
    "anonymity": "anonymous",
    "status": "paid",
    "payment_reference": {"rail": "check", "reference": "000000", "paid_date": "2026-01-02"},
    "dates": {"recommended_at": "2026-01-01T00:00:00Z", "approved_at": "2026-01-01T12:00:00Z"},
}


def set_path(obj, path, value):
    """Return a deep copy of obj with JSON-pointer path set (value=DELETE removes it)."""
    keys = [k for k in path.split("/")[1:]]
    def go(node, ks):
        if not ks:
            return value
        k = int(ks[0]) if isinstance(node, list) else ks[0]
        if len(ks) == 1 and value is DELETE:
            return ([x for i, x in enumerate(node) if i != k] if isinstance(node, list)
                    else {kk: vv for kk, vv in node.items() if kk != k})
        if isinstance(node, list):
            return [go(x, ks[1:]) if i == k else copy.deepcopy(x) for i, x in enumerate(node)]
        return {**copy.deepcopy(node), k: go(node.get(k, {}), ks[1:])}
    return go(obj, keys)


DELETE = object()

NEGATIVES = [
    ("neg-01-ein-with-hyphen", "Recipient EIN copied raw from Chariot's org lookup ('13-3441466')",
     CHARIOT_RECORD, [("/recipient/ein", "13-3441466")], [("/recipient/ein", "pattern")]),
    ("neg-02-usdc-micro-units-unconverted", "Endaoment requestedAmount left in USDC micro-units",
     ENDAOMENT_RECORD, [("/amount/value", "1000000")], [("/amount/value", "pattern")]),
    ("neg-03-amount-as-number", "Amount as a JSON number (Chariot cents), not a decimal string",
     CHARIOT_RECORD, [("/amount/value", 25000)], [("/amount/value", "type")]),
    ("neg-04-amount-zero", "Zero amount",
     CHARIOT_RECORD, [("/amount/value", "0.00")], [("/amount/value", "not")]),
    ("neg-05-sub-cent-amount", "USDC amount with sub-cent precision (1234567 micro-units) rounded neither way",
     ENDAOMENT_RECORD, [("/amount/value", "1.234567")], [("/amount/value", "pattern")]),
    ("neg-06-endaoment-status-raw", "Endaoment asyncStatus copied raw ('PendingLiquidation')",
     ENDAOMENT_RECORD, [("/status", "PendingLiquidation")], [("/status", "enum")]),
    ("neg-07-anonymity-boolean", "Chariot's anonymous boolean copied raw",
     CHARIOT_RECORD, [("/anonymity", False)], [("/anonymity", "enum")]),
    ("neg-08-paid-without-payment-reference", "Status paid with no payment_reference",
     SYNTHETIC_PAID, [("/payment_reference", DELETE)], [("", "required")]),
    ("neg-09-paid-without-paid-date", "Status paid with a payment_reference that lacks paid_date",
     SYNTHETIC_PAID, [("/payment_reference/paid_date", DELETE)], [("/payment_reference", "required")]),
    ("neg-10-missing-grant-id", "No grant_id",
     CHARIOT_RECORD, [("/grant_id", DELETE)], [("", "required")]),
    ("neg-11-purpose-empty", "Purpose with neither codes nor text",
     CHARIOT_RECORD, [("/purpose", {})], [("/purpose", "anyOf")]),
    ("neg-12-pcs-facet-mismatch", "Subject code SC020000 labelled as a support strategy",
     CHARIOT_RECORD, [("/purpose/codes/0", {"vocabulary": "PCS", "facet": "support_strategy", "code": "SC020000"})],
     [("/purpose/codes/0", "oneOf")]),
    ("neg-13-ntee-vocabulary", "NTEE code (Endaoment's recipient nteeCode example E91) in place of PCS",
     CHARIOT_RECORD, [("/purpose/codes/0", {"vocabulary": "NTEE", "facet": "subject", "code": "E91"})],
     [("/purpose/codes/0/vocabulary", "const")]),
    ("neg-14-purpose-text-too-long", "Purpose text of 512 characters (limit 511)",
     CHARIOT_RECORD, [("/purpose/text", "x" * 512)], [("/purpose/text", "maxLength")]),
    ("neg-15-six-purpose-codes", "Six PCS codes (limit 5)",
     CHARIOT_RECORD, [("/purpose/codes", [{"vocabulary": "PCS", "facet": "support_strategy", "code": c}
                                          for c in ["UA", "UA00", "UA0000", "UB", "UC", "UD"]])],
     [("/purpose/codes", "maxItems")]),
    ("neg-16-unknown-field-donor-email", "Unknown top-level field carrying donor contact data",
     CHARIOT_RECORD, [("/donor_email", "dana@example.com")], [("", "additionalProperties")]),
    ("neg-17-recipient-no-identifier", "Recipient object with no EIN and no alternative id",
     CHARIOT_RECORD, [("/recipient", {})], [("/recipient", "anyOf")]),
    ("neg-18-date-not-utc-timestamp", "recommended_at given as a bare date",
     CHARIOT_RECORD, [("/dates/recommended_at", "2026-06-10")], [("/dates/recommended_at", "pattern")]),
    ("neg-19-lowercase-currency", "Currency 'usd'",
     CHARIOT_RECORD, [("/amount/currency", "usd")], [("/amount/currency", "pattern")]),
    ("neg-20-wrong-schema-version", "schema_version 0.2",
     CHARIOT_RECORD, [("/schema_version", "0.2")], [("/schema_version", "const")]),
]


BASE_IDS = {id(CHARIOT_RECORD): "pos-01-chariot-create-grant (record, mutated)",
            id(ENDAOMENT_RECORD): "pos-03-endaoment-async-grant (record, mutated)",
            id(SYNTHETIC_PAID): "pos-04-synthetic-paid-check (record, mutated)"}


def apply_mutations(record, muts):
    out = record
    for path, value in muts:
        out = set_path(out, path, value)
    return out


def positive(vid, desc, record, provenance, not_carried, sources):
    return vid, {
        "vector_id": vid, "description": desc, "expect": "valid", "schema": "../schema-v0.1.json",
        "status_label": "draft, unendorsed",
        "sources": [{"url": u, **CACHED[u]} for u in sources],
        "field_provenance": provenance, "source_fields_not_carried": not_carried, "record": record,
    }


def negative(vid, desc, base, muts, expected):
    return vid, {
        "vector_id": vid, "description": desc, "expect": "invalid", "schema": "../schema-v0.1.json",
        "status_label": "draft, unendorsed",
        "derived_from": BASE_IDS[id(base)],
        "mutations": [{"record_path": p, "value": ("<deleted>" if v is DELETE else v)} for p, v in muts],
        "expected_errors": [{"instance_path": p, "keyword": k} for p, k in expected],
        "record": apply_mutations(base, muts),
    }


def all_vectors():
    pos = [
        positive("pos-01-chariot-create-grant", "Chariot DAFpay 'Create Grant' request and response example (v2026-04-01), converted",
                 CHARIOT_RECORD, CHARIOT_PROV, CHARIOT_NOT_CARRIED, [CHARIOT, CANDID_DEV]),
        positive("pos-02-chariot-grant-status-approved", "Chariot 'Create Grant' request plus 'Get Grant Status' response example (approved), converted",
                 CHARIOT_STATUS_RECORD, CHARIOT_STATUS_PROV, CHARIOT_NOT_CARRIED, [CHARIOT, CANDID_DEV]),
        positive("pos-03-endaoment-async-grant", "Endaoment 'Create async grant' (OpenAPI 4.88.0) request and response, assembled from per-field examples, converted",
                 ENDAOMENT_RECORD, ENDAOMENT_PROV, ENDAOMENT_NOT_CARRIED, [ENDAOMENT]),
        ("pos-04-synthetic-paid-check", {
            "vector_id": "pos-04-synthetic-paid-check",
            "description": "SYNTHETIC (not converted from any source): placeholder zero identifiers; exercises status paid, the payment_reference rule, two PCS facets and sponsor_id",
            "expect": "valid", "schema": "../schema-v0.1.json", "status_label": "draft, unendorsed",
            "sources": [{"url": CANDID_DEV, **CACHED[CANDID_DEV], "used_for": "PCS example codes SC020000, UA0000"}],
            "field_provenance": [], "record": SYNTHETIC_PAID}),
    ]
    neg = [negative(*n) for n in NEGATIVES]
    return pos + neg


def main(argv):
    outdir = os.path.join(argv[1], "standards/daf-grant-record/vectors")
    os.makedirs(outdir, exist_ok=True)
    written = [(vid, json.dumps(v, indent=2, ensure_ascii=False) + "\n") for vid, v in all_vectors()]
    for vid, text in written:
        with open(os.path.join(outdir, vid + ".json"), "w", encoding="utf-8") as f:
            f.write(text)
    print(len(written), "vectors written to", outdir)


if __name__ == "__main__":
    main(sys.argv)
