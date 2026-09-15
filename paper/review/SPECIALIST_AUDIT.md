# Specialist-style mathematical audit

**Date:** 2026-09-15  
**Reviewed commit:** `689af3eaed081e62699690fd1f8ae6af1d560fc4`  
**Manuscript:** *Inflation for Classical Pair-Source Networks: Termination and Quantitative Obstructions*, current 49-page version.

## Correction status: addressed, 2026-09-15

The follow-up revision addresses A1–A5 and the opening nonconvexity sentence. The original findings below describe the reviewed commit, before these corrections.

| Finding | Resolution |
| --- | --- |
| A1 | Required scenario files, parameter caps and complete unique order/hierarchy records; explicit partial-run labeling; 19 failure-handling tests |
| A2 | Private-source convention in Theorem 4.8, also referenced by Corollary 6.1 |
| A3 | Corrected attribution and explanation: degree-two diagonal constraints suffice for the quadratic bound |
| A4 | Qualified the abstract, Section 8, README, YAML map and verification guide; rationality remains analytic and the mapped triangle declaration is an endpoint specialization |
| A5 | Marked the campaign report historical and identified the undistributed discovery scripts; current guide states the supported verification workflow |

The refreshed artifact manifest excludes mutable replay logs and verifies all 47 listed files. The threshold verifier passed 20,266 checks across all 40 published records; its 19-case mutation suite passed. Both final LaTeX builds have zero overfull/underfull boxes or unresolved references, and the standalone PDF text matches the manuscript. The six changed pages were rendered and visually checked. The paper remains 49 pages and all 57 proof bodies are unchanged. Lean sources are unchanged from the successful audit build below.

Follow-up evidence: [corrections/summary.json](specialist-audit-evidence/corrections/summary.json).

## Recommendation

**Minor revisions before submission.** This audit found no fatal gap or counterexample in the main classification proof or the quantitative arguments examined. The classification has a coherent proof, and the quantitative results give the paper substance beyond a graph classification. The issues below are localized definition, explanation, formalization-coverage and reproducibility issues. They do not require another structural rewrite.

This is an AI-assisted referee-style audit by the same assistant involved in the preceding editorial work. It is not independent human specialist review, an external acceptance decision, or a guarantee of correctness or priority. In particular, a successful Lean build verifies the formal statements against their definitions; it does not automatically verify every sentence of the manuscript.

## Findings requiring correction

### A1 — P2: The parity verifier can report success without any certificates

**Location:** `artifact/certificates/exponent/verify_exponent.py:543–551`.

The driver prints a missing-file message and continues when either required JSON file is absent. With an empty certificate directory, it exits with code zero and prints:

```text
=== brackets ===

OK: 0 exact checks passed in 0.0s
```

This was reproduced on the reviewed commit using the documented `--dir` argument. A broken download or incorrect directory can therefore look like a successful verification to an automated runner. In addition, `verify_file` iterates the records supplied by the certificate without enforcing a complete, unique list of scenario/order/hierarchy claims.

**Correction:** Reject missing required files. Distinguish verification of a partial certificate from verification of the full published coverage. For a full replay, require exactly the advertised scenario/order/hierarchy records, and add negative tests for a missing file and a removed or duplicated record. Preserve an explicitly labeled partial mode if useful.

**Impact:** Reproducibility assurance. The actual distributed threshold files passed all 20,004 checks in this audit; this finding does not refute their numerical bounds.

### A2 — P2: The general-scenario extension needs a convention for source-free observations

**Location:** `paper/sections/17-cycle-quantitative.tex:151`, Theorem 4.8; inherited by Corollary 6.1.

Section 2 excludes isolated observed vertices. Theorem 4.8 generalizes to any correlation scenario and says to replace edges by sources in the inflation definition, but does not require each observation to read a source.

Under the literal generalized definition, an observation with no parents has one copied coordinate, because there is only one empty index tuple. That same coordinate appears in every diagonal row. For a single fair binary observation and no sources, compatibility is immediate, but order two would require the law of `(O,O)` to be two independent fair bits. That is impossible: its probability at `(0,1)` is zero instead of one quarter. Thus this extension does not define a sound compatibility test on the whole class described.

The conditional convex-order assertion for a law that passes the stated test is not disproved by this example. The problem is the claimed general modeling scope and its inflation convention.

**Correction:** Require at least one parent source per observation, or explicitly append an independent private source to every source-free observation before defining the inflation. State that convention in the general theorem. Pair-source scenarios in the classification are unaffected.

### A3 — P3: The explanation of the source-count improvement overstates the diagonal information needed

**Location:** `paper/sections/17-cycle-quantitative.tex:182`.

The text attributes removal of the source-count factor to using the full diagonal law instead of its first two degrees. The full law is used for comparison with *every* convex function, but the quadratic estimate already follows from degree-two diagonal information.

Indeed, retain the random-permutation construction and the identity

\[
\mathbb E[\widehat P\mid\omega]=q_\omega.
\]

For `n >= 2`, degree-two diagonal constraints and symmetry make every pair of distinct rows independent with marginal `P`. Consequently,

\[
\mathbb E\|\widehat P-P\|_2^2
=\frac{1-\|P\|_2^2}{n},
\qquad
\mathbb E\|q_\omega-P\|_2^2
\le\mathbb E\|\widehat P-P\|_2^2.
\]

No higher diagonal degree enters this calculation. The improvement comes from the conditional-expectation/variance argument.

**Correction:** Separate the full convex-order assertion from its quadratic corollary. Also identify the exact `L(1-||P||²)/n` comparison as a consequence of the collision argument, rather than as the literal formula in the cited equation. [Navascués–Wolfe equation (A7)](https://arxiv.org/html/1707.06476v3) gives a sampling-distance bound, and equation (37) states the asymptotic Euclidean rate.

**Impact:** Accuracy of explanation and attribution; the new bound itself survives this audit.

### A4 — P3: The formalization map needs clause-level qualifications

**Location:** `README.md:294`, `paper/sections/11-reproducibility.tex`, and the corresponding coverage metadata.

The manuscript's Theorem 3.2 includes a rational-witness assertion. The mapped Lean theorem `nontermination_of_not_doubleStar` proves existence, normalization, strict positivity, expressible feasibility and finite-latent incompatibility for a real-valued law. Its statement contains no rationality predicate. The analytic rationality argument is straightforward from the displayed finite constructions, but it is not the same claim as a formal proof of rationality.

There are smaller parameter-level differences too. The mapped terminal theorem `triangle_linear_witness` is stated at `q = 1/(16t)`, whereas manuscript Theorem 4.4 covers the entire positive interval below that value. Its auxiliary lemmas appear to supply the more general ingredients. The README already describes the endpoint specialization, which should be retained rather than silently promoted to full statement coverage.

**Correction:** Label the classification equivalence and positive-witness existence as formalized, and the rationality clause as analytic unless a declaration proving it is added. Preserve the existing finite-latent and binary-outcome qualifications. List parameter-specialized declarations as such.

**Impact:** Precision of the verification claim, not an identified defect in the analytic theorem.

### A5 — P3: The threshold artifact's local instructions refer to undistributed scripts

**Location:** `artifact/certificates/exponent/REPORT.md:6–19`.

The report instructs readers to run `build_exponent.py` and `analyse_exponent.py`, but neither file is tracked in this repository. The report is historical campaign material; its statement that nothing under `artifact/` was touched is also confusing now that the report lives there.

**Correction:** Mark the report as historical and direct readers to the current verification guide, or distribute the discovery scripts if regeneration is intended to be supported. State explicitly whether the release supports certificate verification, certificate regeneration, or both.

**Impact:** The shipped checker is sufficient to verify the supplied certificates. Reproducing the discovery workflow by following this report is currently unsupported.

## Mathematical audit coverage

The current TeX proof chain was examined, including the supporting appendices. These are the principal checks and their outcomes; “no gap found” is an audit observation, not a replacement proof.

| Claim | What was checked | Outcome |
| --- | --- | --- |
| Classification, Theorem 3.2 | Correct logical direction of termination/nontermination; connected components; shortest induced cycle or induced five-path; induced-subgraph extension | No gap found |
| Root-sink equivalence | Active-trail criterion; closure under marginalization and gluing; cancellation on positive fibers and treatment of zero fibers | No gap found |
| Double-star reconstruction | Independence of all leaf copies; positive conditioning event covering leaf supports; simultaneous response tables; fresh independent sources; empty leaf sets and unsupported values | No gap found |
| Cycle witnesses | Fourier normalization and positivity; allowable character boundaries; ancestral products; contraction to a triangle; quantitative rigidity; noise and TV constants | No gap found |
| Five-path witness | Conditional bilocal inequality; endpoint-cell denominators; real-part product functional; real injectable expectations; disjoint auxiliary coordinates for ancestral blocks | No gap found |
| Corrected densities | Phase estimate; bounds on `R`; Fourier coefficients changed only outside prescribed boundaries; constants for three and four source families | No gap found |
| Convex-order theorem | Compatibility of each extracted law; conditional mean identity; Jensen; empirical variance; conversion between TV and Euclidean norm | Argument valid, with A2 and A3 to clarify |
| Square order conversion | Coloring source-type conflicts; capacity bound `2b + 2Δ <= 3t`; embedding components in diagonal rows; independence within a row | No gap found |
| Count-moment reductions | Parity-forced potentials; gauge/permutation symmetrization; balanced degree necessity; terminal routing with internal-copy capacity; triangle specialization | No gap found |
| Threshold comparisons | Rational endpoint meaning; certified dual interval coverage; monotonicity up to the square's exact physical endpoint; no inference of equality from matching brackets | Supplied certificates passed |
| Defect construction and fan | Disjoint defect supports; full diagonal products; finite-order pointwise and second-moment inequalities; first rejecting integer | No gap found |
| Distance asymptotics | Finner lower bound; compatible base-bit/flag construction; all eight leading atom deviations; Euclidean redistribution constant | No gap found |
| Bit-length theorem | Fixed semialgebraic description; specialization to integer polynomials; nonzero root separation; dyadic family for lower bound; fixed-scenario order versus runtime | No gap found |
| Supplementary results | Pair-retaining fan; conditioning square to triangle; profile variance; independent-cell bounds; sequential support compression; identity polarization; order-two extraction example | No gap found |

## Fresh verification

All commands below were run during this audit. Evidence is under `paper/review/specialist-audit-evidence/`. The Lean build used the existing pinned dependency cache; this was not a clean rebuild of all dependencies from newly downloaded sources.

| Check | Result |
| --- | --- |
| `lake build` with Lean 4.33.0 | PASS, 3387 jobs reported; the two registry Challenge placeholders produce the documented `sorry` warnings |
| `bash scripts/check_axioms.sh` | PASS, 112 audited declarations; dependencies limited to `propext`, `Classical.choice`, `Quot.sound` |
| Classification certificate verifier | PASS; local classification manifest: all eight listed files match |
| Parity-threshold verifier, full supplied files | PASS, 20,004 exact checks through order ten |
| Replay runner in a temporary artifact copy | PASS, ten replay commands, including hardened defect checks, effective rejection, fan and classification checks |
| Nontermination mutation tests | PASS for the hardened checker; documented failure of frozen assertions under optimization reproduced |
| Fan mutation tests | PASS under their stated contract; deleting an entire record is explicitly treated as a smaller valid certificate, not as full-coverage verification |
| Empty threshold directory negative test | **FAIL of the desired contract:** exit zero and `OK: 0 exact checks passed`; finding A1 |

The top-level artifact manifest's certificate and verifier hashes match the current files. Ten committed replay JSON records differ from that historical manifest. The verification guide already distinguishes the frozen artifact identities from later replay logs. This is not evidence of changed certificate mathematics; separating immutable inputs from mutable execution records would make provenance easier to inspect.

## Literature and significance

The comparison with the foundational inflation work is substantively appropriate. [Navascués and Wolfe](https://arxiv.org/html/1707.06476v3) establish star termination at order two and distinguish finite compatibility testing from finite attainment in polynomial optimization. The manuscript's double-star classification and explicit obstructions address the former question. Its attribution of those starting points should stay prominent.

The passage to bounded latent alphabets has the right external support: [Rosset, Gisin and Wolfe](https://arxiv.org/html/1709.00707) explicitly give six latent values per source for the binary triangle and establish closedness and semialgebraicity. The paper properly identifies this bridge as outside the graph formalization.

[Da Silva, Pozas-Kerstjens and Parisio](https://arxiv.org/html/2503.16654) study symmetric binary-triangle correlations. The manuscript correctly avoids treating its chosen parity family as itself a newly discovered family; its contribution is the hierarchy behavior and associated constructions.

These source checks support the paper's positioning. The limited targeted search did not establish a complete priority history, and several searches returned no useful results. No claim of exhaustive novelty certification follows from that search. In particular, the general convex-order formulation merits attention from someone familiar with both finite exchangeability and inflation.

My assessment is that the main classification is a potentially significant specialist contribution to classical network compatibility. The source-count-independent convergence estimate is the result most likely to be useful outside this particular graph classification. The exponential input-length result concerns the required inflation order and should continue to be distinguished from computational hardness of compatibility itself.

## Organization and writing

The classification-first sequence is sound. The cycle and path constructions earn their length; the defect family supplies a different quantitative phenomenon. I would not request another large reorganization or arbitrary page cut. The appendices appropriately hold the structural details and finite computations. The presentation is now mathematical rather than promotional.

One simple wording correction remains in the opening paragraph: compatible sets **need not be convex**, rather than universally “form a nonconvex set.” A single edge already has the whole observed simplex as its compatible set.

After A1–A5 and that sentence are addressed, this audit supplies no reason to delay a preprint for another editorial cycle. For journal submission, the decisive remaining uncertainty is external specialist scrutiny of correctness and novelty, rather than unresolved spacing, length, or generic writing concerns.
