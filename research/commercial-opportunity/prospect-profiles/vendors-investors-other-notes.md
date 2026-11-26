# Prospect hypotheses: vendors, investors, nonprofits, educators, adjacent buyers (PV01–PV31)

**Date:** 2026-11-20. **Companion:** `prospects-other.csv` (31 rows, 20 fields, all fields quoted). **Builder:** `../build_prospects_other.py`.
**Status:** these are hypotheses about who might buy, not qualified leads. No outreach, logins, forms or paywalled sources were used. LinkedIn was not used.
**Tags:** [F] official or primary page read in this pass or in a repo file; [R] search-index snippet only; [S] secondary republication; [C] computed in the repo; [A] aggregator; [I] inference.

## 1. Patterns

1. **No prospect shows public evidence of buying independent DAF research.** No vendor, investor or nonprofit was found commissioning outside DAF market, technology or due-diligence work. Every budget field is either "none found" or rests on adjacent evidence: named deal advisers, serial M&A, or sponsor-funded research. Willingness to pay is unproven across the set.
2. **Investors name banks and law firms, never diligence firms.** Public deal notices name financial and legal advisers only:
   - **Ren 2023:** Raymond James for Ren; Ropes & Gray for Bain [R].
   - **Ren 2025:** Houlihan Lokey and Goodwin Procter for Great Hill [R/S].
   - **Foundation Source 2023:** Canaccord and Greenberg Traurig for GTCR; Baird, Lincoln and K&L Gates for the seller [R].
   - **Envestnet 2024:** J.P. Morgan and Ropes & Gray for Bain; Paul, Weiss for Envestnet [R].
   - **Deed 2026:** Berenson and Skadden for Bonterra; Raymond James and Orrick for Deed [R].
   - **Benevity 2020–21:** Norton Rose Fulbright for Benevity [R].

   No L.E.K., Bain & Company, Crosslake, West Monroe or Stax engagement on any DAF-ecosystem deal was found. Those firms market integrated commercial and technical diligence generically [R]. The realistic entry point for investors is **as a DAF-specialist subcontractor or expert inside a generalist due-diligence team**, or through expert networks, not direct sponsor mandates.
3. **The strongest fits involve transactions or vendor choice:**
   - repeat acquirers: Foundation Source/GTCR (PV04, PV17) and Bonterra/Apax (PV08);
   - sponsors in exit windows: Bain and Great Hill on Ren (PV15, PV16), Hg on Benevity (PV18);
   - a strategic running two DAF vendors: SEI, on TIFIN Give and Ren (PV21);
   - a challenger before a funding round that needs third-party evidence: Chariot (PV03).
4. **Nonprofits and educators have weak budgets but clear needs.** Gift offices show real operational gaps: pledge fulfilment, credit and recognition, events, and DAF anonymity (repo gift-office file). Their buying signal is weak. AFP and CGP pay mainly in exposure. The Lilly School sells research rather than buying it.
5. **Ownership does not make a channel captive.** As the repo found, Bain (Ren and Envestnet) and GTCR (Foundation Source and AssetMark) do not route their wealth platforms to their own DAF vendor. Owning a vendor therefore does not imply demand for cross-portfolio DAF strategy.

## 2. Conflicts of interest (most material first)

- **Vendor clients against independent vendor assessment.** Echelon's existing work critiques Ren's share claims, assurance statements and contract durability, Benevity's disbursement delays and YourCause's voided-check rules. Taking paid work from Ren, Foundation Source, TIFIN Give, Chariot or Benevity while publishing vendor comparisons would be read as capture. **Rule:** run a separate engagement line with an information barrier, publish who funded any public research, and decline to rank a current client.
- **Buy side against sell side on the same asset.** Ren's owners (PV15, PV16) and Ren's potential acquirers, competitors or distributors (PV04, PV21) cannot both be served on Ren matters.
- **Distributor against vendor.** Assessing TIFIN Give for SEI (PV21) is incompatible with a TIFIN Give mandate (PV02).
- **Education.** The American College (PV24) has been investigated critically by Echelon. Any paid curriculum role needs disclosure and should wait until the DAFCP findings are validated. CGP and AFP are sponsored by vendors (PG Calc, FreeWill), so neutral content must stay vendor-agnostic.
- **The Bain family.** Bain Capital owns Ren, Envestnet and part of FreeWill. Bain & Company runs a technology due-diligence practice; it is a separate firm, but a likely competitor or channel partner. Map these ties before taking related work.

## 3. Named decision-makers: verification status

- **Read first-hand on official pages:**
  - Ren: Joe Fisher, Gideon Taub, Nathan Gill, Michele Hoza.
  - Chariot: Salo Serfati, Aaron Kahane, Drew Schneider, Mitch Stein.
  - Endaoment: Robbie Heeger, Zach Bronstein, Ricardo Pedroni.
- **Snippet or secondary only ([R]/[S]); verify before any use:**
  - Foundation Source: Joseph Mrak III, Jeffrey Haskell.
  - Daffy: Adam Nash.
  - Benevity: Soraya Alexander.
  - Givinga: Joe Phoenix.
  - Great Hill (Pulse 2.0 republication): Nick Cayer, Matt Vettel, Bob Anderson.
- **Unresolved:** TIFIN Give's current head. Snippets give conflicting COO names (Blake Rohde, Andrew Dahlinghaus).
- **Left blank on purpose:** Bain, GTCR, Hg, Apax, Stanford, ALSAC, AFP, CGP, Lilly, the CPA firm and the law firm. The DAFCP programme director's name is left out pending validation.

## 4. Searches that were unsuccessful or blocked

- No commercial or technical due-diligence provider was named for Ren, Foundation Source, Benevity, Bonterra/Deed or Envestnet. Searches covered L.E.K., Crosslake, West Monroe, Stax and Bain.
- Great Hill: no evidence of a diligence or research vendor, and greathillpartners.com was not read.
- The businesswire.com originals returned 403, so the Ren/Great Hill release was read from a republication.
- foundationsource.com/about-us/leadership returned 404. daffy.org/about rendered empty.
- foundant.com disallows ClaudeBot, and investor.blackbaud.com robots.txt returned 403. Neither was fetched.
- No Goodstack–PayPal Giving Fund relationship was found.
- No Lilly School DAF study dated 2026 was found.
- No AFP DAF toolkit for 2026 was found.
- No DAF-specific evidence was found for Crescendo.
- **Fiscal sponsors:** nothing was profiled beyond Givinga's ProjectFS. Tides and similar sponsors were not researched, and no evidence was invented.
- The CPA firm (PKF O'Connor Davies) and the law firm (Quarles & Brady) were chosen from search snippets of their practice pages as examples only. Withum, Wipfli and PwC Canada (philanthropic advisory) were other candidates.

## 5. Suggested next validation steps

1. Read the leadership pages and releases tagged [R] first-hand, checking robots.txt before each fetch.
2. Read 990 Part IX and Schedule O consulting lines for the charity prospects (Endaoment, GiveClear, Give Interactive's owner Signatry, PayPal Giving Fund) for any outside-services spend.
3. Test the subcontractor route: whether generalist due-diligence firms take on sector-specialist experts for niche fintech or philanthropy assets. This is a channel question, not a contact.
4. Monitor the trigger events: a Chariot or Daffy funding round, an Hg or Benevity process, Ren sell-down news, Foundation Source add-ons, and the close of Vanguard's Altruist acquisition.
