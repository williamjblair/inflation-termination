import TriangleInflation.Defs
import TriangleInflation.Finner
import TriangleInflation.FinnerMeasure
import TriangleInflation.Defect
import TriangleInflation.DefectLaw
import TriangleInflation.Main
import TriangleInflation.Fan
import TriangleInflation.Exponent
import TriangleInflation.Rate
import TriangleInflation.ConvexOrder
import TriangleInflation.Graph

/-!
# Inflation for classical pair-source networks

Definitions and theorems for the manuscript *Inflation for Classical Pair-Source Networks:
Termination and Quantitative Obstructions* (included under `paper/`). Every theorem in this
directory is proved; `Audit.lean` checks that the transitive axioms are `propext`,
`Classical.choice` and `Quot.sound` only.

Two developments live here. The triangle modules (`TriangleInflation/*.lean`) carry the
nontermination theorem for the classical triangle and the quantitative work around it, and
`FinnerMeasure.lean` upgrades the Finner inequality, and with it the nontermination theorem,
to arbitrary measurable latent spaces. The graph modules (`TriangleInflation/Graph/*.lean`)
carry the pair-source generalization and the classification theorem: a finite order of the
Navascués–Wolfe hierarchy characterizes compatibility exactly when every connected component
of the observed graph is a double star.

The formalization boundaries are recorded in the header of `TriangleInflation/Defs.lean`, in
the header of `TriangleInflation/Graph/Defs.lean` and in `README.md`.

The two registry statements are `Palomar/TriangleInflation/ClassificationChallenge.lean` and
`Palomar/TriangleInflation/Challenge.lean`, proved in
`PalomarSolutions/TriangleInflationClassification.lean` and
`PalomarSolutions/TriangleInflation.lean`.
-/
