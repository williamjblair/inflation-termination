# Artifact

| path | content |
|---|---|
| `witnesses/` | maintained statement and proof of the nontermination theorem (copies of `foundations/inflation-nontermination/`) |
| `certificates/nontermination/` | frozen exact certificates `t1/t2/t3-defect.json`, `t2-full-lp.json`, `t2-corrupted-negative-control.json`, original `check.py` and `reconstruct.py` |
| `certificates/effective/` | frozen exact order-2 Farkas calibration (`farkas.json`, `check.py`) |
| `certificates/exponent/odd/` | extension threshold certificates (triangle `t = 11..13`, square `t = 11` AI) and degree-set checks for Proposition 4.12; `verify_odd.py` imports `../verify_exponent.py` |
| `certificates/beyond-finner/` | exact checks for Remark 6.3 (`verify_beyond_finner.py`): the identities behind the bound `F(P) >= -Σ(P)/n` ([A]) and sampled tests of the cubic certificates ([B]). Parts [C] and [D] check material from an earlier, longer version of Section 6.3 that was removed from the manuscript on 16 September 2026: a sampled test that an atomic Finner violation forces both triangle certificates to be nonnegative and that no fan inequality fails at any order for a law satisfying all eight atomic Finner inequalities, and three worked laws with their rejecting-order bounds. They still pass and are kept for provenance; the manuscript makes no claim that depends on them. |
| `certificates/hypergraph/` | reconstruction, transport and census checks for the companion paper on sources shared by three or more observers (`verify_hypergraph.py`, stored records under `certificates/`). This material belongs to that paper, not to the present manuscript; theorem numbers in the checker refer to the removed Section 7. |
| `verifiers/` | replay runner, hardened checkers (fail closed, refuse `-O`), `harden.py`, mutation tests, manifest generator |
| `replay_logs/` | fresh replay records with OS, architecture, Python, commands, wall times, hashes |
| `MANIFEST.json`, `SHA256SUMS` | identities of inputs, checkers and documentation; excludes mutable `replay_logs/` |

What the computer verifies: that the explicit defect-cube tables at orders 1–3
have the claimed symmetry, copied-triangle marginals, disjoint diagonal
supports and tensor-power diagonal law, that the order-2 full table satisfies
every NW linear constraint, and that the Finner gaps are the stated rationals.
The all-order theorem is proved analytically and does not depend on these
checks.
