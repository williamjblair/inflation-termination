# Inflation for classical pair-source networks

This repository accompanies the manuscript *Inflation for Classical Pair-Source Networks:
Termination and Quantitative Obstructions* (William Blair, 2026). It contains the paper, the
exact rational certificates behind its finite computations, and a Lean 4 formalization of its
main theorems.

- **Paper:** [`paper/main.pdf`](paper/main.pdf) (52 pages) with LaTeX sources under
  [`paper/`](paper/). Not yet posted to arXiv.
- **Lean:** 113 audited declarations, each depending only on `propext`,
  `Classical.choice` and `Quot.sound`. Lean `v4.33.0`, Mathlib
  `db584cd6d46c92f209a44c0f1c829460d327499d`.
- **Palomar:** the classification theorem is registered as
  [`PALOMAR-2026-09-14-000009`](https://palomar-registry.org/entry.html?id=PALOMAR-2026-09-14-000009&version=2),
  version 2, from commit `898300eb`. Version 1, from commit `93cc53f1`, registers the same
  Lean statement.

## Results

The inflation hierarchy of Navascués and Wolfe is asymptotically complete: every incompatible
law is rejected at some finite order. They asked whether, for a fixed scenario, one finite
order decides compatibility. The paper answers the question for pair-source scenarios, where
every latent source is shared by exactly two observers and the scenario is a finite simple
graph.

**Classification (Theorem 3.2).** With binary observations, some finite order characterizes
compatibility if and only if every connected component of the graph is a tree of diameter at
most three, a double-star. In that case order two suffices. Otherwise, at every order `t`
there is a strictly positive rational law that passes the order-`t` test and is incompatible.
The statement holds for the Navascués–Wolfe test and its ancestral-independence and
recursively expressible strengthenings, and the last two coincide on pair-source scenarios.

**Quantitative convergence (Section 4).** On the square and the triangle, the largest
total-variation distance from compatibility among laws accepted at order `t` lies between
`c/t` and `C/√t`, with `c = 1/47` on the square and `1/43` on the triangle (Corollary 4.9).
The upper bound `√(K−1)/(2√t)` holds in any scenario with `K` joint outcomes
(Theorem 4.8). Exact certificates bracket the parity thresholds of the two tests through
order ten (Proposition 4.11).

**The triangle family (Section 5).** For every `t ≥ 1` the explicit law

```
P_t = ε_t·δ_000 + (1 − ε_t)·Bern(r_t)^⊗3,   ε_t = 1/(2t³),   r_t = (1 − ε_t)^(t−1)
```

passes the order-`t` test and violates the Finner inequality by at least `ε_t²/2`
(Theorem 5.2). Along the family `P_ε` the first rejecting order is `Θ(ε^{-1/3})`
(Proposition 5.13), and over rational inputs of `B` bits the worst required order is
`2^{Θ(B)}` (Proposition 6.2).

Scenarios in which a source is shared by three or more observers are treated in a companion
paper in preparation.

## Contents

This is the current standalone owner of the pair-source manuscript and its
verification package. The broader
[resource-theory programme](https://github.com/williamjblair/resource-theory)
retains its mathematical ledger and earlier source editions; those snapshots
do not supersede this paper's current release instructions. Programme direction
and cross-repository ownership are documented in the
[science-factory vision](https://github.com/williamjblair/autonomous-science/blob/master/VISION.md)
and [repository map](https://github.com/williamjblair/autonomous-science/blob/master/docs/REPOSITORY_MAP.md).
These links do not change theorem scope, publication status or priority.

```
paper/                      manuscript sources and PDF
  release/                  arXiv package, claims, non-claims, priority audit, release status
  review/                   editorial and referee-style audits, verification guide
artifact/                   exact rational certificates, checkers, replay records, manifest
TriangleInflation/          the Lean library
  Defs.lean                 triangle definitions and modelling decisions
  Finner.lean               the Finner inequality, finite latent alphabets
  FinnerMeasure.lean        the Finner inequality, arbitrary latent spaces
  Defect.lean, DefectLaw.lean   the defect-cube law of Theorem 5.1
  Main.lean                 Theorems 5.1 and 5.2
  Fan.lean, Exponent.lean   the fan inequalities, R_p, finite bounds along P_ε
  Rate.lean, ConvexOrder.lean   the order-t rate and the convex-order bound
  Graph/                    the pair-source development (18 modules): definitions, soundness,
                            root-sink lemma, transport, exhaustion, double-star
                            reconstruction, cycle and five-path witnesses, corrected
                            densities, the classification theorem
Palomar/, PalomarSolutions/ the two registry statements and their proofs
Audit.lean                  prints the axioms of every audited declaration
scripts/                    check_axioms.sh (the gate) and gen_challenge.py
formalization.yaml          provenance and scope in the mathlib-initiative format
PORTING.md                  differences from the author's working repository
SUBMISSION.md               the Palomar registration procedure and its record
```

## Reproduce

**Lean.**

```bash
lake exe cache get
lake build
bash scripts/check_axioms.sh
```

The gate fails on any `sorry` or `admit` outside the two Challenge files, on a Challenge that
has drifted from the library definitions, and on any axiom outside `propext`,
`Classical.choice` and `Quot.sound`. A build from a warm Mathlib cache takes a few minutes;
`Graph/FivePathWitness.lean` is the slow module, about two minutes for one 32-point
computation.

**Certificates.** From the repository root with Python 3 (the replay runner also uses `mpmath`):

```bash
python3 -B artifact/verifiers/run_replay.py
python3 -B artifact/verifiers/mutation_tests.py
python3 -B artifact/verifiers/mutation_tests_fan.py
python3 -B artifact/certificates/classification/verify_classification.py
python3 -B artifact/certificates/exponent/verify_exponent.py
python3 -B artifact/verifiers/mutation_tests_exponent.py
python3 -B artifact/certificates/exponent/odd/verify_odd.py
python3 -B artifact/certificates/beyond-finner/verify_beyond_finner.py
```

The checkers use exact integer and rational arithmetic.
`run_replay.py` rewrites the logs under `artifact/replay_logs/`; restore them with
`git checkout artifact/replay_logs` to return to the committed snapshot. Expected outputs and
running times are in [`paper/review/VERIFICATION_GUIDE.md`](paper/review/VERIFICATION_GUIDE.md).
`artifact/certificates/hypergraph/` belongs to the companion paper.

**Paper.**

```bash
bash paper/release/build_arxiv.sh
```

This builds the flattened arXiv package under `paper/release/arxiv-src/` and the upload
archive `paper/release/arxiv-src.tar.gz`.

## Registry statements

Each statement is a Palomar Comparator comparison: a Challenge that imports only Mathlib and
states the theorem with its proof left open, a Solution that declares the same name and
proves it from the library, and a configuration permitting only the three standard axioms.

| | classification | triangle |
|---|---|---|
| declaration | `TriangleInflation.Graph.classification_NW` | `TriangleInflation.no_finite_characterizing_order` |
| Challenge | `Palomar/TriangleInflation/ClassificationChallenge.lean` | `Palomar/TriangleInflation/Challenge.lean` |
| Solution | `PalomarSolutions/TriangleInflationClassification.lean` | `PalomarSolutions/TriangleInflation.lean` |
| configuration | `Palomar/TriangleInflation/classification-comparator.json` | `Palomar/TriangleInflation/comparator.json` |
| library proof | `classification_NW_lib` | `no_finite_characterizing_order_lib` |
| paper | Theorem 3.2 | Theorem 5.2 |
| Palomar | registered (version 2) | not registered |

```lean
theorem TriangleInflation.Graph.classification_NW (Γ : PairGraph) :
    ((∃ t : ℕ, 1 ≤ t ∧ ∀ P : GTarget Γ, IsLaw P → (GNWFeasible Γ t P ↔ GCompatible Γ P))
      ↔ IsDoubleStarForest Γ.G) ∧
    (IsDoubleStarForest Γ.G →
      ∀ P : GTarget Γ, IsLaw P → (GNWFeasible Γ 2 P ↔ GCompatible Γ P))

theorem TriangleInflation.no_finite_characterizing_order (t : ℕ) (ht : 1 ≤ t) :
    ∃ P : ThreeBit → ℝ, IsLaw P ∧ AIFeasible t P ∧ NWFeasible t P ∧ ¬ TriangleCompatible P
```

A `PairGraph` is a finite simple graph without isolated vertices, with one binary observation
per vertex and one independent source per edge. `IsDoubleStarForest G` says that `G` is
acyclic and that reachable vertices are at distance at most three.

A Challenge may not import the project, so it carries the definitions its statement uses.
`scripts/gen_challenge.py` copies them verbatim from `TriangleInflation/Defs.lean` and
`TriangleInflation/Graph/Defs.lean`, and the gate fails if a committed Challenge differs from
the regenerated one. The Solutions live under their own root module because Palomar's
verifier resolves every module under the Challenge's root directory in the recompiled
Challenge (PalomarSubmission#108).

Both comparisons pass locally with Comparator and `lean4export` built at Lean `v4.33.0`. On
macOS, Comparator's `scripts/fake-landrun.sh` replaces the Linux sandbox, so a local run
checks the comparison and not the isolation; Palomar runs both on its own infrastructure.

## What is formalized

The formal statements use three conventions, recorded in the headers of the two `Defs.lean`
files and in `formalization.yaml`.

1. **Binary observations.** The transfer to larger observed alphabets (Remark 3.8,
   Corollary 5.3) is not formalized.
2. **Finite latent alphabets.** `GCompatible` and `TriangleCompatible` quantify over models
   with finite latent spaces, where the paper allows arbitrary measurable ones. The formal
   compatible sets are therefore a priori smaller, and "not compatible" is the weaker
   reading. For the triangle, the arbitrary-latent form is also proved
   (`TriangleCompatibleM`, `no_finite_characterizing_orderM`).
3. **Laws are real weight functions** on finite types with the predicate `IsLaw`, except in
   `FinnerMeasure.lean`.

The recursively expressible test is formalized on the graph side, and
`gExpFeasible_iff_gAIFeasible` proves that it coincides with the ancestral-independence test.
The rationality of the classification witnesses is proved in the paper, not in Lean. The
square and triangle witnesses are proved at `q = 1/(16t)`; the wider ranges of Theorems 4.3
and 4.4 are proved in the paper only.

**Coverage.** *Proved* means formalized as stated, under the conventions above; *partial*
means a named part is; *not formalized* means no Lean statement exists. Declarations are in
`TriangleInflation.Graph` in the first table and in `TriangleInflation` in the second.

Pair-source scenarios (Sections 2 to 4, Appendices A and B):

| Paper | Statement | Status | Lean |
|---|---|---|---|
| Def. 2.1–2.5 | scenarios, inflation, the three tests | proved | `gNWFeasible_of_gAIFeasible`, `gAIFeasible_of_gExpFeasible`, `gNWFeasible_triangle_iff`, `gAIFeasible_triangle_iff`, `gCompatible_triangle_iff` |
| Prop. 2.6 | soundness of the three tests | proved | `compatible_gNWFeasible`, `compatible_gAIFeasible`, `compatible_gExpFeasible` |
| **Thm. 3.2** | **classification** | **proved** (binary, finite latent; rationality in the paper) | **`classification_NW`**, `classification_AI`, `classification_exp`, `nontermination_of_not_doubleStar` |
| Lem. 3.4, A.1 | root-sink lemma, trail criterion | proved | `gExpFeasible_iff_gAIFeasible`, `isAISet_iff_decomposition`, `isAISet_glue`, `RootSinkAux.exists_activeTrail` |
| Lem. 3.5 | source-disjoint independence | partial (order two) | `blockMarg_union_of_sourceDisjoint`, `blockMarg_biUnion_of_sourceDisjoint`, `gTwist_law` |
| Lem. 3.6 | induced-subgraph transport | proved | `induced_transport`, `transport_ai_feasible`, `transport_compatible_restrict` |
| Lem. 3.7 | exhaustion | proved | `exhaustion`, `flip_full_support`, `flip_gExpFeasible` |
| Rem. 3.8 | larger observed alphabets | not formalized | |
| Thm. 3.10, Cor. 3.11 | double-star reconstruction at order two | proved (binary) | `doubleStar_terminates`, `exists_dsStruct`, `DSStruct.gCompatible_of_dsStruct`, `centreLeaf_mass`, `gCompatible_of_localDecoder` |
| Lem. 3.14–3.18 | cycle target, characters, exact parity rigidity | partial | `cycleTarget_isLaw`, `cycleTarget_moment`, `parity_rigidity` |
| Lem. 3.19–3.20, Thm. 3.21 | quantitative rigidity, cycle witness and distance | proved | `CycleModelAux.quant_rigidity`, `cycle_witness`, `cycle_exp_witness`, `cycle_not_compatible`, `cycle_distance` |
| Lem. 3.23–3.24, Cor. 3.25, Thm. 3.26 | five-path target, bilocal inequality, witness | proved | `fivePathTarget_isLaw`, `fivePathTarget_corr`, `bilocal_of_compatible`, `fivePath_not_compatible`, `fivePath_distance`, `fivePath_witness`, `fivePath_exp_witness` |
| Lem. 4.2 | corrected Fourier density | partial (`c = 4` and `c = 5` at `tq ≤ 1/16`) | `triW_ge`, `triW_nonneg`, `triW_moment`, `triDensity_isLaw`, `triParity_isLaw` |
| Thm. 4.3 | square witness | partial (`q = 1/(16t)`) | `square_linear_witness` |
| Thm. 4.4 | triangle witness | partial (`q = 1/(16t)`) | `triangle_linear_witness` |
| Lem. 4.5, Cor. 4.6–4.7 | max-moment inequality, survivor bounds | not formalized | |
| Thm. 4.8, Cor. 4.9 | convex-order bound, brackets | partial (triangle upper bound) | `rate_triangle_sharp`, `tv_le_of_nwFeasible`, `tv_le_sqrt_seven`, `tvDist` |
| Thm. 4.10, Props. 4.11–4.12, App. B | order conversion, certified thresholds | not formalized | |

The triangle family (Sections 5 and 6, Appendices C and D):

| Paper | Statement | Status | Lean |
|---|---|---|---|
| Thm. 5.1 | the defect law is accepted by the AI and NW tests | proved | `membership_AI`, `membership_NW`, `defectLaw_witnesses_AI` |
| **Thm. 5.2** | **no finite characterizing order** | **proved** | **`no_finite_characterizing_order`**, `no_finite_characterizing_orderM` |
| Cor. 5.3 | larger observed alphabets | not formalized | |
| Lem. 5.4 | disjoint-ancestry independence | proved | `defect_independence`, `defect_independence_family`, `rootSupport_disjoint` |
| Lem. 5.5 | copied-triangle law | proved | `defect_copiedTriangle_law`, `sParam_mem_Icc` |
| Lem. 5.6 | symmetry of the defect law | proved | `defect_symmetric` |
| Lem. 5.7 | Finner inequality | proved (both latent conventions) | `finner_of_compatible`, `finner_of_compatibleM` |
| Lem. 5.8 | the explicit violation | proved | `witness_violation`, `witness_margin`, `witness_not_compatible`, `witness_not_compatibleM` |
| Lem. 5.9 | diagonal law | proved | `diagRegion_disjoint`, `defect_diagonal_law` |
| Lem. 5.10 | expressible prescriptions of the defect law | not formalized in the triangle module | |
| App. A.3 | injectable sets of the triangle | proved | `injectable_iff_injectableRaw`, `nwFeasible_of_aiFeasible` |
| Thm. 5.11 | fan inequalities and rejecting order | partial | `fan_first`, `fan_second`, `tminNW_le_of_finner_violation` |
| Prop. 5.12 | `R_p` rejected at order two | partial | `Rlaw_tminNW`, `Rlaw_tminAI`, `Rlaw_not_compatibleM` |
| Prop. 5.13 | `t_min(P_ε) = Θ(ε^{-1/3})` | partial (finite bounds) | `Peps_tminNW_bounds`, `Peps_tminAI_bounds`, `Peps_not_compatibleM` |
| Thm. 5.14, Cor. 5.15 | distance asymptotics | not formalized | |
| Cor. 6.1 | distance-promised rejecting order | partial (triangle) | `rate_triangle` |
| Prop. 6.2 | `2^{Θ(B)}` bit-length law | not formalized | |
| Rem. 6.3 | cubic parity certificates | not formalized | |
| App. C, D | certificate formats, supplementary inequalities | not formalized | |

## Status and review

The proofs in the paper are complete and analytic; the certificates check finite instances
and the proofs do not depend on them. The manuscript has been through AI-assisted editorial
and referee-style audits (`paper/review/`) and targeted priority sweeps
(`paper/release/PRIORITY_AUDIT.md`), which found no predecessor for the classification beyond
star scenarios, for the `Ω(1/t)` lower bounds or for the source-free constant of the
convex-order bound. These are not independent human review, and
firstness is not certified. `paper/release/NONCLAIMS.md` lists what the paper does not
claim.

## Licence

MIT; see [`LICENSE`](LICENSE). The manuscript under `paper/` is covered by the same licence.
