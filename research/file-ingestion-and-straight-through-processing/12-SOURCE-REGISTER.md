# 12 — Source register

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Data: [`sources.csv`](../../data/file-ingestion-2026-11/sources.csv) (derived from [`evidence.csv`](../../data/file-ingestion-2026-11/evidence.csv)); source ids are content hashes of the URL or repository path.

<!-- BEGIN GENERATED: sources -->
| Stream | Confirmed | Inferred | Proposed | Total |
|---|---|---|---|---|
| A-daf-industry | 125 | 9 | 8 | 142 |
| B-formats-industries | 43 | 21 | 2 | 66 |
| C-security-storage-ai | 37 | 17 | 1 | 55 |
| total | 205 | 47 | 11 | 263 |

| Source id | Source | Title | Publisher | Kind | Evidence |
|---|---|---|---|---|---|
| FIS-9776cf77 | derived calculation from FIE-C-001, FIE-C-002 | Derived from FIE-C-001/002 | Derived | repository | FIE-C-051 |
| FIS-c525c619 | derived calculation from FIE-C-006 | Derived from FIE-C-006 | Derived | repository | FIE-C-052 |
| FIS-32d252c3 | derived calculation from FIE-C-020, FIE-C-021, FIE-C-022, FIE-C-023 | Derived | Derived | repository | FIE-C-054 |
| FIS-9db62aaa | derived calculation from FIE-C-020, FIE-C-021, FIE-C-023, FIE-C-024 | Derived: 0.23 vs 0.023 (AWS); 0.23 vs 0.026 (Azure ZRS) | Derived | repository | FIE-C-026 |
| FIS-e9e4d4f4 | derived calculation from FIE-C-045 (tokens per page assumed) | Derived from FIE-C Claude pricing row | Derived | repository | FIE-C-055 |
| FIS-67093c23 | https://access.redhat.com/security/cve/cve-2023-4863 | CVE-2023-4863 | Red Hat / CISA | web | FIE-C-033 |
| FIS-bf9927a7 | https://access.redhat.com/security/vulnerabilities/ImageTragick | ImageTragick - CVE-2016-3714 | Red Hat | web | FIE-C-034 |
| FIS-487e768c | https://achdevguide.nacha.org/ach-file-overview | ACH File Overview (ACH Developer Guide) | Nacha | web | FIE-B-031; FIE-B-032 |
| FIS-c4568106 | https://advisor.morganstanley.com/scott.altemose/documents/field/s/sc/scott-a--altemose/MS-GIFT-2025.pdf | MS GIFT 2025 brochure | Morgan Stanley Global Impact Funding Trust (MS GIFT) | web | FIE-A-066 |
| FIS-046d9495 | https://advisorservices.schwab.com/managing-your-business/tech-integration/daily-data-files | Schwab daily data files | Charles Schwab | web | FIE-B-055; FIE-B-060 |
| FIS-f561d762 | https://aws.amazon.com/about-aws/whats-new/2026/04/s3-five-additional-checksum-algorithms/ | Amazon S3 now supports five additional checksum algorithms | AWS | web | FIE-C-031 |
| FIS-0b3c6985 | https://aws.amazon.com/marketplace/pp/prodview-qdlnubma3h23o | MetaDefender listing (AWS Marketplace) | OPSWAT | web | FIE-C-017 |
| FIS-83b75ad4 | https://aws.amazon.com/rds/postgresql/pricing/ | RDS for PostgreSQL pricing + secondary guides | AWS / Bytebase / NetApp | web | FIE-C-023 |
| FIS-5e070e89 | https://b-hive.benevity.com/hc/en-us/articles/48194398193812-Understanding-the-payroll-donation-process | Benevity: Understanding the payroll donation process (search snippet; fetch 403) | Benevity | web | FIE-A-113; FIE-A-114 |
| FIS-a5c46a41 | https://bnymellonwealth.com/content/pershing/archived/us1/en/what-we-provide/prime-services/technology.html | Pershing technology (archived) | BNY Pershing | web | FIE-B-057 |
| FIS-2ef7d8fc | https://bugzilla.mozilla.org/show_bug.cgi?id=1893645 | Arbitrary Javascript injection in PDF.js through FontMatrix | Mozilla | web | FIE-C-035 |
| FIS-8eb7e7c4 | https://candid.org/explore-apis/ | Explore APIs | Candid | web | FIE-B-053 |
| FIS-b62e48a1 | https://caqh.org/hubfs/Index/2024%20Index%20Report/CAQH%202024%20Index%20Report%20Key%20Takeaways%20FINAL.pdf | CAQH 2024 Index Key Takeaways | CAQH | web | FIE-B-006 |
| FIS-070ae905 | https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html | File Upload Cheat Sheet | OWASP | web | FIE-C-018; FIE-C-040 |
| FIS-e8e52a3f | https://clearingcustody.fidelity.com/app/item/RD_9883092/integration-xchange.html | Integration Xchange | Fidelity Clearing & Custody | web | FIE-B-056 |
| FIS-26997c82 | https://client.schwab.com/secure/file/P-2014616/APP39630-10-01.pdf | Schwab Charitable Gift Transfer LOA | Charles Schwab (custodian) | web | FIE-A-120 |
| FIS-e703e304 | https://cloud.google.com/document-ai/pricing | Document AI pricing | Google | web | FIE-C-044 |
| FIS-b898496d | https://cloud.google.com/run/pricing | Cloud Run pricing (not verified) | Google | web | FIE-C-053 |
| FIS-c948d942 | https://cloud.google.com/sql/pricing | Cloud SQL pricing | Google | web | FIE-C-025 |
| FIS-54f96374 | https://cloud.google.com/storage/pricing | Cloud Storage pricing | Google | web | FIE-C-022 |
| FIS-92a213ee | https://community.foundant.com/funders_community_foundations/discussion/2808/does-anyone-else-have-challenges-with-unidentified-stock-gifts | Foundant Community: unidentified stock gifts thread | Foundant CommunitySuite (community foundations) | web | FIE-A-106 |
| FIS-adbe4beb | https://community.owasp.org/attacks/CSV_Injection | CSV Injection | OWASP | web | FIE-C-039 |
| FIS-242751d3 | https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/whitepapers/compliance/Amazon-S3-Compliance-Assessment-2026.pdf | Amazon S3 Compliance Assessment 2026 | Cohasset Associates / AWS | web | FIE-C-028 |
| FIS-b105a845 | https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html | Locking objects with Object Lock | AWS | web | FIE-C-027 |
| FIS-57aaadf9 | https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection-s3-quotas-guardduty.html | Quotas in Malware Protection for S3 | AWS | web | FIE-C-003 |
| FIS-421564c6 | https://docs.aws.amazon.com/guardduty/latest/ug/monitor-with-eventbridge-s3-malware-protection.html | Monitoring S3 object scans with Amazon EventBridge | AWS | web | FIE-C-005 |
| FIS-b4a6163f | https://docs.aws.amazon.com/guardduty/latest/ug/tag-based-access-s3-malware-protection.html | Using tag-based access control (TBAC) with Malware Protection for S3 | AWS | web | FIE-C-004 |
| FIS-5931eb22 | https://docs.cloud.google.com/architecture/automate-malware-scanning-for-documents-uploaded-to-cloud-storage | Automate malware scanning for files uploaded to Cloud Storage | Google | web | FIE-C-011 |
| FIS-2c6a5e72 | https://docs.givechariot.com/guides/disbursements/how-it-works | Chariot Disbursements: how it works / API reference | Chariot | web | FIE-A-096 |
| FIS-e1ccdf9e | https://docs.givechariot.com/v2026-04-01/guides/dafpay/overview | DAFpay overview | Chariot | web | FIE-A-099 |
| FIS-05d05de5 | https://docs.google.com/document/d/19t4zL12nKiDno7wqqNRlSdeNaTVJImkhXo2aWoNKoMo/export?format=pdf | Church FAQ describing Charityvest flow (secondary) | Charityvest | web | FIE-A-086 |
| FIS-edabb32c | https://docs.sixlabors.com/articles/imagesharp/security.html | ImageSharp Security Considerations | Six Labors | web | FIE-C-036 |
| FIS-2d61893f | https://docs.virustotal.com/docs/how-it-works | How VirusTotal works | VirusTotal (Google) | web | FIE-C-016 |
| FIS-17c9b3b5 | https://ecommerce.x12.org/license/developer-use | X12 developer use license | X12 | web | FIE-B-037 |
| FIS-f7c48926 | https://ehrsource.com/articles/payment-posting-reconciliation/ | Payment Posting and Reconciliation | EHRSource | web | FIE-B-063 |
| FIS-f92ef6ac | https://engage.aefonline.org/upgrade-hub/ | AEF Technology Upgrade hub / FAQ (search snippets + page) | American Endowment Foundation (AEF) | web | FIE-A-044; FIE-A-048 |
| FIS-ae037e7c | https://europe.thomsonreuters.com/us/guides/ardent-partners-2025-ap-metrics | Ardent Partners 2025 AP metrics (summary) | Ardent Partners via Thomson Reuters | web | FIE-B-008 |
| FIS-542f1388 | https://fidelitycharitable.org/advisors/support/account-maintenance.html | For Advisors: Account maintenance | Fidelity Charitable | web | FIE-A-019 |
| FIS-e466829a | https://fidelitycharitable.org/advisors/support/contributions.html | For Advisors: Contributions | Fidelity Charitable | web | FIE-A-001; FIE-A-002; FIE-A-005; FIE-A-006; FIE-A-008; FIE-A-013; FIE-A-022; FIE-A-127; FIE-A-131; FIE-A-134 |
| FIS-456caad1 | https://finance.duke.edu/adrecords/gifts-securities/ | Duke: Gifts of Securities (example) | Pershing (BNY) (custodian) | web | FIE-A-121 |
| FIS-f3d914e0 | https://financialdataexchange.org/about-fdx/ofx-work-group/ | OFX Work Group | Financial Data Exchange | web | FIE-B-039 |
| FIS-b6432815 | https://fixtrading.org/online-specification | FIX Latest Online Specification | FIX Trading Community | web | FIE-B-040 |
| FIS-8c37ab21 | https://frbservices.org/binaries/content/assets/crsocms/resources/financial-services/fednow/042126-quarterly-1q2026-fednow-ascii.txt | FedNow quarterly statistics 1Q2026 | Federal Reserve Financial Services | web | FIE-B-025 |
| FIS-38ed534e | https://frbservices.org/news/press-releases/071525-iso20022-migration-announcement | ISO 20022 migration announcement | Federal Reserve Financial Services | web | FIE-B-026 |
| FIS-430c5292 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | LLM01:2025 Prompt Injection | OWASP GenAI | web | FIE-C-049 |
| FIS-5281838a | https://github.com/Cisco-Talos/clamav/blob/main/COPYING.txt | ClamAV COPYING | Cisco Talos | web | FIE-C-015 |
| FIS-e9bac67c | https://givechariot.com/resources/insights/new-access-method-for-dafgiving360-in-dafpay | Chariot: New access method for DAFgiving360 in DAFpay | DAFgiving360 (formerly Schwab Charitable) | web | FIE-A-042 |
| FIS-85f85f73 | https://help.daffy.org/en/articles/12649376-when-will-my-stock-contribution-appear-in-my-daffy-account | When will my stock contribution appear in my Daffy account? | Daffy | web | FIE-A-083 |
| FIS-3de5af2d | https://help.daffy.org/en/articles/12649914-does-daffy-accept-stock-transfers-through-acats | Does Daffy accept stock transfers through ACATS? | Daffy | web | FIE-A-082 |
| FIS-4fa968b7 | https://help.daffy.org/en/articles/16219844-when-is-the-last-day-i-can-contribute-to-my-daffy-fund-for-it-to-count-on-my-2026-taxes | Daffy deadline + DAFgiving360 form | Cross-sponsor | web | FIE-A-133 |
| FIS-7c419e62 | https://help.daffy.org/en/articles/5594136-how-do-i-contribute-crypto-to-daffy | How do I contribute crypto to Daffy? | Daffy | web | FIE-A-084 |
| FIS-652608f7 | https://help.givechariot.com/onboarding/trust-and-safety/compliance | Chariot Compliance | Chariot | web | FIE-A-097 |
| FIS-17a228e0 | https://instafill.ai/forms/make-a-contribution-vanguard-charitable | Third-party form-filler description of Vanguard Charitable contribution form | Vanguard Charitable | web | FIE-A-060 |
| FIS-d80cb253 | https://intercom.help/bluegive-help-center/en/articles/9105614-bulk-attestations | BlueGive: Bulk attestations | BlueGive | web | FIE-A-094 |
| FIS-3db09020 | https://intercom.help/bluegive-help-center/en/articles/9922250-bulk-securities-upload | BlueGive: Bulk securities upload; Give RIA: Bulk securities contribution | BlueGive / Give RIA (TIFIN-family sponsors) | web | FIE-A-093 |
| FIS-11ba89e7 | https://intercom.help/rengiving/en/ | Ren Help Center (search; negative) | Ren (incl. Stellar/iPhi) | web | FIE-A-055 |
| FIS-5b0fd9c5 | https://intercom.help/rengiving/en/articles/10810347-edward-jones-charitable-gift-fund | Edward Jones Charitable Gift Fund (Ren help, search snippet) | Edward Jones Charitable Gift Fund (RCF) | web | FIE-A-057 |
| FIS-9faad3f4 | https://intercom.help/rengiving/en/articles/11004460-ej-daf-opening-instructions | EJ DAF Opening Instructions (Ren help; marked not for public use; read via search snippet; page now 404) | Edward Jones Charitable Gift Fund (RCF) | web | FIE-A-056 |
| FIS-25a2d3c2 | https://intercom.help/the-signatry/articles/6681020-how-to-contribute-stock-to-a-daf | How to contribute stock to a DAF (The Signatry) | The Signatry (independent sponsor) | web | FIE-A-089 |
| FIS-5ef6061a | https://investor.vanguard.com/gifting-stock | Vanguard brokerage gifting page (custodian side; sponsor page not found) | Vanguard Charitable | web | FIE-A-061; FIE-A-122 |
| FIS-1ada19f0 | https://learn.microsoft.com/azure/storage/blobs/immutable-storage-overview | Overview of immutable storage for blob data | Microsoft | web | FIE-C-029 |
| FIS-327cd0df | https://learn.microsoft.com/dotnet/api/system.xml.xmlreadersettings | XmlReaderSettings Class | Microsoft | web | FIE-C-037 |
| FIS-902656c3 | https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/model-overview | Document processing models | Microsoft | web | FIE-C-043 |
| FIS-7ad92c1f | https://learn.microsoft.com/en-us/azure/defender-for-cloud/introduction-malware-scanning | Introduction to Defender for Storage Malware Scanning | Microsoft | web | FIE-C-007; FIE-C-009; FIE-C-010 |
| FIS-9c057c7c | https://learn.microsoft.com/en-us/azure/defender-for-cloud/on-upload-malware-scanning | On-upload malware scanning | Microsoft | web | FIE-C-008 |
| FIS-c94e4639 | https://learn.microsoft.com/en-us/dotnet/api/system.text.json.jsonserializeroptions.maxdepth | JsonSerializerOptions.MaxDepth | Microsoft | web | FIE-C-038 |
| FIS-c17a917f | https://man.archlinux.org/man/extra/clamav/clamd.conf.5.en | clamd.conf(5) | ClamAV / Arch | web | FIE-C-014 |
| FIS-8e626469 | https://moderntreasury.com/learn/ach-return-code-reference | ACH return code reference | Modern Treasury | web | FIE-B-033 |
| FIS-397a252b | https://morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-recoverable-grants-faqs.pdf | MS GIFT Recoverable Grants FAQs | Morgan Stanley Global Impact Funding Trust (MS GIFT) | web | FIE-A-069 |
| FIS-c568612a | https://npact.document360.io/docs/how-to-import-grants | NPact: How to Import Grants (search snippet) | NPact (FIMS / DonorCentral, ex-Blackbaud) | web | FIE-A-109 |
| FIS-9deaaaf7 | https://nptrust.org/grant-recommendation-npt | NPT Grant Recommendation form | National Philanthropic Trust (NPT) | web | FIE-A-034 |
| FIS-b08117e3 | https://oag.ca.gov/charities/reports | Registry Reports | California Attorney General | web | FIE-B-052 |
| FIS-6535e469 | https://ofac.treasury.gov/sdn-list-data-formats-data-schemas/frequently-asked-questions-on-advanced-sanctions-list-standard | FAQs on advanced sanctions list standard | OFAC / US Treasury | web | FIE-B-051 |
| FIS-34abe77f | https://openwall.com/lists/oss-security/2019/08/06/3 | oss-security: ClamAV zip bomb | Openwall | web | FIE-C-013 |
| FIS-ed8f1e70 | https://pitchbook.com/profiles/company/507247-48 | PitchBook profile (secondary) | NPact (FIMS / DonorCentral, ex-Blackbaud) | web | FIE-A-110 |
| FIS-50846cd1 | https://platform.claude.com/docs/en/about-claude/pricing | Claude pricing (skill cache dated 2026-11-03) | Anthropic | web | FIE-C-045 |
| FIS-46a05bd9 | https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock | Claude API skill platform-availability table | Anthropic | web | FIE-C-047 |
| FIS-ab7df1fa | https://prices.azure.com/api/retail/prices | Azure Retail Prices API - 'Malware Scanning Data Ingested' | Microsoft | web | FIE-C-006; FIE-C-021; FIE-C-024; FIE-C-042 |
| FIS-997799df | https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonGuardDuty/current/us-east-1/index.json | AWS Price List API - GuardDuty | AWS | web | FIE-C-001; FIE-C-002 |
| FIS-cad39827 | https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/us-east-1/index.json | AWS Price List API - S3 | AWS | web | FIE-C-020 |
| FIS-2545a3b3 | https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonTextract/current/us-east-1/index.json | AWS Price List API - Textract | AWS | web | FIE-C-041 |
| FIS-c9a58261 | https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-commercial-api-data | How long do you store commercial API data | Anthropic | web | FIE-C-046 |
| FIS-ab64497d | https://ramp.com/blog/paper-check-processing-nonprofits | Paper check processing for nonprofits | Ramp | web | FIE-B-065 |
| FIS-51072b4c | https://registry.opendata.aws/irs990/ | IRS 990 Filings (Registry of Open Data on AWS) | AWS | web | FIE-B-048 |
| FIS-601c1d67 | https://schwabcharitable.org/non-cash-assets/cryptocurrency | Non-cash assets: cryptocurrency (search snippet) | DAFgiving360 (formerly Schwab Charitable) | web | FIE-A-040 |
| FIS-c9007cb5 | https://services.google.com/fh/files/misc/sec_cohasset_assessment_gcs_dec_2023.pdf | Cohasset assessment - Google Cloud Storage (Dec 2023) | Cohasset / Google | web | FIE-C-030 |
| FIS-2e7e11c8 | https://stealthagents.com/research/ai-cash-application-automation-statistics-2026 | AI cash application automation statistics 2026 | StealthAgents (aggregator) | web | FIE-B-013 |
| FIS-0498ba5b | https://support.foundant.com/hc/en-us/articles/40104667727255-Import-Grants | Foundant: Import Grants | Foundant CommunitySuite | web | FIE-A-104 |
| FIS-75ac22a2 | https://support.foundant.com/hc/en-us/articles/6899159450775 | Foundant: transaction import / donation import | Foundant CommunitySuite | web | FIE-A-105 |
| FIS-84b4de31 | https://swift.com/products/swift-gpi | Swift gpi product page | Swift | web | FIE-B-016 |
| FIS-59aa3cf1 | https://theclearinghouse.org/payment-systems/Articles/2024/04/CHIPS_Network_Migrates_ISO_20022_04-10-2024 | CHIPS Network successfully migrates to ISO 20022 | The Clearing House | web | FIE-B-027 |
| FIS-dc91cee5 | https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html | Zero-Click AI Vulnerability Exposes Microsoft 365 Copilot Data | The Hacker News | web | FIE-C-050 |
| FIS-41196c82 | https://tifin.com/product/give/our-solutions/ | TIFIN Give solutions | TIFIN Give (GiveClear Foundation) | web | FIE-A-090 |
| FIS-cc0fae02 | https://tifin.com/product/give/wealth-management-firms | TIFIN Give for wealth management firms | TIFIN Give (GiveClear Foundation) | web | FIE-A-091 |
| FIS-b3dc765a | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/resources/attachments/hr_data_structure.docx | Human Resource (HR) Data Structure | YourCause CSRconnect (Blackbaud) | web | FIE-A-117 |
| FIS-7a65595a | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/resources/attachments/sftp_connection_file_transfer.docx | CSRconnect SFTP connection & file transfer; Payroll Reconciliation Categories | YourCause CSRconnect (Blackbaud) | web | FIE-A-116 |
| FIS-079d7fe0 | https://webstore.ansi.org/Standards/ASCX9/ANSIX91001872021 | ANSI X9.100-187-2021 | ANSI Webstore / ASC X9 | web | FIE-B-036 |
| FIS-27321755 | https://www.acord.org/forms-pages/forms-participation-programs | ACORD forms participation programs | ACORD | web | FIE-B-042 |
| FIS-0745fe85 | https://www.aefonline.org/partner-gateway-welcome/ | Partner Gateway welcome / AEF FAQ | American Endowment Foundation (AEF) | web | FIE-A-045 |
| FIS-fba8a3aa | https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/ | Ren brings AEF fully onto its technology platform (press release 2026-04-08) | American Endowment Foundation (AEF) | web | FIE-A-043 |
| FIS-14a2b862 | https://www.ajmc.com/view/caqh-index-finds-20-billion-in-cost-savings-opportunities | CAQH Index finds $20 billion in cost savings opportunities | AJMC | web | FIE-B-007 |
| FIS-c25a7a58 | https://www.ali.org/sites/default/files/2026-08/transfer-securities_8-2026.pdf | American Law Institute securities transfer form (2026-08) | DTC (industry) | web | FIE-A-123 |
| FIS-997162d3 | https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf | Charitable Gift Fund Program Guidelines (Version 3.2024) | Bank of America Charitable Gift Fund | web | FIE-A-062; FIE-A-063; FIE-A-064 |
| FIS-73d9ceec | https://www.bankofamerica.com/signature-services/medallion-signature-guarantee/ | Bank of America: Medallion signature guarantee | Medallion Signature Guarantee (industry control) | web | FIE-A-125 |
| FIS-34f1acde | https://www.billtrust.com/?p=18777 | Billtrust AR Benchmark (page) | Billtrust | web | FIE-B-012 |
| FIS-344a90b8 | https://www.caqh.org/hubfs/Index/2024%20Index%20Report/CAQH_IndexReport_2024_FINAL.pdf | 2024 CAQH Index Report | CAQH | web | FIE-B-001; FIE-B-002; FIE-B-003; FIE-B-004; FIE-B-005; FIE-B-066 |
| FIS-98a5f069 | https://www.cfo.com/news/metric-of-the-month-accounts-payable-cost/659393/ | Metric of the Month: Accounts Payable Cost | CFO.com / APQC | web | FIE-B-010 |
| FIS-cb13aacc | https://www.coresecurity.com/blog/powertech-antivirus-and-clamav-detection-rate-comparison | Search-result summary (Splunk study cited); AV-TEST Linux tests place ClamAV near bottom | Splunk / AV-TEST via secondary | web | FIE-C-012 |
| FIS-d2b216b1 | https://www.corpay.com/en-IE/resources/blog/ap-team-productivity-benchmarks | AP Team Productivity benchmarks | Corpay citing APQC | web | FIE-B-011 |
| FIS-a5912df5 | https://www.dafgiving360.org/features/forms | Forms for Donors / Transfer of Assets form (search snippets) | DAFgiving360 (formerly Schwab Charitable) | web | FIE-A-037 |
| FIS-5bd697c0 | https://www.dafgiving360.org/temporarily-suspended-charities | Temporarily suspended charities / Explore charities (search snippets) | DAFgiving360 (formerly Schwab Charitable) | web | FIE-A-039 |
| FIS-0976fbea | https://www.donorperfect.com/nonprofit-technology-blog/featured/reduce-costs-and-relieve-burdens-with-nonprofit-cheque-scanning/ | Reduce costs with nonprofit check scanning | DonorPerfect | web | FIE-B-062 |
| FIS-cb148e4d | https://www.donorstrust.org/requesting-grant-daf/ | DonorsTrust Basics: Requesting a Grant (negative for intake) | DonorsTrust | web | FIE-A-088 |
| FIS-03f98d63 | https://www.dtcc.com/asset-services/securities-processing/deposit-withdrawal-at-custodian | Deposit and Withdrawal at Custodian | DTCC | web | FIE-B-054 |
| FIS-8f71b532 | https://www.federalreserve.gov/paymentsystems/frps_cy2015_24_topline.htm | National Payment Volumes, Top-Line Data (CY 2015-24) | Federal Reserve | web | FIE-B-023 |
| FIS-7be3d906 | https://www.fidelitycharitable.org/advisors/support/grants.html | Granting on behalf of a client / Grant Recommendation Form | Fidelity Charitable | web | FIE-A-014 |
| FIS-80af4344 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/144-145-contribution-form.pdf | 144/145 Contribution Form | Fidelity Charitable | web | FIE-A-009 |
| FIS-e3e0ffd7 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/complex-asset-contribution-form.pdf | Complex Asset Contribution Form (1.830409.113, created 2025-02) | Fidelity Charitable | web | FIE-A-010 |
| FIS-cf924877 | https://www.fidelitycharitable.org/faqs/all/returned-grant.html | Returned grant FAQ (via repo sponsor-grant-payment-policies.csv) | Fidelity Charitable | web | FIE-A-018 |
| FIS-9ee1c00e | https://www.fidelitycharitable.org/giving-account/contribution-timelines.html | Contribution processing guidelines and timelines | Fidelity Charitable | web | FIE-A-003; FIE-A-004; FIE-A-007; FIE-A-132 |
| FIS-5c84b667 | https://www.fidelitycharitable.org/giving-account/what-you-can-donate/donating-bitcoin-to-charity.html | Donating bitcoin to charity (and LOU) | Fidelity Charitable | web | FIE-A-012 |
| FIS-24a2a9d3 | https://www.fidelitycharitable.org/legal/granting-due-diligence.html | Grant review and due diligence process | Fidelity Charitable | web | FIE-A-015 |
| FIS-54cbc59d | https://www.financialprofessionals.org/about/learn-more/press-releases/Details/survey-79-percent-of-organizations-were-victims-of-attempted-or-actual-payments-fraud-activity-in-2024 | Survey: 79% of organizations were victims of payments fraud in 2024 | AFP | web | FIE-B-018; FIE-B-059 |
| FIS-8aea5fe7 | https://www.financialprofessionals.org/training-resources/resources/articles/Details/making-the-switch-moving-from-checks-to-digital-payments | Making the switch: moving from checks to digital payments | AFP | web | FIE-B-017 |
| FIS-d4422f2b | https://www.frbservices.org/wp-content/uploads/101326-fednow-service-operating-procedures.pdf | FedNow Service Operating Procedures v3.7 (Oct 2026) | Federal Reserve Financial Services | web | FIE-B-029 |
| FIS-c21d475c | https://www.growyourgiving.org/greater-giving/contribute-to-your-fund/ | Contribute to Your Fund (GKCCF) | Greater Horizons / Greater Kansas City Community Foundation | web | FIE-A-071; FIE-A-072; FIE-A-073; FIE-A-076 |
| FIS-d5b063d4 | https://www.growyourgiving.org/professional-advisors/charitable-giving-solutions/daf-financial-advisor-managed-account-faqs/ | DAF Financial Advisor-Managed Account FAQs | Greater Horizons / Greater Kansas City Community Foundation | web | FIE-A-074; FIE-A-075; FIE-A-077 |
| FIS-8632854a | https://www.highradius.com/resources/Blog/cash-application-process-leveraging-automation/ | Cash application process automation | HighRadius citing NACM | web | FIE-B-014 |
| FIS-2f6b291d | https://www.ice.com/publicdocs/Fee_Overview_2026.pdf | ICE Fee Overview 2026 | ICE | web | FIE-B-058 |
| FIS-6742e2dd | https://www.interactivebrokers.com/support/faq/content/29082320 | Interactive Brokers FAQ | Interactive Brokers (custodian) | web | FIE-A-124 |
| FIS-f72bd431 | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | Exempt Organizations Business Master File Extract (EO BMF) | IRS | web | FIE-B-043 |
| FIS-2bbf6d32 | https://www.irs.gov/charities-non-profits/form-990-series-downloads | Form 990 series downloads | IRS | web | FIE-B-047 |
| FIS-ea0dd0f6 | https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads | Tax Exempt Organization Search bulk data downloads | IRS | web | FIE-B-044; FIE-B-045; FIE-B-046 |
| FIS-7ad26f0f | https://www.irs.gov/e-file-providers/current-valid-xml-schemas-and-business-rules-for-exempt-organizations-and-other-tax-exempt-entities-modernized-e-file | Current valid XML schemas and business rules for EO MeF | IRS | web | FIE-B-049 |
| FIS-bb63567a | https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-dec-26-2025 | 2025 Filing season statistics | IRS | web | FIE-B-022 |
| FIS-8e2a1fef | https://www.irs.gov/newsroom/taxpayer-first-act-exempt-organizations | Taxpayer First Act - Exempt Organizations | IRS | web | FIE-B-050 |
| FIS-a62907ab | https://www.iso20022.org/faq | ISO 20022 FAQ | ISO 20022 RA (Swift) | web | FIE-B-030 |
| FIS-aa124944 | https://www.mailgun.com/state-of-email-deliverability/chapter/email-authentication-requirements/ | State of Email Deliverability - authentication | Mailgun | web | FIE-B-020 |
| FIS-cdd029ab | https://www.mismo.org/standards-resources/additional-tools-and-resources/about-mismo-licenses | About MISMO licenses | MISMO | web | FIE-B-041 |
| FIS-1d7d8b48 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf | MS GIFT Grantmaking | Morgan Stanley Global Impact Funding Trust (MS GIFT) | web | FIE-A-067 |
| FIS-b96619a8 | https://www.nacha.org/news/fbis-ic3-finds-almost-85-billion-lost-business-email-compromise-last-three-years | FBI's IC3 finds almost $8.5 billion lost to BEC in last three years | Nacha (citing FBI IC3) | web | FIE-B-019 |
| FIS-5f2899ac | https://www.nacha.org/news/same-day-ach-and-business-business-payments-propel-ach-network-volume-growth-2025 | Same Day ACH and B2B payments propel ACH Network volume growth in 2025 | Nacha | web | FIE-B-024 |
| FIS-aec0d6aa | https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-2 | Risk Management Topics - Fraud Monitoring Phase 2 | Nacha | web | FIE-B-034 |
| FIS-329a1991 | https://www.nptrust.org/funding-and-transfer-instructions-npt/ | NPT Funding & Transfer Instructions (form code NPT FOR FTI 0826) | National Philanthropic Trust (NPT) | web | FIE-A-024; FIE-A-025; FIE-A-026; FIE-A-027; FIE-A-028; FIE-A-029; FIE-A-030; FIE-A-031; FIE-A-032; FIE-A-131 |
| FIS-6be0d8c7 | https://www.nptrust.org/illiquid-asset-contribution-guidelines-npt | Illiquid Asset Contribution Guidelines / Real Estate Contribution Guidelines (2021-2022 PDFs) | National Philanthropic Trust (NPT) | web | FIE-A-033 |
| FIS-2aba4a0b | https://www.numeric.io/blog/bank-reconciliation-automation | Bank Reconciliation Automation guide 2026 | Numeric | web | FIE-B-015 |
| FIS-8ab28b0e | https://www.orderful.com/blog/cost-of-growing-trading-partner-backlog | Cost of growing trading partner backlog | Orderful | web | FIE-B-021 |
| FIS-22ee6932 | https://www.postgresql.org/docs/current/storage-toast.html | PostgreSQL docs: TOAST | PostgreSQL GDG | web | FIE-C-019 |
| FIS-cbbb2950 | https://www.postscanmail.com/services/digital-mailroom.html | Mailroom Automation | PostScan Mail | web | FIE-B-061 |
| FIS-2a70bac3 | https://www.reninc.com/wp-content/uploads/2022/03/RCF-Application-10-20-21-1.pdf | RCF Application (2021) | Renaissance Charitable Foundation (RCF) | web | FIE-A-058 |
| FIS-bdc7af40 | https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf | Ren Inc. Product Descriptions (2023-06-12) | Ren (incl. Stellar/iPhi) | web | FIE-A-049; FIE-A-050; FIE-A-051 |
| FIS-8a82c983 | https://www.reninc.com/wp-content/uploads/2026/05/2309-RCF-FRM-DAF-LPLCircular.pdf | RCF LPL circular (2023-10) | LPL Financial | web | FIE-A-126 |
| FIS-ef2fca07 | https://www.scanpilot.ai/research/handwriting-ocr-benchmark/ | Handwriting OCR Benchmark (2026) | ScanPilot (vendor) | web | FIE-C-048 |
| FIS-3670e375 | https://www.stedi.com/edi/x12-004050/823 | EDI 823 Lockbox | Stedi | web | FIE-B-038 |
| FIS-79c7c2c6 | https://www.stern.nyu.edu/experience-stern/faculty-research/why-goldman-sachs-affiliated-charity-giving-causes-goldman-sachs-opposes | Secondary article citing Program Circular | Goldman Sachs Philanthropy Fund | web | FIE-A-070 |
| FIS-81613a47 | https://www.submittable.com/docs/brightfunds/Bright_Funds_FAQs_Template.docx | Bright Funds FAQs Template | Bright Funds | web | FIE-A-118 |
| FIS-6a347882 | https://www.swift.com/news-events/press-releases/global-financial-community-completes-switch-iso-20022-paving-way-new-levels-cross-border-payment-speed-and-innovation-around-world | Global financial community completes switch to ISO 20022 | Swift | web | FIE-B-028 |
| FIS-a097368a | https://www.theglobaltreasurer.com/2016/01/14/the-camt053-bank-statement-standard-a-users-guide/ | The CAMT053 bank statement standard: a user's guide | The Global Treasurer | web | FIE-B-035 |
| FIS-e93a6eed | https://www.usenix.org/conference/woot19/presentation/fifield | A better zip bomb | USENIX / David Fifield | web | FIE-C-032 |
| FIS-3e7b4a74 | https://www.wexinc.com/resources/blog/what-does-it-cost-to-process-an-invoice-ap-benchmarks-every-finance-team-should-know/ | What does it cost to process an invoice | WEX (citing Ardent) | web | FIE-B-009 |
| FIS-c74625ab | https://x12.org/licensing | X12 Licensing Program | X12 | web | FIE-B-064 |
| FIS-a683c5c5 | n/a | Proposal | Proposed (any sponsor) | repository | FIE-A-136; FIE-A-137; FIE-A-140; FIE-A-141; FIE-A-142 |
| FIS-b359438f | repo:data/mission-2026-11-14/aogf-benevity-reconciliation.csv | AOGF / Benevity reconciliation | Benevity / American Online Giving Foundation | repository | FIE-A-115 |
| FIS-985c1f1e | repo:data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv | CF vendor migrations 2022-2026 | Foundant CommunitySuite | repository | FIE-A-108 |
| FIS-d6e0ba1a | repo:data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv | CF rails and portals census v2 | Community foundations (portal/rails census) | repository | FIE-A-111 |
| FIS-d3576cdb | repo:data/mission-2026-11-14/daf-data-standards-2026.csv | DS16 DAF Direct | Fidelity Charitable | repository | FIE-A-023; FIE-A-100; FIE-A-128; FIE-A-138 |
| FIS-e5fee95b | repo:data/mission-2026-11-14/matching-gift-daf-policies-2026.csv | Matching gift DAF policies | Corporate matching programs | repository | FIE-A-119 |
| FIS-3033a2eb | repo:data/mission-2026-11-14/sponsor-grant-payment-policies.csv | Sponsor grant payment policies (row Fidelity Charitable) | Fidelity Charitable | repository | FIE-A-016; FIE-A-035; FIE-A-038; FIE-A-059; FIE-A-085; FIE-A-087; FIE-A-092; FIE-A-095; FIE-A-098; FIE-A-101 |
| FIS-84b199ad | repo:research/ai-native-daf-enterprise/02-business-capabilities/functional-areas/C-contribution-processing.md | C. Contribution processing §1 | Ren (incl. Stellar/iPhi) | repository | FIE-A-052; FIE-A-129; FIE-A-135 |
| FIS-28ca5085 | repo:research/ai-native-daf-enterprise/03-workflow-redesign/wf-relationships-servicing.md | Workflow: relationships and servicing | Proposed (any sponsor) | repository | FIE-A-139 |
| FIS-29a234a3 | repo:research/mission-2026-11-14/b4013-02-b4222-02-remittance-and-portal-features.md | Grant remittance at the top-10 sponsors §3 | Fidelity Charitable | repository | FIE-A-017; FIE-A-053; FIE-A-068; FIE-A-078; FIE-A-081; FIE-A-102; FIE-A-103; FIE-A-107; FIE-A-130 |
| FIS-0381d4ce | repo:research/mission-2026-11-14/b4222-02-01-01-foundant-docs-ncf-donate.md | Foundant docs and NCF donate button §2.2 (quoting ncfgiving.com guide) | National Christian Foundation (NCF) | repository | FIE-A-079; FIE-A-080 |
| FIS-96e976b1 | repo:research/mission-2026-11-14/direction-ai-product-census.md | AI product census (Kindsight mention) | CSuite / Kindsight | repository | FIE-A-112 |
| FIS-e43945bc | repo:research/mission-2026-11-14/direction-noncash-gift-infrastructure.md | Non-cash gift infrastructure (P-NEW-NCG-01) §1 item 6 | Fidelity Charitable | repository | FIE-A-011; FIE-A-041; FIE-A-047 |
| FIS-af608509 | repo:research/mission-2026-11-14/direction-nonprofit-side-experience.md | Nonprofit-side experience (practitioner forum paraphrase, line ~101) | Fidelity Charitable | repository | FIE-A-020 |
| FIS-44a6280d | repo:research/mission-2026-11-14/gap19-edward-jones-wealth-channels.md | Gap-19 pass §0 item 6; remittance doc §4 | Bank of America Charitable Gift Fund | repository | FIE-A-065 |
| FIS-b3095e73 | repo:research/mission-2026-11-14/queue-npt-givingpoint-fidelity-stack.md | NPT GivingPoint and Fidelity stack (P-QA1-02) | Fidelity Charitable | repository | FIE-A-021; FIE-A-036 |
| FIS-4ed86cb4 | repo:research/mission-2026-11-14/queue-ren-iphi-attrition.md | Ren iPhi attrition §1 item 7 / remittance doc row AEF | American Endowment Foundation (AEF) | repository | FIE-A-046; FIE-A-054 |
<!-- END GENERATED: sources -->
