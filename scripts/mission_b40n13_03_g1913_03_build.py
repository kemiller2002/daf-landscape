"""P-B40N13-03 / P-G1913-03: build the DAF grant-schema map and the processor account-count CSVs.

Usage: python3 -I scripts/mission_b40n13_03_g1913_03_build.py . [CACHE_LOG ...]
  root       repo root ('.')
  CACHE_LOG  optional log.jsonl files written by the robots-respecting fetcher
             (scratchpad q1303/scripts/get.py). Each line maps a URL to a cached file.
             990 XMLs missing from the cache are fetched from the GivingTuesday mirror
             (an S3 object store with no robots.txt; user agent research-script/1.0).
             If source pages are cached, every quote in both CSVs is checked verbatim.

Outputs (data/mission-2026-11-14/):
  daf-grant-schema-map-2026-11-19.csv
  processor-account-counts-2026-11-19.csv
Prints every figure used in the research note. Stdlib only, no mutable global state.
"""
import csv
import html
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce

RETRIEVED = "2026-11-19"
UA = "research-script/1.0"
OUT = "data/mission-2026-11-14"
PANEL = "data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv"
CORR = "data/mission-2026-11-14/dafrc-corrected-market-totals.csv"
GT = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"
DAFRC = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"

# --- sources -------------------------------------------------------------------------------------
CH_EP = "https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md"
EN_AG = "https://docs.endaoment.org/developers/api/transfers/create-an-async-grant-request.md"
G360 = "https://standard.threesixtygiving.org/en/latest/technical/reference/"
GSDM = "https://tfx.treasury.gov/system/files/2026-11/gsdm-rss-v1.3.xlsx"
GDS = "https://www.grants.gov/data-standards"
I990SI = "https://www.irs.gov/instructions/i990si"
I990SD = "https://www.irs.gov/instructions/i990sd"
FG_DISC = "https://www.forgood.org/legal-pages/charitable-solicitation-disclosures"
GV_SOL = "https://www.givinga.com/solutions"
BB_FAQ = "https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-about-blackbaud-giving-fund-bbgf.html"
MS_BING = "https://support.microsoft.com/en-us/bing/cash-donations-on-bing"
BEN_SSI = "https://go.benevity.com/hubfs/website/legal/Benevity-SSI-Disbursements.pdf"
PP_POL = "https://www.paypal.com/us/webapps/mpp/givingfund/policies/donor-account-policy"

# --- Part A: schema map --------------------------------------------------------------------------
# One row per field of the minimal open DAF grant record (core) plus supporting fields.
# 'q_*' entries are verbatim quotes checked against the cached source when it is available.
SCHEMA_COLS = ["row_id", "record_field", "tier", "proposed_type", "proposed_definition",
               "chariot_field", "chariot_status", "endaoment_field", "endaoment_status",
               "g360_field", "g360_status", "federal_field", "federal_status",
               "form990_location", "form990_requires", "form990_quote", "form990_source", "gap_note",
               "chariot_quote", "endaoment_quote", "g360_quote", "federal_quote"]

SCHEMA = [
    dict(row_id="SM-01", record_field="grant_id", tier="core", proposed_type="string; globally unique as <sponsor org-id>:<sponsor grant id>",
         proposed_definition="Sponsor-issued identifier of one grant, stable from recommendation to payment; prefixed with the sponsor's org-id (US-EIN-#########) as 360Giving prefixes ids",
         chariot_field="response id (e.g. grant_3kd02); request carries Chariot's own id in note", chariot_status="returned (sponsor id); Chariot id required in note",
         endaoment_field="GrantTransferDto.id (uuid)", endaoment_status="returned, required",
         g360_field="id", g360_status="required", federal_field="FAIN (plus URI for aggregates)", federal_status="conditional per validation rule",
         form990_location="none", form990_requires="no", form990_quote="",
         gap_note="No public filing carries a grant id; Schedule I is one row per recipient per year",
         chariot_quote="\"id\": \"grant_3kd02\"", endaoment_quote="description: Unique identifier of the transfer",
         g360_quote="The unique identifier for this grant", federal_quote="FAIN"),
    dict(row_id="SM-02", record_field="fund_id", tier="core", proposed_type="string; sponsor-scoped opaque id (no donor name)",
         proposed_definition="Identifier of the donor-advised fund the grant is drawn from; opaque so it can be shared without naming the donor",
         chariot_field="fund_id", chariot_status="required (from GET /funds)",
         endaoment_field="originFundId (uuid)", endaoment_status="required",
         g360_field="none (fundingOrganization is the funder; grantProgramme/code is the nearest)", g360_status="no field",
         federal_field="none (funding agency/office codes; AssistanceListingNumber is the programme)", federal_status="no field",
         form990_location="Schedule D Part I line 1 counts funds only", form990_requires="no",
         form990_quote="Report in column (a) the total number of donor advised funds", form990_source=I990SD,
         gap_note="Only the two DAF APIs carry a fund id; both grant schemas stop at the funder",
         chariot_quote="\"fund_id\": \"fund_a91x\"", endaoment_quote="description: ID of the fund that is the origin of the grant",
         g360_quote="Grant Programme:Code", federal_quote="AssistanceListingNumber"),
    dict(row_id="SM-03", record_field="recipient_ein", tier="core", proposed_type="string; 9 digits, no hyphen",
         proposed_definition="IRS EIN of the recipient organization; foreign or non-EIN recipients use an org-id scheme instead",
         chariot_field="ein (or organization_id resolved from EIN)", chariot_status="required (EIN or org id)",
         endaoment_field="destinationOrgId (Endaoment uuid); OrgSimpleListingDto.ein in responses", endaoment_status="uuid required; EIN returned",
         g360_field="recipientOrganization/0/id (org-id, e.g. a charity or company number scheme)", g360_status="required (org or individual)",
         federal_field="AwardeeOrRecipientUEI", federal_status="conditional per validation rule (UEI, not EIN)",
         form990_location="Schedule I Part II column (b)", form990_requires="yes",
         form990_quote="Enter the employer identification number (EIN) of the grant recipient.",
         gap_note="Schedule I requires the EIN only for recipients receiving more than $5,000 in the year",
         chariot_quote="Chariot identifies every nonprofit by its EIN.", endaoment_quote="description: IRS Employer Identification Number (EIN) without hyphen",
         g360_quote="Recipient Org:Identifier A globally unique identifier for this organisation.", federal_quote="AwardeeOrRecipientUEI"),
    dict(row_id="SM-04", record_field="amount", tier="core", proposed_type="integer minor units + currency (ISO 4217)",
         proposed_definition="Amount recommended or awarded for this grant, integer cents; currency USD unless stated",
         chariot_field="amount", chariot_status="required (integer cents USD)",
         endaoment_field="requestedAmount", endaoment_status="required (USDC smallest unit, 1000000 = 1 USD)",
         g360_field="amountAwarded + currency (amountDisbursed optional)", g360_status="required",
         federal_field="FederalActionObligation", federal_status="conditional per validation rule",
         form990_location="Schedule I Part II column (d) cash; (e) noncash", form990_requires="partial (annual total per recipient, not per grant)",
         form990_quote="Enter the total dollar amount of cash grants to each recipient organization or entity for the tax year.",
         gap_note="Units differ: cents (Chariot), USDC micro-units (Endaoment), whole currency (360Giving), dollars (FABS)",
         chariot_quote="All monetary amounts are **integer cents in USD**", endaoment_quote="The amount in USDC to be granted, in the smallest currency unit",
         g360_quote="Amount Awarded amountAwarded number", federal_quote="FederalActionObligation"),
    dict(row_id="SM-05", record_field="purpose_code", tier="core", proposed_type="object {vocabulary, code}; plus optional purpose_text <= 511 chars",
         proposed_definition="Coded purpose from a named open vocabulary, with free text kept separate and treated as untrusted input",
         chariot_field="purpose (free text)", chariot_status="field in recommended shape",
         endaoment_field="purpose (free text, maxLength 511)", endaoment_status="required",
         g360_field="classifications/0/vocabulary + classifications/0/code", g360_status="optional",
         federal_field="AssistanceListingNumber (programme code) + AwardDescription (text)", federal_status="required",
         form990_location="Schedule I Part II column (h)", form990_requires="partial (free-text description, no code)",
         form990_quote="Describe the purpose or ultimate use of the grant funds or other assistance.",
         gap_note="Only 360Giving and FABS carry a code; both DAF APIs and Schedule I use free text",
         chariot_quote="\"purpose\": \"Wherever needed most\"", endaoment_quote="maxLength: 511",
         g360_quote="Classifications:Code A codelist value in the chosen vocabulary.", federal_quote="AssistanceListingNumber"),
    dict(row_id="SM-06", record_field="anonymity", tier="core", proposed_type="enum: full_contact | name_only | anonymous",
         proposed_definition="Donor disclosure level chosen for this grant (who the charity is told the donor is)",
         chariot_field="anonymous (boolean)", chariot_status="field in recommended shape",
         endaoment_field="shareMyEmail (boolean, default false); recommender (name, optional)", endaoment_status="optional",
         g360_field="none for donor; recipientIndividual ids are anonymised for individual recipients", g360_status="no donor field",
         federal_field="RecordType 3 (PII-redacted individual recipient)", federal_status="recipient-side only",
         form990_location="none (Schedule B donor data is not public for public charities)", form990_requires="no", form990_quote="",
         gap_note="Booleans in both DAF APIs cannot express the three-way split sponsors publish (full / name only / anonymous)",
         chariot_quote="`anonymous: true` means the donor's name and contact details are withheld from the nonprofit",
         endaoment_quote="Whether to share the fund's donor-of-record email with the receiving",
         g360_quote="Recipient Ind:Identifier recipientIndividual/id", federal_quote="Non-Aggregate Record to an Individual Recipient (PII-Redacted)"),
    dict(row_id="SM-07", record_field="status", tier="core", proposed_type="enum: pending | approved | paid | rejected | canceled | returned",
         proposed_definition="Lifecycle state of the grant; Chariot's five values plus returned (payment came back or check voided)",
         chariot_field="status", chariot_status="required in GET /grants/{id}",
         endaoment_field="asyncStatus (PendingLiquidation | Liquidated | Cancelled); status deprecated", endaoment_status="returned, required",
         g360_field="none (dates and transactions imply state)", g360_status="no field",
         federal_field="ActionType (new, continuation, termination, closeout...)", federal_status="required",
         form990_location="none", form990_requires="no", form990_quote="",
         gap_note="Endaoment states describe liquidation, not approval or payment; no schema has 'returned'",
         chariot_quote="| `paid`     | Payment sent to the nonprofit", endaoment_quote="description: Current status of the async transfer request",
         g360_quote="Update the Last Modified date whenever the status of a grant changes", federal_quote="ActionType"),
    dict(row_id="SM-08", record_field="payment_reference", tier="core", proposed_type="object {rail, reference, paid_date}",
         proposed_definition="Rail (ach | check | paypal | stripe | wire | onchain) and the rail's own reference (ACH trace number, check number, provider transaction id, tx hash), so a bank line can be matched to the grant",
         chariot_field="note (Chariot id must appear on grant letter / remittance advice)", chariot_status="required on remittance, out of band",
         endaoment_field="transactionHash", endaoment_status="returned (nullable)",
         g360_field="disbursementTransaction/0/id", g360_status="optional",
         federal_field="none in FABS (outlays are reported elsewhere)", federal_status="no field",
         form990_location="none (column (d) defines cash grants by method, not reference)", form990_requires="no",
         form990_quote="Cash grants include grants and allocations paid by cash, check, money order, electronic fund or wire transfer",
         gap_note="Only Endaoment's on-chain hash ties the record to the payment; Chariot asks sponsors to copy its id onto the remittance",
         chariot_quote="must appear on the grant letter / remittance advice sent to the nonprofit",
         endaoment_quote="description: Transaction hash of the donation made to the target entity",
         g360_quote="disbursementTransaction/0/id", federal_quote=""),
    dict(row_id="SM-09", record_field="sponsor_id", tier="supporting", proposed_type="string; US-EIN-#########",
         proposed_definition="EIN of the sponsoring organization that legally makes the grant",
         chariot_field="implicit (the sponsor hosts the API)", chariot_status="implicit",
         endaoment_field="implicit (Endaoment)", endaoment_status="implicit",
         g360_field="fundingOrganization/0/id + name", g360_status="required", federal_field="AwardingSubTierAgencyCode / AwardingOfficeCode", federal_status="conditional",
         form990_location="return header (filer EIN)", form990_requires="yes (filer)", form990_quote="",
         gap_note="Needed once records leave the sponsor's own system",
         chariot_quote="", endaoment_quote="", g360_quote="Funding Org:Identifier A globally unique identifier for this organisation.", federal_quote="AwardingSubTierAgencyCode"),
    dict(row_id="SM-10", record_field="idempotency_key", tier="supporting", proposed_type="string (uuid)",
         proposed_definition="Client-supplied key so a retried request never creates a second grant",
         chariot_field="Idempotency-Key header", chariot_status="required",
         endaoment_field="idempotencyKey", endaoment_status="required",
         g360_field="none (publication schema)", g360_status="n/a", federal_field="CorrectionDeleteIndicator (record processing)", federal_status="optional",
         form990_location="none", form990_requires="no", form990_quote="",
         gap_note="Transaction-API concern; not part of a published record",
         chariot_quote="Create Grant **must be idempotent**", endaoment_quote="description: Unique identifier to prevent duplicate grant requests",
         g360_quote="", federal_quote="CorrectionDeleteIndicator"),
    dict(row_id="SM-11", record_field="dates", tier="supporting", proposed_type="recommended_at, approved_at, paid_at (ISO 8601)",
         proposed_definition="Timestamps for recommendation, approval and payment",
         chariot_field="created_at, updated_at", chariot_status="returned",
         endaoment_field="createdAtUtc, updatedAtUtc", endaoment_status="returned, required",
         g360_field="awardDate (+ plannedDates, actualDates, transaction dates)", g360_status="awardDate required",
         federal_field="ActionDate", federal_status="required",
         form990_location="none (tax year only)", form990_requires="no", form990_quote="",
         gap_note="Schedule I gives the tax year, not a grant date",
         chariot_quote="\"created_at\": \"2026-06-10T14:30:00Z\"", endaoment_quote="description: UTC timestamp when the transfer was created",
         g360_quote="Award Date When the decision to award this grant was made.", federal_quote="ActionDate"),
    dict(row_id="SM-12", record_field="restriction_text", tier="supporting", proposed_type="string; untrusted",
         proposed_definition="Binding use restriction the recipient must accept, separate from the purpose code",
         chariot_field="none (purpose only)", chariot_status="no field",
         endaoment_field="specialInstructions", endaoment_status="optional",
         g360_field="description (grant description)", g360_status="required", federal_field="AwardDescription", federal_status="required",
         form990_location="Schedule I Part II column (h) (combined with purpose)", form990_requires="partial",
         form990_quote="Don’t use general terms, such as charitable, educational, religious, or scientific.",
         gap_note="Endaoment alone separates a binding restriction from the stated purpose",
         chariot_quote="", endaoment_quote="Binding instructions for the use of granted assets that the",
         g360_quote="Description A short description of this grant activity.", federal_quote="AwardDescription"),
]

QUOTE_SOURCES = {"chariot_quote": CH_EP, "endaoment_quote": EN_AG, "g360_quote": G360,
                 "federal_quote": GSDM, "form990_quote": I990SI}

# --- Part B: processor returns ------------------------------------------------------------------
# dafrc_fy: the DAFRC panel row this return is compared with ("" = context only).
PROC = [
    dict(row_id="PA-01", entity="AOGF (Benevity)", ein="810739440", obj="202530159349302758", dafrc_fy="2024", role="DAFRC FY2024 basis",
         account_unit="individual workplace donor accounts (micro-donations) plus corporate DAFs, in one column",
         unit_basis="filer note on Sched D Part I line 1; FYE 2026 split of the same population",
         self_quote="AOGF HAS A MICRODONATION DAF MODEL VERSUS A CONVENTIONAL DAF ENDOWMENT MODEL.", self_src="xml",
         count_in_account_stats="no (report separately; at most 695 corporate DAFs on AOGF's own later basis)",
         treatment="Exclude 720,545 from donor-advised account totals and per-account rates; show in a processor-account series; use AOGF's FYE 2026 column (a) of 695 as the DAF count",
         label="F"),
    dict(row_id="PA-02", entity="AOGF (Benevity)", ein="810739440", obj="202641969349302754", dafrc_fy="", role="context: FYE 2025-03 amended",
         account_unit="as PA-01", unit_basis="filer note on Sched D Part I line 1(a)",
         self_quote="AOGF HAS A WORKPLACE GIVING MODEL, WHICH INCLUDES CORPORATE AND INDIVIDUAL DONATIONS (INCLUDING MICRO-DONATIONS) AND VARIOUS FUND STRUCTURES THAT ARE NOT CONVENTIONAL DAF MODELS.",
         self_src="xml", count_in_account_stats="no", treatment="as PA-01", label="F"),
    dict(row_id="PA-03", entity="AOGF (Benevity)", ein="810739440", obj="202642259349301349", dafrc_fy="", role="context: FYE 2026-03 reclassification",
         account_unit="column (a): corporate DAFs with ongoing advice; column (b): individual micro-donation accounts",
         unit_basis="Schedule O Part VI line 4",
         self_quote="INDIVIDUAL DONORS MAY USE THE PLATFORM TO MAKE MICRO-DONATIONS AND RECOMMEND GRANTS TO ELIGIBLE CHARITIES AT OR NEAR THE TIME OF DONATION, WITHOUT ONGOING ADVISORY PRIVILEGES WITH RESPECT TO THEIR DONATIONS.",
         self_src="xml", count_in_account_stats="column (a) 695 yes, as employer DAFs; column (b) no", treatment="Use as the basis for PA-01", label="F"),
    dict(row_id="PA-04", entity="PayPal Charitable Giving Fund", ein="450931286", obj="202422999349301487", dafrc_fy="2023", role="context: CY2023 filed",
         account_unit="consumer donor accounts created by checkout and platform giving", unit_basis="Part III text; donor account policy not readable (403)",
         self_quote="THROUGH OUR PARTNERSHIPS, WE MAKE IT EASY FOR DONORS TO SUPPORT THE CHARITIES THEY CARE ABOUT ON THE WEBSITES AND APPS THEY USE EVERY DAY.",
         self_src="xml", count_in_account_stats="no (separate series)", treatment="as PA-05", label="F"),
    dict(row_id="PA-05", entity="PayPal Charitable Giving Fund", ein="450931286", obj="202533079349301308", dafrc_fy="2024", role="DAFRC FY2024 (imputed 694,979; filed value replaces it under R1)",
         account_unit="consumer donor accounts created by checkout and platform giving", unit_basis="Part III text; donor account policy not readable (403); repo [S] snippet describes a balance with later recommendations",
         self_quote="THROUGH OUR PARTNERSHIPS, WE MAKE IT EASY FOR DONORS TO SUPPORT THE CHARITIES THEY CARE ABOUT ON THE WEBSITES AND APPS THEY USE EVERY DAY.",
         self_src="xml", count_in_account_stats="no (separate series; ongoing-privilege status unverified)",
         treatment="Use filed 380,644, not 694,979; keep out of comparable donor-account totals and per-account complaint rates; report per $ granted", label="F"),
    dict(row_id="PA-06", entity="Givinga Foundation", ein="474172718", obj="202403139349303260", dafrc_fy="2023", role="context: CY2023 filed",
         account_unit="individual and employee giving accounts on employer programs", unit_basis="Part III text; givinga.com/solutions",
         self_quote="Optional individual employee accounts", self_src="web:" + GV_SOL,
         count_in_account_stats="no (separate series)", treatment="as PA-08", label="F"),
    dict(row_id="PA-07", entity="Givinga Foundation", ein="474172718", obj="202522379349301497", dafrc_fy="2024", role="CY2024 original return: Part I amounts blank",
         account_unit="not reported", unit_basis="Schedule D Part I lines 1-4 blank on the original return",
         self_quote="", self_src="", count_in_account_stats="n/a", treatment="Superseded by the amended return (PA-08)", label="F"),
    dict(row_id="PA-08", entity="Givinga Foundation", ein="474172718", obj="202503179349301975", dafrc_fy="2024", role="DAFRC FY2024 ('paper submission'); value matches the e-filed amendment",
         account_unit="individual and employee giving accounts on employer programs (enrolment, not active advising)", unit_basis="Part III text; givinga.com/solutions",
         self_quote="THE GIVINGA FOUNDATION IS A SPONSORING ORGANIZATION BUILT AND DESIGNED TO SUPPORT THE CHARITABLE GIVING ACTIVITIES OF ALL ITS INDIVIDUAL ACCOUNT HOLDERS EQUALLY.",
         self_src="xml", count_in_account_stats="no (separate series; low reliability)",
         treatment="Cite the e-filed amendment (2025-11-13) as the source; exclude from comparable totals; average EOY value is under $2 per account", label="F"),
    dict(row_id="PA-09", entity="Blackbaud Giving Fund (YourCause)", ein="460942102", obj="202312409349300046", dafrc_fy="2022", role="context: last filed count (CY2022)",
         account_unit="employer and campaign giving programs (corporate, matching, peer-to-peer), not donor accounts [I]",
         unit_basis="Part III text; count of a few hundred against $0.5-0.7bn of grants",
         self_quote="THE BLACKBAUD GIVING FUND HARNESSES THE POWER OF CORPORATE GIVING TO MAKE GRANTS FROM DONOR ADVISED FUNDS",
         self_src="xml:202542169349301664", count_in_account_stats="no (program funds, not donor accounts)", treatment="as PA-10", label="F/I"),
    dict(row_id="PA-10", entity="Blackbaud Giving Fund (YourCause)", ein="460942102", obj="202542169349301664", dafrc_fy="2024", role="DAFRC FY2024 (imputed 460; line 1 blank on the return)",
         account_unit="no count filed; DAFRC's 460 is an imputation", unit_basis="Schedule D Part I line 1 blank FY2023-FY2025; amounts filed",
         self_quote="THE BLACKBAUD GIVING FUND ALSO MAKES GRANTS FROM DONOR ADVISED FUNDS THAT SUPPORT PEER TO PEER CHARITABLE GIVING CAMPAIGNS.",
         self_src="xml", count_in_account_stats="no (no filed count)",
         treatment="Do not compute per-account rates; mark the count 'not filed (DAFRC imputed 460)'", label="F"),
    dict(row_id="PA-11", entity="Blackbaud Giving Fund (YourCause)", ein="460942102", obj="202622529349301602", dafrc_fy="", role="context: CY2025 (employee donations reclassified out of DAF)",
         account_unit="no count filed", unit_basis="Schedule O Part III line 3",
         self_quote="BBGF DETERMINED THAT EMPLOYEE DONATIONS MADE THROUGH CSRCONNECT SHOULD NOT BE TREATED BY BBGF AS CONTRIBUTIONS TO DONOR ADVISED FUNDS.",
         self_src="xml", count_in_account_stats="no", treatment="Flag FY2025 DAF dollars as a changed basis", label="F"),
    dict(row_id="PA-12", entity="Network for Good / For Good", ein="680480736", obj="202513039349301631", dafrc_fy="2024", role="DAFRC FY2024 (imputed 1; filed value is also 1)",
         account_unit="one pooled donor-advised fund that every donor gives through; donors name a charity per gift",
         unit_basis="filed count; For Good disclosures",
         self_quote="By donating on our website or partner sites, you are contributing to a donor-advised fund at ForGood, Inc., d/b/a ForGood (“ForGood”), a Delaware nonprofit organization that is tax-exempt under Section 501(c)(3) of the Internal Revenue Code.",
         self_src="web:" + FG_DISC, count_in_account_stats="no (count of funds, not of donors)",
         treatment="The filed 1 is correct for what line 1 asks (number of funds); it is not an account count, so per-account rates are undefined", label="F"),
]

PROC_COLS = ["row_id", "entity", "ein", "role", "tax_period_end", "return_object_id", "return_ts", "amended",
             "dafrc_fiscal_year", "dafrc_number_of_daf_accounts", "dafrc_source_number_of_accounts",
             "filed_l1_col_a_daf_count", "filed_l1_col_b_other_count", "filed_daf_contributions", "filed_daf_grants",
             "filed_daf_eoy_value", "dafrc_minus_filed", "grants_per_account", "eoy_value_per_account",
             "account_unit", "unit_basis", "self_description_quote", "self_description_source",
             "count_in_account_stats", "recommended_treatment", "evidence_label", "xml_url", "retrieved"]

SD_TAGS = {"filed_l1_col_a_daf_count": "DonorAdvisedFundsHeldCnt", "filed_l1_col_b_other_count": "FundsAndOtherAccountsHeldCnt",
           "filed_daf_contributions": "DonorAdvisedFundsContriAmt", "filed_daf_grants": "DonorAdvisedFundsGrantsAmt",
           "filed_daf_eoy_value": "DonorAdvisedFundsVlEOYAmt"}


# --- helpers -------------------------------------------------------------------------------------
def load_cache(logs):
    """Map URL -> cached file. File paths in a log are relative to the log's parent directory."""
    recs = [(p, json.loads(l)) for p in logs if os.path.exists(p) for l in open(p, encoding="utf-8")]
    return {r["url"]: (r["file"] if os.path.isabs(r["file"]) else os.path.join(os.path.dirname(os.path.dirname(p)), r["file"]))
            for p, r in recs if r.get("status") == 200 and r.get("file")}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def read_bytes(cache, url):
    path = cache.get(url)
    return open(path, "rb").read() if path and os.path.exists(path) else fetch(url)


def local(tag):
    return tag.split("}")[-1]


def first(root, tag):
    return next((e.text for e in root.iter() if local(e.tag) == tag), None)


def xml_facts(raw):
    root = ET.fromstring(raw)
    sd = next((e for e in root.iter() if local(e.tag) == "IRS990ScheduleD"), None)
    return {**{k: (first(sd, t) if sd is not None else None) or "" for k, t in SD_TAGS.items()},
            "tax_period_end": first(root, "TaxPeriodEndDt") or "", "return_ts": first(root, "ReturnTs") or "",
            "amended": "yes" if first(root, "AmendedReturnInd") in ("X", "1", "true") else "no",
            "_text": " ".join(" ".join(e.text.split()) for e in root.iter() if e.text and e.text.strip())}


def norm(s):
    s = html.unescape(s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(s.split())


def page_text(raw):
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    return norm(re.sub(r"<[^>]+>", " ", t))


def xlsx_text(raw):
    import io
    import zipfile
    z = zipfile.ZipFile(io.BytesIO(raw))
    return norm(" ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "replace"))
                         for n in z.namelist() if n.endswith(".xml")))


def ratio(a, b, nd=2):
    return f"{int(a) / int(b):.{nd}f}" if a not in ("", None) and b not in ("", None) and int(b) else ""


def panel_index(root):
    with open(os.path.join(root, PANEL), newline="", encoding="utf-8") as f:
        return {(r["ein"], r["fiscal_year_end"]): r for r in csv.DictReader(f)}


def corrected_accounts(root, fy):
    with open(os.path.join(root, CORR), newline="", encoding="utf-8") as f:
        return next(int(r["corrected_value"]) for r in csv.DictReader(f)
                    if r["fiscal_year"] == fy and r["metric"] == "daf_accounts_eoy")


def proc_row(p, facts, panel):
    d = panel.get((p["ein"], p["dafrc_fy"]), {}) if p["dafrc_fy"] else {}
    dval = d.get("number_of_daf_accounts", "")
    fa = facts["filed_l1_col_a_daf_count"]
    return {"row_id": p["row_id"], "entity": p["entity"], "ein": p["ein"], "role": p["role"],
            "tax_period_end": facts["tax_period_end"], "return_object_id": p["obj"], "return_ts": facts["return_ts"],
            "amended": facts["amended"], "dafrc_fiscal_year": p["dafrc_fy"], "dafrc_number_of_daf_accounts": dval,
            "dafrc_source_number_of_accounts": d.get("source_number_of_accounts", ""),
            **{k: facts[k] for k in SD_TAGS},
            "dafrc_minus_filed": (int(dval) - int(fa)) if dval and fa else "",
            "grants_per_account": ratio(facts["filed_daf_grants"], fa or (dval if p["row_id"] == "PA-10" else "")),
            "eoy_value_per_account": ratio(facts["filed_daf_eoy_value"], fa or (dval if p["row_id"] == "PA-10" else "")),
            "account_unit": p["account_unit"], "unit_basis": p["unit_basis"], "self_description_quote": p["self_quote"],
            "self_description_source": (GT.format(p["obj"]) if p["self_src"] == "xml" else
                                        GT.format(p["self_src"].split(":", 1)[1]) if p["self_src"].startswith("xml:") else
                                        p["self_src"].split(":", 1)[1] if p["self_src"].startswith("web:") else ""),
            "count_in_account_stats": p["count_in_account_stats"], "recommended_treatment": p["treatment"],
            "evidence_label": p["label"], "xml_url": GT.format(p["obj"]), "retrieved": RETRIEVED}


def quote_checks(rows, texts):
    def check(row):
        src = row["self_description_source"]
        q = row["self_description_quote"]
        t = texts.get(src)
        return (row["row_id"], "self_description_quote", "n/a" if not q else "unread" if t is None else norm(q) in t)
    return list(map(check, rows))


def schema_checks(texts):
    src_of = lambda r, col: r.get("form990_source", I990SI) if col == "form990_quote" else QUOTE_SOURCES[col]
    pairs = [(r["row_id"], col, r[col], src_of(r, col)) for r in SCHEMA for col in QUOTE_SOURCES if r[col]]
    return [(rid, col, "unread" if texts.get(src) is None else norm(q) in texts[src]) for rid, col, q, src in pairs]


def write(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    cache = load_cache(argv[2:])
    panel = panel_index(root)
    facts = {p["obj"]: xml_facts(read_bytes(cache, GT.format(p["obj"]))) for p in PROC}
    facts.update({o: xml_facts(read_bytes(cache, GT.format(o))) for o in
                  {p["self_src"].split(":", 1)[1] for p in PROC if p["self_src"].startswith("xml:")} - set(facts)})
    prows = [proc_row(p, facts[p["obj"]], panel) for p in PROC]

    web_srcs = {CH_EP, EN_AG, G360, I990SI, I990SD, GV_SOL, FG_DISC}
    texts = {**{u: page_text(open(cache[u], "rb").read()) for u in web_srcs if u in cache},
             **({GSDM: xlsx_text(open(cache[GSDM], "rb").read())} if GSDM in cache else {}),
             **{GT.format(o): norm(f["_text"]) for o, f in facts.items()}}
    checks = quote_checks(prows, texts) + schema_checks(texts)

    out = os.path.join(root, OUT)
    write(os.path.join(out, "daf-grant-schema-map-2026-11-19.csv"), SCHEMA_COLS + ["source_urls", "retrieved"],
          [{**r, "form990_source": r.get("form990_source", I990SI if r["form990_quote"] else ""), "source_urls": " ; ".join([CH_EP, EN_AG, G360, GSDM + " (GSDM v1.3 FABS, core lineage of " + GDS + ", unread)", I990SI]),
            "retrieved": RETRIEVED} for r in SCHEMA])
    write(os.path.join(out, "processor-account-counts-2026-11-19.csv"), PROC_COLS, prows)

    # --- printed figures -------------------------------------------------------------------------
    fy24 = [r for r in prows if r["dafrc_fiscal_year"] == "2024" and r["row_id"] != "PA-07"]
    dafrc_sum = sum(int(r["dafrc_number_of_daf_accounts"]) for r in fy24)
    filed_or_dafrc = [int(r["filed_l1_col_a_daf_count"] or r["dafrc_number_of_daf_accounts"]) for r in fy24]
    corr = corrected_accounts(root, "2024")
    aogf26 = int(facts["202642259349301349"]["filed_l1_col_a_daf_count"])
    print("== processor rows")
    print("\n".join(f"{r['row_id']} {r['entity'][:28]:28} {r['tax_period_end']} dafrc={r['dafrc_number_of_daf_accounts']:>8} "
                    f"({r['dafrc_source_number_of_accounts']}) filed_a={r['filed_l1_col_a_daf_count']:>8} b={r['filed_l1_col_b_other_count']:>7} "
                    f"grants/acct={r['grants_per_account']} eoy/acct={r['eoy_value_per_account']} amended={r['amended']} ts={r['return_ts'][:10]}"
                    for r in prows))
    five_sum = sum(filed_or_dafrc)
    print(f"== FY2024 five processors: DAFRC sum {dafrc_sum:,}; filed-or-DAFRC sum {five_sum:,}; "
          f"corrected market accounts {corr:,}; share {five_sum / corr:.4f}")
    print(f"== comparable series (corrected minus five processors) {corr - five_sum:,}; plus AOGF FYE2026 col (a) {aogf26}: {corr - five_sum + aogf26:,}")
    print(f"== AOGF FYE2026 col (b) {facts['202642259349301349']['filed_l1_col_b_other_count']}")
    print("== quote checks:", sum(1 for c in checks if c[2] is True), "true;",
          sum(1 for c in checks if c[2] is False), "false;", sum(1 for c in checks if c[2] == "unread"), "unread;",
          sum(1 for c in checks if c[2] == "n/a"), "n/a")
    print("\n".join(f"   MISS {c}" for c in checks if c[2] is False))
    req = {r["record_field"]: r["form990_requires"] for r in SCHEMA if r["tier"] == "core"}
    print("== Form 990 requires (core fields):", json.dumps(req))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
