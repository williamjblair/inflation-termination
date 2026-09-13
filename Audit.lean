import TriangleInflation
import PalomarSolutions.TriangleInflation

/-!
# Axiom audit

`#print axioms` for the registry statement and for every library theorem the manuscript's
coverage table names. `scripts/check_axioms.sh` fails if any report mentions `sorryAx` or an
axiom outside `[propext, Classical.choice, Quot.sound]`.
-/

-- The registry statement: the theorem Comparator compares against
-- `Palomar/TriangleInflation/Challenge.lean`.
#print axioms TriangleInflation.no_finite_characterizing_order

-- INF-D2.1: Definitions 2.1 and 2.2 (def:NW, def:AI), Section 2.2
#print axioms TriangleInflation.nwFeasible_of_aiFeasible
#print axioms TriangleInflation.injectable_iff_injectableRaw

-- INF-C2.1: Section 2.1, the compatible set C_tri
#print axioms TriangleInflation.finner_of_compatible

-- INF-L3.3: Lemma 3.3 (lem:disjoint)
#print axioms TriangleInflation.indep_of_disjoint_support
#print axioms TriangleInflation.indep_of_disjoint_family
#print axioms TriangleInflation.line_inter_ancestors
#print axioms TriangleInflation.rootSupport_disjoint
#print axioms TriangleInflation.defect_independence
#print axioms TriangleInflation.defect_independence_family

-- INF-L3.4: Lemma 3.4 (lem:triangle-law) and equation (eq:s)
#print axioms TriangleInflation.defect_copiedTriangle_law
#print axioms TriangleInflation.one_sub_sParam_mul
#print axioms TriangleInflation.sParam_mem_Icc

-- INF-L3.5: Lemma 3.5 (lem:symmetry)
#print axioms TriangleInflation.defect_symmetric

-- INF-L3.8: Lemma 3.8 (lem:violation)
#print axioms TriangleInflation.witness_violation
#print axioms TriangleInflation.witness_not_compatible
#print axioms TriangleInflation.witness_margin

-- INF-L3.9: Lemma 3.9 (lem:diag) and equation (eq:Rl)
#print axioms TriangleInflation.diagRegion_disjoint
#print axioms TriangleInflation.inDiagRegion_iff
#print axioms TriangleInflation.defect_diagonal_law

-- INF-T3.1: Theorem 3.1 (thm:membership), with Section 3.3
#print axioms TriangleInflation.defectLaw_witnesses_AI
#print axioms TriangleInflation.membership_AI
#print axioms TriangleInflation.membership_NW

-- INF-T3.2: Theorem 3.2 (thm:main) and its corollary
#print axioms TriangleInflation.epsFam_mem
#print axioms TriangleInflation.main_membership
#print axioms TriangleInflation.main_violation
#print axioms TriangleInflation.Pfam_isLaw
#print axioms TriangleInflation.no_finite_characterizing_order_lib

-- INF-T4.1: Theorem 4.1 (thm:fan), equations (eq:fan), (eq:fan-pointwise), (eq:fan-order)
#print axioms TriangleInflation.fan_pointwise
#print axioms TriangleInflation.fan_first
#print axioms TriangleInflation.fan_second
#print axioms TriangleInflation.tminNW_le_of_finner_violation
#print axioms TriangleInflation.tminAI_le_of_finner_violation

-- INF-P4.2: Proposition 4.2 (prop:Rp)
#print axioms TriangleInflation.Rlaw_not_compatible
#print axioms TriangleInflation.nwFeasible_one
#print axioms TriangleInflation.aiFeasible_one
#print axioms TriangleInflation.Rlaw_not_nwFeasible_two
#print axioms TriangleInflation.Rlaw_tminNW
#print axioms TriangleInflation.Rlaw_tminAI

-- INF-P5.1: Proposition 5.1 (prop:family), finite parts
#print axioms TriangleInflation.Peps_aiFeasible
#print axioms TriangleInflation.Peps_nwFeasible
#print axioms TriangleInflation.Peps_not_nwFeasible
#print axioms TriangleInflation.Peps_not_compatible
#print axioms TriangleInflation.Peps_tminNW_bounds
#print axioms TriangleInflation.Peps_tminAI_bounds

-- INF-P7.1: Proposition 7.1 (prop:promised), equation (eq:nw-rate) for the triangle
#print axioms TriangleInflation.rate_triangle
