#!/usr/bin/env python3
"""Generate Palomar/TriangleInflation/Challenge.lean from TriangleInflation/Defs.lean.

Palomar's Comparator exports the Challenge statement and the Solution statement and
compares them constant by constant: every constant occurring in the statement has to be
identical, by name and by definition body, in the two import closures. The Challenge may
import Mathlib only, so it cannot import the library; it must therefore carry the
definitions itself. Generating it mechanically from the library's definitions file is what
keeps the two copies identical.

The generated file is

    the Mathlib imports of Defs.lean
    a Challenge-specific module docstring
    the body of Defs.lean verbatim, from `namespace TriangleInflation` to its `end`
    the registry theorem, stated and left as `sorry`

Run from the repository root:

    python3 scripts/gen_challenge.py          # write the file
    python3 scripts/gen_challenge.py --check  # exit 1 if the file on disk is stale
"""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFS = ROOT / "TriangleInflation" / "Defs.lean"
OUT = ROOT / "Palomar" / "TriangleInflation" / "Challenge.lean"

NAMESPACE_OPEN = "namespace TriangleInflation\n"
NAMESPACE_CLOSE = "end TriangleInflation\n"

DOCSTRING = '''/-!
# Nontermination of the inflation hierarchy for the classical triangle

*For every finite order `t` of the Navascués–Wolfe inflation hierarchy for the classical
triangle scenario, there is a three-bit law that passes the order-`t` test — including the
ancestral-independence prescriptions — and is nevertheless not triangle compatible.*

Equivalently: no finite level of the hierarchy characterizes the triangle-compatible set
`C_tri`, so the hierarchy does not terminate. The witnesses are the explicit family
`P_t = Q(ε_t, r_t)` with `ε_t = 1/(2t³)` and `r_t = (1 - ε_t)^(t-1)`; membership comes from an
explicit defect-cube inflation law, and incompatibility from the Finner inequality
`P(000)² ≤ P_A(0) P_B(0) P_C(0)`, which `P_t` violates by at least `ε_t²/2`.

This is Theorem 3.2 and its corollary in *Inflation for the Classical Triangle:
Nontermination and Quantitative Complexity* (William Blair, manuscript, 2026), included
under `paper/`; the construction is Section 3.1, the incompatibility Section 3.2.

## Recorded formalization boundaries

* **Finite latent alphabets.** `TriangleCompatible` quantifies over `TriangleModel`s whose
  three latent spaces are `Fintype`s, where the paper (Section 2) allows arbitrary
  measurable latent spaces. The reduction to bounded finite alphabets for the triangle
  (Rosset, Gisin and Wolfe, 2018) is quoted in the paper and is **not** formalized. The
  formal `TriangleCompatible` is therefore a priori a subset of the paper's `C_tri`, which
  is the safe direction here: `¬ TriangleCompatible P` is the weaker of the two readings,
  and it is what the theorem asserts.
* **The recursively expressible hierarchy is not formalized.** The paper's `I^exp_t`
  (Definition 2.3) needs `d`-separation in the inflated causal graph and the
  Wolfe–Spekkens–Fritz recursion; that machinery is out of scope. Only `I^NW_t`
  (`NWFeasible`) and `I^AI_t` (`AIFeasible`) are defined. Since
  `I^exp_t ⊆ I^AI_t ⊆ I^NW_t`, the membership assertions below are the weaker halves of
  the paper's claims.
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

THEOREM = '''/-- **Nontermination of the inflation hierarchy for the classical triangle.**

For every order `t ≥ 1` there is a three-bit law `P` which is a probability law, which is
ancestral-independence feasible at order `t` (`AIFeasible t P`, the stronger of the two
formalized tests), which is Navascués–Wolfe feasible at order `t` (`NWFeasible t P`), and
which is not triangle compatible (`¬ TriangleCompatible P`).

So no finite order of the hierarchy characterizes the triangle-compatible set: whatever
order `t` is chosen, the order-`t` test admits a law that no triangle model produces.
Paper Theorem 3.2 and the corollary that follows it. -/
theorem no_finite_characterizing_order (t : ℕ) (ht : 1 ≤ t) :
    ∃ P : ThreeBit → ℝ, IsLaw P ∧ AIFeasible t P ∧ NWFeasible t P ∧ ¬ TriangleCompatible P := by
  sorry
'''


def build() -> str:
    text = DEFS.read_text()

    imports = []
    for line in text.splitlines(keepends=True):
        if line.startswith("import "):
            imports.append(line)
        elif imports and line.strip() == "":
            continue
        elif imports:
            break
    for line in imports:
        module = line.split()[1]
        if not module.startswith("Mathlib"):
            sys.exit(f"gen_challenge: Defs.lean imports {module}; a Challenge may import "
                     "Mathlib only")

    start = text.index(NAMESPACE_OPEN)
    end = text.rindex(NAMESPACE_CLOSE)
    body = text[start:end]          # namespace line through the last declaration
    if not body.endswith("\n\n"):
        body = body.rstrip("\n") + "\n\n"

    return "".join(imports) + "\n" + DOCSTRING + "\n" + body + THEOREM + "\n" + NAMESPACE_CLOSE


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if the file on disk differs from the generated one")
    args = parser.parse_args()

    generated = build()
    if args.check:
        if not OUT.exists() or OUT.read_text() != generated:
            print(f"FAIL: {OUT.relative_to(ROOT)} is stale; run python3 scripts/gen_challenge.py",
                  file=sys.stderr)
            return 1
        print(f"PASS: {OUT.relative_to(ROOT)} matches TriangleInflation/Defs.lean")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(generated)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(generated.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
