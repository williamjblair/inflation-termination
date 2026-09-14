# Exact small-order certificates

`t1-defect.json`, `t2-defect.json`, and `t3-defect.json` are exact generative
certificates for the defect-cube law.  The validator checks nonnegativity,
normalization, covariance under every adjacent-transposition generator of
`S_t^3`, all `t^3` copied-triangle marginals, mutual disjointness of the full
diagonal root supports, all `8^t` diagonal equations, and the exact Finner
gap.

`t2-full-lp.json` is a sparse full-table LP witness reconstructed independently
by enumerating all 256 order-two defect cubes.  It lists 166 nonzero
coordinates out of 4096.  `check.py` does not import the reconstructor: it
treats the JSON as an untrusted LP vector and directly checks normalization,
nonnegativity, all 12,288 generator-coordinate symmetry equations, and all 64
diagonal equations.

`t2-corrupted-negative-control.json` moves one denominator unit from the
all-one atom to the all-zero atom.  It remains normalized and nonnegative, but
the validator rejects its diagonal marginal.

Run `../reproduce.sh` from any directory.  All arithmetic uses Python integers
and `fractions.Fraction`; no LP solver or floating-point comparison is used.
