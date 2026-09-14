# Manuscript review and revision — 14 September 2026

Reviewed the complete manuscript at `53c7c27a`, including all sections, the three appendices, bibliography, certificate descriptions and formalization boundaries. This is an editorial and mathematical consistency review, supported by fresh certificate replays and the existing Lean audit. It is not independent specialist peer review.

## Revised paper

The headline classification remains Theorem 4.2. Sections 5–7 now present its three proof components consecutively: double-star reconstruction, cycle obstruction and five-path obstruction. The quantitative cycle refinements occupy Section 8. The defect family and its consequences occupy Sections 9–14. The new Section 17 distinguishes analytic proof, exact finite computation, and Lean coverage.

The abstract is 207 words. Repeated proof roadmaps, scope statements, research-campaign history and verification inventories have been consolidated. The triangle recursive-prescription proof now invokes the earlier root-sink lemma. The larger-alphabet corollary uses the existing transfer argument. The bibliography has clickable source and DOI links. The paper has eight vector figures and a compact contents list.

## Mathematical corrections

1. **Double-star response-table cardinality.** The number of maps from a product of leaf supports to the central alphabet is the alphabet size raised to the *product* of support sizes. The former product of separately exponentiated alphabet sizes generally gave the wrong count. The reconstruction itself is unchanged; empty leaf products equal one.
2. **Auxiliary positivity versus observed full support.** The cycle auxiliary density is positive, but its pushforward obeys parity constraints and is not positive on every observed assignment. The five-path witness likewise has deterministic relations among copied observations. The revised statements distinguish a positive auxiliary density, a nonnegative rational witness, and a strictly positive target. The noisy cycle targets and the path target retain the positivity needed by the classification.
3. **Exact thresholds versus certified brackets.** The saved primal witnesses lie at rational lower endpoints. A dual polynomial root does not establish feasibility at that root. Unjustified exact values were replaced by the actual certificate intervals. The exact order-one values and triangle NW order-two endpoint remain, with a proof reference.
4. **Equality and asymptotic claims.** Matching intervals at odd orders do not prove equality of thresholds. Ten finite orders do not prove an asymptotic exponent, limiting constant, or exclusion of another asymptotic behavior along the same direction. These claims were removed from the theorem discussion and open problems. The finite even-order strict separations remain certified. The cross-order strict comparison was restricted to `2 <= t <= 9`, excluding `t = 3`; the former inclusion of `t = 1` failed for the triangle.
5. **Count-moment proof.** Replaced the path-realization sketch with a construction: pair opposite terminals only on the larger bipartition, match the remaining terminals along adjacent edges, and route the opposite pairs through unused copies on the other bipartition. The proof now checks the internal-copy budget. The triangle degree realization is stated explicitly. The boundary characterization is correctly stated for a cycle, not an arbitrary connected graph. The monotonicity proof now handles `q = 0` before dividing by `q`.
6. **Five-path distance.** Its theorem gives a lower bound of order `t^-2`, not a matching distance asymptotic. The concluding paragraph now states that distinction. The formal product functional uses `6t + t^2` coordinates, correcting the former count.
7. **Verification claims.** The finite-threshold proposition does depend on computation; the blanket statement that no proofs depend on computation was removed. Paths to a coverage file and an open Lean library absent from this repository were replaced by the actual README, YAML and audit locations. Finite-latent graph formalization is distinguished from the arbitrary-latent triangle theorem.
8. **Other precision fixes.** Corrected the fan certificate parameter list from the actual checked records (including `k = 5`, excluding the absent `k = 16384`). Added the missing `n >= 2` hypotheses to the supplementary same-order inequality and independent-cell bound. A compatibility inequality is no longer described as itself giving a finite rejecting order. The hypergraph discussion no longer asserts an undefined induced-substructure transport theorem.
9. **Attribution.** The polynomial-optimization nontermination example is attributed explicitly to Navascués–Wolfe, rather than to the preceding Wolfe–Spekkens–Fritz sentence. Checked the context against [Navascués–Wolfe, Section 4.1](https://arxiv.org/html/1707.06476v3). The finite-cardinality scope is consistent with [Rosset–Gisin–Wolfe](https://arxiv.org/abs/1709.00707).

## Supporting material retained and deferred

The compiled supplementary appendix retains complete proofs of the pair-retaining fan inequality and square conditioning, independent-cell variance and distance bounds, finite catalogue, polynomial identity transfer, and order-two extraction obstruction.

The full former appendix is preserved byte-for-byte in `deferred-supporting-original.tex`. The following material is excluded from the submitted paper:

- The superseded orthogonal quadratic witness, which adds length without improving the main lower bound.
- The matching-selector construction and exact square rejection theorem, whose factorization and proof details were delegated to source notes unavailable in this repository.
- The sharp defect ceiling and binary/ternary independent-cell claims, whose uniform tail estimates and long proofs are missing from the manuscript.
- The order-six parity extraction theorem, which had a theorem statement but no proof here.

Deferral is not a disproof. These results require complete, reviewable proofs and accessible provenance before reintegration. Historical narrative claims in the frozen certificate reports are not promoted to mathematical conclusions; the paper uses the verified rational data with the narrower scope above.

## Figures

1. Double-stars versus induced cycles and the five-path.
2. Triangle source DAG and one indexed copied triangle.
3. Cycle contraction to three arc products.
4. Five-path conditioning and the bilocal obstruction.
5. Conditional-expectation diagram for the convex-order argument.
6. Certified parity thresholds, read directly from the certificate JSON files, with no fit or extrapolation.
7. Defect-cube line geometry and the conditional mixture law.
8. Fan incidence diagram with the cross-pair moment used by the inequalities.

TikZ renders the diagrams. `paper/figures/generate_thresholds.py` renders the plot, and `thresholds-provenance.json` records its input hashes. The submission package includes the plot PDF; no Python or shell escape is needed to compile it.

## Validation

- `lake build`: passed, 3387 jobs. The only open-proof warnings are the two required registry challenge statements.
- `bash scripts/check_axioms.sh`: passed for all 112 audited declarations; only `propext`, `Classical.choice`, and `Quot.sound`.
- Classification certificate verifier: passed.
- Parity-threshold verifier: all 20,004 exact checks passed.
- Fan verifier: passed for 14 targets and its pointwise, embedding and negative-control checks.
- Hardened nontermination checker: passed in a temporary copy of its certificate directory.
- All 35 printed decimal threshold endpoints agree exactly with the JSON; all two-sided widths equal `4 * 10^-9`.
- The new routing construction passed 37,470 finite degree/capacity checks through order 12. This sanity check supplements the written proof.
- Main and standalone submission PDFs compile without overflow or unresolved references. Extracted text agrees between the two builds.
- All pages were rendered and visually inspected; the proof diagrams received additional enlarged inspection.

The main Lean statements and certificate bytes were not changed. New prose proofs and mathematical corrections have not been independently reviewed by a specialist. The worst-case convergence exponent and exact defect-family constant remain open.

## Publication state

This is a local revision. No push, arXiv upload, Palomar registration, or message to another person was performed. The previously registered version 1 and the pending version-2 submission described by the author identify their earlier snapshots. The local revision should not be described as the manuscript already attached to either record.


## Figure and spacing follow-up

The layout review after commit `802d4ab` revised all eight figures: aligned panel labels and node sizes, increased the convex-order arrow clearance, moved defect-cube labels into a separate legend, separated the fan connector from its explanation, and widened the threshold plot gutter. Caption and float spacing is now explicit. Float barriers keep the path illustration before the target-properties lemma and the convex-order diagram before the following corollary. Both tables have improved row spacing; the certificate table uses ragged-right columns, and bibliography URLs can wrap without stretching prose.

The manuscript remains 53 pages with eight figures. All pages were rendered for a layout sweep, with enlarged inspection of every figure, both numbered tables, and the bibliography. Main and standalone builds were checked again; the mathematical statements, Lean sources, and certificate data were unchanged in this follow-up. Earlier Lean and exact arithmetic checks above were not rerun for these layout changes.

The editorial revision was committed and pushed as `802d4ab`; the author has also authorized committing and pushing this layout follow-up. Neither action updates an arXiv submission or a Palomar record.
