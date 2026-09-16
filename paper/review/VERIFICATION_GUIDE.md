# Verification guide

This guide accompanies the reorganized manuscript. The analytic proofs, finite computations and Lean coverage are distinguished in Section 8. Appendix C describes the certificate formats and finite ranges. Declaration-level mappings are in `README.md` and `formalization.yaml`.

## Exact certificates

Run from the repository root:

```sh
python3 -B artifact/verifiers/run_replay.py
python3 -B artifact/verifiers/mutation_tests.py
python3 -B artifact/verifiers/mutation_tests_fan.py
python3 -B artifact/certificates/classification/verify_classification.py
python3 -B artifact/certificates/exponent/verify_exponent.py
python3 -B artifact/verifiers/mutation_tests_exponent.py
python3 -B artifact/certificates/exponent/odd/verify_odd.py
python3 -B artifact/certificates/beyond-finner/verify_beyond_finner.py
```

The checkers use Python integers and rational arithmetic; no LP solver is required. The parity checks verify primal moments, dual nonpositivity on all count configurations, and signs of expectation polynomials using Sturm sequences. Figure 6 reads its interval endpoints from those certificates. Matching rational brackets do not prove equality of thresholds.

The threshold verifier requires both scenario files and all 40 published order/hierarchy records by default, rejecting missing, duplicate or mislabeled records. `--max-order N` checks complete coverage through N; for N below ten its success message says `PARTIAL`. The mutation suite covers missing files and records, duplicate records, incorrect metadata and corrupted weights. The release supports verification of the supplied threshold certificates; the discovery scripts named in the historical campaign report are not distributed.

The two checkers added on 16 September 2026 for this manuscript are standard-library only and refuse optimized execution:

- `exponent/odd/verify_odd.py` (about 50 s) imports `../verify_exponent.py` and reuses its record checks on `exponent/odd/certificates/{triangle,square}.json`: triangle orders 11 to 13 in both hierarchies and square order 11 in the AI hierarchy. Both files are required and each must carry exactly these records; the published t ≤ 10 inventory check is replaced by this extension inventory, not skipped. It also checks the degree-set identities and the containment behind Proposition 4.12, the order-three face example, the intermediate degree systems in `layers-triangle.json`, and the odd-order bracket identities and order-12 separation quoted after Proposition 4.12. The expected final line is `OK: 5115 local checks and 9084 verify_exponent checks passed`.
- `beyond-finner/verify_beyond_finner.py` (about 4 s) checks Remark 6.3: the algebraic identities behind the bound `F(P) >= -Σ(P)/n`, and sampled falsification tests of the cubic certificates on exact laws of random finite models. It also runs checks written for an earlier, longer version of Section 6.3 that are not part of the current manuscript (see `artifact/README.md`). Expected: `PASS: 68183 exact checks`.

These checks cover finite instances. Remark 6.3 and Proposition 4.12 are proved analytically; sampled checks are falsification tests, not proofs.

The directory `artifact/certificates/hypergraph/` and its checker belong to the companion paper on sources shared by three or more observers. They are kept in the artifact for that paper and are not part of this manuscript's verification.

The replay runner uses temporary certificate copies and writes records under `artifact/replay_logs/`, which are tracked files; restore them with `git checkout -- artifact/replay_logs/` after a replay unless a refreshed record is intended. Its independent numerical distance check requires `mpmath`. The manifest and SHA-256 sums identify the distributed inputs, checkers and documentation. They exclude `artifact/replay_logs/`, whose execution records change on replay.

The artifact retains the original nontermination checker for provenance. Python's optimization flag disables its assertions. Use the hardened checker, which rejects optimized execution. The mutation tests check that corrupted inputs fail. The fan checker uses explicit exceptions and also runs under optimization.

## Lean build and audit

```sh
lake build
bash scripts/check_axioms.sh
```

The audit lists 113 declarations and checks dependence only on `propext`, `Classical.choice` and `Quot.sound`. It also checks that the registry challenge definitions match the library. The two challenge files contain the unproved statements required by the registry format; their solutions and the audited library contain no `sorry`.

The graph development proves the binary classification for finite latent alphabets. The transfer to arbitrary latent spaces uses Rosset–Gisin–Wolfe's cardinality theorem, which is not formalized here. The larger-observed-alphabet transfer is also outside this development. The classification equivalence and strictly positive witness existence are formalized; rationality of those witnesses is analytic. The mapped corrected-witness declarations `square_linear_witness` and `triangle_linear_witness` prove the endpoint specialization `q = 1/(16t)` of Theorems 4.3 and 4.4, with density constants `c = 5` and `c = 4`; the manuscript theorems cover `0 < q <= (16/15)^{2/t} - 1` and `0 < q <= (9/8)^{2/t} - 1` with `c = m R^{m-1}`, and that extension is analytic.

`TriangleInflation/FinnerMeasure.lean` separately proves Finner and triangle nontermination for arbitrary latent probability spaces and measurable stochastic responses. Its main statement is `no_finite_characterizing_orderM`. The graph bridge supplies recursively expressible conclusions from the triangle module's AI statements.

The general convex-order inequality, the corrected densities beyond `q = 1/(16t)`, the max-moment bound and survivor corollaries, square order conversion, count-moment and threshold results including Proposition 4.12, the cubic certificates and rejecting orders of Remark 6.3, distance asymptotics, bit-length theorem and supplementary inequalities are not formalized. The finite bounds on the defect family are formalized; their limiting statements are not. Consult the README and YAML map for individual declarations.

## Paper and submission package

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../tmp/pdfs/build paper/main.tex
cp tmp/pdfs/build/main.pdf paper/main.pdf
python3 paper/release/build_arxiv.py
```

The package builder creates `paper/release/arxiv-src/` and `paper/release/arxiv-src.tar.gz`, flattens local inputs, and checks a standalone build without shell escape. The bundled threshold figure needs no Python at submission time. The build should have no unresolved references, multiply defined labels or overfull boxes. Render the resulting PDF to check float placement and spacing after structural edits.

These commands describe how to replay verification. They do not imply that every check was rerun for every editorial revision; `EDITORIAL_REVIEW.md` and `validation.json` record which checks ran and against which snapshot. Git pushes do not update an arXiv submission or a Palomar record.
