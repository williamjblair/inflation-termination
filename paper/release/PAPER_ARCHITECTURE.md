# Additions of 16 September 2026

A ninth main section, Section 7 (sources shared by three or more observers), now follows Section 6; open problems and verification are Sections 8 and 9. Section 6 gains Subsection 6.3 (explicit rejecting orders for parity violations), Section 4 gains Proposition 4.12 with its proof in Appendix B.4, and Lemma 4.2 carries the sharper constant. The PDF has 62 pages, 46 of main text. See `paper/review/ADDITIONS-2026-09-16.md`.

---

# Current architecture — 15 September 2026

The paper has eight main sections:

1. Introduction: contributions, literature comparison and reading guide.
2. Pair-source scenarios and inflation: one general setup, followed by the triangle example.
3. Termination classification: theorem, structural tools, reduction, reconstruction, cycle and five-path obstructions.
4. Quantitative convergence: corrected densities, distance lower bounds, convex-order upper bound, order conversion and finite separations.
5. Defect family: construction, incompatibility, passing prescriptions, fan rejection, exponent and distance.
6. Rejecting orders from distance and input size.
7. Open problems.
8. Verification and availability.

Appendix A supplies full root-sink and transport proofs and the triangle injectable characterization. Appendix B contains the order-conversion proof, count-moment reductions and certified threshold table. Appendix C documents certificates; Appendix D retains the supplementary inequalities and extraction arguments. Operational replay instructions are in `paper/review/VERIFICATION_GUIDE.md`.

The 49-page PDF has 35 pages of main text. Complete proofs and all eight figures are retained. This organization supersedes the plans below; their older theorem numbers and proposed bounds are historical.

---

> Historical audit retained from before the editorial revision. For current section numbers, corrections, deferred results and validation, see `paper/review/EDITORIAL_REVIEW.md` and the opening update in `RELEASE_STATUS.md`.

# Paper architecture

chosen_structure: OPTION 2 — focused flagship now; faithfulness / strong
converse deferred to a sequel. The flagship includes, besides the headline,
the elementary quantitative complements that share its proof vocabulary:
NW's asymptotic completeness as background, the rejection-order growth of the
single family (lower bound ε^{-1/3}/2, upper bound 84/ε), and the
distance-promised rejecting order max(2,⌈Ld/δ²⌉) as a one-page proposition
derived from NW's finite de Finetti estimate. The reverse-KL strong converse
and the regularized-faithfulness theorem are described in one paragraph of
the discussion, with no theorem statement, as the subject of a separate paper.

headline theorem: For every finite order t there is an explicit incompatible
binary triangle distribution P_t that satisfies the complete order-t
Navascués–Wolfe inflation test. Hence no finite inflation order characterizes
classical compatibility for the triangle (any observed alphabets of size at
least two), although the hierarchy is complete in the limit.

why split, not unified:
- Proof cores are disjoint. The headline is a two-page construction plus a
  Cauchy–Schwarz (Finner) separation and exact small-order certificates. The
  strong converse is a rectangular-box product inequality, conditional-KL
  bookkeeping and entropy transport over arbitrary block laws; faithfulness
  composes it with an LP-separation witness extracted from NW completeness.
  Nothing in the second core is used by the first, and vice versa.
- Reader overlap is partial. The headline is aimed at the causal-inference /
  network-nonlocality community that reads NW and WSF. The strong converse is
  an information-theoretic (hypothesis-testing, synthesis) statement whose
  natural referees and predecessors (van Dam–Gill–Grünwald statistical
  strength; Weilenmann–Budroni–Navascués memory attacks) are different.
- Length and legibility. A unified paper would run to 40+ pages with two
  notational systems (inflation tables vs. block laws, orbit contexts, root
  boxes) and would bury the one-sentence theorem the reader should remember.
- Priority profiles differ. The nontermination theorem maps exactly onto a
  published open question and has a clean bounded priority audit. The
  faithfulness family is graded B with a less settled predecessor question
  and benefits from its own audit before release.
- Conceptual complementarity is real but is served by a paragraph, not by a
  merged proof: "complete in the limit, not uniformly finitely terminating,
  and finite violations still carry quantitative force" is stated in the
  discussion with a forward reference.

proof overlap: NW's Theorem 1 / eq. (A7) (finite de Finetti closeness) is the
only shared ingredient; it enters the flagship as the "complete in the limit"
background and the distance-promised order, and enters the sequel as the
source of the finite witness.

reader overlap: both papers cite NW 2020, WSF 2019, Fritz 2012, Renou et al.
2019; the sequel additionally addresses information theorists.

publication-strength comparison: focused flagship — one memorable theorem,
short, elementary, fully self-contained, exact certificates, exact mapping to
a published question, ~15 pages: stronger. Unified — broader but diffuse,
harder to referee, headline diluted, and the second half not yet through its
own priority gate: weaker as a flagship.

what is deferred: strong converse compiler (Δ²/A² reverse-KL rate,
exponential TV separation, delivery strong converse); regularized
faithfulness γ_G(P)=0 ⇔ P ∈ C_G with the modulus δ⁴/(16d²[(t₀+1)t₀^L−t₀]);
the KL-promised rejecting order 24·4^k (mentioned, not proved here);
computability statements beyond one paragraph.

title chosen (2026-09-12): "Inflation for the Classical Triangle: Nontermination and Quantitative Complexity"
(alternatives in ARXIV_METADATA.md).

## Update 2026-09-13: reframing around the pair-source classification

The 2026-09-13 packet (research-handoffs/2026-09-13/claude-code) proves a
classification of finite termination for every pair-source scenario and
quantitative obstructions on the square, the triangle and the five-vertex
path. The manuscript is reframed accordingly, without dropping any triangle
result:

- Theorem A is now the classification (Section 4): a binary pair-source
  scenario admits a finite characterizing order iff every component is a
  double-star, and then order two suffices; the same for the AI and exp
  hierarchies, which coincide on pair-source scenarios (root-sink lemma).
- Theorem B is the pair of brackets `Ω(1/t) ≤ H_t ≤ O(t^{-1/2})` on the square
  and the triangle (Section 6), from the corrected Fourier density and the
  convex-order upper bound; plus the order conversion `NW_{⌊3t/2⌋} ⊆ AI_t ⊆ NW_t`
  on the square.
- Theorem C is the former Theorem A (the defect-cube family) with the former
  Theorem B (sharp exponent along `P_ε`) and its companions as Sections 8–13,
  presented with family-specific scope: the `Θ(d^{-1/3})` law belongs to one
  direction of approach and is not a worst-case rate.
- Section order: introduction; triangle hierarchies; pair-source setup;
  classification; double-star; cycles (with the rates); five-path; then the
  defect family sections; prior work; open problems; reproducibility;
  Appendix A (expressible sets), B (certificates), C (supporting results from
  the packet: rare-selector family, defect ceilings, parity extraction).
- Title: "Inflation for Classical Pair-Source Networks: Termination and
  Quantitative Obstructions".

Deferred material (strong converse, faithfulness) is unchanged.
