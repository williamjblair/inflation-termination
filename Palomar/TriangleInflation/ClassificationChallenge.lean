import Mathlib.Algebra.BigOperators.Field
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic.DeriveFintype
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Combinatorics.SimpleGraph.Metric
import Mathlib.Data.List.Chain

/-!
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

namespace TriangleInflation

open Finset

/-! ## Laws as weight functions -/

/-- A probability weight function on a finite type: nonnegative and summing to one. -/
def IsLaw {α : Type*} [Fintype α] (w : α → ℝ) : Prop :=
  (∀ a, 0 ≤ w a) ∧ ∑ a, w a = 1

/-- Pushforward of a weight function along a map of finite types. -/
def pushforward {α β : Type*} [Fintype α] [DecidableEq β] (w : α → ℝ) (F : α → β) : β → ℝ :=
  fun b => ∑ a : α, if F a = b then w a else 0

/-- The product of independent per-coordinate weight functions on `ι → Bool`. -/
def prodLaw {ι : Type*} [Fintype ι] (w : ι → Bool → ℝ) : (ι → Bool) → ℝ :=
  fun x => ∏ i, w i (x i)

/-! ## Three-bit laws -/

/-- The outcome type of the triangle: the three observed bits `(A, B, C)`.
`false` is the paper's outcome `0`. -/
abbrev ThreeBit := Bool × Bool × Bool

/-- The three observed parties of the triangle. -/
inductive Party
  | A | B | C
  deriving DecidableEq, Repr

/-- The bit that a party reads off a three-bit outcome. -/
def partyBit : Party → ThreeBit → Bool
  | .A, w => w.1
  | .B, w => w.2.1
  | .C, w => w.2.2

/-- `P(000)`: the all-zero atom. -/
def atom000 (P : ThreeBit → ℝ) : ℝ := P (false, false, false)

/-- `P_A(0)`: the zero marginal of the first bit. -/
def margA (P : ThreeBit → ℝ) : ℝ := ∑ y : Bool, ∑ z : Bool, P (false, y, z)

/-- `P_B(0)`: the zero marginal of the second bit. -/
def margB (P : ThreeBit → ℝ) : ℝ := ∑ x : Bool, ∑ z : Bool, P (x, false, z)

/-- `P_C(0)`: the zero marginal of the third bit. -/
def margC (P : ThreeBit → ℝ) : ℝ := ∑ x : Bool, ∑ y : Bool, P (x, y, false)

/-- The `t`-fold tensor power `P^{⊗t}`, as a law on `Fin t → ThreeBit`. -/
def tensorPow (t : ℕ) (P : ThreeBit → ℝ) : (Fin t → ThreeBit) → ℝ :=
  fun v => ∏ l : Fin t, P (v l)

/-! ## The copied observations of the order-`t` inflation

Paper Section 2.2. `A^{ij}` has `X`-index `i` and `Z`-index `j`; `B^{ik}` has `X`-index `i`
and `Y`-index `k`; `C^{jk}` has `Z`-index `j` and `Y`-index `k`. -/

/-- The `3t²` copied observations of the order-`t` inflation. -/
inductive Obs (t : ℕ)
  | A (i j : Fin t) : Obs t
  | B (i k : Fin t) : Obs t
  | C (j k : Fin t) : Obs t
  deriving DecidableEq, Fintype

/-- A deterministic assignment of the copied observations, an element of `{0,1}^{3t²}`. -/
abbrev Assign (t : ℕ) := Obs t → Bool

/-- Which party a copied observation is a copy of. -/
def Obs.party {t : ℕ} : Obs t → Party
  | .A _ _ => .A
  | .B _ _ => .B
  | .C _ _ => .C

/-- The copied latent variables of the order-`t` inflation: `X_i`, `Z_j`, `Y_k`. -/
inductive Latent (t : ℕ)
  | X (i : Fin t) : Latent t
  | Z (j : Fin t) : Latent t
  | Y (k : Fin t) : Latent t
  deriving DecidableEq, Fintype

/-- The copied latent ancestors of a copied observation:
`A^{ij} ↦ {X_i, Z_j}`, `B^{ik} ↦ {X_i, Y_k}`, `C^{jk} ↦ {Z_j, Y_k}`. -/
def Obs.ancestors {t : ℕ} : Obs t → Finset (Latent t)
  | .A i j => {Latent.X i, Latent.Z j}
  | .B i k => {Latent.X i, Latent.Y k}
  | .C j k => {Latent.Z j, Latent.Y k}

/-- The copied latent ancestors of a set of copied observations. -/
def ancestorsOf {t : ℕ} (S : Finset (Obs t)) : Finset (Latent t) :=
  S.biUnion Obs.ancestors

/-- Paper Definition 2.2: two sets of copied observations are *ancestrally independent*
when their copied latent ancestors are disjoint. -/
def AncestrallyIndependent {t : ℕ} (S T : Finset (Obs t)) : Prop :=
  Disjoint (ancestorsOf S) (ancestorsOf T)

/-- The copied triangle `Δ_{ijk} = {A^{ij}, B^{ik}, C^{jk}}` (paper Section 2.2). -/
def copiedTriangle {t : ℕ} (i j k : Fin t) : Finset (Obs t) :=
  {Obs.A i j, Obs.B i k, Obs.C j k}

/-- The diagonal triangle `Δ_{lll}` (paper Section 2.2). -/
def diagonalTriangle {t : ℕ} (l : Fin t) : Finset (Obs t) := copiedTriangle l l l

/-- The three-bit outcome that an assignment gives to the copied triangle `Δ_{ijk}`. -/
def readTriangle {t : ℕ} (i j k : Fin t) (ω : Assign t) : ThreeBit :=
  (ω (Obs.A i j), ω (Obs.B i k), ω (Obs.C j k))

/-- The tuple of three-bit outcomes of the `t` diagonal triangles `(Δ_{lll})_{l ∈ [t]}`. -/
def readDiagonal {t : ℕ} (ω : Assign t) : Fin t → ThreeBit :=
  fun l => readTriangle l l l ω

/-! ### The symmetry group -/

/-- The action of `(σ_X, σ_Z, σ_Y) ∈ S_t × S_t × S_t` on copied observations. The first
component permutes `X`-copy indices, the second `Z`-copy indices, the third `Y`-copy
indices, exactly as in Definition 2.1(i). -/
def Obs.perm {t : ℕ} (π : Equiv.Perm (Fin t) × Equiv.Perm (Fin t) × Equiv.Perm (Fin t)) :
    Obs t → Obs t
  | .A i j => .A (π.1 i) (π.2.1 j)
  | .B i k => .B (π.1 i) (π.2.2 k)
  | .C j k => .C (π.2.1 j) (π.2.2 k)

/-- Relabelling an assignment by an index permutation. -/
def relabel {t : ℕ} (π : Equiv.Perm (Fin t) × Equiv.Perm (Fin t) × Equiv.Perm (Fin t))
    (ω : Assign t) : Assign t := fun v => ω (Obs.perm π v)

/-- Paper Definition 2.1(i): invariance under independent permutations of the three
index families. -/
def SymmetricLaw (t : ℕ) (Γ : Assign t → ℝ) : Prop :=
  ∀ π ω, Γ (relabel π ω) = Γ ω

/-! ### Injectable sets

Paper Definition 2.2 and Appendix A. -/

/-- The primitive condition of Wolfe–Spekkens–Fritz Definition 4, specialized to the
triangle: erasing copy indices is injective on the set, and any two members that are copies
of variables sharing a source in the triangle agree in the copy index of that source. -/
def SharedAgree {t : ℕ} : Obs t → Obs t → Prop
  | .A i _, .B i' _ => i = i'
  | .B i' _, .A i _ => i = i'
  | .A _ j, .C j' _ => j = j'
  | .C j' _, .A _ j => j = j'
  | .B _ k, .C _ k' => k = k'
  | .C _ k', .B _ k => k = k'
  | _, _ => True

/-- The primitive definition of an injectable set (paper Appendix A). -/
def InjectableRaw {t : ℕ} (S : Finset (Obs t)) : Prop :=
  (∀ u ∈ S, ∀ v ∈ S, u.party = v.party → u = v) ∧ (∀ u ∈ S, ∀ v ∈ S, SharedAgree u v)

/-- Paper Definition 2.2 together with Appendix A: for the triangle the injectable sets are
exactly the subsets of copied triangles. This characterization is the working definition
here; `Main.injectable_iff_injectableRaw` records its equivalence with `InjectableRaw`. -/
def Injectable {t : ℕ} (S : Finset (Obs t)) : Prop :=
  ∃ i j k : Fin t, S ⊆ copiedTriangle i j k

/-- The restriction of an assignment to a set of copied observations. -/
def restrictAssign {t : ℕ} (S : Finset (Obs t)) (ω : Assign t) : S → Bool := fun v => ω v.1

/-- The outcome pattern that a three-bit law prescribes on an injectable set: each member
reads the bit of the party it is a copy of. -/
def partyRead {t : ℕ} (S : Finset (Obs t)) (w : ThreeBit) : S → Bool :=
  fun v => partyBit v.1.party w

/-! ### The defect cube (paper Section 3.1)

`Cell t` indexes the cube `[t]³` of defect bits `D_{ijk}`; `Obs t` indexes the private bits
`N_v`. The root bits are indexed by `Root t = Cell t ⊕ Obs t`. -/

/-- The cells `(i,j,k) ∈ [t]³` of the defect cube. -/
abbrev Cell (t : ℕ) := Fin t × Fin t × Fin t

/-- The root bits of the defect cube: defects on cells, private bits on observations. -/
abbrev Root (t : ℕ) := Cell t ⊕ Obs t

/-- `onLine v c` says the cell `c` lies on the line `Λ(v)` read by the observation `v`:
`Λ(A^{ij}) = {(i,j,k) : k ∈ [t]}`, `Λ(B^{ik}) = {(i,j,k) : j ∈ [t]}`,
`Λ(C^{jk}) = {(i,j,k) : i ∈ [t]}` (paper Section 3.1). -/
def onLine {t : ℕ} : Obs t → Cell t → Bool
  | .A i j, c => (c.1 == i) && (c.2.1 == j)
  | .B i k, c => (c.1 == i) && (c.2.2 == k)
  | .C j k, c => (c.2.1 == j) && (c.2.2 == k)

/-- The output map of paper equation (eq:outputs): an observation outputs `1` exactly when
its private bit and every defect on its line are `0`. -/
def outputs {t : ℕ} (d : Cell t → Bool) (N : Obs t → Bool) : Assign t :=
  fun v => decide (N v = false ∧ ∀ c : Cell t, onLine v c = true → d c = false)

/-- The output map read off a joint root assignment. -/
def outputsOf {t : ℕ} (x : Root t → Bool) : Assign t :=
  outputs (fun c => x (Sum.inl c)) (fun v => x (Sum.inr v))

/-- The root bits that a set of copied observations reads: the defect cells on their lines,
together with their own private bits (paper Lemma 3.3, "disjoint inputs"). -/
def rootSupport {t : ℕ} (S : Finset (Obs t)) : Finset (Root t) :=
  (Finset.univ.filter (fun c : Cell t => ∃ v ∈ S, onLine v c = true)).image Sum.inl
    ∪ S.image Sum.inr

/-- `R_l`, the union of the three lines of the diagonal triangle `Δ_{lll}`: the cells with
at least two coordinates equal to `l` (paper equation (eq:Rl)). -/
def inDiagRegion {t : ℕ} (l : Fin t) (c : Cell t) : Bool :=
  onLine (Obs.A l l) c || onLine (Obs.B l l) c || onLine (Obs.C l l) c

noncomputable section

/-! ## The paper's explicit laws -/

/-- `Bern(r)`, with `Bern(r)(true) = r`. -/
def bern (r : ℝ) : Bool → ℝ := fun b => if b then r else 1 - r

/-- Paper equation (eq:Q): `Q(ε,r) = ε δ_{000} + (1-ε) Bern(r)^{⊗3}`. -/
def Q (ε r : ℝ) : ThreeBit → ℝ := fun w =>
  ε * (if w = (false, false, false) then 1 else 0)
    + (1 - ε) * (bern r w.1 * bern r w.2.1 * bern r w.2.2)

/-- `ε_t = 1/(2t³)` (paper Theorem 3.2). -/
def epsFam (t : ℕ) : ℝ := 1 / (2 * (t : ℝ) ^ 3)

/-- `r_t = (1 - ε_t)^{t-1}` (paper Theorem 3.2). -/
def rFam (t : ℕ) : ℝ := (1 - epsFam t) ^ (t - 1)

/-- The nontermination family `P_t = Q(ε_t, r_t)` (paper Theorem 3.2). -/
def Pfam (t : ℕ) : ThreeBit → ℝ := Q (epsFam t) (rFam t)

/-- The divergent-rejecting-order family `P_ε = Q(ε, 1 - ε^{2/3}/2)` (paper Proposition 5.1). -/
def Peps (ε : ℝ) : ThreeBit → ℝ := Q ε (1 - ε ^ ((2 : ℝ) / 3) / 2)

/-- `R_p = (1-p) δ_{111} + p δ_{000}` (paper Proposition 4.2). -/
def Rlaw (p : ℝ) : ThreeBit → ℝ := fun w =>
  (1 - p) * (if w = (true, true, true) then 1 else 0)
    + p * (if w = (false, false, false) then 1 else 0)

/-- `s = 1 - r/(1-ε)^{t-1}`, the private-bit parameter of paper equation (eq:s). -/
def sParam (t : ℕ) (ε r : ℝ) : ℝ := 1 - r / (1 - ε) ^ (t - 1)

/-! ## Triangle compatibility -/

/-- A triangle model with finite latent alphabets: three latent spaces with weight
functions, and the three response probabilities `f(x,z) = Pr(A = 0 | x,z)`,
`g(x,y) = Pr(B = 0 | x,y)`, `h(z,y) = Pr(C = 0 | z,y)`. -/
structure TriangleModel where
  X : Type
  Y : Type
  Z : Type
  fintypeX : Fintype X
  fintypeY : Fintype Y
  fintypeZ : Fintype Z
  μX : X → ℝ
  μY : Y → ℝ
  μZ : Z → ℝ
  f : X × Z → ℝ
  g : X × Y → ℝ
  h : Z × Y → ℝ

attribute [instance] TriangleModel.fintypeX TriangleModel.fintypeY TriangleModel.fintypeZ

/-- The response law of a party: probability `q` of the outcome `0 = false`. -/
def respMass (q : ℝ) : Bool → ℝ := fun b => if b then 1 - q else q

/-- A triangle model is valid when the three source weights are laws and the three response
probabilities take values in `[0,1]`. -/
def TriangleModel.Valid (M : TriangleModel) : Prop :=
  IsLaw M.μX ∧ IsLaw M.μY ∧ IsLaw M.μZ ∧
    (∀ p, 0 ≤ M.f p ∧ M.f p ≤ 1) ∧ (∀ p, 0 ≤ M.g p ∧ M.g p ≤ 1) ∧
    (∀ p, 0 ≤ M.h p ∧ M.h p ≤ 1)

/-- The observed law of a triangle model: the sources are independent and the responses are
conditionally independent given the sources (paper Section 2.1). -/
def TriangleModel.law (M : TriangleModel) : ThreeBit → ℝ := fun w =>
  ∑ x : M.X, ∑ y : M.Y, ∑ z : M.Z,
    M.μX x * M.μY y * M.μZ z
      * respMass (M.f (x, z)) w.1 * respMass (M.g (x, y)) w.2.1 * respMass (M.h (z, y)) w.2.2

/-- Paper Section 2.1: the triangle-compatible set `C_tri`, with the finite-latent-alphabet
formalization boundary described in the file header. -/
def TriangleCompatible (P : ThreeBit → ℝ) : Prop :=
  ∃ M : TriangleModel, M.Valid ∧ M.law = P

/-! ## The finite inflation tests -/

/-- Paper Definition 2.1: the Navascués–Wolfe feasible set `I^NW_t`. A law `Γ_t` on the
copied observations, invariant under `S_t³`, whose diagonal law is the tensor power `P^{⊗t}`. -/
def NWFeasible (t : ℕ) (P : ThreeBit → ℝ) : Prop :=
  ∃ Γ : Assign t → ℝ, IsLaw Γ ∧ SymmetricLaw t Γ ∧
    pushforward Γ readDiagonal = tensorPow t P

/-- The injectable-marginal prescriptions of paper Definition 2.2: every injectable set has
the corresponding marginal of `P`. -/
def InjectableMarginals (t : ℕ) (Γ : Assign t → ℝ) (P : ThreeBit → ℝ) : Prop :=
  ∀ S : Finset (Obs t), Injectable S →
    pushforward Γ (restrictAssign S) = pushforward P (partyRead S)

/-- The ancestral-independence prescriptions of paper Definition 2.2: every union of
pairwise ancestrally independent injectable sets has the product of the corresponding
marginals. The union is presented as a finite family, whose joint restriction law is
required to factor. -/
def AncestralProducts (t : ℕ) (Γ : Assign t → ℝ) (P : ThreeBit → ℝ) : Prop :=
  ∀ (n : ℕ) (S : Fin n → Finset (Obs t)), (∀ m, Injectable (S m)) →
    (∀ m m', m ≠ m' → AncestrallyIndependent (S m) (S m')) →
    pushforward Γ (fun ω m => restrictAssign (S m) ω)
      = fun φ : ∀ m : Fin n, (S m) → Bool =>
          ∏ m : Fin n, pushforward P (partyRead (S m)) (φ m)

/-- Paper Definition 2.2: the ancestral-independence feasible set `I^AI_t`. -/
def AIFeasible (t : ℕ) (P : ThreeBit → ℝ) : Prop :=
  ∃ Γ : Assign t → ℝ, IsLaw Γ ∧ SymmetricLaw t Γ ∧
    pushforward Γ readDiagonal = tensorPow t P ∧
    InjectableMarginals t Γ P ∧ AncestralProducts t Γ P

/-! ## The defect-cube witness -/

/-- The per-root Bernoulli weights: defects are `Bern(ε)`, private bits are `Bern(s)`. -/
def rootWeight (t : ℕ) (ε s : ℝ) : Root t → Bool → ℝ
  | Sum.inl _ => bern ε
  | Sum.inr _ => bern s

/-- The joint law of the independent root bits of the defect cube. -/
def rootLaw (t : ℕ) (ε s : ℝ) : (Root t → Bool) → ℝ := prodLaw (rootWeight t ε s)

/-- Paper Section 3.1: the defect-cube law `Γ_t`, the pushforward of the independent defect
and private bits under the output map (eq:outputs). Unfolding `pushforward` and `prodLaw`
gives the explicit finite sum of product weights of paper equation (eq:table):
`Γ_t(w) = ∑_{x : outputsOf x = w} ∏_{roots} bern _ (x _)`. -/
def defectLaw (t : ℕ) (ε s : ℝ) : Assign t → ℝ :=
  pushforward (rootLaw t ε s) outputsOf

/-! ## First rejecting order

Paper Section 2.2: `t_min^H(P) = min {t ≥ 1 : P ∉ I^H_t}`. Formalized as `Nat.sInf`, which
returns the junk value `0` when the set is empty. The set is nonempty exactly when some
finite order rejects `P`; that this happens for every incompatible `P` is the asymptotic
completeness of the hierarchy, which is quoted from Navascués–Wolfe in the paper and is not
formalized here. Every statement about `t_min` below therefore either exhibits a rejecting
order or assumes one. -/

/-- `t_min^NW(P)`, the first order of the Navascués–Wolfe hierarchy that rejects `P`. -/
def tminNW (P : ThreeBit → ℝ) : ℕ := sInf {t : ℕ | 1 ≤ t ∧ ¬ NWFeasible t P}

/-- `t_min^AI(P)`, the first order of the ancestral-independence hierarchy that rejects `P`. -/
def tminAI (P : ThreeBit → ℝ) : ℕ := sInf {t : ℕ | 1 ≤ t ∧ ¬ AIFeasible t P}

end

end TriangleInflation

namespace TriangleInflation.Graph

open Finset TriangleInflation

/-! ### Pair-source scenarios -/

/-- A pair-source scenario (AUDIT-NOTES A1): a finite simple graph without isolated
vertices. Each vertex carries one binary observed variable, each edge one independent latent
source shared by its two endpoints. -/
structure PairGraph where
  /-- The observed vertices. -/
  V : Type
  fintypeV : Fintype V
  decEqV : DecidableEq V
  /-- The source graph; an edge is an independent latent source. -/
  G : SimpleGraph V
  decAdj : DecidableRel G.Adj
  /-- No isolated vertices: an observation with no source has no copying convention. -/
  no_isolated : ∀ v : V, ∃ w : V, G.Adj v w

attribute [instance] PairGraph.fintypeV PairGraph.decEqV PairGraph.decAdj

/-- The latent sources of a pair-source scenario: the edges of its graph. -/
abbrev PairGraph.Edge (Γ : PairGraph) := {e : Sym2 Γ.V // e ∈ Γ.G.edgeFinset}

/-- The sources incident to a vertex. -/
def PairGraph.inc (Γ : PairGraph) (v : Γ.V) : Finset Γ.Edge :=
  Finset.univ.filter (fun e => v ∈ (e.1 : Sym2 Γ.V))

/-- A target law: a weight function on the binary observed vertices. -/
abbrev GTarget (Γ : PairGraph) := (Γ.V → Bool) → ℝ

/-! ### Order-`t` copied observations -/

/-- The copied observations of the order-`t` inflation (AUDIT-NOTES A1): one observation for
each vertex `v` and each choice of a copy index for every source incident to `v`. -/
abbrev GObs (Γ : PairGraph) (t : ℕ) := Σ v : Γ.V, (Γ.inc v → Fin t)

/-- A deterministic assignment of all copied observations. -/
abbrev GAssign (Γ : PairGraph) (t : ℕ) := GObs Γ t → Bool

variable {Γ : PairGraph} {t : ℕ}

/-- The action of a per-source permutation of copy indices on copied observations. -/
def gPerm (π : Γ.Edge → Equiv.Perm (Fin t)) (o : GObs Γ t) : GObs Γ t :=
  ⟨o.1, fun e => π e.1 (o.2 e)⟩

/-- The induced action on assignments. -/
def gRelabel (π : Γ.Edge → Equiv.Perm (Fin t)) (ω : GAssign Γ t) : GAssign Γ t :=
  fun o => ω (gPerm π o)

/-- Symmetry of a witness under independent permutations of the copy indices of each source
(AUDIT-NOTES A1; the pair-source form of `TriangleInflation.SymmetricLaw`). -/
def GSymmetric (t : ℕ) (Δ : GAssign Γ t → ℝ) : Prop :=
  ∀ (π : Γ.Edge → Equiv.Perm (Fin t)) (ω : GAssign Γ t), Δ (gRelabel π ω) = Δ ω

/-! ### The copied original scenarios and the diagonal rows -/

/-- The copied observation of the vertex `v` in the copy of the original scenario selected by
the index vector `ι`. -/
def copyObs (ι : Γ.Edge → Fin t) (v : Γ.V) : GObs Γ t := ⟨v, fun e => ι e.1⟩

/-- The observed outcome that an assignment gives to the copied scenario selected by `ι`. -/
def readCopy (ι : Γ.Edge → Fin t) (ω : GAssign Γ t) : Γ.V → Bool := fun v => ω (copyObs ι v)

/-- The `t` diagonal rows: row `r` takes the copy index `r` on every source
(AUDIT-NOTES A1). -/
def readDiag (ω : GAssign Γ t) : Fin t → (Γ.V → Bool) := fun r => readCopy (fun _ => r) ω

/-- The `t`-fold tensor power of a target law. -/
def gTensorPow (t : ℕ) (P : GTarget Γ) : (Fin t → (Γ.V → Bool)) → ℝ :=
  fun v => ∏ r : Fin t, P (v r)

/-! ### The order-`t` Navascués–Wolfe test -/

/-- The Navascués–Wolfe feasible set of a pair-source scenario (AUDIT-NOTES A1): a symmetric
law on the copied observations whose diagonal law is the tensor power of the target. -/
def GNWFeasible (Γ : PairGraph) (t : ℕ) (P : GTarget Γ) : Prop :=
  ∃ Δ : GAssign Γ t → ℝ, IsLaw Δ ∧ GSymmetric t Δ ∧ pushforward Δ readDiag = gTensorPow t P

/-! ### Compatibility -/

/-- A model of a pair-source scenario with finite latent alphabets: one latent alphabet and
source law per edge, and for each vertex the probability `resp v` of the outcome
`false = 0` given the values of the sources incident to it. -/
structure GModel (Γ : PairGraph) where
  /-- The latent alphabet of each source. -/
  L : Γ.Edge → Type
  fintypeL : ∀ e, Fintype (L e)
  /-- The law of each source. -/
  μ : ∀ e, L e → ℝ
  /-- `resp v c = Pr(outcome at v is 0 | incident sources take the values c)`. -/
  resp : ∀ v : Γ.V, ((e : Γ.inc v) → L e.1) → ℝ

attribute [instance] GModel.fintypeL

/-- A model is valid when every source law is a law and every response probability lies in
`[0,1]`. -/
def GModel.Valid (M : GModel Γ) : Prop :=
  (∀ e, IsLaw (M.μ e)) ∧ (∀ v c, 0 ≤ M.resp v c ∧ M.resp v c ≤ 1)

/-- The observed law of a model: the sources are independent and the responses are
conditionally independent given the sources. -/
def GModel.law (M : GModel Γ) : GTarget Γ := fun w =>
  ∑ x : (∀ e : Γ.Edge, M.L e),
    (∏ e : Γ.Edge, M.μ e (x e)) * ∏ v : Γ.V, respMass (M.resp v (fun e => x e.1)) (w v)

/-- The compatible set `C_G` of a pair-source scenario, with the finite-latent-alphabet
boundary described in the file header (AUDIT-NOTES D1). -/
def GCompatible (Γ : PairGraph) (P : GTarget Γ) : Prop :=
  ∃ M : GModel Γ, M.Valid ∧ M.law = P

/-! ### Double-star forests -/

/-- A double-star forest: every connected component is a tree of diameter at most three
(AUDIT-NOTES A3). Stated as acyclicity together with a diameter bound inside each
component. -/
def IsDoubleStarForest {V : Type} (G : SimpleGraph V) : Prop :=
  G.IsAcyclic ∧ ∀ u v : V, G.Reachable u v → G.dist u v ≤ 3

end TriangleInflation.Graph

open TriangleInflation TriangleInflation.Graph in
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
