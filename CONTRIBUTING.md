# Contributing evidence

Every change should make the repository more traceable, not merely larger.

## Add or change a claim

1. Add the source to `data/source-register.csv` with a stable source ID.
2. Record publication/effective date when the source supplies one; otherwise use `n.d.`.
3. Record the actual access date and an evidence grade.
4. Add the smallest supportable claim to the landscape or matrix and cite the source ID.
5. If the source is vendor-authored, describe the capability without adopting promotional superlatives.
6. Put inferences and interview propositions in the hypothesis backlog, not in verified fields.

## Evidence rules

- Prefer a regulator, filing, audited statement, policy, contract, or official documentation over a marketing page.
- Do not use a search-result snippet as the permanent source; cite the underlying page or document.
- Do not infer that a missing capability is absent. Use `unknown` unless an authoritative source establishes `no`.
- Do not copy changing statistics without their period, unit, definition, and source.
- Record acquisitions and rebrands with both the announcement date and the current entity name.
- Archive or replace broken sources; do not silently delete the evidence trail.

## CSV conventions

- UTF-8, comma-delimited, one header row, LF line endings.
- Stable IDs are never reused.
- Multiple source or role IDs use `|` as a separator.
- Dates use `YYYY-MM-DD`; use `YYYY`, `YYYY-MM`, or `n.d.` only when the source is less precise.
- Capability values are `yes`, `no`, `unknown`, or `not_applicable`.
- A `yes` means the cited evidence directly supports the capability, not that the product has been independently tested.

## Pull request checklist

- [ ] Every new fact has a registered source.
- [ ] Facts and hypotheses are separated.
- [ ] Vendor-reported claims are identified as such.
- [ ] Dates and current names have been checked.
- [ ] CSV files parse and retain their headers.
- [ ] Links resolve or the limitation is documented.
