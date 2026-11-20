# Minimal open DAF grant record: JSON Schema v0.1 and test vectors (P-B4013-03-02)

> **Status: draft, unendorsed.** This is research output, not a product launch or a proposed industry standard. No sponsor, intermediary, standards body or regulator has reviewed, endorsed or adopted it.

- **Queue item:** P-B4013-03-02, from [`queue-proposals-b40n13-03-g1913-03.csv`](../../data/mission-2026-11-14/queue-proposals-b40n13-03-g1913-03.csv).
- **Date:** 2026-11-20. The Candid and Creative Commons pages were read on that date. The Chariot and Endaoment pages are the robots-checked copies cached on 2026-11-19 (scratchpad `q1303/std`). Public pages only: no logins, no forms, no keyed API calls, no outreach.
- **Starting point:** the draft record in [b40n13-03-g1913-03-schema-and-processor-accounts.md](b40n13-03-g1913-03-schema-and-processor-accounts.md) §3.2 and [`daf-grant-schema-map-2026-11-19.csv`](../../data/mission-2026-11-14/daf-grant-schema-map-2026-11-19.csv) (12 rows), together with the wave-40A corrections in [validation-wave40a-report.md](validation-wave40a-report.md). The correction that matters here: Endaoment's `status` (PendingReview / Approved / Rejected) is deprecated, so **approval status is no longer exposed** in its API.
- **Files written:**
  - [`standards/daf-grant-record/schema-v0.1.json`](../../standards/daf-grant-record/schema-v0.1.json): JSON Schema draft 2020-12. 13 top-level properties, 9 of them required.
  - [`standards/daf-grant-record/vectors/`](../../standards/daf-grant-record/vectors/): 24 vectors. 4 positive (3 converted from the docs, 1 synthetic) and 20 negative.
  - [`scripts/mission_validate_grant_record.py`](../../scripts/mission_validate_grant_record.py): stdlib-only validator, written in functional style.
  - [`data/mission-2026-11-14/queue-proposals-b4013-03-02.csv`](../../data/mission-2026-11-14/queue-proposals-b4013-03-02.csv): 6 rows.
- **Labels:**
  - [F] first-party text read in this pass.
  - [R] carried over from a repo file.
  - [C] computed by the script.
  - [I] inference or design choice.
  - [B] blocked by robots.txt or an unreadable robots.txt.

---

## 0. Answers

| Question | Answer |
|---|---|
| **Purpose vocabulary** | **Candid PCS.** Candid's own PCS site states the licence first-hand: "The PCS is available for use under a Creative Commons Attribution 4.0 International license." Every page footer, the downloads page included, reads "This work is licensed under a Creative Commons Attribution 4.0 International License", with a link to creativecommons.org/licenses/by/4.0/ [F]. The NTEE fallback was therefore not needed (§4). |
| **But** | **The full PCS code list could not be read.** The 2024 taxonomy file is served under `/content/`, which taxonomy.candid.org's robots.txt disallows. The site's term data comes from data.taxonomy.candid.org, whose robots.txt returns 401 [B]. The schema therefore checks the **shape** of a PCS code (facet letter plus digit pairs, taken from the four codes on Candid's developer page) but not whether the code exists (§4.3). |
| **Schema** | Nine required fields: `schema_version`, `grant_id`, `fund_id`, `recipient` (EIN, or an alternative scheme), `amount` (two-decimal string plus ISO 4217 code), `purpose` (PCS codes and/or text), `anonymity` (3 levels), `status` (6 values), `dates`. Four optional fields: `sponsor_id`, `restriction_text`, `payment_reference` (required when status is `paid` or `returned`), `external_ids` (§3.1). |
| **Test vectors** | Three vectors are converted from the docs: Chariot Create Grant, Chariot Create Grant plus Get Grant Status, and Endaoment async grant. They carry **55 provenance entries: exact 4, renamed 19, transformed 20, not available 12** [C]. 43 source snippets were found verbatim in the cached pages [C]. Twenty negative vectors each fail on exactly the intended keyword and path [C]. |
| **Validation** | **24 of 24 vectors behave as declared** (4 valid, 20 invalid). The validator implements 21 keywords, and the schema uses 20 of them; none falls outside that set. The 12-case self-test passes [C]. |

---

## 1. Method

1. **Inputs read.** The draft record (§3.2 of the b40n13-03 note), the 12-row schema map CSV, and the wave-40A report sections on the schema study [R].
2. **Source payloads.** Cached copies from scratchpad `q1303/std`, fetched on 2026-11-19 by the robots-respecting fetcher `q1303/scripts/get.py` (user agent `research-script/1.0`):
   - Chariot DAFpay OAuth "API Endpoints" page (v2026-04-01, Markdown), sha256 `8c17df40…`;
   - Endaoment "Create async grant" page, which embeds the OpenAPI document version 4.88.0, sha256 `7790bd52…`.
   - Neither page was fetched again.
3. **Candid licence.** The same fetcher was used, with output in scratchpad `q1332/web`.
   - Read: the PCS home page, Downloads, "Full PCS Taxonomy with Definitions", the PCS FAQ, and the Subjects and Support Strategies pages on taxonomy.candid.org.
   - Read: Candid's developer page "Candid's taxonomy".
   - Read: the CC BY 4.0 deed and legal code on creativecommons.org.
   - Each host's robots.txt was read first. A URL was fetched only if both `*` and the agent were allowed.
4. **Conversion.** Each source field was mapped by hand to the record and classed as:
   - **exact**: same field name, value unchanged;
   - **renamed**: value unchanged, different field name or nesting;
   - **transformed**: value changed, either by a named transform the validator recomputes or by a "manual" mapping explained in a note;
   - **not available**: the source has no value for that record field.
   - `schema_version` is a constant and is not classed.
   - The vector files were written by a one-off generator (scratchpad `q1332/make_vectors.py`). Each vector is self-contained.
5. **Negative vectors.** Each is a single mutation of a positive record, mostly copying a raw source value that a converter must not pass through. The vector states the expected `(instance_path, keyword)` errors.
6. **Validation.** Run as `python3 -I scripts/mission_validate_grant_record.py . <scratchpad>/q1303/std/log.jsonl <scratchpad>/q1332/web/log.jsonl`. Without the logs it skips only the snippet check. The script:
   - checks the schema's keywords against the implemented subset;
   - runs a self-test;
   - validates every vector;
   - recomputes named transforms;
   - checks that `not_available` paths are absent;
   - finds each `source_snippet` verbatim in the cached source, after collapsing whitespace and, for HTML, stripping tags.

## 2. Robots and access log (2026-11-20)

| Host | robots.txt | Result |
|---|---|---|
| docs.givechariot.com | 200, allowed (2026-11-19, q1303 log) | cached copy used, not refetched |
| docs.endaoment.org | 200, allowed (2026-11-19, q1303 log) | cached copy used, not refetched |
| taxonomy.candid.org | 200. Disallows `/content/*`, `/search*`, `/media/*`, `/user/*` and others | 8 pages allowed and fetched: 7 × 200, 1 × 404 (`/about`, a guessed URL). **The xlsx at `/content/download/…/PCS_Taxonomy_Definitions_2024.xlsx` is disallowed and was not fetched [B]** |
| data.taxonomy.candid.org | **401** ("You must log in or use a valid token to access this API") | **not fetched [B]**: an unreadable robots.txt counts as blocked |
| developer.candid.org | 200, allowed (disallows `/*/api-next`, `/edit/`, `/login`, …) | 1 × 200 |
| candid.org | 403 (CloudFront "Request blocked") | not used |
| creativecommons.org | 200, allowed | deed and legal code: 2 × 200 |

crt.sh, certspotter and sec.gov were not used. The user agent was never changed.

---

## 3. Results: the record

### 3.1 Field definitions (schema-v0.1.json)

| Field | Req. | Type / constraint | Definition |
|---|---|---|---|
| `schema_version` | yes | const `"0.1"` | Draft schema version |
| `grant_id` | yes | opaque id `^[A-Za-z0-9][A-Za-z0-9._:~-]{0,199}$` | Sponsor-issued grant identifier, stable from recommendation to payment. Recommended form outside the sponsor: `US-EIN-#########:<local id>` (360Giving prefix practice) |
| `fund_id` | yes | opaque id | Sponsor-scoped fund identifier. Must not contain the donor's name |
| `sponsor_id` | no | `^US-EIN-[0-9]{9}$` | Org-id of the sponsoring organization |
| `recipient.ein` | one of | `^[0-9]{9}$` | IRS EIN without hyphen |
| `recipient.alternative_id` | one of | `{scheme, id}`. The scheme is an org-id list code (`GB-CHC`) or a private `x-…` code | Second identifier, or the only one when the recipient has no EIN (e.g. foreign) |
| `amount.value` | yes | string `^(0\|[1-9][0-9]{0,14})\.[0-9]{2}$`, not `"0.00"` | Grant amount as a two-decimal string. No floats, no minor units |
| `amount.currency` | yes | `^[A-Z]{3}$` | ISO 4217 alphabetic code |
| `purpose.codes` | one of | 1–5 unique PCS code objects `{vocabulary:"PCS", facet, code, label?}` | Coded purpose. The facet letter must match the code (S/P/U/T) |
| `purpose.text` | one of | string, 1–511 characters | Free-text purpose. Untrusted input |
| `restriction_text` | no | string | Binding use restriction, kept apart from the purpose. Untrusted input |
| `anonymity` | yes | `full_contact` \| `name_only` \| `anonymous` | Donor disclosure level |
| `status` | yes | `pending` \| `approved` \| `paid` \| `rejected` \| `canceled` \| `returned` | Lifecycle state |
| `payment_reference` | if paid/returned | `{rail, reference, paid_date?}`. Rail is `ach` \| `check` \| `wire` \| `paypal` \| `stripe` \| `onchain` \| `other` | The rail's own reference. `paid_date` (YYYY-MM-DD) is required when status is paid or returned |
| `external_ids` | no | array of `{system, id}` | Ids in other systems, e.g. an intermediary request id |
| `dates` | yes | `recommended_at` required; `approved_at`, `updated_at` optional; UTC `…Z` timestamps | Lifecycle timestamps |

Every object sets `additionalProperties: false`, so a record cannot carry stray fields such as donor contact data (negative vector neg-16).

### 3.2 Design rationale and changes from the §3.2 draft [I]

- **Amount: a two-decimal string, not integer cents.**
  - The draft used integer minor units. The task asked for conversions such as "USDC micro-units to decimal USD", and a decimal string is unit-free across the three conventions found: Chariot's cents, Endaoment's USDC micro-units, and 360Giving's whole-currency `amountAwarded`.
  - A string avoids float rounding.
  - The converter refuses amounts that are not a whole number of cents. For example, 1,234,567 micro-units is $1.234567, and is rejected rather than rounded (neg-05). The validator's `usdc_micro_to_usd_decimal` raises an error on such input.
- **Recipient.**
  - EIN first, because Chariot ("Chariot identifies every nonprofit by its EIN.") and Schedule I column (b) key on it [R].
  - `alternative_id` holds platform ids (Chariot's `organization_id`, Endaoment's `destinationOrgId`) or an org-id for non-EIN recipients.
  - `anyOf` requires at least one identifier.
- **Purpose.**
  - The draft's single `purpose_code` became `purpose.codes` (up to 5) plus `purpose.text`, with at least one required.
  - The limit of five follows Candid's own rule for grant-level coding ("not required; can have up to 5 codes") [F].
  - Text alone is allowed because both DAF APIs carry only free text. A schema that required a code would reject every converted Endaoment record unless the converter guessed a code.
- **Anonymity.** Three levels, as in the draft. The conversions show why a boolean is not enough:
  - Chariot `anonymous: false` maps to `full_contact`.
  - Endaoment `shareMyEmail` (default false) together with a `recommender` name maps to `name_only`.
- **Status.** Chariot's five values plus `returned`, as in the draft. An `if`/`then` rule requires a `payment_reference` with `paid_date` once status is `paid` or `returned`.
- **Dropped from the published record:** `idempotency_key`. The schema map already classed it as a "transaction-API concern; not part of a published record".
- **Added: `external_ids`.** Chariot's request id must travel with the grant ("must appear on the grant letter / remittance advice sent to the nonprofit"), so the record needs a place for an intermediary's id that is neither the grant id nor the payment reference.

### 3.3 Mapping table: source fields to record (converted vectors)

| Record field | Chariot (Create Grant; Get Grant Status) | Class | Endaoment (async grant, OAS 4.88.0) | Class |
|---|---|---|---|---|
| grant_id | response `id` = `grant_3kd02` | renamed | `GrantTransferDto.id` (uuid example) | renamed |
| fund_id | `fund_id` = `fund_a91x` | exact | `originFundId` | renamed |
| recipient.ein | `13-3441466` from the Search Organizations example for `org_77fq`, hyphen stripped → `133441466` | transformed (`ein_strip_hyphen`) | `destinationOrg.ein` example `530196605` | renamed [I: per-field examples assembled] |
| recipient.alternative_id | `organization_id` = `org_77fq` (scheme `x-sponsor-org-id`) | renamed (scheme label: transformed) | `destinationOrgId` (scheme `x-endaoment-org-uuid`) | renamed (scheme label: transformed) |
| amount.value | `25000` cents → `"250.00"` | transformed (`usd_cents_to_decimal`) | `'1000000'` USDC micro-units → `"1.00"` | transformed (`usdc_micro_to_usd_decimal`) |
| amount.currency | convention "integer cents in USD" → `USD` | transformed | "(1000000 = 1 USD)" → `USD` [I] | transformed |
| purpose.text | `purpose` = "Wherever needed most" | renamed | `purpose` = "Supporting educational programs" | renamed |
| purpose.codes | hand-coded PCS `UA0000` General support [I] | transformed | — (education code not readable first-hand) | not available |
| restriction_text | — | not available | `specialInstructions` | renamed |
| anonymity | `anonymous: false` → `full_contact` | transformed | `shareMyEmail` default false + `recommender` → `name_only` [I] | transformed |
| status | `pending` (create); `approved` (status) | exact | `asyncStatus` example `pending` | renamed |
| payment_reference | — (pending; no rail field) | not available | `transactionHash` → reference; rail `onchain` [I]; no paid date | renamed / transformed / not available |
| external_ids | `note` "DAFpay Grant Request: grant_req_01jp…" → id | transformed (`after_last_colon_space`) | — | not available |
| sponsor_id | — | not available | — | not available |
| dates.recommended_at | `created_at` | renamed | `createdAtUtc` | renamed |
| dates.updated_at | `updated_at` (status vector) | renamed | `updatedAtUtc` | renamed |
| dates.approved_at | `updated_at` when status = approved (status vector) [I]; absent in create | transformed / not available | — (approval no longer exposed, wave 40A) | not available |

Source fields not carried into the record (listed in each vector):
- **Endaoment:** `idempotencyKey`, `recommendationIds`, `destinationSubprojectId`, the `recommender` name itself, `netAmount`, `fee`, `chainId`, `type`, the deprecated `status`, and `destinationOrg` fields other than the EIN.
- **Chariot:** the `Idempotency-Key` header, `status_description`, and the organization name and address.

**Status mapping** (documented values) [F/I]:

| Source value | Record |
|---|---|
| Chariot `pending`, `approved`, `paid`, `rejected`, `canceled` | same value (exact) |
| Endaoment `asyncStatus` `PendingLiquidation` | `pending` |
| Endaoment `asyncStatus` `Cancelled` | `canceled` |
| Endaoment `asyncStatus` `Liquidated` | **no safe mapping.** It describes the liquidation of the fund's assets, not approval or payment (P-B4013-03-02-05) |
| Endaoment deprecated `status` `PendingReview` / `Approved` / `Rejected` | `pending` / `approved` / `rejected` (deprecated; not used in the vector) |

Two quirks of the source documents are kept as found [F]:
- Endaoment's OpenAPI gives `asyncStatus` the example `pending`, which is not in its own enum. It also gives `type` the example `grant`, which is not in its enum either.
- Every uuid example in Endaoment's OpenAPI is the same placeholder (`123e4567-e89b-12d3-a456-426614174000`), so grant, fund and organization ids coincide in the Endaoment vector.

### 3.4 Per-vector provenance counts [C]

| Vector | exact | renamed | transformed | not available | snippets verified |
|---|---|---|---|---|---|
| pos-01-chariot-create-grant | 2 | 4 | 7 | 4 | 13 |
| pos-02-chariot-grant-status-approved | 2 | 5 | 8 | 3 | 15 |
| pos-03-endaoment-async-grant | 0 | 10 | 5 | 5 | 15 |
| pos-04-synthetic-paid-check | synthetic: placeholder zero ids, no provenance | | | | 0 |
| **Total** | **4** | **19** | **20** | **12** | **43** |

Reading:
- **Chariot's recommended shape carries every field the record needs except sponsor, payment reference and restriction.** Most of its values must be transformed (amount unit, EIN hyphen, anonymity boolean, request id inside `note`).
- **Endaoment's values mostly pass unchanged under new names.** It lacks a purpose code, a paid date and any approval state.

---

## 4. Purpose vocabulary: licence findings

### 4.1 What Candid's own pages say [F] (taxonomy.candid.org, read 2026-11-20)

- **Home page, "Use the PCS" panel:** "The PCS is available for use under a Creative Commons Attribution 4.0 International license. This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use."
- **Footer of every PCS page read** (home, Downloads, "Full PCS Taxonomy with Definitions", FAQ, Subjects, Support Strategies): "This work is licensed under a Creative Commons Attribution 4.0 International License." The link goes to `https://creativecommons.org/licenses/by/4.0/`.
- **Downloads → "Full PCS Taxonomy with Definitions":** "The November 2024 release version of the PCS with definitions with definitions and reference to old GCS and NTEE codes." File `PCS_Taxonomy_Definitions_2024.xlsx` (328.44 kB). The file was not fetched because robots.txt disallows `/content/*` [B].
- **FAQ:**
  - "The most recent update was completed in November 2024."
  - "Candid has committed to reviewing the PCS approximately every three to four years".
  - "The Philanthropy Classification System is based on the NTEE and the majority of the Subject codes overlap between the two models."
  - On the crosswalk: "You may request a copy by e-mailing".
- **Support Strategies page**, on grant-level coding: "grant details to reflect the specific strategy or implementation approach being supported by the grant when that is outside of, or more granular than, the recipient organization’s core strategy (not required; can have up to 5 codes)".

### 4.2 The licence itself [F] (creativecommons.org/licenses/by/4.0/, read 2026-11-20)

- Deed: "You are free to: Share — copy and redistribute the material in any medium or format for any purpose, even commercially. Adapt — remix, transform, and build upon the material for any purpose, even commercially."
- Condition: "Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made."
- **Decision.** CC BY 4.0 permits referencing PCS codes in a schema, including commercial use, provided attribution is given. PCS was chosen and NTEE was not needed as the fallback.
- **Attribution.** The schema's `description` carries: "Philanthropy Classification System (PCS) by Candid, https://taxonomy.candid.org/, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/". It also states that the schema references codes but neither reproduces nor modifies the taxonomy.

### 4.3 What could not be confirmed

- **The full code list.** Only four codes were read first-hand, from the "PCS examples" table on developer.candid.org/docs/candids-taxonomy [F]:
  - Subject "Climate change" `SC020000 or SC02`;
  - Population "Adults" `PA020000 or PA02`;
  - Support Strategy "General support" `UA0000 or UA` ("Support for the day-to-day operating costs of an organization or to further the general purpose of an organization. Also includes support which may be applied to any use or to fund any purpose (unrestricted support); does not include unspecified support.");
  - Transaction "Cash grants" `TA00 or TA`.
  - The schema's code patterns (`^S[A-Z]([0-9]{2}){0,3}$` and the same form for P, U and T) generalise from these four [I]. Codes in other facets (organization type, geography) are not accepted in v0.1.
- **When the licence changed.** The repo carries "reported moved to CC BY 4.0 in Nov 2025" [R]. The pages read state the current licence but give no date for it.
- **Scope.** The CC BY statement appears on the PCS website and on its downloads page. The Taxonomy API (key required) was not read, so whether its terms add conditions is unknown.
- **Developer page.** It still carries no licence statement, as the repo already noted [F].

---

## 5. Validation results [C]

```
schema keywords outside the implemented subset: none
validator self-test: 12/12 passed
cached sources loaded: 23
vectors: 24 (4 positive, 20 negative); passed 24
provenance entries: 55 exact 4, renamed 19, transformed 20, not_available 12
snippets verified against cache: 43
RESULT: PASS
```

Every negative vector fails only on the intended keyword. The one exception is neg-13, which fails on two linked keywords, as listed below.

| Vector | Mutation (raw value a converter must not pass through) | Error |
|---|---|---|
| neg-01 | EIN `13-3441466` (Chariot org lookup, hyphenated) | `/recipient/ein` pattern |
| neg-02 | amount `1000000` (Endaoment USDC micro-units, unconverted) | `/amount/value` pattern |
| neg-03 | amount `25000` as a JSON number (Chariot cents) | `/amount/value` type |
| neg-04 | amount `0.00` | `/amount/value` not |
| neg-05 | amount `1.234567` (sub-cent USDC) | `/amount/value` pattern |
| neg-06 | status `PendingLiquidation` (Endaoment raw) | `/status` enum |
| neg-07 | anonymity `false` (Chariot boolean) | `/anonymity` enum |
| neg-08 | status paid, no payment_reference | `/` required (if/then) |
| neg-09 | status paid, payment_reference without paid_date | `/payment_reference` required (if/then) |
| neg-10 | no grant_id | `/` required |
| neg-11 | purpose `{}` | `/purpose` anyOf |
| neg-12 | `SC020000` labelled support_strategy | `/purpose/codes/0` oneOf |
| neg-13 | NTEE `E91` (Endaoment's recipient `nteeCode` example) as purpose | `/purpose/codes/0/vocabulary` const (+ oneOf) |
| neg-14 | purpose text of 512 characters | `/purpose/text` maxLength |
| neg-15 | six PCS codes | `/purpose/codes` maxItems |
| neg-16 | extra `donor_email` field | `/` additionalProperties |
| neg-17 | recipient `{}` | `/recipient` anyOf |
| neg-18 | recommended_at `2026-06-10` | `/dates/recommended_at` pattern |
| neg-19 | currency `usd` | `/amount/currency` pattern |
| neg-20 | schema_version `0.2` | `/schema_version` const |

**The validator.**
- **Keywords.** It implements `type`, `enum`, `const`, `pattern`, `minLength`, `maxLength`, `minItems`, `maxItems`, `uniqueItems`, `required`, `properties`, `additionalProperties`, `items`, `allOf`, `anyOf`, `oneOf`, `not`, `if`/`then`/`else` and local `$ref`.
- **Annotations ignored:** `$schema`, `$id`, `$comment`, `$defs`, `title`, `description`, `default` and `examples`.
- **Any other keyword fails the run.**
- **Equality follows JSON semantics.** `false` ≠ `0` and key order is ignored. The self-test covers both.
- **Style.** Each keyword is a pure function returning a tuple of errors. There is no mutable global state.

---

## 6. Relation to other schemas [R/I]

- **360Giving 1.4.**
  - `grant_id` with an org-id prefix, `recipient` as `US-EIN-…`, and `purpose.codes` as `{vocabulary, code}` mirror 360Giving's `id`, `recipientOrganization/0/id` and `classifications/0/{vocabulary, code}`.
  - `payment_reference.reference` corresponds to `disbursementTransaction/0/id`.
  - 360Giving still has no fund, donor-disclosure or status field, so those would be lost in a round trip (P-B4013-03-02-03).
- **Form 990 Schedule I.** It requires only the EIN in full, plus an annual amount and a free-text purpose (b40n13-03 §3.3). Every v0.1 record therefore carries more than the public return, and none of the extra fields is needed for tax filing.
- **Federal GSDM / GDS v3.0.** Not reconsidered. grants.gov was still unread (P-B4013-03-01).

## 7. Limits

- **Draft, unendorsed.** The schema was not reviewed by any sponsor, by Chariot or Endaoment, by Candid or by 360Giving.
- **Example payloads, not live data.**
  - Chariot's shapes are "recommended shapes" ("Chariot does not require you to implement an exact API specification").
  - The Endaoment vector is assembled from per-field OpenAPI `example` values that were never meant to describe one coherent grant: the uuids coincide, the EIN comes from a response DTO, and the example status is outside its enum.
  - Chariot's EIN comes from a separate endpoint's example, linked by `org_77fq`.
- **Hand mappings.** 11 of the 20 transformed entries use `manual` transforms [C]: pos-01 has 3, pos-02 has 4 and pos-03 has 4. They cover PCS coding of "Wherever needed most", the scheme labels, currency, Endaoment anonymity, the onchain rail, and Chariot's approval time taken from `updated_at` [I]. The other 9 are recomputed by the validator. Manual entries cannot be recomputed, only reviewed.
- **PCS codes are checked for shape only.** The code list was robots-blocked, so a well-formed but non-existent code passes (§4.3). Only the S, P, U and T facets are accepted.
- **Amount.** Only two-decimal currencies fit. Currencies with zero or three minor digits (JPY, BHD) would need a rule keyed to the ISO 4217 minor unit. The currency code is checked for shape, not against the ISO list. Recording USDC as USD is [I].
- **Validator subset.** Timestamp and date checks are regex only (2026-02-31 would pass). `format` is not used. Only local `$ref` is resolved. The schema itself was not validated against the 2020-12 metaschema, because no package could be installed (P-B4013-03-02-04).
- **The vector generator is in the scratchpad** (`q1332/make_vectors.py`), which may be cleared. The vector files themselves are self-contained.

## 8. Data dictionaries

### 8.1 Vector files (`standards/daf-grant-record/vectors/*.json`)

| Key | Meaning |
|---|---|
| `vector_id` | File stem. `pos-` = must validate, `neg-` = must fail |
| `description` | What the vector is |
| `expect` | `valid` or `invalid` |
| `schema` | Relative path to the schema |
| `status_label` | Always "draft, unendorsed" |
| `sources` | Positive vectors: source URL, retrieval date, cache file, sha256 (and OpenAPI version) |
| `field_provenance[]` | Positive converted vectors. `record_path` (JSON pointer); `conversion` (exact / renamed / transformed / not_available); `source_field`; `source_url`; `source_snippet` (verbatim text checked against the cache); `source_value` (pre-conversion value); `transform` (named and recomputed, or `manual`); `note` |
| `source_fields_not_carried` | Source fields deliberately left out of the record |
| `derived_from`, `mutations[]` | Negative vectors: the base positive vector and the single change (`<deleted>` = removed) |
| `expected_errors[]` | Negative vectors: `instance_path` and `keyword` that must appear among the errors |
| `record` | The record under test |

### 8.2 `queue-proposals-b4013-03-02.csv` (6 rows, 17 columns)

Same header and format as `queue-proposals-gap19-13.csv`:
- `question_id`, `question`, `area`;
- the scores `importance`, `p_change`, `gap`, `commercial`, `availability`, `effort` (1–5, except `p_change`, a probability);
- `depends_on`, `breadth_gap` (yes/no), `state`, `assigned_to`;
- `conclusion_affected`, `proposed_by`, `rationale`, `evidence_pointer`.

## 9. Suggested corrections (not applied)

### `research/mission-2026-11-14/direction-data-standards-interoperability.md`
- **Find:** "The [developer page](https://developer.candid.org/docs/candids-taxonomy) states no licence."
- **Replace with:** "The [developer page](https://developer.candid.org/docs/candids-taxonomy) states no licence, but Candid's PCS site does, first-hand: “The PCS is available for use under a Creative Commons Attribution 4.0 International license” (taxonomy.candid.org, read 2026-11-20; the date of the change is not stated) [b4013-03-02]"

### `data/mission-2026-11-14/daf-data-standards-2026.csv` (row DS15)
- **Find:** "Licence text not read first-hand"
- **Replace with:** "Licence read first-hand on taxonomy.candid.org (CC BY 4.0, 2026-11-20); full code list robots-blocked (/content/*) [b4013-03-02]"

## 10. Source register

| ID | Source | Read | Used for |
|---|---|---|---|
| S1 | [Chariot DAFpay OAuth: API Endpoints (v2026-04-01)](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md). Cache q1303/std/cfc76e7268828bd5, sha256 8c17df40… | 2026-11-19 (cached) | Vectors pos-01, pos-02; §3.3 |
| S2 | [Endaoment: Create async grant](https://docs.endaoment.org/developers/api/transfers/create-an-async-grant-request.md), embedding `https://api.endaoment.org/oas-json` v4.88.0. Cache q1303/std/9955741ee77ac16b, sha256 7790bd52… | 2026-11-19 (cached) | Vector pos-03; §3.3 |
| S3 | [Candid PCS home](https://taxonomy.candid.org/) | 2026-11-20 | Licence quote §4.1 |
| S4 | [PCS Downloads](https://taxonomy.candid.org/resources/downloads); [Full PCS Taxonomy with Definitions](https://taxonomy.candid.org/resources/downloads/full-pcs-taxonomy-with-definitions2) | 2026-11-20 | Release, file name, footer licence; xlsx robots-blocked |
| S5 | [PCS FAQ](https://taxonomy.candid.org/resources/pcs-faq) | 2026-11-20 | Update cycle, NTEE relation, crosswalk |
| S6 | [PCS Support Strategies](https://taxonomy.candid.org/support-strategies); [Subjects](https://taxonomy.candid.org/subjects) | 2026-11-20 | Up-to-5 grant codes rule |
| S7 | [Candid developer docs: Candid's taxonomy](https://developer.candid.org/docs/candids-taxonomy) | 2026-11-20 | The four PCS example codes |
| S8 | [CC BY 4.0 deed](https://creativecommons.org/licenses/by/4.0/); [legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) | 2026-11-20 | Licence terms §4.2 |
| S9 | `https://data.taxonomy.candid.org/robots.txt` (401) | 2026-11-20 | Blocked [B] |
| R1 | [b40n13-03-g1913-03-schema-and-processor-accounts.md](b40n13-03-g1913-03-schema-and-processor-accounts.md) §3; [`daf-grant-schema-map-2026-11-19.csv`](../../data/mission-2026-11-14/daf-grant-schema-map-2026-11-19.csv) | repo | Draft record, field map |
| R2 | [validation-wave40a-report.md](validation-wave40a-report.md) §8 | repo | Endaoment status correction |
