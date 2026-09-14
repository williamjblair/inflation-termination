# Reproduce

Environment of the release replays (recorded per run in `artifact/replay_logs/*.json`):
macOS 27.0 (Darwin, arm64), Python 3.13.9, standard library only.

    cd artifact
    python3 -B verifiers/run_replay.py       # nt-frozen-reconstruct-check, nt-frozen-check, nt-hardened-check,
                                             # nt-hardened-reconstruct-check, eff-frozen-check, eff-hardened-check
    python3 -B verifiers/mutation_tests.py   # writes replay_logs/mutation-nontermination.{json,log}
    python3 -B verifiers/mutation_tests_fan.py   # fan checker: 13 scenarios, fails closed also under -O/-OO
    python3 -B certificates/classification/verify_classification.py   # cycle, path, square, triangle and low-order square certificates (exact; refuses -O)
    python3 -B verifiers/make_manifest.py    # MANIFEST.json, SHA256SUMS

| check | expected | recorded |
|---|---|---|
| `reconstruct.py --check` (frozen / hardened) | regenerates the five certificate files byte-identically; `PASS`, 166 nonzero order-2 coordinates | `replay_logs/nt-*-reconstruct-check.json` |
| `check.py` (frozen / hardened) | `"status": "PASS"`; orders 1,2,3 with 8/64/512 diagonal equations; order-2 table normalized over 2^32 with 12,288 symmetry and 64 diagonal equations; negative control rejected at a diagonal equation | `replay_logs/nt-*-check.json` (~0.2 s) |
| effective-inflation Farkas calibration (frozen / hardened) | `PASS` | `replay_logs/eff-*-check.json` |
| fan certificates (`certificates/fan/verify_certificates.py`, normal and `-O`) | `"status": "PASS"`, 14 targets; byte-identical stdout under `-O` | `replay_logs/fan-check*.json` |
| independent fan recheck (`verifiers/fan_independent_check.py`) | pointwise inequality exhaustive for `t ≤ 7`; sandwich table; `v_4 = 6969/2097152`; `R_p` rejected at `t = 2`; distance-construction ratios → `d_0` | `replay_logs/fan-independent-check.log` |
| classification certificates (`certificates/classification/verify_classification.py`) | `"status": "PASS"`; cycles C3/C4/C5 at orders 1–2, five-path at orders 1–2, square witness at orders 1–2 and triangle witness at orders 1–3 (plain and flipped: positivity, symmetry, diagonal law, every AI prescription, target incompatibility, negative control); corrected-density minimum scans to t=5 (square) and t=6 (triangle); low-order square: count-form primals at q=3/20 (NW_2) and q=1/10 (AI_2) expanded to 2^16 atoms, AI_2 dual with the identity E[D]=(1+q)(q³−33q²+27q−3) on 81 configurations, NW_3 dual on 256 configurations at q=1/10 | stdout JSON (input SHA-256s recorded in the output) |
| mutation suite | hardened checker fails closed on truncated, empty, corrupted-atom, wrong-order, missing-branch, normalization-preserving sign corruption, negative entry, wrong root law, bad support, un-rejected negative control, `-O`, `-OO`; frozen checker fails OPEN under `-O`/`-OO` (documented defect: bare `assert`) | `replay_logs/mutation-nontermination.json` |

arXiv package from the repository root: `bash paper/release/build_arxiv.sh` (flat `main.tex`, `main.bbl`,
compiles with `-no-shell-escape`, no absolute paths).

Frozen originals (`artifact/certificates/*/check.py`, `reconstruct.py`) are
byte-identical to the maintained repository files at revision `768d404` and are
never modified; release checkers are the `*_hardened.py` copies produced by
`verifiers/harden.py` (an AST transform that rewrites every `assert` to an
explicit exception and adds an `if not __debug__: raise` guard).

The 14 September editorial revision adds `paper/figures/generate_thresholds.py` (Python + matplotlib) to regenerate the certificate-derived vector plot. TikZ diagrams compile directly in LaTeX. The arXiv archive includes the rendered plot and flattened diagram source, so upload compilation requires neither Python nor shell escape. Run `python3 -B artifact/certificates/exponent/verify_exponent.py` for all 20,004 parity-threshold checks.
