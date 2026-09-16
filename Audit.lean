import TriangleInflation
import PalomarSolutions.TriangleInflation
import PalomarSolutions.TriangleInflationClassification

/-!
# Axiom audit

`#print axioms` for the two registry statements and for every library declaration the
manuscript's coverage table names. `scripts/check_axioms.sh` fails if any report mentions
`sorryAx` or an axiom outside `[propext, Classical.choice, Quot.sound]`.

The section headings are the identifiers of the coverage table in `README.md`, which carries
the paper statement each group covers.
-/

/-! ## The registry statements -/

-- The headline registry statement: the theorem Comparator compares against
-- `Palomar/TriangleInflation/ClassificationChallenge.lean`.
#print axioms TriangleInflation.Graph.classification_NW

-- The triangle registry statement: the theorem Comparator compares against
-- `Palomar/TriangleInflation/Challenge.lean`.
#print axioms TriangleInflation.no_finite_characterizing_order

/-! ## The pair-source graph development -/

-- Definitions 2.1 to 2.5, Section 2
#print axioms TriangleInflation.Graph.gNWFeasible_of_gAIFeasible
#print axioms TriangleInflation.Graph.gAIFeasible_of_gExpFeasible
#print axioms TriangleInflation.Graph.gNWFeasible_triangle_iff
#print axioms TriangleInflation.Graph.gAIFeasible_triangle_iff
#print axioms TriangleInflation.Graph.gCompatible_triangle_iff

-- Proposition 2.6, soundness of the three tests
#print axioms TriangleInflation.Graph.compatible_gNWFeasible
#print axioms TriangleInflation.Graph.compatible_gAIFeasible
#print axioms TriangleInflation.Graph.compatible_gExpFeasible

-- Lemma A.1 and Lemma 3.4, the trail criterion and the root-sink lemma
#print axioms TriangleInflation.Graph.gExpFeasible_iff_gAIFeasible
#print axioms TriangleInflation.Graph.isAISet_iff_decomposition
#print axioms TriangleInflation.Graph.isAISet_glue
#print axioms TriangleInflation.Graph.RootSinkAux.exists_activeTrail
#print axioms TriangleInflation.Graph.RootSinkAux.gInjectable_iff_raw_of_one_le
#print axioms TriangleInflation.Graph.RootSinkAux.not_forall_gInjectable_iff_raw

-- Lemma 3.5, source-disjoint independence
#print axioms TriangleInflation.Graph.blockMarg_union_of_sourceDisjoint
#print axioms TriangleInflation.Graph.blockMarg_biUnion_of_sourceDisjoint
#print axioms TriangleInflation.Graph.gTwist_law

-- Lemma 3.6, induced-subgraph transport
#print axioms TriangleInflation.Graph.induced_transport
#print axioms TriangleInflation.Graph.transport_ai_feasible
#print axioms TriangleInflation.Graph.transport_compatible_restrict

-- Theorem 3.2, the classification, and Lemma 3.7, exhaustion
#print axioms TriangleInflation.Graph.classification_NW_lib
#print axioms TriangleInflation.Graph.classification_AI
#print axioms TriangleInflation.Graph.classification_exp
#print axioms TriangleInflation.Graph.nontermination_of_not_doubleStar
#print axioms TriangleInflation.Graph.exhaustion
#print axioms TriangleInflation.Graph.flip_full_support
#print axioms TriangleInflation.Graph.flip_gExpFeasible

-- Theorem 3.10, binary case, and Corollary 3.11
#print axioms TriangleInflation.Graph.doubleStar_terminates
#print axioms TriangleInflation.Graph.exists_dsStruct
#print axioms TriangleInflation.Graph.DSStruct.gCompatible_of_dsStruct
#print axioms TriangleInflation.Graph.centreLeaf_mass
#print axioms TriangleInflation.Graph.gCompatible_of_localDecoder

-- Lemmas 3.14 to 3.18, the cycle target and parity rigidity
#print axioms TriangleInflation.Graph.cycleTarget_isLaw
#print axioms TriangleInflation.Graph.cycleTarget_moment
#print axioms TriangleInflation.Graph.parity_rigidity

-- Lemmas 3.19 and 3.20 and Theorem 3.21, the cycle witness and its distance
#print axioms TriangleInflation.Graph.CycleModelAux.quant_rigidity
#print axioms TriangleInflation.Graph.cycle_witness
#print axioms TriangleInflation.Graph.cycle_exp_witness
#print axioms TriangleInflation.Graph.cycle_not_compatible
#print axioms TriangleInflation.Graph.cycle_distance

-- Lemma 4.2, the corrected Fourier density at m = 3
#print axioms TriangleInflation.Graph.triW_ge
#print axioms TriangleInflation.Graph.triW_nonneg
#print axioms TriangleInflation.Graph.triW_moment
#print axioms TriangleInflation.Graph.triDensity_isLaw
#print axioms TriangleInflation.Graph.triParity_isLaw

-- Theorem 4.4, the triangle witness at q = 1/(16t)
#print axioms TriangleInflation.Graph.triangle_linear_witness

-- Theorem 4.3 (square witness) at the endpoint q = 1/(16t), corrected density m = 4, c = 5
#print axioms TriangleInflation.Graph.square_linear_witness

-- Lemmas 3.23 and 3.24, Corollary 3.25 and Theorem 3.26, the five-observer path
#print axioms TriangleInflation.Graph.fivePathTarget_isLaw
#print axioms TriangleInflation.Graph.fivePathTarget_corr
#print axioms TriangleInflation.Graph.bilocal_of_compatible
#print axioms TriangleInflation.Graph.fivePath_not_compatible
#print axioms TriangleInflation.Graph.fivePath_distance
#print axioms TriangleInflation.Graph.fivePath_witness
#print axioms TriangleInflation.Graph.fivePath_exp_witness

/-! ## The triangle development -/

-- Definitions 2.3 and 2.4 for the triangle, Section 2.3
#print axioms TriangleInflation.nwFeasible_of_aiFeasible
#print axioms TriangleInflation.injectable_iff_injectableRaw

-- Section 2.3, the compatible set C_tri, finite and arbitrary latent alphabets
#print axioms TriangleInflation.finner_of_compatible
#print axioms TriangleInflation.TriangleCompatibleM
#print axioms TriangleInflation.triangleCompatibleM_of_triangleCompatible

-- Lemma 5.4
#print axioms TriangleInflation.indep_of_disjoint_support
#print axioms TriangleInflation.indep_of_disjoint_family
#print axioms TriangleInflation.line_inter_ancestors
#print axioms TriangleInflation.rootSupport_disjoint
#print axioms TriangleInflation.defect_independence
#print axioms TriangleInflation.defect_independence_family

-- Lemma 5.5 and equation (eq:s)
#print axioms TriangleInflation.defect_copiedTriangle_law
#print axioms TriangleInflation.one_sub_sParam_mul
#print axioms TriangleInflation.sParam_mem_Icc

-- Lemma 5.6
#print axioms TriangleInflation.defect_symmetric

-- Lemma 5.7, the Finner inequality
#print axioms TriangleInflation.finner_of_compatibleM

-- Lemma 5.8, the explicit violation
#print axioms TriangleInflation.witness_violation
#print axioms TriangleInflation.witness_not_compatible
#print axioms TriangleInflation.witness_not_compatibleM
#print axioms TriangleInflation.witness_margin

-- Lemma 5.9 and equation (eq:Rl)
#print axioms TriangleInflation.diagRegion_disjoint
#print axioms TriangleInflation.inDiagRegion_iff
#print axioms TriangleInflation.defect_diagonal_law

-- Theorem 5.1, with Section 5.3
#print axioms TriangleInflation.defectLaw_witnesses_AI
#print axioms TriangleInflation.membership_AI
#print axioms TriangleInflation.membership_NW

-- Theorem 5.2 and its corollary
#print axioms TriangleInflation.epsFam_mem
#print axioms TriangleInflation.main_membership
#print axioms TriangleInflation.main_violation
#print axioms TriangleInflation.main_violationM
#print axioms TriangleInflation.Pfam_isLaw
#print axioms TriangleInflation.no_finite_characterizing_order_lib
#print axioms TriangleInflation.no_finite_characterizing_orderM

-- Theorem 5.11, the fan inequalities
#print axioms TriangleInflation.fan_pointwise
#print axioms TriangleInflation.fan_first
#print axioms TriangleInflation.fan_second
#print axioms TriangleInflation.tminNW_le_of_finner_violation
#print axioms TriangleInflation.tminAI_le_of_finner_violation

-- Proposition 5.12, the family R_p
#print axioms TriangleInflation.Rlaw_not_compatible
#print axioms TriangleInflation.Rlaw_not_compatibleM
#print axioms TriangleInflation.nwFeasible_one
#print axioms TriangleInflation.aiFeasible_one
#print axioms TriangleInflation.Rlaw_not_nwFeasible_two
#print axioms TriangleInflation.Rlaw_tminNW
#print axioms TriangleInflation.Rlaw_tminAI

-- Proposition 5.13, finite parts
#print axioms TriangleInflation.Peps_aiFeasible
#print axioms TriangleInflation.Peps_nwFeasible
#print axioms TriangleInflation.Peps_not_nwFeasible
#print axioms TriangleInflation.Peps_not_compatible
#print axioms TriangleInflation.Peps_not_compatibleM
#print axioms TriangleInflation.Peps_tminNW_bounds
#print axioms TriangleInflation.Peps_tminAI_bounds

-- Corollary 6.1, equation (eq:nw-rate) for the triangle
#print axioms TriangleInflation.rate_triangle

-- Theorem 4.8 and Corollary 4.9, upper bounds, for the triangle
#print axioms TriangleInflation.tvDist
#print axioms TriangleInflation.rate_triangle_sharp
#print axioms TriangleInflation.tv_le_of_nwFeasible
#print axioms TriangleInflation.tv_le_sqrt_seven
