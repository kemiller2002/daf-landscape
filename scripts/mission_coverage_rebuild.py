#!/usr/bin/env python3
"""Coverage-matrix rebuild from post-baseline evidence (P-GAP19-02), functional style, stdlib only.

Reads the 2026-11-14 matrix (kept unchanged) and writes a NEW matrix:
  data/mission-2026-11-14/coverage-matrix-entities-2026-11-19.csv

Every cell keeps its 2026-11-14 status unless a curated evidence entry below gives a concrete
pointer (validation-register claim id, or dataset + row key, or doc + section). Rules:
  R1  IC only where a validation-register row (any wave) confirms a claim that addresses the
      checklist item for that entity. Register entity names are matched by hand (the old script
      matched exact strings, so rows such as 'DAFgiving360' never reached
      'DAFgiving360 (Schwab Charitable)').
  R2  PV where a register row partially confirms, or confirms only a narrow part of the item
      (one page, one product line, search-index capture only).
  R3  EC where a post-baseline dataset row (or doc section) holds entity-specific evidence on the
      item; DS where it holds only a fragment (e.g. one dated event for 'timeline', a zero-record
      complaint scan, a revenue floor for a private vendor's financials).
  R4  IP where a recorded check shows the item is not publicly available (sponsor SOC reports:
      sponsor-audit-notes.csv soc_report_reference=none; vendor scope: vendor-assurance-scope-2026.csv).
  R5  No downgrade, except where the old cell's only support does not address the item (logged as
      'corrected').
  R6  CE is kept unless a later register row resolves the conflict.

Usage: python3 scripts/mission_coverage_rebuild.py .
"""
import csv
import glob
import os
import sys
from pathlib import Path

STATUS = {
    "NI": "Not investigated", "DS": "Discovery started", "EC": "Evidence collected",
    "PV": "Partially validated", "IC": "Independently corroborated", "CE": "Contradictory evidence",
    "IP": "Insufficient public information", "RC": "Research completed to current evidence standard",
}
RANK = {"NI": 0, "DS": 1, "IP": 1.5, "EC": 2, "PV": 3, "IC": 4, "RC": 5}

E = {
    "REN": "Ren (RenPSG)", "RCF": "Renaissance Charitable Foundation (RCF)", "TIFIN": "TIFIN Give",
    "GCF": "GiveClear Foundation", "FS": "Foundation Source", "CV": "Charityvest", "CHA": "Chariot",
    "DAFFY": "Daffy", "FID": "Fidelity Charitable", "D360": "DAFgiving360 (Schwab Charitable)",
    "VAN": "Vanguard Charitable", "NPT": "National Philanthropic Trust (NPT)",
    "AEF": "American Endowment Foundation (AEF)", "STL": "Stellar Technology Solutions / iPhi",
    "GVG": "Givinga", "EJ": "Edward Jones", "MS": "Morgan Stanley (GIFT)",
    "GS": "Goldman Sachs (two DAF programs)", "BOA": "Bank of America Charitable Gift Fund",
    "TIAA": "TIAA (Charityvest-sponsored DAF)", "ONE": "OneAscent (OneGive)",
    "SEI": "SEI (SEI Charitable Fund)", "PAVE": "Pave Finance", "NCF": "National Christian Foundation",
    "JCF": "Jewish Communal Fund", "SVCF": "Silicon Valley Community Foundation",
    "BEN": "Benevity / workplace processors", "DD": "DAF Direct",
    "CAN": "Candid / IRS BMF (eligibility data)", "GIV": "Give Interactive", "END": "Endaoment",
    "FDT": "Foundant (CommunitySuite)", "NPA": "NPact (FIMS / DonorCentral)",
}

# Register evidence: (entity key, item, grade, claim ids, note). Grade follows R1/R2.
REG = (
    ("FID", "fees", "IC", "V10-05b V2B-09", "fee-page inputs and audited FMR admin-fee note confirmed"),
    ("FID", "custody_invest", "IC", "V11-07a V17-01 V19-26 V22-18 V27-04", "CIAP terms, pool expense ratios and returns confirmed"),
    ("FID", "financials", "IC", "V11-06 V14-26 V17-04 V1-15", "FY2024-25 990/audit lines confirmed"),
    ("FID", "grant_workflow", "IC", "V12-04 V13-04 V21-07 V25B-15 V4-04", "minimum grant, EFT, voids, grant notices confirmed"),
    ("FID", "tech_admin", "IC", "V12-03 V15-12 V7-06", "FMR services agreement and data-export terms confirmed"),
    ("FID", "distribution", "IC", "V26-32", "corporate DAF channel (556 corporate DAFs) confirmed; Empower/eMoney feed partial (V16-23)"),
    ("FID", "distribution", "PV", "V16-23", "data-feed channel partially confirmed"),
    ("FID", "operating_evidence", "IC", "V13-05 V23-26 V24B-15", "app defects and grant/balance metrics confirmed"),
    ("FID", "ai", "IC", "V28-24", "Virtual Assistant described as NL search engine; confirmed"),
    ("FID", "ai", "PV", "V24B-05", "job-posting AI scan partially confirmed"),
    ("VAN", "fees", "IC", "V10-05c", "admin fee and pool fee inputs confirmed"),
    ("VAN", "custody_invest", "IC", "V11-07e V20-19 V27-03 V2B-11", "no adviser-managed option; in-fund ER; pool returns confirmed"),
    ("VAN", "financials", "IC", "V18-13", "FY2024 990 Schedule I line confirmed"),
    ("VAN", "grant_workflow", "IC", "V12-04 V12-05 V26-18", "minimum grant, PayPal Grant Payments, impermissible-grant rules confirmed"),
    ("VAN", "operating_evidence", "IC", "V24B-19 V21-09", "average grant, December share, disaster electronic share confirmed"),
    ("VAN", "timeline", "PV", "V3-07", "Give Interactive recordkeeper timing partially confirmed"),
    ("NPT", "fees", "IC", "V10-05f V25B-28", "fee schedule PDF date and complex-asset minimums confirmed"),
    ("NPT", "custody_invest", "IC", "V11-07b", "adviser-managed minimum confirmed; Wells Fargo investment management partial (V22-20)"),
    ("NPT", "financials", "IC", "V12-02 V14-29 V14-30 V18-16 V18-12", "FY2025 990 IT expense, Schedule I and summary financials confirmed"),
    ("NPT", "grant_workflow", "IC", "V12-04 V12-05 V18-20", "minimum grant, no ACH / PayPal Grant Payments, EFT check confirmed"),
    ("AEF", "tech_admin", "IC", "V10-07 V12-06 V9-05", "move to Ren 2026-04-06 and legacy DonorCentral/NPact confirmed"),
    ("AEF", "custody_invest", "IC", "V11-07c", "no adviser-fee cap; investment-management fees ~0.46% confirmed"),
    ("AEF", "financials", "IC", "V16-02 V14-03", "990 line 11f computation and Part VII-B payments confirmed (V16-01 partial)"),
    ("AEF", "grant_workflow", "IC", "V16-26", "Ren ACH grant-payment route confirmed"),
    ("RCF", "custody_invest", "PV", "V11-07d", "absence of adviser-fee cap in circulars confirmed only"),
    ("RCF", "grant_workflow", "IC", "V2A-23", "Charity Check vetting policy confirmed (claim moved here from 'assurance')"),
    ("D360", "grant_workflow", "IC", "V12-04", "minimum grant $50 confirmed (2024 document)"),
    ("D360", "operating_evidence", "IC", "V2A-08", "1.5M grants CY2025, 38% recurring confirmed"),
    ("D360", "distribution", "IC", "V22-22", "77% of assets adviser-associated; 5,200+ advisers confirmed"),
    ("D360", "custody_invest", "PV", "V11-09", "pool fund changes confirmed via search-index capture only"),
    ("D360", "fees", "PV", "V11-07f", "one adviser's DAFgiving360 fee menu confirmed"),
    ("MS", "custody_invest", "IC", "V15-10 V17-05", "circular MSSB fees and 990 investment-adviser line confirmed"),
    ("MS", "financials", "IC", "V16-10 V23-14", "990 cost lines confirmed (V17-06/07 partial; V29-05 contradicted a repo recompute, not the filing)"),
    ("MS", "tech_admin", "IC", "V2B-15", "msgift.donorfirstx.com 'DFX powered by Ren' confirmed"),
    ("GS", "grant_workflow", "IC", "V15-09 V18-01", "2024-ratio program circular ($100 min grant, check or wire) confirmed; V18-01 resolves 33C conflict"),
    ("GS", "custody_invest", "IC", "V16-11", "GSAM fund ERs and third-party allocation fees confirmed"),
    ("GS", "ownership_funding", "IC", "V19-06", "Ayco CF merged into GS DAPF 2025-07-01 confirmed"),
    ("GS", "timeline", "DS", "V19-06", "one dated structural event only"),
    ("BOA", "fees", "IC", "V15-11", "Program Guidelines v3.2024 fee tiers confirmed"),
    ("BOA", "custody_invest", "IC", "V28-14 V15-11", "Bank of America as institutional trustee; Private Bank 0.12% investment fee confirmed"),
    ("BOA", "financials", "IC", "V16-12 V19-29", "990 line 11f and Schedule I confirmed"),
    ("BOA", "tech_admin", "IC", "V18-19", "DFX donor guide confirmed"),
    ("EJ", "fees", "PV", "V10-05e", "0.70% program fee confirmed at low confidence; admin tiers contradicted"),
    ("EJ", "financials", "DS", "V18-27", "program-level report figures only (partial); no audited/990 review of the channel"),
    ("TIFIN", "fees", "IC", "V10-05d", "adviser fee cap 1.00% confirmed"),
    ("TIFIN", "distribution", "IC", "V19-20", "Alera Charitable white-label confirmed"),
    ("TIFIN", "ownership_funding", "PV", "V20-20", "separation/sale signals partially confirmed"),
    ("GCF", "grant_workflow", "IC", "V18-14", "90-day void window confirmed"),
    ("GCF", "financials", "PV", "V23-25", "TIFIN Give payment share of operating cost partially confirmed"),
    ("SEI", "legal_role", "IC", "V1-18", "SEI Charitable Fund sponsored by GiveClear confirmed"),
    ("SEI", "tech_admin", "IC", "V1-18", "powered by TIFIN Give confirmed"),
    ("FS", "fees", "PV", "V4-12", "fee paid by Charityvest disclosed in audited note (no published price list)"),
    ("FS", "ai", "IC", "V22-07 V28-25", "AI focus statements (internal use, roadmap) confirmed"),
    ("CV", "tech_admin", "IC", "V1-07", "Foundation Source technology confirmed"),
    ("CHA", "grant_workflow", "IC", "V10-06 V25B-13 V22-26", "DAFpay credential flow, grant-letter ID, account controls confirmed"),
    ("CHA", "operating_evidence", "IC", "V20-25", "94.57% electronic grant payments (vendor statement) confirmed; V21-10, V29-15 partial"),
    ("CHA", "ownership_funding", "IC", "V22-03", "Form D $11.0m equity confirmed"),
    ("CHA", "ai", "IC", "V24B-06", "AI job titles confirmed; AI agent claim partial (V2A-13)"),
    ("DAFFY", "grant_workflow", "IC", "V26-18", "pledge / split-ticket grant rules confirmed"),
    ("DAFFY", "distribution", "PV", "V21-14", "financial-adviser delegate route partially confirmed"),
    ("STL", "operating_evidence", "IC", "V11-01a", "iPhi tenant attrition 6/57 reproduced"),
    ("STL", "timeline", "IC", "V17-26 V23-11", "acquired-codebase status and archive dates confirmed"),
    ("REN", "operating_evidence", "PV", "V11-01a", "retention evidence for the iPhi line only"),
    ("REN", "grant_workflow", "IC", "V16-25 V16-26", "Ren for Charities ACH code and FAQ confirmed"),
    ("REN", "financials", "PV", "V22-01 V16-10", "named Ren receipts from sponsor 990s confirmed (revenue floor; corporate financials not public)"),
    ("REN", "distribution", "IC", "V25B-21 V2B-15", "Giving Block crypto DAF partnership and MS GIFT DFX confirmed"),
    ("REN", "ai", "PV", "V28-24", "giving-platform page has no AI terms (one page)"),
    ("GVG", "fees", "IC", "V15-17", "partner programme 0.30% fee confirmed"),
    ("GVG", "distribution", "IC", "V15-17", "Janus Henderson partner programme confirmed"),
    ("GVG", "tech_admin", "IC", "V15-17", "Givinga Inc. technology for Givinga Foundation confirmed"),
    ("GVG", "ownership_funding", "PV", "V17-23", "Form D equity offering partially confirmed"),
    ("GVG", "ai", "PV", "V28-24", "homepage has no AI terms (one page)"),
    ("GVG", "legal_role", "PV", "V23-12", "account-basis statement partially confirmed"),
    ("END", "financials", "IC", "V14-24 V15-20 V16-16 V17-13 V28-07", "FY2022-25 990s vs audits confirmed"),
    ("END", "fees", "IC", "V15-21", "fee schedule scope and Altruist admin tiers confirmed"),
    ("END", "grant_workflow", "IC", "V15-22 V25B-14", "OpenAPI grant submission and settlement confirmed"),
    ("END", "distribution", "IC", "V5-07 V21-16", "Altruist DAFs sponsored by Endaoment; API/OAuth integration terms confirmed"),
    ("END", "timeline", "DS", "V4-01", "one dated event (Altruist launch) only"),
    ("END", "legal_role", "PV", "V2A-18", "sponsor-of-record API tiers partially confirmed"),
    ("NPA", "legal_role", "IC", "V10-02 V12-08 V16-27 V16-28", "Fusion Laboratories LLC dba NPact (terms, W-9) confirmed"),
    ("NPA", "tech_admin", "IC", "V12-06 V13-03 V14-02 V14-08", "DonorCentral/FIT/Foundation Cloud operation confirmed"),
    ("NPA", "ownership_funding", "IC", "V11-08a", "BroadWest acquisition closing 2020-12-30 confirmed"),
    ("NPA", "financials", "DS", "V14-03", "AEF payments to NPact only (revenue floor; private company)"),
    ("SVCF", "tech_admin", "IC", "V13-01 V14-01", "NetSuite + NPact FIT confirmed"),
    ("SVCF", "grant_workflow", "IC", "V8-10", "DAF grants paid by check confirmed"),
    ("SVCF", "financials", "IC", "V18-12 V11-05b", "990 Schedule I flows confirmed"),
    ("SVCF", "distribution", "IC", "V26-33", "corporate-advised-fund channel grants confirmed"),
    ("SVCF", "legal_role", "PV", "V8-08", "fund-agreement clause partially confirmed"),
    ("JCF", "grant_workflow", "IC", "V26-06", "vetting and payment policy (JCF NY) confirmed"),
    ("JCF", "operating_evidence", "IC", "V26-07", "FY2023 grant counts and median grant confirmed"),
    ("JCF", "financials", "IC", "V20-17", "FY2024-25 990 Part VII-B and IT spend confirmed"),
    ("JCF", "tech_admin", "DS", "V20-17", "990 shows no platform vendor; provider still unidentified"),
    ("NCF", "fees", "IC", "V10-05c", "fee tiers confirmed"),
    ("NCF", "grant_workflow", "IC", "V26-05", "grant eligibility and ACH/wire policy confirmed"),
    ("NCF", "custody_invest", "IC", "V27-11", "pool relaunch 2026-09-01 confirmed"),
    ("NCF", "tech_admin", "PV", "V6-05", "Salesforce-based portal, eGrants partially confirmed"),
    ("BEN", "financials", "IC", "V19-09 V19-11 V20-01 V26-34", "AOGF 990 FYE 2026-03 confirmed"),
    ("BEN", "tech_admin", "IC", "V19-12", "Benevity paid $54.7m administrative services by AOGF confirmed"),
    ("BEN", "fees", "IC", "V12-04 V9-08", "Cause Support Fee schedule confirmed"),
    ("BEN", "ownership_funding", "PV", "V7-07e", "General Atlantic/TPG stakes partially confirmed"),
    ("BEN", "ai", "PV", "V21-20 V2A-12", "Match Assurance claims partially confirmed"),
    ("BEN", "operating_evidence", "IC", "V24A-21", "2025-06-17 deactivation incident confirmed"),
    ("DD", "legal_role", "IC", "V19-17", "DAF Direct Trust operates dafdirect.org confirmed"),
    ("DD", "ownership_funding", "IC", "V19-17", "Trust owns the Widget confirmed"),
    ("DD", "fees", "IC", "V25B-11", "no fees confirmed"),
    ("DD", "distribution", "IC", "V25B-11 V24B-11", "three participating sponsors; donate-page placements confirmed"),
    ("CAN", "distribution", "IC", "V28-35", "GuideStar search in BofA CGF guide; Groundswell integration confirmed"),
    ("CAN", "grant_workflow", "IC", "V15-06 V15-07", "Charity Check report content and BMF date confirmed"),
    ("GIV", "ownership_funding", "IC", "V3-10", "validator primary-source finding: Signatry controls Give Interactive LLC (Schedule R)"),
    ("GIV", "timeline", "IC", "V23-04 V5-12", "company timeline and WaterStone launch date confirmed"),
    ("GIV", "operating_evidence", "PV", "V15-32 V3-08 V23-03", "tenant churn and client-asset totals partially confirmed"),
    ("FDT", "ownership_funding", "IC", "V18-24", "SmartSimple merger 2024-08-13 and GivingData May 2025 confirmed"),
    ("FDT", "timeline", "PV", "V18-18 V18-24", "dated product and merger events confirmed; no full timeline"),
    ("TIAA", "timeline", "DS", "V4-08", "one partially confirmed event"),
    ("ONE", "ownership_funding", "PV", "V1-22", "ADV indirect equity interest in the tech vendor (one disclosure)"),
)

# Dataset / document evidence: (entity key, item, grade, pointer, note). Grade follows R3/R4.
DS_EV = (
    ("AEF", "fees", "EC", "sponsor-fee-schedules.csv [sponsor=American Endowment Foundation]; all-in-cost-comparison-2026.csv", "published fee rows"),
    ("AEF", "timeline", "EC", "company-timeline-events.csv [CT095 CT127 CT155 CT157 CT186]", "five dated events 2024-2026"),
    ("BOA", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=Bank of America Charitable Gift Fund: document_status=not_public; soc_report_reference=none]", "SOC reports not public"),
    ("BOA", "operating_evidence", "DS", "complaint-rates-normalised.csv [sponsor=BofA Charitable Gift Fund: 0 records]", "complaint scan found no records"),
    ("BEN", "distribution", "EC", "corporate-daf-programs-2021-2026.csv [SA03]; charity-data-provider-integrations-2026.csv", "corporate DAF-column accounts"),
    ("BEN", "legal_role", "EC", "pass-through-sponsors-2026.csv [American Online Giving Foundation]; relationship-graph-nodes.csv", "AOGF legal form and owner"),
    ("BEN", "ownership_funding", "EC", "pe-ownership-by-company.csv [company=Benevity]", "owner rows"),
    ("CAN", "assurance", "IP", "vendor-assurance-scope-2026.csv [vendor=Candid: vendor_claim_only; scope not public]", "self-reported SOC 2, no scope"),
    ("CAN", "distribution", "EC", "charity-data-provider-integrations-2026.csv [provider=Candid rows]", "integrator list"),
    ("CV", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=Charityvest: read; soc_report_reference=none]", "SOC reports not public"),
    ("DD", "timeline", "EC", "company-timeline-events.csv [CT017 CT018 CT020 CT191]", "four dated events"),
    ("D360", "tech_admin", "EC", "form990-top-contractors.csv [EIN=31-1640316 FY2024-25: Charles Schwab & Co 'BROKERAGE & ADMIN SERVICES']", "administrator from 990"),
    ("DAFFY", "tech_admin", "EC", "breadth-entity-profiles.csv [Daffy Charitable Fund: self]; sponsor-eft-providers-2026.csv [Daffy: Chariot Disbursements]", "self-built platform; payments vendor named"),
    ("END", "operating_evidence", "DS", "complaint-rates-normalised.csv [sponsor=Endaoment: 0 records]", "complaint scan found no records"),
    ("END", "tech_admin", "EC", "breadth-entity-profiles.csv [Endaoment: self]; vendor-data-rights-matrix.csv", "self-built API"),
    ("FID", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=Fidelity Charitable: read FY2025; soc_report_reference=none]", "SOC reports not public"),
    ("FDT", "ai", "EC", "philanthropy-ai-products-2026.csv [AIP11 Fia, beta]; agent-delegation-terms-2026.csv", "AI product listed, beta"),
    ("FDT", "financials", "DS", "vendor-footprint-from-990.csv [vendor=Foundant Technologies: 6 sponsors, $1.36m]", "revenue floor only; private company"),
    ("FDT", "distribution", "EC", "cf-vendor-map-by-ein-v2.csv [portal_vendor=Foundant CommunitySuite: 413 CFs]; research/mission-2026-11-14/queue-cf-vendor-map.md §3", "client footprint by EIN"),
    ("FDT", "timeline", "EC", "cf-vendor-migrations-2022-2026.csv [event rows: iPhi -> Foundant 2025-05-14, 2026-06-01]", "migration dates"),
    ("GCF", "fees", "EC", "all-in-cost-comparison-2026.csv [TIFIN Give (GiveClear Foundation sponsor)]", "program fee rows"),
    ("GCF", "timeline", "EC", "company-timeline-events.csv [CT028 CT107 CT141 CT143 CT149 CT185]", "six dated events"),
    ("GCF", "ai", "EC", "philanthropy-ai-products-2026.csv [AIP01 Louise, sponsor GiveClear]", "AI product on GiveClear-sponsored DAFs"),
    ("GCF", "operating_evidence", "IP", "complaint-rates-normalised.csv [GiveClear Foundation: 0 records]", "kept IP; no operating data published"),
    ("GVG", "ownership_funding", "EC", "pe-ownership-by-company.csv [company=Givinga]; emerging-entrants-funding-ai.csv", "investor rows"),
    ("GVG", "ai", "EC", "philanthropy-ai-products-2026.csv [AIP10: none found]", "AI scan: none"),
    ("GS", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=Goldman Sachs Philanthropy Fund: not_public; soc_report_reference=none]", "SOC reports not public"),
    ("GS", "operating_evidence", "EC", "complaint-rates-normalised.csv [GS DAPF: 1 record]; daf-user-complaints-corpus.csv", "complaint rate"),
    ("GS", "ownership_funding", "EC", "pe-ownership-by-company.csv [company=Ayco; owner=Goldman Sachs, 2003]", "affiliate ownership"),
    ("JCF", "custody_invest", "EC", "sponsor-investment-menus-2026.csv [sponsor=Jewish Communal Fund]; form990-top-contractors.csv [EIN=23-7174183 investment managers]", "investment menu and managers"),
    ("JCF", "tech_admin", "DS", "faith-sponsor-platforms-2026.csv [Jewish Communal Fund (New York): not confirmed; Give Interactive staging tenants]", "lead only"),
    ("MS", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=Morgan Stanley GIFT: not_public; soc_report_reference=none]", "SOC reports not public"),
    ("MS", "operating_evidence", "EC", "complaint-rates-normalised.csv [Morgan Stanley GIFT: 1 record]; daf-user-complaints-corpus.csv", "complaint rate"),
    ("MS", "timeline", "DS", "company-timeline-events.csv [CT087]", "one dated event"),
    ("NPA", "financials", "DS", "vendor-footprint-from-990.csv [vendor=NPact: AEF $673k TY2022-24]", "revenue floor only; private company"),
    ("NPA", "distribution", "EC", "cf-vendor-map-by-ein-v2.csv [portal_vendor=Foundation Cloud portal (spectrumportal.net): 17 CFs]; spectrumportal-tenant-audit.csv", "client footprint"),
    ("NPA", "timeline", "DS", "company-timeline-events.csv [CT095]; validation-register-wave11.csv#V11-08a", "two dated events"),
    ("NCF", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=NCF: read 2025; soc_report_reference=none]", "SOC reports not public"),
    ("NCF", "operating_evidence", "EC", "daf-user-complaints-corpus.csv [organization=National Christian Foundation]; complaint-rates-normalised.csv", "complaint records"),
    ("NPT", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=NPT: summary_only; soc_report_reference=none]", "SOC reports not public"),
    ("RCF", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=RCF: read 2024; soc_report_reference=none]", "corrected: old IC rested on V2A-23 (vetting policy, not SOC)"),
    ("RCF", "custody_invest", "EC", "sponsor-investment-menus-2026.csv [RCF]; infund-expense-nationals-2026.csv [N092]", "menu rows"),
    ("RCF", "operating_evidence", "IP", "complaint-rates-normalised.csv [RCF: 0 records]; sponsor-service-levels-2026.csv", "kept IP"),
    ("REN", "ai", "EC", "philanthropy-ai-products-2026.csv [AIP08: none found]; daf-hiring-signals-2026.csv [org=Ren: 6 postings, no AI titles]", "AI scan: none"),
    ("REN", "operating_evidence", "EC", "ren-iphi-tenant-census.csv; data/mission-2026-11-14/ren-iphi-attrition-summary.json", "tenant census"),
    ("SEI", "timeline", "DS", "company-timeline-events.csv [CT147 CT185]; research/mission-2026-11-14/queue-batch35-access-owners-faith.md §3", "two dated events"),
    ("SEI", "ownership_funding", "DS", "research/mission-2026-11-14/queue-batch35-access-owners-faith.md §3 (SEI as TIFIN investor, edge E051)", "parent-side fact only"),
    ("SVCF", "custody_invest", "EC", "sponsor-investment-menus-2026.csv [Silicon Valley Community Foundation]", "menu row"),
    ("SVCF", "fees", "EC", "cf-daf-fee-census-2026.csv [ein=205205488]", "fee schedule row"),
    ("SVCF", "operating_evidence", "EC", "daf-user-complaints-corpus.csv [CMP-235]; sponsor-service-levels-2026.csv", "complaint and service-level rows"),
    ("STL", "ownership_funding", "EC", "company-funding.csv [Stellar Technology Solutions]; acquired-codebase-status-2026.csv; pe-ownership-by-company.csv", "acquisition rows"),
    ("TIAA", "timeline", "DS", "company-timeline-events.csv [CT179]", "one dated event"),
    ("TIFIN", "assurance", "IP", "vendor-assurance-scope-2026.csv [TIFIN Give: vendor_claim_only; trust center gated]", "scope not public"),
    ("TIFIN", "operating_evidence", "EC", "grant-latency-statements-2026.csv [L13]; validation-register-wave21.csv#V21-10", "turnaround statement"),
    ("VAN", "ai", "EC", "daf-hiring-signals-2026.csv [org=Vanguard Charitable: 4 postings, no AI titles]", "job-posting AI scan"),
    ("VAN", "assurance", "IP", "sponsor-audit-notes.csv [sponsor=Vanguard Charitable: read FY2026; soc_report_reference=none]", "SOC reports not public"),
    ("CHA", "operating_evidence", "EC", "grant-latency-statements-2026.csv; daf-user-complaints-corpus.csv", "latency and complaints"),
    ("EJ", "financials", "DS", "research/mission-2026-11-14/queue-batch33-market-structure.md §4.1 (ER015)", "program report; 10-K route not tried (P-GAP19-07)"),
)

CORRECTIONS = {("RCF", "assurance")}  # R5: old IC whose only support did not address the item


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def register_index(directory):
    """claim_id -> tuple of (file, wave label, validation_result)."""
    idx = {}
    for path in sorted(glob.glob(os.path.join(directory, "validation-register*.csv"))):
        name = os.path.basename(path)
        wave = name[len("validation-register"):-4].lstrip("-").replace("wave", "") or "1"
        for r in read_rows(path):
            idx.setdefault(r["claim_id"], []).append((name, wave, r["validation_result"]))
    return idx


def reg_entries(idx):
    def one(key, item, grade, ids, note):
        hits = tuple((cid, h) for cid in ids.split() for h in idx.get(cid, ())[:1])
        missing = [cid for cid in ids.split() if cid not in idx]
        if missing:
            raise SystemExit(f"unknown claim ids {missing}")
        pointer = "; ".join(f"{h[0]}#{cid}" for cid, h in hits)
        waves = "; ".join(f"wave {h[1]} {cid} ({h[2]})" for cid, h in hits)
        label = "validated" if grade == "IC" else "partially validated" if grade == "PV" else "register context"
        return (E[key], item, grade, pointer, f"{label}: {waves}", note)
    return tuple(one(*r) for r in REG)


def ds_entries():
    return tuple((E[k], item, g, "data/mission-2026-11-14/" + p if not p.startswith("research/") else p, "", n)
                 for k, item, g, p, n in DS_EV)


def decide(old, evidence, corrected):
    """Return new status code given old code and evidence grades (R1-R6)."""
    grades = [g for g, *_ in evidence]
    if corrected:
        return max(grades, key=lambda g: RANK[g]) if grades else "NI"
    if not grades:
        return old
    best = max(grades, key=lambda g: RANK[g])
    if old == "CE":
        return "CE"
    if old == "IP" and best in ("DS", "IP"):
        return "IP"
    return best if RANK[best] > RANK[old] else old


def validation_for_old_ic(old_rows_validated, key):
    return old_rows_validated.get(key, "")


def old_ic_validation(directory):
    """Exact-name confirmed rows (how the 2026-11-14 script assigned IC)."""
    out = {}
    for path in sorted(glob.glob(os.path.join(directory, "validation-register*.csv"))):
        name = os.path.basename(path)
        wave = name[len("validation-register"):-4].lstrip("-").replace("wave", "") or "1"
        for r in read_rows(path):
            if r["validation_result"].lower() == "confirmed" and r["checklist_item"]:
                out.setdefault((r["entity"], r["checklist_item"]), []).append(f"wave {wave} {r['claim_id']}")
    return {k: "; ".join(v) for k, v in out.items()}


def rebuild(old_rows, evidence, old_val):
    by_cell = {}
    for ent, item, grade, ptr, val, note in evidence:
        by_cell.setdefault((ent, item), []).append((grade, ptr, val, note))
    inv = {v: k for k, v in E.items()}

    def row(r):
        key = (r["entity"], r["checklist_item"])
        ev = by_cell.get(key, [])
        corrected = (inv.get(r["entity"]), r["checklist_item"]) in CORRECTIONS
        old = r["status_code"]
        new = decide(old, ev, corrected)
        change = ("corrected" if corrected else "unchanged" if new == old
                  else "relabelled" if new == "IP" else "upgraded")
        vals = [v for _, _, v, _ in ev if v]
        if old == "IC" and not corrected:
            vals = [f"validated (2026-11-14 exact-name match): {old_val.get(key, 'n/a')}"] + vals
        pointers = [p for _, p, _, _ in ev]
        return {
            "entity": r["entity"], "segment": r["segment"], "checklist_item": r["checklist_item"],
            "checklist_definition": r["checklist_definition"],
            "status_code": new, "status": STATUS[new], "status_code_2026_11_14": old, "change": change,
            "evidence_pointer": " | ".join(pointers) if pointers else f"baseline only: {r['evidence_files']}",
            "validation_status": " | ".join(vals) if vals else "not validated",
            "rebuild_notes": "; ".join(n for _, _, _, n in ev),
            "baseline_evidence_files": r["evidence_files"], "baseline_notes": r["notes"],
            "assessed_by": "coverage rebuild 2026-11-19 (P-GAP19-02; pointer-based, see rebuild doc)",
        }
    return tuple(row(r) for r in old_rows)


def write_csv(path, records):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    out = root / "data" / "mission-2026-11-14"
    old_rows = read_rows(out / "coverage-matrix-entities.csv")
    idx = register_index(str(out))
    records = rebuild(old_rows, reg_entries(idx) + ds_entries(), old_ic_validation(str(out)))
    unknown = {e for e, *_ in reg_entries(idx) + ds_entries()} - {r["entity"] for r in old_rows}
    if unknown:
        raise SystemExit(f"unknown entities {unknown}")
    write_csv(out / "coverage-matrix-entities-2026-11-19.csv", records)
    from collections import Counter
    print(Counter((r["status_code_2026_11_14"], r["status_code"]) for r in records if r["change"] != "unchanged"))
    print(Counter(r["change"] for r in records))
