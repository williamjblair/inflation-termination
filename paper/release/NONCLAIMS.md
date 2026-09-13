# Non-claims

The manuscript does not claim, and the reader must not infer:

- **"Inflation is incomplete."** False: the hierarchy is asymptotically complete
  (Navascués–Wolfe); the paper relies on it.
- **"Some incompatible instance passes every order."** False and excluded by
  completeness; the witness depends on `t` (`∀t ∃P_t`, never `∃P ∀t`).
- **"Compatibility is undecidable."** Not claimed; rational triangle compatibility
  is decidable (Rosset–Gisin–Wolfe + real algebraic geometry).
- **"No instance-dependent bound exists."** Not claimed; explicit bounds exist for
  Finner-refuted laws (Thm 4.1), under a distance promise (Prop. 7.1), and in
  principle by quantifier elimination.
- **"Inflation is computationally useless."** Not claimed.
- **Not a sharp worst-case convergence theorem.** The worst-case distance
  `sup_{P ∈ I_n} d_TV(P, C_△)` is only known to lie between `Ω(n^{-3})` and
  `O(n^{-1/2})`.
- **Not a universal distance-only condition number.** The `Θ(d^{-1/3})` law holds
  along `P_ε`; `R_p` has `t_min = 2` at every distance.
- **Not an exact leading constant.** Only `1/2 ≤ liminf ≤ limsup ≤ 4 − 2√3`;
  convergence of `ε^{1/3} t_min(P_ε)` is not proved.
- **Not a runtime lower bound for all compatibility algorithms.** The `2^{Θ(B)}`
  law bounds the inflation order; membership for the fixed scenario is decidable
  in polynomial time in `B` in principle (fixed quantifier-free formula).
- **Not a finite-stabilization classification** of scenarios.
- **Not a quantum (or no-signalling / polygon) inflation theorem.**
- **Not an exact operational-divergence asymptotic** (the regularized reverse-KL
  quantity is described only; nothing about its exact value).
- **Not that the fan crossing is the first complete-LP rejection** in general.
- **Not scenarios other than the triangle.**
- **Not priority / firstness**; see PRIORITY_AUDIT.md.
- **Not formal (Lean) verification.**
- **Not the strong-converse or faithfulness theorems**, which belong to a separate paper.
