# Classification certificates

Exact rational certificates for the new inflation results of the 2026-09-13 packet,
as audited in `research-handoffs/2026-09-13/claude-code/review/AUDIT-NOTES.md`.
Where the audit notes and the packet disagree, the constants here follow the audit
notes.

Every number below was produced by exact integer and `fractions.Fraction`
arithmetic. No floating point enters any certified claim. Floating point is used
only inside `build_classification.py`, and only to *discover* linear-programming
solutions and dual vectors that are then rationalized and re-verified exactly.

## Files

| file | content |
|---|---|
| `build_classification.py` | generator; numpy/scipy for LP discovery only |
| `verify_classification.py` | verifier; standard library only (`fractions`, `itertools`, `json`, `hashlib`), refuses `-O`/`-OO`, raises `CertificateError` on any failure |
| `five_path.json` | five-path witness, B5 2.2 / AUDIT-NOTES A4 |
| `cycles.json` | cycle witnesses, B4 3-6 / B5 4 |
| `square.json` | corrected square density, B6 1-3 |
| `triangle.json` | triangle analogue, AUDIT-NOTES B2(ii), not in the packet |
| `low_order_square.json` | low-order square thresholds, B6 5 |
| `MANIFEST.json` | SHA-256 of every file in this directory |

Replay:

```
python3 -B papers/inflation-nontermination/artifact/certificates/classification/verify_classification.py
python3 -B papers/inflation-nontermination/artifact/certificates/classification/build_classification.py   # regenerates the JSON
```

The verifier takes about half a minute; the builder about a minute.

## Conventions

* Signs are +-1; a stored bit 1 means the sign -1. For the five-path endpoints A
  and E the stored bit is the {0,1} setting x resp. z of the target formula.
* TV distance is half the l1 distance.
* A global witness is a normalized nonnegative table on **all** copied observations.
* **NW_t**: invariance under independent permutations of each source's copy
  indices, plus the full diagonal law P^(x)t.
* **AI_t**: additionally every injectable set (a subset of one copied original
  scenario, i.e. one copy of each source) carries the target marginal, and every
  family of pairwise ancestrally-disjoint injectable sets carries the product
  joint law.

Injectable sets are enumerated by brute force from the definition: choose one copy
index per source, take the copied original scenario it selects, take all of its
nonempty subsets. AI families are enumerated by brute force as all sets of
pairwise ancestrally-disjoint injectable sets. At every order with at most 20
copied observations the verifier *also* enumerates all 2^n masks, splits each into
shared-source-copy components, keeps the masks whose components are all injectable
(these are the "AI sets" counted below), and checks every partition of those
components into blocks with injectable union. The two enumerations produce the
same prescriptions, which is itself checked.

A check on an AI family {F_1,...,F_r} is the single character equality
E_witness[chi_{union F_i}] = prod_i Phat_target(vertices(F_i)). Ranging over all
families this is equivalent to the full joint-law prescription, because every
subset U_i of F_i again forms a family.

## 1. Five-path witness (B5 2.2)

Scenario A(X), B(X,L), C(L,R), D(R,Z), E(Z).
Target P_h(x,b,c,d,z) = (1/32)[1 + bcd (1+h)/4 (1+(-1)^(x+z))], h = 1/(16 t^2).
Witness: auxiliary law H_t(u,v) = 2^(-2t) Re[prod (1 + i gamma u_i) prod (1 - i gamma v_j)],
gamma = 1/(4t), built here as the real polynomial sum over even S of (-h)^(|S|/2)
times the product over S of sigma, with sigma = (u, -v); fair endpoint bits X_a,
Z_e; fair masks r_i, s_j; fair private eps_{ij}; A^a = X_a, B^{ai} = r_i u_i^{X_a},
D^{je} = s_j v_j^{Z_e}, E^e = Z_e, and C^{ij} = r_i s_j, multiplied by eps_{ij}
exactly when u_i != v_j.

Built at **t = 1** (5 copied observations, 32 atoms) and **t = 2** (16 copied
observations, 65,536 atoms), from the construction, exactly.

| | t = 1 | t = 2 |
|---|---|---|
| h | 1/16 | 1/64 |
| copied observations (3t^2+2t) | 5 | 16 |
| global atoms | 32 | 65,536 |
| positive atoms | 32 | 12,672 |
| minimum atom | 15/1024 | 0 |
| minimum positive atom | 15/1024 | 3713/268435456 |
| symmetry generators checked | 0 (t = 1 has none) | 4 |
| diagonal cells checked | 32 | 1024 |
| AI sets (masks) | 32 | 5,488 |
| AI family prescriptions checked | 51 | 18,054 |
| injectable-set characters | 31 | 316 |

Normalization, nonnegativity, symmetry under one adjacent transposition per
source, the full diagonal law against P_h^(x)t on every cell, every injectable
marginal and every ancestrally-disjoint product prescription: **all pass**.

Target atom bound: min P_h = (1-h)/64 exactly, i.e. 15/1024 at t = 1 and 63/4096
at t = 2. **Pass.**

Bilocal violation, computed from the target table rather than from the formula:
f_{xz} = (1+h)/2 for x = z and 0 otherwise, so I = J = (1+h)/4. Since I = J,
(sqrt I + sqrt J)^2 = 4I, and the verifier checks the exact rational identity
4I = 1+h (17/16 at t = 1, 65/64 at t = 2) together with the squared strict
inequality 4IJ > (1-I-J)^2 (289/1024 > 225/1024 at t = 1; 4225/16384 > 3969/16384
at t = 2). So sqrt I + sqrt J = sqrt(1+h) > 1. **Pass.**

Negative control: one unit of mass (1/denominator) moved from the all-zero atom to
the all-one atom. Both atoms are fixed by every copy permutation, so normalization
and every symmetry survive; the diagonal law then rejects 2 cells at each order.
**Pass (rejects, as required).**

## 2. Cycle witnesses (B4 3-6, B5 4)

Density H_{N,q}(s) = 2^(-N) sum over even S of (-q)^(|S|/2) prod_S s, on N = mt
signs, q = 1/(4 m^2 t^2); outputs O_v^{ij} = s_{v-1,i} s_{v,j}; target Fourier
moments Phat(F) = (-q)^(|boundary F|/2).

Built at m = 3, 4, 5 for t = 1 and t = 2. The 20-bit table (m = 5, t = 2) was
affordable and is included.

| m, t | q | copied obs. | positive atoms | minimum positive atom | diagonal cells | AI sets | AI family prescriptions |
|---|---|---|---|---|---|---|---|
| 3, 1 | 1/36 | 3 | 4 | 11/48 | 8 | 8 | 8 |
| 4, 1 | 1/64 | 4 | 8 | 3713/32768 | 16 | 16 | 18 |
| 5, 1 | 1/100 | 5 | 16 | 1801/32000 | 32 | 32 | 42 |
| 3, 2 | 1/144 | 12 | 32 | 2677103/95551488 | 64 | 243 | 243 |
| 4, 2 | 1/256 | 16 | 128 | 3829785601/549755813888 | 256 | 1,881 | 2,425 |
| 5, 2 | 1/400 | 20 | 512 | 9101406417999/5242880000000000 | 1024 | 14,231 | 26,671 |

The minimum atom of the table itself is 0 at every order (the witness is supported
on the 2^(mt) images of the auxiliary sign cube); the column above is the minimum
over the support. Normalization, nonnegativity, symmetry, the full diagonal law
with moments (-q)^(|boundary F|/2), and every AI prescription: **all pass**. At
n <= 16 the closed-form character function was additionally checked against the
Walsh-Hadamard transform of the stored table on all 2^n characters, with no
mismatch.

Target incompatibility certificate. The cycle is cut into three contiguous arcs
(m = 3: {0},{1},{2}; m = 4: {0},{1},{2,3}; m = 5: {0},{1,2},{3,4}). Each arc
product has mean exactly -q, and E[V1 V2 V3] = 1, so V1 V2 V3 = 1 almost surely.
The product of the three means is -q^3:

| m, t | arc means | product of means |
|---|---|---|
| 3, 1 | -1/36 each | -1/46656 |
| 4, 1 | -1/64 each | -1/262144 |
| 5, 1 | -1/100 each | -1/1000000 |
| 3, 2 | -1/144 each | -1/2985984 |
| 4, 2 | -1/256 each | -1/16777216 |
| 5, 2 | -1/400 each | -1/64000000 |

Exact triangle parity rigidity requires the product of the three means of a
parity-perfect compatible triangle law to be nonnegative (means (st, su, tu) have
product (stu)^2 >= 0). Here it is strictly negative. **Pass.**

Negative control as in section 1, at every (m, t): **rejects**.

## 3. Corrected square density (B6 1-2, target from B6 1, inequality from B6 3)

Four families of t signs, f_g = prod_i (1 + i sqrt(q) s_{g,i}),
W = Re prod_{g=1}^{4} f_g + 5 sum_g (1 - Re f_g), q = 1/(16t);
outputs A^{il} = x_i w_l, B^{ij} = x_i y_j, C^{jk} = y_j z_k, D^{kl} = z_k w_l;
target P_q, the B6 section 1 sign table.

### The expansion

W is a real polynomial in q. Writing the coefficient of prod_{v in S} s_v as c_S:

* c_S = 1 for S empty;
* c_S = 0 for |S| odd;
* c_S = -4 (-q)^(|S|/2) for S nonempty, even, inside a single family;
* c_S = (-q)^(|S|/2) for S even and meeting at least two families.

Derivation. Re prod_g f_g keeps only even powers of i sqrt(q), and
(i sqrt q)^|S| = (-q)^(|S|/2) for |S| even, giving (-q)^(|S|/2) on every even S.
Re f_g gives (-q)^(|S|/2) on even S inside family g and nothing else. Hence the
empty coefficient is 1 + 5*4 - 5*4 = 1, within-family even coefficients are
(1 - 5)(-q)^(|S|/2), and coefficients meeting two or more families are untouched.
The builder derives it this way and evaluates W by summing the expansion over all
subsets; the verifier evaluates W by an exact complex computation in the ring
Q[J]/(J^2 + q) with J = i sqrt(q), i.e. exact Gaussian rationals. The two routes
were compared on **every** character of the density at t = 1, 2, 3 (16, 256 and
4,096 characters): **0 mismatches**.

### Positivity and normalization

W depends only on the per-family minus-counts, immediately from
f_g = (1 + i sqrt q)^(t-a) (1 - i sqrt q)^a. The scan therefore runs over count
tuples with an explicit multiplicity audit that accounts for every one of the
2^(4t) assignments, and the mean of W over the sign cube is checked to be exactly 1.

| t | q | assignments | min W | >= 1/3 |
|---|---|---|---|---|
| 1 | 1/16 | 16 | 161/256 = 0.6289 | yes |
| 2 | 1/32 | 256 | 530561/1048576 = 0.5060 | yes |
| 3 | 1/48 | 4,096 | 6531524257/12230590464 = 0.5340 | yes |
| 4 | 1/64 | 65,536 | 141348562911745/281474976710656 = 0.5022 | yes |
| 5 | 1/80 | 1,048,576 | 5569468986191750561/10737418240000000000 = 0.5187 | yes |

**Pass**: W > 0 everywhere, minimum >= 1/3 at every order checked.

### Old uncorrected density

With the within-family coefficient left at 1 (that is, the plain Re prod f_g) the
density is negative at the all-plus assignment while the corrected one is positive:

| t | q | uncorrected W(all +) | corrected W(all +) |
|---|---|---|---|
| 3 | 1/48 | -2059855199/12230590464 = -0.1684 | 13228382881/12230590464 = 1.0816 |
| 4 | 1/64 | -129605850521087/281474976710656 = -0.4605 | 396785341276673/281474976710656 = 1.4097 |

**Pass.** This confirms that the corrected witness is not a reparametrization of
the old one.

### Full observed tables

| | t = 1 | t = 2 |
|---|---|---|
| copied observations (4t^2) | 4 | 16 |
| positive atoms | 8 | 128 |
| minimum positive atom | 161/2048 | 530561/134217728 |
| symmetry generators | 0 | 4 |
| diagonal cells | 16 | 256 |
| AI sets (masks) | 16 | **1,881** |
| AI family prescriptions | 18 | 2,425 |

The 1,881 count at t = 2 was obtained here by independent brute force and agrees
with the packet. Symmetry, the full diagonal law against P_q^(x)t, and all AI
prescriptions: **pass**.

### Flipped tables

Independent flips with eta = q/64 applied to every copied observation, exactly;
the target becomes T_eta^(x)4 P_q.

| | t = 1 (eta = 1/1024) | t = 2 (eta = 1/2048) |
|---|---|---|
| positive atoms | 16 of 16 | 65,536 of 65,536 |
| full support | yes | yes |
| symmetry, diagonal law, all AI prescriptions | pass | pass |

Exact incompatibility certificate for the flipped target, evaluating the certified
square inequality max{EA, EB, E[AB]} + 4 P(ABCD = -1) >= 0 (B6 section 3):

| t | EA = EB | E[AB] | P(ABCD = -1) | value |
|---|---|---|---|---|
| 1 | -511/8192 | -261121/4194304 | 535300095/137438953472 | **-1603803137/34359738368** |
| 2 | -1023/32768 | -1046529/33554432 | 4288679935/2199023255552 | **-12857651201/549755813888** |

The t = 2 value **reproduces the packet's reported -12857651201/549755813888
exactly**.

### P_q is a probability law iff q <= 3 - 2 sqrt 2

The only atom that can go negative is P(0000) = (1 - 6q + q^2)/8, and for
0 <= q <= 1 the condition 1 - 6q + q^2 >= 0 is equivalent to (3-q)^2 >= 8, i.e.
q <= 3 - 2 sqrt 2. Both forms were evaluated exactly on ten rationals and their
verdicts agree in every case, including the tight bracket

* q = 343/2000 = 0.1715: 1 - 6q + q^2 = 1649/4000000 > 0, **is** a probability law;
* q = 429/2500 = 0.1716: 1 - 6q + q^2 = -959/6250000 < 0, **is not**.

3 - 2 sqrt 2 = 0.17157... lies between them. **Pass.**

## 4. Triangle analogue (AUDIT-NOTES B2(ii)), the new result

Not in the packet. Three families of t signs x, y, z;
W = Re(f_x f_y f_z) + 4 sum_g (1 - Re f_g), q = 1/(16t);
outputs A^{ij} = x_i z_j, B^{ik} = x_i y_k, C^{jk} = z_j y_k;
target Pi(-q,-q,-q), i.e. (1 + x a + y b + z c)/4 on the parity face abc = 1 and 0
elsewhere. The expansion coefficients are as in section 3 with the within-family
factor -3 instead of -4.

The verifier checks that the target really has E[A] = E[B] = E[C] = -q and
E[ABC] = 1 before using it.

### Positivity

| t | q | assignments | min W | >= 3/5 |
|---|---|---|---|---|
| 1 | 1/16 | 8 | 13/16 = 0.8125 | yes |
| 2 | 1/32 | 64 | 23649/32768 = 0.7217 | yes |
| 3 | 1/48 | **512** | 440789/589824 = 0.7473 | yes |
| 4 | 1/64 | 4,096 | 49447760257/68719476736 = 0.7196 | yes |
| 5 | 1/80 | 32,768 | 15416296709037/20971520000000 = 0.7351 | yes |
| 6 | 1/96 | 262,144 | 497816206205719393/692533995824480256 = 0.7188 | yes |

The t = 3 row is the exhaustive enumeration of the 2^9 = 512 sign assignments
asked for. The mean of W over the sign cube is exactly 1 at every order. **Pass.**

For the record, the *uncorrected* triangle density at the all-plus assignment is
**not** negative at t = 3 (59755/196608 = 0.3039) or t = 4
(5917040513/68719476736 = 0.0861); the sign change that occurs for the square at
t = 3 does not occur for the triangle in that range. This is reported, not claimed
as a failure: the correction is still what keeps the density bounded away from 0,
and the negativity statement in the packet is about the square.

### Full tables and characters

| | t = 1 | t = 2 | t = 3 |
|---|---|---|---|
| copied observations (3t^2) | 3 | 12 | 27 |
| method | full table (8 atoms) | full table (4,096 atoms) | exact Fourier characters, no stored table |
| positive atoms | 4 | 32 | not applicable |
| symmetry generators | 0 | 3 | not applicable |
| diagonal cells / characters | 8 cells | 64 cells | 512 characters |
| AI sets (masks) | 8 | 243 | 2^27 masks not enumerable |
| AI family prescriptions | 8 | 243 | **15,850** |
| injectable sets | 7 | 44 | 135 |

At t = 1, 2 the closed-form character function was checked against the
Walsh-Hadamard transform of the stored table on all 2^n characters (0 mismatches),
so the t = 3 character route is validated against explicit tables at the orders
where both are available. At t = 3 every diagonal character (all 512) and every
one of the 15,850 AI family prescriptions was verified exactly.

**All pass at t = 1, 2, 3.**

### Flipped version

eta = q/192 on every copied observation.

| t | eta | full support | symmetry | diagonal | AI |
|---|---|---|---|---|---|
| 1 | 1/3072 | yes (8 of 8) | pass | pass | pass (8) |
| 2 | 1/6144 | yes (4,096 of 4,096) | pass | pass | pass (243) |
| 3 | 1/9216 | not evaluated (2^27 atoms) | not applicable | pass (512 characters) | pass (15,850) |

Full support at t = 3 is not evaluated. It follows from the bound that every atom
of a table flipped independently with probability eta in (0, 1/2) is at least
eta^n, but that is an argument, not a finite check, and is recorded as such.

### Incompatibility

Unflipped target: the three means are exactly -q, E[ABC] = 1, and the product of
the means is -q^3:

| t | means | product of means |
|---|---|---|
| 1 | -1/16 each | -1/4096 |
| 2 | -1/32 each | -1/32768 |
| 3 | -1/48 each | -1/110592 |

Parity-rigidity obstruction: a parity-perfect compatible triangle law has means
(st, su, tu) for signs s, t, u absorbed from the three sources, whose product is
(stu)^2 >= 0. The target's product is strictly negative. That is the certified
obstruction for the unflipped target.

Flipped target. The inequality evaluated here is **B4 section 6 equation (20)**:
for two adjacent observations A, B of a pair-source scenario and a selected
collection V whose other members do not depend on any source shared by A and B,
every compatible law satisfies

    max{EA, EB, E[AB]} + 8 P(prod_{v in V} O_v = -1) >= 0.

The triangle with V = {A, B, C} satisfies the hypothesis: A and B share source x,
and C carries only z and y. This is the certified inequality. The constant-4
version is the *square* inequality B6 (7) and is **not** claimed for the triangle;
both values are reported, the 8-version being the one that certifies.

| t | EA = EB = EC | E[AB] | E[ABC] | P(ABC = -1) | max + 8P (certified) | max + 4P (reported only) |
|---|---|---|---|---|---|---|
| 1 | -1535/24576 | -2356225/37748736 | 3616805375/3623878656 | 7073281/7247757312 | **-49476119/905969664** | -106025519/1811939328 |
| 2 | -3071/98304 | -9431041/301989888 | 28962726911/28991029248 | 28302337/57982058496 | **-198042647/7247757312** | -424387631/14495514624 |
| 3 | -4607/221184 | -21224449/1019215872 | 97781036543/97844723712 | 63687169/195689447424 | **-445699607/24461180928** | -955086383/48922361856 |

All three certified values are strictly negative, so the flipped targets violate a
compatible-set inequality. The product of the flipped means is also strictly
negative at every order (-3616805375/14843406974976, -28962726911/949978046398464,
-97781036543/10820843684757504 at t = 1, 2, 3), and the parity error is the
P(ABC = -1) column.

**Conclusion for item 4: every listed check passes at the orders checked**
(positivity t = 1..6; full tables t = 1, 2; exact characters t = 3; flipped
versions t = 1, 2 with full support and t = 3 by characters). The witness
therefore places Pi(-q,-q,-q) with q = 1/(16t) inside AI_t at t = 1, 2, 3, and the
corresponding incompatibility certificates are exact and negative. This is a
finite-order verification of AUDIT-NOTES B2(ii). It is **not** a proof of the
all-order statement, which rests on the analytic argument in the audit notes (the
c = 4, m = 3 positivity bound W >= 3/5 and the boundary argument for AI
characters).

## 5. Low-order square certificates (B6 5)

### The parity-forcing reduction (lemma, with proof sketch)

Used by the count-moment certificates in 5(b) and 5(c). It is stated here as an
explicit assumption of those certificates.

**Lemma.** Let P_q be the square parity family, so ABCD = 1 almost surely, and let
Gamma be any NW_t witness for P_q. Then

1. Gamma is supported on arrays with A^{il} B^{ij} C^{jk} D^{kl} = 1 for every
   (i, j, k, l).
2. Every such array has the potential representation A^{il} = x_i w_l,
   B^{ij} = x_i y_j, C^{jk} = y_j z_k, D^{kl} = z_k w_l with signs
   x, y, z, w in {+-1}^t, unique up to flipping all four potential vectors at once.
3. Consequently Gamma corresponds to a distribution on {+-1}^(4t) invariant under
   the global flip, and averaging over the source-copy permutations (which Gamma
   already admits) reduces it to a distribution w_a on the minus-sign counts
   a in {0,...,t}^4, whose observable characters are
   sum_a w_a prod_g K_{k_g}^(t)(a_g) with
   K_k^(t)(a) = [sum_j (-1)^j C(a,j) C(t-a, k-j)] / C(t,k).

*Proof sketch.* (1) For any (i, j, k, l) there are permutations of the four
sources' copy indices sending i, j, k, l to 1, and they carry
(A^{il}, B^{ij}, C^{jk}, D^{kl}) to the first diagonal row, whose law is P_q by the
NW diagonal prescription. Parity is therefore perfect on every copied 4-cycle.
(2) Fixing j = k = 1 in the constraint gives a_{il} = b_{i1} c_{11} d_{1l}, so A is
a rank-one sign matrix; dividing the general constraint by the j = k = 1 one shows
b_{ij}/b_{i1} depends only on j, hence b_{ij} = b_{i1} b_{1j} b_{11}, and likewise
for c and d; the compatibility b_{1j} c_{j1} = a_{11} d_{11} (the constraint at
i = k = l = 1) is exactly what lets the same y serve in b and c. The gauge group is
s_x s_y = s_y s_z = s_z s_w = s_w s_x = 1, i.e. the global flip only.
(3) Immediate from (2): a character of the observations is a product of potential
signs whose total size is even (boundaries of observation sets are even), hence
gauge-invariant, and permutation averaging replaces a specified k_g-subset of
family g by the uniform one, giving the Krawtchouk ratio. QED

The AI_t (resp. NW_t) prescriptions then become linear equations
sum_a w_a prod_g K_{k_g}(a_g) = (-q)^(S/2), S = sum_g k_g, over the degree tuples
that actually arise. The verifier does **not** take B6's characterisation on trust:
it computes the AI degree set by brute force from the family enumeration and checks
it equals {k : S even, 2 max_g k_g <= S, k_g <= t}, and it computes the NW degree
set from the diagonal-row boundaries.

| t | NW degree tuples | AI degree tuples | AI minus NW |
|---|---|---|---|
| 2 | **33** | **37** | (0,2,2,2) and its 3 rotations |
| 3 | 96 | 112 | 16 tuples |

The 33 and 37 agree with B6 ("all 37 AI and 33 NW moment equations").

### (a) NW_2 feasibility, q = 3/20 and q = 1/10

Discovered with `scipy.optimize.linprog` on the symmetry-reduced count LP, then the
support of the returned vertex was taken and the exact rational solution obtained
by Gaussian elimination over `Fraction`, symmetrized over the gauge complement
a -> t - a. The stored certificate is the exact count-weight vector.

The verifier re-reads the weights, checks w_a >= 0 and sum w_a = 1, checks all 34
moment equations exactly, then **expands the weights to the full 16-bit table** and
runs the full NW checks on it.

| q | nonzero count tuples | positive atoms of the 16-bit table | minimum positive atom | diagonal cells |
|---|---|---|---|---|
| 3/20 | 66 | **82** | 2401/10240000 | 256 |
| 1/10 | 66 | **82** | 1681/640000 | 256 |

Symmetry, normalization, nonnegativity and the full diagonal law P_q^(x)2:
**pass** at both q. So P_{3/20}, P_{1/10} are in NW_2, confirming B6 (12) at these
two points.

B6 reports an NW_2 witness with **88** positive atoms. Mine has **82**. Both are
vertices of the same feasible polytope (there are 2^8/2 = 128 candidate arrays);
the packet's witness was not in the returned files, so this is a difference of
certificate, not a contradiction. Recorded as a discrepancy.

Both NW_2 witnesses fail 64 of the 2,425 AI_2 family prescriptions (the first is
reported in the JSON). At q = 3/20 that is consistent with AI_2 infeasibility; at
q = 1/10 it merely says this particular NW_2 vertex is not an AI_2 witness, and a
separate AI_2 witness is given below. It is **not** used as evidence of anything.

### (b) AI_2 at q = 1/10 (feasible) and q = 3/20 (infeasible)

**q = 1/10, feasible.** Exact count-weight witness with 74 nonzero count tuples,
expanding to a 16-bit table with **106 positive atoms**, minimum positive atom
451/320000. It passes normalization, nonnegativity, all 4 symmetry generators, all
256 diagonal cells, all 1,881 AI sets and all 2,425 AI family prescriptions.
**Pass.** So P_{1/10} is in AI_2, confirming B6 (13) at this point.

**q = 3/20, infeasible.** Three independent certificates.

1. *B6 equation (16), independently evaluated.* With Kbar_k(a) the average of
   prod_g K_{k_g}^(2)(a_g) over the distinct permutations of k,
   D(a) = -3 - 24 Kbar_0011 - 6 Kbar_0022 + 8 Kbar_0222 + 24 Kbar_1122 + Kbar_2222.
   On all **81** count configurations D(a) <= 0 with maximum exactly 0. The nine
   permutation-and-complement orbits take the values **-32** on the orbit of 0001,
   **-16** at 1111, and **0** on the other seven. This reproduces B6's description
   exactly. The prescribed expectation is E[D] = -3 + 24q - 6q^2 - 32q^3 + q^4, and
   the polynomial identity E[D] = (1+q)(q^3 - 33q^2 + 27q - 3) is verified
   coefficient by coefficient in the verifier (stdlib, exact) and symbolically with
   sympy in the builder. At q = 3/20, E[D] = **57201/160000 > 0**, reproducing B6's
   number exactly. At q = 1/10, E[D] = -6919/10000 < 0, consistent with feasibility
   there.
2. *An independently discovered count-form dual.* LP-discovered, rationalized to
   denominator 1080, verified exactly: maximum value 0 over the 81 configurations,
   prescribed expectation 19067/1280000 > 0. Every degree tuple carrying a nonzero
   coefficient is checked to be AI_2-prescribed.
3. *A direct certificate on the full 16-bit table*, with no count reduction and
   hence no dependence on the lemma. lambda is supported on the 1,881 AI sets,
   constant on the 142 orbits of the copy-permutation group, with denominator 392.
   The verifier expands lambda over the orbits, computes
   F(omega) = sum_U lambda_U chi_U(omega) by a Walsh-Hadamard transform over **all
   65,536 assignments**, and finds max F = **0**, so F <= 0 pointwise, while the
   prescribed expectation sum_U lambda_U b_U = **57201/490000 > 0**. The LP was set
   up over the 5,488 assignment orbits, which is legitimate because the AI
   constraint set is invariant under the group; the verification is pointwise on all
   65,536 atoms. Note 57201/490000 = (16/49) * (57201/160000): the full-table
   certificate is a rescaling of B6's D, a strong cross-check between the two routes.

Hence **P_{3/20} is in NW_2 minus AI_2, and P_{1/10} is in AI_2**: B6's separation
at q = 3/20 is reproduced.

### (c) NW_3 infeasibility at q = 1/10

The full table has 2^36 variables, so the count-moment reduction is used; this
certificate **depends on the lemma above**. Variables w_a, a in {0,1,2,3}^4, i.e.
4^4 = **256** configurations; 96 NW_3 degree tuples plus normalization.

Dual discovered by LP over permutation-symmetrized coefficients, rationalized to
denominator 540, verified exactly: the functional is <= 0 on **all 256**
configurations with maximum exactly 0, every degree tuple used is NW_3-prescribed,
and the prescribed expectation is

    634237/540000000 = 1.17451e-3 > 0.

So P_{1/10} is not in NW_3, confirming B6 (17)'s conclusion.

**Discrepancy with the packet's number.** B6 reports 164197/150000000 = 1.09465e-3.
A Farkas certificate is defined only up to a positive scaling, and the LP optimum
depends on the normalization imposed on the dual vector (here sup-norm <= 1 on the
symmetrized coefficients), so a specific rational value is not an invariant of the
statement. The packet's dual coefficients were not in the returned files
(AUDIT-NOTES B5 records exactly this), so **B6's constant 164197/150000000 was not
reproduced and is not confirmed**. What is confirmed is the infeasibility itself,
with the exact certificate recorded here.

### (d) Threshold and identity

* P_q is a probability law iff q <= 3 - 2 sqrt 2: see section 3, ten exact cases
  with a separating bracket at 343/2000 and 429/2500. **Pass.**
* Root bracket for g(q) = q^3 - 33q^2 + 27q - 3:
  g(1324743/10000000) = -575495517199593/10^21 < 0 and
  g(1324744/10000000) = 2452028532857/1953125000000000000 > 0, so g has a root in
  the interval, matching B6's r = 0.13247433. **Pass.**
* E[D] = (1+q)(q^3 - 33q^2 + 27q - 3): verified symbolically (sympy, builder) and
  coefficient by coefficient with fractions (verifier), plus exact spot values at
  q = 3/20 and q = 1/10. **Pass.**

## Summary of status

| certificate | orders checked | status |
|---|---|---|
| `five_path` | t = 1, 2 | pass, including the exact bilocal violation and the negative control |
| `cycles` | m = 3, 4, 5 at t = 1; m = 3, 4, 5 at t = 2 | pass, including the 20-bit m = 5, t = 2 table |
| `square` | density t = 1..5; tables and flipped tables t = 1, 2; uncorrected comparison t = 3, 4 | pass; the packet's -12857651201/549755813888 reproduced exactly |
| `triangle` | density t = 1..6; tables t = 1, 2; characters t = 3; flipped t = 1, 2 (tables) and t = 3 (characters) | pass at every order checked |
| `low_order_square` | NW_2 and AI_2 at q = 3/20 and 1/10; NW_3 at q = 1/10 | pass; NW_2 atom count 82 not 88, and the NW_3 dual constant not reproduced (see above) |

## What these certificates do not establish

* They are finite-order checks. The all-order theorems (uniform nontermination, the
  Omega(1/t) square rate, the Omega(1/t) triangle rate) rest on the analytic
  arguments in AUDIT-NOTES, not on these programs.
* The distance lower bounds (q/6, q/12, 5q/48, 13q/192, and the corrected five-path
  constant h/96) are not evaluated here. What is evaluated is the exact value of the
  certifying inequality on the exact target, which is the finite part of those
  arguments.
* exp_t = AI_t is quoted from the root-sink lemma (AUDIT-NOTES A2); nothing here
  checks the recursive expressible closure directly.
* The triangle result (section 4) is new and is reported as verified **at
  t = 1, 2, 3 only**.
