# Artifact

| path | content |
|---|---|
| `witnesses/` | maintained statement and proof of the nontermination theorem (copies of `foundations/inflation-nontermination/`) |
| `certificates/nontermination/` | frozen exact certificates `t1/t2/t3-defect.json`, `t2-full-lp.json`, `t2-corrupted-negative-control.json`, original `check.py` and `reconstruct.py` |
| `certificates/effective/` | frozen exact order-2 Farkas calibration (`farkas.json`, `check.py`) |
| `verifiers/` | replay runner, hardened checkers (fail closed, refuse `-O`), `harden.py`, mutation tests, manifest generator |
| `replay_logs/` | fresh replay records with OS, architecture, Python, commands, wall times, hashes |
| `MANIFEST.json`, `SHA256SUMS` | identities of every file |

What the computer verifies: that the explicit defect-cube tables at orders 1–3
have the claimed symmetry, copied-triangle marginals, disjoint diagonal
supports and tensor-power diagonal law, that the order-2 full table satisfies
every NW linear constraint, and that the Finner gaps are the stated rationals.
The all-order theorem is proved analytically and does not depend on these
checks.
