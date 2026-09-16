#!/usr/bin/env python3
"""Exact verifier for the explicit rejecting orders of Section 6.3 of the paper
(Propositions 6.3, 6.4, 6.6, Corollary 6.5, Remark 6.7).  "NOTE.md" below refers to
the audit note of 2026-09-16, which is not distributed; the paper states the results.

Run from the repository root:
  python3 -B artifact/certificates/beyond-finner/verify_beyond_finner.py

Standard library only (fractions, itertools, random with a fixed seed); no
floating point in any check.  Refuses to run under -O and exits with status 1
on the first failed check.

What is checked exactly
  [A] the algebraic identities behind the barycentre step:
        A1  the exact second-order remainder of a product of three linear forms;
        A2  E P_hat = P and E (L(P_hat) - L(P))^2 = (1 - L(P)^2)/n for every
            character L, by full enumeration of P^{(x)n} at small n;
        A3  Var_P(chi) <= 2 (1 - ||P||_2^2) for every sign function chi.
  [B] falsification tests of the two certificates on compatible laws (exact
      laws of random finite deterministic models; a sampled test, not a proof):
        triangle  E A E B E C + 10 P(ABC = -1) >= 0  (and its odd relabelling),
        square    E A E B E[AB] + 8 P(ABCD = -1) >= 0 (and 8 P(ABCD = +1)).
  [C] sampled exact checks of the two elementary propositions of NOTE.md
      section 5: an atomic Finner violation forces F_+ >= 0 and F_- >= 0, and
      no fan inequality fails at any order for a law satisfying all eight
      atomic Finner inequalities.
  [D] the worked examples: validity, all eight atomic Finner inequalities,
      the functional Finner inequality E f(A)g(B)h(C) <= ||f|| ||g|| ||h||
      for all nonnegative f, g, h (exact polynomial certificate), no fan
      inequality of Theorem thm:fan failing at any order, the sign of the new
      certificate, and the stated rejecting-order bounds of every route.

Usage:  python3 verify_beyond_finner.py
"""

import itertools
import random
import sys
from fractions import Fraction as Fr
from math import isqrt

if not __debug__:
    sys.stderr.write("verify_beyond_finner.py refuses to run with -O\n")
    raise SystemExit(2)

CHECKS = 0


class VerifyError(Exception):
    pass


def need(ok, msg):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise VerifyError(msg)


# ---------------------------------------------------------------- basics ----

BITS3 = list(itertools.product((0, 1), repeat=3))
BITS4 = list(itertools.product((0, 1), repeat=4))


def sg(bit):
    return 1 - 2 * bit  # bit 0 <-> +1, as in the paper


def tri_stats(P):
    """Means of A, B, C and eps = P(ABC = -1) for a law on three bits."""
    l = [sum(P[x] * sg(x[i]) for x in BITS3) for i in range(3)]
    eps = sum(P[x] for x in BITS3 if sg(x[0]) * sg(x[1]) * sg(x[2]) == -1)
    return l, eps


def sq_stats(P):
    """Means of A, B, AB and eps = P(ABCD = -1) for a law on four bits."""
    l = [sum(P[x] * sg(x[0]) for x in BITS4),
         sum(P[x] * sg(x[1]) for x in BITS4),
         sum(P[x] * sg(x[0]) * sg(x[1]) for x in BITS4)]
    eps = sum(P[x] for x in BITS4 if sg(x[0]) * sg(x[1]) * sg(x[2]) * sg(x[3]) == -1)
    return l, eps


C_TRI = Fr(10)
C_SQ = Fr(8)


def F_tri(P):
    l, eps = tri_stats(P)
    p = l[0] * l[1] * l[2]
    return p + C_TRI * eps, -p + C_TRI * (1 - eps)


def F_sq(P):
    l, eps = sq_stats(P)
    p = l[0] * l[1] * l[2]
    return p + C_SQ * eps, p + C_SQ * (1 - eps)


def norm2sq(P):
    return sum(v * v for v in P.values())


def is_law(P, bits):
    return all(P[x] >= 0 for x in bits) and sum(P[x] for x in bits) == 1


def marg(P, i, v):
    return sum(P[x] for x in P if x[i] == v)


def sqrt_upper(q, digits=12):
    """A rational upper bound for sqrt(q), q >= 0 rational."""
    q = Fr(q)
    scale = 10 ** digits
    n = q.numerator * q.denominator * scale * scale
    r = isqrt(n)
    if r * r < n:
        r += 1
    return Fr(r, q.denominator * scale)


def floor_fr(q):
    return q.numerator // q.denominator


# ------------------------------------------------------ [A] identities ----

def check_A(rng):
    # A1: for linear forms L1, L2, L3 and probability vectors P, Q,
    # L1L2L3(Q) - L1L2L3(P) - D(L1L2L3)(P)[Q-P] = h1 h2 L3(Q) + l2 h1 h3 + l1 h2 h3.
    for bits, chars in ((BITS3, [lambda x: sg(x[0]), lambda x: sg(x[1]), lambda x: sg(x[2])]),
                        (BITS4, [lambda x: sg(x[0]), lambda x: sg(x[1]),
                                 lambda x: sg(x[0]) * sg(x[1])])):
        for _ in range(200):
            P = rand_law(rng, bits)
            Q = rand_law(rng, bits)
            L = lambda M, i: sum(M[x] * chars[i](x) for x in bits)
            l = [L(P, i) for i in range(3)]
            q = [L(Q, i) for i in range(3)]
            h = [q[i] - l[i] for i in range(3)]
            lhs = q[0] * q[1] * q[2] - l[0] * l[1] * l[2] - (
                h[0] * l[1] * l[2] + l[0] * h[1] * l[2] + l[0] * l[1] * h[2])
            rhs = h[0] * h[1] * q[2] + l[1] * h[0] * h[2] + l[0] * h[1] * h[2]
            need(lhs == rhs, "A1 remainder identity failed")
            need(abs(q[2]) <= 1 and abs(l[0]) <= 1 and abs(l[1]) <= 1, "A1 range")
            need(abs(rhs) <= h[0] ** 2 + h[1] ** 2 + h[2] ** 2, "A1 |R| <= sum h_i^2")

    # A2: empirical law of n i.i.d. draws, full enumeration.
    for bits, n in ((BITS3, 1), (BITS3, 2), (BITS3, 3), (BITS4, 2)):
        P = rand_law(rng, bits)
        ind = len(bits[0])
        chars = [lambda x: sg(x[0]), lambda x: sg(x[1]), lambda x: sg(x[0]) * sg(x[1])]
        if ind == 3:
            chars.append(lambda x: sg(x[2]))
            chars.append(lambda x: sg(x[0]) * sg(x[1]) * sg(x[2]))
        else:
            chars.append(lambda x: sg(x[0]) * sg(x[1]) * sg(x[2]) * sg(x[3]))
        mean = {x: Fr(0) for x in bits}
        sec = [Fr(0)] * len(chars)
        lP = [sum(P[x] * c(x) for x in bits) for c in chars]
        for seq in itertools.product(bits, repeat=n):
            w = Fr(1)
            for x in seq:
                w *= P[x]
            for x in seq:
                mean[x] += w / n
            for k, c in enumerate(chars):
                emp = sum(Fr(c(x)) for x in seq) / n
                sec[k] += w * (emp - lP[k]) ** 2
        need(all(mean[x] == P[x] for x in bits), "A2 E P_hat != P")
        for k in range(len(chars)):
            need(sec[k] == (1 - lP[k] ** 2) / n, "A2 variance identity failed")

    # A3: Var_P(chi) <= 2 (1 - ||P||^2) for every sign function chi (all 2^8 on BITS3).
    for _ in range(40):
        P = rand_law(rng, BITS3)
        r = 1 - norm2sq(P)
        for signs in itertools.product((1, -1), repeat=8):
            m = sum(P[x] * s for x, s in zip(BITS3, signs))
            need(1 - m * m <= 2 * r, "A3 Var <= 2(1-||P||^2) failed")


def rand_law(rng, bits, den=60, sparse=False):
    w = [rng.randint(0, den) if not sparse or rng.random() < 0.6 else 0 for _ in bits]
    if sum(w) == 0:
        w[0] = 1
    s = sum(w)
    return {x: Fr(v, s) for x, v in zip(bits, w)}


# --------------------------------------- [B] certificates on compatible ----

def rand_dist(rng, k):
    w = [rng.randint(1, 9) for _ in range(k)]
    s = sum(w)
    return [Fr(v, s) for v in w]


def rand_table(rng, k1, k2, bias):
    return [[0 if rng.random() < bias else 1 for _ in range(k2)] for _ in range(k1)]


def triangle_model_law(rng):
    kx, ky, kz = (rng.randint(1, 3) for _ in range(3))
    mx, my, mz = rand_dist(rng, kx), rand_dist(rng, ky), rand_dist(rng, kz)
    bias = [rng.random() for _ in range(3)]
    A = rand_table(rng, kx, kz, bias[0])  # A(X,Z)
    B = rand_table(rng, kx, ky, bias[1])  # B(X,Y)
    C = rand_table(rng, kz, ky, bias[2])  # C(Z,Y)
    P = {x: Fr(0) for x in BITS3}
    for i in range(kx):
        for j in range(ky):
            for k in range(kz):
                P[(A[i][k], B[i][j], C[k][j])] += mx[i] * my[j] * mz[k]
    return P


def square_model_law(rng):
    kx, ky, kz, kw = (rng.randint(1, 3) for _ in range(4))
    mx, my, mz, mw = (rand_dist(rng, k) for k in (kx, ky, kz, kw))
    bias = [rng.random() for _ in range(4)]
    A = rand_table(rng, kx, kw, bias[0])  # A(X,W)
    B = rand_table(rng, kx, ky, bias[1])  # B(X,Y)
    C = rand_table(rng, ky, kz, bias[2])  # C(Y,Z)
    D = rand_table(rng, kz, kw, bias[3])  # D(Z,W)
    P = {x: Fr(0) for x in BITS4}
    for i, j, k, l in itertools.product(range(kx), range(ky), range(kz), range(kw)):
        P[(A[i][l], B[i][j], C[j][k], D[k][l])] += mx[i] * my[j] * mz[k] * mw[l]
    return P


def check_B(rng, trials=3000):
    for _ in range(trials):
        P = triangle_model_law(rng)
        need(is_law(P, BITS3), "B triangle model law invalid")
        fp, fm = F_tri(P)
        need(fp >= 0 and fm >= 0, "B triangle certificate negative on a compatible law")
        P = square_model_law(rng)
        need(is_law(P, BITS4), "B square model law invalid")
        fp, fm = F_sq(P)
        need(fp >= 0 and fm >= 0, "B square certificate negative on a compatible law")


# ------------------------------------------- Finner and fan machinery ----

def atomic_finner_gaps(P):
    """min over the 8 atoms of P_A P_B P_C - P(atom)^2 (>= 0 iff all hold)."""
    return min(marg(P, 0, x[0]) * marg(P, 1, x[1]) * marg(P, 2, x[2]) - P[x] ** 2
               for x in BITS3)


def fan_first_fail(P, tmax_scan=None):
    """Least order t at which some inequality of thm:fan (either one, any atom,
    any root) fails; None if none fails at any order.  Exact."""
    best = None
    for x in BITS3:
        z = P[x]
        m = [marg(P, i, x[i]) for i in range(3)]
        for root in range(3):
            a = m[root]
            b, c = [m[i] for i in range(3) if i != root]
            bc = b * c
            # second inequality: t (z^2 - abc) <= a z - abc, linear in t.
            slope, rhs = z * z - a * bc, a * z - a * bc
            if slope > 0:
                t = floor_fr(rhs / slope) + 1
                t = max(t, 1)
                best = t if best is None else min(best, t)
            else:
                need(1 * slope <= rhs, "fan second inequality fails at t = 1")
            # first inequality: g(t) = bc t^2 - (bc + 2z) t + 2a >= 0.
            if bc == 0:
                if z > 0:
                    t = floor_fr(a / z) + 1
                    best = t if best is None else min(best, t)
                continue
            g = lambda t: bc * t * t - (bc + 2 * z) * t + 2 * a
            v = (bc + 2 * z) / (2 * bc)
            cands = {1, max(1, floor_fr(v)), max(1, floor_fr(v) + 1)}
            if min(g(t) for t in cands) < 0:
                lo, hi = 1, max(cands, key=lambda t: -g(t))
                if g(lo) < 0:
                    t = 1
                else:
                    # g(lo) >= 0 > g(hi), g decreasing on [1, v]: bisect.
                    while hi - lo > 1:
                        mid = (lo + hi) // 2
                        if g(mid) < 0:
                            hi = mid
                        else:
                            lo = mid
                    t = hi
                best = t if best is None else min(best, t)
    return best


def functional_finner_certificate(P):
    """Exact proof that E f(A) g(B) h(C) <= ||f(A)|| ||g(B)|| ||h(C)|| for all
    nonnegative f, g, h, for a law P with all one-variable marginals positive.

    For f = (1, r), r >= 0, the supremum over g, h of the squared ratio is
    lambda_max(R), R = D_B^{-1} N D_C^{-1} N^T, N_bc = P(0bc) + r P(1bc).  The
    inequality is lambda_max(R) <= s := P_A(0) + P_A(1) r^2, i.e.
    p = s^2 - s tr R + det R >= 0 and q = 2 s - tr R >= 0 on [0, infinity),
    including the direction f = (0, 1) (leading coefficients).  p vanishes at
    r = 1 (f constant); we divide by (r - 1)^2 exactly and check the quotient."""
    for i in range(3):
        for v in (0, 1):
            need(marg(P, i, v) > 0, "functional Finner: zero marginal not handled")

    def padd(p, q):
        n = max(len(p), len(q))
        return [(p[k] if k < len(p) else 0) + (q[k] if k < len(q) else 0) for k in range(n)]

    def pmul(p, q):
        out = [Fr(0)] * (len(p) + len(q) - 1)
        for i, x in enumerate(p):
            for j, y in enumerate(q):
                out[i + j] += x * y
        return out

    def pscale(p, c):
        return [c * x for x in p]

    PA0, PA1 = marg(P, 0, 0), marg(P, 0, 1)
    PB = [marg(P, 1, 0), marg(P, 1, 1)]
    PC = [marg(P, 2, 0), marg(P, 2, 1)]
    N = [[[P[(0, b, c)], P[(1, b, c)]] for c in (0, 1)] for b in (0, 1)]
    R = [[None, None], [None, None]]
    for b in (0, 1):
        for b2 in (0, 1):
            acc = [Fr(0)]
            for c in (0, 1):
                acc = padd(acc, pscale(pmul(N[b][c], N[b2][c]), 1 / PC[c]))
            R[b][b2] = pscale(acc, 1 / PB[b])
    s = [PA0, Fr(0), PA1]
    tr = padd(R[0][0], R[1][1])
    det = padd(pmul(R[0][0], R[1][1]), pscale(pmul(R[0][1], R[1][0]), Fr(-1)))
    p = padd(padd(pmul(s, s), pscale(pmul(s, tr), Fr(-1))), det)
    q = padd(pscale(s, Fr(2)), pscale(tr, Fr(-1)))
    p = p + [Fr(0)] * (5 - len(p))
    # synthetic division by (r - 1) twice
    for _ in range(2):
        need(sum(p) == 0, "functional Finner: p(1) != 0")
        quo = [Fr(0)] * (len(p) - 1)
        carry = Fr(0)
        for k in range(len(p) - 1, 0, -1):
            carry = p[k] + carry
            quo[k - 1] = carry
        p = quo
    need(len(p) == 3, "functional Finner: quotient degree")

    def quad_nonneg_halfline(c):
        g0, g1, g2 = (list(c) + [Fr(0)] * 3)[:3]
        return g0 >= 0 and g2 >= 0 and (g1 >= 0 or g1 * g1 <= 4 * g0 * g2)

    need(quad_nonneg_halfline(p), "functional Finner: quartic certificate fails")
    need(quad_nonneg_halfline(q), "functional Finner: trace certificate fails")
    return True


# --------------------------------------------- [C] two propositions ----

def check_C(rng, trials=40000):
    viol = 0
    fin = 0
    for k in range(trials):
        P = rand_law(rng, BITS3, den=rng.choice([6, 20, 200]), sparse=(k % 2 == 0))
        if atomic_finner_gaps(P) < 0:
            viol += 1
            fp, fm = F_tri(P)
            need(fp >= 0 and fm >= 0, "C: Finner violation with negative F_triangle")
        elif k % 20 == 0:
            fin += 1
            need(fan_first_fail(P) is None, "C: fan rejects a Finner-satisfying law")
    need(viol > 1000 and fin > 500, "C: too few samples in a branch")
    # the extremal cases of the proof, on a fine rational grid of parity laws
    # with a small odd admixture concentrated on one atom
    for num in range(0, 21):
        for num2 in range(0, 21 - num):
            m = (Fr(-num, 20), Fr(-num2, 20), Fr(-(20 - num - num2), 20))
            base = parity_law(m)
            for o in BITS3:
                for lam in (Fr(1, 1000), Fr(1, 50), Fr(1, 5)):
                    P = {x: (1 - lam) * base[x] + (lam if x == o else 0) for x in BITS3}
                    if atomic_finner_gaps(P) < 0:
                        fp, fm = F_tri(P)
                        need(fp >= 0 and fm >= 0, "C grid: Finner violation with F < 0")


# ------------------------------------------------------ [D] examples ----

def parity_law(m):
    """Pi(x,y,z) of eq:paritylaw: (1 + x A + y B + z C)/4 on ABC = 1."""
    P = {}
    for x in BITS3:
        s = [sg(v) for v in x]
        P[x] = (1 + m[0] * s[0] + m[1] * s[1] + m[2] * s[2]) / 4 if s[0] * s[1] * s[2] == 1 else Fr(0)
    return P


def mix_uniform(P, lam, bits):
    return {x: (1 - lam) * P[x] + lam / len(bits) for x in bits}


def square_parity_moment_law(m):
    """(1 + m1 A + m2 B + m3 AB)/8 on ABCD = 1, C uniform."""
    P = {}
    for x in BITS4:
        s = [sg(v) for v in x]
        P[x] = (1 + m[0] * s[0] + m[1] * s[1] + m[2] * s[0] * s[1]) / 8 if s[0] * s[1] * s[2] * s[3] == 1 else Fr(0)
    return P


def square_target(q):
    """eq:squaretarget, bit strings ABCD."""
    P = {x: Fr(0) for x in BITS4}
    P[(0, 0, 0, 0)] = (1 - 6 * q + q * q) / 8
    for w in ("0011", "0110", "1001", "1100"):
        P[tuple(int(ch) for ch in w)] = (1 - q * q) / 8
    for w in ("0101", "1010", "1111"):
        P[tuple(int(ch) for ch in w)] = (1 + q) ** 2 / 8
    return P


def tri_routes(P):
    l, eps = tri_stats(P)
    fp, fm = F_tri(P)
    F = min(fp, fm)
    sv = 3 - sum(x * x for x in l)
    r = 1 - norm2sq(P)
    need(sv <= 6 * r, "sum of variances <= 6(1-||P||^2)")
    newF = floor_fr(sv / (-F)) + 1 if F < 0 else None
    newF6 = floor_fr(6 * r / (-F)) + 1 if F < 0 else None
    # relabelled max-moment quantity from lem:quantrigidity
    G = None
    for s in itertools.product((1, -1), repeat=3):
        e = eps if s[0] * s[1] * s[2] == 1 else 1 - eps
        val = max(s[i] * l[i] for i in range(3)) + 8 * e
        G = val if G is None else min(G, val)
    paper = floor_fr(Fr(175) / (G * G)) + 1 if G < 0 else None
    direct = None
    if G < 0:
        root = sqrt_upper(sv) + 8 * sqrt_upper(eps * (1 - eps))
        direct = floor_fr(root * root / (G * G)) + 1
    return dict(l=l, eps=eps, F=F, sv=sv, newF=newF, newF6=newF6, G=G, paper=paper, direct=direct)


def sq_routes(P):
    l, eps = sq_stats(P)
    fp, fm = F_sq(P)
    F = min(fp, fm)
    sv = 3 - sum(x * x for x in l)
    r = 1 - norm2sq(P)
    need(sv <= 6 * r, "square: sum of variances <= 6(1-||P||^2)")
    newF = floor_fr(sv / (-F)) + 1 if F < 0 else None
    G = None
    for sa, sb in itertools.product((1, -1), repeat=2):
        val = max(sa * l[0], sb * l[1], sa * sb * l[2]) + 4 * min(eps, 1 - eps)
        G = val if G is None else min(G, val)
    paper = floor_fr(Fr(135) / (G * G)) + 1 if G < 0 else None
    direct = None
    if G < 0:
        e = min(eps, 1 - eps)
        root = sqrt_upper(sv) + 4 * sqrt_upper(e * (1 - e))
        direct = floor_fr(root * root / (G * G)) + 1
    return dict(l=l, eps=eps, F=F, sv=sv, newF=newF, G=G, paper=paper, direct=direct)


W_LAW = {x: (Fr(1, 3) if sum(x) == 1 else Fr(0)) for x in BITS3}

TRI_EXAMPLES = [
    # name, law, expected (F, new bound, paper route, direct route)
    ("T1 W law", W_LAW, (Fr(-1, 27), 73, 1576, 25)),
    ("T2 Pi(-1/4,-1/4,-1/4)", parity_law((Fr(-1, 4),) * 3), (Fr(-1, 64), 181, 2801, 46)),
    ("T3 Pi(-1/20,-9/20,-9/20)", parity_law((Fr(-1, 20), Fr(-9, 20), Fr(-9, 20))), (Fr(-81, 8000), 257, 70001, 1038)),
    ("T4 999/1000 T3 + uniform/1000",
     mix_uniform(parity_law((Fr(-1, 20), Fr(-9, 20), Fr(-9, 20))), Fr(1, 1000), BITS3), None),
    ("T5 Pi(-1/100,-99/200,-99/200)", parity_law((Fr(-1, 100), Fr(-99, 200), Fr(-99, 200))), None),
]

SQ_EXAMPLES = [
    ("S1 square (1 - A/20 - 9B/20 - 9AB/20)/8 on ABCD=1", square_parity_moment_law((Fr(-1, 20), Fr(-9, 20), Fr(-9, 20)))),
    ("S2 square P_q, q = 1/10", square_target(Fr(1, 10))),
]


def check_D(verbose=True):
    rows = []
    for name, P, expected in TRI_EXAMPLES:
        need(is_law(P, BITS3), f"{name}: not a law")
        need(atomic_finner_gaps(P) >= 0, f"{name}: some atomic Finner inequality fails")
        functional_finner_certificate(P)
        need(fan_first_fail(P) is None, f"{name}: a fan inequality rejects at some order")
        R = tri_routes(P)
        need(R["F"] < 0, f"{name}: F_triangle not negative")
        need(R["newF"] <= R["newF6"], f"{name}: variance form weaker than 6(1-||P||^2) form")
        if expected is not None:
            need((R["F"], R["newF"], R["paper"], R["direct"]) == expected,
                 f"{name}: expected values changed: {(R['F'], R['newF'], R['paper'], R['direct'])}")
        rows.append((name, R))
    # T4 has full support
    need(all(v > 0 for v in TRI_EXAMPLES[3][1].values()), "T4 not of full support")
    # T4, T5: the linear route beats both quadratic routes
    for idx in (2, 3, 4):
        R = rows[idx][1]
        need(R["newF"] < R["direct"] < R["paper"], f"{rows[idx][0]}: route ordering changed")
    # T2: the direct quadratic route beats the linear one
    need(rows[1][1]["direct"] < rows[1][1]["newF"], "T2 route ordering changed")
    for name, P in SQ_EXAMPLES:
        need(is_law(P, BITS4), f"{name}: not a law")
        R = sq_routes(P)
        need(R["F"] < 0, f"{name}: F_square not negative")
        rows.append((name, R))
    need(rows[5][1]["newF"] < rows[5][1]["direct"] < rows[5][1]["paper"], "S1 ordering changed")
    need(rows[6][1]["direct"] < rows[6][1]["newF"], "S2 ordering changed")
    if verbose:
        for name, R in rows:
            print(f"  {name}")
            print(f"     means {[str(x) for x in R['l']]}  eps {R['eps']}  F {R['F']} (~{float(R['F']):.6g})")
            print(f"     t_min^NW <= linear route {R['newF']};  quadratic direct {R['direct']};"
                  f"  quadratic via distance {R['paper']}")
    return rows


def main():
    rng = random.Random(20260916)
    try:
        print("[A] identities");               check_A(rng)
        print("[B] certificates on compatible laws (sampled)"); check_B(rng)
        print("[C] Finner/F disjointness and fan silence (sampled)"); check_C(rng)
        print("[D] examples");                 check_D()
    except VerifyError as exc:
        print(f"FAIL after {CHECKS} checks: {exc}")
        raise SystemExit(1)
    print(f"PASS: {CHECKS} exact checks")


if __name__ == "__main__":
    main()
