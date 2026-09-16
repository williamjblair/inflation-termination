> Historical audit retained from before the editorial revision. For current section numbers, corrections, deferred results and validation, see `paper/review/EDITORIAL_REVIEW.md` and the opening update in `RELEASE_STATUS.md`.

## Additions of 16 September 2026 (current numbering)

These entries use the numbering of the current PDF. "Analytic" means proved in the text and audited on 16 September 2026; "exact" means also checked by a finite rational certificate; "Lean" means formalized in this repository.

A1. **Lemma 4.2 (corrected density).** For `m in {3,4}`, `t >= 1` and `q > 0` with `R = (1+q)^{t/2} <= m²/(m²-1)`, that is `q <= (9/8)^{2/t} - 1` for `m = 3` and `q <= (16/15)^{2/t} - 1` for `m = 4`, and `c = m R^{m-1}`, the density `W = Re ∏ f_g + c Σ_g (1 - Re f_g)` satisfies `W >= R^{m-1}(m² - (m²-1)R) >= 0` and has the characters of `eq:Wmoments`. The range contains `q <= 1/(8t)` (`m = 4`) and `q <= 2/(9t)` (`m = 3`). Analytic. Lean for `m = 3, c = 4` and, inside `square_linear_witness`, `m = 4, c = 5`, both at `tq <= 1/16`.
A2. **Theorems 4.3 and 4.4.** `P_q ∈ I_t^AI(□) = I_t^exp(□)` for `0 < q <= (16/15)^{2/t} - 1`; `Π(-q,-q,-q) ∈ I_t^AI(△) = I_t^exp(△)` for `0 < q <= (9/8)^{2/t} - 1`. Analytic; exact certificates at `q = 1/(16t)` (square orders 1 to 2, triangle orders 1 to 3); Lean at the endpoint specialization `q = 1/(16t)` only (`square_linear_witness`, `triangle_linear_witness`).
A3. **Corollaries 4.6, 4.7 and 4.9.** With `q_t = (16/15)^{2/t} - 1` and `q_t = (9/8)^{2/t} - 1`: `H_t^exp(□) = H_t^AI(□) >= q_t/6 > 1/(47t)` and `H_t^exp(△) = H_t^AI(△) >= q_t/10 > 1/(43t)`, also for the supremum over strictly positive accepted laws; the brackets of Corollary 4.9 use these lower bounds with the unchanged upper bounds. Analytic.
A4. **Proposition 4.12 (order conversion along the parity direction).** For `s >= 1` and `t >= max{s, ⌊3s/2⌋}`, `q_t^NW <= q_s^AI` on the square and the triangle. Analytic.
A5. **Brackets at triangle orders 11 to 13.** `q_t^AI` and `q_t^NW` have identical certified brackets at `t = 11, 13`, with an AI dual using NW keys only, and `q_12^AI < q_12^NW`. Exact certificates. Whether the thresholds coincide at every odd order is not claimed.
A6. **Proposition 6.3 (cubic parity certificates).** On `C_□`: `EA EB E[AB] + 8 R(ABCD = -1) >= 0` and `EA EB E[AB] + 8 R(ABCD = 1) >= 0`; on `C_△`: `±EA EB EC + 10 R(ABC = ∓1) >= 0`. Analytic; sampled exact falsification test.
A7. **Proposition 6.4 and Corollary 6.5 (explicit rejecting orders).** For `P ∈ I_n^NW`, `F(P) >= -Σ(P)/n` with `Σ(P) <= min{3, 6(1 - ‖P‖²)}`; hence `t_min^H(P) <= ⌊Σ(P)/(-F(P))⌋ + 1` when `F(P) < 0`, and the quadratic bound of Corollary 6.5(ii) when `G(P) < 0`, for `H` in NW, AI, exp. Analytic.
A8. **Proposition 6.6.** A three-bit law that violates a Finner inequality has both triangle certificates nonnegative; a law satisfying all eight Finner inequalities fails no fan inequality at any order. Analytic; sampled exact check. Remark 6.7 examples exact.
A9. **Section 7 (hypergraph scenarios).** Lemmas 7.2, 7.3, 7.5, Corollary 7.6; Theorem 7.7 (an observer reading every source drops out); Theorem 7.9 (hyper-double-star reconstruction at order `T_H`); Corollary 7.10 (termination for the peeling class `P`); Proposition 7.11 (on graphs, `P` is the double-stars); Theorem 7.13 (for binary observations, strictly positive rational laws in `I_t^exp(H) \ C_H` at every `t`, with the cycle and five-path distance bounds, whenever a pair set carries a non-double-star component with an edge). Analytic; exact instance checks. Conjecture 7.14 is open; `K_4^(3)` is the only four-observer scenario the two results leave undecided (exhaustive enumeration).

# Claims

Exact scope of what the manuscript proves (numbering as in the paper after the
2026-09-13 integration; Theorems A, B, C are Theorems 1.1, 1.2, 1.3 of the
introduction). "Analytic" means proved in the text; "exact" means also checked
by a finite rational certificate; "Lean" means formalized (scope in
`lean/coverage/inflation-nontermination.json`).

## Pair-source scenarios (Sections 3–7)

1. **Definitions 3.1–3.5.** A pair-source scenario is a finite simple graph
   without isolated vertices; vertices are binary observed variables, edges
   independent sources. Order-`t` hierarchies `I_t^NW(G) ⊇ I_t^AI(G) ⊇ I_t^exp(G)`
   are defined as for the triangle; Proposition 3.6 (soundness) shows
   `C_G ⊆ I_t^exp(G)`. Analytic.
2. **Lemma 3.7 (trail criterion) and Lemma 3.9 (root-sink).** In an inflation
   graph whose latent nodes are roots and observed nodes sinks, conditioning on
   an observed set activates exactly the trails whose internal observed nodes
   lie in it. Consequently the recursively expressible closure equals the
   ancestral-independence family and `I_t^exp(G) = I_t^AI(G)` for every
   pair-source `G` and every `t`, the triangle included. Analytic (the
   packet's component criterion was corrected to the trail criterion).
3. **Lemma 3.10 (source-disjoint independence).** Under any order-`≥2` witness,
   observed blocks with no common source are independent. Analytic.
4. **Lemma 3.11 (transport).** A witness for a connected induced subgraph `H`
   extends to `G` with fair bits on the other vertices; the extended target is
   at least as far from `C_G` as the original from `C_H`. Analytic.
5. **Theorem 4.2 (Theorem A, classification).** For binary pair-source `G`:
   some finite NW order equals `C_G` iff some finite AI order does iff some
   finite exp order does iff every component is a double-star (tree of
   diameter `≤ 3`); then `I_2 = C_G`. Otherwise for every `t` a strictly
   positive rational law in `I_t^exp(G) \ C_G`. Analytic; assembled from
   Lemma 4.3 (exhaustion: a connected non-double-star contains an induced
   cycle or an induced `P_5`), Theorem 5.1, Theorem 6.8, Theorem 7.5 and
   Lemma 3.11. Remark 4.4: larger fixed observed alphabets (nontermination
   transfers; termination with `T = max(2, leaf alphabets)`). Remark 4.5: not a
   statement about hypergraph scenarios.
6. **Theorem 5.1 (double-star reconstruction).** `I_T^NW(G) = C_G` for a
   double-star with finite observed alphabets, `T = max({2} ∪ leaf alphabet
   sizes)`; Corollaries 5.2–5.4 (binary: order two; paths on `≤ 4` vertices;
   disjoint unions). Analytic.
7. **Lemmas 6.1–6.7, Theorem 6.8 (cycles at every order).** For `m ≥ 3`,
   `q = 1/(4m²t²)`, `η = q/(32m)`, the flipped parity law `T_η^{⊗m} P_{m,q}` is
   strictly positive rational, lies in `I_t^AI(C_m) = I_t^exp(C_m)`, and is at
   total-variation distance `≥ 11/(640 m² t²)` from `C_{C_m}`. Ingredients:
   positivity of the parity density `H_{N,q}` for `N² q ≤ 1/4`; boundary
   lemma for prescribed characters; parity rigidity (Lemma 6.5) and `5η`
   quantitative parity rigidity `max{EA,EB,EC} ≥ −4(1−E[ABC])` (Lemma 6.6); Lemma 6.7 (distance `≥ q/10`). Analytic; exact
   certificate at small orders (`artifact/certificates/classification/`).
8. **Lemma 6.10 (corrected density).** For `m` families of `t` signs and
   `tq ≤ 1/16`, `W = Re ∏ f_g + c Σ_g (1 − Re f_g)` is a probability density
   (`m = 4, c = 5`: `W ≥ 1/3`; `m = 3, c = 4`: `W ≥ 3/5`) whose characters
   equal `(−q)^{|S|/2}` for even `S` meeting at least two families. Analytic.
9. **Theorem 6.11 (square at `q = Θ(1/t)`).** `P_q ∈ I_t^AI(□) = I_t^exp(□)` for
   `0 < q ≤ 1/(16t)`. Analytic; exact certificate at small orders.
10. **Theorem 6.12 (triangle at `q = Θ(1/t)`).** `Π(−q,−q,−q) ∈ I_t^AI(△)` for
    `0 < q ≤ 1/(16t)`. Analytic; exact certificates at orders 1 to 3 (plain and
    flipped); Lean-proved for every `t ≥ 1` (`triangle_linear_witness`).
11. **Lemma 6.13 (max-moment inequality).** Every square-compatible law obeys
    `max{EA, EB, EAB} + 4 P(ABCD = −1) ≥ 0`; hence `d_TV(P_q, C_□) ≥ q/6`.
    Analytic.
12. **Corollaries 6.14–6.15 (full-support survivors).**
    `H_t^exp(□) = H_t^AI(□) ≥ 5/(768t)` and `H_t^exp(△) = H_t^AI(△) ≥ 27/(5120t)`
    (the triangle bound inherits the pending status of item 10).
13. **Theorem 6.16 (convex order).** For `P ∈ I_n^NW(G)` with witness `Γ`, the
    uniform-index law `q_ω` of a deterministic table is compatible and
    `E Φ(q_ω) ≤ E Φ(P̂_n)` for convex `Φ`; `E‖q_ω − P‖² ≤ (1 − ‖P‖²)/n`;
    `d_TV(P, C_G) ≤ √(K−1)/(2√n)`. Analytic; Lean for the triangle
    (`ConvexOrder.lean`).
14. **Corollary 6.17 (Theorem B, brackets).**
    `5/(768t) ≤ H_t^exp(□) = H_t^AI(□) ≤ H_t^NW(□) ≤ min{1, √15/(2√t)}` and
    `27/(5120t) ≤ H_t^exp(△) = H_t^AI(△) ≤ H_t^NW(△) ≤ √7/(2√t)`. The exponent
    in `[1/2, 1]` is not determined.
15. **Theorem 6.18 (order conversion).**
    `I^NW_{⌊3t/2⌋}(□) ⊆ I_t^AI(□) = I_t^exp(□) ⊆ I_t^NW(□)` for `t ≥ 2`. Analytic.
16. **Lemmas 6.19 to 6.21, Proposition 6.22 (parity thresholds).** Count-moment
    (Krawtchouk) reduction of the parity tests for AI and NW on the square and
    the triangle, monotonicity along the parity direction, and certified brackets
    for the thresholds `q^AI_t`, `q^NW_t` at orders 1 to 10 (Table 1): AI ⊊ NW at
    even orders, coincidence at odd orders ≤ 9, exact values `2−√3`, `1/5`, `1/7`
    and the root of `q³−33q²+27q−3`; `I_3^NW(□) ⊊ I_2^AI(□) ⊊ I_2^NW(□)`. The
    reductions are proof sketches in the text; the thresholds are exact
    certificates (artifact/certificates/exponent). Fitted constants are not
    claimed.
17. **Lemma 7.2, Lemma 7.3 (bilocal inequality), Corollary 7.4, Theorem 7.5
    (five-path).** Every `P_5`-compatible law with positive endpoint cells obeys
    `√|I| + √|J| ≤ 1`; `d_TV(P_h, C_{P_5}) ≥ h/96`; `P_{h_t} ∈ I_t^exp(P_5)` for
    `h_t = 1/(16t²)` with a strictly positive rational witness; hence
    `H_t^H(P_5) ≥ 1/(1536 t²)`. Analytic (distance constant corrected from the
    packet's `h/16`); exact certificate at small orders.

## The triangle defect family (Sections 8–13)

18. **Theorem 8.1 (membership).** `Q(ε,r) = ε δ_000 + (1−ε) Bern(r)^{⊗3}` with
    `0 ≤ r ≤ (1−ε)^{t−1}` lies in `I_t^exp ⊆ I_t^AI ⊆ I_t^NW`. Analytic; exact
    at `t = 1,2,3`; Lean for NW and AI.
19. **Theorem 8.2 (Theorem C).** `P_t = Q(ε_t, r_t)`, `ε_t = 1/(2t³)`,
    `r_t = (1−ε_t)^{t−1}`: `P_t ∈ I_t^exp` and
    `P_t(000)² − P_{t,A}(0)P_{t,B}(0)P_{t,C}(0) ≥ ε_t²/2`. Quantifiers `∀t ∃P_t`.
    Corollary 8.3: any observed alphabets `≥ 2`. Lean (`no_finite_characterizing_order`,
    finite-latent compatible set; measure-theoretic Finner in `FinnerMeasure.lean`).
20. **Lemmas 8.4–8.11.** Disjoint-ancestry independence; copied-triangle law;
    symmetry; Finner for arbitrary latent spaces; explicit violation; diagonal
    law; latent projection; recursive expressible prescriptions.
21. **Theorem 9.1 (fan inequalities).** `t z ≤ a + C(t,2) bc` and
    `t(z² − abc) ≤ az − abc` for every order-`t` NW-feasible law; explicit
    rejecting order for every Finner violation. Lean.
22. **Proposition 9.2.** `R_p` incompatible with `t_min = 2` at every distance. Lean.
23. **Proposition 10.1 (sharp exponent along `P_ε`).**
    `1/2 ≤ liminf ε^{1/3} t_min ≤ limsup ≤ 4 − 2√3`; exponent proved, constant
    not. Finite bounds in Lean.
24. **Theorem 11.1, Corollary 11.2 (distance asymptotics).**
    `d_TV(P_ε, C_△) = (1 − 2^{-3/2})ε + O(ε^{4/3})`; `t_min = Θ(d_TV^{-1/3})` along
    `P_ε` only. Analytic.
25. **Corollary 12.1 (distance-promised order).** `t_min ≤ ⌊(1−‖P‖²)/δ_2²⌋ + 1
    ≤ ⌊(K−1)/(4δ²)⌋ + 1` for every correlation scenario, from the convex-order
    theorem (now stated in that generality); NW's `L`-dependent collision
    estimate is superseded. Triangle case in Lean.
26. **Proposition 13.1 (bit-length law).** Worst first rejecting order over
    `B`-bit rational three-bit laws is `2^{Θ(B)}`. Analytic.

## Supporting results (Appendix C)

27. Square rare-selector family with exact first rejection `t² − t + 2`
    (Propositions C.1–C.6); defect ceiling `4/(27n³) + O(n^{−4})` and the iid-cell
    and ternary `Θ(n^{−3})` ceilings (C.7–C.11); parity extraction and the
    identity-transfer theorem (C.12–C.14). Stated with proofs or proof sketches
    from the packet sources; the appendix says which finite checks the packet
    ran and that these results are not used by Theorems A–C.

## Computational content

28. Exact rational certificates: defect cube at `t = 1,2,3`; sparse order-two
    table; negative control; order-two Farkas calibration; fan certificates
    (14 targets, all-order polynomial identity, 174,760 assignments, 271,500
    count orbits, 2,660 embeddings, 8 negative controls); classification
    certificates for the cycle, square, triangle and path witnesses at small
    orders and the square low-order LP certificates (`artifact/certificates/classification/`;
    status in `RELEASE_STATUS.md`). The proofs do not depend on them.

Added 2026-09-14 (campaign):
- **Lemma 6.6 (quantitative parity rigidity).** For every triangle-compatible `R`, `max{E A, E B, E C} ≥ −4(1 − E[ABC])`. Replaces the parity-repair lemma; gives Lemma 6.7 with `q/10`, Theorem 6.8 with `11/(640 m² t²)`, Corollary 6.15 with `27/(5120 t)`, Proposition C.1 with `τ/10`. Lean-proved (`CycleModelAux.quant_rigidity`).
- **Lemma 6.20 (NW form of the count-moment reduction) and Lemma 6.21 (monotonicity along the parity direction).** Proof sketches in the text; assumed by the threshold verifier.
- **Proposition 6.22 (parity thresholds at orders ≤ 10).** Certified brackets for `q^AI_t`, `q^NW_t` on the square and the triangle; even/odd separation pattern; exact values `2−√3`, `1/5`, `1/7`, root of `q³−33q²+27q−3`; chain `NW_3 ⊊ AI_2 ⊊ NW_2`. Exact certificates; not formalized. Fitted constants and the `t ≥ 11` numerics are NOT claimed.
