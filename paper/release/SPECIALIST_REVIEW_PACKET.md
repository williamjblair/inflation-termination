> Historical audit retained from before the editorial revision. For current section numbers, corrections, deferred results and validation, see `paper/review/EDITORIAL_REVIEW.md` and the opening update in `RELEASE_STATUS.md`.

# Specialist review packet

Manuscript: `paper/main.tex` (title: *Inflation for Classical Pair-Source
Networks: Termination and Quantitative Obstructions*; the packet of
2026-09-13 added Sections 3–7 and Appendix C, see `CLAIMS.md`; this review
packet still describes the triangle results, now Theorem C and Sections 8–13,
with their former numbering in parentheses). Certificates: `artifact/`.
Audits: `release/`.

## 1. Theorems (one page)

Classical triangle: independent latent `X,Y,Z`; observed `A = A(X,Z)`,
`B = B(X,Y)`, `C = C(Z,Y)`, arbitrary stochastic responses; `C_△` the compatible
laws on three bits. Order-`t` Navascués–Wolfe test: a law `Γ_t` on the `3t²`
copied observations `A^{ij}, B^{ik}, C^{jk}`, invariant under `S_t³` acting on
the three index families, with `Law((A^{ll}, B^{ll}, C^{ll})_{l=1..t}) = P^{⊗t}`.
`I_t^AI` adds products on ancestrally independent injectable sets; `I_t^exp`
adds the recursive expressible-set prescriptions. `Bern(r)(1) = r`.

**Theorem A (3.2).** For every `t ≥ 1`, `P_t = ε_t δ_000 + (1−ε_t) Bern(r_t)^{⊗3}`,
`ε_t = 1/(2t³)`, `r_t = (1−ε_t)^{t−1}`, lies in `I_t^exp ⊆ I_t^AI ⊆ I_t^NW` and
violates Finner by `≥ ε_t²/2`. No finite order characterizes triangle
compatibility, for any observed alphabets `≥ 2`.

**Theorem B (5.1 with 4.1, 6.1).** Along `P_ε = ε δ_000 + (1−ε) Bern(1−ε^{2/3}/2)^{⊗3}`,
`1/2 ≤ liminf ε^{1/3} t_min^H ≤ limsup ε^{1/3} t_min^H ≤ 4 − 2√3` for
`H ∈ {NW, AI, exp}`; `d_TV(P_ε, C_△) = (1−2^{-3/2})ε + O(ε^{4/3})`; hence
`t_min = Θ(d_TV^{-1/3})` along this direction. Fan inequalities: every
order-`t` feasible law obeys `t z ≤ a + C(t,2) bc` and `t(z²−abc) ≤ az−abc`.
General bound `t_min ≤ ⌊LK/(4δ²)⌋+1`; worst order over `B`-bit rational inputs
`2^{Θ(B)}`; `R_p` has `t_min = 2` at every distance.

## 2. Open-question mapping

NW 2020 §4.1 (boxed Open Question and the framing paragraph naming the
triangle): Theorem A is its negation at the named scenario in the only
possible quantifier form (`release/OPEN_QUESTION_AUDIT.md`, verbatim text).
NW's own §4.1 contains the order-2 `P_v`/Finner example and the optimization
non-termination proof; both are cited as the closest precedents.

## 3. Hard family

Defect cube: iid `D_ijk ~ Bern(ε)` on `[t]³`, private bits, `A^{ij} = 1{N=0, D_ijk=0 ∀k}`
etc.; copied triangle law `Q(ε,r)`; diagonal supports `R_l` (cells with ≥ 2
coordinates `= l`) mutually disjoint; index permutations permute iid bits.

## 4. Eight proof obligations

1. **All-order hard-family passage** (Sec. 3.1–3.3): copied-triangle law by
   conditioning on `D_ijk`; mutual (not pairwise) disjointness of `R_1..R_t`;
   `S_t³` covariance; injectable ⊆ copied triangles; AI products from disjoint
   inputs; recursive expressibility via latent-projection containment and Markov
   transfer of d-separations; zero-mass branch of WSF Definition 7.
2. **Finner incompatibility** (Lemma 3.7–3.8): two Cauchy–Schwarz steps with
   Tonelli, arbitrary latent spaces and kernels; `ε_t² − t³ε_t³ = ε_t²/2`.
3. **NW indexing identity behind the fan theorem** (Sec. 4): `E[B_k C_l] = bc` for
   `k ≠ l` from `X_1→1, Z_1→2, Y_k→1, Y_l→2` (extended arbitrarily to `[t]`) and
   the degree-2 diagonal law on `(Δ_111, Δ_222)`; `E T_k = z`, `E A = a` from the
   degree-1 law. Check that no product prescription on non-diagonal sets is
   used, and that the identity is never applied at `k = l`.
4. **Fan inequality** (Thm 4.1): pointwise `Σ_k A B_k C_k ≤ A + ½ Σ_{k≠l} B_k C_l`
   via `Σ B_k ≥ S`, `Σ C_k ≥ S`, `½(S−1)(S−2) ≥ 0`; second-moment form via
   `(EU)² ≤ E A · E U²` and `T_k T_l ≤ B_k C_l`; the cyclic minimum and the
   `≥ 1` ratio remark.
5. **Asymptotic `ε^{-1/3}` upper bound** (Prop. 5.1): expansion
   `v_t = (x − 1/2 − x²/8) ε^{2/3} + O(ε)`; roots `4 ± 2√3`; exact finite bound via
   `D ≥ 5ε²/32` and root gap `≥ (4√10/9) ε^{-1/3} > 1`, `v_1 < 0`.
6. **Distance asymptotics** (Thm 6.1): Finner lower bounds for TV and ℓ₂
   (`√(8/7)` from the zero-sum vector); the compatible model (base bits `√u`,
   flags `hε`, `u = σ + (2^{-3/2} + h)ε`, `h = (1−2^{-3/2})/7`) with atoms
   `u^{3/2}`, `u − u^{3/2}`, `0`, `1 − 3u + 2u^{3/2}` before flags; the `O(ε^{4/3})`
   remainders.
7. **Semialgebraic bit-length upper bound** (Prop. 8.1): compact semialgebraic
   parameter space (RGW finite cardinality); fixed quantifier-free description
   of the graph of `u = ‖P − C_△‖_2²`; some atom vanishes at the single point
   `u(P)`; root lower bound `1/(H+1)` with `H = 2^{O(B)}`; Prop. 7.1. Lower bound
   from `P_ε` at `ε = 2^{-3j}` (`O(j)` bits, `t_min > 2^{j−1}`).
8. **No hidden AI assumption in the NW statements**: Theorem A's NW membership
   (Sec. 3.3), the fan identities (Sec. 4), and Prop. 7.1's sampling argument
   (deterministic tables are valid responses; `L` without private roots) use
   only symmetry and diagonal laws; the AI/expressible conclusions are proved
   separately and are stronger, not assumed.

## 5. Reproduction

    cd artifact
    python3 -B verifiers/run_replay.py         # nontermination (frozen+hardened), Farkas, fan (normal, -O), independent fan recheck
    python3 -B verifiers/mutation_tests.py     # 26 scenarios (frozen -O defect documented)
    python3 -B verifiers/mutation_tests_fan.py # 13 scenarios
    python3 -B verifiers/make_manifest.py

## 6. Closest predecessors

NW 2020 (question, completeness, (A7), `P_v`, optimization non-termination);
WSF 2019 (hierarchy; logical-tautology certificates, the method behind the
fan inequality); Finner 1992 / Renou et al. 2019 (the inequality); RGW 2018
(closedness, semialgebraicity, decidability); Girardin–Gisin 2023 (finite-order
NSI analogue); da Silva et al. 2025 (minimal-triangle boundary work).

## 7. Non-claims

See `NONCLAIMS.md`.

## 8. Open questions left

Exact constant along `P_ε`; worst-case Hausdorff exponent (`n^{-3}` vs
`n^{-1/2}`); finite-stabilization classification; quantum analogue; tariff
computability (Section 10).
