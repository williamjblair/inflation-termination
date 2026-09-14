# Audit scope and immutable source references

Repository: `williamjblair/resource-theory`.
Pinned default-branch commit: `768d404c631659574d9fad232c028df4f63fbc3b`.
Tree: `7b84880c69dba943d46bca908dbcaeaa650fd6e8`.
Commit time reported by GitHub: `2026-09-12T21:57:48Z`.

The pin was read through the connected GitHub service, and all subsequent
repository reads used this full commit. No claim is made that the branch has
not changed since that read. The repository was not modified.

## Load-bearing written sources inspected

The identifiers in the last column are Git blob SHA-1 identifiers reported
by GitHub metadata, not locally recomputed SHA-256 file digests. The commit
and path independently identify each exact artifact.

| Path | Read scope | Git blob |
|---|---|---|
| foundations/inflation-nontermination/proof.md | All mathematical sections 1–7, and replay description | fbbcba45519cc30a71bda9cc8d11f2ee873a50c1 |
| foundations/inflation-nontermination/verification.md | Full | 24b4eedeca7c6932c8d43bf56126a27b08588230 |
| papers/inflation-nontermination/internal-review.md | Full | 05ba3a554b91bc644a25281b58e91712c708a1c5 |
| papers/inflation-nontermination/priority.md | Full bounded priority report | Exact commit/path above |
| papers/inflation-nontermination/reproduce.sh | Full; not executed | ecce0260db6afe0f996281b254d799fb17a7ac13 |
| papers/inflation-nontermination/certificates/check.py | Full code; not executed | 4f735d419b15c66fa0ee386dc788bd0a5b56c30f |
| foundations/inflation-strong-converse/proof.md | Full mathematical proof | d2d58692f70753b0fcdbe0b2eb59f0abd5d56edb |
| foundations/inflation-strong-converse/exponential-separation.md | Full, including stronger rate and scope | 664dccfe9b3ff5ff802f2fa24563d94a7846e511 |
| foundations/faithfulness/proof.md | Full mathematical proof | 5fd383ae7c44437dddf6db891cb75c6bc2b869df |
| foundations/faithfulness/quantitative-proof.md | Full | 6d555b399ead38dbf7a55f1b334978a5bea44421 |
| foundations/faithfulness/hierarchy-correction.md | Full | ac58c7d47fe6f76c44680da62b2f68950b313e8b |
| foundations/effective-inflation/proof.md | Sections 1–7; beginning of calibration Section 8 | ee96230861c084962cab6bcd836dd49d34480229 |

The defect construction, its diagonal-support argument, and recursive
expressibility proof were inspected directly, not inferred from RESULT.md.
The fan proof does not assume the false fixed-order equality of NW and the
maximal-AI relaxation. The sparse operational application uses the newer
Delta^2/A^2 compiler, not the older Delta^2/(32A^2) consequence.

## Maintained context inspected

| Path | Scope | Git blob |
|---|---|---|
| OPEN-PROBLEMS.md | Full, with OP1 load-bearing | 4716ef637416c4ce0f59a38a8aa442f2814e59ef |
| RESULTS.md | Relevant foundation, nontermination, faithfulness and effective-inflation entries; not every unrelated row | 5b7c5a49e706eef4180628ea83c2c0ed687451c2 |
| RESULTS.json | Opening status and retrieved relevant nontermination/effectivity entries; not the entire JSON | 93bb0a286322eec1566052353e95d87976e5d244 |
| THEOREMS.md | Foundation opening and relevant retrieved context; not every unrelated theorem | 9a458d3e3be2a2eade0f110ce450e077d25f85ad |
| PRIORITY.md | Opening and relevant inflation/faithfulness/effectivity rows | 7a0ef09bd5c6f1c734eb078d92ff7b213c253350 |
| SIGNIFICANCE.md | Full | 903783bd2b25953436e4239c8f2715e677a9fbd6 |
| CAMPAIGN.md | Full | 80a8b0297c8f8f371c1b6f5348fddd6a336e6c1e |

Directory and tree metadata were also inspected. Some historical source
packets named by these files live outside this repository in the owner's
research workspace. They were not all accessed. The request to inspect every
historical packet, verifier, and certificate has therefore not been
exhaustively completed, and this report does not pretend otherwise.

The upstream certificate directory was listed, and its checker read, but
not every certificate JSON or reconstruction implementation was inspected
or executed. Upstream reports of previous PASS outcomes remain attributed
to those reports. The newly reported execution results below are separate.

## Public primary-source read scope

- Navascués–Wolfe, arXiv:1707.06476: quantitative de Finetti theorem,
  Euclidean extraction, Appendix A collision formula, and Section 4.1
  finite-stabilization question. The relevant PDF formulas were visually
  checked with screenshots. Version-suffixed refetch attempts failed, but the unversioned v3 PDF
  was retrieved again successfully, with Appendix A visually checked.
- Wolfe–Spekkens–Fritz, arXiv:1609.00672v5: expressibility definitions,
  marginal witness and logical-tautology methodology, and relevant
  triangle examples. This is the methodological predecessor of the fan
  witness; the method itself is not claimed new.
- Rosset–Gisin–Wolfe, arXiv:1709.00707: finite cardinality, six-state triangle
  bound, semialgebraicity, and Appendix D. A version-suffixed refetch failed, but the unversioned primary PDF
  was retrieved again successfully. A requested page screenshot failed;
  the relevant primary text and paper query were available.
- da Silva–Pozas-Kerstjens–Parisio, arXiv:2503.16654: relevant v1 text was
  retrieved through academic search, then the updated v2 main text was read
  directly at `https://arxiv.org/html/2503.16654v2`. The boundary criteria are
  explicitly conjectural in that text; the comparison in REPORT.md uses v2.
- Additional recent classical, postselected, and quantum inflation work was
  discovered or inspected at abstract/metadata level. These are not counted
  as complete full-text priority checks.

The external search was conducted with a cutoff of 12 September 2026.
It is not an exhaustive literature census. The proposed all-order fan law
and hard-family exponent were not found in the inspected primary passages;
that is not proof of historical firstness. No global priority certificate is
issued, and no quantum theorem is claimed.

## What is new versus inherited

Inherited: the hard family, the passing construction, nontermination,
qualitative completeness, finite cardinality/semialgebraicity, the general
faithfulness compiler, the promised-KL rejecting-order type, computability
of exact finite rational compatibility, and upper semicomputability of the
regularized target-first divergence.

New derivations in this packet: the bare-NW fan inequalities, the matching
hard-family exponent with near-matching constants, the leading TV/Euclidean
distance constants, the sparse-fan operational lower bound as an application
of the maintained compiler, and the stated fixed-scenario encoding-length
corollary. The improved general convergence/margin constants are elementary
bookkeeping refinements of known machinery, not promoted as independent
conceptual breakthroughs. Historical priority for all new derivations
remains unestablished.

## Executed verification

The delivered `generate_certificates.py` and `verify_certificates.py` are
separate implementations. The checker imports no generator functions, uses
explicit exceptions rather than assertions, and was run in both ordinary
and optimized Python. Both runs passed with identical output.

The executed checks are:

- 14 exact rational target laws and their passing/rejecting sandwiches;
- five all-order nonnegative-polynomial slack cases;
- 174,760 exhaustive deterministic assignments;
- 271,500 count-orbit cases;
- 2,660 source-index/permutation checks for the NW product marginal;
- eight negative controls rejected.

These checks do not exhaustively solve complete higher-order inflation LPs.
The universal pointwise proof is supplied in REPORT.md; the finite
certificates instantiate it. Exact first rejecting orders are claimed only
where the proved passing and rejecting bounds coincide.

All new local files are hashed in SHA256SUMS. The archive contains no font
files, private repository clone, access tokens, or uninspected source payloads.
