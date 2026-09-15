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
```

The checkers use Python integers and rational arithmetic; no LP solver is required. The parity checks verify primal moments, dual nonpositivity on all count configurations, and signs of expectation polynomials using Sturm sequences. Figure 6 reads its interval endpoints from those certificates. Matching rational brackets do not prove equality of thresholds.

The threshold verifier requires both scenario files and all 40 published order/hierarchy records by default, rejecting missing, duplicate or mislabeled records. `--max-order N` checks complete coverage through N; for N below ten its success message says `PARTIAL`. The mutation suite covers missing files and records, duplicate records, incorrect metadata and corrupted weights. The release supports verification of the supplied threshold certificates; the discovery scripts named in the historical campaign report are not distributed.

The replay runner uses temporary certificate copies and writes records under `artifact/replay_logs/`. Its independent numerical distance check requires `mpmath`. The manifest and SHA-256 sums identify the distributed inputs, checkers and documentation. They exclude `artifact/replay_logs/`, whose execution records change on replay.

The artifact retains the original nontermination checker for provenance. Python's optimization flag disables its assertions. Use the hardened checker, which rejects optimized execution. The mutation tests check that corrupted inputs fail. The fan checker uses explicit exceptions and also runs under optimization.

## Lean build and audit

```sh
lake build
bash scripts/check_axioms.sh
```

The audit lists 112 declarations and checks dependence only on `propext`, `Classical.choice` and `Quot.sound`. It also checks that the registry challenge definitions match the library. The two challenge files contain the unproved statements required by the registry format; their solutions and the audited library contain no `sorry`.

The graph development proves the binary classification for finite latent alphabets. The transfer to arbitrary latent spaces uses Rosset–Gisin–Wolfe's cardinality theorem, which is not formalized here. The larger-observed-alphabet transfer is also outside this development. The classification equivalence and strictly positive witness existence are formalized; rationality of those witnesses is analytic. The mapped corrected-triangle declaration proves the endpoint `q = 1/(16t)`, while manuscript Theorem 4.4 covers the full interval below it.

`TriangleInflation/FinnerMeasure.lean` separately proves Finner and triangle nontermination for arbitrary latent probability spaces and measurable stochastic responses. Its main statement is `no_finite_characterizing_orderM`. The graph bridge supplies recursively expressible conclusions from the triangle module's AI statements.

The general convex-order inequality, square corrected-density witness and max-moment bound, square order conversion, count-moment and threshold results, distance asymptotics, bit-length theorem and supplementary inequalities are not formalized. The finite bounds on the defect family are formalized; their limiting statements are not. Consult the README and YAML map for individual declarations.

## Paper and submission package

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=../tmp/pdfs/build paper/main.tex
cp tmp/pdfs/build/main.pdf paper/main.pdf
python3 paper/release/build_arxiv.py
```

The package builder creates `paper/release/arxiv-src/` and `paper/release/arxiv-src.tar.gz`, flattens local inputs, and checks a standalone build without shell escape. The bundled threshold figure needs no Python at submission time. The build should have no unresolved references, multiply defined labels or overfull boxes. Render the resulting PDF to check float placement and spacing after structural edits.

These commands describe how to replay verification. They do not imply that every check was rerun for every editorial revision; `EDITORIAL_REVIEW.md` and `validation.json` record which checks ran and against which snapshot. Git pushes do not update an arXiv submission or a Palomar record.
