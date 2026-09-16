# Additions of 16 September 2026

Four results audited on 16 September 2026 were added to the manuscript reviewed in `SPECIALIST_AUDIT.md`. They were first integrated into an older copy of the manuscript and then ported onto this structure. The specialist audit's corrections are kept, including the private-source convention of Theorem 4.8 (finding A2). Section, theorem and equation numbers in Sections 1 to 6 are unchanged except for the new statements listed below. Open problems and verification move from Sections 7 and 8 to Sections 8 and 9.

The PDF now has 62 pages: the title and contents page, 46 pages of main text (pages 2 to 47), and the appendices and references. Both LaTeX builds have no undefined references, multiply defined labels, or overfull or underfull boxes, and the standalone PDF text matches `paper/main.pdf`.

## What was added and where

| Result | Location | Status |
| --- | --- | --- |
| Sharper corrected density: `c = m R^{m-1}`, range `R = (1+q)^{t/2} <= m²/(m²-1)` | Lemma 4.2 | Analytic, audited |
| Square witness for `q <= (16/15)^{2/t} - 1`, containing `q <= 1/(8t)` | Theorem 4.3 | Analytic, audited; exact certificates at `q = 1/(16t)`, orders 1 and 2, with `c = 5`; Lean at `q = 1/(16t)` only (`square_linear_witness`) |
| Triangle witness for `q <= (9/8)^{2/t} - 1`, containing `q <= 2/(9t)` | Theorem 4.4 | Analytic, audited; exact certificates at `q = 1/(16t)`, orders 1 to 3, with `c = 4`; Lean at `q = 1/(16t)` only (`triangle_linear_witness`) |
| Survivors: `H_t >= q_t/6 > 1/(47t)` on the square, `H_t >= q_t/10 > 1/(43t)` on the triangle, also over strictly positive laws | Corollaries 4.6 and 4.7 | Analytic, audited |
| Brackets with the new lower bounds | Corollary 4.9; introduction; Figure 6 guarantee curves | Analytic, audited |
| Order conversion along the parity direction: `q^NW_t <= q^AI_s` for `t >= max{s, floor(3s/2)}` | Proposition 4.12, proof in Appendix B.4 | Analytic, audited |
| Triangle brackets at orders 11 to 13: identical at 11 and 13 with an AI dual on NW keys, `q^AI_12 < q^NW_12` | Paragraph after Proposition 4.12 | Exact certificates; the odd-order coincidence stays open |
| Cubic parity certificates, constants 8 (square) and 10 (triangle) | Proposition 6.3 | Analytic, audited; sampled exact falsification test |
| Barycentre bound `F(P) >= -Σ(P)/n` | Proposition 6.4 | Analytic, audited; identities checked exactly at small `n` |
| Explicit rejecting orders, linear and quadratic forms | Corollary 6.5 | Analytic, audited |
| Laws with `F < 0` satisfy every Finner inequality; the fan inequalities never fail for such laws | Proposition 6.6 | Analytic, audited; sampled exact check |
| Worked examples, including the W law and a full-support law | Remark 6.7 | Exact |
| Hypergraph scenarios: carried-over facts, absorption, traces, observers that read every source, hyper-double-star reconstruction, peeling, graphs, nontermination through pair sets, Conjecture 7.14 | Section 7 (Definitions 7.1, 7.4, 7.8, 7.12; Lemmas 7.2, 7.3, 7.5; Corollaries 7.6, 7.10; Theorems 7.7, 7.9, 7.13; Proposition 7.11) | Analytic, audited; exact reconstruction, transport and census checks; `K_4^(3)` is the only undecided scenario on four observers by exhaustive enumeration |
| Questions on hypergraph termination and explicit rejecting orders | Questions 8.4 and 8.5, Remark 3.9 pointer, introduction | Open questions |

## Formalization

The square witness of Theorem 4.3 is now proved in Lean at `q = 1/(16t)` (`TriangleInflation/Graph/SquareWitness.lean`, `TriangleInflation.Graph.square_linear_witness`). Like the triangle declaration, it is an endpoint specialization with the constants `c = 5` and `c = 4`; the wider ranges with `c = m R^{m-1}`, Corollaries 4.6 and 4.7, Proposition 4.12, Section 6.3 and Section 7 are not formalized. `Audit.lean` prints the axioms of the new declaration, and the gate reports 113 audited declarations.

## Certificates

New directories under `artifact/certificates/`: `exponent/odd/`, `beyond-finner/` and `hypergraph/`. Two adaptations were needed for this repository. The hardened `verify_exponent.py` binds a file to the published `t <= 10` inventory, so `verify_odd.py` substitutes an exact extension inventory for its files and fails if either is missing. `verify_hypergraph.py` compared its census record only when present and rewrote its transport record on every run; it now requires both stored records and compares them. Negative tests confirmed both failures. The replay commands are in `VERIFICATION_GUIDE.md`.

## Audits

The audits are research notes in the author's development repository (`resource-theory`), not distributed here:

- `papers/inflation-nontermination/research/2026-09-16/theorem-b/AUDIT.md` (corrected density, survivor constants, brackets)
- `papers/inflation-nontermination/research/2026-09-16/beyond-finner/NOTE.md` (Section 6.3)
- `papers/inflation-nontermination/research/2026-09-16/hypergraph-termination/AUDIT.md` (Section 7)
- `papers/inflation-nontermination/research/2026-09-16/odd-order/NOTE.md` (Proposition 4.12 and the order 11 to 13 brackets)

As with `SPECIALIST_AUDIT.md`, these are AI-assisted audits, not independent human specialist review.

## Deviations from the reference integration

- The certificates of Theorems 4.3 and 4.4 and the Lean declarations use the constants `c = 5` and `c = 4`. A sentence after Theorem 4.4 notes that these constants satisfy `cR >= mR^m` for `tq <= 1/16`, so the positivity step holds with them; this restates the previously audited argument.
- After Proposition 4.12 the reference text said the conversion "accounts for" the agreement of the order-three AI and order-four NW brackets. The conversion gives only `q^NW_4 <= q^AI_3`, so the text now says the brackets agree at that pair, the exception in Proposition 4.11(iii).
- The note after Question 8.5 and the introduction attribute Finner satisfaction only to laws with `F < 0` on the triangle, as in Proposition 6.6. The reference text attributed it to all laws caught by parity rigidity.
- Section 7 follows Section 6 rather than the classification so that existing numbers in Sections 4 to 6 are unchanged. The explicit-rejecting-order subsection follows the bit-length subsection for the same reason, keeping Proposition 6.2.
