# The worst-case convergence exponent along the cycle parity direction

Computational campaign, 2026-09-14. Square (4-cycle) and triangle, both
hierarchies, orders `t = 1 .. 10`.

| file | role |
| --- | --- |
| `build_exponent.py` | discovery (scipy LP) and exact certificate construction; writes `certificates/*.json` |
| `verify_exponent.py` | independent checker, Python standard library only, no floating point, refuses `-O` |
| `analyse_exponent.py` | reads the certificates and prints the bracket table, the fits and the separations |
| `certificates/square.json`, `certificates/triangle.json` | the certificates |

```
python3 build_exponent.py --max-order 10
python3 verify_exponent.py
python3 analyse_exponent.py
```

Nothing in `paper/`, `release/` or `artifact/` was touched.

---

## 1. What is measured

For the cycle `C_m` and `q >= 0` let `P_{m,q}` be the parity family of
Definition `def:cycletarget`, the law on `{-1,1}^m` with
`E[prod_{v in F} O_v] = (-q)^{|dF|/2}`. For `m = 4` this is the square family
`P_q` of `eq:squaretarget`, a probability law exactly on `[0, 3 - 2 sqrt 2]`;
for `m = 3` it is `Pi(-q,-q,-q)` of `eq:paritylaw`, a probability law exactly
on `[0, 1/3]`. Set, for `H` in `{AI, NW}`,

```
    q_max^H(t) = sup { q in [0, q_top] : P_{m,q} in I^H_t(C_m) },
```

with `q_top` a rational cap at the top of the probability range:
`1715728752/10^10 < 3 - 2 sqrt 2` for the square, exactly `1/3` for the
triangle. `Theorem thm:squarelinear` and `Theorem thm:trianglelinear` give
`q_max^AI(t) >= 1/(16 t)`.

### 1.1 The supremum is a threshold

**Lemma (monotonicity in `q`).** If `P_{m,q} in I^H_t(C_m)` and
`0 <= q' <= q` then `P_{m,q'} in I^H_t(C_m)`.

*Proof.* By Section 2 a witness is a law on sign potentials `s = (s_{g,i})`.
Multiply every `s_{g,i}` by an independent `+-1` variable of mean
`rho = sqrt(q'/q)`. A character of total degree `S` is multiplied by `rho^S`,
so its value `(-q)^{S/2}` becomes `(-q')^{S/2}`. The result is again a law,
again invariant under the copy-index permutations and the global flip, and
every prescribed character now takes the value prescribed for `P_{m,q'}`. []

Proved by hand here, not machine-checked. The certificates do not depend on
it: infeasibility is certified directly on the whole interval `[q_hi, q_top]`.

---

## 2. The count-moment reduction used

`Lemma lem:countmoment` states the reduction for the square and `AI_t`. The
campaign needs it for the triangle too, and for `NW_t`. The form used is:

> Let `m in {3,4}`, `t >= 1`, `q` in the probability range. Then
> `P_{m,q} in I^H_t(C_m)` if and only if there are `w_a >= 0`,
> `a in {0..t}^m`, with `sum_a w_a = 1` and
>
> ```
>     sum_a w_a prod_g K^{(t)}_{k_g}(a_g) = (-q)^{S/2},    S = sum_g k_g,
> ```
>
> for exactly the degree tuples `k` in `D_H(t)`, where
>
> * `D_AI(t) = { k in {0..t}^m : S even, 2 max_g k_g <= S }`;
> * `D_NW(t) = { b_1 + ... + b_t : each b_r an even-weight 0/1 vector }`.

**(a) Parity forcing, both hierarchies.** A copied cycle picks one copy index
per source and the corresponding copied observation at each vertex.
Independent permutations of the copy indices carry it to the first diagonal
row, so under any symmetric witness it has the diagonal law `P_{m,q}`, whose
total product is `+1` almost surely (`eq:cycletarget` at `F` = all vertices).
For `AI_t` this also follows from injectability.

**(b) Sign potentials.** The arrays satisfying every copied-cycle parity are
exactly `O_v^{(i,j)} = s_{v-1,i} s_{v,j}`, with `s` unique up to the
simultaneous flip of all `m` families. For `m = 4` this is the argument in the
proof sketch of `lem:countmoment`. For `m = 3`, in the convention of
`thm:trianglelinear` (`A^{ij} = x_i z_j`, `B^{ik} = x_i y_k`,
`C^{jk} = z_j y_k`): from `A^{ij} B^{ik} C^{jk} = 1` at `j = 1`,
`B^{ik} = A^{i1} C^{1k}`, so `x_i := A^{i1}`, `y_k := C^{1k}` give
`B^{ik} = x_i y_k`; at `i = 1`, `C^{jk} = A^{1j} x_1 y_k`, so
`z_j := A^{1j} x_1` gives `C^{jk} = z_j y_k` and then `A^{ij} = x_i z_j`.
Flips `(eps, delta, gamma)` of `(x, y, z)` leaving all three arrays fixed obey
`eps gamma = eps delta = gamma delta = 1`, hence are equal: a global flip.

**(c) Symmetrization.** Averaging a witness over independent copy-index
permutations and over the global flip leaves a law exchangeable inside each
family, i.e. a mixture over the count vector `a = (a_g)` of the uniform law on
the corresponding slice. The average of `prod_g prod_{i in I_g} s_{g,i}` with
`|I_g| = k_g` is `prod_g K^{(t)}_{k_g}(a_g)`, the normalized Krawtchouk
polynomial being the mean of a `k`-element sign product drawn without
replacement.

**(d) Which degrees are prescribed.**

*AI.* By `Lemma lem:boundary` the boundary of an injectable block is empty or
a pair of copied sources in two distinct families, and the blocks of an AI
family have disjoint ancestries, so the boundary elements are distinct. The
degree tuple is therefore the degree sequence of a loopless multigraph on the
`m` source types with at most `t` at each node: `S` even and
`2 max_g k_g <= S`. Conversely every such tuple is realized, and both scripts
*construct* an explicit AI family for every tuple in `D_AI(t)` and validate it
against the definitions (each block injectable, blocks pairwise ancestrally
disjoint, total boundary equal to `k`): each multigraph edge is routed along an
arc of the source cycle and given fresh copy indices. In addition, for
`t <= 3` both scripts enumerate *every* AI family of the order-`t` inflation by
brute force and confirm that the boundary degree tuples are exactly `D_AI(t)`.
This reproduces the counts in the existing classification certificate:
`33` NW against `37` AI degree tuples at `t = 2`, `96` against `112` at
`t = 3` (square).

*NW.* The diagonal law prescribes exactly the characters
`prod_r prod_{v in F_r} O_v^{(r)}`, one vertex subset per diagonal row. In
potential form the degree of family `g` is `#{ r : g in dF_r }` and the value
is `prod_r (-q)^{|dF_r|/2} = (-q)^{S/2}`. The boundary map on vertex subsets
of `C_m` has image exactly the even-weight vectors (the cut space of a
connected graph), so `D_NW(t)` is the set of `t`-fold sums of even-weight
vectors. Both scripts recompute it by dynamic programming and check
`D_NW(t)` is contained in `D_AI(t)`.

**(e) Sufficiency.** Given `w`, draw `a ~ w`, then a uniformly random sign
assignment with `a_g` negatives in family `g`, and define the copied
observations by the potential. The law is symmetric by construction; all
diagonal-law characters match, so the diagonal law is `P_{m,q}^{ot}`; and for
`AI`, every character of an AI set, or of a subset of one of its blocks, has a
degree tuple in `D_AI(t)` and value `(-q)^{S/2}` (`lem:boundary` again). A law
on a finite sign cube is determined by its characters, so all the prescriptions
hold.

The verifier assumes (a)-(e). Everything downstream is checked exactly.

### 2.1 Symmetry used in the search only

`D_AI(t)`, `D_NW(t)` and the right-hand side `(-q)^{S/2}` are invariant under
permuting the `m` families, so the feasible set may be symmetrized over the
full symmetric group and the LP reduced to orbit masses on nondecreasing count
tuples indexed by nondecreasing degree keys. That is a reduction of the search
only: the emitted primal is an `S_m`-invariant distribution on all `(t+1)^m`
count configurations and the emitted dual is a functional on all of them, and
the verifier checks the unsymmetrized statements.

---

## 3. What each certificate contains

* **Lower end.** A rational `w >= 0` on the count configurations with
  `sum w = 1` satisfying every equation of the system at a rational `q_lo`, in
  exact fractions.
* **Upper end.** A chain of rational Farkas vectors `c` on the degree keys with
  `sum_k c_k kbar(k, a) <= 0` at every one of the `(t+1)^m` count
  configurations, whose prescribed expectations
  `p(q) = sum_k c_k (-q)^{S/2}` are rational polynomials, and whose positivity
  intervals chain together to cover `[q_hi, q_top]`. Positivity on each piece
  is certified by Sturm's theorem: positive at both ends and no root inside.
  So `P_{m,q}` is outside `I^H_t` for **every** `q` in `[q_hi, q_top]`, not
  only at `q_hi`.

The dual cone is independent of `q` (only the objective depends on it), which
is why a single dual usually covers the whole interval in one piece.

---

## 4. Certified brackets

`q_lo` is certified feasible, `q_hi` certified infeasible together with the whole
of `[q_hi, q_top]`. Every entry marked `(cap)` means the hierarchy accepts
`P_{m,q}` at the top of the range tested, so no upper bound is claimed at that
order. Ratio is `q_lo^NW / q_lo^AI`.

### 4.1 Square (`C_4`), cap `q_top = 1715728752/10^10 < 3 - 2 sqrt 2`

|  t | AI `q_lo` | AI `q_hi` | NW `q_lo` | NW `q_hi` | `t q^AI` | `t q^NW` | NW/AI |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
|  1 | 0.1715728742 | (cap) | 0.1715728742 | (cap) | 0.17157 | 0.17157 | 1.0000 |
|  2 | 0.1324743290 | 0.1324743330 | 0.1715628752 | (cap) | 0.26495 | 0.34313 | 1.2951 |
|  3 | 0.0950228950 | 0.0950228990 | 0.0950228950 | 0.0950228990 | 0.28507 | 0.28507 | 1.0000 |
|  4 | 0.0835279580 | 0.0835279620 | 0.0950228950 | 0.0950228990 | 0.33411 | 0.38009 | 1.1376 |
|  5 | 0.0657380020 | 0.0657380060 | 0.0657380020 | 0.0657380060 | 0.32869 | 0.32869 | 1.0000 |
|  6 | 0.0603176600 | 0.0603176640 | 0.0645356170 | 0.0645356210 | 0.36191 | 0.38721 | 1.0699 |
|  7 | 0.0502565110 | 0.0502565150 | 0.0502565110 | 0.0502565150 | 0.35180 | 0.35180 | 1.0000 |
|  8 | 0.0470271490 | 0.0470271530 | 0.0494541280 | 0.0494541320 | 0.37622 | 0.39563 | 1.0516 |
|  9 | 0.0406784540 | 0.0406784580 | 0.0406784540 | 0.0406784580 | 0.36611 | 0.36611 | 1.0000 |
| 10 | 0.0384981990 | 0.0384982030 | 0.0400943600 | 0.0400943640 | 0.38498 | 0.40094 | 1.0415 |

### 4.2 Triangle (`C_3`), cap `q_top = 1/3` (the exact endpoint)

|  t | AI `q_lo` | AI `q_hi` | NW `q_lo` | NW `q_hi` | `t q^AI` | `t q^NW` | NW/AI |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
|  1 | 0.3333333333 | (cap) | 0.3333333333 | (cap) | 0.33333 | 0.33333 | 1.0000 |
|  2 | 0.2679491900 | 0.2679491940 | 0.3333333333 | (cap) | 0.53590 | 0.66667 | 1.2440 |
|  3 | 0.1999999980 | 0.2000000020 | 0.1999999980 | 0.2000000020 | 0.60000 | 0.60000 | 1.0000 |
|  4 | 0.1730047060 | 0.1730047100 | 0.1999999980 | 0.2000000020 | 0.69202 | 0.80000 | 1.1560 |
|  5 | 0.1428571400 | 0.1428571440 | 0.1428571400 | 0.1428571440 | 0.71429 | 0.71429 | 1.0000 |
|  6 | 0.1283741760 | 0.1283741800 | 0.1381856900 | 0.1381856940 | 0.77025 | 0.82911 | 1.0764 |
|  7 | 0.1092774840 | 0.1092774880 | 0.1092774840 | 0.1092774880 | 0.76494 | 0.76494 | 1.0000 |
|  8 | 0.1011416960 | 0.1011417000 | 0.1070388380 | 0.1070388420 | 0.80913 | 0.85631 | 1.0583 |
|  9 | 0.0888129680 | 0.0888129720 | 0.0888129680 | 0.0888129720 | 0.79932 | 0.79932 | 1.0000 |
| 10 | 0.0833179940 | 0.0833179980 | 0.0870307060 | 0.0870307100 | 0.83318 | 0.87031 | 1.0446 |

Every bracket is `4 * 10^-9` wide. `verify_exponent.py` passes 20004 exact
checks in about 44 seconds; `build_exponent.py --max-order 10` takes about 27
minutes, almost all of it in the exact `10 x 10` square solves (the `t = 10`
square primal and dual are `431` and `351` rational unknowns; `t = 11` was left
uncertified, see Section 7).

### 4.3 Exact values where the dual polynomial factors

The first dual piece of each order is a rational polynomial whose sign change
sits inside the bracket. Several factor:

| scenario | order | dual polynomial | threshold |
| --- | --- | --- | --- |
| square | `t = 2`, AI | `q^4 - 32 q^3 - 6 q^2 + 24 q - 3 = (1+q)(q^3 - 33 q^2 + 27 q - 3)` | the root `r` of `g` in `prop:lowthresholds`, `0.13247433...` |
| square | `t = 3`, AI = NW | `3 q^6 - 30 q^5 - 19 q^4 + 28 q^3 - 19 q^2 - 30 q + 3` (palindromic) | `0.09502290...` |
| triangle | `t = 2`, AI | `q^3 - 3 q^2 - 3 q + 1 = (q+1)(q^2 - 4q + 1)` | `2 - sqrt 3` exactly |
| triangle | `t = 3`, AI = NW | `5 q^3 + 9 q^2 + 3 q - 1 = (5q - 1)(q+1)^2` | `1/5` exactly |
| triangle | `t = 4`, NW | `5 q^4 + 14 q^3 + 12 q^2 + 2 q - 1 = (5q - 1)(q+1)^3` | `1/5` exactly |
| triangle | `t = 5`, AI = NW | `7 q^5 + 27 q^4 + 38 q^3 + 22 q^2 + 3 q - 1` | rational root `1/7` |

The `t = 2` square entry is the paper's own dual `D`, recovered here
independently from the LP: `E[D] = (1+q) g(q)` with
`g(q) = q^3 - 33 q^2 + 27 q - 3`, exactly as `prop:lowthresholds` states.

At every **odd** order the AI dual and the NW dual come out *identical* (square
`t = 3, 5, 7, 9`; triangle `t = 3, 5, 7, 9`), and in most cases palindromic
(self-reciprocal). At even orders the two are different polynomials and the AI
one has much larger coefficients.

---

## 5. Scaling

Both hierarchies, both cycles: **exponent 1**, with a clear odd/even
oscillation superimposed.

The one-step log-log slope alternates (square AI: `-0.82, -0.45, -1.07, -0.47,
-1.18, -0.50, -1.23, -0.52` for `t = 2..10`) because consecutive orders sit on
different branches. The same-parity slope `d ln q / d ln t` from `t` to `t+2` is
the meaningful one and drifts monotonically towards `-1`:

| `t -> t+2` | square AI | square NW | triangle AI | triangle NW |
| --- | ---: | ---: | ---: | ---: |
| 2 -> 4 | -0.665 | | -0.631 | |
| 4 -> 6 | -0.803 | -0.954 | -0.736 | -0.912 |
| 6 -> 8 | -0.865 | -0.925 | -0.829 | -0.888 |
| 8 -> 10 | -0.897 | -0.940 | -0.869 | -0.927 |

Assuming `t q_max(t) = c - a/t` and eliminating `a` from same-parity pairs:

| pair | square AI | square NW | triangle AI | triangle NW |
| --- | ---: | ---: | ---: | ---: |
| (4,6) | 0.4175 | 0.4015 | 0.9267 | 0.8873 |
| (6,8) | 0.4192 | 0.4209 | 0.9258 | 0.9379 |
| (8,10) | 0.4200 | 0.4222 | 0.9294 | 0.9263 |

So

```
    q_max^AI(t) = q_max^NW(t) (1 + O(1/t)) = c_m / t + O(1/t^2),
    c_4 ~ 0.420 (square),      c_3 ~ 0.927 (triangle).
```

The answer to the question asked is therefore **exponent 1, not slower**: the
linear lower bounds `q >= 1/(16t)` of `thm:squarelinear` and
`thm:trianglelinear` have the right exponent and are loose only in the
constant, by a factor `16 c_4 ~ 6.7` on the square and `16 c_3 ~ 14.8` on the
triangle.

Uncertified floating-point continuation (same LP, no exact certificate; listed
because it supports the extrapolation, not because it is proved):

| t | square AI | square NW | triangle AI | triangle NW |
| ---: | --- | --- | --- | --- |
| 11 | 0.0341673711 | 0.0341673711 | 0.0745969210 | 0.0745969210 |
| 12 | | | 0.0707484078 | 0.0732603051 |
| 13 | | | 0.0643174762 | 0.0643174762 |
| 14 | | | 0.0614290315 | 0.0632745398 |
| 15 | | | 0.0565222200 | 0.0565306427 |
| 16 | | | 0.0541947960 | 0.0556384604 |

(`t q` at `t = 16` on the triangle: 0.867 AI, 0.890 NW, still climbing towards
`c_3`.)

---

## 6. Separations

### 6.1 `AI_t` against `NW_t` at the same order

Along the parity direction the two hierarchies separate **exactly at the even
orders** and **coincide at the odd orders**. Certified, for the square:

```
    t = 2:  q_max^AI <= 0.1324743330 < 0.1715628752 <= q_max^NW
    t = 4:  q_max^AI <= 0.0835279620 < 0.0950228950 <= q_max^NW
    t = 6:  q_max^AI <= 0.0603176640 < 0.0645356170 <= q_max^NW
    t = 8:  q_max^AI <= 0.0470271530 < 0.0494541280 <= q_max^NW
    t = 10: q_max^AI <= 0.0384982030 < 0.0400943600 <= q_max^NW
```

and for the triangle:

```
    t = 2:  q_max^AI <= 0.2679491940 < 0.3333333333 <= q_max^NW
    t = 4:  q_max^AI <= 0.1730047100 < 0.1999999980 <= q_max^NW
    t = 6:  q_max^AI <= 0.1283741800 < 0.1381856900 <= q_max^NW
    t = 8:  q_max^AI <= 0.1011417000 < 0.1070388380 <= q_max^NW
    t = 10: q_max^AI <= 0.0833179980 < 0.0870307060 <= q_max^NW
```

Each of these certifies `I^AI_t(C_m) != I^NW_t(C_m)` by exhibiting a `q` in the
gap (any rational strictly between the two endpoints), and in fact certifies it
for the whole interval between them, since the AI dual is positive on
`[q_hi^AI, q_top]` and the NW primal is feasible at `q_lo^NW` (and below it, by
the monotonicity lemma).

At `t = 3, 5, 7, 9` the two brackets are *identical* — not merely overlapping:
the LP returns the same threshold and the same dual polynomial for the two
degree systems, although the degree systems themselves differ at every order
`t >= 2` (square: 96 NW against 112 AI degree tuples at `t = 3`; 3400 against
4200 at `t = 9`). The extra AI degree equations are not binding at odd orders
along this direction. This is a genuine answer to the `t = 3` part of Goal 3:
**there is no AI/NW separation on the square at `t = 3` along the parity
direction**; the separation reported in `prop:lowthresholds` at `t = 2` and the
new ones at `t = 4, 6, 8, 10` are even-order phenomena.

The gap closes like `1/t`: the ratio `q^NW / q^AI` at even orders is
`1.2951, 1.1376, 1.0699, 1.0516, 1.0415` at `t = 2,4,6,8,10`, i.e. about
`1 + 0.41/t` on the square and `1 + 0.46/t` on the triangle, so
`q^NW(t) - q^AI(t) = O(1/t^2)`.

### 6.2 Does `NW_{t+1}` already beat `AI_t`?

Certified yes at every order except `t = 3` (square and triangle), where
`q_max^NW(4) = q_max^AI(3)`:

```
    square   t = 2:  q^NW(3) <= 0.0950228990 < 0.1324743290 <= q^AI(2)
             t = 4:  q^NW(5) <= 0.0657380060 < 0.0835279580 <= q^AI(4)
             t = 5:  q^NW(6) <= 0.0645356210 < 0.0657380020 <= q^AI(5)
             t = 6:  q^NW(7) <= 0.0502565150 < 0.0603176600 <= q^AI(6)
             t = 7:  q^NW(8) <= 0.0494541320 < 0.0502565110 <= q^AI(7)
             t = 8:  q^NW(9) <= 0.0406784580 < 0.0470271490 <= q^AI(8)
             t = 9:  q^NW(10) <= 0.0400943640 < 0.0406784540 <= q^AI(9)
```

with the same pattern on the triangle. The `t = 3` exception is the observation
that `q_max^NW(3) = q_max^NW(4)`: along this direction the fourth order of the
Navascues-Wolfe hierarchy buys nothing over the third. On the triangle both
equal `1/5` exactly.

### 6.3 Consistency with `thm:orderconversion`

`NW_{floor(3t/2)} subset AI_t` requires `q_max^NW(floor(3t/2)) <= q_max^AI(t)`.
Checked at `t = 1..6` (so `NW_9` against `AI_6`), square and triangle: **no
contradiction at any order**. It is strict at `t = 2, 4, 5, 6` and *tight* at
`t = 3`, where the brackets for `q_max^NW(4)` and `q_max^AI(3)` coincide. The
parity direction therefore does not refute the stronger statement
`NW_t subset AI_t` (i.e. `NW_t = AI_t`) at odd `t` — it is consistent with it.

---

## 7. Discrepancies, caveats, and what this does and does not settle

1. **The linear lower bounds are right in the exponent and loose in the
   constant.** `thm:squarelinear`/`thm:trianglelinear` give `q >= 1/(16t)`;
   the truth is `~ 0.420/t` and `~ 0.927/t`. Feeding the certified `q_lo` into
   the distance machinery of `cor:squaredistance` and `cor:triangledistance`
   (which applies to any witness, since the noise argument only multiplies
   characters by `(1-2 eta)^{|F|}` on both sides) gives, at `t = 10`,

   ```
       H^AI_10(square)   >= 5 q / 48   = 0.0040102   (paper: 5/(768*10)  = 0.00065)
       H^AI_10(triangle) >= 13 q / 192 = 0.0056412   (paper: 13/(3072*10) = 0.00042)
   ```

   a factor 6.2 and 13.3. These are per-order statements from per-order
   certificates, not a closed-form improvement of the theorems, and they are
   not machine-checked here (only the `q` is).

2. **The parity direction does not close the gap in `cor:brackets`.** The
   bracket there is `c/t <= H^AI_t <= H^NW_t <= sqrt(K-1)/(2 sqrt t)`. Along
   this direction `NW` has the *same* exponent as `AI` and a constant within
   `1 + O(1/t)` of it, so the parity family cannot exhibit `t^{-1/2}` behaviour
   for `NW`. If `H^NW_t(square)` really decays like `t^{-1/2}`, the near-extremal
   laws lie in some other direction; and if the convex-order upper bound of
   `thm:convexorder` is loose, this direction gives no evidence either way.
   Question `q:hausdorff` is untouched: what is measured here is one family,
   not the supremum over the feasible set.

3. **Odd/even alternation is the dominant structure and is not explained.**
   AI and NW coincide at odd orders (certified `t <= 9`) and separate at even
   orders (certified `t <= 10`); the same alternation shows up in `t q_max(t)`
   and in the dual polynomials (identical and palindromic at odd orders). The
   uncertified numerics at `t = 15` on the triangle show AI `0.05652222` against
   NW `0.05653064`, a relative gap of `1.5 * 10^-4`: either the odd-order
   coincidence fails eventually, or that is floating-point noise at an order
   where the LP is poorly conditioned. This should be settled by certifying
   `t = 11, 13, 15` on the triangle before anything is claimed about it.

4. **What is exact and what is not.**
   * Exact (rational arithmetic, re-checked by `verify_exponent.py`): the two
     degree systems and the containment between them at every order `t <= 10`;
     the brute-force enumeration of AI families at `t <= 3` and the explicit AI
     realization of every AI degree tuple at every `t <= 10`; every primal
     witness at `q_lo`; every dual functional's nonpositivity on all `(t+1)^m`
     count configurations; every dual expectation polynomial; the Sturm
     certificates that those polynomials have no root in their stated
     intervals, hence infeasibility on the whole of `[q_hi, q_top]`.
   * Assumed, proved by hand, not machine-checked: the count-moment reduction
     itself (Section 2, extending `lem:countmoment` to the triangle and to
     `NW_t`), and the monotonicity lemma of Section 1.1. The necessity half of
     the AI degree characterisation (boundary pairs give a loopless multigraph
     degree sequence) is a hand proof for `t >= 4`; it is machine-confirmed for
     `t <= 3` by brute force, and the sufficiency half is machine-confirmed at
     every `t <= 10` by explicit construction.
   * Numerical only: everything in the `t >= 11` table of Section 5, the fitted
     constants `c_4 ~ 0.420` and `c_3 ~ 0.927`, and the fitted exponents.

5. **Where the campaign stopped and why.** The certified range is `t <= 10` for
   both cycles. The bottleneck is not the LP but the exact rational solve on the
   LP basis: the square at `t = 10` has 431 (AI) and 351 (NW) rational unknowns
   and took 682 s and 433 s; `t = 11` would have roughly 560 and 460, with
   numerators growing faster than `n^3`, so an order or two more is affordable
   but not much beyond that with this method. The floating-point LP itself is
   cheap (the `t = 11` square bisection took 227 s) but the count system becomes
   badly scaled at large `t` — the target moments are `(-q)^{S/2}` with `S` up
   to `4t`, i.e. `10^-24` at `t = 10` — so numbers past `t = 11` on the square
   and `t = 16` on the triangle were not attempted. (The discovery LP is run in
   a shifted, well-scaled form: the unknown is the deviation from the corrected
   density of `lem:corrected`, which satisfies every moment equation identically
   in `q` and for every value of the constant `c`, so the right-hand side of the
   discovery LP is zero and only positivity is at stake.)

6. **Small mismatches with the certificate endpoints.** `q_lo` for `NW_2` on the
   square is `0.1715628752`, one part in `10^5` below the cap rather than at it:
   at the cap the LP vertex is degenerate and the exact solve on its support
   fails, so the builder backs off. That is a property of the certificate, not
   of the threshold: by the monotonicity lemma, membership at `0.1715628752`
   gives membership below it, and the LP finds `NW_2` feasible numerically all
   the way to the cap.

---

## 8. Cross-checks against the paper

* The `AI_2` dual on the square is exactly the paper's `D` of
  `prop:lowthresholds`: expectation `(1+q)(q^3 - 33 q^2 + 27 q - 3)`, nonpositive
  on all 81 count configurations with maximum 0. Reproduced from scratch.
* `P_{3/20} in NW_2 \ AI_2`: certified here, since
  `q_max^AI(2) <= 0.132474333 < 3/20` (the AI dual is positive at `3/20`, which
  lies in `[q_hi, q_top]`) and `3/20 < 0.1715628752 <= q_max^NW(2)`.
* `P_{1/10} in AI_2 \ NW_3`: certified here, since
  `q_max^NW(3) <= 0.095022899 < 1/10` and `1/10 < 0.132474329 <= q_max^AI(2)`.
* `33 / 37` NW and AI degree tuples at `t = 2` and `96 / 112` at `t = 3` on the
  square, reproduced by brute force over all AI families and by the dynamic
  programme over diagonal-row boundaries.
* `INW_3 subsetneq IAI_2 subsetneq INW_2` (the chain of `prop:lowthresholds`)
  follows from the `t = 2` and `t = 3` brackets.
