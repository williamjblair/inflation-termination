# Finite binary-triangle inflation does not stabilize — proof

Keep the three hierarchy semantics distinct. This does not concern current retained constructor admission and does not assert publication priority.

Source edition: `PROOF.md` (`~/Documents/Codex/2026-08-29/assess-vela-breakthrough-chatgpt-conversation-6a91c3a3/work/continuous-campaign/axis5/gen244-binary-triangle-inflation-nontermination-audit/PROOF.md`), lines 3–279; original SHA256 `a38310645a78b5d9372ef55080899308e4ab4b84f57ee207e21979913f5e3bf4`. The imported ranges and presentation-only changes are recorded in [the source index](<../SOURCES.json>). Source-specific labels inside the proof identify its original conventions, not a second current compiler.

**RESULT-CERT-0 specification delta (12 September 2026).**  This edition adds
the explicit rational family and small-order replay, expands the load-bearing
diagonal-support and stochastic-kernel arguments, repairs the logical basis of
the diverging-order sentence, and proves that the auxiliary `84/epsilon` bound
already follows from bare NW at order at least three.  The source edition is
preserved above and in git history.

## 1. Three hierarchy semantics

At order `t`, write

\[
A^{ij},\quad B^{ik},\quad C^{jk}
\qquad(i,j,k\in[t])
\]

for the copied binary observations.  The latent-copy ancestors are respectively

\[
\{X_i,Z_j\},\qquad \{X_i,Y_k\},\qquad \{Z_j,Y_k\}.
\]

We distinguish three feasible sets.

1. `I_t^NW`: a global law invariant under independent permutations of the
   `X`, `Z`, and `Y` copy indices whose degree-`t` diagonal marginal is
   `P^tensor t`.
2. `I_t^AI`: in addition, every injectable marginal is the corresponding
   target marginal and every union of ancestrally independent injectable
   components has the prescribed product law.
3. `I_t^exp`: in addition, all recursively expressible marginals obtained by
   the Wolfe--Spekkens--Fritz conditional-independence rules are prescribed.

Consequently

\[
\mathcal I_t^{\rm exp}\subseteq
\mathcal I_t^{\rm AI}\subseteq
\mathcal I_t^{\rm NW}.
\]

For the triangle, an injectable set is exactly a subset of one copied triangle

\[
\Delta_{ijk}=\{A^{ij},B^{ik},C^{jk}\}.
\]

The exact replay exhaustively checks this characterization through `t=6`; the
general statement follows because injectability permits at most one copy of
each original observed node and requires the shared latent indices to agree.

## 2. Defect law

Let the bits

\[
D_{ijk}\sim\operatorname{Bern}(\varepsilon)
\]

be mutually independent.  Add mutually independent private bits

\[
N_v\sim\operatorname{Bern}(s),\qquad 0\le s\le1,
\]

independent of all defects.  Define

\[
A^{ij}=1
\iff N_{A^{ij}}=0\text{ and }D_{ijk}=0\text{ for every }k,
\]

and cyclically for `B^{ik}` and `C^{jk}`.

The defect supports are

\[
\begin{aligned}
\Lambda(A^{ij})&=\{(i,j,k):k\in[t]\},\\
\Lambda(B^{ik})&=\{(i,j,k):j\in[t]\},\\
\Lambda(C^{jk})&=\{(i,j,k):i\in[t]\}.
\end{aligned}
\]

If two observed copies have disjoint ancestral sets, their defect supports are
disjoint.  Indeed, an intersection of two supports forces equality of the
index belonging to a shared source type.  The same conclusion for two sets of
variables follows by taking their unions.  Pairwise ancestrally disjoint
blocks therefore depend on mutually disjoint subfamilies of the independent
`D` and `N` variables, and are mutually independent.

## 3. Injectable law

Fix `i,j,k` and condition on `D_ijk`.

- If `D_ijk=1`, the copied triangle is `000`.
- If `D_ijk=0`, each of its three variables depends on its private bit and on
  `t-1` remaining defects.  Those three families are disjoint.  Hence the
  outputs are conditionally independent, each with success probability

\[
r=(1-s)(1-\varepsilon)^{t-1}.
\]

Thus

\[
\Law(A^{ij},B^{ik},C^{jk})
=\varepsilon\delta_{000}
+(1-\varepsilon)\operatorname{Bern}(r)^{\otimes3}.
\]

Given `0<=r<=(1-epsilon)^(t-1)`, choose

\[
s=1-\frac r{(1-\varepsilon)^{t-1}}\in[0,1].
\]

Every injectable marginal is a projection of this law.  The disjoint-support
lemma gives every AI product.  Independent index permutations merely permute
the iid defect and private-bit families, so the global law is `S_t^3`
invariant.

For completeness, write `R_l` for the full defect support of the diagonal
triangle `Delta_lll`.  Directly from the three line definitions,

\[
R_\ell=
\{(\ell,\ell,k):k\in[t]\}
\cup\{(\ell,j,\ell):j\in[t]\}
\cup\{(i,\ell,\ell):i\in[t]\}.
\]

Equivalently, `R_l` is the set of cube cells having at least two coordinates
equal to `l`.  If `l!=m`, a cell cannot have at least two coordinates equal to
`l` and at least two equal to `m`, because it has only three coordinates.
Thus `R_l cap R_m` is empty.  The private bits used by distinct diagonal
triangles are also distinct.  The complete random-input supports of all `t`
diagonal triangles are therefore mutually disjoint.  This proves their mutual
independence, not merely their pairwise independence, and hence their joint
law is `P^tensor t`.  This proves membership in both `I_t^AI` and `I_t^NW`.

## 4. Recursive expressible sets

The stronger statement needs more than the preceding unconditional product
argument.  Let `H_t` be the latent DAG whose independent roots are the defects
and private bits and whose observed children are those in the construction.

The observed latent projection of `H_t` is a subgraph of the observed latent
projection of the genuine order-`t` triangle inflation DAG.  A defect
`D_ijk` joins only `A^ij`, `B^ik`, and `C^jk`; every pair among these already
shares, respectively, `X_i`, `Z_j`, or `Y_k` in the genuine inflation.
Private bits add no observed-observed edge.  Deleting latent-projection edges
cannot create an m-connecting path.  Therefore every observed d-separation
used in the genuine inflation's recursive expressibility calculus also holds
under the defect law.

Starting from the already-correct injectable marginals, induction over the
recursive expressible-set construction now shows that each prescribed
conditional-product/marginalization formula equals the corresponding marginal
of the single defect law.  Copy-index equality constraints follow from global
`S_t^3` symmetry.  Hence the construction also lies in `I_t^exp`.

This argument does not assert that AI-expressible and general expressible sets
coincide; they do not need to.

## 5. Finner separation

Let a genuine triangle model be written with arbitrary independent source
laws `mu_X,mu_Y,mu_Z` and stochastic binary response kernels.  Put

\[
F(x,z)=P(A=0\mid x,z),\quad
G(x,y)=P(B=0\mid x,y),\quad
H(z,y)=P(C=0\mid z,y).
\]

These measurable functions take values in `[0,1]`; Tonelli applies even when
the latent alphabets are unrestricted.  Define

\[
u(x)^2=\int G(x,y)^2\,d\mu_Y(y),\qquad
v(z)^2=\int H(z,y)^2\,d\mu_Y(y).
\]

Cauchy--Schwarz in `y`, followed by Cauchy--Schwarz in the independent pair
`(x,z)`, gives

\[
\begin{aligned}
P(000)
&\le \int F(x,z)u(x)v(z)\,d\mu_X(x)d\mu_Z(z)\\
&\le
\left(\int F^2\,d\mu_Xd\mu_Z\right)^{1/2}
\left(\int u^2\,d\mu_X\int v^2\,d\mu_Z\right)^{1/2}\\
&\le \sqrt{P_A(0)P_B(0)P_C(0)}.
\end{aligned}
\]

The final step uses `F^2<=F`, `G^2<=G`, and `H^2<=H`.  Thus, without a
determinization or finite-alphabet assumption,

\[
P(000)^2\le P_A(0)P_B(0)P_C(0).
\]

For

\[
P=Q\left(\varepsilon,(1-\varepsilon)^{t-1}\right),
\]

we have

\[
P(000)\ge\varepsilon,
\qquad
P_A(0)=1-(1-\varepsilon)^t\le t\varepsilon,
\]

and the same marginal at all three parties.  If
`0<epsilon<t^(-3)`, then

\[
P(000)^2\ge\varepsilon^2
>t^3\varepsilon^3
\ge P_A(0)P_B(0)P_C(0).
\]

So `P` is incompatible although it passes all three order-`t` relaxations.
This proves strict containment at every finite order.

For the explicit choice in the certification theorem,

\[
\varepsilon_t=\frac1{2t^3},\quad q_t=1-\varepsilon_t,\quad
r_t=q_t^{t-1},\quad P_t=Q(\varepsilon_t,r_t),
\]

the same estimates give the exact uniform margin

\[
\begin{aligned}
P_t(000)^2-
P_{t,A}(0)P_{t,B}(0)P_{t,C}(0)
&\ge \varepsilon_t^2-t^3\varepsilon_t^3\\
&=\frac{\varepsilon_t^2}{2}>0.
\end{aligned}
\]

This includes `t=1`, where `P_1=(delta_000+delta_111)/2`.

## 6. One family and rejection order

Put

\[
P_\varepsilon
=Q\left(\varepsilon,1-\tfrac12\varepsilon^{2/3}\right),
\qquad \sigma=\tfrac12\varepsilon^{2/3}.
\]

Then

\[
P_\varepsilon(000)\ge\varepsilon,
\qquad
P_{\varepsilon,A}(0)
\le\varepsilon+\sigma
=\varepsilon^{2/3}(\varepsilon^{1/3}+1/2).
\]

For `epsilon<1/8`, the cube of the last expression is strictly less than
`epsilon^2`, so Finner is violated.  If

\[
t\le1+\tfrac12\varepsilon^{-1/3},
\]

then Bernoulli's inequality gives

\[
(1-\varepsilon)^{t-1}
\ge1-(t-1)\varepsilon
\ge1-\tfrac12\varepsilon^{2/3}.
\]

The membership theorem applies.  If

\[
t_{\min}^{H}(P)=\min\{t\ge1:P\notin\mathcal I_t^H\},
\qquad H\in\{\mathrm{exp},\mathrm{AI},\mathrm{NW}\},
\]

then the displayed passing range forces every one of these minimum orders to
exceed `1+(1/2)epsilon^(-1/3)` up to the harmless integer endpoint.  This
explicit lower bound makes the minimum rejection orders diverge.  The separate
fact `P_epsilon -> delta_111` does not imply that conclusion by itself.

## 7. Separate NW rejection upper bound

For a fixed inflated assignment, sample independent uniform indices `I,J,K`
and output

\[
(a_{IJ},b_{IK},c_{JK}).
\]

This is a genuine empirical triangle law, so Finner holds pointwise.  Average
over an order-`t` NW-feasible global law.  In the square of the all-zero
triangle count, the ordered pairs with all three copied-source indices unequal
number exactly `t^3(t-1)^3`.  For `t>=2`, source-index permutations send the
two copied triangles to `Delta_111,Delta_222`; the NW diagonal law assigns
these terms

\[
t^3(t-1)^3 P(000)^2.
\]

On the product-of-marginals side, the same number of fully source-disjoint
triples occur.  For `t>=3`, a term `A^ij B^uk C^vw` with `i!=u`, `j!=v`, and
`k!=w` can be sent by independent source-index permutations to
`A^11 B^22 C^33`.  Projecting the NW degree-three diagonal law assigns it

\[
t^3(t-1)^3P_A(0)P_B(0)P_C(0).
\]

There are at most `3t^5` collision terms.  Each contains a colliding
cross-party pair.  NW symmetry and the degree-one diagonal law assign that
pair the corresponding two-party target marginal, so the whole collision
event is at most

\[
M(P)=\max\{P_{AB}(00),P_{AC}(00),P_{BC}(00),
P_A(0)P_B(0),P_A(0)P_C(0),P_B(0)P_C(0)\}.
\]

Therefore every bare NW-feasible law at order `t>=3` obeys

\[
P(000)^2-P_A(0)P_B(0)P_C(0)
\le\frac{3t^2}{(t-1)^3}M(P).
\]

For the single family and `epsilon<=1/64`, the left side is at least
`(37/64)epsilon^2`, `M(P)<=2epsilon`, and
`t^2/(t-1)^3<=8/t`.  NW membership forces

\[
t\le\frac{48\cdot64}{37\varepsilon}<\frac{84}{\varepsilon}.
\]

Let `N=floor(3072/(37 epsilon))+1`.  It is above `3` in the stated range, and
NW feasibility fails at `N`.  Moreover

\[
N\le\frac{3072}{37\varepsilon}+1
\le\frac{84}{\varepsilon},
\]

because `epsilon<=1/64<36/37`.  Hence

\[
t_{\min}^{\rm NW}(P_\varepsilon)\le\frac{84}{\varepsilon}.
\]

The earlier AI-only scope was unnecessarily restrictive: the particular
two-triangle and three-singleton products used here are already consequences
of bare NW.  This does not identify the NW and AI feasible sets.

## 8. Exact small-order replay

The standalone paper package includes rational certificates at `t=1,2,3`.
The structural validator checks every adjacent-transposition generator,
every copied-triangle marginal, explicit mutual disjointness of the diagonal
root supports, and all `8^t` diagonal equations.  At `t=2` it additionally
checks a sparse full 4096-coordinate LP vector reconstructed by exhaustive
enumeration of the 256 defect cubes.  A normalization-preserving nonnegative
corruption is rejected by the diagonal equations.  No floating-point
arithmetic or LP solver is used; see
[`papers/inflation-nontermination/reproduce.sh`](../../papers/inflation-nontermination/reproduce.sh).
