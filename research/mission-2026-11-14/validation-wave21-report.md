# Validation wave 21: batch 36 claims (account metric on an ongoing-advisory basis, blank-return carry-forward, Fidelity rail-share series, latency statements, donor terms on agent delegation, Vanguard and DAFpay clauses, Benevity Match Assurance, DAFpay anonymity data flow, Schwab custodial codes, Candid PDF v2, DAFpay stacking fees, Schwab OSA)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave21.
**Register:** [`validation-register-wave21.csv`](../../data/mission-2026-11-14/validation-register-wave21.csv), rows V21-01 to V21-27.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching a page and skipped what it excluded (details under Limits). I do not reproduce credentials. For each claim I formed a verdict from primary sources first and compared it with the batch-36 documents afterwards. The sources were:
- **Script, re-run:** `scripts/mission_account_metric.py accounts --fetch`, in a scratch copy of `scripts/` and `data/mission-2026-11-14/` so that repo outputs were not overwritten. It fetched the eight returns itself. The rebuilt `dafrc-market-accounts-restated.csv` is **byte-identical** to the repo file, and the rebuild check against `dafrc-corrected-market-totals.csv` has a maximum absolute difference of 0. The `rails` task was not re-run; its rows were checked against the pages instead.
- **Independent arithmetic** from `dafrc-sponsor-schedule-d-fy2019-2024.csv` and `dafrc-corrections-itemized.csv` (AOGF, Givinga, PPGF and CF of Middle Tennessee rows).
- **IRS XML, re-parsed** with my own regexes (GivingTuesday mirror): AOGF FYE 2026-03 and FYE 2025-03 (amended), Givinga CY2024 (amended), PPGF CY2024, Blackbaud Giving Fund CY2025, Give Back Foundation CY2025, Network for Good CY2024, Philanthropi CY2024. IRS `index_2026.csv`: HEAD only.
- **Documents and pages:**
  - Fidelity Charitable Giving Reports 2023–2026 (PDF; `pdftotext`, `pdfinfo`);
  - Vanguard Charitable release of 2023-09-20 (PR Newswire), Policies & Guidelines page and Form VCIP 081426;
  - Charityvest grant-status guide; AssetMark Charitable help article; Chariot TIFIN Give case study;
  - Daffy Member Agreement (2025-11-11) and docs.daffy.org/agents;
  - Endaoment T&C (2026-08-12), developer overview and "Going to Production";
  - DAFpay Donor Terms (effective 2025-09-24);
  - Benevity Live! 2026 release, AI blog, AI CSR platform page, Responsible AI Policy and community release spotlight;
  - Chariot v2026-04-01 OAuth API-endpoints guide and Get Grant reference; help page "OAuth For DAF Sponsors"; pricing page;
  - BridgeFT registration-type reference; Candid PDF v2 changelog and verification guide;
  - Schwab Online Services Agreement (schwab.com/legal/terms); DAFgiving360 2024 Program Policies (PDF);
  - Bloomerang, Donorbox (DAF page and pricing), Funraise help, BetterWorld help and Givebutter help.
- **Methodology:** `evidence-quadrant-methodology.md` §7 (AI overlay vocabulary) and `quadrant-v11-rescore.md` §3.

## Headline

Batch 36's numbers reproduce, and its quotes are verbatim. Three results hold independently:
- **The account restatement.** A1 is 1,122,971, 2,495,659, 2,352,992 and 2,589,633 accounts for FY2021–24. A2 (also excluding Givinga and PPGF) is 597,569 to 787,978. Each follows from the corrected totals minus AOGF's filed count plus its 695 FYE 2026 DAFs. The 0.5977 grant share and the 0.7674 EOY share come straight from AOGF's FYE 2026 Schedule D.
- **The blank-return variants.** B1 runs from −$25.3m (FY2022) to +$169.6m (FY2023) of assets, and B2 from +$41.3m to +$170.6m. DAFRC's CF of Middle Tennessee imputations lie exactly on the FY2019–FY2023 straight line, and FY2020 lies on it too.
- **Fidelity's rail series.** The four Giving Reports read >50%, "Nearly 54%", >58% and 67% EFT by grant count. Two of them carry the EFT counts that do not reconcile (950,000 and "more than 750,000"). The 2026 report's "more than 2 million" does reconcile with 67% × 3m.

The Charityvest (95% within 35 days), AssetMark (median 2 days, 0 electronic), Daffy, Vanguard, DAFpay, Chariot-spec, BridgeFT and Schwab quotes are all verbatim.

**One claim is contradicted.** Endaoment's T&C *does* forbid passing credentials to an unregistered tool: "API Access credentials, tokens, and keys are personal to you (or your authorized organization) and may not be shared, sold, or transferred except as we expressly permit." Its developer docs also describe a second sanctioned track besides OAuth: a server-to-server **Partner API** keyed to the partner, with "No donor OAuth login required on your side". So the batch's "no term at Daffy, Endaoment or Chariot forbids it" and "OAuth-only" readings need correcting.

Four further wording fixes are needed:
1. **Daffy Organizers.** The Daffy Agreement uses the same "any individual, corporation, or trust" words for **Organizers**, who have "equal access to the fund". The Financial Advisor is therefore not the only entity route.
2. **DAFpay stacking count.** The text says DAFpay is dearer "on 4 of 5 platforms" but then lists five. It is dearer on all five quantified platforms at default settings (Donorbox only at Stripe's nonprofit rate). The sixth platform, GiveCampus, publishes no figure.
3. **Rail panel composition.** 12 of the 20 rail-panel rows are vendor or secondary, not 15.
4. **Blank-return accounts.** The "0.05% of accounts" bound holds for B1 only. B2 adds 4,360 accounts (0.14%) in FY2023.

**Benevity overlay.** Downgrading Benevity from RED to **AMBER (provisional)** is supported under §7. It is not eligible for GREEN, and the conditions are under V21-27.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V21-01 | A1: 1,122,971 / 2,495,659 / 2,352,992 / 2,589,633 | **Confirmed** | Script re-run byte-identical. Corrected total − (AOGF count − 695) in each year. |
| V21-02 | A1 shares 0.5977 / 0.7674; Schedule O wording | **Confirmed** | 1,390,021,897 / 935,709,539 and 205,671,333 / 62,329,679; "without ongoing advisory privileges". |
| V21-03 | A2 787,978 (597,569 in FY2021); growth 9.7% vs 20.6% / 32.1%; averages | **Confirmed** | 2,589,633 − 1,421,011 − 380,644. Givinga 42,307 → 1,543,203 (36.5x). Givinga + PPGF are 69.6% of A1. |
| V21-04 | index_2026 still 2026-10-21; BBGF CSRconnect wording | **Confirmed** | Last-modified 21 Oct 2026 13:03:05 GMT. BBGF Part III wording verbatim; count element absent. |
| V21-05 | B1 −$17.3m / −$25.3m / +$169.6m / +$123.8m; B2; ≤0.07% of assets | **Confirmed** | Exact to the dollar. The "0.05% of accounts" bound is B1 only: B2 adds +4,360 accounts in FY2023 (0.14%). |
| V21-06 | CFMT imputations are straight-line interpolation | **Confirmed** | 270,448,587 → 396,053,709: 333,251,148.0 and 364,652,428.5. FY2020 (301,849,868) is on the same line. |
| V21-07 | Fidelity >50% / ~54% / >58% / 67% EFT; PDF dates | **Confirmed** | "Nearly 54%". CreationDates 2024-04-15 (2023 report), 2024-03-06, 2025-02-19, 2026-04-21. |
| V21-08 | Fidelity EFT counts do not reconcile (950,000; >750,000) | **Confirmed** | Implied 1.24m and 1.57m. The 2026 count (>2m vs 2.01m) does reconcile; the doc does not say so. |
| V21-09 | Vanguard 57% of $3.7m (Maui); >$130m since May 2023 | **Confirmed** | PR Newswire 2023-09-20, verbatim. The FY2024 "$1 billion" reprint was not re-read. |
| V21-10 | TIFIN 82% / $34.1m / 5,175; "15 of 20 rows vendor or secondary" | **Partially confirmed** | The case study is verbatim. The CSV has 8 first-party and 12 other rows. |
| V21-11 | Charityvest "95% … within 35 days" | **Confirmed** | Verbatim. The page names PayPal and check only, with no Chariot mention. |
| V21-12 | AssetMark median 2 days overall, 0 electronic | **Confirmed** | lastUpdatedDate 2026-11-10 ("Updated this week"); no sample stated. |
| V21-13 | 28 latency statements, 5 measured | **Confirmed** | 3 undisclosed-sample and 2 n = 1 rows. |
| V21-14 | Daffy FA "any individual, corporation, or trust"; the one entity route | **Partially confirmed** | Quote verbatim. The same wording applies to Organizers, who have "equal access to the fund". |
| V21-15 | Daffy: no API clause; loss on member; "cannot be canceled"; "acts as you" | **Confirmed** | All verbatim. |
| V21-16 | Endaoment T&C quotes (API Access, assent, abuse, sole responsibility, no refunds) | **Confirmed** | All verbatim; "Last updated August 12, 2026". |
| V21-17 | Endaoment: no term forbids credential hand-off; OAuth client is the sanctioned route | **Contradicted** | The T&C bars sharing "API Access credentials, tokens, and keys". The docs have two tracks: OAuth and a Partner API key. |
| V21-18 | Vanguard "Interested parties must be individuals …"; VCIP form | **Confirmed** | Verbatim. Form 3 pp., created 2026-08-14; SSN last 4 or PIN, birth date, signature. |
| V21-19 | DAFpay clause (c), "anyone else's", user definition, 2FA, $1,000 cap | **Confirmed** | All verbatim; effective 2025-09-24. The many-donor bar is a close reading [I]. |
| V21-20 | Benevity: AI does not approve; auto-approval configurable; 30%→<3% one client | **Partially confirmed** | First-party quotes verbatim. b-hive returned 403 again, so the two key help statements stay [R]. |
| V21-21 | Chariot `anonymous` semantics; Get Current Donor; ID on letter; no anonymity field | **Confirmed** | All verbatim; Get Grant reference has no "anonym" string. |
| V21-22 | BridgeFT Schwab DASCG / DASPL / DASPI / CHGFT; none for NFS / Pershing | **Confirmed** | updatedAt 2025-10-06. |
| V21-23 | Candid v2 sample is date-only; guides promise a timestamp | **Partially confirmed** | Changelog embed and guide wording confirmed. The sample PDF was not re-read (docs.candid.org robots AccessDenied). |
| V21-24 | DAFpay dearer than card "on 4 of 5 platforms"; $5.20–$29 per $1,000 | **Partially confirmed** | Rates verbatim. Dearer on all five quantified platforms at default; GiveCampus has no figure. |
| V21-25 | Chariot "80% of DAFpay usage" fee-free; "$199/mo + 2.9%" | **Confirmed** | Both verbatim; undated, metric undefined. |
| V21-26 | Schwab SOSA: credential sharing deemed authorised; $100 cap; incorporated by DAFgiving360 | **Confirmed** | Verbatim; page code 0225-M8PR; 2024 policies incorporate the OSA. |
| V21-27 | Benevity overlay RED → AMBER | **Partially confirmed** | Supported as AMBER (provisional) under §7; not GREEN; conditions below. |

**V21-27, Benevity overlay verdict.**
- **§7 vocabulary:**
  - RED requires that "AI can complete a money-moving or status-clearing action without documented sponsor or human approval".
  - AMBER is "capability live with undocumented limits, but sponsor approval remains".
- **Why RED no longer fits.** The RED basis in `quadrant-v11-rescore.md` §3 was "No human or company approval step is documented". That is no longer true on first-party text:
  - the blog says AI builds the submission "before it even reaches program administrators";
  - the AI platform page says AI "never takes an irreversible action without human confirmation";
  - the Responsible AI Policy keeps material decisions "human-led".
- **Why not GREEN.** Two gaps remain:
  1. **The AI-specific statements are search-index only.** The statement that AI "does not approve or decline" and the auto-approval setting rest on b-hive pages that return 403 [R].
  2. **Auto-approval can remove the human.** A company admin can turn on auto-approval for all requests or under a threshold, so an AI-built, AI-"verified" submission can then be approved with no human. How the AI check feeds that rule is not public.
- **Verdict: AMBER (provisional).** Revert to RED if Benevity documents auto-approval keyed to the AI verification. This also respects the wave-18 rule "AI may add a flag, never clear one": the AI's eligibility check is an added flag, and clearing is a rule set by the client.

## Exact corrections

### `research/mission-2026-11-14/queue-batch36-agent-terms-controls.md`
1. **§0, P-B35C-01 row (credential hand-off).**
   - **Find:** "**No published term at Daffy, Endaoment or Chariot expressly permits or forbids giving a credential to a third-party tool router. All three put the loss from unauthorised use on the user.**"
   - **Replace with:** "**No published term at Daffy or Chariot expressly permits or forbids giving a credential to a third-party tool router. Endaoment's T&C does forbid it: \"API Access credentials, tokens, and keys are personal to you (or your authorized organization) and may not be shared, sold, or transferred except as we expressly permit.\" All three put the loss from unauthorised use on the user [V wave 21].**"
2. **§0, same row (Endaoment route).**
   - **Find:** "Its sanctioned third-party path is a **registered OAuth client**: Endaoment issues the client ID and secret after a joint validation."
   - **Replace with:** "It documents two sanctioned third-party tracks: a **registered OAuth client**, where the donor signs in with OAuth + PKCE and Endaoment issues the production client ID and secret after a joint validation; and a **Partner API**, a server-to-server API key with which the partner provisions users and funds and submits grants (\"No donor OAuth login required on your side\") [F; V wave 21]."
3. **§0, same row (Daffy entity delegate).**
   - **Find:** "**New finding:** a Daffy Financial Advisor \"may be any individual, corporation, or trust\" with its own login. That is a sanctioned entity delegate."
   - **Replace with:** "**New finding:** a Daffy Financial Advisor \"may be any individual, corporation, or trust\" with its own login. That is a sanctioned entity delegate. The Agreement uses the same words for Organizers, who have \"equal access to the fund\" [V wave 21]."
4. **§1.2, reading 2.**
   - **Find:** "2. **Endaoment's design is the cleanest delegation model.** Third-party software gets its own OAuth client registration."
   - **Replace with:** "2. **Endaoment's design is the cleanest delegation model.** Third-party software gets its own OAuth client registration, or a partner integrates through the separate Partner API (its own API key, partner-provisioned users). Either way the T&C bars handing a donor's own credentials or tokens to an unregistered tool (\"personal to you … may not be shared, sold, or transferred except as we expressly permit\") [V wave 21]."
5. **§1.2, reading 3.**
   - **Find:** "3. **Daffy's corporate Financial Advisor is the one entity-delegate route found in any donor contract read.**"
   - **Replace with:** "3. **Daffy's corporate Financial Advisor, and on identical wording a corporate or trust Organizer, are the only entity-delegate routes found in any donor contract read** [V wave 21]."
6. **§5, reading 4 (Benevity overlay).**
   - **Find:** "4. **Suggested overlay change (not applied):** move A5 Benevity from **RED (provisional) to AMBER**. The basis is that the AI does not approve and humans approve by default. Keep a note that rule-based auto-approval can remove human review."
   - **Replace with:** "4. **Overlay change (validated wave 21; apply at the next re-score):** move A5 Benevity from **RED (provisional) to AMBER (provisional)**. First-party pages keep a human approval by default, so the §7 RED test (no documented human approval) is not met. It is not GREEN: the \"does not approve\" and auto-approval statements are [R] only, and an admin-enabled auto-approval rule can approve AI-built submissions with no human. Revert to RED if Benevity documents auto-approval keyed to the AI verification [V wave 21]."

### `research/mission-2026-11-14/queue-batch36-metrics-rails.md`
1. **§2.3 (accounts bound).**
   - **Find:** "It does not matter for market size: at most 0.07% of assets and 0.05% of accounts in any year."
   - **Replace with:** "It does not matter for market size: at most 0.07% of assets in any year under B1 or B2, and 0.05% of accounts under B1. B2 adds up to 4,360 accounts (0.14%, FY2023) [V wave 21]."
2. **§3.3, Fidelity counts.**
   - **Find:** "  - The counts may cover a partial period or a subset; the reports do not say [C/I] (P-B36A-02)."
   - **Replace with:** "  - The counts may cover a partial period or a subset; the reports do not say [C/I] (P-B36A-02). The 2026 report's \"more than 2 million\" does reconcile with 67% × 3m = 2.01m [C; V wave 21]."
3. **§5, rail-share limits.**
   - **Find:** "15 of 20 rows are vendor-published or secondary."
   - **Replace with:** "12 of 20 rows are vendor-published or secondary; 8 are first-party [V wave 21]."

### `research/mission-2026-11-14/queue-batch36-anonymity-feeds-fees.md`
1. **§4, finding 1 (platform count).**
   - **Find:** "DAFpay costs more than card on 4 of 5 platforms at their default or most common settings:"
   - **Replace with:** "DAFpay costs more than card on all five platforms with a quantified comparison, at their default or most common settings (Donorbox only at Stripe's nonprofit rate; GiveCampus, the sixth platform in the CSV, publishes no figure) [V wave 21]:"

### `research/mission-2026-11-14/queue-sponsor-terms-data-clauses.md`
1. **Credential table, DAFgiving360 row** (batch 36C proposal 1, validated).
   - **Find:** "Bound by Schwab's Online Services Agreement (not public)."
   - **Replace with:** "Bound by Schwab's Online Services Agreement, which is public at schwab.com/legal/terms (the page titled 'Schwab Online Services Agreement'). It deems credential sharing to authorise the recipient's acts and caps Schwab's liability at $100 (batch 36C; V wave 21)."

### `research/mission-2026-11-14/queue-batch32-feeds-owners-codebases.md`
1. **§1, custodial route** (batch 36C proposal 5, validated).
   - **Find:** "- **Wealth-captives.** These are unchanged from batch 31:"
   - **Replace with:** "- **Schwab registration codes (batch 36C; V wave 21).** BridgeFT's public registration-type reference (updated 2025-10-06) shows that Schwab passes DAF-specific registration codes: DASCG 'Charity Account (Donor Advised Account)' and DASPL 'Charity Account (Schwab Private Label)'. The NFS and Pershing tables show none. Which programs use the codes is not stated.\n- **Wealth-captives.** These are unchanged from batch 31:"

### `research/mission-2026-11-14/quadrant-v11-rescore.md`
1. **§1 summary bullet.**
   - **Find:** "One provider is RED (provisional, A5 adjacent): Benevity Match Assurance."
   - **Replace with:** "No provider is RED. Benevity Match Assurance (A5 adjacent) moves from RED (provisional) to AMBER (provisional): first-party pages keep human approval by default, while a rule-based auto-approval setting [R] can remove it (V wave 21)."
2. **§3 table, A5 Benevity row.**
   - **Find:** "| A5 | Benevity | **RED (provisional)** | Match Assurance uses AI to verify receipt eligibility and auto-submits match requests. No human or company approval step is documented. This is adjacent to, not inside, the validation product. |"
   - **Replace with:** "| A5 | Benevity | **AMBER (provisional)** | Match Assurance uses AI to verify receipt eligibility and auto-submits match requests. Program administrators approve by default: the AI builds the submission \"before it even reaches program administrators\", and Benevity's AI \"never takes an irreversible action without human confirmation\". Help-centre snippets [R] say the AI \"does not approve or decline\", but admins can enable auto-approval for all requests or under a threshold. Revert to RED if auto-approval is documented as keyed to the AI check. This is adjacent to, not inside, the validation product (V wave 21). |"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.15:** "### 11.16 Batch 36 (validated, wave 21)", containing:

   > **Batch 36 (validated, wave 21).** On a strict "ongoing advisory privilege" basis, applying only AOGF's own FYE 2026 reclassification, the DAF market held 2.59m accounts in FY2024 (1.12m in FY2021), not 3.31m. Grants fall only 1.2% and assets under 0.03%. Excluding the two other micro-account processors (Givinga and PayPal Giving Fund) leaves 0.79m accounts in FY2024. On that basis accounts grew 9.7% a year over FY2021–24, against 20.6% on corrected totals. Account counts and per-account averages should therefore always be shown with and without the processors. Replacing DAFRC's "closed" flags and imputations for blank Schedule D returns moves market assets by −$25m to +$170m a year (at most 0.07%). DAFRC's imputations interpolate linearly between filed years, as the CF of Middle Tennessee rows show exactly. Fidelity Charitable is the only sponsor publishing a dated electronic-grant series: >50%, nearly 54%, >58% and 67% of grants by EFT in its 2023–2026 reports. Two of those reports give EFT counts that do not reconcile with the shares. Latency is published as policy, not measurement. The only measured figures are vendor ones: Charityvest says 95% of checks are deposited within 35 days of sending, and AssetMark reports a median of 2 days overall and 0 days electronic. No donor contract read admits a software service as a delegate. Vanguard interested parties "must be individuals". DAFpay bars use "on behalf of or to provide services to third parties". Endaoment's terms bar sharing API credentials and tokens, and it sanctions only registered OAuth clients and keyed Partner API integrations. Daffy alone lets a corporation or trust act as a Financial Advisor or Organizer with its own login. Benevity's Match Assurance AI pre-checks and submits match requests while administrators approve by default, so its AI overlay moves from RED to AMBER (provisional): a configurable auto-approval rule can still remove the human. On DAFpay, a sponsor-side `anonymous` flag governs the sponsor's letter. Chariot still pulls the donor's name and contact details, and the grant ID must appear on the remittance. Schwab's custodial feed carries DAF registration codes (DASCG, DASPL); Fidelity's and Pershing's, as documented by BridgeFT, do not. With fees not donor-covered, DAFpay costs nonprofits $5–$29 more per $1,000 than card on all five platforms with published comparisons. Chariot says fee-free subscriptions made up "80% of DAFpay usage" in the past year (undated). Schwab's Online Services Agreement, which binds DAFgiving360 users, treats shared credentials as authorising the recipient and caps Schwab's liability at $100 [V wave 21]. Sources: [queue-batch36-metrics-rails.md](mission-2026-11-14/queue-batch36-metrics-rails.md), [queue-batch36-agent-terms-controls.md](mission-2026-11-14/queue-batch36-agent-terms-controls.md), [queue-batch36-anonymity-feeds-fees.md](mission-2026-11-14/queue-batch36-anonymity-feeds-fees.md), [validation-wave21-report.md](mission-2026-11-14/validation-wave21-report.md).

## Data-file notes (not .md; for the owning agent)

- **`agent-delegation-terms-2026.csv`:**
  - **Add an Endaoment row** (clause_topic `credential_sharing`, clause_present Y, delegation_effect "bars sharing except as Endaoment expressly permits"). key_quote: "API Access credentials, tokens, and keys are personal to you (or your authorized organization) and may not be shared, sold, or transferred except as we expressly permit."
  - **Add an Endaoment row** (`registered_third_party_app`) for the Partner API track: "For tech-platform partners calling our server-to-server APIs with an API key. No donor OAuth login required on your side."
  - **AT03 notes:** add that Organizers carry the same "any individual, corporation, or trust" wording.
- **`dafpay-stacking-fees-2026.csv`:** no value change. S07's card side rests on funraise.org, which robots-disallows ClaudeBot; it was not re-read.
- **`grant-rail-shares-panel-2026.csv`:** no change. S04's implied 2,010,000 matches the report's "more than 2 million".
- **`dafrc-market-accounts-restated.csv`, `grant-latency-statements-2026.csv`, `anonymity-data-flow-2026.csv`:** no change.
- **`sponsor-terms-clauses-2026.csv` row 31 and `nonprofit-daf-receipt-fees-2026.csv` (batch 36C proposals 2–4):** supported. The SOSA title, Bloomerang's 3.95% / 4.95% + $0.30 and 4.85% rates, and Chariot's "$199/mo + 2.9%" were re-read. The "1% On donations from sources you link" and Mailroom prices were not re-read.

## Limits

- **Robots and access.**
  - robots.txt was read first on every host:
    - the GivingTuesday S3 mirror (no file, 404) and apps.irs.gov (redirects to an irs.gov 404, so no file);
    - fidelitycharitable.org, vanguardcharitable.org, prnewswire.com and guide.charityvest.org;
    - intercom.help (crawl-delay 1, respected), daffy.org, docs.daffy.org (404, no file), docs.endaoment.org and dafpay.com;
    - benevity.com (anthropic-ai and ClaudeBot allowed), community.benevity.com and b-hive.benevity.com (allows `/hc/` articles);
    - docs.givechariot.com, help.givechariot.com, www.givechariot.com, docs.bridgeft.com and developer.candid.org;
    - www.schwab.com (readable this time; `/legal/` not disallowed) and static1.squarespace.com (404, no file);
    - help.bloomerang.com, donorbox.org, help.funraise.io, help.betterworld.org and help.givebutter.com.
  - **Not fetched:** funraise.org disallows ClaudeBot. docs.candid.org returns AccessDenied on robots.txt.
  - **403 responses:** both b-hive articles returned 403 to a plain request and were not retried.
- **Not re-run or not re-read:**
  - the `rails` task of the script, and the index row count (472,357);
  - the Vanguard FY2024 "$1 billion" reprint;
  - the DJCF and Founders Pledge case studies and the Chariot n = 1 latency sample;
  - the GS DAF and SVCF texts (validated in wave 20);
  - the Louise / TIFIN Give help centre;
  - the Foundant and Foundation Source rows;
  - the PPGF delivery policy and the Chronicle article;
  - the Bloomerang default-on blog and the AASP thread.
- **Interpretation.** These remain inferences, as batch 36 labels them:
  - the A1 back-cast and the A2/A3 bounds;
  - the "many-donor agent barred" reading of DAFpay clause (c);
  - re-identification through the Chariot grant ID;
  - the "Schwab Private Label = sponsor-branded programs" reading;
  - the Benevity overlay itself, which rests partly on [R] snippets.

This is research, not legal advice.
