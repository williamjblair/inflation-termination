# Submission finalization — 16 September 2026

Reviewed the full manuscript from baseline `76a1644f2f92ef3ec4f0462147ee69903964b0ba`, including the new quantitative results, supporting arguments, figures, tables and references. The final PDF has **52 pages**, including 37 pages of main text (pages 2–38), eight figures and two numbered tables. This is an editorial and mathematical consistency review, not independent specialist peer review.

## Changes

- Shortened the abstract to 208 words while retaining the classification, quantitative rates, hierarchy comparisons, rejecting-order results and formalization scope. Synchronized the arXiv fields.
- Removed repetitive introductions, vague claims and the manuscript's unlinked companion-paper promise. Preserved the existing eight-section structure and all results.
- Required positive noise in both full-support survivor corollaries. Clarified the direction of the erasure bijection in the cycle argument and corrected a witness/law membership statement in Appendix B.
- Replaced an unsupported suggestion of limiting threshold constants with certified finite-order values. Sharpened the open questions so they do not assume a power-law rate or ask for a strict separation at order one.
- Expanded the cubic-certificate rejecting-order argument: the Taylor remainder, the variance bounds and the averaging step are now explicit. The text retains the attribution to Navascués–Wolfe and distinguishes the explicit bound from the stronger known rejection of the W law.
- Restricted the Appendix D counterexample to the coefficient-extraction step it actually refutes; it does not disprove a general inequality-transfer or distance theorem.
- Split the crowded parameter-range display into cases and moved the coverage table out of a nearly empty float page. Set the bibliography in the standard smaller reference size, eliminating a final page containing only the end of one reference. Main-text type size and margins are unchanged.
- Cited published Palomar version 1. The public recent-record listing showed only that version during this review; the author reports a new-version submission is running. No registry submission or configuration was changed.

All 180 original labels and all 59 proof environments remain. Of the proof bodies, 57 are byte-identical to the baseline; the two edits clarify the classification proof's closing reference and correct the Appendix B membership statement. The expanded cubic argument is in a remark, outside those proof environments.

## Verification

Both the ordinary build and the flattened submission build pass. The final LaTeX passes have no overfull or underfull boxes, unresolved references or multiply defined labels. Their extracted PDF text is identical. All pages were visually reviewed as rendered contact sheets, and pages affected by the final layout edits were re-rendered and checked individually.

Fresh checks:

| Check | Result |
| --- | --- |
| `python3 -B artifact/certificates/exponent/odd/verify_odd.py` | Pass: 5,115 local checks and 9,084 exponent checks |
| `python3 -B artifact/certificates/beyond-finner/verify_beyond_finner.py` | Pass: 68,183 exact checks |
| Artifact manifest | All 56 entries match |
| Standalone archive | Four expected members; archived bytes match the release directory |
| Abstract and arXiv fields | Exact match |

The cubic verifier includes checks on sampled models. Those checks do not replace the analytic proof of the universal inequalities. Unchanged legacy certificate suites were not rerun in full.

No Lean sources, Palomar files, dependency pins, certificate files or verification scripts were edited by this review. Concurrent changes to Lean files, `formalization.yaml` and `scripts/gen_challenge.py` appeared during the review and were left alone. Consequently, this report does not claim that the entire working tree's protected files remain byte-identical or that those concurrent changes have been validated. No Lean build or axiom audit was rerun.

The machine-readable record and output hashes are in [submission-finalization-2026-09-16.json](submission-finalization-2026-09-16.json). Earlier review records describe their own snapshots and do not supersede this record.

## Submission files

- `paper/main.pdf`: final manuscript.
- `paper/release/arxiv-src.tar.gz`: upload archive containing `main.tex`, `main.bbl`, `references.bib` and `figures/thresholds.pdf`.
- `paper/release/ARXIV_PASTE.md`: synchronized submission fields.

The source archive builds locally using pdfLaTeX without shell escape. The author should inspect arXiv's generated PDF before completing submission. No arXiv upload, Palomar action, commit or push was performed in this review.
