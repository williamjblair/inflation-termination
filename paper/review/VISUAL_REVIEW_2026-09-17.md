# Figure and layout revision — 17 September 2026

Baseline: `74c4d88cd443c3f2e687a8ec44e1cbe2e08bd9c0`.

Revised all eight figures, using editable TikZ diagrams and a vector PDF plot. The manuscript now has 53 pages, one more than the baseline, with unchanged body type size and margins. The additional space accommodates the expanded explanatory diagrams.

## Changes

- **Classification:** aligned the terminating and nonterminating cases in labeled panels, with the graph conditions and their consequences directly below the diagrams.
- **Triangle:** arranged sources along the triangle edges, removing crossings from the original and copied causal diagrams. Matching source colors preserve the correspondence between the panels.
- **Cycle reduction:** highlighted each arc and labeled the products that become the three triangle observations. Separated the boundary-source and private-randomness explanations.
- **Five-observer path:** added the conditional bilocal diagram beneath the original path. Highlighted the conditioned endpoints and displayed the compatible bound beside the target's violation.
- **Convex order:** replaced the box flowchart with permuted-row and independent-index sampling diagrams. Displayed the conditional-expectation identity and convex comparison together.
- **Thresholds:** improved typography, marker visibility, the shared legend, and the annotation identifying the one-sided square order-two bound. Hollow NW markers allow coincident AI markers to remain visible. The analytic guarantees retain dashed lines and their explicit formulas. No certificate inputs, certified values, or analytic curves changed.
- **Defect cube:** reduced background-grid contrast, labeled the three observation lines directly, and made the solid, dashed, and dotted line styles distinct. Displayed the shared-defect case split beside the cube.
- **Fan:** highlighted one cross pair and placed its disjoint source-parent sets alongside the fan. Removed redundant copy labels that interfered with the cross-pair annotation.

The diagrams use shared node, arrow, panel-title, and annotation styles. Shapes, labels, and line patterns preserve the distinctions when printed in grayscale.

## Validation

- Ordinary and standalone arXiv builds pass, with matching extracted PDF text and 53 pages each.
- The final ordinary build has no overfull or underfull boxes, undefined references, or multiply defined labels. The standalone build also passes its reference and overflow checks.
- All eight figures were inspected in the manuscript and as enlarged standalone previews. Grayscale previews were checked; the final plot and defect-cube refinements were re-rendered.
- The original eight figure labels are preserved.
- The threshold provenance file is byte-identical to the baseline; its recorded certificate SHA-256 hashes match the current inputs.
- The arXiv archive contains the four expected members, whose bytes match the release directory.
- Mathematical statements, proof bodies, Lean sources, Palomar files, and certificate data are unchanged. This revision does not rerun mathematical or Lean verification for those unchanged files.

Deliverables: `paper/main.pdf`, `paper/release/arxiv-src/main.pdf`, and `paper/release/arxiv-src.tar.gz`. Local inspection images are under the ignored directory `tmp/pdfs/visual-refresh/`.
