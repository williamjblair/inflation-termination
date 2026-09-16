> Historical audit retained from before the editorial revision. For current section numbers, corrections, deferred results and validation, see `paper/review/EDITORIAL_REVIEW.md` and the opening update in `RELEASE_STATUS.md`.

## Additions of 16 September 2026 (current numbering)

- **Not a classification of hypergraph scenarios.** Section 7 proves termination for the class of Corollary 7.10 and nontermination whenever a pair set carries a non-double-star component. Conjecture 7.14 is not proved; whether `K_4^(3)` terminates is open, and on five observers eleven reduced scenarios are left undecided by the two results.
- **Not that the AI and NW parity thresholds coincide at odd orders.** The brackets agree at every certified odd order through 13 on the triangle and through 9 on the square; no proof is claimed, and the floating-point triangle values at order 15 decide nothing.
- **Not sharp constants.** The survivor bounds `1/(47t)` and `1/(43t)` are not claimed optimal, and the certificate constants 8 and 10 of Proposition 6.3 are not known to be sharp.
- **Not an explicit rejecting order for every incompatible law.** Section 6.3 covers laws detected by the cubic certificates or the max-moment form; Question 8.5 remains open for the rest.
- **Not a Lean proof of the wider ranges.** Lean proves the square and triangle witnesses at `q = 1/(16t)` only, with `c = 5` and `c = 4`. The ranges with `c = m R^{m-1}`, Corollaries 4.6 and 4.7, Proposition 4.12, Section 6.3 and Section 7 are analytic only.
- **Sampled checks are not proofs.** The random compatible models in `artifact/certificates/beyond-finner/` test the constants of Proposition 6.3; the proof is in the text.

# Non-claims

The manuscript does not claim, and the reader must not infer:

- **"Inflation is incomplete."** False: the hierarchy is asymptotically complete
  (Navascués–Wolfe); the paper relies on it.
- **"Some incompatible instance passes every order."** False and excluded by
  completeness; the witness depends on `t` (`∀t ∃P_t`, never `∃P ∀t`).
- **"Compatibility is undecidable."** Not claimed; rational triangle compatibility
  is decidable (Rosset–Gisin–Wolfe + real algebraic geometry).
- **"No instance-dependent bound exists."** Not claimed; explicit bounds exist for
  Finner-refuted laws (Thm 9.1), parity violations on the square (Lemma 6.13),
  under a distance promise (Prop. 12.1), and in principle by quantifier elimination.
- **"Inflation is computationally useless."** Not claimed.
- **Not a sharp worst-case convergence theorem.** On the square and the triangle
  the worst-case distance `H_t` is bracketed between `Ω(1/t)` and `O(t^{-1/2})`
  (Cor. 6.17); the exponent in `[1/2, 1]` is open. On longer cycles and on `P_5`
  only `Ω(t^{-2})` lower bounds are proved. The `Θ(d^{-1/3})` law of Cor. 11.2 is
  a statement about one family, not a worst-case rate.
- **Not a universal distance-only condition number.** The `Θ(d^{-1/3})` law holds
  along `P_ε`; `R_p` has `t_min = 2` at every distance.
- **Not an exact leading constant.** Only `1/2 ≤ liminf ≤ limsup ≤ 4 − 2√3`;
  convergence of `ε^{1/3} t_min(P_ε)` is not proved.
- **Not a runtime lower bound for all compatibility algorithms.** The `2^{Θ(B)}`
  law bounds the inflation order; membership for the fixed scenario is decidable
  in polynomial time in `B` in principle (fixed quantifier-free formula).
- **Not a classification beyond pair-source scenarios.** Theorem 4.2 classifies
  finite simple graphs with binary observed variables (and, by Remark 4.4, any
  fixed finite observed alphabets). Scenarios with a source shared by three or
  more observed variables, and general DAGs with observed parents, are not
  classified.
- **Not a quantum (or no-signalling / polygon) inflation theorem.**
- **Not an exact operational-divergence asymptotic** (the regularized reverse-KL
  quantity is described only; nothing about its exact value).
- **Not that the fan crossing is the first complete-LP rejection** in general.
- **Not strictness of `I_t^AI ⊊ I_t^NW` at every order.** The separations
  `I_3^NW(□) ⊊ I_2^AI(□) ⊊ I_2^NW(□)` are at particular orders and rest on exact
  certificates (Prop. 6.20, pending); Theorem 6.18 bounds the order conversion
  by a factor `3/2` on the square only.
- **Not that the three hierarchies differ on pair-source scenarios beyond
  NW versus AI.** `I_t^exp = I_t^AI` on every pair-source scenario (Lemma 3.9).
- **Not a quantitative result for the packet's supporting families** beyond what
  Appendix C states; the rare-selector and ceiling results there are reported
  with the packet's own finite checks, which were not replayed here.
- **Not priority / firstness**; see PRIORITY_AUDIT.md.
- **Formal verification is partial, and its scope is stated.** Formalized in Lean 4 with Mathlib (audited library `lean/ResourceTheory/`, no `sorry`, axioms `propext`, `Classical.choice`, `Quot.sound` only; coverage map `lean/coverage/inflation-nontermination.json`): the triangle nontermination theorem with its lemmas (finite-latent and arbitrary-latent-space forms), Appendix A, the fan inequalities with the rejecting-order bound, Proposition 9.2, the finite bounds of Proposition 10.1, the triangle case of Proposition 12.1 and the convex-order ℓ² rate; and, for pair-source scenarios with binary observations and finite latent alphabets, the definitions and nesting of the three tests, soundness, the root-sink lemma, source-disjoint independence at order two, transport, exhaustion, the double-star reconstruction, the cycle and five-path witnesses at every order with their incompatibility and distance bounds, the quantitative parity rigidity, the triangle witness at q = 1/(16t), local flips, and Theorem 4.2 itself. Not formalized: the square witness of Theorem 6.11 (kept with `sorry` in the separate unaudited library `lean/InflationGraphOpen/`), Lemma 6.13, Corollaries 6.14–6.15, Theorem 6.18, Proposition 6.20, the larger-alphabet transfer, Appendix C, Theorem 11.1, Corollary 11.2, Proposition 13.1, the liminf/limsup form of Proposition 10.1, and Corollary 8.3. Nonmembership in the finite-latent compatible set is the weaker reading and does not by itself give nonmembership in the arbitrary-latent set; the arbitrary-latent form is proved only for the triangle defect family.
- **Not the strong-converse or faithfulness theorems**, which belong to a separate paper.
