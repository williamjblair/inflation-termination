#!/usr/bin/env python3
"""Independent exact verifier for the parity-direction threshold certificates.

Standard library only; no floating point anywhere.  Refuses to run under -O,
because every check is an assertion about exact rational arithmetic.

For each cycle (square, triangle), each order t and each hierarchy H in
{AI, NW} the certificate claims a bracket

        q_lo  <=  q_max^H(t)  <=  q_hi          (or  q_max^H(t) >= q_lo  only),

    q_max^H(t) = sup { q in [0, q_top] : P_{m,q} in I^H_t(C_m) },

where P_{m,q} is the cycle parity family.  This script re-derives the degree
systems from scratch, then checks

  (P)  the rational weights at q_lo are nonnegative, sum to one, and reproduce
       every prescribed Krawtchouk moment of P_{m,q_lo} exactly;
  (D)  the rational dual coefficients give a functional that is nonpositive on
       every one of the (t+1)^m count configurations, whose prescribed
       expectation is the stated polynomial in q, and that this polynomial is
       strictly positive on the whole interval [q_hi, q_top] (Sturm).

What is *assumed*, not re-proved here: the count-moment reduction itself
(Lemma lem:countmoment of sections/15-cycles.tex, extended to the triangle and
to the NW degree system in REPORT.md).  Everything downstream of the reduction
is checked exactly.

Usage:  python3 verify_exponent.py [--dir CERTDIR] [--max-order N]
"""

import argparse
import itertools
import json
import os
import sys
import time
from collections import Counter
from fractions import Fraction as F
from math import comb, factorial, gcd

if not __debug__:
    sys.stderr.write("verify_exponent.py refuses to run with assertions disabled (-O)\n")
    raise SystemExit(2)


class VerifyError(Exception):
    pass


CHECKS = 0


def need(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise VerifyError(message)


# ==========================================================================
# exact Krawtchouk data (integer numerators; denominators kept separate)
# ==========================================================================


def sign_sum_table(t):
    """S[k][a] = binom(t,k) * K^{(t)}_k(a), an integer."""
    return [[sum((-1) ** j * comb(a, j) * comb(t - a, k - j) for j in range(k + 1))
             for a in range(t + 1)] for k in range(t + 1)]


# ==========================================================================
# degree systems, re-derived
# ==========================================================================


def cycle_boundaries(m):
    out = set()
    for size in range(m + 1):
        for sub in itertools.combinations(range(m), size):
            c = [0] * m
            for v in sub:
                c[(v - 1) % m] += 1
                c[v] += 1
            out.add(tuple(x % 2 for x in c))
    return sorted(out)


def nw_degrees(m, t):
    opts = cycle_boundaries(m)
    cur = {tuple([0] * m)}
    for _ in range(t):
        cur = {tuple(d[i] + o[i] for i in range(m)) for d in cur for o in opts}
    return sorted(cur)


def ai_degrees(m, t):
    return sorted(k for k in itertools.product(range(t + 1), repeat=m)
                  if sum(k) % 2 == 0 and 2 * max(k) <= sum(k))


# ---- brute force over AI families (t <= 3) -------------------------------


def node_roots(m, node):
    v, (i, j) = node
    return frozenset({((v - 1) % m, i), (v, j)})


def ai_degrees_bruteforce(m, t):
    nodes = [(v, (i, j)) for v in range(m) for i in range(t) for j in range(t)]
    roots = [node_roots(m, nd) for nd in nodes]
    inj = set()
    for choice in itertools.product(range(t), repeat=m):
        members = [i for i in range(len(nodes))
                   if all(choice[g] == c for g, c in roots[i])]
        for size in range(1, len(members) + 1):
            for sub in itertools.combinations(members, size):
                inj.add(frozenset(sub))
    inj = sorted(inj, key=lambda s: (len(s), sorted(s)))
    inj_roots = [frozenset().union(*[roots[i] for i in b]) for b in inj]
    inj_bnd = []
    for b in inj:
        par = Counter()
        for i in b:
            for gc in roots[i]:
                par[gc] += 1
        inj_bnd.append(frozenset(gc for gc, n in par.items() if n % 2))
    out = set()

    def rec(start, used, bnd):
        d = [0] * m
        for g, _c in bnd:
            d[g] += 1
        out.add(tuple(d))
        for i in range(start, len(inj)):
            if inj_roots[i] & used:
                continue
            rec(i + 1, used | inj_roots[i], bnd | inj_bnd[i])

    rec(0, frozenset(), frozenset())
    return sorted(out)


# ---- explicit realization of every AI degree tuple (all t) ---------------


def arcs(m, g1, g2):
    out = []
    for (a, b) in ((g1, g2), (g2, g1)):
        length = (b - a) % m
        verts = [(a + s) % m for s in range(1, length + 1)]
        internal = [(a + s) % m for s in range(1, length)]
        out.append((verts, internal))
    return out


def realize_degrees(m, t, k):
    if max(k) > t or sum(k) % 2 or 2 * max(k) > sum(k):
        return None
    if m == 3:
        n01 = (k[0] + k[1] - k[2]) // 2
        n12 = (k[1] + k[2] - k[0]) // 2
        n20 = (k[2] + k[0] - k[1]) // 2
        if min(n01, n12, n20) < 0:
            return None
        edges = [((0, 1), n01), ((1, 2), n12), ((2, 0), n20)]
    elif m == 4:
        found = None
        for n02 in range(min(k[0], k[2]) + 1):
            for n13 in range(min(k[1], k[3]) + 1):
                a, b = k[0] - n02, k[1] - n13
                c, d = k[2] - n02, k[3] - n13
                if a + c != b + d:
                    continue
                if n13 > (t - k[0]) + (t - k[2]) or n02 > (t - k[1]) + (t - k[3]):
                    continue
                for n01 in range(0, min(a, b) + 1):
                    n12, n30 = b - n01, a - n01
                    n23 = c - n12
                    if min(n12, n23, n30) < 0 or n23 + n30 != d:
                        continue
                    found = (n01, n12, n23, n30, n02, n13)
                    break
                if found:
                    break
            if found:
                break
        if not found:
            return None
        n01, n12, n23, n30, n02, n13 = found
        edges = [((0, 1), n01), ((1, 2), n12), ((2, 3), n23), ((3, 0), n30),
                 ((0, 2), n02), ((1, 3), n13)]
    else:
        return None
    free = [list(range(t)) for _ in range(m)]
    blocks = []
    ordered = sorted(edges, key=lambda e: (e[0][1] - e[0][0]) % m not in (1, m - 1))
    for (g1, g2), mult in ordered:
        for _ in range(mult):
            placed = False
            for verts, internal in arcs(m, g1, g2):
                nsrc = Counter([g1, g2] + list(internal))
                if any(len(free[g]) < c for g, c in nsrc.items()):
                    continue
                pick = {g: [free[g].pop(0) for _ in range(c)] for g, c in nsrc.items()}
                copy_of = {g: v[0] for g, v in pick.items()}
                blocks.append([(v, (copy_of[(v - 1) % m], copy_of[v])) for v in verts])
                placed = True
                break
            if not placed:
                return None
    return blocks


def check_realization(m, t, k, blocks):
    """A family of copied observations is an AI family when every block is
    injectable (one copy per vertex, one copy index per source) and the blocks
    have pairwise disjoint ancestries.  Its prescribed character has degree
    tuple = the total boundary."""
    seen = set()
    deg = [0] * m
    for block in blocks:
        verts = [v for v, _ in block]
        if len(set(verts)) != len(verts):
            return False
        used = {}
        for nd in block:
            for g, c in node_roots(m, nd):
                if used.setdefault(g, c) != c:
                    return False
        for g, c in used.items():
            if (g, c) in seen or c >= t or c < 0:
                return False
            seen.add((g, c))
        par = Counter()
        for nd in block:
            for gc in node_roots(m, nd):
                par[gc] += 1
        bnd = [gc for gc, n in par.items() if n % 2]
        if len(bnd) not in (0, 2) or len({g for g, _ in bnd}) != len(bnd):
            return False
        for g, _c in bnd:
            deg[g] += 1
    return tuple(deg) == tuple(k)


# ==========================================================================
# helpers
# ==========================================================================


def sorted_tuples(m, t):
    return [tuple(x) for x in itertools.combinations_with_replacement(range(t + 1), m)]


def orbit_size(m, ab):
    d = factorial(m)
    for v in Counter(ab).values():
        d //= factorial(v)
    return d


def lcm(a, b):
    return a * b // gcd(a, b)


def perm_sum(m, S, key, ab, perms):
    """sum over sigma in S_m of prod_g S[key_g][ab_{sigma(g)}]  (integer)."""
    tot = 0
    for p in perms:
        pr = 1
        for g in range(m):
            pr *= S[key[g]][ab[p[g]]]
        tot += pr
    return tot


# ==========================================================================
# exact polynomial positivity (Sturm)
# ==========================================================================


def _trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def poly_eval(a, x):
    return sum(c * x ** i for i, c in enumerate(a))


def poly_div_rem(a, b):
    a = list(a)
    db = len(b) - 1
    while _trim(a) and len(a) - 1 >= db:
        sh = len(a) - 1 - db
        f = a[-1] / b[-1]
        for i in range(len(b)):
            a[sh + i] -= f * b[i]
        _trim(a)
    return a


def sturm_chain(a):
    a = _trim(list(a))
    if len(a) <= 1:
        return [a]
    d = _trim([F(i) * a[i] for i in range(1, len(a))])
    chain = [a, d]
    while len(chain[-1]) > 1:
        r = _trim([-x for x in poly_div_rem(chain[-2], chain[-1])])
        if not r:
            break
        chain.append(r)
    return chain


def sign_changes(chain, x):
    s = [1 if poly_eval(c, x) > 0 else -1 for c in chain if poly_eval(c, x) != 0]
    return sum(1 for i in range(1, len(s)) if s[i] != s[i - 1])


def distinct_roots_in(a, lo, hi):
    """Number of distinct real roots of the polynomial a in (lo, hi]."""
    ch = sturm_chain(a)
    return sign_changes(ch, lo) - sign_changes(ch, hi)


# ==========================================================================
# per-order checks
# ==========================================================================


def check_primal(m, t, S, degkeys, weights, q, perms):
    """weights: dict nondecreasing count tuple -> orbit mass (Fraction).
    Checks nonnegativity, normalization, and every prescribed moment of the
    symmetric distribution w_a = weights[sort(a)] / |orbit(sort(a))|.

    For such a w,  sum_a w_a prod_g K_{k_g}(a_g) = sum_abar V_abar kbar(k, abar),
    which depends on k only through sort(k); so ranging over the nondecreasing
    degree keys covers every prescribed degree tuple.  Integers throughout."""
    need(all(v >= 0 for v in weights.values()), "primal weight is negative")
    need(sum(weights.values()) == 1, "primal weights do not sum to 1")
    qn, qd = q.numerator, q.denominator
    Dv = 1
    for v in weights.values():
        Dv = lcm(Dv, v.denominator)
    items = [(ab, int(v * Dv)) for ab, v in weights.items()]
    for key in degkeys:
        Ssum = sum(key)
        h = Ssum // 2
        lhs = 0
        for ab, nv in items:
            lhs += nv * perm_sum(m, S, key, ab, perms)
        P = 1
        for g in range(m):
            P *= comb(t, key[g])
        # sum_a w_a prod K = (-q)^{S/2}
        lhs *= qd ** h
        rhs = Dv * factorial(m) * P * ((-1) ** h) * (qn ** h)
        need(lhs == rhs, f"primal moment mismatch at degree {key}")
    return True


def check_dual(m, t, S, coeffs, obs, perms):
    """coeffs: dict nondecreasing key -> Fraction.  The unsymmetrized Farkas
    multiplier is lambda_k = coeffs[sort(k)] / |orbit of sort(k)| on every
    prescribed degree tuple k, and then

        sum_k lambda_k prod_g K_{k_g}(a_g) = sum_key coeffs[key] kbar(key, a),

    with kbar the permutation average.  kbar(key, a) depends on a only through
    sort(a), so checking the nondecreasing configurations checks all (t+1)^m of
    them.  Everything is done in integers: kbar = perm_sum / (m! prod_g C(t,k_g)),
    and multiplying by the positive constant (common denominator) * m! * lcm of
    the prod_g C(t,k_g) clears them."""
    keys = sorted(coeffs)
    Dc = 1
    for v in coeffs.values():
        Dc = lcm(Dc, v.denominator)
    P = {}
    L = 1
    for key in keys:
        p = 1
        for g in range(m):
            p *= comb(t, key[g])
        P[key] = p
        L = lcm(L, p)
    num = {key: int(coeffs[key] * Dc) * (L // P[key]) for key in keys}
    worst = None
    for ab in obs:
        val = 0
        for key in keys:
            val += num[key] * perm_sum(m, S, key, ab, perms)
        if worst is None or val > worst:
            worst = val
        need(val <= 0, f"dual functional positive at configuration {ab}")
    return worst == 0


def dual_poly_coeffs(coeffs):
    out = {}
    for key, c in coeffs.items():
        d = sum(key) // 2
        out[d] = out.get(d, F(0)) + c * ((-1) ** d)
    deg = max(out) if out else 0
    return [out.get(i, F(0)) for i in range(deg + 1)]


# ==========================================================================
# driver
# ==========================================================================


def verify_file(path, max_order=None, log=print):
    data = json.load(open(path))
    m = data["cycle_length"]
    q_top = F(data["q_top"])
    name = data["scenario"]
    log(f"\n=== {name} (C_{m}), cap q_top = {data['q_top']} ===")
    log(f"    {data['q_top_note']}")

    orders = [r for r in data["orders"]
              if max_order is None or r["t"] <= max_order]
    tmax = max(r["t"] for r in orders)

    # ---- degree systems ------------------------------------------------
    deg_cache = {}
    for t in range(1, tmax + 1):
        nw = nw_degrees(m, t)
        ai = ai_degrees(m, t)
        deg_cache[t] = {"NW": nw, "AI": ai}
        need(set(nw) <= set(ai), f"t={t}: NW degrees not inside AI degrees")
        rec = data["degree_systems"][str(t)]
        need(rec["nw_count"] == len(nw), f"t={t}: NW degree count mismatch")
        need(rec["ai_count"] == len(ai), f"t={t}: AI degree count mismatch")
        if t <= 3:
            need(ai_degrees_bruteforce(m, t) == ai,
                 f"t={t}: brute force over AI families disagrees with the "
                 f"characterisation S even, 2 max k <= S")
        bad = 0
        for k in ai:
            blocks = realize_degrees(m, t, k)
            if blocks is None or not check_realization(m, t, k, blocks):
                bad += 1
        need(bad == 0, f"t={t}: {bad} AI degree tuples not realized by an AI family")
        log(f"  t={t}: NW {len(nw)} / AI {len(ai)} degree tuples"
            + ("  [AI brute-forced over all AI families]" if t <= 3 else "")
            + "  [every AI tuple realized by an explicit AI family]")

    # ---- orders ---------------------------------------------------------
    table = []
    for rec in orders:
        t, hier = rec["t"], rec["hierarchy"]
        S = sign_sum_table(t)
        perms = list(itertools.permutations(range(m)))
        obs = sorted_tuples(m, t)
        full = deg_cache[t][hier]
        need(rec["degree_tuples"] == len(full),
             f"t={t} {hier}: degree tuple count mismatch")
        degkeys = sorted({tuple(sorted(k)) for k in full})
        need(rec["symmetrized_keys"] == len(degkeys),
             f"t={t} {hier}: symmetrized key count mismatch")

        t0 = time.time()
        q_lo = F(rec["q_lo"])
        need(0 < q_lo <= q_top, f"t={t} {hier}: q_lo outside (0, q_top]")
        weights = {tuple(a): F(v) for a, v in rec["primal_weights"]}
        for ab in weights:
            need(tuple(sorted(ab)) == ab and len(ab) == m and max(ab) <= t,
                 f"t={t} {hier}: malformed count tuple {ab}")
        check_primal(m, t, S, degkeys, weights, q_lo, perms)

        line = {"t": t, "hierarchy": hier, "q_lo": q_lo, "q_hi": None,
                "support": len(weights), "dual_pieces": 0}
        if rec["q_hi"] is None:
            log(f"  t={t} {hier}: P_q in I^{hier}_{t} at q = {rec['q_lo']}"
                f" = {float(q_lo):.10f}  (feasible up to the cap; no upper bound)"
                f"   [{time.time() - t0:.1f}s]")
            table.append(line)
            continue

        q_hi = F(rec["q_hi"])
        need(q_lo < q_hi <= q_top, f"t={t} {hier}: q_hi outside (q_lo, q_top]")
        pieces = rec["dual_pieces"]
        need(len(pieces) >= 1, f"t={t} {hier}: no dual pieces")
        left = q_hi
        nterms = 0
        for idx, piece in enumerate(pieces):
            a, b = F(piece["interval"][0]), F(piece["interval"][1])
            need(a == left, f"t={t} {hier}: dual piece {idx} does not start where "
                            f"the previous one ended")
            need(a < b <= q_top, f"t={t} {hier}: dual piece {idx} has an empty "
                                 f"or out-of-range interval")
            coeffs = {tuple(k): F(v) for k, v in piece["coefficients"]}
            for k in coeffs:
                need(tuple(sorted(k)) == k and k in set(degkeys),
                     f"t={t} {hier}: dual key {k} is not a prescribed degree tuple")
            check_dual(m, t, S, coeffs, obs, perms)
            poly = dual_poly_coeffs(coeffs)
            stated = {int(d): F(v) for d, v in piece["polynomial"]}
            deg = max(list(stated) + [len(poly) - 1])
            need(all(stated.get(i, F(0)) == (poly[i] if i < len(poly) else F(0))
                     for i in range(deg + 1)),
                 f"t={t} {hier}: piece {idx} polynomial disagrees with its coefficients")
            need(poly_eval(poly, a) > 0 and poly_eval(poly, b) > 0,
                 f"t={t} {hier}: piece {idx} expectation not positive at an endpoint")
            nr = distinct_roots_in(poly, a, b)
            need(nr == 0, f"t={t} {hier}: piece {idx} polynomial has {nr} root(s) "
                          f"inside its own interval")
            nterms += len(coeffs)
            left = b
        need(left == q_top, f"t={t} {hier}: the dual pieces do not reach q_top")
        line.update({"q_hi": q_hi, "dual_pieces": len(pieces)})
        log(f"  t={t} {hier}: q_lo = {float(q_lo):.10f} <= q_max <= {float(q_hi):.10f}"
            f" = q_hi   (primal support {len(weights)}, {len(pieces)} dual piece(s)"
            f" covering [q_hi, q_top], {nterms} terms)   [{time.time() - t0:.1f}s]")
        table.append(line)
    return data, table


def summarize(tables, log=print):
    log("\n=== brackets ===")
    for name, table in tables.items():
        log(f"\n{name}")
        log(f"  {'t':>3} {'H':>3} {'q_lo':>14} {'q_hi':>14} {'t*q_lo':>9}")
        for r in sorted(table, key=lambda r: (r["t"], r["hierarchy"])):
            hi = f"{float(r['q_hi']):.10f}" if r["q_hi"] else "  (cap)"
            log(f"  {r['t']:>3} {r['hierarchy']:>3} {float(r['q_lo']):>14.10f}"
                f" {hi:>14} {r['t'] * float(r['q_lo']):>9.5f}")


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--dir", default=os.path.join(here, "certificates"))
    ap.add_argument("--max-order", type=int, default=None)
    args = ap.parse_args()
    t0 = time.time()
    tables = {}
    for name in ("square", "triangle"):
        path = os.path.join(args.dir, f"{name}.json")
        if not os.path.exists(path):
            print(f"missing {path}")
            continue
        _data, table = verify_file(path, args.max_order)
        tables[name] = table
    summarize(tables)
    print(f"\nOK: {CHECKS} exact checks passed in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
