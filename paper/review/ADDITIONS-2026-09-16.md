# Additions of 16 September 2026

## Revision after the referee audit and priority sweep

Two reports on commit `0885897` led to a cut revision the same day. Both are research notes in the author's development repository (`resource-theory`), not distributed here, and both are AI-assisted, not independent human review:

- `papers/inflation-nontermination/research/2026-09-16/review/REFEREE_AUDIT.md` (minor revision; four P2 findings, five P3 findings)
- `papers/inflation-nontermination/research/2026-09-16/priority/PRIORITY_SWEEP_SECTIONS_6.3_7.md` (verdicts, citations and attribution sentences for Sections 6.3 and 7)

### What was cut and why

- **Section 7, sources shared by three or more observers, was removed** and becomes a separate companion paper. The referee audit (P3-4) judged that it interrupted the path from the quantitative bounds to the open problems and that a strong-journal referee would ask for a split; its P2-2 and P2-3 findings (the misstated nontermination criterion in the abstract and introduction, the unreduced seven-observer claim) and P3-1 (census status) concern that section and go with it. What stays: one sentence in the introduction's scope paragraph, Remark 3.9 with a citation to Fritz 2012 Proposition 3.7, and Question 7.4 restated neutrally. The conjecture environment, the census and hypergraph rows of Appendix C and every cross-reference were removed. `artifact/certificates/hypergraph/` stays in the artifact, and `artifact/README.md` says it belongs to the companion paper.
- **Section 6.3 was cut to Remark 6.3** (under one page). The sweep found that all three worked examples are rejected at AI order two by the Spiral-inflation inequality (52) of Wolfe, Spekkens and Fritz, that the W law's incompatibility is their Example 2, that its Finner compliance is noted by Renou et al. 2019, and that the `1/n` mechanism is Navascués–Wolfe 2020 Theorem 1 with eqs. (34) and (A5). The remark keeps the two cubic certificates with a short proof, the bound `F(P) >= -Σ(P)/n` with `Σ(P) <= 3` as a consequence of Theorem 4.8, the resulting rejecting order, and these attributions. Removed: the worked examples, the quadratic route (former Corollary 6.5(ii)) and its comparison, the Hessian remark, and Proposition 6.6. `verify_beyond_finner.py` still checks the removed examples and the former Proposition 6.6; `artifact/README.md` says so.
- **Fritz 2012** is cited after the proof of Lemma 3.7 as the direct ancestor of the forbidden-induced-subgraph shape of the exhaustion argument (Theorem 3.8, Lemma 3.9) and of the hypergraph framing, and has a row in `paper/release/PRIORITY_AUDIT.md`.

### Referee findings

| finding | resolution |
| --- | --- |
| P2-1, paragraph after Proposition 4.12 | The false no-go sentence, the degree-gap and parity-weighted-moment claims and the floating-point remark were deleted. "Coincide" became "have identical certified brackets", with a pointer to Proposition 4.11(ii). |
| P2-2, hypergraph criterion in abstract and introduction | Moot: the sentences were removed with Section 7; no remaining sentence states a hypergraph criterion. |
| P2-3, seven-observer minimality | Moot: removed with Section 7. |
| P2-4, ledgers | `CLAIMS.md` and `NONCLAIMS.md` rewritten in current numbering; superseded bodies (with `5/(768t)`, `27/(5120t)`, the claim of Lean coverage over a range of `q`, and paths that do not exist here) removed, remaining in git history. Lean scope of both corrected witnesses stated as `q = 1/(16t)` only. `README.md` gives 113 audited declarations (two registry statements and 111 library results) and no longer says the non-claims agree with the coverage tables. |
| P3-1, census status in Section 9 | Moot: removed with Section 7. |
| P3-2, abstract overclaim on cubic certificates | The abstract now states only the rejecting order `⌊3/v⌋ + 1` for a law that violates a certificate by `v`; the Finner proposition is gone. |
| P3-3, Lemmas B.1 and B.2 sketched | Appendix B.2 now has Lemma B.1 (sign potentials) with a full proof of the potential representation, its uniqueness up to a global flip, and the sufficiency statement for a family-exchangeable potential law; Lemmas B.2 and B.3 cite it for both directions. Proposition 4.12 cites Lemma B.1(ii). |
| P3-4, structure and length | Section 7 removed and Section 6.3 cut; open problems and verification are Sections 7 and 8 again. |
| P3-5, notation | Clashes that remain after the cuts: the guarantee endpoint of Corollaries 4.6 and 4.7 is now `\underline q_t`, distinct from the thresholds `q_t^H`. The hypergraph `H`, the split sources `S`, the centre set `Z`, the parity error `ε` and `G(P)` of Section 6.3 left with the cuts. Not changed: `H` as hierarchy label and profile, `c` and `T` in their separate local uses. |

Also fixed from the audit's P4 list: the Appendix C table now lists the corrected square certificates at orders 1 and 2 (last paragraph of the audit); `formalization.yaml` and the README describe the finite bounds behind `Θ(ε^{-1/3})` rather than the asymptotic form; the verification guide says how to restore `artifact/replay_logs/` after a replay; the arXiv abstract matches `main.tex`.

### Result

The PDF has 54 pages: the title and contents page, 38 pages of main text (pages 2 to 39), and the appendices and references. The abstract has 1622 characters. Both LaTeX builds have no undefined references, multiply defined labels, or overfull or underfull boxes, and the standalone PDF text matches `paper/main.pdf`. Section and theorem numbers in Sections 1 to 5 are unchanged, except that Lemmas B.1 to B.3 of the earlier version are now Lemmas B.2 to B.4 after the new Lemma B.1.

## Additions as integrated at commit 0885897

The record below describes the integration before the revision above. Its rows for Section 6.3 (Propositions 6.3, 6.4, 6.6, Corollary 6.5, Remark 6.7) and Section 7, its page counts and its section numbers for open problems and verification are superseded.

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
