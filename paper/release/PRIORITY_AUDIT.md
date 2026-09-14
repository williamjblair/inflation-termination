# Priority audit

Audit date: 2026-09-12; public literature through this date. Sources were
read from primary text where possible (NW arXiv LaTeX and published PDF; WSF
LaTeX; Renou et al. LaTeX). Raw findings with verbatim quotations:
`release/PRIORITY_FINDINGS_raw.md`; verified bibliography with audit tags:
`release/references_with_audit_notes.bib`. Search absence does not certify
firstness. Addendum 2026-09-13: Gitton's 2025 ETH thesis was obtained in full
(DOI 10.3929/ethz-b-000745278, 238 pages) and swept by literal keyword search;
the 2023–2026 sum-of-squares bit-size literature and arXiv:2507.15632 were swept from primary text.
The theses of Wolfe, Pozas-Kerstjens and Fraser were still not obtained.

| source | exact theorem / result | overlap | difference | priority implication | citation required |
|---|---|---|---|---|---|
| Navascués–Wolfe 2020 §4.1 Open Question | asks whether for every scenario some finite order solves exact compatibility; names the triangle | poses the question we answer | none | NO_MATCH (question, not answer) | yes |
| Navascués–Wolfe 2020 §4.1, optimization non-termination | for approximate causal *optimization* in the one-variable scenario the order-n relaxation of `min −P(0)P(1)` overshoots `−1/4` at every n | same shape ("no finite termination"), same authors, same page | different problem (optimization vs compatibility), unconstrained scenario, an inflation law overshooting rather than an incompatible observed law; cannot become a compatibility counterexample | PARTIALLY_OVERLAPPING; **strongest predecessor** | yes, prominently |
| Navascués–Wolfe 2020 §4.1, `P_v` family | binary `P_v` (v on 111, uniform elsewhere) passes order-2 triangle inflation; Finner excludes `v > 57/64` | template of the construction at t = 2 | one fixed order; no hierarchy conclusion; our family and the uniform-in-t proof are new | PARTIALLY_OVERLAPPING | yes |
| Navascués–Wolfe 2020 Thm 1, (A7), closedness | asymptotic completeness; ℓ¹ de Finetti bound `2(1 − ∏(1−x/n)^L)` | the "complete in the limit" half; input to Prop. 3.5 | — | SUBSTANTIALLY_PRECEDED for Prop. 3.5 (credited as their theorem with explicit constants) | yes |
| Wolfe–Spekkens–Fritz 2019 | inflation technique; injectable / AI-expressible / expressible sets (Def. 7); effectivity remark ("not clear how to upper bound"); `∃P ∀G'` completeness question | definitions used verbatim; effectivity question ancestor | their completeness question has the opposite quantifier and is answered by NW | PARTIALLY_OVERLAPPING | yes |
| Finner 1992 | generalized Hölder inequality | the incompatibility tool | our margin computation only | CLEARLY_PRECEDED (inequality) | yes |
| Renou et al. PRL 2019 | triangle form `P(abc) ≤ √(P_A P_B P_C)`, classical via two Cauchy–Schwarz or Loomis–Whitney; non-star-convexity | the exact inequality used | — | CLEARLY_PRECEDED (inequality) | yes |
| Rosset–Gisin–Wolfe 2018 | finite latent cardinality; compatible sets closed and semialgebraic | closedness (quantifier form); decidability and in-principle computability of a rejecting order | — | PARTIALLY_OVERLAPPING; forces the effectivity question to be stated as *explicit* effectivity | yes |
| Weilenmann–Budroni–Navascués 2025 | no membership test for non-convex sets in the non-iid regime; triangle named | bears on the strong-converse sequel, not on this paper | — | UNRESOLVED for the sequel; cited here for scope of Sec. 9 | yes |
| Girardin–Gisin 2023 | four-output NSI triangle box violating Finner and passing polygon NSI inflations through the enneagon | closest finite-order analogue | different hierarchy and resource; finitely many levels | NO_MATCH (analogue) | yes |
| Fraser–Wolfe 2018; Gitton 2022; Gitton et al. 2025 (EJM); Boghiu et al. 2023; da Silva et al. 2025; Pozas-Kerstjens et al. 2023 | finite-order triangle inequalities, selected witnesses, software, symmetry reduction, minimal-triangle models | finite orders only | no all-order family | NO_MATCH | courtesy |
| Wolfe et al. 2021 (quantum inflation); Ligthart–Gachechiladze–Gross 2023; Ligthart–Gross 2023 | quantum hierarchies: incompleteness via undecidability; convergent variants | different mechanism | quantum | NO_MATCH | courtesy |
| Nie 2014; NPA 2008; Christandl et al. 2007 | finite convergence of SOS hierarchies only under optimality conditions; NPA convergence; finite de Finetti | analogy of shape | different objects | NO_MATCH | optional |
| Tavakoli et al. 2022 review | presents classical inflation as asymptotically complete | framing | full text not examined for an explicit "finite order open" sentence | UNRESOLVED-minor | courtesy |
| Wolfe–Spekkens–Fritz 2019 §IV.D eqs. (59)–(61), (43) (tautology + union bound → marginal inequalities); Fraser–Wolfe 2018 wagon-wheel/web inequalities | the fan inequality `Σ_k A B_k C_k ≤ A + ½Σ_{k≠l} B_k C_l` is a certificate of exactly this kind; fixed small inflations only | method and graph | no published closed-form family indexed by copy count; no second-moment (Cauchy–Schwarz) inflation bound located; Gitton–Renner 2025 state that analytic pen-and-paper inflation arguments are open | PARTIALLY_OVERLAPPING (method preceded; t-indexed family and rejecting-order corollary new) | yes |
| Gisin–Mei–Tavakoli–Renou–Brunner 2020 (Nat. Commun. 11, 2378; arXiv:1906.06495), Supp. App. 3 | a two-parameter family is Finner-incompatible iff `q > 1 + p − 2p^{2/3}`: the same 2/3-power boundary shape | the `ε^{2/3}` marginal scale along `P_ε` | no rejecting-order growth, no distance asymptotics, no `1−2^{-3/2}` constant; NSI setting | PARTIALLY_OVERLAPPING (boundary shape); NO_MATCH (asymptotics) | yes |
| Diaconis–Freedman 1980 (finite exchangeable sequences) | the without-replacement de Finetti rates `k/n`, `k(k−1)/n` and their unimprovability | the collision rate behind NW (A7) and Prop. 7.1 | — | tool; cite | yes |
| O'Donnell 2017; Raghavendra–Weitz 2017 (SOS bit complexity) | relaxation hierarchies can require exponential bit size / level in the input | Prop. 8.1 is a transfer of this phenomenon to inflation | different hierarchy and objects | NO_MATCH (analogy; cite as prior art in spirit) | yes |
| Gitton 2022 Thm 8; Ligthart–Gachechiladze–Gross 2023 | convergence of postselected inflation (rate "likely not tight"); convergent quantum hierarchy without rate | no order-vs-distance law | — | NO_MATCH | courtesy |
| Steudel–Ay / WSF Example 1; Rosset–Gisin–Wolfe App. C | incompatibility of the perfectly correlated law (`R_{1/2}`) | `R_p` incompatibility is classical | uniform-in-p rejecting order 2 is the only new content | CLEARLY_PRECEDED (incompatibility) | yes (WSF, RGW) |
| da Silva–Pozas-Kerstjens–Parisio 2025 (v2) | local models and low-order inflation for the minimal triangle; conjectural boundary criteria | same scenario | no growth-of-order statement | NO_MATCH | courtesy |
| Gitton 2025 ETH thesis (Diss. ETH No. 30974; full text, 238 pp.) | general inflation framework with identical-party constraints; generalized de Finetti theorem; convergence of inflation relaxations with an `O(1/z)` squared-`ℓ²` error (Thm 5.4, eq. (5.51)); triangle symmetry reduction; exact integer certificates; Frank–Wolfe; shared-random-bit and EJM applications | asymptotic completeness with a rate (same family of statements as NW Thm 1 / Prop. 7.1) | literal sweep for "finite order", "no finite", "every order", "arbitrarily high", "asymptotic", "terminat", "counterexample", "Hausdorff", "bit size", "exponential", "1/3", "defect": zero hits for an all-order nontermination statement, a rejecting-order growth law, a distance-to-boundary asymptotic, or a bit-length law; "Finner" appears only in the bibliography (Girardin–Gisin); the convergence chapter states that improved rates from additional constraints are unknown | NO_MATCH for Theorems A, B and Props. 6–8; PARTIALLY_OVERLAPPING for the quantitative convergence (cite alongside NW) | yes (courtesy, Sec. 9) |
| Raghavendra–Weitz 2017; Gribling–Polak–Slot 2023 (arXiv:2305.14944); Vargas 2024 (arXiv:2401.12613); Bortolotti–Mastrolilli–Vargas 2025 (arXiv:2504.17756); Bortolotti–Mastrolilli–Palomba–Vargas 2025/26 (arXiv:2509.06928; SIAM J. Discrete Math., DOI 10.1137/25M1796576) | exponential coefficient bit size at fixed SOS degree and sufficient conditions for bounded bit size; polynomial-time computability of a fixed moment-SOS level; NP-hardness of deciding finite convergence of Lasserre hierarchies (already for standard quadratic programs); automatability criteria extended to refutations; symmetric Archimedean formulations admit low-bit-size low-degree proofs, separating degree from bit size | same phenomenon class (level or coefficient size exponential in the input) | these results concern coefficient bit complexity at a given degree, the cost of computing a fixed level, or the decidability of eventual stabilization; none states a first-rejecting-level law `2^{Θ(B)}` in the input length for inflation or for any causal-compatibility hierarchy; the symmetric-formulation result shows that symmetry can force degree without forcing bit size, which is consistent with Prop. 8.1 rather than a predecessor of it | NO_MATCH (analogy class; cite) | yes |
| Levin–Chandrasekaran, arXiv:2507.15632v2 (2025), "Any-dimensional polynomial optimization via de Finetti theorems" (full text swept 2026-09-13) | any-dimensional polynomial problems via representation stability; new de Finetti-type theorems for sequences of random arrays with explicit convergence rates; sum-of-squares bounds for mean-field games, symmetric functions, graph homomorphism densities | shares the finite de Finetti tool family with NW Thm 1 / Prop. 7.1 | zero occurrences of "inflation", "causal", "Navascués", "Finner", "rejecting", "exponential", "finite convergence", or any bit-length statement; "triangle" appears only as a graph in Ramsey multiplicity; no causal-compatibility hierarchy, no first-rejecting-level law | NO_MATCH | no |
| arXiv sweep 2023–2026 ("does not terminate", "no finite inflation level", "false positives at every level", triangle/binary/asymptotic) | only per-distribution asymptotic completeness statements | — | — | NO_MATCH | — |

## Overall

`PRIORITY_STATUS = PRIORITY_NOT_KILLED; no predecessor located for Theorem A or for the t-indexed fan family, the sharp exponent, the distance asymptotics, or the bit-length law; the fan method (WSF), the general bound (NW Thm 1/(A7), Diaconis–Freedman), the 2/3-power boundary shape (Gisin et al. 2020) and the exponential-level phenomenon (SOS literature) are preceded and cited; firstness not certified and still subject to specialist review. Addendum 2026-09-13: Gitton's 2025 ETH thesis retrieved and swept in full text; no matching all-order nontermination, rejecting-order growth, distance-asymptotic or bit-length theorem located. The SOS/Positivstellensatz bit-complexity literature was swept through Raghavendra–Weitz 2017, Gribling–Polak–Slot 2023, Vargas 2024, Bortolotti–Mastrolilli–Vargas 2025 and Bortolotti–Mastrolilli–Palomba–Vargas 2025/26; these address coefficient bit complexity, automatability, degree, or finite-convergence decision complexity, not a first-rejecting-order law in the input length. arXiv:2507.15632 (Levin–Chandrasekaran, any-dimensional polynomial optimization via de Finetti theorems) swept in full text on 2026-09-13: no causal or inflation content; NO_MATCH. Remaining unswept: the theses of Wolfe, Pozas-Kerstjens and Fraser.`

`STRONGEST_PREDECESSOR = Navascués–Wolfe 2020: §4.1 (optimization non-termination; order-2 P_v/Finner example) for Theorem A, and Theorem 1 with eqs. (33)–(37), (A7) for the general distance bound.`

Mandatory attributions carried into the manuscript: NW's question, their
optimization non-termination and their `P_v` example (Sections 1, 7, 8);
Finner and Renou et al. for the inequality (Sections 2, 5, 8); WSF for the
definitions (Section 2); RGW for closedness/semialgebraicity and its
consequence for effectivity (Sections 2, 7, 10); WBN for the scope of any
strong-converse statement (Section 8).

Findings about claims outside this paper (recorded for the sequel): the
qualitative faithfulness biconditional is NW's completeness restated as a
gauge and must be framed as a quantitative refinement; the strong converse must
define its class of block laws against Weilenmann–Budroni–Navascués; NW's `D`
is ℓ¹ and any imported modulus must track the factor two.

## Addendum 2026-09-13 (evening): the pair-source packet

No literature sweep has been run for the packet results. The rows below record
what must be checked before any release, and the known predecessors that the
manuscript already cites. Status for every row: TARGETED_REVIEW_REQUIRED.

| result | known ingredients (cited, not claimed) | what a targeted sweep must look for |
|---|---|---|
| pair-source termination classification (Thm 4.2) | NW 2020 star termination at order two; WSF 2019 definitions; Rosset–Gisin–Wolfe closedness | any published statement that a scenario class terminates or fails to terminate at a finite inflation order; "double-star", "caterpillar of diameter three", "bilocal"/"path" nontermination |
| root-sink lemma (`exp = AI` on pair-source scenarios) | WSF 2019 Def. 7 (expressible sets); d-separation in the inflation DAG | whether WSF or later work already observes that the recursive closure adds nothing on scenarios without observed parents |
| double-star reconstruction (Thm 5.1) | NW 2020 §4.1 (stars) | any order-two reconstruction argument for trees |
| five-path witness and bilocal inequality (Thm 7.5, Lemma 7.3) | Branciard–Rosset–Gisin–Pironio 2012 (bilocal inequalities); Tavakoli et al. 2022 review | inflation nontermination statements for the bilocal or `n`-local chain scenarios; explicit `√|I|+√|J| ≤ 1` forms with settings given by observers |
| cycle parity witnesses (Thm 6.8) and rigidity (Lemmas 6.5–6.6) | Boreiri–Ulu–Brunner–Sekatski 2025 (rigidity of parity-perfect correlations); parity/GHZ-type triangle distributions | parity-based inflation witnesses at all orders; Fourier-density constructions of symmetric inflation tables |
| corrected density and `Θ(1/t)` rates (Lemma 6.10, Thms 6.11–6.12) | none located | quantitative lower bounds on the distance of accepted laws to the compatible set |
| convex-order bound (Thm 6.16) | NW 2020 Thm 1/(A7); Diaconis–Freedman 1980; Gitton 2025 thesis Thm 5.4 (`O(1/z)` squared-`ℓ²` error) | a source-independent `√(K−1)/(2√n)` bound or a convex-order statement for inflation diagonals (Gitton's rate may already be source-independent: check the constant) |
| order conversion on the square (Thm 6.18) | none located | comparisons of NW and AI orders |
| low-order thresholds (Prop. 6.20) | Pozas-Kerstjens et al. 2023 (inflation software with symmetry reduction) | published order-two or order-three square parity thresholds |
| supporting results (Appendix C) | Shearer 1985; MacWilliams–Sloane 1977 | rare-selector or matching-based inflation witnesses; defect-ceiling asymptotics |

`PRIORITY_STATUS` for the packet results: NOT_SWEPT. The overall status line
above applies only to the former manuscript (Sections 8–13).

## Addendum 2026-09-14: targeted sweep for Sections 3–7 (pair-source classification, brackets, witnesses)

Full table with verbatim quotations and verified bibliographic data:
`research/2026-09-14/priority/PRIORITY_SWEEP_SECTIONS_3-7.md` (22 primary full texts plus the
arXiv abstract corpora for "causal compatibility" and "inflation technique", 2023–2026).

| result | verdict | strongest predecessor | action taken in the manuscript |
|---|---|---|---|
| Theorem 4.2 (termination classification), Theorem 5.1 | PARTIALLY_OVERLAPPING | Navascués–Wolfe 2020 §4.1: "This example can be generalized to prove convergence at order n=2 of any star-shaped correlation scenario" (the diameter-≤2 case) | cited; the four-on-line scenario of NW Fig. 8, which they leave open, is named at Corollary 5.3; Henson–Lal–Pusey 2014 cited as the prior classification enterprise (different criterion, parts from ours at diameter 3) |
| Lemma 3.9 (exp = AI on root-sink scenarios) | NO_MATCH | WSF 2019 "leave the investigation of more general expressible sets to future work"; their strict-gap example lies outside the root-sink class | recorded in Section 14 |
| Theorems 6.8, 7.5 (all-order cycle and path witnesses), Lemma 6.10 | NO_MATCH | — | — |
| Theorem 6.16 (convex-order bound, source-free constant) | PARTIALLY_OVERLAPPING (shape n^{-1/2} is NW Thm 1; Gitton 2022 Thm 8 constant carries S_c(S_c − 1/2); Fraser 2020 rate carries LC) — the 2026-09-13 open check "is Gitton's rate source-independent?" is resolved: NO | Gitton 2022 Thm 8, Fraser 2020, Hoeffding 1963 Thm 4 cited in Section 14 |
| Theorem 6.18 (order conversion), Proposition 6.20 (second-order separations) | NO_MATCH | — | — |
| Lemma 6.5 (exact parity rigidity) | CLEARLY_PRECEDED | Boreiri, Girardin, Ulu, Lipka-Bartosik, Brunner, Sekatski, PRA 107, 062413 (2023) — previously mis-attributed to the 2025 Quantum paper | attribution corrected in Sections 6 and 14 |
| Lemma 6.6 (parity repair) | SUBSTANTIALLY_PRECEDED | Boreiri–Ulu–Brunner–Sekatski, Quantum 9, 1830 (2025), Result 2, with the tighter constant 3ε | the manuscript now says so; the difference is generality (arbitrary latent alphabets, stochastic responses) |
| rigidity on cycles | PARTIALLY_OVERLAPPING | Renou–Beigi, PRA 105, 022408 (2022) §IV (token counting on all ring scenarios; integer counts, not parity) | cited in Sections 6 and 14 |
| Lemma 7.3 (bilocal inequality) | CLEARLY_PRECEDED | Branciard–Rosset–Gisin–Pironio 2012 | already cited |

Not accessed: Gitton 2025 ETH thesis (Research Collection HTTP 500 on 2026-09-14; its arXiv
predecessor 2202.04103 swept in full instead); theses of Wolfe and Pozas-Kerstjens. arXiv API
rate-limited; the 2023–2026 sweep used the HTML search (titles and abstracts).

`PRIORITY_STATUS (Sections 3–7) = PRIORITY_NOT_KILLED; no predecessor for the classification
beyond stars, the root-sink collapse, the all-order witnesses, the Θ(1/t) lower bounds, the
source-free convex-order constant, the order conversion or the second-order separations;
preceded and now cited: star termination (NW), parity rigidity (Boreiri et al. 2023) and its
noise-robust form (Boreiri et al. 2025, tighter constant), ring token-counting rigidity
(Renou–Beigi 2022), the n^{-1/2} rate family (NW, Gitton, Fraser), Hoeffding's convex-order
domination, HLP's classification. Firstness not certified.`
