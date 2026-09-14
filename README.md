# Nontermination of the classical inflation hierarchy for the triangle

A Lean 4 formalization of the headline theorem of *Inflation for the Classical Triangle:
Nontermination and Quantitative Complexity* (William Blair, manuscript, 2026, included
under [`paper/`](paper/)): **no finite order of the classical inflation hierarchy
characterizes compatibility in the binary triangle causal scenario.**

Everything here is kernel-proved. `Audit.lean` prints the axioms of the registry statement
and of every library theorem the manuscript's coverage table names; all of them depend on
`propext`, `Classical.choice` and `Quot.sound` and nothing else. There is exactly one
`sorry` in the repository, in `Palomar/TriangleInflation/Challenge.lean`, where Palomar's
submission rules require it.

## The theorem

```lean
theorem no_finite_characterizing_order (t : ℕ) (ht : 1 ≤ t) :
    ∃ P : ThreeBit → ℝ, IsLaw P ∧ AIFeasible t P ∧ NWFeasible t P ∧ ¬ TriangleCompatible P
```

For every order `t ≥ 1` there is a three-bit law `P` which is a probability law
(`IsLaw P`), which is feasible at order `t` for the ancestral-independence hierarchy
`I^AI_t` (`AIFeasible t P`) and hence for the Navascués–Wolfe hierarchy `I^NW_t`
(`NWFeasible t P`), and which is not triangle compatible (`¬ TriangleCompatible P`). So
whatever order is chosen, the order-`t` test admits a law that no triangle model produces,
and no finite level of the hierarchy cuts out the compatible set `C_△`.

Navascués and Wolfe (2020, §4.1) ask whether some finite order settles exact compatibility.
Their hierarchy is asymptotically complete, so every incompatible law is rejected at *some*
finite order; the theorem says that order cannot be bounded uniformly.

The witnesses are the explicit rational family

```
P_t = Q(ε_t, r_t),   ε_t = 1/(2t³),   r_t = (1 − ε_t)^(t−1),
Q(ε, r) = ε·δ_000 + (1 − ε)·Bern(r)^⊗3.
```

Membership is proved by an explicit inflation law on the order-`t` copied observations
(paper Section 3.1): independent `Bern(ε)` defect bits on the cube `[t]³` of source-copy
indices together with independent `Bern(s)` private bits, with a copied observation
outputting `1` exactly when its private bit and every defect on its line are `0`. That law
is `S_t³`-symmetric, has the tensor power `P^⊗t` as its diagonal law, and satisfies the
injectable-marginal and ancestral-independence prescriptions. Incompatibility is the Finner
inequality `P(000)² ≤ P_A(0)·P_B(0)·P_C(0)` (paper Section 3.2), which `P_t` violates by at
least `ε_t²/2 > 0`.

## Formalization boundaries

Three, all recorded as scope restrictions of the theorem as stated. They are recorded in the header
of `TriangleInflation/Defs.lean`, restated in `Palomar/TriangleInflation/Challenge.lean`,
and in `formalization.yaml` under `fidelity.divergences`.

1. **Finite latent alphabets.** `TriangleCompatible` quantifies over `TriangleModel`s whose
   three latent spaces are `Fintype`s; the paper (Section 2) allows arbitrary measurable
   latent spaces. The reduction to bounded finite alphabets (Rosset, Gisin and Wolfe, 2018)
   is quoted in the paper and is *not* formalized. The formal compatible set is therefore a
   priori a subset of the paper's `C_△`, so the formalized `¬ TriangleCompatible P` is the
   weaker of the two readings, and it is what the theorem asserts.
2. **The recursively expressible hierarchy is not formalized.** The paper's `I^exp_t`
   (Definition 2.3) needs `d`-separation in the inflated causal graph and the
   Wolfe–Spekkens–Fritz recursion. Only `I^NW_t` and `I^AI_t` are defined here. Since
   `I^exp_t ⊆ I^AI_t ⊆ I^NW_t`, the formalized membership is the weaker half of the paper's
   Theorem 3.1, and the rejection statements are the stronger halves.
3. **Laws are bare real weight functions** on finite types with the predicate `IsLaw`, not
   Mathlib `Measure`s or `PMF`s; all inequalities are real-valued. The first rejecting order
   `t_min` is `Nat.sInf` of the set of rejecting orders, which returns `0` when that set is
   empty, so every statement about it either exhibits a rejecting order or assumes one.
   Asymptotic completeness itself is quoted from Navascués–Wolfe, not formalized.

Paper results outside this development: Theorem 6.1 and Corollary 6.2 (distance
asymptotics) and Proposition 8.1 (the `2^{Θ(B)}` bit-length law) are unformalized;
Propositions 5.1 and 7.1 are formalized in their finite parts only.

## Layout

```
TriangleInflation/          the library
  Defs.lean                 definitions and the representational decisions
  Finner.lean               the Finner inequality for finite-latent triangle models
  Defect.lean               independence from disjoint root supports
  DefectLaw.lean            the defect-cube law: symmetry, diagonal and injectable marginals
  Main.lean                 Theorem 3.1, Theorem 3.2 and the nontermination corollary
  Fan.lean                  the order-t fan inequalities; the family R_p
  Exponent.lean             the Θ(ε^{-1/3}) bounds along P_ε
  Rate.lean                 the order-t second-moment rate bound
TriangleInflation.lean      aggregator
Palomar/TriangleInflation/
  Challenge.lean            the registry statement: imports Mathlib only, proof `sorry`
  comparator.json           what Comparator compares
PalomarSolutions/
  TriangleInflation.lean    the Solution: same declaration, proved from the library
Audit.lean                  #print axioms for the registry statement and 45 library theorems
scripts/gen_challenge.py    generates Challenge.lean from TriangleInflation/Defs.lean
scripts/check_axioms.sh     the verification gate
formalization.yaml          provenance, sources, automation, review (the
                            mathlib-initiative self-reporting standard; Palomar reads it)
paper/                      main.pdf and its LaTeX sources; release/ holds the claim,
                            non-claim, priority and reproduction documents
```

## The registry statement

`Palomar/TriangleInflation/` is one Comparator comparison in the shape the Palomar
submission standard asks for: a `Challenge.lean` importing only Mathlib and stating the
result as a single declaration left as `sorry`, and a `comparator.json` permitting only the
three standard axioms. The matching Solution, `PalomarSolutions/TriangleInflation.lean`,
declares the same name and proves it from the library.

Comparator compares the two statements constant by constant, so every constant in the
statement has to be identical, by name and by definition body, in the two import closures.
The statement mentions `ThreeBit`, `IsLaw`, `AIFeasible`, `NWFeasible` and
`TriangleCompatible`, which are project definitions, and the Challenge may not import the
project, so the Challenge carries them itself. `scripts/gen_challenge.py` writes
`Challenge.lean` as the Mathlib imports of `TriangleInflation/Defs.lean`, a
Challenge-specific header, the body of that file verbatim from `namespace
TriangleInflation` to its close, and the theorem. `scripts/check_axioms.sh` runs the
generator in `--check` mode and fails if the committed file has drifted.

Challenge and Solution declare the same name, `TriangleInflation.no_finite_characterizing_order`,
so the library's own theorem carries the suffix `_lib`
(`TriangleInflation.no_finite_characterizing_order_lib` in `TriangleInflation/Main.lean`)
and the Solution discharges the registry name by applying it. The Solution sits under its
own root module rather than under `Palomar`: the registry's verifier puts its recompiled
Challenge first on `LEAN_PATH` and Lean resolves every module sharing that root directory
there, so a Solution under `Palomar.*` is never found (PalomarSubmission#108).

To reproduce the registry's mechanical check locally you need
[Comparator](https://github.com/leanprover/comparator) and a `lean4export` built at this
repository's Lean version on `PATH` (on macOS, Comparator's `scripts/fake-landrun.sh`
stands in for the Linux sandbox and is not adversarial):

```bash
lake build
lake env comparator Palomar/TriangleInflation/comparator.json
```

Registration is a deliberate, separate act: nothing in this repository submits anything.

## Verify locally

```bash
lake exe cache get     # or bring your own prebuilt Mathlib at the pinned rev
lake build
bash scripts/check_axioms.sh
```

The gate refuses a literal `sorry` or `admit` anywhere under `TriangleInflation/` or
`PalomarSolutions/`, requires the Challenge to carry exactly one, regenerates the Challenge
from `TriangleInflation/Defs.lean` and fails if the committed file differs, and fails on any
axiom outside `[propext, Classical.choice, Quot.sound]`.

Lean `v4.33.0`; Mathlib pinned at `db584cd6d46c92f209a44c0f1c829460d327499d`, a commit on
canonical `master`. Mathlib is the only dependency.

## Coverage

| Paper | Statement | Status | Lean |
|---|---|---|---|
| Def. 2.1, 2.2 | `I^NW_t`, injectable sets, ancestral independence, `I^AI_t` | proved | `nwFeasible_of_aiFeasible`, `injectable_iff_injectableRaw` |
| Def. 2.3 | the recursively expressible set `I^exp_t` | unformalized | none |
| §2.1 | the compatible set `C_△` | partial (finite latent alphabets) | `TriangleCompatible`, `finner_of_compatible` |
| Lem. 3.3 | disjoint-ancestry independence | proved | `defect_independence`, `defect_independence_family`, `rootSupport_disjoint` |
| Lem. 3.4 | the copied-triangle law and the parameter `s` | proved | `defect_copiedTriangle_law`, `sParam_mem_Icc` |
| Lem. 3.5 | `S_t³` symmetry of the defect-cube law | proved | `defect_symmetric` |
| Lem. 3.7 | the Finner inequality | proved | `finner_of_compatible` |
| Lem. 3.8 | the explicit violation | proved | `witness_violation`, `witness_margin`, `witness_not_compatible` |
| Lem. 3.9 | mutual disjointness of the diagonal supports `R_l` | proved | `diagRegion_disjoint`, `defect_diagonal_law` |
| Thm. 3.1 | membership `Q(ε,r) ∈ I^AI_t ⊆ I^NW_t` | partial (`I^exp_t` excluded) | `membership_AI`, `membership_NW` |
| **Thm. 3.2 + cor.** | **no finite characterizing order** | **proved** | **`no_finite_characterizing_order`** |
| App. A | injectable sets are the subsets of copied triangles | proved | `injectable_iff_injectableRaw` |
| Thm. 4.1 | the order-`t` fan inequalities and the rejecting-order corollary | partial | `fan_first`, `fan_second`, `tminNW_le_of_finner_violation` |
| Prop. 4.2 | `R_p` has rejecting order 2 at every distance | partial | `Rlaw_tminNW`, `Rlaw_tminAI` |
| Prop. 5.1 | `t_min(P_ε) = Θ(ε^{-1/3})` | partial (finite parts) | `Peps_tminNW_bounds`, `Peps_tminAI_bounds` |
| Thm. 6.1, Cor. 6.2 | distance asymptotics | unformalized | none |
| Prop. 7.1 | the distance-promised order bound | partial | `rate_triangle` |
| Prop. 8.1 | the `2^{Θ(B)}` bit-length law | unformalized | none |

All declarations are in the namespace `TriangleInflation`.

## Status of the manuscript

The manuscript is not yet posted to arXiv. This registry entry is meant to precede it and to
be cited by it. `paper/release/PRIORITY_AUDIT.md` records `PRIORITY_NOT_KILLED`, with
Navascués–Wolfe 2020 §4.1 as the strongest located predecessor, and does not certify
firstness; `paper/release/NONCLAIMS.md` records exactly what is and is not formalized, and
its scope agrees with the Coverage table above. No independent human review of the
mathematics has been performed.

A green build here is a scoped, re-checkable build and axiom result. It is not scientific
acceptance.

## Licence

MIT; see [`LICENSE`](LICENSE). The manuscript under `paper/` is by the same author and is
covered by the same licence.
