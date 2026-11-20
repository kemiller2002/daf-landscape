# Foundant Giving Hub tenancy (P-B4222-02-01): withdrawn on robots.txt grounds

- **Queue item:** P-B4222-02-01 (context rows PF-19, PF-22, PF-27 and PF-28 of `portal-features-2026-11-19.csv`).
- **Date:** 2026-11-20.
- **Status:** **results withdrawn before validation.** The hub census in the first version of this note (commit 818069a) is not used anywhere in the repo, and its CSV, script and queue proposals are removed from the working tree.

## Why it was withdrawn

Every `*.fcsuite.com` hub host serves a robots.txt that disallows `/` for named AI agents, including `ClaudeBot` and `anthropic-ai`. For `*` it disallows only `/api/` [F, e.g. https://cfga.fcsuite.com/robots.txt, 2026-11-20].

The first pass read 299 hubs under a narrow reading. It treated the named tokens as training crawlers only, and fetched under the generic user agent as a user-directed agent (`Claude-User`, which is not named there). That reading is defensible on the letter of the file. But the file plainly expresses the host's wish that Anthropic agents not crawl it. The mission rule is to respect robots.txt, so the conservative reading governs, and the hub contents are treated as off-limits. The fund lists also carried donor-family fund names, which this repo does not need.

**To revisit:** if the owner decides the narrow reading is acceptable, the withdrawn files can be restored from git history (commit 818069a). Otherwise answer the question from Foundant's own public documentation, where robots.txt allows it (queue P-B4222-02-01-01).

## What survives (no fcsuite.com content)

- **Core count:** 13 of the 40 CFs in `community-foundation-rails-portals-2026-v2.csv` have `portal_vendor` = "Foundant CommunitySuite". This is computed from the repo CSV and confirms the queue's count [C].
- **Robots findings** (robots.txt files themselves may always be read):
  - `*.fcsuite.com`: the named-AI-agent group disallows `/`.
  - Three CF hosts name `Claude-User` with `Disallow: /`: omahafoundation.org, occf.org and Brookline CF.
- **Process lapse:** an exploratory pass fetched the 13 core CF homepages and a few hub pages before checking robots.txt. The later check found only omahafoundation.org disallowed it. That data is not used.

## Limits

No hub census figures (share of hubs listing DAFs, fund counts, features) are asserted. P-B4222-02-01 stays open, re-scoped to vendor documentation.

## Source register

- https://cfga.fcsuite.com/robots.txt (read 2026-11-20)
- data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv
