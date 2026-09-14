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
