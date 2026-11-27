# REV3 - Channel partner review

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV3, perspective 4 of 5. Challenges P3-CHL-REV3028..REV3036. Written in the voice of a hypothetical community-foundation software vendor considering embedding Unbound as a DAF module. No real partner was contacted. Same model family as the authors.

## Position

I sell fund accounting, grants and donor portals to community foundations. My customers ask for a better DAF experience. Unbound is pitched to me as the module that fills the gap (DEC-001; 12:57). I would like that to be true, but the package describes a relationship I would not sign, at economics I would not accept, from a supplier my own procurement would not pass.

## Challenges

**28. You are asking me to bear first-line support, implementation and the customer, and to accept "continuity on partner exit without data migration" (high; judgment on terms).** Report 12:88 proposes that if our relationship ends, my customers may "continue on Unbound directly ... without data migration". 12:84 rules out any ROFR, acquisition option or MFN. 12:85 gives *Echelon* a change-of-control termination right. Taken together, I fund your access to my customers, then you can take them. I would demand:
- a customer non-solicit for the term plus 24 months;
- exclusivity in my segment (community foundations), or no direct sales to my installed base;
- source-code escrow with release triggers that include key-person loss;
- step-in rights;
- MFN pricing;
- mutual change-of-control rights.

Report 12:93 concedes that "partners will resist most of these terms". The model, however, assigns H a "moderate" failure band (14:30) on the assumption that I accept non-exclusivity (P3-HYP-FGJ005). **Proposed change:** model H with partner-standard terms (exclusivity in segment, non-solicit, escrow), and report the walk-away decision against those terms, not against Echelon's preferred list.

**29. The 15-40% share band is the reseller band, but I would also carry implementation and first-line support, which is not a reseller role (high; judgment).** Report 12:26 places an embedded module in the "resell, implement and support" band, at 20-40% with a base of 25%. A vendor whose product sits inside my suite, under my brand, with my support desk and my SOC 2 boundary, is closer to an OEM component. OEM economics often run the other way: I pay a per-unit royalty, I set the price, and the supplier's share is the minority. Phase II's 30% (CHL-084) and the 40-50% stress are closer to my opening position than 25%. **Proposed change:** add an OEM-royalty structure (supplier receives 30-50% of the partner's list price) as a scenario for A3 and H, and re-rank.

**30. Two revenue figures for the same channel route: A3 uses $300k per customer, H uses $60k (high; internal inconsistency, circular ranking).**
- A3, "design partner -> licensed platform", inherits Phase II ER-7 revenue of $150-600k per customer, net of channel (P3-ASM-AB030; sequence-values TPL-UNB-S2 revenue_per_customer).
- H, "partner-embedded pilot ... multi-partner licensing", which is the DEC-001-approved route with my safeguards, uses $25k / $60k / $150k gross with a 25% share (sequence-values H-UNB).
- A3 pays back at month 62; H never does (14:40, 14:46).

Report 14:274 admits the two sets "are not reconciled". Report 16:246 still concludes "prefer channels whose customers pay at Phase II ER-7 scale". At $81 per account, $300k net implies about 5,300 accounts gross per customer. Very few community foundations have that many DAFs (the tail median sponsor runs 24, 05:25). The ranking is an artefact of the revenue input. **Proposed change:** run A3 at H's revenue, or show the customer count per sponsor that $300k implies and the number of such sponsors in the partner's segment. Do not present A3 as the first-ranked route until then.

**31. "Customer-funded: implementation fees and billing in advance" assumes Echelon bills my customers (medium; contradiction).** Report 16:10 and 16:244 and 14:10 name customer funding (advance billing, implementation fees) as the cheapest lever. Report 03:70 states that under partner-first the partner "collects from the customer, then remits". I invoice my customers and pay my suppliers in arrears after collection, often quarterly. Advance billing is not available to you through me. **Proposed change:** disable the customer-funded variant for partner-delivered sequences (A3, H), or model partner prepayment as a separately negotiated (and priced) term.

**32. My build-versus-buy test is not considered (medium; incumbent response, omission).** Report 13 models incumbent responses against Unbound, but not *my* response after I have seen your architecture, data model and migration format in diligence (12:83 IP retention notwithstanding). My options, on public precedent:
- build my own DAF module (Foundant already sells DAF fund accounting to CFs, 07:97);
- acquire a small DAF technology firm (CLM-025, P3-CLM-EK009);
- white-label an established DAF administrator.

The package's own finding is that every Unbound advantage can be copied in 6-30 months (07:21). That is shorter than my integration programme with you. **Proposed change:** add a partner-defection scenario (partner builds or acquires at month 18-36 after integration), with revenue loss and stranded integration cost, to 13 and 19.

**33. Support and SLA burden on me is unpriced and untested (medium; transferred work).** First line moves to me (02:77; P3-ASM-AB015 $0-100k a year for Echelon). The package does not ask what the transfer costs me, so it cannot test whether my 25% covers it. December year-end peaks, grant-release issues and donor-facing incidents land on my desk. My contracts with customers carry uptime and support SLAs from day one. DEC-010 forbids *process* SLAs until rehearsals, but I need an availability and incident-response SLA from you at signing, backed by credits. Nothing in the lean run (support $40k, maintenance $120k) can stand behind a 24x7 severity-1 response. **Proposed change:** price the partner's first-line cost per account, and an Echelon availability SLA with credits and on-call, as inputs to the share negotiation.

**34. Vendor viability is the gating diligence item, and the package's mitigation does not pass it (high; judgment).** My vendor-risk team will ask:
- How many people can fix a severity-1 ledger defect at 2 a.m. in December?
- Where is your SOC 2 Type 2?
- What happens to the code if the founder is unavailable?
- What insurance limits do you carry?

The answers in the package are: one founder plus contracted reviewers (02:83, 02:104); no SOC report, with controls design-stage (09:33); PolyForm Noncommercial components with commercial terms "forthcoming" (09:8); and insurance to be bound at the term sheet (16:244). Report 12:8 calls the partner the solution to the entrant's lack of SOC history and vendor-viability record. The truth is the reverse: I inherit those gaps and my customers' TPRM will flag them to me. **Proposed change:** make "minimum vendor-viability package" (escrow, a second qualified engineer, a SOC 2 Type 1 with a defined Type 2 date, published commercial licence, insurance certificate) a precondition for V-6 term-sheet talks, and cost it before G1.

**35. Shared Echelon infrastructure is a liability in my diligence, not an advantage (medium; shared-infrastructure assumption).** Report 15 shows sharing lowers Unbound's cost only if other Echelon products earn revenue (15:7). From my side, shared hosting, a shared control catalogue and shared operators mean my customers' data and availability depend on products I do not contract for. My security review will ask for tenant and product isolation evidence across Echelon, and may require dedicated infrastructure. That cancels the S7 saving for my book (P3-ASM-AB029). **Proposed change:** in 15, add a "partner requires dedicated deployment" case where the S7 factor is 1.0 or above.

**36. Data and charity intelligence rights: I need to know what I can show my customers (low; data rights).** Report 11 and DEC-004 restrict licensed enrichment to per-sponsor licences. If I already license Candid or GuideStar data for my suite, the package does not say whether Unbound may consume my licence inside the module, or must license again per sponsor. Either way that is cost that someone in the channel carries (11:142, "licensed enrichment +$0-9.9k per sponsor"). **Proposed change:** state who holds third-party data licences in each channel model, and add the duplicate-licence case to the partner economics.

## What would make me sign

A module with no exclusivity *for you*, a segment exclusivity *for me*, a royalty I set prices around, escrow and a second engineer, a SOC 2 Type 1 now and a Type 2 date, and a reference customer on synthetic or real migration evidence. The package's best route (A3) assumes almost none of that.
