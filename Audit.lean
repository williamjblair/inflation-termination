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

-- INF-D3.1: Definitions 3.1 to 3.5, Section 3.1
#print axioms TriangleInflation.Graph.gNWFeasible_of_gAIFeasible
#print axioms TriangleInflation.Graph.gAIFeasible_of_gExpFeasible
#print axioms TriangleInflation.Graph.gNWFeasible_triangle_iff
#print axioms TriangleInflation.Graph.gAIFeasible_triangle_iff
#print axioms TriangleInflation.Graph.gCompatible_triangle_iff

-- INF-P3.6: Proposition 3.6, soundness of the three tests
#print axioms TriangleInflation.Graph.compatible_gNWFeasible
#print axioms TriangleInflation.Graph.compatible_gAIFeasible
#print axioms TriangleInflation.Graph.compatible_gExpFeasible

-- INF-L3.9: Lemma 3.7 and Lemma 3.9, the root-sink lemma
#print axioms TriangleInflation.Graph.gExpFeasible_iff_gAIFeasible
#print axioms TriangleInflation.Graph.isAISet_iff_decomposition
#print axioms TriangleInflation.Graph.isAISet_glue
#print axioms TriangleInflation.Graph.RootSinkAux.exists_activeTrail
#print axioms TriangleInflation.Graph.RootSinkAux.gInjectable_iff_raw_of_one_le
#print axioms TriangleInflation.Graph.RootSinkAux.not_forall_gInjectable_iff_raw

-- INF-L3.10: Lemma 3.10, source-disjoint independence
#print axioms TriangleInflation.Graph.blockMarg_union_of_sourceDisjoint
#print axioms TriangleInflation.Graph.blockMarg_biUnion_of_sourceDisjoint
#print axioms TriangleInflation.Graph.gTwist_law

-- INF-L3.11: Lemma 3.11, induced-subgraph transport
#print axioms TriangleInflation.Graph.induced_transport
#print axioms TriangleInflation.Graph.transport_ai_feasible
#print axioms TriangleInflation.Graph.transport_compatible_restrict

-- INF-T4.2: Theorem 4.2, the classification, and Lemma 4.3, exhaustion
#print axioms TriangleInflation.Graph.classification_NW_lib
#print axioms TriangleInflation.Graph.classification_AI
#print axioms TriangleInflation.Graph.classification_exp
#print axioms TriangleInflation.Graph.nontermination_of_not_doubleStar
#print axioms TriangleInflation.Graph.exhaustion
#print axioms TriangleInflation.Graph.flip_full_support
#print axioms TriangleInflation.Graph.flip_gExpFeasible

-- INF-T5.1: Theorem 5.1, binary case, and Corollary 5.2
#print axioms TriangleInflation.Graph.doubleStar_terminates
#print axioms TriangleInflation.Graph.exists_dsStruct
#print axioms TriangleInflation.Graph.DSStruct.gCompatible_of_dsStruct
#print axioms TriangleInflation.Graph.centreLeaf_mass
#print axioms TriangleInflation.Graph.gCompatible_of_localDecoder

-- INF-L6.1: Lemmas 6.1 to 6.5, the cycle target and parity rigidity
#print axioms TriangleInflation.Graph.cycleTarget_isLaw
#print axioms TriangleInflation.Graph.cycleTarget_moment
#print axioms TriangleInflation.Graph.parity_rigidity

-- INF-T6.8: Lemma 6.6, Lemma 6.7 and Theorem 6.8, the cycle witness and its distance
#print axioms TriangleInflation.Graph.CycleModelAux.quant_rigidity
#print axioms TriangleInflation.Graph.cycle_witness
#print axioms TriangleInflation.Graph.cycle_exp_witness
#print axioms TriangleInflation.Graph.cycle_not_compatible
#print axioms TriangleInflation.Graph.cycle_distance

-- INF-L6.10: Lemma 6.10, the corrected Fourier density at m = 3
#print axioms TriangleInflation.Graph.triW_ge
#print axioms TriangleInflation.Graph.triW_nonneg
#print axioms TriangleInflation.Graph.triW_moment
#print axioms TriangleInflation.Graph.triDensity_isLaw
#print axioms TriangleInflation.Graph.triParity_isLaw

-- INF-T6.11: Theorem 6.12, the triangle witness at q = 1/(16t)
#print axioms TriangleInflation.Graph.triangle_linear_witness

-- INF-L7.3: Lemmas 7.2 and 7.3, Corollary 7.4 and Theorem 7.5, the five-observer path
#print axioms TriangleInflation.Graph.fivePathTarget_isLaw
#print axioms TriangleInflation.Graph.fivePathTarget_corr
#print axioms TriangleInflation.Graph.bilocal_of_compatible
#print axioms TriangleInflation.Graph.fivePath_not_compatible
#print axioms TriangleInflation.Graph.fivePath_distance
#print axioms TriangleInflation.Graph.fivePath_witness
#print axioms TriangleInflation.Graph.fivePath_exp_witness

/-! ## The triangle development -/

-- INF-D2.1: Definitions 2.1 and 2.2, Section 2.2
#print axioms TriangleInflation.nwFeasible_of_aiFeasible
#print axioms TriangleInflation.injectable_iff_injectableRaw

-- INF-C2.1: Section 2.1, the compatible set C_tri, finite and arbitrary latent alphabets
#print axioms TriangleInflation.finner_of_compatible
#print axioms TriangleInflation.TriangleCompatibleM
#print axioms TriangleInflation.triangleCompatibleM_of_triangleCompatible

-- INF-L8.4: Lemma 8.4
#print axioms TriangleInflation.indep_of_disjoint_support
#print axioms TriangleInflation.indep_of_disjoint_family
#print axioms TriangleInflation.line_inter_ancestors
#print axioms TriangleInflation.rootSupport_disjoint
#print axioms TriangleInflation.defect_independence
#print axioms TriangleInflation.defect_independence_family

-- INF-L8.5: Lemma 8.5 and equation (eq:s)
#print axioms TriangleInflation.defect_copiedTriangle_law
#print axioms TriangleInflation.one_sub_sParam_mul
#print axioms TriangleInflation.sParam_mem_Icc

-- INF-L8.6: Lemma 8.6
#print axioms TriangleInflation.defect_symmetric

-- INF-L8.7: Lemma 8.7, the Finner inequality
#print axioms TriangleInflation.finner_of_compatibleM

-- INF-L8.8: Lemma 8.8, the explicit violation
#print axioms TriangleInflation.witness_violation
#print axioms TriangleInflation.witness_not_compatible
#print axioms TriangleInflation.witness_not_compatibleM
#print axioms TriangleInflation.witness_margin

-- INF-L8.9: Lemma 8.9 and equation (eq:Rl)
#print axioms TriangleInflation.diagRegion_disjoint
#print axioms TriangleInflation.inDiagRegion_iff
#print axioms TriangleInflation.defect_diagonal_law

-- INF-T8.1: Theorem 8.1, with Section 8.3
#print axioms TriangleInflation.defectLaw_witnesses_AI
#print axioms TriangleInflation.membership_AI
#print axioms TriangleInflation.membership_NW

-- INF-T8.2: Theorem 8.2 and its corollary
#print axioms TriangleInflation.epsFam_mem
#print axioms TriangleInflation.main_membership
#print axioms TriangleInflation.main_violation
#print axioms TriangleInflation.main_violationM
#print axioms TriangleInflation.Pfam_isLaw
#print axioms TriangleInflation.no_finite_characterizing_order_lib
#print axioms TriangleInflation.no_finite_characterizing_orderM

-- INF-T9.1: Theorem 9.1, the fan inequalities
#print axioms TriangleInflation.fan_pointwise
#print axioms TriangleInflation.fan_first
#print axioms TriangleInflation.fan_second
#print axioms TriangleInflation.tminNW_le_of_finner_violation
#print axioms TriangleInflation.tminAI_le_of_finner_violation

-- INF-P9.2: Proposition 9.2, the family R_p
#print axioms TriangleInflation.Rlaw_not_compatible
#print axioms TriangleInflation.Rlaw_not_compatibleM
#print axioms TriangleInflation.nwFeasible_one
#print axioms TriangleInflation.aiFeasible_one
#print axioms TriangleInflation.Rlaw_not_nwFeasible_two
#print axioms TriangleInflation.Rlaw_tminNW
#print axioms TriangleInflation.Rlaw_tminAI

-- INF-P10.1: Proposition 10.1, finite parts
#print axioms TriangleInflation.Peps_aiFeasible
#print axioms TriangleInflation.Peps_nwFeasible
#print axioms TriangleInflation.Peps_not_nwFeasible
#print axioms TriangleInflation.Peps_not_compatible
#print axioms TriangleInflation.Peps_not_compatibleM
#print axioms TriangleInflation.Peps_tminNW_bounds
#print axioms TriangleInflation.Peps_tminAI_bounds

-- INF-P12.1: Proposition 12.1, equation (eq:nw-rate) for the triangle
#print axioms TriangleInflation.rate_triangle

-- INF-T6.16: Theorem 6.16 and Corollary 6.17, upper bounds, for the triangle
#print axioms TriangleInflation.tvDist
#print axioms TriangleInflation.rate_triangle_sharp
#print axioms TriangleInflation.tv_le_of_nwFeasible
#print axioms TriangleInflation.tv_le_sqrt_seven
