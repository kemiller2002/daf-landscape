# Non-cash gift infrastructure: vendors, intermediaries and sponsor complex-asset desks (P-NEW-NCG-01)

*Prepared 2026-11-15. Recency rule: 2021–2026. Builds on, does not repeat: [queue-batch29-regulation-litigation-crypto.md](queue-batch29-regulation-litigation-crypto.md) §5 (crypto stress test, including its wave-14 corrections), [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md) FD13/FD15/FD47 (and wave-4 corrections W4-10/W4-11), [firms-interested-in-daf-organizations.md](firms-interested-in-daf-organizations.md) (governing W4-9 Giving Block terms), [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md), [queue-payment-rails-cluster.md](queue-payment-rails-cluster.md) §4.2, [vendor-footprint-990-harvest.md](vendor-footprint-990-harvest.md), [breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md) §4.2.*

**Outputs:** [`noncash-gift-vendors-2026.csv`](../../data/mission-2026-11-14/noncash-gift-vendors-2026.csv) (NCG-01 to NCG-17), [`relationship-graph-edges-additions-23.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-23.csv) (EW001–EW020), [`queue-proposals-batch40-n14.csv`](../../data/mission-2026-11-14/queue-proposals-batch40-n14.csv) (P-B40N14-01 to -03).

**Labels:** [F] filing or primary sponsor/company document read this pass; [C] company claim (self-reported); [R] reused from repo with its source; [S] search extract only, page not read; [I] inference; [U] unresolved.

---

## 1. Summary

1. **Non-cash intake splits into three layers that rarely overlap.** [I]
   - *Nonprofit-side intake vendors* (The Giving Block, Engiven, Overflow, GivingIQ/DonateStock, FreeWill) put stock, crypto and DAF-grant buttons on charity websites. They charge the nonprofit (1.5%–4% a gift, or subscriptions).
   - *Intermediary charities* receive the asset, sell it and grant the proceeds: DonateStock Charitable, FreeWill Impact Fund, Dechomai (with Charitable Solutions LLC), Realty Gift Fund.
   - *Sponsor complex-asset desks* (Fidelity Charitable, NPT, Ren's sponsors, Daffy) take private stock, LP interests and real estate into DAFs. They charge either nothing extra or a due-diligence fee.
2. **DAF links run through Chariot, not the sponsors.** [F/R] The Giving Block and FreeWill both route DAF grants through DAFpay (Chariot) ([TGB](https://thegivingblock.com/integrations/chariot/); [FreeWill](https://nonprofits.freewill.com/products/donor-advised-funds)). GivingIQ's EasyDAF does not name its rail. Overflow's FAQ lists bank DAFs. No large sponsor names any intake vendor as an authorised partner, which matches the repo's finding in `queue-payment-rails-cluster.md` §4.2.
3. **Direct sponsor–vendor links are few and specific.** [F/R]
   - Ren/RCF has used The Giving Block for crypto DAFs since 2022, with a $100k minimum.
   - DonateStock had an exclusive stock partnership with GVNG (2021-12-21).
   - Engiven is GVNG's crypto partner.
   - GivingIQ's advisory board includes a former Fidelity Charitable president. That is a people link, not a contract.
4. **The big complex-asset flows go through Dechomai.** [F] Dechomai Asset Trust took in $986m (CY2021), $525m (CY2022) and $961m (CY2023). Each year it receives grants from national sponsors: DAFgiving360 gave $12.3m–$25.5m a year in FY6/22–FY6/25, and Fidelity gave $56.7m in non-cash in FY6/22. AEF says outright that it is "partnered with Dechomai Foundation" for illiquid gifts. Dechomai Foundation paid Charitable Solutions LLC $3.00m, $3.81m and $4.43m in 2022–24. The only fee schedule found is "1–3% with minimum fee of $10,000", in an undated one-pager.
5. **Published fees, from free to 3.9%.**
   - **No extra fee:** Fidelity ("no additional charge for contributions of non-publicly traded assets") and Ren ("all due diligence at no extra cost").
   - **Cost-based:** NPT charges a "gift processing fee" sized to the due diligence, plus liquidation costs.
   - **Intermediary:** Dechomai charges 1–3%, with a $10k minimum.
   - **Nonprofit-side:** GivingIQ charges 3.9% on stock and crypto (2.5–2.9% on Premium) and 1.5% on DAF grants. Engiven charges about 4% (search extract only). The Giving Block, Overflow and FreeWill do not publish fees. Crypto for Charity says it is zero-fee.
6. **Volume disclosure is thin outside Fidelity and The Giving Block.** [F/C]
   - Fidelity received $2.6bn of non-publicly traded assets in 2025 ($2.3bn in 2024; 8% of contributions). Its lifetime total is $18.1bn, of which $1.7bn is crypto. It handles about 500 complex contributions a year and averages 65 days from acceptance to liquidity.
   - The Giving Block processed more than $100m of crypto in 2025, across 22,343 donations. Its stock volume rose 127% and its DAF volume "more than" doubled.
   - Everything else is company claims, or small 990 figures such as FreeWill Impact Fund's $5.68m (CY2023).
7. **2021+ events:**
   - Shift4 acquired The Giving Block (2022-02), cut the earnout by $(47.1)m and settled it at $10.4m. In 2025 Shift4 stopped carrying crypto settlement assets after adopting SAB 122.
   - FreeWill acquired Cocatalyst (2021-12-06) and Grant Assistant (2024-10-22).
   - FreeWill raised a $30m Series B led by Bain Capital Double Impact (2022-03).
   - Engiven raised $2.3m under Form D (2021–22).
   - Overflow raised a $20m Series B (2024-02).
   - DonateStock rebranded as GivingIQ (2026-04-30).
   - **No shutdowns of named vendors were found.**

---

## 2. Vendor profiles

### 2.1 The Giving Block (Shift4) — NCG-01
- **Ownership** [F]: Shift4 subsidiary. The FY2025 10-K (filed 2026-02-27) describes it as "Our cryptocurrency donation marketplace allows donors to easily gift a variety of cryptocurrencies to approximately 2,400 charities", against "over 2,000" in the FY2023 and FY2024 10-Ks ([FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1794669/000179466926000010/four-20251231.htm); [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1794669/000179466925000011/four-20241231.htm)).
  - Shift4 counts "alternative payments methods, including cryptocurrency and stock donations" in payments-based revenue and volume. It does not disclose a figure for The Giving Block alone.
  - From 2025, under SAB 122, "the Company no longer recognizes crypto settlement assets and liabilities". That ends the $1.8m/$3.5m/$5.7m year-end series in repo batch 29 §5.1.
- **Deal terms** (governing W4-9, [R]): $53.3m non-contingent plus $57.8m contingent consideration, with a maximum earnout of $246m. FY2022 brought a $(47.1)m earnout cut, and the earnout settled at $10.4m.
- **Products and fees** [F]: "Simplify" and "Accelerate" packages; "The Giving Block has an annual subscription for fundraising packages and transaction fees for donations". No rates are published ([packages](https://thegivingblock.com/?p=118084)).
- **Volumes** [C]: >$100m crypto in 2025 (+66%); 22,343 donations; average $11,019; >$32m in stablecoins; cumulative >$300m since 2018. Online stock volume +127%; digital DAF volume "more than doubling" ([2026 annual report](https://thegivingblock.com/annual-report/)).
- **DAF links** [R]: DAFpay integration; Ren/RCF crypto DAF (2022-06-08); Franklin Charitable Giving Program via RCF (repo edge E061).

### 2.2 Engiven — NCG-02
- **Funding** [F]: Engiven, Inc. (CIK 1742131, Escondido CA).
  - Form D 2022-01-28: $1,100,000 sold to one investor (first sale 2021-09-26).
  - Form D 2022-12-05: $1,200,000 sold of $2,700,000 offered, to three investors (first sale 2022-11-21).
  - Reg CF Form C filings in 2020 ([EDGAR](https://www.sec.gov/Archives/edgar/data/1742131/000174213122000002/primary_doc.xml)).
  - Total 2021–22 under Form D: **$2.3m**, which matches CB Insights' "3 rounds, $2.3M" ([S]).
- **Products** [C]: stock, "95+ cryptocurrencies" and bequests; SOC 2 Type 1 and 2; Chainalysis screening through its partner exchange; an optional custody fund in place of automatic conversion to USD ([about](https://www.engiven.com/about)). Customer counts conflict on its own site ("10,000+" and "1000+").
- **Integrations:**
  - Pushpay (2023-05-16, [R]);
  - Simple Donation via API (2022-11-15; [PR Newswire](https://www.prnewswire.com/news-releases/simple-donation-delivers-cryptocurrency-solution-through-partnership-with-engiven-301678020.html)) [F];
  - GVNG, a DAF-like "personal charity account", as crypto partner ([engiven.com/nonprofits](https://engiven.com/nonprofits)) [C];
  - Subsplash and ACS Technologies [S].
- **Fees** [S]: ACS Technologies help pages, seen only as a search extract, give a 4% processing fee per stock or crypto gift, charged to the church. engiven.com/pricing returns 404.

### 2.3 Overflow — NCG-03
- **Funding** [C]: Series A $10m (2021, led by R7) and Series B $20m on 2024-02-07, led by Wesleyan Investment Foundation with Uncork, R7 and The GP ([Overflow](https://www.overflow.co/learn/overflow-announces-20-million-series-b-round)).
  - The only Form D under "We Are Overflow PBC" (CIK 1849639) is dated 2021-03-05. It offers $150,600 with the first sale "yet to occur" ([EDGAR](https://www.sec.gov/Archives/edgar/data/1849639/000184963921000001/primary_doc.xml)) [F].
  - **No Form D matches the $10m or $20m rounds** [U].
- **Products** [C]: stock, crypto, DAF, ACH, card, wills and wallets through one integration. In 2024 it had more than 240,000 users and 450 organisations, and an average stock gift of $12,979.
- **DAF and fees:** the FAQ (search extract, [R]) lists BofA CGF, J.P. Morgan and BNY Mellon. Fees are not published. The FAQ and zendesk pages returned 404/403 on 2026-11-15.

### 2.4 GivingIQ (formerly DonateStock) — NCG-04
- **Ownership** [F/C]: private; co-founder and CEO Steve Latham; "backed by proven entrepreneurs, family offices and Capital Factory". **Pamela Norley, a former President of Fidelity Charitable, sits on the advisory board** ([about](https://givingiq.com/about)). No Form D was found.
- **Rebrand** (2026-04-30) [F]: DonateStock became GivingIQ and added EasyDAF (grant initiation on the nonprofit's own site), EasyCrypto and EasyQCD, the last due in summer 2026 ([release](https://givingiq.com/press/announce)).
- **Published fees** [F] ([pricing](https://givingiq.com/for-nonprofits/pricing)):

| Annual fundraising budget | Standard: stock/crypto | Standard: DAF grant | Premium: stock/crypto | Premium: DAF grant | Premium platform fee |
|---|---|---|---|---|---|
| ≤ $1m | 3.9% | 1.5% | 2.9% | 1.5% | $59/mo |
| ≤ $5m | 3.9% | 1.5% | 2.8% | 1.5% | $99/mo |
| ≤ $10m | 3.9% | 1.5% | 2.7% | 1.5% | $179/mo |
| ≤ $25m | 3.9% | 1.5% | 2.6% | 1.5% | $299/mo |
| ≤ $50m | 3.9% | 1.5% | 2.5% | 1.5% | $499/mo |
| > $50m | quote | quote | quote | quote | quote |

  On gifts over $100,000 the fee falls to 1% on proceeds above $100,000. Payouts come every two weeks on Standard and weekly on Premium.
- **DAF links:**
  - Exclusive stock partnership with GVNG, 2021-12-21. Gift receipts came from **DonateStock Charitable, Inc.** ([PR Newswire](https://www.prnewswire.com/news-releases/donatestock-announces-exclusive-stock-gifting-partnership-with-gvng-301449046.html)) [F].
  - DonateStock Charitable (EIN 87-1569770) files Schedule D as a DAF sponsor [R]:
    - FY2022: 10 DAFs, $9.37m in, $8.85m out;
    - FY2024: 33 DAFs, $2.16m at year-end;
    - FY2023: contributions and grants recorded as 0, probably missing data ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542229349300304_public.xml)).
  - Partners include GoFundMe Pro and Bonterra ([partners](https://givingiq.com/partners)).

### 2.5 FreeWill and Crypto for Charity — NCG-05, NCG-06
- **Funding** [F]: Form D 2022-03-04 for FreeWill Co. (CIK 1913898): $29,999,927 sold to six investors (first sale 2022-02-15) ([EDGAR](https://www.sec.gov/Archives/edgar/data/1913898/000191389822000001/primary_doc.xml)). This is the $30m Series B led by Bain Capital Double Impact; the Series A was led by ICONIQ Growth ([Bain Capital Double Impact](https://www.baincapitaldoubleimpact.com/news/freewill-raises-30-million-series-b-transform-nonprofit-fundraising-non-cash-giving)).
- **Acquisitions** [F/C]:
  - **Cocatalyst**, 2021-12-06, terms undisclosed. Cocatalyst was a stock and crypto donation platform founded in 2018; it added crypto in 2021 "in partnership with FTX" ([release via MarketScreener](https://uk.marketscreener.com/news/latest/FreeWill-acquires-Cocatalyst-as-donations-of-appreciated-assets-to-nonprofits-surge-37224567/)).
  - **Grant Assistant**, 2024-10-22, terms undisclosed ([PR Newswire](https://prnewswire.com/news-releases/freewill-acquires-grantassistant-an-ai-based-platform-to-speed-and-simplify-grant-proposals-for-nonprofits-and-international-development-organizations-302282203.html)).
- **Crypto for Charity** [F/C]: launched 2021-12-06. Gifts go to **FreeWill Impact Fund**, "our affiliated 501(c)(3)" (EIN 86-1218871). They are converted "usually within 10 minutes" and the net proceeds are granted on. FreeWill calls it "zero-fee" and says it reaches more than 55,000 nonprofits ([FreeWill](https://www.freewill.com/learn/how-to-donate-crypto-to-charity)).
  - It is **not a DAF**; it is an intermediary-charity model.
  - FreeWill Impact Fund's total contributions, all channels: CY2021 $1.19m, CY2022 $2.50m, CY2023 $5.68m ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/861218871.json)) [F].
- **DAF tool** [F]: "FreeWill integrates with DAFpay, created by Chariot" ([product page](https://nonprofits.freewill.com/products/donor-advised-funds)). Recurring DAF grants were added in 2025 [S].
- **Volume claims** [C], on bases that change and should not be added together:
  - committed gifts >$4bn (2021-12), ~$5bn (2022-03), >$10bn (2024-10) and >$15.2bn (undated [llm-info](https://www.nonprofits.freewill.com/llm-info));
  - stock giving +50% and DAF giving >+200% by 2025-04 [S].
  - "Committed gifts" are mostly bequest intentions.
- **Fees:** not published. Revenue comes from "subscription fees from nonprofits and financial institutions".

### 2.6 Endaoment's crypto rails — NCG-07
- **Fees** [F] ([fee schedule](https://docs.endaoment.org/donors/resources)):
  - donation fee from 0.50% (below $250k) down to 0.05% (above $100m);
  - grant fee 1.0%, or 1.5% combined on direct donations to an organisation;
  - $0 portfolio fee on crypto portfolios;
  - complex or private assets "case-by-case";
  - no minimums.
- **Policies** [F] ([Fund Policies](https://docs.endaoment.org/governance/documentation/policies-and-procedures.md)):
  - "Endaoment may consider for acceptance cash, publicly traded securities, digital assets (including cryptocurrencies and other tokens), and other property".
  - "Any legal fees incurred in review of complex gifts will be charged to the Fund."
  - Grants are paid via Chariot once the pending balance is at least $25.
  - The risk framework caps positions so that Endaoment "never holds a majority of the available liquidity" of any pool.
- **Partner API** [F]: provision users, create partner-managed funds, submit settled grants, and pledge crypto and stock ([llms.txt index](https://docs.endaoment.org/llms.txt)).
- **Repo facts, not repeated here** [R]: crypto made up 99.7% of FY6/2024 contributions; Altruist DAFs (2026-10); the Chariot disbursement partnership.

### 2.7 Charitable Solutions LLC and Dechomai — NCG-08
- **Fee schedule** [F]: a one-pager headed "Duties Performed by Charitable Solutions, LLC / Dechomai Foundation, Inc." lists real estate, LP/LLC, S-corp and C-corp stock, restricted stock, farmland, timber, mineral rights, royalties and art. It states **"DECHOMAI DONATION IS 1-3% WITH MINIMUM FEE OF $10,000"**. Its flow: the asset is transferred to Dechomai, which provides the Form 8283 help, sells the asset, files Form 8282 and grants the net proceeds ([PDF](https://content.gitbook.com/content/m6D70REL1x557OfeIjyD/blobs/ETpsREc9M2EpHfkAknik/Complex%20Asset%20Donations%20-%20Charitable%20Solutions%20-%201-Pager.pdf)).
  - The document is undated; its file metadata shows a 2014 build. Treat the fee as the *last published* figure, not a current one.
- **Services** [F]: CGA reinsurance brokerage and National Gift Annuity Foundation administration ([site](https://www.charitablesolutionsllc.com/)).
- **Payments and scale** [F/R]:
  - Dechomai Foundation paid Charitable Solutions LLC $2,998,459 (2022), $3,805,114 (2023) and $4,425,428 (2024) (`form990-contractors-harvest-full.csv`; repo edge EC006).
  - Dechomai Asset Trust contributions: $986m (CY2021), $525m (CY2022), $961m (CY2023). Dechomai Foundation contributions: $351m (CY2023) ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/260724604.json)).
- **Sponsor links** [F/R]:
  - AEF: "Currently, AEF is partnered with Dechomai Foundation"; AEF "may not accept gifts of illiquid assets directly" ([AEF](https://aefonline.org/?p=9807)).
  - Schedule I grants from national sponsors to Dechomai Asset Trust (`daf-to-daf-flows-990.csv`):
    - DAFgiving360: $12.29m (FY6/22), $25.50m (FY6/23), $15.06m (FY6/24), $19.48m (FY6/25);
    - Fidelity: $56.73m non-cash (FY6/22);
    - AEF: $4.80m (2022);
    - Goldman Sachs PF: $0.75m (2023), $1.25m (2024);
    - smaller amounts from Morgan Stanley GIFT and ImpactAssets.

### 2.8 Real-estate gift processors — NCG-09, NCG-10
- **Realty Gift Fund** [C]: an AEF article quotes co-founder Bruce Geiss as "one of AEF's partners that accepts real estate donations". It reports an average gift of $600,000 and an average grant to the DAF of 94% of net sale proceeds ([AEF](https://www.aefonline.org/?p=9641); undated). Ren once hosted a "Welcome to Realty Gift Fund" PDF (2024-01 upload); the link now returns 404 [U].
- **RealtyCharity** [U]: realtycharity.org returned a proxy 502, so robots.txt could not be read and the site was not fetched. Web searches found no entity of that name. **Not profiled.**

---

## 3. Sponsor complex-asset acceptance: what the repo had and what this pass added

**What the repo already held:**
- Crypto handling at Fidelity, NPT, Ren and Daffy (batch 29 §5.2);
- Daffy's private stock: more than $600m received through Aug 2026, with liquidation plans from 2026-10 (`competitive-history-timelines.md`);
- Complex-asset processing modelled as process P03 (`ai-economics-replacement-analysis.md`);
- Ren's complex-asset capability (`capabilities.csv`).

**What was missing:** minimums, fees and timelines. The table below fills those gaps from primary pages where possible.

| Sponsor | Assets accepted | Minimums | Fees | Timeline and holding | Source |
|---|---|---|---|---|---|
| **Fidelity Charitable** | C-corp, S-corp, LLC/LP, pre-IPO, restricted/control stock, PE, hedge fund, life insurance, oil and gas royalties; crypto **BTC, ETH, LTC, SOL** (SOL is new against the repo's BTC/ETH/LTC). Real estate is not listed | No account minimum. No stated asset minimum | "**No additional charge** for contributions of non-publicly traded assets". The standard admin fee applies. UBIT and costs are deducted from the account | **65 days on average** from acceptance to liquidity; about **500** complex contributions a year. "Generally" limits itself to a minority interest. Crypto is liquidated "through select providers" | [F] [what you can donate](https://www.fidelitycharitable.org/giving-account/what-you-can-donate.html); [crypto](https://www.fidelitycharitable.org/giving-account/what-you-can-donate/donating-bitcoin-to-charity.html); [fact sheet](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/complex-assets-fact-sheet.pdf) |
| **Fidelity: volumes** | Non-publicly traded contributions **$2.3bn (2024), $2.6bn (2025)**; 8% of 2025 contribution dollars. Lifetime $18.1bn, including $1.7bn of crypto | | | | [F] [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) |
| **NPT** | Real estate, alternatives, private business interests, art, structured notes, restricted stock, crypto | **Real estate $2,000,000; alternatives $1,000,000; private business $500,000; art and collectibles $250,000; structured notes $250,000; restricted stock $25,000; crypto $25,000** (document NPT BRO IACG 0824, unchanged from its 0920 version) | A "gift processing fee" that depends on the due diligence required, with a good-faith estimate first. Liquidation costs and the ongoing admin fee are deducted. Real estate needs a **$25,000 good-faith initial contribution** and **6 months of carrying costs** paid in advance | Real estate due diligence takes **3–6 months on average**. Property must be debt-free, not under contract and vacant if residential. It is sold as-is, and NPT "will not hold or renovate". Other illiquids may be held at NPT's discretion | [F] [illiquid guidelines (2024)](https://www.nptrust.org/illiquid-asset-contribution-guidelines-npt); [real estate guidelines](https://nptrust.org/wp-content/uploads/2022/08/Real-Estate-Contribution-Guidelines-NPT.pdf) |
| **Ren-administered sponsors (RCF etc.)** | Business interests; LP, OP and GP fund positions; crypto; unencumbered real estate | Not stated (an older $250k figure appears only in a search extract [S]) | "Handle all due diligence **at no extra cost**". The crypto DAF must keep 15% in traditional assets [R] | "Private stock can be held beyond one year, with no put option required" | [C] [Ren noncash flyer 2026-05](https://www.reninc.com/wp-content/uploads/2026/05/Noncash-Assets-.pdf) |
| **AEF** | Illiquid assets and real estate | Not confirmed (a $500k real estate figure appears only in a search extract [S]) | Not published | Does not accept illiquids directly. Uses **Dechomai** and **Realty Gift Fund** | [C] [AEF](https://aefonline.org/?p=9807) |
| **DAFgiving360** | Illiquid assets case-by-case; some are liquidated by a third party. Certain real estate and PE go through a "charitable intermediary" | Not verified | Not verified | Not verified | [S] (pages and robots.txt returned 403). [I]: the intermediary wording fits its annual Schedule I grants to Dechomai Asset Trust |
| **Daffy** | Private and restricted stock; crypto portfolios | n/v | n/v | Custom liquidation plans (2026-10) | [R] |
| **Endaoment** | Any asset; complex gifts case-by-case | None | Complex-gift legal fees are charged to the Fund | n/s | [F] (§2.6) |
| **Vanguard Charitable** | Not verified | Not verified | Not verified | Not verified | [U]: no primary page found |

**Reading** [I]:
- Fidelity and Ren compete on *no extra fee*.
- NPT prices complex assets at cost and screens with high minimums.
- AEF, and on the evidence DAFgiving360, outsource the hardest assets (real estate, some private interests) to an intermediary charity. Dechomai is the one visible in the filings.
- For an entrant, partnering with an intermediary (1–3%, $10k minimum, if still current) is the observable route to complex-asset capability without building an in-house desk.

---

## 4. Limits

- **Robots and access:**
  - dafgiving360.org: robots.txt returned 403, so it was not fetched.
  - realtycharity.org: proxy 502.
  - help.acst.com: not fetched.
  - donatestock.com: 403. Its pricing was read on givingiq.com instead.
  - Overflow FAQ and zendesk: 404/403.
  - crt.sh was not used.
- **Undated sources:** the Dechomai fee one-pager, the AEF articles and Fidelity's fact sheet ($15.5bn lifetime, an older figure than the 2026 report's $18.1bn) carry no dates.
- **Unverified items:** The Giving Block's fees, and the form or size of any Overflow raise in SEC filings.
- **Company claims:** volume figures from FreeWill, Engiven, GivingIQ and Overflow are self-reported.
- **No outreach was made, and no sales or demo forms were submitted.**

---

## 5. Source register

| ID | Source | Date | Used in |
|---|---|---|---|
| N01 | [Shift4 FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1794669/000179466926000010/four-20251231.htm) | 2026-02-27 | §2.1 |
| N02 | [Shift4 FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1794669/000179466925000011/four-20241231.htm); [FY2023 10-K](https://www.sec.gov/Archives/edgar/data/1794669/000179466924000007/four-20231231.htm) | 2025-02-19; 2024 | §2.1 |
| N03 | [The Giving Block 2026 annual report](https://thegivingblock.com/annual-report/) | 2026-03 | §2.1 |
| N04 | [The Giving Block packages](https://thegivingblock.com/?p=118084) | live 2026-11-15 | §2.1 |
| N05 | [Engiven Form D 2022-12](https://www.sec.gov/Archives/edgar/data/1742131/000174213122000002/primary_doc.xml); [Form D 2022-01](https://www.sec.gov/Archives/edgar/data/1742131/000174213122000001/primary_doc.xml) | 2022 | §2.2 |
| N06 | [Engiven about](https://www.engiven.com/about); [nonprofits](https://engiven.com/nonprofits) | live | §2.2 |
| N07 | [Simple Donation–Engiven release](https://www.prnewswire.com/news-releases/simple-donation-delivers-cryptocurrency-solution-through-partnership-with-engiven-301678020.html) | 2022-11-15 | §2.2 |
| N08 | [Overflow Series B](https://www.overflow.co/learn/overflow-announces-20-million-series-b-round); [Overflow Form D](https://www.sec.gov/Archives/edgar/data/1849639/000184963921000001/primary_doc.xml) | 2024-02-07; 2021-03-05 | §2.3 |
| N09 | [GivingIQ pricing](https://givingiq.com/for-nonprofits/pricing); [release](https://givingiq.com/press/announce); [about](https://givingiq.com/about); [partners](https://givingiq.com/partners) | 2026-04-30; live | §2.4 |
| N10 | [DonateStock–GVNG release](https://www.prnewswire.com/news-releases/donatestock-announces-exclusive-stock-gifting-partnership-with-gvng-301449046.html) | 2021-12-21 | §2.4 |
| N11 | [DonateStock Charitable FY2024 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542229349300304_public.xml) | 2025-08-10 | §2.4 |
| N12 | [FreeWill Form D](https://www.sec.gov/Archives/edgar/data/1913898/000191389822000001/primary_doc.xml); [Bain Capital Double Impact release](https://www.baincapitaldoubleimpact.com/news/freewill-raises-30-million-series-b-transform-nonprofit-fundraising-non-cash-giving) | 2022-03 | §2.5 |
| N13 | [FreeWill–Cocatalyst release](https://uk.marketscreener.com/news/latest/FreeWill-acquires-Cocatalyst-as-donations-of-appreciated-assets-to-nonprofits-surge-37224567/) | 2021-12-06 | §2.5 |
| N14 | [FreeWill–Grant Assistant release](https://prnewswire.com/news-releases/freewill-acquires-grantassistant-an-ai-based-platform-to-speed-and-simplify-grant-proposals-for-nonprofits-and-international-development-organizations-302282203.html) | 2024-10-22 | §2.5 |
| N15 | [FreeWill crypto page](https://www.freewill.com/learn/how-to-donate-crypto-to-charity); [DAF product](https://nonprofits.freewill.com/products/donor-advised-funds); [llm-info](https://www.nonprofits.freewill.com/llm-info) | live | §2.5 |
| N16 | [FreeWill Impact Fund (ProPublica API)](https://projects.propublica.org/nonprofits/api/v2/organizations/861218871.json) | CY2021–23 | §2.5 |
| N17 | [Endaoment fee schedule](https://docs.endaoment.org/donors/resources); [Fund Policies](https://docs.endaoment.org/governance/documentation/policies-and-procedures.md); [llms.txt](https://docs.endaoment.org/llms.txt) | live | §2.6 |
| N18 | [Charitable Solutions site](https://www.charitablesolutionsllc.com/); [complex-asset one-pager](https://content.gitbook.com/content/m6D70REL1x557OfeIjyD/blobs/ETpsREc9M2EpHfkAknik/Complex%20Asset%20Donations%20-%20Charitable%20Solutions%20-%201-Pager.pdf) | live; undated | §2.7 |
| N19 | [Dechomai Asset Trust (ProPublica API)](https://projects.propublica.org/nonprofits/api/v2/organizations/260724604.json); [Dechomai Foundation](https://projects.propublica.org/nonprofits/api/v2/organizations/061676688.json) | CY2021–23 | §2.7 |
| N20 | [AEF real estate (Dechomai)](https://aefonline.org/?p=9807); [AEF "The Power of Real Estate"](https://www.aefonline.org/?p=9641) | undated | §2.7, §2.8, §3 |
| N21 | [Fidelity: what you can donate](https://www.fidelitycharitable.org/giving-account/what-you-can-donate.html); [crypto](https://www.fidelitycharitable.org/giving-account/what-you-can-donate/donating-bitcoin-to-charity.html); [contribution timelines](https://www.fidelitycharitable.org/giving-account/contribution-timelines.html); [fact sheet](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/complex-assets-fact-sheet.pdf) | live | §3 |
| N22 | [Fidelity 2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | 2026 | §3 |
| N23 | [NPT illiquid guidelines (0824)](https://www.nptrust.org/illiquid-asset-contribution-guidelines-npt); [2021 copy (0920)](https://www.nptrust.org/wp-content/uploads/2021/03/Illiquid-Asset-Contribution-Guidelines-NPT_RC.pdf); [real estate guidelines](https://nptrust.org/wp-content/uploads/2022/08/Real-Estate-Contribution-Guidelines-NPT.pdf) | 2024-08; 2020; 2022-08 | §3 |
| N24 | [Ren noncash assets flyer](https://www.reninc.com/wp-content/uploads/2026/05/Noncash-Assets-.pdf) | 2026-05 | §3 |
| R | Repo: batch 29 §5; FD13/FD15/FD47; W4-9; `daf-to-daf-flows-990.csv`; `form990-contractors-harvest-full.csv`; `dafrc-sponsor-schedule-d-fy2019-2024.csv`; `company-timeline-events.csv` CT068; `queue-payment-rails-cluster.md` §4.2 | — | throughout |

---

## 6. Data dictionary

### `noncash-gift-vendors-2026.csv`

| Column | Meaning |
|---|---|
| vendor_id | NCG-NN. Rows 01–10 are vendors and intermediaries; rows 11–17 are sponsor complex-asset desks |
| vendor | Common name |
| legal_entity_or_affiliate | Legal entity, CIK or EIN, and affiliated charities |
| segment | Role in the non-cash chain (intake vendor, intermediary charity, sponsor desk) |
| ownership | Owner or investors |
| funding_disclosed | Rounds from press or filings |
| form_d_summary | EDGAR Form D facts (amount sold, investors, first-sale date), or "none found" |
| products | Asset types and tools |
| daf_integrations | Named sponsors, DAF-like wallets or DAF rails |
| published_fees | Fees as published; "not published" where none was found |
| disclosed_volumes | Volumes, with year and basis |
| events_2021plus | Acquisitions, rounds, rebrands, write-downs |
| status_2026 | Active, unresolved or gap as of 2026-11-15 |
| evidence_label | F/C/R/S/I/U, as above |
| primary_urls | Sources, separated by " ; " |
| notes | Caveats |

### `relationship-graph-edges-additions-23.csv`

Uses the same columns as `relationship-graph-edges.csv`. The prefix is EW. EW002–EW004 restate repo facts as edges.

### `queue-proposals-batch40-n14.csv`

Columns follow `queue-proposals-README.md`.

## Validation corrections (wave 25B, 2026-11-15) — governing
Source: [validation-wave25b-report.md](validation-wave25b-report.md); register `data/mission-2026-11-14/validation-register-wave25b.csv`.

1. **§2.7, Fidelity grant.**
   - **Find:** "    - Fidelity: $56.73m non-cash (FY6/22);"
   - **Replace with:** "    - Fidelity: $56.73m non-cash (FY6/22). This comes from an amended FY6/22 return (object 202430459349302913, filed 2024), which also shows $197,000 in cash to Dechomai Foundation [V wave 25B];"
2. **§2.7, one-pager date.**
   - **Find:** "  - The document is undated; its file metadata shows a 2014 build. Treat the fee as the *last published* figure, not a current one."
   - **Replace with:** "  - The document is undated. Its file metadata shows it was created on 2014-11-18 and last modified on 2023-01-02. Treat the fee as the *last published* figure, not a current one [V wave 25B]."
3. **§2.2, Engiven fees.**
   - **Find:** "engiven.com/pricing returns 404."
   - **Replace with:** "engiven.com/pricing returns 404. The ACS help page (`help.acst.com/en/giving/realm-giving/guides/stock-and-cryptocurrency`) is allowed by robots but renders client-side, and its static HTML has no fee text, so the 4% stays unverified [V wave 25B]."
