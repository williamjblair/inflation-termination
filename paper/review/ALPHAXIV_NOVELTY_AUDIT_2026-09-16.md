# Novelty and prior-art audit using alphaXiv

Date: 2026-09-16. Manuscript evaluated: commit `934c4741617c5632421ed2657ebc0649553a6905`.

## Verdict

No predecessor to the manuscript's finite-termination classification was found in the checked primary-source material. The strongest contribution remains the binary pair-source graph classification: finite termination precisely for disjoint unions of double-stars, together with explicit incompatible laws surviving every prescribed finite order in the other cases. The all-order constructions and quantitative rejecting-order results also remain distinct from the predecessors examined.

This is a bounded literature comparison, not a certification of priority or a new proof audit. AlphaXiv supplied query-selected PDF pages, not an exhaustive full-text review of every source. Its discovery and author-matching limitations prevent an unqualified claim that all relevant literature has been excluded. The initially unresolved Gitton thesis comparison was completed using the author-supplied PDF; see the final section below.

One concrete citation improvement emerged: explicitly credit Fritz's path-to-Bell and path-to-bilocal identifications where the manuscript uses endpoint observations as settings. This concerns attribution of a known ingredient; it does not displace the finite-order reconstruction or the all-order path witnesses.

## Claim-by-claim comparison

| Manuscript claim or ingredient | Closest checked antecedent | Assessment |
| --- | --- | --- |
| Double-star finite reconstruction and graph classification | Navascués–Wolfe, §4.1; Fritz, Theorem 3.8 and Lemma 3.9 | NW establish star termination and discuss finite-order questions. Fritz classifies when all correlations, in his defined sense, are classical; that is a different predicate. His induced-subgraph reduction is an antecedent, already credited in the manuscript. No equivalent inflation-termination classification was located. |
| Incompatible distributions accepted at arbitrarily prescribed orders | NW's order-two triangle examples and polynomial-optimization nonattainment example | The optimization example concerns a scenario where every distribution is compatible. It does not establish nontermination of compatibility testing. No replacement for the manuscript's all-order compatibility witnesses was found. |
| Path reconstruction and five-path obstruction | Fritz, Theorems 2.4 and 2.9; the bilocal inequality already cited in the manuscript | The conversion from endpoint observations to measurement settings is established prior work. The contribution here is the inflation-order theorem and the accepted incompatible families. Add explicit Fritz citations. |
| AI–expressible equality for the root-sink setting | Wolfe–Spekkens–Fritz, Definitions 7–8 and discussion of stronger expressible constraints | Their general separation uses a broader causal setting. The retrieved material does not state the manuscript's restricted equality. Do not generalize this equality beyond its stated hypotheses. |
| Source-count-independent convex-order estimate | NW finite de Finetti argument; Gitton, Theorem 8 and thesis Theorem 5.4; Fraser's convergence hierarchy | Convergence, sampling arguments, and the general inverse-square-root distance rate are prior work. The distinguishing assertion is the stronger comparison and removal of the explicit source-count factor, not the rate alone. The supplied thesis confirms the source dependence of its stated bound; see the final section. |
| Distance-dependent rejecting order and rational input-size bounds | Existing convergence bounds and finite-level nonlocality certificates | No matching all-order lower bound, defect-family scaling, or rational-bitlength rejecting-order theorem was found in the checked material. An inflation-order lower bound is not a runtime lower bound for every compatibility algorithm. |
| Parity repair and cubic certificates | Boreiri et al.; earlier WSF polynomial inequalities | Exact and robust triangle parity rigidity are prior work. Boreiri et al. obtain a repair bound at most three times the parity error; the manuscript's five-times-error bound is not an improved robustness constant. Cubic network inequalities also predate this paper. The specific certificate can be useful without a claim to inventing either ingredient. |
| Order-indexed fan inequalities | WSF marginal-polytope method; Fraser–Wolfe wagon-wheel and web inequalities | The certificate method is established. The possible new content is the displayed family indexed by order and its quantitative consequence. Algebraic independence from every earlier inequality was not established by this audit. |

The present related-work section already makes most of these distinctions correctly. In particular, it credits parity rigidity, bilocality, the marginal-polytope method, and the earlier convergence arguments.

## Recommended attribution changes

In `paper/sections/14-double-star.tex`, after the four-observer-path result, add a sentence along these lines:

> Fritz's Theorem 2.4 identifies classical correlations on the four-observer path with Bell-local conditional distributions; the result here bounds the inflation order needed for reconstruction.

In `paper/sections/16-five-path.tex`, near the scenario definition or the bilocal attribution, add:

> The identification with bilocality after conditioning on the endpoint observations is given by Fritz's Theorem 2.9.

Use the existing `Fritz2012` bibliography entry. Fritz states these equivalences for his defined correlations, with conditioning restricted to supported endpoint values; do not recast them as equivalences for arbitrary joint distributions without the requisite marginal constraints.

Any earlier audit describing endpoint conditioning itself as a new device should be read as superseded by this finding. No manuscript, Lean, release-package, or registry files were changed during this audit.

## Primary-source evidence

Page numbers below refer to the PDF pages returned by alphaXiv. These are the principal comparison locations, not a claim that every page of each work was reviewed.

| Source and retrieved version | Relevant material and comparison |
| --- | --- |
| [Navascués–Wolfe, 1707.06476v3](https://arxiv.org/abs/1707.06476v3) | pp. 7–9: star termination, finite-order question, optimization nonattainment, and de Finetti error bounds. |
| [Fritz, 1206.5115v2](https://arxiv.org/abs/1206.5115v2) | pp. 8, 11: Theorems 2.4 and 2.9; pp. 22–23: Theorem 3.8, Lemma 3.9, and induced-subgraph transport. |
| [Wolfe–Spekkens–Fritz, 1609.00672v5](https://arxiv.org/abs/1609.00672v5) | pp. 16–18, 21, 25: expressibility, AI constraints, polynomial inequalities, and stronger expressible constraints. |
| [Gitton, 2202.04103v1](https://arxiv.org/abs/2202.04103v1) | pp. 58–61, especially Theorem 8 and equation (63): postselected-inflation convergence, with source parameters in the bound. |
| [Fraser, 1902.07091v2](https://arxiv.org/abs/1902.07091v2) | pp. 29–30: uniform latent approximation and convergence of a different hierarchy. Its latent-cardinality parameter is not an inflation level. |
| [Boreiri et al., 2207.08532v2](https://arxiv.org/abs/2207.08532v2) | Exact parity-token-counting rigidity and minimal binary network examples. |
| [Boreiri et al., 2311.02182v3](https://arxiv.org/abs/2311.02182v3) | p. 6, Results 1–2 and equations (15)–(21): approximate rigidity and total-variation repair bound. |
| [da Silva–Pozas-Kerstjens–Parisio, 2503.16654v2](https://arxiv.org/abs/2503.16654v2) | pp. 1–5: symmetric binary-triangle families, local models, finite-copy inflation, and conjectured boundaries. No all-order survival theorem located. Version 2 was checked explicitly after an initial version-1 retrieval. |
| [Fraser–Wolfe, 1709.06242v2](https://arxiv.org/abs/1709.06242v2) | p. 9 and surrounding material: wagon-wheel and web certificates from particular inflations. |
| [Gitton–Renner, 2510.15143v1](https://arxiv.org/abs/2510.15143v1) | pp. 23–24 and related certificate material: exact EJM nonclassicality certification and discussion of larger inflations near compatibility. No general order-growth or termination classification found. |
| [Fully quantum inflation, 2501.12320v2](https://arxiv.org/abs/2501.12320v2) | pp. 1–2, 13–14: state compatibility and different encodings; its classification concerns different objects. |
| [Quantum bilocal completeness, 2212.11299v2](https://arxiv.org/abs/2212.11299v2) | pp. 1, 9–10: asymptotic completeness for quantum/commuting-observable models, rather than the present classical finite-termination question. |
| [Symmetric sum-of-squares bit-size bounds, 2509.06928v1](https://arxiv.org/abs/2509.06928v1) | Degree versus coefficient-size bounds for proofs; not a bound relating a rational distribution's input length to its first rejecting inflation order. |
| [Levin–Chandrasekaran, 2507.15632v2](https://arxiv.org/abs/2507.15632v2) | General dimension-varying polynomial optimization, representation stability, and de Finetti methods. No matching classical-inflation classification identified in the returned pages. |

## Scope and unresolved comparisons

- Fourteen distinct, correctly identified primary papers were inspected through alphaXiv's PDF-query tool. One had two versions retrieved. Raw returned excerpts and discovery results are retained locally under the ignored directory `tmp/alphaxiv-prior-art/`.
- Two discovery searches were used. The first returned mostly unrelated material and was discarded; the focused inflation/network search supplied relevant leads. Unrelated search results are not evidence of novelty.
- AlphaXiv's researcher lookup failed to match all six requested authors reliably. Those results were excluded. This audit therefore does not establish comprehensive recent-author or 2026 coverage.
- Gitton's *Certifying non-classicality in causal networks* thesis, [ETH DOI](https://doi.org/10.3929/ethz-b-000745278), was not successfully retrieved during the alphaXiv search. Its title lookup returned a different paper, which was excluded; DOI and direct official-host retrieval attempts also failed. The user subsequently supplied the thesis, allowing direct verification of Theorem 5.4 and equation (5.51), recorded below.
- No exhaustive symbolic comparison of the cubic and fan certificates against all earlier inequalities was performed. No independent literature proof of priority was obtained for each low-order threshold or constant.

## Submission consequence

The checked literature gives no reason to withdraw the main theorem or recast the paper as a reproduction. Keep the contribution centered on finite termination, explicit all-order witnesses, and quantitative rejecting-order bounds. The path citations have been added and the thesis comparison completed. Detailed certificate priority remains qualified. The novelty case is credible on the checked evidence; it is not an unconditional clearance of the entire literature.

## Follow-up: citation changes implemented

At the author's request, both Fritz citations were added after this audit, and the manuscript PDF and flattened arXiv package were rebuilt. Both builds pass; the manuscript remains 52 pages. The main build log has no overfull or underfull boxes, undefined references, or multiply defined labels. The extracted text of the ordinary and submission PDFs matches. The new citations render correctly on PDF pages 12 and 18, which were visually inspected. The archive's four members match the release-directory files byte for byte. No mathematical statements, proofs, Lean files, or Palomar files were changed.

## Follow-up: Gitton thesis comparison completed

Source: user-supplied `/Users/williamblair/Downloads/thesis_gitton.pdf`, 238 PDF pages, SHA-256 `e6588400b0061229e347e981de4d5ba430f1e35ff9c00d42619cbddc7c7de022`. Compared against manuscript commit `250bf0cef38e3734e967ca2f86cb2548ad4347e3`.

The targeted review covered Chapter 5, the defining inflation constraints in Chapter 4, the norm convention in Chapter 2, and the introduction and conclusion. Full-document text searches checked for additional convergence or termination statements. The displayed equations on printed pages 83 and 85 (PDF pages 102 and 104) were also visually inspected. This was a targeted novelty comparison, not a line-by-line audit of all 238 pages.

### Direct comparison of the bounds

Gitton uses the Euclidean norm, defined in equation (2.4). Theorem 5.4, equation (5.54), gives a compatible model with

\[
\|p-p^M\|_2^2\le 2\varepsilon_1^{N,z}+\varepsilon_2^{N,z}.
\]

For equal inflation sizes, equation (5.51), printed page 82 / PDF page 101, expands this as

\[
2\varepsilon_1^{N,z}+\varepsilon_2^{N,z}
=\frac{\sum_s 2N_s(s)(3N_s(s)-2)}{z}+O(z^{-2}).
\]

Here `N_s(s)` counts sources of type `s`. In the ordinary setting with one distinct type per source and `L` sources, equations (5.16), (5.39), and (5.40) give exactly

\[
\varepsilon_1^{N,z}=0,\qquad
\varepsilon_2^{N,z}=2[1-(1-1/z)^L]
=2L/z+O(z^{-2}).
\]

For the ordinary triangle, equation (5.65), printed page 85 / PDF page 104, states

\[
\|p-p^M\|_2^2\le 6/z-6/z^2+2/z^3.
\]

The manuscript instead obtains, for an order-`t` NW witness,

\[
\mathbb E_\Gamma\|q_\omega-P\|_2^2
\le \frac{1-\|P\|_2^2}{t},
\qquad
d_{\mathrm{TV}}(P,\mathcal C_G)
\le\frac{\sqrt{K-1}}{2\sqrt t}.
\]

On the binary triangle, `K=8`, so the squared Euclidean bound is at most `7/(8t)`. With `z=t`, the thesis's stated triangle bound is therefore not the manuscript's sharper estimate. More generally, its explicit source-count dependence remains. The manuscript's TV bound still depends on the number of observed joint outcomes; source-count independence does not mean independence of all problem dimensions.

### Shared ingredients and scope

Gitton's Definition 5.1 constructs a classical model by drawing uniform source indices and reading an inflation table. This is the same extraction construction used in the manuscript's ordinary-network setting. He credits the triangle formula (5.12) to NW equation (A2). The extraction construction and the inverse-square-root distance rate are established ingredients.

The thesis does not give the manuscript's comparison for every convex functional of the extracted distribution in the reviewed material. Its convergence proof uses the collision estimates of Theorem 5.2 and the quadratic estimate of Lemma 5.3. The new assertion being compared is the conditional-expectation/convex-order bound and its improved constant.

There is a scope distinction: the thesis also treats sources constrained to have the same distribution and parties constrained to use the same strategy. The manuscript's ordinary correlation-scenario theorem does not replace those additional results. In the common setting, an NW witness satisfies Gitton's averaged two-copy constraint (4.72). Conversely, that constraint alone is not an assertion of the full independent diagonal law required for the manuscript's all-convex-functional statement. The manuscript explicitly notes that its quadratic estimate only needs degree-two diagonal constraints.

No finite-termination graph classification or explicit all-order incompatible survivor construction was located in this targeted thesis review. Its Chapter 5 establishes asymptotic convergence, which is consistent with the manuscript's nontermination results.

### Consequence

The specific thesis-comparison gap is closed: the checked thesis result does not preempt the source-count-independent estimate, and no theorem correction is indicated. A direct citation to `Gitton2025Thesis`, Definition 5.1 and Theorem 5.4 / equation (5.65), would make the attribution and quantitative comparison easier for readers to verify. The bibliography entry already exists. This follow-up updates the audit only; it does not change the manuscript or publish another commit.
