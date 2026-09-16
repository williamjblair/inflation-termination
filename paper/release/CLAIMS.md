# Claims

Exact scope of what the manuscript proves, in the numbering of the current PDF (revision of 16 September 2026, after the cut of the hypergraph section and the shortening of Section 6.3). "Analytic" means proved in the text; "exact" means also checked by a finite rational certificate under `artifact/certificates/`; "Lean" means formalized in this repository, with declaration names in `README.md` and `formalization.yaml`. Earlier ledgers with older numbering and superseded constants were removed from this file on 16 September 2026; they remain in the git history.

## Pair-source scenarios: setup and classification (Sections 2 and 3, Appendix A)

1. **Definitions 2.1 to 2.5, Proposition 2.6.** A pair-source scenario is a finite simple graph without isolated vertices, with one independent source per edge. The order-`t` feasible sets satisfy `C_G ⊆ I_t^exp(G) ⊆ I_t^AI(G) ⊆ I_t^NW(G)`. Analytic; Lean (binary observations, finite latent alphabets).
2. **Lemma 3.4 (root-sink) and Lemma A.1.** `I_t^exp(G) = I_t^AI(G)` for every pair-source `G` and every `t`. Analytic; Lean.
3. **Lemma 3.5 (source-disjoint independence).** Under any order-`t` NW witness with `t >= 2`, observed blocks with no common source are independent. Analytic; Lean at order two.
4. **Lemma 3.6 (induced-subgraph transport).** A witness on an induced subgraph extends with fair bits, and the extended law is at least as far from `C_G`. Analytic; Lean.
5. **Theorem 3.2 (classification).** For binary observations: some finite NW order equals `C_G` iff some finite AI order does iff some finite exp order does iff every component is a double-star (tree of diameter at most three), and then order two suffices. Otherwise, for every `t`, a strictly positive rational law lies in `I_t^exp(G) \ C_G`. Analytic; Lean for the equivalence and strictly positive witness existence with finite latent alphabets; rationality of the witnesses is analytic. Registered as `PALOMAR-2026-09-14-000009`.
6. **Lemma 3.7 (exhaustion).** A connected non-double-star graph with an edge has an induced cycle or an induced `P_5`. Analytic; Lean. The shape of the argument follows Fritz 2012, Theorem 3.8 and Lemma 3.9 (stars; induced `C_3`, `C_4` or `P_4`), cited in the text.
7. **Remark 3.8.** The classification transfers to any fixed finite observed alphabets, with termination order `max({2} ∪ leaf alphabet sizes)`. Analytic.
8. **Remark 3.9.** For three observers reading one source every law is compatible (Fritz 2012, Proposition 3.7), so the observer graph does not decide termination once sources may be shared by three or more observers. Scenarios of that kind are not treated in this manuscript.
9. **Theorem 3.10, Corollaries 3.11 to 3.13 (double-star reconstruction).** `I_T^NW(G) = C_G` for a double-star with finite alphabets; order two for binary observations; the four-observer path; disjoint unions. Analytic; Lean for Theorem 3.10 and Corollary 3.11 (binary case).
10. **Lemmas 3.14 to 3.20, Theorem 3.21 (cycles).** For `m >= 3`, `q = 1/(4m²t²)` and `η = q/(32m)`, the flipped parity law is strictly positive rational, lies in `I_t^exp(C_m) = I_t^AI(C_m)`, and has distance at least `11/(640 m² t²)` from `C_{C_m}`. Exact parity rigidity (Lemma 3.18) is due to Boreiri et al. 2023; Lemma 3.19 is a moment form of the robustness of Boreiri et al. 2025. Analytic; exact certificates for `C_3, C_4, C_5` at orders 1 and 2; Lean (Lemmas 3.14 to 3.18 in part).
11. **Lemmas 3.23, 3.24, Corollary 3.25, Theorem 3.26 (five-observer path).** `d_TV(P_h, C_{P_5}) >= h/96`; `P_{h_t} ∈ I_t^exp(P_5)` for `h_t = 1/(16t²)`, with distance at least `1/(1536 t²)`. The bilocal inequality is due to Branciard, Rosset, Gisin and Pironio. Analytic; exact certificates at orders 1 and 2; Lean.

## Quantitative convergence on the triangle and square (Section 4, Appendix B)

12. **Lemma 4.2 (corrected density).** For `m ∈ {3,4}`, `R = (1+q)^{t/2} <= m²/(m²-1)` and `c = m R^{m-1}`, the density `W` satisfies `W >= R^{m-1}(m² - (m²-1)R) >= 0` and has the stated characters. The range contains `q <= 1/(8t)` (`m = 4`) and `q <= 2/(9t)` (`m = 3`). Analytic. Lean proves a variant with the fixed constants `c = 4` (`m = 3`) and `c = 5` (`m = 4`, inside `square_linear_witness`) for `tq <= 1/16`.
13. **Theorems 4.3 and 4.4.** `P_q ∈ I_t^AI(□) = I_t^exp(□)` for `0 < q <= (16/15)^{2/t} - 1`; `Π(-q,-q,-q) ∈ I_t^AI(△) = I_t^exp(△)` for `0 < q <= (9/8)^{2/t} - 1`. Analytic. Exact certificates at `q = 1/(16t)` with `c = 5` (square, orders 1 and 2) and `c = 4` (triangle, orders 1 to 3). Lean at `q = 1/(16t)` only: `square_linear_witness` and `triangle_linear_witness` assume `q = 1/(16t)`, not a range of `q`.
14. **Lemma 4.5 and Corollaries 4.6, 4.7.** Every square-compatible law satisfies `max{EA, EB, E[AB]} + 4 P(ABCD = -1) >= 0`. With the guarantee endpoints `q_t = (16/15)^{2/t} - 1` and `q_t = (9/8)^{2/t} - 1` (written with an underline in the paper): `H_t^exp(□) = H_t^AI(□) >= q_t/6 > 1/(47t)` and `H_t^exp(△) = H_t^AI(△) >= q_t/10 > 1/(43t)`, also over strictly positive accepted laws. Analytic.
15. **Theorem 4.8 (convex order).** For any correlation scenario with `K` joint outcomes (private-source convention), the uniform-index law of a witness table is compatible, `E Φ(q_ω) <= E Φ(P̂_n)` for convex `Φ`, and `H_n^NW(G) <= min{1, √(K-1)/(2√n)}`. Analytic; Lean for the triangle norm estimates.
16. **Corollary 4.9 (brackets).** `(1/6)((16/15)^{2/t} - 1) <= H_t^exp(□) = H_t^AI(□) <= H_t^NW(□) <= min{1, √15/(2√t)}` and `(1/10)((9/8)^{2/t} - 1) <= H_t^exp(△) = H_t^AI(△) <= H_t^NW(△) <= √7/(2√t)`. The exponent in `[1/2, 1]` is not determined. Analytic.
17. **Theorem 4.10 (order conversion on the square).** `I^NW_{⌊3t/2⌋}(□) ⊆ I_t^AI(□) = I_t^exp(□) ⊆ I_t^NW(□)` for `t >= 2`. Analytic.
18. **Lemmas B.1 to B.4 (sign potentials, count-moment reductions, monotonicity).** Every parity-perfect table is a potential table, unique up to a global flip; a family-exchangeable law on potentials with the prescribed means is a witness; feasibility of the square and triangle parity targets reduces to Krawtchouk moment equations on the degree sets `D_AI(t)` and `D_NW(t)`; the accepted parameters form an interval. Analytic, with the proofs written out in full on 16 September 2026.
19. **Proposition 4.11 (thresholds through order ten).** Certified brackets for `q_t^AI` and `q_t^NW` on both scenarios (Table 1); `q_t^AI < q_t^NW` at every even `t <= 10`; identical certified brackets at every odd `t <= 9`, which do not establish equal thresholds; `I_3^NW(□) ⊊ I_2^AI(□) ⊊ I_2^NW(□)`. Exact certificates.
20. **Proposition 4.12 (order conversion along the parity direction).** `q_t^NW <= q_s^AI` for `t >= max{s, ⌊3s/2⌋}` on the square and the triangle. Analytic.
21. **Triangle brackets at orders 11 to 13 (paragraph after Proposition 4.12).** Identical certified brackets for `q_t^AI` and `q_t^NW` at `t = 11, 13`, with an AI dual on NW keys, and `q_12^AI < q_12^NW`. Exact certificates. Equality of the thresholds at odd orders is not claimed.

## The triangle defect family (Section 5)

22. **Theorem 5.1 (membership).** `Q(ε, r) ∈ I_t^exp ⊆ I_t^AI ⊆ I_t^NW` for `0 < ε < 1`, `0 <= r <= (1-ε)^{t-1}`. Analytic; exact at `t = 1, 2, 3`; Lean for NW and AI.
23. **Theorem 5.2 and Corollary 5.3.** `P_t = Q(ε_t, r_t)` with `ε_t = 1/(2t³)` lies in `I_t^exp` and violates Finner by at least `ε_t²/2`; no finite order characterizes `C_△`, for any observed alphabets of size at least two. Analytic; Lean for Theorem 5.2 with AI and NW membership (finite latent alphabets, and arbitrary latent spaces in `FinnerMeasure.lean`; the exp half through the graph bridge); Corollary 5.3 not formalized.
24. **Lemmas 5.4 to 5.10.** Disjoint-ancestry independence, copied-triangle law, symmetry, Finner for arbitrary latent spaces, the violation, diagonal law, recursive prescriptions. Analytic; Lean for Lemmas 5.4 to 5.9.
25. **Theorem 5.11 (fan inequalities).** `tz <= a + C(t,2) bc` and `t(z² - abc) <= az - abc` on `I_t^NW`, with an explicit rejecting order for every Finner violation. Analytic; exact certificates for fourteen targets; Lean in part (the two inequalities and the rejecting-order corollary for NW).
26. **Proposition 5.12.** `R_p` is incompatible with first rejecting order 2 for every `p`. Analytic; Lean in part.
27. **Proposition 5.13.** Along `P_ε`, `1/2 <= liminf ε^{1/3} t_min <= limsup <= 4 - 2√3`. Analytic; the finite bounds in Lean.
28. **Theorem 5.14, Corollary 5.15.** `d_TV(P_ε, C_△) = (1 - 2^{-3/2})ε + O(ε^{4/3})`, and `t_min = Θ(d^{-1/3})` along this family only. Analytic.

## Rejecting orders from distance, input size and parity certificates (Section 6)

29. **Corollary 6.1 (distance-promised order).** `t_min^NW(P) <= ⌊(1 - ‖P‖²)/δ_2²⌋ + 1 <= ⌊(K-1)/(4δ²)⌋ + 1`. Analytic; the triangle case in Lean.
30. **Proposition 6.2 (bit length).** The worst first rejecting order over incompatible rational three-bit laws of bit length at most `B` is `2^{Θ(B)}`. Analytic.
31. **Remark 6.3 (cubic parity certificates and explicit rejecting orders).** On `C_□`: `EA EB E[AB] + 8 R(ABCD = ∓1) >= 0`; on `C_△`: `±EA EB EC + 10 R(ABC = ∓1) >= 0`. For each such left-hand side `F` and `P ∈ I_n^NW`, `F(P) >= -Σ(P)/n` with `Σ(P) <= 3`, so `t_min^H(P) <= ⌊Σ(P)/(-F(P))⌋ + 1 <= ⌊3/(-F(P))⌋ + 1` for all three hierarchies when `F(P) < 0`. Analytic, with a short proof in the remark; sampled exact falsification test of the constants. The `1/n` mechanism is Navascués–Wolfe 2020, Theorem 1 with eqs. (34) and (A5); the source-free constant is the new point.

## Supporting material (Appendices C and D)

32. **Appendix C.** Certificate formats and finite coverage.
33. **Appendix D.** Supplementary inequalities and extraction results (Propositions D.1, D.4, D.5, D.7, Lemmas D.2, D.3, Theorem D.6), proved in the text. Proposition D.7 supplies the triangle NW order-two endpoint used in Proposition 4.11. Not formalized.
