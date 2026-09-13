# Reporting instead of scoring

Responsive UI reviews report concrete findings, not readiness percentages or checklist coverage.

For each finding include the source location, the layout assumption, the triggering condition and impact, and a focused fix. Prioritize loss of access to content/actions over cosmetic spacing. Distinguish direct code evidence from conditional layout consequences in plain language.

The optional legacy scanner retains null `overall_readiness` and `pillar_scores` fields for compatibility with its JSON schema. They are not grades and do not belong in the normal review output.
