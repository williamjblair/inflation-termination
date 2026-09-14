# Porting notes

This repository is a standalone extract of the inflation development that lives in the
author's working repository as `lean/ResourceTheory/Inflation/` and
`lean/ResourceTheory/InflationGraph/`. The extract exists because Palomar asks for a
self-contained repository pinned to a Mathlib commit on canonical `master`, and the working
repository is pinned elsewhere and carries six unrelated developments.

The two repositories build against different pins:

| | working repository | here |
|---|---|---|
| Lean | `leanprover/lean4:v4.33.1` | `leanprover/lean4:v4.33.0` |
| Mathlib | `0df444a360eaa60ab8c11dca51a86af692955474` | `db584cd6d46c92f209a44c0f1c829460d327499d` |

The pinned Mathlib commits are roughly a thousand apart. This file records every difference
between the sources in the two repositories, so that a reader can check that the extract is
the same mathematics.

## Sync of 2026-09-14

Sources: `lean/ResourceTheory/Inflation/*.lean` (10 modules) and
`lean/ResourceTheory/InflationGraph{,/*}.lean` (17 modules and an aggregator) of the working
repository, at the commit that added the pair-source development.

### Mechanical rewrites

Applied to every file, and nothing else was touched:

1. `ResourceTheory.InflationGraph` becomes `TriangleInflation.Graph`, in namespace lines,
   `end` lines, `import` lines and every qualified name. Files move from
   `ResourceTheory/InflationGraph/` to `TriangleInflation/Graph/`, and the aggregator
   `ResourceTheory/InflationGraph.lean` becomes `TriangleInflation/Graph.lean`.
2. `ResourceTheory.Inflation` becomes `TriangleInflation`, likewise. Files move from
   `ResourceTheory/Inflation/` to `TriangleInflation/`. The rewrite is applied in this
   order, since the first name extends the second.
3. The graph modules reach the triangle modules by the relative prefix `Inflation.`, which
   resolves inside `namespace ResourceTheory.InflationGraph` and does not resolve inside
   `namespace TriangleInflation.Graph`. Every such reference is made absolute:
   `Inflation.NWFeasible` becomes `TriangleInflation.NWFeasible`, and so on, in code and in
   doc comments. There were seven in code (`Triangle.lean`, `Cycles.lean`,
   `TriangleWitness.lean`) and five in prose.

### Deliberate content changes

4. `TriangleInflation/Defs.lean` drops its one project dependency. The working copy imports
   `ResourceTheory.Probability.Rational` for the bundled structure `RealDistribution`, and
   defines two one-line bridges, `isLaw_mass` and `ofIsLaw`, between that structure and the
   predicate `IsLaw`. Neither bridge is used anywhere in the inflation development. Here the
   import becomes `Mathlib.Tactic`, the two bridges are deleted, and the two sentences of
   the file header and of the `IsLaw` doc comment that mention `RealDistribution` are cut.
   This is what lets `Defs.lean` be copied verbatim into a Mathlib-only Challenge.
5. `TriangleInflation/Main.lean`: the theorem `no_finite_characterizing_order` is renamed
   `no_finite_characterizing_order_lib`, because the plain name is the one the registry
   Challenge and Solution declare and Comparator compares. Its doc comment gains a paragraph
   saying so.
6. `TriangleInflation/Graph/ClassificationTheorem.lean`: the theorem `classification_NW` is
   renamed `classification_NW_lib`, for the same reason, with the same added paragraph. The
   two references to the old name, in the module docstring and in the aggregator docstring,
   follow.
7. `TriangleInflation/Graph.lean` (the aggregator docstring): the working copy points at
   `lean/coverage/inflation-nontermination.json` and at the sibling library
   `InflationGraphOpen`, which holds the one statement of the pair-source sections that is
   not proved, the square witness `square_linear_witness`. Neither exists here. The
   paragraph now points at the Coverage table of `README.md` and says that the open
   statement is not part of this repository, because the verification gate refuses an
   unfinished proof outside the two Challenges. The wording also avoids the literal token
   the gate greps for.

### Changes that came from the working repository

8. `TriangleInflation/Rate.lean`: ten declarations lost their `private` marker upstream
   (`sum_ind_eq`, `sym_sum`, `marg_two`, `triCount`, `qLaw`, `qLaw_isLaw`,
   `qLaw_compatible`, `sum_ne_pair`, `expect_qLaw`, `exists_le_of_weighted`). They are
   needed by `ConvexOrder.lean`, which is new. Carried over as is. No statement changed.
9. `TriangleInflation/FinnerMeasure.lean` and `TriangleInflation/ConvexOrder.lean` are new
   modules, and so are the eighteen files under `TriangleInflation/Graph/`. The previous
   snapshot of this repository had none of them.

No statement of a previously registered declaration was changed. The registry statement
`TriangleInflation.no_finite_characterizing_order` is character for character what it was.

### Proof changes forced by the older Mathlib

None. The full development, all 28 modules, compiled at `v4.33.0` with Mathlib
`db584cd6` on the first attempt after the mechanical rewrites above, with no proof edit and
no new `set_option`. The `set_option maxHeartbeats 4000000` that
`TriangleInflation/Graph/FivePathWitness.lean` carries for its 32-point computation was
already in the source; that module takes about 135 s here, and is by a wide margin the
slowest.

The only build failures at any point were the unresolved `Inflation.` prefixes of item 3,
which are a consequence of the namespace rewrite and not of the Mathlib version.

### Not ported

`lean/InflationGraphOpen/` of the working repository. It contains one statement,
`square_linear_witness` (paper Theorem 6.11), with an unfinished proof. The gate here
refuses that outside the two Challenge files, and the manuscript's non-claims document
already records the statement as unproved.

## How to redo the sync

The rewrites of items 1 to 3 are textual and can be replayed with two string substitutions
and one word-boundary regular expression, in the order given. Items 4 to 7 are five small
patches, listed above with their exact content. After copying, run

```bash
lake build && bash scripts/check_axioms.sh
```

and regenerate the Challenges if a definitions file moved:

```bash
python3 scripts/gen_challenge.py
```
