# Claims

Exact scope of what the manuscript proves (numbering as in the paper).

1. **Theorem 3.1 (membership).** For `t ≥ 1`, `0 < ε < 1`, `0 ≤ r ≤ (1−ε)^{t−1}`:
   `Q(ε,r) = ε δ_000 + (1−ε) Bern(r)^{⊗3}` lies in `I_t^exp ⊆ I_t^AI ⊆ I_t^NW`.
   (`Bern(r)(1) = r`.)
2. **Theorem 3.2 (Theorem A: no finite characterizing order).** With
   `ε_t = 1/(2t³)`, `r_t = (1−ε_t)^{t−1}`, `P_t = Q(ε_t, r_t)`: `P_t ∈ I_t^exp` and
   `P_t(000)² − P_{t,A}(0)P_{t,B}(0)P_{t,C}(0) ≥ ε_t²/2 > 0`, so `P_t ∉ C_△`.
   Quantifiers `∀t ∃P_t`; includes `t = 1`.
3. **Corollary 3.3.** Same for the triangle with observed alphabets of any sizes `≥ 2`.
4. **Lemmas 3.4–3.11.** Disjoint-ancestry independence; copied-triangle law;
   `S_t³` symmetry; Finner inequality for arbitrary latent spaces and stochastic
   responses (two Cauchy–Schwarz steps); the explicit violation; mutual
   disjointness of the diagonal supports `R_l`; latent-projection containment;
   recursive expressible prescriptions.
5. **Theorem 4.1 (fan inequalities).** Every order-`t` NW-feasible three-bit law
   obeys `t z ≤ a + C(t,2) b c` and `t(z² − abc) ≤ a z − abc`
   (`a,b,c` zero marginals, `z = P(000)`), using only `S_t³` symmetry and the
   degree-1 and degree-2 diagonal conditions (cross identity `E[B_k C_l] = bc`,
   `k ≠ l`, via the index map `X_1→1, Z_1→2, Y_k→1, Y_l→2`). Hence for any
   Finner violation `t_min ≤ ⌊(z·min(a,b,c) − abc)/(z² − abc)⌋ + 1`, for all
   three hierarchies.
6. **Proposition 4.2 (no distance-only lower bound).** `R_p = (1−p)δ_111 + pδ_000`
   is incompatible with `t_min = 2` for every `p ∈ (0,1)`, while
   `d_TV(R_p, C_△) → 0`.
7. **Proposition 5.1 (Theorem B: sharp exponent).** `P_ε = Q(ε, 1 − ε^{2/3}/2)`,
   `0 < ε < 1/8`: incompatible, `P_ε → δ_111`; for `H ∈ {NW, AI, exp}`,
   `⌊1 + ε^{-1/3}/2⌋ + 1 ≤ t_min^H(P_ε) ≤ ⌊τ_-⌋ + 1` (`ε ≤ 1/64`), with
   `τ_- = (z + m²/2 − √((z + m²/2)² − 2m³))/m²`; hence
   `1/2 ≤ liminf ε^{1/3} t_min ≤ limsup ε^{1/3} t_min ≤ 4 − 2√3`, i.e.
   `t_min = Θ(ε^{-1/3})`. Exponent proved; limit existence and constant not.
8. **Theorem 6.1 (distance asymptotics).** `d_TV(P_ε, C_△) = (1 − 2^{-3/2})ε + O(ε^{4/3})`,
   `‖P_ε − C_△‖_2 = √(8/7)(1 − 2^{-3/2})ε + O(ε^{4/3})` (lower bounds from Finner;
   upper bounds from an explicit compatible model with base bits `√u` and flags
   `hε`).
9. **Corollary 6.2 (direction-specific boundary complexity).**
   `t_min^H(P_ε) = Θ(d_TV(P_ε, C_△)^{-1/3}) = Θ(‖P_ε − C_△‖_2^{-1/3})`; not a
   universal condition number (Prop. 4.2).
10. **Proposition 7.1 (distance-promised order).** `P ∈ I_n^NW(G)` implies
    `‖P − C_G‖_2² ≤ [1 − (1 − 1/n)^L] · (1 − ‖P‖_2²) ≤ L(1 − ‖P‖_2²)/n`; hence
    `t_min ≤ ⌊L(1−‖P‖_2²)/δ_2²⌋ + 1 ≤ ⌊LK/(4δ_TV²)⌋ + 1` (triangle: `⌊6/δ²⌋ + 1`).
    `L` counts sources with deterministic responses; TV is half the ℓ¹ norm; NW's
    (A7) is an ℓ¹ bound and the factor is tracked. A genuine compatible component
    is extracted (no convex hull). Credited as NW's quantitative convergence with
    exact constants.
11. **Proposition 8.1 (bit-length law).** Over rational three-bit laws with
    encoding length `≤ B`, the worst first rejecting order is `2^{Θ(B)}` for each
    hierarchy (lower bound: `P_ε`, `ε = 2^{-3j}`; upper bound: Rosset–Gisin–Wolfe
    semialgebraicity, a fixed quantifier-free description, root separation with
    height `2^{O(B)}`, and Prop. 7.1). Hierarchy-level statement only.
12. **Effectivity boundary (Sections 7, 10).** Exact rational compatibility is
    decidable; a rejecting order is computable in principle via quantifier
    elimination; explicit orders exist for Finner-refuted laws (Thm 4.1) and under
    a distance promise (Prop. 7.1). Open: exact constant, worst-case exponent,
    finite-stabilization classification, quantum analogue, tariff computability.
13. **Computational content.** Exact rational certificates at `t = 1,2,3`; sparse
    full order-2 table; rejected negative control; order-2 Farkas calibration;
    fan certificates (14 rational targets, all-order polynomial certificate,
    174,760 assignments, 271,500 count orbits, 2,660 embeddings, 8 negative
    controls); the proofs do not depend on them.
