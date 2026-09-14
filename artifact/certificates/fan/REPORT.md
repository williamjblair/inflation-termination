# Sharp rejecting-order exponent for a binary-triangle hard family

Date of investigation: 12 September 2026.

Pinned upstream repository: `williamjblair/resource-theory`, commit
`768d404c631659574d9fad232c028df4f63fbc3b`.

## Result and scope

For the maintained family

\[
P_\varepsilon=\varepsilon\delta_{000}+(1-\varepsilon)
\operatorname{Bern}\!\left(1-\tfrac12\varepsilon^{2/3}\right)^{\otimes3},
\qquad 0<\varepsilon<1/8,
\]

the first rejecting order of each of the full Navascués–Wolfe (NW),
AI-product strengthened, and maintained expressible-set strengthened classical
hierarchies satisfies

\[
\boxed{t_{\min}^H(P_\varepsilon)=\Theta(\varepsilon^{-1/3})}.
\]

More precisely,

\[
\frac12\le\liminf_{\varepsilon\downarrow0}\varepsilon^{1/3}t_{\min}^H
\le\limsup_{\varepsilon\downarrow0}\varepsilon^{1/3}t_{\min}^H
\le4-2\sqrt3.
\]

The lower construction is inherited from the pinned repository. The new part
is an all-order fan inequality, valid already for bare NW, which improves the
old upper order from O(epsilon^(-1)) to O(epsilon^(-1/3)). The exponent is
resolved; an exact limiting constant is not.

The complete proof below is an analytic derivation, supplemented by exact
finite certificates. It is not a human specialist endorsement, a Lean proof,
an exhaustive historical-priority clearance, or a claim about the sharp
worst-case Hausdorff convergence rate. See AUDIT.md for the actual read set and
limitations. No upstream files were modified.

## 1. Definitions and the inherited passing construction

Use independent sources X,Y,Z and copied outputs
A^{ij}=A(X_i,Z_j), B^{ik}=B(X_i,Y_k), C^{jk}=C(Z_j,Y_k).
An order-t NW extension is a probability law on all 3t^2 copied outputs,
invariant under independent permutations of the three source-index sets,
whose t diagonal triangles have joint law P^{tensor t}. We use t_min as the
least positive integer order which rejects, and infinity on compatible laws.

The strengthened hierarchies have inclusions

\[
\mathcal C_\triangle\subseteq\mathcal I_t^{\rm exp}
\subseteq\mathcal I_t^{\rm AI}\subseteq\mathcal I_t^{\rm NW}.
\]

These are inclusions, not finite-order equalities. The maintained hierarchy
correction specifically rules out conflating full AI marginals with the NW
orbit-diagonal marginal problem [R3].

For Q(epsilon,r)=epsilon delta_000+(1-epsilon)Bern(r)^3, the pinned proof [R1]
constructs an expressible-set extension whenever

\[
r\le(1-\varepsilon)^{t-1}.\tag{1}
\]

Here is the construction. Give every cell (i,j,k) an independent Bernoulli
(epsilon) defect D_{ijk}. A^{ij} is one precisely when all defects on its
k-line vanish and its independent local kill coin vanishes. Define B and C
using the other two line directions. Choose the common kill probability s
so that (1-s)(1-epsilon)^{t-1}=r. In any copied triangle its three defect
lines intersect in exactly their central cell. A central defect forces 000;
conditioned on no central defect, all residual line defects and kill coins
are independent, and the three outputs are Bern(r).

Independent source-index permutations preserve this law. The support of the
l-th diagonal triangle consists of cells with at least two indices equal to
l, together with its private kill coins. These supports are disjoint for
distinct l, giving the full t-fold diagonal law, not merely pairwise diagonal
independence. The source proof additionally verifies the inherited observed
d-separation relations and the recursive expressible-set prescriptions,
including the zero-denominator convention. This gives passage through all
three named variants. It does not assert that the extension is itself a
physical triangle model.

Set

\[
\sigma=\tfrac12\varepsilon^{2/3},\qquad
m=\varepsilon+(1-\varepsilon)\sigma,\qquad
z=\varepsilon+(1-\varepsilon)\sigma^3.\tag{2}
\]

These are the common zero-marginal and P(000). For epsilon<1/8,
m<epsilon^(2/3) and z>=epsilon. Thus z^2>m^3, violating the triangle Finner
inequality. Every P_epsilon is incompatible.

The exact inherited sufficient passing threshold gives

\[
t_{\min}^H(P_\varepsilon)\ge
\left\lfloor1+\frac{\log(1-\sigma)}{\log(1-\varepsilon)}\right\rfloor+1.
\tag{3}
\]

In particular Bernoulli's inequality gives the simpler bound

\[
t_{\min}^H(P_\varepsilon)\ge
\left\lfloor1+\tfrac12\varepsilon^{-1/3}\right\rfloor+1.
\tag{4}
\]

The pinned source also proves the old NW rejecting-order estimate
84/epsilon for epsilon<=1/64. Its proof uses order at least three. That is
not a new bound of this report [R1,R2].

## 2. A fan witness requiring only bare NW marginals

Let P be any binary law, and put a=P_A(0), b=P_B(0), c=P_C(0), z=P(000).
In an order-t NW extension, t>=2, define indicator variables

\[
A=1[A^{11}=0],\quad B_k=1[B^{1k}=0],\quad C_k=1[C^{1k}=0],
\quad T_k=AB_kC_k.
\]

We have

\[
\mathbb EA=a,\qquad\mathbb ET_k=z,\qquad
\mathbb E B_kC_\ell=bc\quad(k\ne\ell).\tag{5}
\]

For the last identity, send X_1 to source index 1, Z_1 to source index 2,
Y_k to index 1 and Y_l to index 2. The independent source permutations can
always be extended to permutations of [t]. They send B^{1k} to B^{11}
and C^{1l} to C^{22}. Their marginal is therefore the projection of two
independent diagonal copies of P. This proves (5) directly from NW; no
additional AI constraint is smuggled into the argument. For k=l, the product
identity is unavailable and is never used.

### Theorem 1: second-moment fan inequality

Every order-t NW-feasible P satisfies

\[
\boxed{t(z^2-abc)\le az-abc.}\tag{6}
\]

Proof. Put U=sum_k T_k. Since U vanishes off A,
(EU)^2<=(EA)(EU^2). Also
U^2=sum_k T_k+sum_{k!=l}T_kT_l, and
T_kT_l<=B_kC_l. Equation (5) gives
(tz)^2<=a[tz+t(t-1)bc], which is (6).

Cyclically choosing the smallest marginal yields the explicit bound

\[
t_{\min}^{\rm NW}(P)\le
\left\lfloor\frac{z\min(a,b,c)-abc}{z^2-abc}\right\rfloor+1,
\qquad z^2>abc.\tag{7}
\]

The ratio is at least one since its numerator minus denominator equals
z(min(a,b,c)-z). This handles the order-one convention.

The inequality also has a rational pointwise certificate. For any rational
lambda,

\[
(2\lambda-1)\sum_kT_k-\lambda^2 A
-\sum_{k\ne\ell}B_kC_\ell\le0.
\]

It follows from A(S-lambda)^2>=0, where S=sum_k B_kC_k, and
AS^2<=AS+sum_{k!=l}B_kC_l. Choosing lambda=tz/a recovers (6).

### Theorem 2: integer fan inequality

Every order-t NW-feasible P satisfies

\[
\boxed{tz\le a+\binom t2bc.}\tag{8}
\]

Proof. The following inequality holds for every deterministic assignment:

\[
\sum_kAB_kC_k\le A+\frac12\sum_{k\ne\ell}B_kC_\ell.\tag{9}
\]

If A=0 it is immediate. If A=1, put S=sum_k B_kC_k. Since sum B and sum C
are each at least S, the right side minus the left side is at least

\[
1+\tfrac12 S(S-1)-S=\tfrac12(S-1)(S-2)\ge0
\]

for every nonnegative integer S. Take expectations and use (5).

Equation (9) is a pointwise marginal-polytope certificate. The proof mechanism
belongs to the established logical/marginal-inequality inflation framework
of Wolfe–Spekkens–Fritz [P2]. Historical priority of this particular all-order
specialization has not been certified.

## 3. Resolving the hard-family exponent

For the family (2), let

\[
v_t=tz-m-\binom t2m^2.\tag{10}
\]

Positive v_t rejects NW and hence both strengthened variants.
For t=x epsilon^(-1/3)+O(1), direct expansion gives

\[
v_t=\left(x-\frac12-\frac{x^2}{8}\right)\varepsilon^{2/3}
+O(\varepsilon).
\tag{11}
\]

The first root is c_*=4-2sqrt(3). For every fixed x strictly between c_* and
the second root 4+2sqrt(3), v_t>0 for all sufficiently small epsilon. Taking
x down to c_* and combining with (4) proves

\[
\boxed{
\frac12\le\liminf\varepsilon^{1/3}t_{\min}^H
\le\limsup\varepsilon^{1/3}t_{\min}^H\le4-2\sqrt3,
\quad H\in\{\mathrm{NW},\mathrm{AI},\mathrm{exp}\}.}
\tag{12}
\]

The second-moment bound (7) independently gives asymptotic upper constant
4/7. The integer fan improves this to about 0.535898385. It does not prove
that the optimal constant equals this number.

### Exact analytic integer upper bound

For 0<epsilon<=1/64 define

\[
D=(z+m^2/2)^2-2m^3,\quad
\tau_- =\frac{z+m^2/2-\sqrt D}{m^2},\quad
T_B=\lfloor\tau_-\rfloor+1.\tag{13}
\]

Then t_min^NW<=T_B, and T_B=c_* epsilon^(-1/3)+O(1).
To check the integer issue, m<=3 epsilon^(2/3)/4 and z>=epsilon imply
D>=5 epsilon^2/32>0. The distance between the two roots is

\[
\frac{2\sqrt D}{m^2}\ge\frac{4\sqrt{10}}9\varepsilon^{-1/3}>1.
\]

Also v_1=z-m<0, and the quadratic is increasing at 1. The first integer
strictly beyond the smaller root is therefore between the roots and has
positive v_t. This proves the finite-epsilon upper bound without a fitted
exponent or a floating-point infeasibility judgment.

## 4. Sharp metric distance asymptotics

Let d_TV denote half the l1 norm and let d_2 denote Euclidean distance on the
eight probability atoms. Define

\[
c_0=2^{-3/2},\qquad d_0=1-c_0.
\]

### Theorem 3

\[
\boxed{d_{\rm TV}(P_\varepsilon,\mathcal C_\triangle)
=d_0\varepsilon+O(\varepsilon^{4/3})},\tag{14}
\]

and

\[
\boxed{d_2(P_\varepsilon,\mathcal C_\triangle)
=\sqrt{8/7}\,d_0\varepsilon+O(\varepsilon^{4/3}).}\tag{15}
\]

#### Lower bounds

The independent product component of P_epsilon is compatible and lies within
TV epsilon and Euclidean O(epsilon). A nearest compatible law therefore has
this accuracy. Compactness, supplied by finite latent cardinality, ensures
existence [P3].

For a TV-nearest Q with distance delta, Q(000)>=z-delta and every zero-marginal
is <=m+delta. Finner gives
z-delta<=(m+delta)^(3/2)=c_0 epsilon+O(epsilon^(4/3)). Since z=epsilon+O(epsilon^2),
this proves the lower bound in (14).

For a Euclidean-nearest Q, coordinate and marginal deviations are also
O(epsilon). Finner again gives
P_epsilon(000)-Q(000)>=d_0 epsilon-O(epsilon^(4/3)).
A zero-sum eight-coordinate vector with one coordinate -D has Euclidean norm
at least sqrt(8/7)D: the other seven coordinates sum to D, and their squared
norm is at least D^2/7. This proves the lower bound in (15).

#### A single compatible construction attaining both bounds

Put h=d_0/7 and u=sigma+(c_0+h)epsilon. For sufficiently small epsilon, give
each of the three independent sources two independent bits: a base bit
Bern(sqrt(u)) and a flag Bern(h epsilon). A node outputs zero if both incident
base bits are one, or either incident flag is one. This is an ordinary
deterministic-response triangle model, with four states per source.

Without flags, the probabilities are

- 000: u^(3/2);
- each exactly-one-zero atom: u-u^(3/2);
- each exactly-two-zero atom: 0;
- 111: 1-3u+2u^(3/2).

At first order in epsilon, a flag creates the exactly-two-zero atom belonging
to its edge. Flag/base overlaps and multiple flags contribute only to the
stated remainder. Since u^(3/2)=c_0 epsilon+O(epsilon^(4/3)), the resulting Q
has

\[
Q(000)-P_\varepsilon(000)=-d_0\varepsilon+O(\varepsilon^{4/3}),
\]

\[
Q(x)-P_\varepsilon(x)=\frac{d_0}7\varepsilon+O(\varepsilon^{4/3})
\quad\text{for all seven }x\ne000.
\]

Taking the two norms proves the matching upper bounds. In particular,

\[
\boxed{t_{\min}^H(P_\varepsilon)
=\Theta(d_{\rm TV}(P_\varepsilon,\mathcal C_\triangle)^{-1/3})
=\Theta(d_2(P_\varepsilon,\mathcal C_\triangle)^{-1/3}).}\tag{16}
\]

This is a family-specific condition law, not a global characterization by a
single distance scalar.

## 5. NW convergence reconstructed, with explicit constants

Navascués–Wolfe [P1] prove a finite de Finetti comparison whose unhalved l1
error at diagonal degree g is

\[
2\left[1-\left(\frac{(n)_g}{n^g}\right)^L\right].\tag{17}
\]

Here L counts independent latent source types in the relevant correlation
presentation, and (n)_g is the falling factorial. Their resulting metric
closeness is O(sqrt(L/n)) in Euclidean norm. Alphabet size enters a conversion
to TV. Formula (17) must not be confused with a TV bound having the same
constant. The maintained repository already reconstructs the g=2 case [R4].

The following sharper bookkeeping is an elementary consequence of the same
empirical-table construction. For a full finite correlation scenario, a
deterministic inflated assignment omega defines a genuine compatible law
q_omega by sampling each source index independently and uniformly. Averaging
against a feasible extension gives E q_omega=P. Sampling twice gives

\[
\mathbb E q_\omega^{\otimes2}=\alpha P^{\otimes2}+(1-\alpha)R,
\qquad\alpha=(1-1/n)^L,
\]

because all source-index pairs are distinct with probability alpha. Therefore

\[
\begin{aligned}
\mathbb E\|q_\omega-P\|_2^2
&=(1-\alpha)\bigl(R\{x=y\}-\|P\|_2^2\bigr)\\
&\le(1-\alpha)(1-\|P\|_2^2).
\end{aligned}
\]

Some actual compatible component achieves no larger error; the mixture need
not be compatible. Thus

\[
\boxed{d_2(P,\mathcal C_G)^2\le
[1-(1-1/n)^L](1-\|P\|_2^2)
\le\frac{L(1-\|P\|_2^2)}n.}\tag{18}
\]

The binary triangle uses L=3, without adding private-root types: deterministic
empirical tables are already valid triangle responses. For other scenarios
one must specify a sufficient deterministic source presentation rather than
silently reuse this count.

For an incompatible P with delta_2=d_2(P,C_G)>0,

\[
\boxed{t_{\min}^{\rm NW}(P)\le
\left\lfloor\frac{L(1-\|P\|_2^2)}{\delta_2^2}\right\rfloor+1.}\tag{19}
\]

With K joint outcomes and delta=d_TV(P,C_G),

\[
\boxed{t_{\min}^{\rm NW}(P)\le
\left\lfloor\frac{LK}{4\delta^2}\right\rfloor+1.}\tag{20}
\]

These are explicit analytic bounds. Their effective use needs a certified
positive distance lower bound; finite rational classical instances also
permit such a bound to be computed by real algebraic methods, as below.

### What is not resolved

Let H_n=sup_{P in I_n} d_TV(P,C_triangle). The present hard family proves
H_n=Omega(n^(-3)), by choosing epsilon=[2(n-1)]^(-3). Equation (18) supplies
H_n=O(n^(-1/2)). Hence this work does not prove that the NW worst-case exponent
1/2 is sharp. It resolves the requested single-family exponent, not the
worst-case Hausdorff problem.

## 6. Why there is no global two-sided distance condition number

Consider R_p=(1-p)delta_111+p delta_000, 0<p<1. Then a=b=c=z=p, so the ratio
in (7) is exactly one. Consequently t_min^H(R_p)=2 for every named hierarchy:
order one is feasible and order two rejects. Yet R_p tends to the compatible
point delta_111, so its distance tends to zero.

Thus no universal bound t_min(P)>=c d(P,C)^(-a) with c,a>0 can hold on all
incompatible binary laws. Equation (16) is meaningful precisely because it
specifies the direction of approach to the boundary. The general upper bound
survives, and the rare-event fan ratio (7) can exploit geometry which plain
distance suppresses.

This also distinguishes hierarchy complexity from intrinsic decision
complexity. The P_epsilon family has a short Finner inequality certificate,
even when deriving rejection from the chosen inflation proof system requires
large t.

## 7. Finite witness margins and operational divergence

All KL divergences in this section use base-two logarithms. This convention
is essential for numerical constants.

### An exact normalization of the NW margin

Let K_t be the polytope of t-fold canonical diagonal marginals of symmetric
full inflated tables, and define

\[
\Delta_t(P)=d_{\rm TV}(P^{\otimes t},K_t).
\]

Finite-dimensional convex duality identifies this with the maximum separating
violation over functions of oscillation at most one. It is nondecreasing in
t, and positive exactly when order t rejects. Also

\[
\Delta_t(P)\le\min\{1,t\,d_{\rm TV}(P,\mathcal C_G)\}.\tag{21}
\]

For a lower bound, put beta_t=1-(1-1/t)^L. We obtain

\[
\boxed{\Delta_t(P)\ge\tfrac12[d_2(P,\mathcal C_G)^2-\beta_t]_+.}\tag{22}
\]

Proof. For R_t in K_t, its two-block marginal R_2 is within TV
eta=d_TV(R_t,P^t) of P^2. The empirical compatible mixture M_2 has form
alpha R_2+beta S_2, with R_2 and S_2 having the same one-block marginals.
For F_P(x,y)=1[x=y]-P(x)-P(y)+||P||_2^2, osc(F_P)<=2,
E_{P^2}F_P=0, and E_{q^2}F_P=||q-P||_2^2. Cancellation of the common
one-block marginals gives
E_{M_2}F_P<=2eta+beta. Every compatible component is at least d_2 away,
so d_2^2<=2eta+beta. Infimize over R_t.

The repository already has the same margin-to-distance mechanism with a
weaker collision constant, as well as its faithfulness application [R4].
Equation (22) is not a new conceptual definition or a first quantitative
faithfulness theorem.

### Applying the maintained stronger compiler to the sparse fan

The pinned exponential-separation proof [R5] strengthens the older compiler
to gamma_G(P)>=Delta^2/A_comp^2. For a rectangular witness with M corners,
its injectable terms use kappa=M-1; terms containing h>=2 independent
injectable pieces use kappa=M+h(M-1); and
A_comp=sum_j |a_j|sqrt(kappa_j/2). These are its conservative bit-KL constants.

For the fan (9), the root box is 1 by 1 by t, so M=t, not t^3.
There are t+1 unit-weight injectable terms, and t(t-1) two-piece cross terms
of weight 1/2. Therefore, whenever v_t in (10) is positive,

\[
\boxed{\gamma_\triangle(P_\varepsilon)\ge\frac{v_t^2}{A_t^2}},\qquad
A_t=(t+1)\sqrt{\frac{t-1}2}
+\binom t2\sqrt{\frac{3t-2}2}.\tag{23}
\]

This uses the maintained compiler, not a new proof of its general theorem.
Local stochastic response seeds can be bundled into incident independent
sources, preserving the triangle topology and the sparse box.

Choose t=ceil(epsilon^(-1/3)). Then
v_t=(3/8+o(1))epsilon^(2/3) and A_t^2=(3/8+o(1))t^5. Thus

\[
\boxed{\liminf_{\varepsilon\downarrow0}
\frac{\gamma_\triangle(P_\varepsilon)}{\varepsilon^3}\ge\frac38.}\tag{24}
\]

This is a certified lower rate, not an exact asymptotic for gamma.

### The reverse direction is already maintained

The existing effective-inflation proof [R6] uses independent local noise and
log-sum comparison to show, with delta=d_TV(P,C_triangle),

\[
\gamma_\triangle(P)\le a_1(P)\le
h(\delta):=\delta[9+2\log_2(1/\delta)].\tag{25}
\]

The function h is strictly increasing. Combining (25) with (20) gives

\[
t_{\min}^{\rm NW}(P)\le
\left\lfloor6/[h^{-1}(\gamma_\triangle(P))]^2\right\rfloor+1
=O(\gamma^{-2}\log^2(1/\gamma)).\tag{26}
\]

The order type, promise interpretation, and known-core computability status
are already present at the pinned revision. The repository's explicit
integer rule is 24*4^k, where (9+2k)2^(-k) is below the supplied positive KL
gap. No novelty is claimed for that rule here.

There can be no divergent universal lower bound on t_min purely in terms
of 1/gamma: the R_p family above has t_min=2 and
0<gamma(R_p)<=D(R_p||Bern(p)_{zero}^{tensor3})=2h_2(p), which tends to zero.
Faithfulness supplies the strict positivity for each p in (0,1).

## 8. Computability and a bit-length complexity law

Rosset–Gisin–Wolfe [P3] give finite latent cardinality and semialgebraicity.
For the binary triangle, six values per source suffice. The parameters are
three six-point source laws and three 6 by 6 stochastic binary response
tables. They form a compact semialgebraic parameter space, and the eight
observed probabilities are polynomial functions of these parameters.

For rational P, real quantifier elimination therefore decides compatibility.
It also determines the positive algebraic squared distance to the compatible
set when P is incompatible. Each finite-order NW test is a finite rational
LP. First deciding membership and then enumerating LPs on the incompatible
branch computes t_min. A zero sentinel or an infinity symbol can be used for
the compatible branch. This is already recognized as known-core in the live
repository [R6,R7], not an undecidability opportunity.

### Theorem 4: worst required order is exponential in rational encoding size

Fix the binary triangle and a standard explicit binary encoding of the eight
rational atom probabilities. Let ell(P) be its total bit length. For each of
the three named hierarchies,

\[
\boxed{
\max_{\ell(P)\le B,\ P\notin\mathcal C_\triangle}t_{\min}^H(P)
=2^{\Theta(B)}.}\tag{27}
\]

Proof of the upper bound. The graph of u=d_2(P,C_triangle)^2 is a fixed
semialgebraic set over the rationals. Eliminate latent parameters once.
This yields a fixed finite Boolean formula involving integer polynomials
in P and u, with fixed degrees. Substituting a rational P of bit length B
and clearing denominators produces univariate integer polynomials of fixed
degree and coefficient height 2^{O(B)}. At the unique positive value u,
at least one nonzero specialized polynomial must vanish: otherwise every
atomic sign, and hence the formula, would persist on a small interval,
contradicting uniqueness. Factor out any power of u. A nonzero positive root
of a fixed-degree integer polynomial with height H is at least c/H when
it is at most one, by bounding the nonconstant terms against its nonzero
integer constant coefficient. Hence u>=2^{-O(B)}. Equation (19) gives
t_min^NW<=2^{O(B)}, and stronger hierarchies reject no later.

Proof of the lower bound. Set k=2^j, epsilon=k^(-3), sigma=1/(2k^2).
All eight probabilities have denominator 8k^9 before reduction. An atom
with w ones has numerator (k^3-1)(2k^2-1)^w, with an additional 8k^6 at
000. Their total encoding length is O(j), but (4) gives t_min^H>=k/2.
Choose j proportional to B. This proves the lower bound.

The constants in (27) depend on the encoding and fixed scenario. This is a
law for required hierarchy level, not a runtime lower bound for all
compatibility algorithms. Indeed the fixed binary scenario has a fixed
quantifier-free membership formula, so membership is polynomial-time in
rational input bit length in principle, with potentially enormous fixed
constants. This last conclusion is a standard fixed-scenario consequence
of semialgebraicity, not a new efficient implementation.

For a variable alphabet on a fixed triangle, finite cardinality gives a
polynomial-size existential-real formulation. No matching hardness reduction
or general varying-graph complexity classification is established here.
The target-first regularized KL value remains only upper semicomputable in
the inspected maintained theory. Its two-sided computability is not implied
by computability of membership or of each finite-block minimum.

## 9. Exact computational certificates

The delivered generator and independent checker use only integer arithmetic
and fractions. They check the pointwise witness before substituting the
target. The packet includes an all-order nonnegative-polynomial certificate
partitioned into five integer cases, 174,760 exhaustive deterministic
assignments, 271,500 count-orbit cases, 2,660 NW cross-pair embeddings, 14 exact
rational targets, and eight rejected mutation/negative controls. Standard
Python and optimized Python (-O) produced identical PASS outputs.

Selected sandwich results for epsilon=k^(-3):

| k | Proved lower order | Certified fan upper order | Exact first order? |
|---:|---:|---:|:---|
| 4 | 4 | 4 | yes |
| 6 | 5 | 5 | yes |
| 8 | 6 | 6 | yes |
| 10 | 7 | 7 | yes |
| 16 | 10 | 10 | yes |
| 32 | 18 | 19 | no |
| 128 | 66 | 70 | no |
| 1024 | 514 | 551 | no |
| 65536 | 32770 | 35122 | no |

For epsilon=1/64, the order-four fan violation is exactly
6969/2097152. Combined with an order-three passing construction, this proves
first order four for all three variants. For epsilon=1/4096, the first order
is exactly ten.

No floating-point infeasibility result is used. No claim is made that a
first fan crossing is generally the first rejection of the complete LP.
The inherited repository reproduction scripts were read but were not rerun
in this session. The reported executed checks are the new packet's checks.

## 10. Priority, significance, and remaining boundary

The strongest direct mathematical predecessors are NW's quantitative
completeness [P1], WSF's pointwise/marginal witness method [P2], the triangle
Finner inequality used by the maintained construction, and the pinned
passing construction itself [R1]. Rosset–Gisin–Wolfe supplies the
computability foundation [P3]. The 2025 da Silva–Pozas-Kerstjens–Parisio
paper [P4] was inspected at its updated v2 main text; it proposes boundary
criteria based on explicit local models and numerical evidence and reports
finite low-order inflation calculations. The inspected portions do not
establish the all-order hard-family scaling law proved here.

The public search was bounded. It does not settle priority against all
postselected-inflation variants, theses, unpublished work, or all 2026
literature. The current repo's historical priority gate is itself unresolved.
The accurate priority statement is: a new derivation relative to the
inspected maintained upper-bound proof, with historical firstness not
certified.

Under the user's campaign rubric, the hard-family exponent target is met.
Under the repository's different significance vocabulary, a specialist
would need to assess the package as a strong instance-complexity theorem,
not as a proved sharp worst-case rate. Its ingredients are elementary; its
content is that they close the stated exponent gap and give exact boundary
distance and rational-encoding consequences.

Still open in this report: the exact leading constant in t_min(P_epsilon),
possible constant differences between hierarchy variants, the sharp
worst-case Hausdorff rate, a complete graph-theoretic finite-stabilization
classification, an exact gamma(P_epsilon) law, two-sided computability of
the regularized target-first divergence, and a quantum analogue.

Known finite-stabilization examples, including the star cases discussed by
NW, do not supply the requested full classification. No quantum theorem is
inferred by embedding a classical counterexample.

Highest-value next action: obtain a specialist proof-and-priority review of
the all-order fan theorem and the resulting sharp-exponent statement before
expanding the theorem package further.

## References and source keys

[P1] Miguel Navascués and Elie Wolfe, *The inflation technique completely
solves the causal compatibility problem*, arXiv:1707.06476v3. Theorem 1,
Euclidean extraction, Appendix A, and Section 4.1.

[P2] Elie Wolfe, Robert W. Spekkens, and Tobias Fritz, *The Inflation
Technique for Causal Inference with Latent Variables*, arXiv:1609.00672v5.
Definitions 7–8, marginal inequalities and logical-tautology constructions.

[P3] Denis Rosset, Nicolas Gisin, and Elie Wolfe, *Universal bound on the
cardinality of local hidden variables in networks*, arXiv:1709.00707v1;
Quantum Information and Computation 18 (2018), 910–926. Propositions 2–3
and Appendix D.

[P4] José Mário da Silva, Alejandro Pozas-Kerstjens, and Fernando Parisio,
*Local models and Bell inequalities for the minimal triangle network*,
arXiv:2503.16654v2, updated 26 September 2025. Main text and the stated
status of the proposed boundary criteria. Earlier v1 passages were also
retrieved; the final comparison uses v2.

[R1] `foundations/inflation-nontermination/proof.md` at the pinned commit.
[R2] Its `verification.md`, and `papers/inflation-nontermination/internal-review.md`.
[R3] `foundations/faithfulness/hierarchy-correction.md`.
[R4] `foundations/faithfulness/quantitative-proof.md`.
[R5] `foundations/inflation-strong-converse/exponential-separation.md` and `proof.md`.
[R6] `foundations/effective-inflation/proof.md`, substantive Sections 1–7.
[R7] `OPEN-PROBLEMS.md`, relevant `RESULTS.json`/`RESULTS.md` entries,
`SIGNIFICANCE.md`, and the relevant `PRIORITY.md` rows.
