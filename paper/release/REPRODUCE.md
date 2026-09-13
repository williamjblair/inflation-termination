# Reproduce

Environment of the release replays (recorded per run in `artifact/replay_logs/*.json`):
macOS 27.0 (Darwin, arm64), Python 3.13.9, standard library only.

    cd artifact
    python3 -B verifiers/run_replay.py       # nt-frozen-reconstruct-check, nt-frozen-check, nt-hardened-check,
                                             # nt-hardened-reconstruct-check, eff-frozen-check, eff-hardened-check
    python3 -B verifiers/mutation_tests.py   # writes replay_logs/mutation-nontermination.{json,log}
    python3 -B verifiers/mutation_tests_fan.py   # fan checker: 13 scenarios, fails closed also under -O/-OO
    python3 -B verifiers/make_manifest.py    # MANIFEST.json, SHA256SUMS

| check | expected | recorded |
|---|---|---|
| `reconstruct.py --check` (frozen / hardened) | regenerates the five certificate files byte-identically; `PASS`, 166 nonzero order-2 coordinates | `replay_logs/nt-*-reconstruct-check.json` |
| `check.py` (frozen / hardened) | `"status": "PASS"`; orders 1,2,3 with 8/64/512 diagonal equations; order-2 table normalized over 2^32 with 12,288 symmetry and 64 diagonal equations; negative control rejected at a diagonal equation | `replay_logs/nt-*-check.json` (~0.2 s) |
| effective-inflation Farkas calibration (frozen / hardened) | `PASS` | `replay_logs/eff-*-check.json` |
| fan certificates (`certificates/fan/verify_certificates.py`, normal and `-O`) | `"status": "PASS"`, 14 targets; byte-identical stdout under `-O` | `replay_logs/fan-check*.json` |
| independent fan recheck (`verifiers/fan_independent_check.py`) | pointwise inequality exhaustive for `t ≤ 7`; sandwich table; `v_4 = 6969/2097152`; `R_p` rejected at `t = 2`; distance-construction ratios → `d_0` | `replay_logs/fan-independent-check.log` |
| mutation suite | hardened checker fails closed on truncated, empty, corrupted-atom, wrong-order, missing-branch, normalization-preserving sign corruption, negative entry, wrong root law, bad support, un-rejected negative control, `-O`, `-OO`; frozen checker fails OPEN under `-O`/`-OO` (documented defect: bare `assert`) | `replay_logs/mutation-nontermination.json` |

arXiv package: `cd release && ./build_arxiv.sh` (flat `main.tex`, `main.bbl`,
compiles with `-no-shell-escape`, no absolute paths).

Frozen originals (`artifact/certificates/*/check.py`, `reconstruct.py`) are
byte-identical to the maintained repository files at revision `768d404` and are
never modified; release checkers are the `*_hardened.py` copies produced by
`verifiers/harden.py` (an AST transform that rewrites every `assert` to an
explicit exception and adds an `if not __debug__: raise` guard).
