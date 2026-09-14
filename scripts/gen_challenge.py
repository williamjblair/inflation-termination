#!/usr/bin/env python3
"""Generate the Palomar Challenge files from the library's definition files.

Palomar's Comparator exports the Challenge statement and the Solution statement and
compares them constant by constant: every constant occurring in the statement has to be
identical, by name and by definition body, in the two import closures. A Challenge may
import Mathlib only, so it cannot import the library; it must therefore carry the
definitions itself. Generating each Challenge mechanically from the library's definition
files is what keeps the two copies identical.

Two Challenges are generated.

`Palomar/TriangleInflation/Challenge.lean` (the triangle nontermination theorem) is

    the Mathlib imports of TriangleInflation/Defs.lean
    a Challenge-specific module docstring
    the body of Defs.lean verbatim, from `namespace TriangleInflation` to its `end`
    the registry theorem, stated and left as `sorry`

`Palomar/TriangleInflation/ClassificationChallenge.lean` (the classification theorem) is

    the Mathlib imports of both definition files
    a Challenge-specific module docstring
    the body of TriangleInflation/Defs.lean verbatim, as above
    the declarations of TriangleInflation/Graph/Defs.lean that the statement needs,
      each copied verbatim and in file order, inside `namespace TriangleInflation.Graph`
    the registry theorem, stated and left as `sorry`

The second Challenge carries a selection rather than the whole graph definitions file
because that file also defines the recursively expressible closure, the named scenarios and
the explicit targets, none of which the classification statement mentions. The selection is
by declaration head, and a head that matches no declaration, or more than one, is an error:
a rename in the library fails the generator rather than silently dropping a definition.

Run from the repository root:

    python3 scripts/gen_challenge.py          # write the files
    python3 scripts/gen_challenge.py --check  # exit 1 if a file on disk is stale
"""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFS = ROOT / "TriangleInflation" / "Defs.lean"
GRAPH_DEFS = ROOT / "TriangleInflation" / "Graph" / "Defs.lean"

TRI_OUT = ROOT / "Palomar" / "TriangleInflation" / "Challenge.lean"
CLS_OUT = ROOT / "Palomar" / "TriangleInflation" / "ClassificationChallenge.lean"

TRI_NS_OPEN = "namespace TriangleInflation\n"
TRI_NS_CLOSE = "end TriangleInflation\n"
GRAPH_NS_OPEN = "namespace TriangleInflation.Graph\n"
GRAPH_NS_CLOSE = "end TriangleInflation.Graph\n"

# The declarations of TriangleInflation/Graph/Defs.lean that the classification statement
# needs, in file order, grouped under headings written here. Each entry is the head of a
# declaration in that file; the generator copies the whole declaration, doc comment
# included, verbatim.
GRAPH_EXTRACT: list[tuple[str, list[str]]] = [
    ("/-! ### Pair-source scenarios -/", [
        "structure PairGraph where",
        "attribute [instance] PairGraph.fintypeV",
        "abbrev PairGraph.Edge",
        "def PairGraph.inc",
        "abbrev GTarget",
    ]),
    ("/-! ### Order-`t` copied observations -/", [
        "abbrev GObs",
        "abbrev GAssign",
        "variable {Γ : PairGraph} {t : ℕ}",
        "def gPerm",
        "def gRelabel",
        "def GSymmetric",
    ]),
    ("/-! ### The copied original scenarios and the diagonal rows -/", [
        "def copyObs",
        "def readCopy",
        "def readDiag",
        "def gTensorPow",
    ]),
    ("/-! ### The order-`t` Navascués–Wolfe test -/", [
        "def GNWFeasible",
    ]),
    ("/-! ### Compatibility -/", [
        "structure GModel",
        "attribute [instance] GModel.fintypeL",
        "def GModel.Valid",
        "def GModel.law",
        "def GCompatible",
    ]),
    ("/-! ### Double-star forests -/", [
        "def IsDoubleStarForest",
    ]),
]

TRI_DOCSTRING = '''/-!
# Nontermination of the inflation hierarchy for the classical triangle

*For every finite order `t` of the Navascués–Wolfe inflation hierarchy for the classical
triangle scenario, there is a three-bit law that passes the order-`t` test, including the
ancestral-independence prescriptions, and is nevertheless not triangle compatible.*

Equivalently: no finite level of the hierarchy characterizes the triangle-compatible set
`C_tri`, so the hierarchy does not terminate. The witnesses are the explicit family
`P_t = Q(ε_t, r_t)` with `ε_t = 1/(2t³)` and `r_t = (1 - ε_t)^(t-1)`; membership comes from an
explicit defect-cube inflation law, and incompatibility from the Finner inequality
`P(000)² ≤ P_A(0) P_B(0) P_C(0)`, which `P_t` violates by at least `ε_t²/2`.

This is Theorem 8.2 and its corollary in *Inflation for Classical Pair-Source Networks:
Termination and Quantitative Obstructions* (William Blair, manuscript, 2026), included
under `paper/`; the construction is Section 8.1, the incompatibility Section 8.2. The
triangle is the smallest scenario the classification theorem
(`Palomar/TriangleInflation/ClassificationChallenge.lean`) puts on the nonterminating side,
and this theorem is the quantitative form of that case.

## Recorded formalization boundaries

* **Finite latent alphabets.** `TriangleCompatible` quantifies over `TriangleModel`s whose
  three latent spaces are `Fintype`s, where the paper (Section 2) allows arbitrary
  measurable latent spaces. The reduction to bounded finite alphabets for the triangle
  (Rosset, Gisin and Wolfe, 2018) is quoted in the paper and is **not** formalized. The
  formal `TriangleCompatible` is therefore a priori a subset of the paper's `C_tri`, which
  is the safe direction here: `¬ TriangleCompatible P` is the weaker of the two readings,
  and it is what the theorem asserts. The library also proves the arbitrary-latent-space
  form of this theorem, in `TriangleInflation/FinnerMeasure.lean`; the registry statement
  is deliberately the elementary one.
* **The recursively expressible hierarchy is not formalized on the triangle.** The paper's
  `I^exp_t` (Definition 2.3) needs `d`-separation in the inflated causal graph and the
  Wolfe–Spekkens–Fritz recursion; that machinery lives in the graph development,
  `TriangleInflation/Graph/`, not in the triangle module. Only `I^NW_t` (`NWFeasible`) and
  `I^AI_t` (`AIFeasible`) are defined here. Since `I^exp_t ⊆ I^AI_t ⊆ I^NW_t`, the
  membership assertions below are the weaker halves of the paper's claims.
* Laws are bare real weight functions on finite types, not Mathlib `Measure`s or `PMF`s;
  the further representational decisions are recorded in the header of
  `TriangleInflation/Defs.lean`, which the definitions below reproduce verbatim.

## How to read this file

Everything between `namespace TriangleInflation` and `end TriangleInflation`, up to the
theorem, is copied character for character from `TriangleInflation/Defs.lean` by
`scripts/gen_challenge.py`, so that the constants of the statement are the same objects the
Solution proves about. The single declaration to audit is the last one.
-/
'''

TRI_THEOREM = '''/-- **Nontermination of the inflation hierarchy for the classical triangle.**

For every order `t ≥ 1` there is a three-bit law `P` which is a probability law, which is
ancestral-independence feasible at order `t` (`AIFeasible t P`, the stronger of the two
formalized tests), which is Navascués–Wolfe feasible at order `t` (`NWFeasible t P`), and
which is not triangle compatible (`¬ TriangleCompatible P`).

So no finite order of the hierarchy characterizes the triangle-compatible set: whatever
order `t` is chosen, the order-`t` test admits a law that no triangle model produces.
Paper Theorem 8.2 and the corollary that follows it. -/
theorem no_finite_characterizing_order (t : ℕ) (ht : 1 ≤ t) :
    ∃ P : ThreeBit → ℝ, IsLaw P ∧ AIFeasible t P ∧ NWFeasible t P ∧ ¬ TriangleCompatible P := by
  sorry
'''

CLS_DOCSTRING = '''/-!
# Which pair-source networks does inflation terminate on?

*For a pair-source scenario with binary observed variables, some finite order of the
Navascués–Wolfe inflation hierarchy characterizes compatibility if and only if every
connected component of the observed graph is a double star, and when it does, order two
already suffices.*

A pair-source scenario is a finite simple graph `G` without isolated vertices: one binary
observed variable per vertex, one independent latent source per edge, each source shared by
the two endpoints of its edge. A double star is a tree of diameter at most three, so
`IsDoubleStarForest G` says that `G` is acyclic and that any two reachable vertices are at
distance at most three.

The statement below is the "only if" and the "if" at once. Reading it left to right: if some
order `t ≥ 1` of the hierarchy equals the compatible set, then every component is a double
star. Reading it right to left: if every component is a double star, then some order does,
and the proof supplies `t = 2`.

This is Theorem 4.2 in *Inflation for Classical Pair-Source Networks: Termination and
Quantitative Obstructions* (William Blair, manuscript, 2026), included under `paper/`
(Section 4). The nonterminating half rests on explicit targets that pass the order-`t` test
at every `t` and are incompatible: a parity target on every induced cycle (Section 6) and a
bilocal target on the five-observer path (Section 7), moved to the ambient graph by
induced-subgraph transport and made strictly positive by independent local flips. The
terminating half reconstructs a model on a double star from its order-two inflation
(Section 5). The triangle case, sharpened to an explicit family with a quantitative
violation margin, is the companion registry statement
`Palomar/TriangleInflation/Challenge.lean`.

## Recorded formalization boundaries

* **Binary observed variables.** Outcomes are `Bool`. The paper's Remark 4.4 extends the
  classification to any fixed finite observed alphabets; that transfer is **not**
  formalized.
* **Finite latent alphabets.** `GCompatible` quantifies over a `GModel`, whose latent
  alphabets are `Fintype`s, where the mathematics allows arbitrary measurable latent
  spaces. The formal compatible set is therefore a priori a subset of the general one, so
  in the nonterminating direction `¬ GCompatible Γ P` is the weaker reading. The
  arbitrary-latent form is proved only for the triangle defect family, in
  `TriangleInflation/FinnerMeasure.lean`.
* Laws are bare real weight functions on finite types with the predicate `IsLaw`, not
  Mathlib `Measure`s or `PMF`s; all inequalities are real-valued. The further
  representational decisions are recorded in the headers of `TriangleInflation/Defs.lean`
  and `TriangleInflation/Graph/Defs.lean`.

## How to read this file

Everything between `namespace TriangleInflation` and its `end` is copied character for
character from `TriangleInflation/Defs.lean`. The declarations inside `namespace
TriangleInflation.Graph` are copied character for character from
`TriangleInflation/Graph/Defs.lean`: they are the ones the statement needs, in the order
that file gives them. Both copies are made by `scripts/gen_challenge.py`, so that the
constants of the statement are the same objects the Solution proves about. The single
declaration to audit is the last one.
-/
'''

CLS_THEOREM = '''open TriangleInflation TriangleInflation.Graph in
/-- **The termination classification for pair-source networks.**

Some finite order of the Navascués–Wolfe hierarchy characterizes compatibility for the
pair-source scenario `Γ` exactly when every connected component of its graph is a double
star, that is, a tree of diameter at most three.

The first conjunct, left to right, is the nontermination half: a graph with any other
component carries, at every order `t ≥ 1`, a law that passes the order-`t` test and has no
model. Right to left it is the reconstruction half. The second conjunct is the order stated
in the paper: on a double-star forest the order-two test already characterizes
compatibility.

Paper Theorem 4.2. -/
theorem TriangleInflation.Graph.classification_NW (Γ : PairGraph) :
    ((∃ t : ℕ, 1 ≤ t ∧ ∀ P : GTarget Γ, IsLaw P → (GNWFeasible Γ t P ↔ GCompatible Γ P))
      ↔ IsDoubleStarForest Γ.G) ∧
    (IsDoubleStarForest Γ.G →
      ∀ P : GTarget Γ, IsLaw P → (GNWFeasible Γ 2 P ↔ GCompatible Γ P)) := by
  sorry
'''


def mathlib_imports(path: pathlib.Path, carried: set[str]) -> list[str]:
    """The import lines of `path`, with imports of the carried modules dropped.

    Anything else that is not a Mathlib module is an error: a Challenge may import
    Mathlib only, and every project definition has to be carried in the file itself.
    """
    lines = []
    for line in path.read_text().splitlines(keepends=True):
        if line.startswith("import "):
            lines.append(line)
        elif lines and line.strip() == "":
            continue
        elif lines:
            break
    kept = []
    for line in lines:
        module = line.split()[1]
        if module in carried:
            continue
        if not module.startswith("Mathlib"):
            sys.exit(f"gen_challenge: {path.name} imports {module}; a Challenge may import "
                     "Mathlib only")
        kept.append(line)
    return kept


def namespace_body(path: pathlib.Path, open_line: str, close_line: str) -> str:
    """The text of `path` from its namespace line up to the final `end`, verbatim."""
    text = path.read_text()
    start = text.index(open_line)
    end = text.rindex(close_line)
    body = text[start:end]
    if not body.endswith("\n\n"):
        body = body.rstrip("\n") + "\n\n"
    return body


def chunks(body: str) -> list[str]:
    """Split a namespace body into blank-line-separated declaration blocks."""
    return [c for c in body.split("\n\n") if c.strip()]


def extract(path: pathlib.Path, open_line: str, close_line: str,
            groups: list[tuple[str, list[str]]]) -> str:
    """The selected declarations of `path`, verbatim, in file order, under headings."""
    blocks = chunks(namespace_body(path, open_line, close_line))
    out: list[str] = []
    for heading, heads in groups:
        out.append(heading)
        for head in heads:
            hits = [b for b in blocks
                    if any(line.startswith(head) for line in b.splitlines())]
            if len(hits) != 1:
                sys.exit(f"gen_challenge: {len(hits)} declarations in {path.name} start with "
                         f"{head!r}, expected exactly 1")
            out.append(hits[0])
    return "\n\n".join(out) + "\n\n"


def build_triangle() -> str:
    imports = mathlib_imports(DEFS, carried=set())
    body = namespace_body(DEFS, TRI_NS_OPEN, TRI_NS_CLOSE)
    return "".join(imports) + "\n" + TRI_DOCSTRING + "\n" + body + TRI_THEOREM + "\n" \
        + TRI_NS_CLOSE


def build_classification() -> str:
    imports = mathlib_imports(DEFS, carried=set())
    for line in mathlib_imports(GRAPH_DEFS, carried={"TriangleInflation.Defs"}):
        if line not in imports:
            imports.append(line)
    tri_body = namespace_body(DEFS, TRI_NS_OPEN, TRI_NS_CLOSE)
    graph_body = extract(GRAPH_DEFS, GRAPH_NS_OPEN, GRAPH_NS_CLOSE, GRAPH_EXTRACT)
    # The graph body keeps its own `open` line, so that the copied declarations elaborate
    # exactly as they do in the library.
    graph_open = "open Finset TriangleInflation\n\n"
    return ("".join(imports) + "\n" + CLS_DOCSTRING + "\n"
            + tri_body + TRI_NS_CLOSE + "\n"
            + GRAPH_NS_OPEN + "\n" + graph_open + graph_body + GRAPH_NS_CLOSE + "\n"
            + CLS_THEOREM)


TARGETS = [(TRI_OUT, build_triangle), (CLS_OUT, build_classification)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if a file on disk differs from the generated one")
    args = parser.parse_args()

    failed = False
    for out, build in TARGETS:
        generated = build()
        rel = out.relative_to(ROOT)
        if args.check:
            if not out.exists() or out.read_text() != generated:
                print(f"FAIL: {rel} is stale; run python3 scripts/gen_challenge.py",
                      file=sys.stderr)
                failed = True
            else:
                print(f"PASS: {rel} matches the library definitions")
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(generated)
            print(f"wrote {rel} ({len(generated.splitlines())} lines)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
