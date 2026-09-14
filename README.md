# Termination of the classical inflation hierarchy on pair-source networks

Lean 4 formalizations of two theorems of *Inflation for Classical Pair-Source Networks:
Termination and Quantitative Obstructions* (William Blair, manuscript, 2026, included under
[`paper/`](paper/)).

**The classification (paper Theorem 4.2).** For a pair-source scenario with binary
observations, some finite order of the Navascués–Wolfe inflation hierarchy characterizes
compatibility if and only if every connected component of the observed graph is a
double-star, and when it does, order two already suffices.

**The triangle (paper Theorem 8.2).** The triangle is the smallest scenario on the
nonterminating side, and there the failure is quantitative: for every order `t` there is an
explicit rational three-bit law that passes the order-`t` test and violates the Finner
inequality by at least `ε_t²/2`.

Everything here is kernel-proved. `Audit.lean` prints the axioms of the two registry
statements and of every library declaration the Coverage table below names; all 112 depend
on `propext`, `Classical.choice` and `Quot.sound` and nothing else. The repository holds
exactly two unfinished proofs, one in each Challenge file, where Palomar's submission rules
require them.

## Layout

`paper/` holds the manuscript with its release documents, `artifact/` the exact rational certificates with their checkers and replay records (run `python3 -B artifact/verifiers/run_replay.py` and the two `verify_*.py` scripts from this directory), `TriangleInflation/` the Lean development, `Palomar/` and `PalomarSolutions/` the two registry statements.

## The two theorems

```lean
theorem TriangleInflation.Graph.classification_NW (Γ : PairGraph) :
    (∃ t : ℕ, 1 ≤ t ∧ ∀ P : GTarget Γ, IsLaw P → (GNWFeasible Γ t P ↔ GCompatible Γ P))
      ↔ IsDoubleStarForest Γ.G
```

A `PairGraph` is a finite simple graph without isolated vertices: one binary observed
variable per vertex, one independent latent source per edge, shared by the two endpoints of
that edge. `IsDoubleStarForest G` says that `G` is acyclic and that any two reachable
vertices lie at distance at most three, which is to say that every component is a tree of
diameter at most three, a double star.

Left to right this is the nontermination half: if a component is anything else, then at
every order `t ≥ 1` there is a strictly positive law that passes the order-`t` test and has
no model, so no finite order equals the compatible set. Right to left it is the
reconstruction half, and the proof supplies `t = 2`.

The nonterminating side is proved by exhaustion: a connected graph that is not a double star
contains an induced cycle or an induced five-observer path (`exhaustion`). On a cycle
`C_m` the witness is the parity target `P_{m,q}` at `q = 1/(4m²t²)`, whose characters have
moments `(−q)^{|∂F|/2}`; it passes the order-`t` test (`cycle_witness`) and sits at distance
at least `q/10` from the compatible set (`cycle_distance`), through an exact and then a
quantitative form of parity rigidity. On the five-observer path the witness is the bilocal
target at `h = 1/(16t²)` (`fivePath_witness`, `fivePath_distance`). Either witness is carried
to the ambient graph by induced-subgraph transport (`induced_transport`) and made strictly
positive by independent local flips, which preserve symmetry and every ancestral-independence
product (`flip_gExpFeasible`).

The terminating side reconstructs a model. On a double star the order-two inflation
determines a labelling of the two centres and their leaves, and the labelling assembles into
a `GModel` (`exists_dsStruct`, `DSStruct.gCompatible_of_dsStruct`, `doubleStar_terminates`).

The same file proves the classification for the ancestral-independence hierarchy
(`classification_AI`) and for the recursively expressible hierarchy (`classification_exp`);
the root-sink lemma proves that the latter two coincide on every pair-source scenario
(`gExpFeasible_iff_gAIFeasible`).

```lean
theorem TriangleInflation.no_finite_characterizing_order (t : ℕ) (ht : 1 ≤ t) :
    ∃ P : ThreeBit → ℝ, IsLaw P ∧ AIFeasible t P ∧ NWFeasible t P ∧ ¬ TriangleCompatible P
```

For every order `t ≥ 1` there is a three-bit law `P` which is a probability law (`IsLaw P`),
which is feasible at order `t` for the ancestral-independence hierarchy `I^AI_t`
(`AIFeasible t P`) and hence for the Navascués–Wolfe hierarchy `I^NW_t` (`NWFeasible t P`),
and which is not triangle compatible (`¬ TriangleCompatible P`).

Navascués and Wolfe (2020, §4.1) ask whether some finite order settles exact compatibility.
Their hierarchy is asymptotically complete, so every incompatible law is rejected at *some*
finite order; the theorem says that order cannot be bounded uniformly.

The witnesses are the explicit rational family

```
P_t = Q(ε_t, r_t),   ε_t = 1/(2t³),   r_t = (1 − ε_t)^(t−1),
Q(ε, r) = ε·δ_000 + (1 − ε)·Bern(r)^⊗3.
```

Membership is proved by an explicit inflation law on the order-`t` copied observations
(paper Section 8.1): independent `Bern(ε)` defect bits on the cube `[t]³` of source-copy
indices together with independent `Bern(s)` private bits, with a copied observation
outputting `1` exactly when its private bit and every defect on its line are `0`. That law
is `S_t³`-symmetric, has the tensor power `P^⊗t` as its diagonal law, and satisfies the
injectable-marginal and ancestral-independence prescriptions. Incompatibility is the Finner
inequality `P(000)² ≤ P_A(0)·P_B(0)·P_C(0)` (paper Section 8.2), which `P_t` violates by at
least `ε_t²/2 > 0`.

## Formalization boundaries

Three, all scope restrictions of the theorems as stated. They are recorded in the headers of
`TriangleInflation/Defs.lean` and `TriangleInflation/Graph/Defs.lean`, restated in the two
Challenge files, and in `formalization.yaml` under `fidelity.divergences`.

1. **Binary observed variables.** The classification is proved for `Bool` outcomes. The
   manuscript's Remark 4.4 extends it to any fixed finite observed alphabets; that transfer
   is **not** formalized.
2. **Finite latent alphabets.** `GCompatible` quantifies over a `GModel` whose latent
   alphabets are `Fintype`s, and `TriangleCompatible` over a `TriangleModel` with three
   finite latent spaces, where the paper allows arbitrary measurable latent spaces. The
   reduction to bounded finite alphabets (Rosset, Gisin and Wolfe, 2018) is quoted in the
   paper and is not formalized, so the formal compatible set is a priori a subset of the
   paper's and "not compatible" is the weaker of the two readings. One exception: for the
   triangle the arbitrary-latent form is proved directly in
   `TriangleInflation/FinnerMeasure.lean` (`TriangleCompatibleM`, `finner_of_compatibleM`,
   `no_finite_characterizing_orderM`). The registry statement is deliberately the elementary
   finite-latent one.
3. **Laws are bare real weight functions** on finite types with the predicate `IsLaw`, not
   Mathlib `Measure`s or `PMF`s, except in `FinnerMeasure.lean`; all other inequalities are
   real-valued. The first rejecting order `t_min` is `Nat.sInf` of the set of rejecting
   orders, which returns `0` when that set is empty, so every statement about it either
   exhibits a rejecting order or assumes one. Asymptotic completeness itself is quoted from
   Navascués–Wolfe, not formalized.

The recursively expressible hierarchy `I^exp_t`, which the previous version of this
repository left out, **is** formalized on the graph side: `dsep` is the trail criterion for
the depth-one inflation DAG, `Expressible` is the Wolfe–Spekkens–Fritz closure, and
`gExpFeasible_iff_gAIFeasible` proves `I^exp_t = I^AI_t`. The triangle module still omits it,
so the statements there about membership are the weaker halves; the bridge theorems
(`gNWFeasible_triangle_iff` and its companions) supply the stronger ones.

Paper results with no Lean statement here: the square witness of Theorem 6.11, the
larger-alphabet transfer of Remark 4.4, Lemma 6.13, Corollaries 6.14 and 6.15, Theorem 6.18,
Proposition 6.20 and its lemmas, Appendix C, the distance asymptotics of Theorem 11.1 and
Corollary 11.2, the `2^{Θ(B)}` bit-length law of Proposition 13.1, the limit form of
Proposition 10.1, and Corollary 8.3.

## Layout

```
TriangleInflation/          the triangle library
  Defs.lean                 definitions and the representational decisions
  Finner.lean               the Finner inequality for finite-latent triangle models
  FinnerMeasure.lean        the same for arbitrary measurable latent spaces
  Defect.lean               independence from disjoint root supports
  DefectLaw.lean            the defect-cube law: symmetry, diagonal and injectable marginals
  Main.lean                 Theorem 8.1, Theorem 8.2 and the nontermination corollary
  Fan.lean                  the order-t fan inequalities; the family R_p
  Exponent.lean             the Θ(ε^{-1/3}) bounds along P_ε
  Rate.lean                 the order-t second-moment rate bound
  ConvexOrder.lean          the convex-order sharpening and the bound √7/(2√t)
  Graph.lean                aggregator for the pair-source development
  Graph/                    the pair-source library, 17 modules
    Defs.lean               scenarios, copied observations, the three tests, compatibility
    Flips.lean              independent local flips
    Soundness.lean          soundness of the three tests
    RootSink.lean           the trail criterion and I^exp_t = I^AI_t
    Triangle.lean           the bridge to the triangle module
    DoubleStar.lean         order-two structure on a double star
    DoubleStarForest.lean   the reconstruction: doubleStar_terminates
    FivePath.lean           the five-path target and the bilocal inequality
    FivePathWitness.lean    the five-path witness at every order
    Cycles.lean             the cycle target and its characters
    CycleWitness.lean       the cycle witness at every order
    CycleObstruction.lean   parity rigidity, incompatibility and the distance bound
    Linear.lean             the linear machinery shared by the witnesses
    TriangleWitness.lean    the triangle witness at q = 1/(16t)
    Transport.lean          induced-subgraph transport and the exhaustion lemma
    Classification.lean     components, bad components, the pieces of Theorem 4.2
    ClassificationTheorem.lean  classification_NW_lib, _AI, _exp
TriangleInflation.lean      root aggregator
Palomar/TriangleInflation/
  ClassificationChallenge.lean  registry statement 1: Mathlib only, proof left open
  classification-comparator.json
  Challenge.lean                registry statement 2: Mathlib only, proof left open
  comparator.json
PalomarSolutions/
  TriangleInflationClassification.lean  Solution 1: same declaration, proved from the library
  TriangleInflation.lean                Solution 2
Audit.lean                  #print axioms for both registry statements and 110 library results
scripts/gen_challenge.py    generates both Challenges from the library definitions files
scripts/check_axioms.sh     the verification gate
formalization.yaml          provenance, sources, automation, review (the
                            mathlib-initiative self-reporting standard; Palomar reads it)
PORTING.md                  every difference from the author's working repository
SUBMISSION.md              what remains to be done by hand to register these statements
paper/                      main.pdf and its LaTeX sources; release/ holds the claim,
                            non-claim, priority, reproduction and release documents
```

## The two registry statements

`Palomar/TriangleInflation/` holds two Comparator comparisons, each in the shape the Palomar
submission standard asks for: a Challenge importing only Mathlib and stating the result as a
single declaration whose proof is left open, and a `*comparator.json` permitting only the
three standard axioms. The matching Solution declares the same name and proves it from the
library.

| | classification | triangle |
|---|---|---|
| Challenge | `Palomar/TriangleInflation/ClassificationChallenge.lean` | `Palomar/TriangleInflation/Challenge.lean` |
| Solution | `PalomarSolutions/TriangleInflationClassification.lean` | `PalomarSolutions/TriangleInflation.lean` |
| config | `Palomar/TriangleInflation/classification-comparator.json` | `Palomar/TriangleInflation/comparator.json` |
| declaration | `TriangleInflation.Graph.classification_NW` | `TriangleInflation.no_finite_characterizing_order` |
| library proof | `classification_NW_lib` | `no_finite_characterizing_order_lib` |
| paper | Theorem 4.2 | Theorem 8.2 and its corollary |

Comparator compares the two statements constant by constant, so every constant in the
statement has to be identical, by name and by definition body, in the two import closures. A
Challenge may not import the project, so it carries the constants it needs itself.
`scripts/gen_challenge.py` writes both files mechanically: the triangle Challenge is the
Mathlib imports of `TriangleInflation/Defs.lean`, a Challenge-specific header, the body of
that file verbatim, and the theorem; the classification Challenge is the same body followed
by the declarations of `TriangleInflation/Graph/Defs.lean` that its statement needs
(`PairGraph`, `GObs`, `GAssign`, `GSymmetric`, `readDiag`, `gTensorPow`, `GNWFeasible`,
`GModel`, `GCompatible`, `IsDoubleStarForest` and their dependencies), each copied verbatim
and in file order. A selector that matches no declaration, or more than one, fails the
generator, so a rename in the library is caught rather than silently dropped.
`scripts/check_axioms.sh` runs the generator in `--check` mode and fails if either committed
file has drifted.

Challenge and Solution declare the same name, so each library theorem carries the suffix
`_lib` and the Solution discharges the registry name by applying it. The Solutions sit under
their own root module rather than under `Palomar`: the registry's verifier puts its
recompiled Challenge first on `LEAN_PATH` and Lean resolves every module sharing that root
directory there, so a Solution under `Palomar.*` is never found (PalomarSubmission#108).

To reproduce the registry's mechanical check locally you need
[Comparator](https://github.com/leanprover/comparator) and a `lean4export` built at this
repository's Lean version on `PATH` (on macOS, Comparator's `scripts/fake-landrun.sh` stands
in for the Linux sandbox and is not adversarial):

```bash
lake build
lake env comparator Palomar/TriangleInflation/classification-comparator.json
lake env comparator Palomar/TriangleInflation/comparator.json
```

Both runs were performed on 2026-09-14 and both passed:

```
Running Lean default kernel on solution.
Lean default kernel accepts the solution
Your solution is okay!
```

Two notes on that run. `lean4export` has to be built at *this* repository's Lean version: a
build at `v4.33.1` refuses the `v4.33.0` oleans with `incompatible header`. And it was a
macOS run, so `scripts/fake-landrun.sh` stood in for `landrun`; it execs the command
unsandboxed, which means the comparison was checked and the isolation was not. Palomar runs
the same comparison on its own infrastructure, with the real sandbox, which is the point of
registering.

Registration is a deliberate, separate act: nothing in this repository submits anything.
`SUBMISSION.md` lists what is left to do by hand.

## Verify locally

```bash
lake exe cache get     # or bring your own prebuilt Mathlib at the pinned rev
lake build
bash scripts/check_axioms.sh
```

The gate refuses a literal `sorry` or `admit` anywhere under `TriangleInflation/` or
`PalomarSolutions/`, requires each Challenge to carry exactly one, regenerates both
Challenges from `TriangleInflation/Defs.lean` and `TriangleInflation/Graph/Defs.lean` and
fails if a committed file differs, and fails on any axiom outside
`[propext, Classical.choice, Quot.sound]`.

A full build from a warm Mathlib cache takes a few minutes.
`TriangleInflation/Graph/FivePathWitness.lean` is the slow module, about 135 s for one
32-point computation, and carries `set_option maxHeartbeats 4000000` for it.

Lean `v4.33.0`; Mathlib pinned at `db584cd6d46c92f209a44c0f1c829460d327499d`, a commit on
canonical `master`. Mathlib is the only dependency.

## Coverage

Statuses are against the manuscript. *Proved* means the paper statement is formalized as
stated, up to the three boundaries above. *Partial* means a proper part of it is, and the
Lean column names which part. *Unformalized* means there is no Lean statement at all.

### Pair-source scenarios (paper Sections 3 to 7)

| Paper | Statement | Status | Lean |
|---|---|---|---|
| Def. 3.1 to 3.5 | pair-source scenarios, the inflation, `I^NW_t`, `I^AI_t`, `I^exp_t` | proved | `gNWFeasible_of_gAIFeasible`, `gAIFeasible_of_gExpFeasible`, `gNWFeasible_triangle_iff`, `gAIFeasible_triangle_iff`, `gCompatible_triangle_iff` |
| Prop. 3.6 | soundness of the three tests | proved | `compatible_gNWFeasible`, `compatible_gAIFeasible`, `compatible_gExpFeasible` |
| Lem. 3.7, 3.9 | the trail criterion and the root-sink lemma, `I^exp_t = I^AI_t` | proved | `gExpFeasible_iff_gAIFeasible`, `isAISet_iff_decomposition`, `isAISet_glue`, `RootSinkAux.exists_activeTrail` |
| Lem. 3.10 | source-disjoint independence | partial (order two) | `blockMarg_union_of_sourceDisjoint`, `blockMarg_biUnion_of_sourceDisjoint`, `gTwist_law` |
| Lem. 3.11 | induced-subgraph transport | proved | `induced_transport`, `transport_ai_feasible`, `transport_compatible_restrict` |
| **Thm. 4.2** | **the termination classification** | **proved** | **`classification_NW`**, `classification_AI`, `classification_exp`, `nontermination_of_not_doubleStar` |
| Lem. 4.3 | exhaustion into an induced cycle or five-path | proved | `exhaustion`, `flip_full_support`, `flip_gExpFeasible` |
| Rem. 4.4 | transfer to larger fixed observed alphabets | unformalized | none |
| Thm. 5.1, Cor. 5.2 | double-star reconstruction at order two | proved (binary case) | `doubleStar_terminates`, `exists_dsStruct`, `DSStruct.gCompatible_of_dsStruct`, `centreLeaf_mass`, `gCompatible_of_localDecoder` |
| Lem. 6.1 to 6.5 | the cycle target, its characters, exact parity rigidity | partial | `cycleTarget_isLaw`, `cycleTarget_moment`, `parity_rigidity` |
| Lem. 6.6 to 6.7, Thm. 6.8 | quantitative rigidity, the cycle witness and its distance | proved | `CycleModelAux.quant_rigidity`, `cycle_witness`, `cycle_exp_witness`, `cycle_not_compatible`, `cycle_distance` |
| Lem. 6.10 | the corrected Fourier density | partial (`m = 3`) | `triW_ge`, `triW_nonneg`, `triW_moment`, `triDensity_isLaw`, `triParity_isLaw` |
| Thm. 6.11 | the square witness at `q = 1/(16t)` | unformalized | none |
| Thm. 6.12 | the triangle witness at `q = 1/(16t)` | proved | `triangle_linear_witness` |
| Lem. 6.13, Cor. 6.14 to 6.15 | order bounds from the parity violation | unformalized | none |
| Thm. 6.16, Cor. 6.17 | the convex-order bound and the brackets | partial (upper bounds, triangle) | `rate_triangle_sharp`, `tv_le_of_nwFeasible`, `tv_le_sqrt_seven`, `tvDist` |
| Thm. 6.18, Prop. 6.20 | order conversion on the square; the low-order separations | unformalized | none |
| Lem. 7.2 to 7.3, Cor. 7.4, Thm. 7.5 | the five-path target, the bilocal inequality, the witness | proved | `fivePathTarget_isLaw`, `fivePathTarget_corr`, `bilocal_of_compatible`, `fivePath_not_compatible`, `fivePath_distance`, `fivePath_witness`, `fivePath_exp_witness` |

### The triangle (paper Sections 2 and 8 to 13)

| Paper | Statement | Status | Lean |
|---|---|---|---|
| Def. 2.1, 2.2 | `I^NW_t`, injectable sets, ancestral independence, `I^AI_t` | proved | `nwFeasible_of_aiFeasible`, `injectable_iff_injectableRaw` |
| Def. 2.3 | the recursively expressible set `I^exp_t` | proved on the graph side | `Expressible`, `gExpFeasible_iff_gAIFeasible` |
| §2.1 | the compatible set `C_△` | proved (both latent conventions) | `TriangleCompatible`, `TriangleCompatibleM`, `triangleCompatibleM_of_triangleCompatible` |
| Lem. 8.4 | disjoint-ancestry independence | proved | `defect_independence`, `defect_independence_family`, `rootSupport_disjoint` |
| Lem. 8.5 | the copied-triangle law and the parameter `s` | proved | `defect_copiedTriangle_law`, `sParam_mem_Icc` |
| Lem. 8.6 | `S_t³` symmetry of the defect-cube law | proved | `defect_symmetric` |
| Lem. 8.7 | the Finner inequality | proved (arbitrary latent spaces) | `finner_of_compatible`, `finner_of_compatibleM` |
| Lem. 8.8 | the explicit violation | proved | `witness_violation`, `witness_margin`, `witness_not_compatible`, `witness_not_compatibleM` |
| Lem. 8.9 | mutual disjointness of the diagonal supports `R_l` | proved | `diagRegion_disjoint`, `defect_diagonal_law` |
| Thm. 8.1 | membership `Q(ε,r) ∈ I^AI_t ⊆ I^NW_t` | proved | `membership_AI`, `membership_NW`, `defectLaw_witnesses_AI` |
| **Thm. 8.2 + cor.** | **no finite characterizing order** | **proved** | **`no_finite_characterizing_order`**, `no_finite_characterizing_orderM` |
| Cor. 8.3 | the rational bit-length form | unformalized | none |
| App. A | injectable sets are the subsets of copied triangles | proved | `injectable_iff_injectableRaw` |
| Thm. 9.1 | the order-`t` fan inequalities and the rejecting-order corollary | partial | `fan_first`, `fan_second`, `tminNW_le_of_finner_violation` |
| Prop. 9.2 | `R_p` has rejecting order 2 at every distance | partial | `Rlaw_tminNW`, `Rlaw_tminAI`, `Rlaw_not_compatibleM` |
| Prop. 10.1 | `t_min(P_ε) = Θ(ε^{-1/3})` | partial (finite parts) | `Peps_tminNW_bounds`, `Peps_tminAI_bounds`, `Peps_not_compatibleM` |
| Thm. 11.1, Cor. 11.2 | distance asymptotics | unformalized | none |
| Prop. 12.1 | the distance-promised order bound | partial (triangle) | `rate_triangle` |
| Prop. 13.1 | the `2^{Θ(B)}` bit-length law | unformalized | none |
| App. C | the certificate formats and the supporting families | unformalized | none |

Declarations without a namespace prefix are in `TriangleInflation` for the second table and
in `TriangleInflation.Graph` for the first.

## Status of the manuscript

The manuscript is not yet posted to arXiv. This registry entry is meant to precede it and to
be cited by it. `paper/release/PRIORITY_AUDIT.md` records `PRIORITY_NOT_KILLED`, with
Navascués–Wolfe 2020 §4.1 as the strongest located predecessor, and does not certify
firstness; its addendum of 2026-09-14 covers the pair-source sections and located no
predecessor for the classification beyond stars, for `I^exp = I^AI`, for the all-order
witnesses or for the `Θ(1/t)` bounds. `paper/release/NONCLAIMS.md` records exactly what is
and is not formalized, and its scope agrees with the Coverage tables above. No independent
human review of the mathematics has been performed.

A green build here is a scoped, re-checkable build and axiom result. It is not scientific
acceptance.

## Licence

MIT; see [`LICENSE`](LICENSE). The manuscript under `paper/` is by the same author and is
covered by the same licence.
