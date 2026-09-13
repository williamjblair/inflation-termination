import TriangleInflation.Defs
import TriangleInflation.Finner
import TriangleInflation.Defect
import TriangleInflation.DefectLaw
import TriangleInflation.Main
import TriangleInflation.Fan
import TriangleInflation.Exponent
import TriangleInflation.Rate

/-!
# Inflation for the classical triangle

Definitions and theorems for the manuscript *Inflation for the Classical Triangle:
Nontermination and Quantitative Complexity* (included under `paper/`). Every theorem in this
directory is proved; `Audit.lean` checks that the transitive axioms are `propext`,
`Classical.choice` and `Quot.sound` only. The formalization boundaries (finite latent
alphabets in `TriangleCompatible`, the recursively expressible hierarchy left out, the first
rejecting order defined as an infimum) are recorded in the header of
`TriangleInflation/Defs.lean` and in `README.md`.

The registry statement of the headline result is `Palomar/TriangleInflation/Challenge.lean`,
proved in `PalomarSolutions/TriangleInflation.lean`.
-/
