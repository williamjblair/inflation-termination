# Binary-triangle inflation complexity

Pinned upstream revision: `768d404c631659574d9fad232c028df4f63fbc3b` of `williamjblair/resource-theory`.

Main theorem: for the maintained rare common-defect family, the first rejecting order of each of the NW, AI-product, and expressible-set strengthened hierarchies is Theta(epsilon^(-1/3)). The asymptotic lower constant is 1/2, and the upper constant is at most 4-2 sqrt(3). The exact limiting constant is not determined.

Read `REPORT.md` for the theorem and proofs. `AUDIT.md` separates the inspected baseline from the new derivations, and records limitations of the audit. This packet does not modify the upstream repository and is not an external referee endorsement or a priority certificate.

## Reproduce

Python 3.10 or later, standard library only:

```sh
python3 generate_certificates.py
python3 verify_certificates.py
python3 -O verify_certificates.py
```

The generator and checker are separate programs. The checker uses explicit exceptions, not `assert`, so optimization does not disable validation. It checks 14 rational targets, an all-order nonnegative-polynomial certificate with five integer cases, exhaustive finite assignments, count-orbit reductions, ancestry/permutation embeddings, and eight negative controls.

`certificates.json` contains exact rational passing and rejecting certificates. The first crossing of the displayed fan inequality is not generally the first rejection of the complete inflation LP. When the passing lower bound equals the rejecting upper bound, the first order is determined by the sandwich, without solving the full LP.

`verification.json` records the checks actually executed. `SHA256SUMS` hashes the delivered packet; upstream Git blob identifiers in `AUDIT.md` are metadata read from GitHub and are not represented as locally recomputed SHA-256 digests.
