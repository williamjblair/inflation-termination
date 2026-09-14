# Open-question audit

Primary sources read in full: arXiv:1707.06476v3 LaTeX source and the
published Journal of Causal Inference typesetting (verbatim extracts in
`release/OPEN_QUESTION_FINDINGS_raw.md`).

| field | content |
|---|---|
| source | M. Navascués, E. Wolfe, *The Inflation Technique Completely Solves the Causal Compatibility Problem*, J. Causal Inference 8 (2020) 70–91, §4.1 "On finite-order convergence", p. 82 |
| exact question (framing paragraph, verbatim) | "For arbitrary correlation scenarios 𝒢 with observed variables of specified cardinality, we inquire whether *some* finite-order inflation is always sufficient to characterize the set of compatible distributions. Are there causal structures for which inflation converges only asymptotically? Could the triangle scenario be such an example?" |
| exact question (boxed, verbatim) | "**Open Question.** For any correlation scenario 𝒢, does there exist n such that nth-order inflation solves exact Causal Compatibility?" |
| formalization | `NW-OQ(𝒢): ∃n ∀P (P ∈ I_n(𝒢) ⇒ P ∈ C(𝒢))`; negation `∀n ∃P (P ∈ I_n(𝒢) ∧ P ∉ C(𝒢))` |
| our theorem | For 𝒢 = triangle with binary (hence any ≥2) observed alphabets: `∀t ∃P_t ∈ I_t^NW \ C_△`, explicit `P_t`, explicit Finner margin `ε_t^2/2`; also `P_t ∈ I_t^exp ⊆ I_t^AI` |
| logical implication | Our theorem is literally `¬NW-OQ(triangle, d=2)` with the existential witnessed constructively. A universally quantified question is settled by one scenario. |
| fully answers? | **Yes**, for the triangle: the boxed question receives the answer "no, not for every 𝒢"; the three natural-language questions receive "not always", "yes, there are", "yes, the triangle is such an example". |
| partially answers? | The boxed question quantifies over all scenarios; we settle it by one counterexample and make no statement about other scenarios. |
| stronger/weaker? | Stronger in three respects: minimal cardinality (binary); explicit rational family with explicit margin; quantitative degeneration along `P_ε` (`ε^{-1/3}` ≤ growth ≤ `84/ε`). Also holds for the stronger AI and recursive-expressible tests, which NW deliberately do not impose. |
| scope mismatch? | None found. Three notes stated in the manuscript: (i) "n-th order inflation" in NW imposes diagonal conditions of every degree ≤ n; the degree-t condition implies the lower ones by marginalization (App. A); (ii) NW's indexing `A(U_1^i,U_2^j), B(U_2^i,U_3^j), C(U_3^i,U_1^j)` is the same object as ours up to relabelling (Sec. 2); (iii) NW's `D` is the ℓ¹ distance (twice TV) — the constants in Prop. 3.5 are stated in the ℓ¹ convention where imported and converted explicitly. |
| adjacent NW results that must be cited | (a) the order-2 binary family `P_v` passing second-order triangle inflation and refuted by Finner for `v > 57/64` — template of our construction; (b) non-termination of inflation for approximate causal *optimization* in the one-variable scenario — a different problem in an unconstrained scenario; (c) Theorem 1 / (A7) and closedness (Rosset–Gisin–Wolfe) — which exclude a single all-orders witness and fix the quantifier form. |
| what NW did not ask | An effective bound on the rejecting order as a function of `P` (closer to a remark of Wolfe–Spekkens–Fritz); the `∃P ∀G'` completeness question of WSF, which their own added-in-proof paragraph records as answered by NW. |
| convention check | The Finner margin `≥ ε_t^2/2` was rechecked in exact rational arithmetic for `t ∈ {1,…,200}` during the audit; it holds only for `Bern(r)(1) = r`, which the manuscript now states explicitly. |
| equation-number check | "(16)–(19)" and "(A7)" are correct in the published numbering; the arXiv build numbers the test (17)–(20). The manuscript cites the published numbering and notes the difference. |

## Update 2026-09-13

| field | content |
|---|---|
| our theorem (after the packet) | For every pair-source scenario `G` (finite simple graph, binary observed variables): `NW-OQ(G)` holds iff every component of `G` is a double-star, with `n = 2`; otherwise `∀t ∃P_t ∈ I_t^exp(G) \ C_G`, strictly positive rational (Theorem 4.2). |
| fully answers? | The boxed question is answered "no" (as before, by the triangle) and, within the pair-source class, the finer question "for which `G`" is answered completely. The star case (`NW-OQ` true at `n = 2`) is NW's own Section 4.1 result and is cited as such. |
| what remains | Scenarios with a source shared by three or more observed variables, and DAGs with observed parents, are not classified (Remark 4.5, Question 15.4). |
| convention check | The classification and the witnesses use signs `±1` with `+1 ↔ 0`; the cycle and path witnesses are stated with rational flip probabilities so that every witness is strictly positive. |

