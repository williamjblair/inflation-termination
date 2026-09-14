# Finite binary-triangle inflation does not stabilize

Keep the three hierarchy semantics distinct. This does not concern current retained constructor admission and does not assert publication priority.

Source edition: `RESULT.md` (`~/Documents/Codex/2026-08-29/assess-vela-breakthrough-chatgpt-conversation-6a91c3a3/work/continuous-campaign/axis5/gen244-binary-triangle-inflation-nontermination-audit/RESULT.md`), lines 32–128; original SHA256 `834bd9c2c41bbe7a12d6e0873c4ed623336c7576a5ae7e291b070f2c06028334`. The imported ranges and presentation-only changes are recorded in [the source index](<../SOURCES.json>). Source-specific labels inside the proof identify its original conventions, not a second current compiler.

**RESULT-CERT-0 specification delta (12 September 2026).**  The original
source is preserved above and in git history.  The maintained statement now
records the exact rational specialization, grounds rejection-order divergence
in its proved passing range, and corrects the `84/epsilon` scope from AI-only
to bare NW at order at least three.  No theorem was weakened.

## Exact theorem

For `t>=1`, `0<epsilon<1`, and

\[
Q(\varepsilon,r)
=\varepsilon\delta_{000}
+(1-\varepsilon)\operatorname{Bern}(r)^{\otimes3},
\]

the defect law proves

\[
\boxed{
0\le r\le(1-\varepsilon)^{t-1}
\quad\Longrightarrow\quad
Q(\varepsilon,r)\in\mathcal I_t^{\rm exp}
\subseteq\mathcal I_t^{\rm AI}
\subseteq\mathcal I_t^{\rm NW}.
}
\]

Here `NW` is the published permutation-symmetric diagonal-product hierarchy,
`AI` also prescribes products on ancestrally independent injectable blocks,
and `exp` additionally includes the recursive expressible-set marginals of
Wolfe--Spekkens--Fritz.  The inclusions displayed are inclusions of feasible
sets, so the strongest relaxation is written on the left.

Taking

\[
r=(1-\varepsilon)^{t-1},
\qquad 0<\varepsilon<t^{-3},
\]

gives a strict Finner violation and hence a point in every difference

\[
\mathcal I_t^{\rm exp}\setminus\mathcal C_\triangle,
\quad
\mathcal I_t^{\rm AI}\setminus\mathcal C_\triangle,
\quad
\mathcal I_t^{\rm NW}\setminus\mathcal C_\triangle.
\]

In particular, the completely explicit rational choice

\[
\varepsilon_t=\frac1{2t^3},\qquad
q_t=1-\varepsilon_t,\qquad
r_t=q_t^{t-1},\qquad
P_t=Q(\varepsilon_t,r_t)
\]

satisfies

\[
P_t\in\mathcal I_t^{\rm NW}\setminus\mathcal C_\triangle,
\qquad
P_t(000)^2-
P_{t,A}(0)P_{t,B}(0)P_{t,C}(0)
\ge\frac{\varepsilon_t^2}{2}>0
\]

for every `t>=1`.  This is the fixed-parameter version used by the exact
small-order certificates.

## Single family

For

\[
P_\varepsilon
=Q\left(\varepsilon,1-\tfrac12\varepsilon^{2/3}\right),
\qquad 0<\varepsilon<\tfrac18,
\]

one has

\[
P_\varepsilon\notin\mathcal C_\triangle,
\qquad
P_\varepsilon\to\delta_{111},
\]

and

\[
t\le1+\tfrac12\varepsilon^{-1/3}
\quad\Longrightarrow\quad
P_\varepsilon\in\mathcal I_t^{\rm exp}.
\]

The displayed passing-order lower bound, rather than convergence to
`delta_111` by itself, proves that the rejecting order diverges for every
hierarchy above.  The separate empirical-triangle argument also gives, for
`epsilon<=1/64`,

\[
t_{\min}^{\rm NW}(P_\varepsilon)\le\frac{84}{\varepsilon}.
\]

Although the original proof scoped this estimate to AI products, bare NW
symmetry and its degree-two and degree-three diagonal laws already supply the
products used in the empirical expansion at every relevant order `t>=3`.

## Repairs

1. The zero-rate endpoint in the general membership statement needs private
   kill probability `s=1`; use `s in [0,1]`, not `[0,1)`.
2. The published NW hierarchy and the stronger AI/expressible hierarchy must
   not be called identical.  The construction passes all of them, which is
   stronger than needed.
3. Recursive expressible-set compatibility is justified by an explicit
   latent-projection argument, not merely by unconditional independence of
   ancestrally disjoint blocks.
4. The `84/epsilon` rejection bound is not AI-only: at order `t>=3`, the bare
   NW diagonal law and source-index symmetry give the two-triangle and three-
   singleton products used in its collision expansion.
5. The moment-extension proof supplied independently is not used to repair
   this proof and remains a separate audit target.
6. Convergence `P_epsilon -> delta_111` does not itself imply a diverging
   rejecting order; the explicit passing range does.
