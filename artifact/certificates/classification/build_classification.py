#!/usr/bin/env python3
"""Builder for the classification certificates.

Generates five_path.json, cycles.json, square.json, triangle.json and
low_order_square.json.  numpy/scipy are used ONLY to discover linear-programming
solutions and dual vectors; every number that ends up in a certificate is
recomputed here with exact integers and fractions, and is re-derived from
scratch by the independent stdlib-only verify_classification.py.

The constructions here are implemented along a deliberately different route from
the verifier: densities come from the derived subset expansion / count formula,
never from the complex Gaussian-rational product that the verifier uses, so the
two implementations cross-check each other.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction as F
from math import comb, gcd
from pathlib import Path

if not __debug__:
    raise RuntimeError("build_classification.py must run without -O/-OO.")

HERE = Path(__file__).resolve().parent


class BuildError(Exception):
    pass


def need(ok, message):
    if not ok:
        raise BuildError(message)


# ==========================================================================
# densities, by the derived expansion (independent of the verifier's route)
# ==========================================================================


def expansion_coefficient(sizes, q, c):
    """Coefficient of prod_{v in S} s_v in W = Re prod_g f_g + c sum_g (1-Re f_g),
    where sizes[g] = |S cap family g|.  Derived in REPORT.md."""
    total = sum(sizes)
    if total == 0:
        return F(1)
    if total % 2:
        return F(0)
    base = (-q) ** (total // 2)
    return base if sum(1 for k in sizes if k) >= 2 else (1 - c) * base


def density_by_expansion(groups, q, c):
    """Direct sum over all subsets of the sign vector."""
    flat = [s for g in groups for s in g]
    owner = [gi for gi, g in enumerate(groups) for _ in g]
    total = F(0)
    n = len(flat)
    for mask in range(1 << n):
        sizes = [0] * len(groups)
        prod = 1
        for i in range(n):
            if mask >> i & 1:
                sizes[owner[i]] += 1
                prod *= flat[i]
        total += expansion_coefficient(sizes, q, c) * prod
    return total


def subset_sign_sum(t, a, k):
    """sum over k-subsets of a family of t signs with a minus signs of the
    product of the chosen signs."""
    return sum((-1) ** j * comb(a, j) * comb(t - a, k - j) for j in range(k + 1))


def density_by_counts(counts, t, q, c):
    """W as a function of the per-family minus-counts, from the same expansion
    grouped by family sizes."""
    m = len(counts)
    full = F(0)
    for sizes in itertools.product(range(t + 1), repeat=m):
        if sum(sizes) % 2:
            continue
        term = (-q) ** (sum(sizes) // 2)
        for g in range(m):
            term *= subset_sign_sum(t, counts[g], sizes[g])
        full += term
    single = []
    for g in range(m):
        acc = F(0)
        for k in range(0, t + 1, 2):
            acc += (-q) ** (k // 2) * subset_sign_sum(t, counts[g], k)
        single.append(acc)
    return full + c * sum(F(1) - x for x in single)


# ==========================================================================
# scenarios (independent, minimal re-implementation)
# ==========================================================================


SCENARIOS = {
    "square": (["A", "B", "C", "D"],
               {"A": ("x", "w"), "B": ("x", "y"), "C": ("y", "z"), "D": ("z", "w")},
               ["x", "y", "z", "w"]),
    "triangle": (["A", "B", "C"],
                 {"A": ("x", "z"), "B": ("x", "y"), "C": ("z", "y")},
                 ["x", "y", "z"]),
}


def make_nodes(vertices, incidence, sources, t):
    sidx = {g: i for i, g in enumerate(sources)}
    nodes = []
    for v in vertices:
        for copies in itertools.product(range(t), repeat=len(incidence[v])):
            nodes.append((v, tuple((sidx[g], c) for g, c in zip(incidence[v], copies))))
    return nodes


def cycle_spec(m):
    return ([f"V{v}" for v in range(m)],
            {f"V{v}": (f"e{(v - 1) % m}", f"e{v}") for v in range(m)},
            [f"e{v}" for v in range(m)])


# ==========================================================================
# exact helpers
# ==========================================================================


def fwht(values):
    a = list(values)
    h = 1
    while h < len(a):
        for i in range(0, len(a), 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a


def lcm_den(values):
    den = 1
    for value in values:
        den = den * value.denominator // gcd(den, value.denominator)
    return den


def as_atoms(probs):
    den = lcm_den(probs.values())
    atoms = {}
    for mask, value in probs.items():
        num = value * den
        need(num.denominator == 1, "non-integral numerator")
        if num != 0:
            atoms[mask] = int(num)
    return atoms, den


def flip_dense(atoms, den, n, eta):
    p, r = eta.numerator, eta.denominator
    keep = r - p
    cur = [0] * (1 << n)
    for w, value in atoms.items():
        cur[w] = value
    for bit in range(n):
        step = 1 << bit
        cur = [keep * cur[w] + p * cur[w ^ step] for w in range(len(cur))]
    return {w: value for w, value in enumerate(cur) if value != 0}, den * r ** n


def flip_law(target, nv, eta):
    cur = list(target)
    for bit in range(nv):
        step = 1 << bit
        cur = [(1 - eta) * cur[w] + eta * cur[w ^ step] for w in range(len(cur))]
    return cur


def moments_of(atoms, den, n):
    dense = [0] * (1 << n)
    for w, value in atoms.items():
        dense[w] = value
    arr = fwht(dense)
    return [F(x, den) for x in arr]


# ==========================================================================
# witnesses
# ==========================================================================


def product_atoms(vertices, incidence, sources, t, q, c, eta=None):
    nodes = make_nodes(vertices, incidence, sources, t)
    n = len(nodes)
    nsrc = len(sources)
    N = nsrc * t
    memo = {}
    probs = {}
    for bits in itertools.product((0, 1), repeat=N):
        counts = tuple(sum(bits[g * t + i] for i in range(t)) for g in range(nsrc))
        if counts not in memo:
            memo[counts] = density_by_counts(counts, t, q, c)
        weight = memo[counts]
        if weight == 0:
            continue
        mask = 0
        for i, (_, roots) in enumerate(nodes):
            parity = 0
            for g, cp in roots:
                parity ^= bits[g * t + cp]
            mask |= parity << i
        probs[mask] = probs.get(mask, F(0)) + weight / (1 << N)
    atoms, den = as_atoms(probs)
    if eta is not None:
        atoms, den = flip_dense(atoms, den, n, eta)
    return nodes, atoms, den


def five_path_atoms(t):
    vertices = ["A", "B", "C", "D", "E"]
    incidence = {"A": ("X",), "B": ("X", "L"), "C": ("L", "R"), "D": ("R", "Z"), "E": ("Z",)}
    sources = ["X", "L", "R", "Z"]
    nodes = make_nodes(vertices, incidence, sources, t)
    index = {nd: i for i, nd in enumerate(nodes)}
    h = F(1, 16 * t * t)
    probs = {}
    for ub in itertools.product((0, 1), repeat=t):
        for vb in itertools.product((0, 1), repeat=t):
            u = [1 - 2 * b for b in ub]
            vv = [1 - 2 * b for b in vb]
            sigma = u + [-x for x in vv]
            weight = F(0)
            for mask in range(1 << (2 * t)):
                size = bin(mask).count("1")
                if size % 2:
                    continue
                prod = 1
                for i in range(2 * t):
                    if mask >> i & 1:
                        prod *= sigma[i]
                weight += (-h) ** (size // 2) * prod
            if weight == 0:
                continue
            base_weight = weight / (1 << (6 * t + t * t))
            for X in itertools.product((0, 1), repeat=t):
                for Z in itertools.product((0, 1), repeat=t):
                    for rb in itertools.product((0, 1), repeat=t):
                        for sb in itertools.product((0, 1), repeat=t):
                            r = [1 - 2 * b for b in rb]
                            s = [1 - 2 * b for b in sb]
                            base = 0
                            for a in range(t):
                                if X[a]:
                                    base |= 1 << index[("A", ((0, a),))]
                                for i in range(t):
                                    if r[i] * (u[i] if X[a] else 1) < 0:
                                        base |= 1 << index[("B", ((0, a), (1, i)))]
                            for e in range(t):
                                if Z[e]:
                                    base |= 1 << index[("E", ((3, e),))]
                                for j in range(t):
                                    if s[j] * (vv[j] if Z[e] else 1) < 0:
                                        base |= 1 << index[("D", ((2, j), (3, e)))]
                            for eps in itertools.product((0, 1), repeat=t * t):
                                mask2 = base
                                for i in range(t):
                                    for j in range(t):
                                        sign = r[i] * s[j]
                                        if u[i] != vv[j] and eps[i * t + j]:
                                            sign = -sign
                                        if sign < 0:
                                            mask2 |= 1 << index[("C", ((1, i), (2, j)))]
                                probs[mask2] = probs.get(mask2, F(0)) + base_weight
    atoms, den = as_atoms(probs)
    return nodes, atoms, den, h


# ==========================================================================
# targets
# ==========================================================================


def five_path_target(h):
    out = []
    for w in range(32):
        x = w & 1
        z = (w >> 4) & 1
        bcd = (-1) ** (((w >> 1) & 1) + ((w >> 2) & 1) + ((w >> 3) & 1))
        out.append(F(1, 32) * (1 + bcd * F(1 + h, 4) * (1 + (-1) ** (x + z))))
    return out


def cycle_target(m, q):
    moments = []
    for Fmask in range(1 << m):
        bnd = sum(1 for e in range(m)
                  if ((Fmask >> e) & 1) ^ ((Fmask >> ((e + 1) % m)) & 1))
        moments.append((-q) ** (bnd // 2))
    den = lcm_den(moments)
    return [F(x, den << m) for x in fwht([int(v * den) for v in moments])]


def square_target(q):
    out = []
    for w in range(16):
        bits = [(w >> k) & 1 for k in range(4)]
        if sum(bits) % 2:
            out.append(F(0))
            continue
        word = "".join(str(b) for b in bits)
        if word == "0000":
            out.append((1 - 6 * q + q * q) / 8)
        elif word in ("0011", "0110", "1001", "1100"):
            out.append((1 - q * q) / 8)
        else:
            out.append((1 + q) ** 2 / 8)
    return out


def triangle_target(q):
    out = []
    for w in range(8):
        a, b, c = [1 - 2 * ((w >> k) & 1) for k in range(3)]
        out.append(F(1 - q * (a + b + c), 4) if a * b * c == 1 else F(0))
    return out


# ==========================================================================
# structural enumeration (builder's own compact implementation)
# ==========================================================================


def structure(vertices, incidence, sources, t):
    nodes = make_nodes(vertices, incidence, sources, t)
    n = len(nodes)
    rootmask = []
    for _, roots in nodes:
        m = 0
        for g, c in roots:
            m |= 1 << (g * t + c)
        rootmask.append(m)
    vidx = {v: i for i, v in enumerate(vertices)}
    vertex_of = [vidx[v] for v, _ in nodes]

    def injectable(block):
        seen, used = set(), {}
        for i in block:
            if vertex_of[i] in seen:
                return False
            seen.add(vertex_of[i])
            for g, c in nodes[i][1]:
                if used.setdefault(g, c) != c:
                    return False
        return True

    inj = set()
    for choice in itertools.product(range(t), repeat=len(sources)):
        members = [i for i in range(n) if all(choice[g] == c for g, c in nodes[i][1])]
        for size in range(1, len(members) + 1):
            for sub in itertools.combinations(members, size):
                inj.add(frozenset(sub))
    inj = sorted(inj, key=lambda s: (min(s), sorted(s)))
    inj_roots = []
    for block in inj:
        m = 0
        for i in block:
            m |= rootmask[i]
        inj_roots.append(m)

    families = []

    def rec(start, used, chosen):
        families.append(tuple(chosen))
        for i in range(start, len(inj)):
            if inj_roots[i] & used:
                continue
            chosen.append(inj[i])
            rec(i + 1, used | inj_roots[i], chosen)
            chosen.pop()

    rec(0, 0, [])

    ai_sets = None
    if n <= 20:
        ai_sets = 0
        for mask in range(1 << n):
            rest = {i for i in range(n) if mask >> i & 1}
            ok = True
            while rest and ok:
                seed = rest.pop()
                block = {seed}
                roots = rootmask[seed]
                grew = True
                while grew:
                    grew = False
                    for j in list(rest):
                        if rootmask[j] & roots:
                            block.add(j)
                            rest.discard(j)
                            roots |= rootmask[j]
                            grew = True
                if not injectable(block):
                    ok = False
            if ok:
                ai_sets += 1
    return {"nodes": nodes, "n": n, "rootmask": rootmask, "vertex_of": vertex_of,
            "injectable_sets": len(inj), "families": families,
            "ai_sets": ai_sets, "injectable_list": inj}


def summarize(vertices, incidence, sources, t, atoms, den, target, *, label, check_ai=True):
    common = den
    for value in atoms.values():
        common = gcd(common, value)
    if common > 1:
        atoms = {w: v // common for w, v in atoms.items()}
        den //= common
    st = structure(vertices, incidence, sources, t)
    n = st["n"]
    nv = len(vertices)
    mom = moments_of(atoms, den, n)
    tmom = [F(x, lcm_den(target)) for x in fwht([int(v * lcm_den(target)) for v in target])]
    # normalization and positivity
    total = sum(atoms.values())
    need(total == den, f"{label}: not normalized")
    support = len(atoms)
    minimum = F(0) if support < (1 << n) else F(min(atoms.values()), den)
    # symmetry
    sidx = {g: i for i, g in enumerate(sources)}
    index = {nd: i for i, nd in enumerate(st["nodes"])}
    gens = 0
    for g in range(len(sources)):
        for c in range(t - 1):
            perm = []
            for v, roots in st["nodes"]:
                new = tuple((gg, (c + 1 if cc == c else c if cc == c + 1 else cc)) if gg == g
                            else (gg, cc) for gg, cc in roots)
                perm.append(index[(v, new)])
            for w, mass in atoms.items():
                dest = 0
                for i in range(n):
                    if w >> i & 1:
                        dest |= 1 << perm[i]
                need(atoms.get(dest, 0) == mass, f"{label}: symmetry failure")
            gens += 1
    # diagonal law
    rows = [[index[(v, tuple((sidx[g], r) for g in incidence[v]))] for v in vertices]
            for r in range(t)]
    positions = [rows[r][v] for r in range(t) for v in range(nv)]
    diag = {}
    for w, mass in atoms.items():
        dest = 0
        for k, pos in enumerate(positions):
            if w >> pos & 1:
                dest |= 1 << k
        diag[dest] = diag.get(dest, 0) + mass
    for cell in range(1 << (nv * t)):
        expected = F(1)
        for r in range(t):
            expected *= target[(cell >> (r * nv)) & ((1 << nv) - 1)]
        need(F(diag.get(cell, 0), den) == expected, f"{label}: diagonal cell {cell}")
    # AI families
    checked = 0
    singles = 0
    failures = []
    for family in st["families"]:
        union = 0
        expected = F(1)
        for block in family:
            for i in block:
                union |= 1 << i
            vm = 0
            for i in block:
                vm |= 1 << st["vertex_of"][i]
            expected *= tmom[vm]
        if mom[union] != expected:
            failures.append((sorted(sorted(b) for b in family), str(mom[union]), str(expected)))
            continue
        checked += 1
        if len(family) == 1:
            singles += 1
    if check_ai:
        need(not failures, f"{label}: AI family failure {failures[:1]}")
    return {"label": label, "order": t, "copied_observations": n,
            "ai_families_failing": len(failures),
            "first_failing_ai_family": (
                {"blocks": failures[0][0], "witness_character": failures[0][1],
                 "prescribed": failures[0][2]} if failures else None),
            "global_atoms": 1 << n, "witness_denominator": str(den),
            "positive_atoms": support, "minimum_atom": str(minimum),
            "minimum_positive_atom": str(F(min(atoms.values()), den)),
            "full_support": support == (1 << n),
            "symmetry_generators_checked": gens,
            "diagonal_cells_checked": 1 << (nv * t),
            "injectable_sets": st["injectable_sets"],
            "ai_sets": st["ai_sets"],
            "ai_families_checked": checked,
            "injectable_set_characters": singles}


# ==========================================================================
# low-order square thresholds
# ==========================================================================


def krawtchouk(t, k, a):
    return F(subset_sign_sum(t, a, k), comb(t, k))


def square_boundary_sets():
    inc = SCENARIOS["square"][1]
    out = set()
    for size in range(5):
        for sub in itertools.combinations("ABCD", size):
            cnt = {g: 0 for g in "xyzw"}
            for v in sub:
                for g in inc[v]:
                    cnt[g] += 1
            out.add(frozenset(g for g in "xyzw" if cnt[g] % 2))
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def nw_degrees(t):
    order = "xyzw"
    options = square_boundary_sets()
    out = set()

    def rec(row, deg):
        if row == t:
            out.add(tuple(deg))
            return
        for bs in options:
            rec(row + 1, [deg[i] + (1 if order[i] in bs else 0) for i in range(4)])

    rec(0, [0, 0, 0, 0])
    return sorted(out)


def ai_degrees_from_families(t):
    vertices, incidence, sources = SCENARIOS["square"]
    st = structure(vertices, incidence, sources, t)
    out = set()
    for family in st["families"]:
        bnd = 0
        for block in family:
            for i in block:
                bnd ^= st["rootmask"][i]
        out.add(tuple(sum(1 for c in range(t) if bnd >> (g * t + c) & 1) for g in range(4)))
    return sorted(out)


def count_row(t, k, a):
    value = F(1)
    for g in range(4):
        value *= krawtchouk(t, k[g], a[g])
    return value


def exact_gauss(rows, rhs, ncols):
    M = [list(r) + [v] for r, v in zip(rows, rhs)]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = F(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    for i in range(r, len(M)):
        if all(x == 0 for x in M[i][:ncols]) and M[i][ncols] != 0:
            return None
    x = [F(0)] * ncols
    for i, c in enumerate(piv):
        x[c] = M[i][ncols]
    return x


def count_primal(t, degs, q):
    import numpy as np
    from scipy.optimize import linprog
    counts = list(itertools.product(range(t + 1), repeat=4))
    A = [[1.0] * len(counts)] + [[float(count_row(t, k, a)) for a in counts] for k in degs]
    b = [1.0] + [float((-q) ** (sum(k) // 2)) for k in degs]
    res = linprog(c=np.zeros(len(counts)), A_eq=np.array(A), b_eq=np.array(b),
                  bounds=(0, None), method="highs")
    if res.status != 0:
        return None
    sup = [i for i, value in enumerate(res.x) if value > 1e-9]
    rows = [[F(1)] * len(sup)] + [[count_row(t, k, counts[i]) for i in sup] for k in degs]
    rhs = [F(1)] + [(-q) ** (sum(k) // 2) for k in degs]
    xs = exact_gauss(rows, rhs, len(sup))
    if xs is None:
        return None
    w = {a: F(0) for a in counts}
    for j, i in enumerate(sup):
        w[counts[i]] += xs[j] / 2
        w[tuple(t - x for x in counts[i])] += xs[j] / 2
    need(sum(w.values()) == 1, "count primal is not normalized")
    need(all(value >= 0 for value in w.values()), "count primal is not nonnegative")
    for k in degs:
        need(sum(w[a] * count_row(t, k, a) for a in counts) == (-q) ** (sum(k) // 2),
             f"count primal misses degree {k}")
    return {a: value for a, value in w.items() if value != 0}


def count_dual(t, degs, q, denominators=(1, 2, 3, 6, 30, 90, 540, 1080, 2700, 5400)):
    """Search for a rational dual certificate for infeasibility of the count
    system, using permutation-symmetrized coefficients."""
    import numpy as np
    from scipy.optimize import linprog
    counts = list(itertools.product(range(t + 1), repeat=4))
    keys = sorted({tuple(sorted(k)) for k in degs})

    def kbar(key, a):
        perms = sorted({p for p in itertools.permutations(key)})
        return sum(count_row(t, p, a) for p in perms) / len(perms)

    M = np.zeros((len(counts), len(keys) + 1))
    obj = np.zeros(len(keys) + 1)
    M[:, 0] = 1.0
    obj[0] = 1.0
    for ci, key in enumerate(keys):
        obj[ci + 1] = float((-q) ** (sum(key) // 2))
        for ai, a in enumerate(counts):
            M[ai, ci + 1] = float(kbar(key, a))
    res = linprog(c=-obj, A_ub=M, b_ub=np.zeros(len(counts)), bounds=(-1, 1), method="highs")
    if res.status != 0 or -res.fun <= 1e-12:
        return None
    for den in denominators:
        cand = []
        ok = True
        for value in res.x:
            num = round(value * den)
            if abs(num / den - value) > 1e-8:
                ok = False
                break
            cand.append(F(num, den))
        if not ok:
            continue
        const = cand[0]
        coeff = {keys[i]: cand[i + 1] for i in range(len(keys)) if cand[i + 1] != 0}
        values = [const + sum(c * kbar(k, a) for k, c in coeff.items()) for a in counts]
        if max(values) > 0:
            continue
        exp = const + sum(c * (-q) ** (sum(k) // 2) for k, c in coeff.items())
        if exp <= 0:
            continue
        return {"denominator": den, "constant": str(const),
                "coefficients": {",".join(map(str, k)): str(c) for k, c in sorted(coeff.items())},
                "maximum_value": str(max(values)),
                "configurations": len(counts),
                "expectation": str(exp)}
    return None


def ai_mask_records(t, q):
    """Every AI set of the square at order t, with the value prescribed by the
    finest (shared-source component) split of the target P_q."""
    vertices, incidence, sources = SCENARIOS["square"]
    st = structure(vertices, incidence, sources, t)
    n = st["n"]
    rootmask = st["rootmask"]
    vertex_of = st["vertex_of"]
    target = square_target(q)
    den = lcm_den(target)
    tmom = [F(x, den) for x in fwht([int(v * den) for v in target])]

    def injectable(block):
        seen, used = set(), {}
        for i in block:
            if vertex_of[i] in seen:
                return False
            seen.add(vertex_of[i])
            for g, c in st["nodes"][i][1]:
                if used.setdefault(g, c) != c:
                    return False
        return True

    out = {}
    for mask in range(1 << n):
        rest = {i for i in range(n) if mask >> i & 1}
        value = F(1)
        ok = True
        while rest:
            seed = rest.pop()
            block = {seed}
            roots = rootmask[seed]
            grew = True
            while grew:
                grew = False
                for j in list(rest):
                    if rootmask[j] & roots:
                        block.add(j)
                        rest.discard(j)
                        roots |= rootmask[j]
                        grew = True
            if not injectable(block):
                ok = False
                break
            vm = 0
            for i in block:
                vm |= 1 << vertex_of[i]
            value *= tmom[vm]
        if ok:
            out[mask] = value
    return st, out


def full_table_dual(t, q, denominators=(8, 49, 98, 196, 392, 784, 1960, 3136)):
    """A Farkas certificate for AI_t infeasibility directly on the 2^(4t^2)-atom
    table: lambda on the AI characters with sum lambda chi <= 0 pointwise and a
    strictly positive prescribed expectation."""
    import numpy as np
    from scipy.optimize import linprog
    vertices, incidence, sources = SCENARIOS["square"]
    st, prescribed = ai_mask_records(t, q)
    n = st["n"]
    index = {nd: i for i, nd in enumerate(st["nodes"])}
    gens = []
    for g in range(len(sources)):
        for c in range(t - 1):
            perm = []
            for v, roots in st["nodes"]:
                new = tuple((gg, (c + 1 if cc == c else c if cc == c + 1 else cc)) if gg == g
                            else (gg, cc) for gg, cc in roots)
                perm.append(index[(v, new)])
            gens.append(perm)

    def act(perm, mask):
        out = 0
        for i in range(n):
            if mask >> i & 1:
                out |= 1 << perm[i]
        return out

    def orbit(mask):
        seen = {mask}
        frontier = [mask]
        while frontier:
            new = []
            for m in frontier:
                for perm in gens:
                    img = act(perm, m)
                    if img not in seen:
                        seen.add(img)
                        new.append(img)
            frontier = new
        return seen

    rep_of = {}
    for mask in prescribed:
        if mask in rep_of:
            continue
        orb = orbit(mask)
        r = min(orb)
        for m in orb:
            rep_of[m] = r
    reps = sorted(set(rep_of.values()))
    col = {r: i for i, r in enumerate(reps)}
    om_rep = {}
    om_list = []
    for w in range(1 << n):
        if w in om_rep:
            continue
        orb = orbit(w)
        idx = len(om_list)
        om_list.append(w)
        for m in orb:
            om_rep[m] = idx
    M = np.zeros((len(om_list), len(reps)))
    obj = np.zeros(len(reps))
    for mask, r in rep_of.items():
        j = col[r]
        obj[j] += float(prescribed[mask])
        for oi, w in enumerate(om_list):
            M[oi, j] += -1.0 if bin(mask & w).count("1") % 2 else 1.0
    res = linprog(c=-obj, A_ub=M, b_ub=np.zeros(len(om_list)), bounds=(-1, 1), method="highs")
    if res.status != 0 or -res.fun <= 1e-12:
        return None
    for den in denominators:
        cand = []
        ok = True
        for value in res.x:
            num = round(value * den)
            if abs(num / den - value) > 1e-8:
                ok = False
                break
            cand.append(num)
        if not ok:
            continue
        coeff = [0] * (1 << n)
        for mask, r in rep_of.items():
            coeff[mask] += cand[col[r]]
        values = fwht(coeff)
        if max(values) > 0:
            continue
        expectation = sum(F(coeff[mask], den) * prescribed[mask] for mask in prescribed)
        if expectation <= 0:
            continue
        stored = [[r, cand[col[r]]] for r in reps if cand[col[r]] != 0]
        return {"denominator": den,
                "orbit_coefficients": stored,
                "ai_sets": len(prescribed),
                "mask_orbits": len(reps),
                "assignment_orbits": len(om_list),
                "atoms_checked": 1 << n,
                "maximum_functional_value": str(F(max(values), den)),
                "expectation": str(expectation)}
    return None


def character_summary(vertices, incidence, sources, t, q, c, target, label, eta=None):
    """Order-t checks carried out on the closed-form character function, for
    orders whose global table is too large to store."""
    st = structure(vertices, incidence, sources, t)
    n = st["n"]
    nv = len(vertices)
    den = lcm_den(target)
    tmom = [F(x, den) for x in fwht([int(v * den) for v in target])]
    factor = None if eta is None else (1 - 2 * eta)

    def chi(mask):
        bnd = 0
        for i in range(n):
            if mask >> i & 1:
                bnd ^= st["rootmask"][i]
        sizes = [sum(1 for cp in range(t) if bnd >> (g * t + cp) & 1)
                 for g in range(len(sources))]
        value = expansion_coefficient(sizes, q, c)
        if factor is not None:
            value *= factor ** bin(mask).count("1")
        return value

    index = {nd: i for i, nd in enumerate(st["nodes"])}
    sidx = {g: i for i, g in enumerate(sources)}
    rows = [[index[(v, tuple((sidx[g], r) for g in incidence[v]))] for v in vertices]
            for r in range(t)]
    cells = 0
    for sel in range(1 << (nv * t)):
        mask = 0
        expected = F(1)
        for r in range(t):
            sub = (sel >> (nv * r)) & ((1 << nv) - 1)
            for vtx in range(nv):
                if sub >> vtx & 1:
                    mask |= 1 << rows[r][vtx]
            expected *= tmom[sub]
        need(chi(mask) == expected, f"{label}: diagonal character {sel}")
        cells += 1
    checked = 0
    singles = 0
    for family in st["families"]:
        union = 0
        expected = F(1)
        for block in family:
            vm = 0
            for i in block:
                union |= 1 << i
                vm |= 1 << st["vertex_of"][i]
            expected *= tmom[vm]
        need(chi(union) == expected, f"{label}: AI family character")
        checked += 1
        if len(family) == 1:
            singles += 1
    return {"label": label, "order": t, "copied_observations": n,
            "global_atoms": f"2**{n}", "method": "exact Fourier characters (no stored table)",
            "diagonal_characters_checked": cells,
            "injectable_sets": st["injectable_sets"],
            "ai_families_checked": checked,
            "injectable_set_characters": singles}


def minimum_density(m, t, q, c):
    """Exhaustive over all 2**(m t) sign assignments.  W depends only on the
    per-family minus-counts, so the scan is organized by count tuple with an
    explicit multiplicity audit covering every assignment."""
    best = None
    covered = 0
    total = F(0)
    for counts in itertools.product(range(t + 1), repeat=m):
        value = density_by_counts(counts, t, q, c)
        mult = 1
        for a in counts:
            mult *= comb(t, a)
        covered += mult
        total += mult * value
        if best is None or value < best:
            best = value
    need(covered == 1 << (m * t), "count scan did not cover every assignment")
    need(total == covered, "the density does not average to 1 over the sign cube")
    return best, covered


def bilocal_numbers(target):
    """I, J of the five-path target, computed from the table."""
    fxz = {}
    for x in (0, 1):
        for z in (0, 1):
            num = F(0)
            den = F(0)
            for w in range(32):
                if (w & 1) != x or ((w >> 4) & 1) != z:
                    continue
                bcd = (-1) ** (((w >> 1) & 1) + ((w >> 2) & 1) + ((w >> 3) & 1))
                num += target[w] * bcd
                den += target[w]
            fxz[(x, z)] = num / den
    I = sum(fxz.values()) / 4
    J = sum(fxz[(x, z)] * (-1) ** (x + z) for x in (0, 1) for z in (0, 1)) / 4
    slack = 1 - I - J
    violated = slack < 0 or 4 * I * J > slack * slack
    return fxz, I, J, slack, violated


# ==========================================================================
# main
# ==========================================================================


P5_SPEC = (["A", "B", "C", "D", "E"],
           {"A": ("X",), "B": ("X", "L"), "C": ("L", "R"), "D": ("R", "Z"), "E": ("Z",)},
           ["X", "L", "R", "Z"])

ARCS = {3: [[0], [1], [2]], 4: [[0], [1], [2, 3]], 5: [[0], [1, 2], [3, 4]]}


def build_five_path():
    orders = []
    for t in (1, 2):
        nodes, atoms, den, h = five_path_atoms(t)
        target = five_path_target(h)
        rec = summarize(*P5_SPEC, t, atoms, den, target, label=f"five-path order {t}")
        rec["h"] = str(h)
        rec["target_minimum_atom"] = str(min(target))
        rec["target_lower_bound_(1-h)/64"] = str((1 - h) / 64)
        need(min(target) == (1 - h) / 64, "five-path target bound")
        fxz, I, J, slack, violated = bilocal_numbers(target)
        need(violated, "five-path bilocal inequality is not violated")
        rec["bilocal"] = {
            "f_xz": {f"{x}{z}": str(v) for (x, z), v in fxz.items()},
            "I": str(I), "J": str(J), "1-I-J": str(slack),
            "4IJ": str(4 * I * J), "(1-I-J)^2": str(slack * slack),
            "sqrt(I)+sqrt(J)_squared": str(I + J + 2 * I),
            "(sqrt(I)+sqrt(J))^2_equals_1+h": str(4 * I) + " = " + str(1 + h),
            "strictly_violates_sqrt(I)+sqrt(J)<=1": True}
        need(4 * I == 1 + h, "five-path (sqrt I + sqrt J)^2 != 1+h")
        orders.append(rec)
    return {"certificate": "five-path witness, B5 section 2.2 / AUDIT-NOTES A4",
            "scenario": "A(X), B(X,L), C(L,R), D(R,Z), E(Z)",
            "target": "P_h(x,b,c,d,z) = (1/32)[1 + bcd (1+h)/4 (1+(-1)^(x+z))], h = 1/(16 t^2)",
            "orders": orders}


def build_cycles():
    records = []
    for m, t in ((3, 1), (4, 1), (5, 1), (3, 2), (4, 2), (5, 2)):
        vertices, incidence, sources = cycle_spec(m)
        q = F(1, 4 * m * m * t * t)
        nodes, atoms, den = product_atoms(vertices, incidence, sources, t, q, 0)
        target = cycle_target(m, q)
        rec = summarize(vertices, incidence, sources, t, atoms, den, target,
                        label=f"C{m} order {t}")
        rec["m"] = m
        rec["q"] = str(q)
        tden = lcm_den(target)
        tmom = [F(x, tden) for x in fwht([int(v * tden) for v in target])]
        arcs = ARCS[m]
        means = []
        for arc in arcs:
            vm = 0
            for v in arc:
                vm |= 1 << v
            means.append(tmom[vm])
        need(all(mu == -q for mu in means), f"C{m}: arc means are not -q")
        allv = (1 << m) - 1
        need(tmom[allv] == 1, f"C{m}: the full parity is not 1")
        rec["incompatibility"] = {
            "arcs": arcs,
            "arc_means": [str(mu) for mu in means],
            "product_of_arc_means": str(means[0] * means[1] * means[2]),
            "E[V1 V2 V3]": str(tmom[allv]),
            "P(V1 V2 V3 = -1)": str((1 - tmom[allv]) / 2),
            "parity_rigidity": "a parity-perfect compatible triangle law has a "
                               "nonnegative product of the three means; here it is -q^3 < 0"}
        records.append(rec)
    return {"certificate": "cycle witnesses, B4 sections 3-6 / B5 section 4",
            "density": "H_{N,q}(s) = 2^{-N} sum_{|S| even} (-q)^{|S|/2} prod_S s, N = m t, "
                       "q = 1/(4 m^2 t^2)",
            "outputs": "O_v^{ij} = s_{v-1,i} s_{v,j}",
            "records": records}


def build_square():
    vertices, incidence, sources = SCENARIOS["square"]
    positivity = []
    for t in range(1, 6):
        q = F(1, 16 * t)
        best, covered = minimum_density(4, t, q, 5)
        need(best >= F(1, 3), f"square density minimum below 1/3 at t={t}")
        positivity.append({"t": t, "q": str(q), "assignments": covered,
                           "minimum_W": str(best), "at_least_1/3": True})
    expansion = []
    for t in (1, 2, 3):
        q = F(1, 16 * t)
        vals = []
        for bits in itertools.product((0, 1), repeat=4 * t):
            groups = [[1 - 2 * bits[g * t + i] for i in range(t)] for g in range(4)]
            vals.append(density_by_expansion(groups, q, 5))
        den = lcm_den(vals)
        coeffs = fwht([int(v * den) for v in vals])
        mismatches = 0
        for S in range(1 << (4 * t)):
            sizes = [sum(1 for i in range(t) if S >> (g * t + i) & 1) for g in range(4)]
            if F(coeffs[S], den << (4 * t)) != expansion_coefficient(sizes, q, 5):
                mismatches += 1
        need(mismatches == 0, f"square expansion mismatch at t={t}")
        expansion.append({"t": t, "characters": 1 << (4 * t), "mismatches": 0})
    uncorrected = []
    for t in (3, 4):
        q = F(1, 16 * t)
        allplus = tuple([0] * 4)
        old = density_by_counts(allplus, t, q, 0)
        new = density_by_counts(allplus, t, q, 5)
        need(old < 0 < new, f"square uncorrected/corrected comparison failed at t={t}")
        uncorrected.append({"t": t, "q": str(q), "uncorrected_W_at_all_plus": str(old),
                            "corrected_W_at_all_plus": str(new)})
    tables = []
    for t in (1, 2):
        q = F(1, 16 * t)
        eta = q / 64
        target = square_target(q)
        nodes, atoms, den = product_atoms(vertices, incidence, sources, t, q, 5)
        rec = summarize(vertices, incidence, sources, t, atoms, den, target,
                        label=f"square order {t}")
        rec["q"] = str(q)
        nodes, fatoms, fden = product_atoms(vertices, incidence, sources, t, q, 5, eta=eta)
        ftarget = flip_law(target, 4, eta)
        frec = summarize(vertices, incidence, sources, t, fatoms, fden, ftarget,
                         label=f"square order {t} with flips")
        frec["eta"] = str(eta)
        fden2 = lcm_den(ftarget)
        fmom = [F(x, fden2) for x in fwht([int(v * fden2) for v in ftarget])]
        EA, EB, EAB, EABCD = fmom[1], fmom[2], fmom[3], fmom[15]
        pneg = (1 - EABCD) / 2
        value = max(EA, EB, EAB) + 4 * pneg
        need(value < 0, "square max-moment certificate is not negative")
        frec["incompatibility"] = {
            "inequality": "max{EA, EB, E[AB]} + 4 P(ABCD = -1) >= 0 for every genuine "
                          "square law (B6 section 3)",
            "EA": str(EA), "EB": str(EB), "E[AB]": str(EAB), "E[ABCD]": str(EABCD),
            "P(ABCD=-1)": str(pneg), "value": str(value), "negative": True}
        tables.append({"plain": rec, "flipped": frec})
    q0 = []
    for q in (F(3, 20), F(1, 10), F(1, 32), F(1, 6), F(17, 100), F(1715, 10000),
              F(1716, 10000), F(9, 50), F(1, 5), F(1, 4)):
        atom = 1 - 6 * q + q * q
        q0.append({"q": str(q), "8*P(0000) = 1-6q+q^2": str(atom),
                   "is_probability_law": atom >= 0,
                   "(3-q)^2-8": str((3 - q) ** 2 - 8),
                   "q_le_3_minus_2sqrt2": (3 - q) ** 2 >= 8})
    need([c["is_probability_law"] for c in q0] ==
         [c["q_le_3_minus_2sqrt2"] for c in q0], "P_q validity is not equivalent to the threshold")
    need(q0[5]["is_probability_law"] and not q0[6]["is_probability_law"],
         "the 3-2sqrt2 bracket does not separate")
    return {"certificate": "corrected square density, B6 sections 1-2 and 3",
            "density": "W = Re prod_{g=1}^{4} f_g + 5 sum_g (1 - Re f_g), "
                       "f_g = prod_i (1 + i sqrt(q) s_{g,i}), q = 1/(16 t)",
            "outputs": "A^{il} = x_i w_l, B^{ij} = x_i y_j, C^{jk} = y_j z_k, D^{kl} = z_k w_l",
            "positivity_scan": positivity,
            "expansion_cross_check": expansion,
            "uncorrected_density_at_all_plus": uncorrected,
            "tables": tables,
            "P_q_validity": {"threshold": "q <= 3 - 2 sqrt 2, tested as (3-q)^2 >= 8, "
                                          "equivalently 1 - 6q + q^2 >= 0",
                             "cases": q0}}


def build_triangle():
    vertices, incidence, sources = SCENARIOS["triangle"]
    positivity = []
    for t in range(1, 7):
        q = F(1, 16 * t)
        best, covered = minimum_density(3, t, q, 4)
        need(best >= F(3, 5), f"triangle density minimum below 3/5 at t={t}")
        positivity.append({"t": t, "q": str(q), "assignments": covered,
                           "minimum_W": str(best), "at_least_3/5": True})
    uncorrected = []
    for t in (3, 4):
        q = F(1, 16 * t)
        allplus = (0, 0, 0)
        uncorrected.append({"t": t, "q": str(q),
                            "uncorrected_W_at_all_plus": str(density_by_counts(allplus, t, q, 0)),
                            "corrected_W_at_all_plus": str(density_by_counts(allplus, t, q, 4))})
    records = []
    for t in (1, 2, 3):
        q = F(1, 16 * t)
        eta = q / 192
        target = triangle_target(q)
        ftarget = flip_law(target, 3, eta)
        if t <= 2:
            nodes, atoms, den = product_atoms(vertices, incidence, sources, t, q, 4)
            rec = summarize(vertices, incidence, sources, t, atoms, den, target,
                            label=f"triangle order {t}")
            nodes, fatoms, fden = product_atoms(vertices, incidence, sources, t, q, 4, eta=eta)
            frec = summarize(vertices, incidence, sources, t, fatoms, fden, ftarget,
                             label=f"triangle order {t} with flips")
        else:
            rec = character_summary(vertices, incidence, sources, t, q, 4, target,
                                    f"triangle order {t}")
            frec = character_summary(vertices, incidence, sources, t, q, 4, ftarget,
                                     f"triangle order {t} with flips", eta=eta)
        rec["q"] = str(q)
        frec["q"] = str(q)
        frec["eta"] = str(eta)
        tden = lcm_den(target)
        tmom = [F(x, tden) for x in fwht([int(v * tden) for v in target])]
        need(tmom[1] == tmom[2] == tmom[4] == -q, "triangle target means")
        need(tmom[7] == 1, "triangle target parity")
        rec["target"] = {"EA": str(tmom[1]), "EB": str(tmom[2]), "EC": str(tmom[4]),
                         "E[AB]": str(tmom[3]), "E[ABC]": str(tmom[7]),
                         "product_of_means": str(tmom[1] * tmom[2] * tmom[4]),
                         "parity_rigidity_obstruction":
                             "compatible parity-perfect triangle laws have means (st,su,tu), "
                             "whose product is a square times (stu)^2 >= 0; here it is -q^3 < 0"}
        fden = lcm_den(ftarget)
        fmom = [F(x, fden) for x in fwht([int(v * fden) for v in ftarget])]
        EA, EB, EC, EAB, EABC = fmom[1], fmom[2], fmom[4], fmom[3], fmom[7]
        pneg = (1 - EABC) / 2
        m8 = max(EA, EB, EAB) + 8 * pneg
        m4 = max(EA, EB, EAB) + 4 * pneg
        need(m8 < 0, "triangle max-moment certificate is not negative")
        frec["incompatibility"] = {
            "certified_inequality":
                "B4 section 6 equation (20): for two adjacent observations A,B of a "
                "pair-source scenario and a selected collection V whose other members do "
                "not depend on the shared A,B source, every compatible law satisfies "
                "max{EA, EB, E[AB]} + 8 P(prod_V O = -1) >= 0.  The triangle with "
                "V = {A,B,C} satisfies the hypothesis: C carries sources z and y only.",
            "EA": str(EA), "EB": str(EB), "EC": str(EC), "E[AB]": str(EAB),
            "E[ABC]": str(EABC), "P(ABC=-1)": str(pneg),
            "max_plus_8P": str(m8), "max_plus_8P_negative": True,
            "max_plus_4P": str(m4), "max_plus_4P_negative": m4 < 0,
            "note": "the constant 4 version is the square inequality B6 (7); it is reported "
                    "for comparison only, the certified triangle statement is the 8 version",
            "product_of_means": str(EA * EB * EC),
            "parity_error_P(ABC=-1)": str(pneg)}
        records.append({"plain": rec, "flipped": frec})
    return {"certificate": "triangle analogue of the corrected density, AUDIT-NOTES B2(ii) "
                           "(NOT in the packet)",
            "density": "W = Re(f_x f_y f_z) + 4 sum_g (1 - Re f_g), q = 1/(16 t)",
            "outputs": "A^{ij} = x_i z_j, B^{ik} = x_i y_k, C^{jk} = z_j y_k",
            "target": "Pi(-q,-q,-q) on the parity face",
            "positivity_scan": positivity,
            "uncorrected_density_at_all_plus": uncorrected,
            "records": records}


def build_low_order():
    vertices, incidence, sources = SCENARIOS["square"]
    degrees = {}
    for t in (2, 3):
        nw = nw_degrees(t)
        ai = ai_degrees_from_families(t)
        predicted = sorted(k for k in itertools.product(range(t + 1), repeat=4)
                           if sum(k) % 2 == 0 and 2 * max(k) <= sum(k))
        need(ai == predicted, f"AI degree characterisation fails at t={t}")
        need(set(nw) <= set(ai), f"NW degrees are not contained in AI degrees at t={t}")
        degrees[str(t)] = {"nw_degree_tuples": len(nw), "ai_degree_tuples": len(ai),
                           "ai_minus_nw": [list(k) for k in sorted(set(ai) - set(nw))],
                           "characterisation": "S even, 2 max_g k_g <= S, k_g <= t "
                                               "(confirmed against brute-force AI families)"}
    primal = []
    for q in (F(3, 20), F(1, 10)):
        for name, degs in (("NW_2", nw_degrees(2)), ("AI_2", ai_degrees_from_families(2))):
            w = count_primal(2, degs, q)
            entry = {"q": str(q), "hierarchy": name, "feasible": w is not None,
                     "moment_equations": len(degs) + 1}
            if w is not None:
                scn_nodes = make_nodes(vertices, incidence, sources, 2)
                probs = {}
                for bits in itertools.product((0, 1), repeat=8):
                    a = tuple(sum(bits[g * 2 + i] for i in range(2)) for g in range(4))
                    weight = w.get(a, F(0))
                    if weight == 0:
                        continue
                    mu = weight
                    for g in range(4):
                        mu /= comb(2, a[g])
                    mask = 0
                    for i, (_, roots) in enumerate(scn_nodes):
                        parity = 0
                        for g, cp in roots:
                            parity ^= bits[g * 2 + cp]
                        mask |= parity << i
                    probs[mask] = probs.get(mask, F(0)) + mu
                atoms, den = as_atoms(probs)
                rec = summarize(vertices, incidence, sources, 2, atoms, den,
                                square_target(q), label=f"{name} witness at q={q}",
                                check_ai=(name == "AI_2"))
                entry["count_weights"] = [[list(a), str(value)] for a, value in sorted(w.items())]
                entry["nonzero_count_tuples"] = len(w)
                entry["expanded_table"] = rec
            primal.append(entry)
    ai2_infeasible = count_dual(2, ai_degrees_from_families(2), F(3, 20))
    need(ai2_infeasible is not None, "no rational AI_2 dual was found at q = 3/20")
    # B6 equation (16), independently evaluated
    keys = [(0, 0, 1, 1), (0, 0, 2, 2), (0, 2, 2, 2), (1, 1, 2, 2), (2, 2, 2, 2)]
    weights = [F(-24), F(-6), F(8), F(24), F(1)]

    def kbar(key, a):
        perms = sorted({p for p in itertools.permutations(key)})
        return sum(count_row(2, p, a) for p in perms) / len(perms)

    b6_values = []
    for a in itertools.product(range(3), repeat=4):
        b6_values.append(F(-3) + sum(cw * kbar(k, a) for k, cw in zip(keys, weights)))
    need(max(b6_values) == 0, "B6 D(a) is not <= 0 with maximum 0")
    b6 = {}
    for q in (F(3, 20), F(1, 10)):
        b6[str(q)] = str(F(-3) + sum(cw * (-q) ** (sum(k) // 2) for k, cw in zip(keys, weights)))
    # symbolic identity via sympy, plus an exact coefficient comparison
    import sympy as sp
    qs = sp.symbols("q")
    lhs = -3 + sum(int(cw) * (-qs) ** (sum(k) // 2) for k, cw in zip(keys, weights))
    rhs = (1 + qs) * (qs ** 3 - 33 * qs ** 2 + 27 * qs - 3)
    need(sp.simplify(sp.expand(lhs - rhs)) == 0, "sympy: E[D] != (1+q) g(q)")
    coeff_lhs = [sp.Poly(sp.expand(lhs), qs).coeff_monomial(qs ** i) for i in range(5)]
    coeff_rhs = [sp.Poly(sp.expand(rhs), qs).coeff_monomial(qs ** i) for i in range(5)]
    need(coeff_lhs == coeff_rhs, "coefficientwise identity failed")
    full = full_table_dual(2, F(3, 20))
    need(full is not None, "no rational full-table AI_2 dual was found at q = 3/20")
    nw3 = count_dual(3, nw_degrees(3), F(1, 10))
    need(nw3 is not None, "no rational NW_3 dual was found at q = 1/10")
    g = [F(-3), F(27), F(-33), F(1)]

    def gval(x):
        return sum(c * x ** i for i, c in enumerate(g))

    bracket = {"g(1324743/10000000)": str(gval(F(1324743, 10000000))),
               "g(1324744/10000000)": str(gval(F(1324744, 10000000))),
               "sign_change": gval(F(1324743, 10000000)) * gval(F(1324744, 10000000)) < 0}
    return {"certificate": "low-order square thresholds, B6 section 5",
            "reduction": "parity forcing + potential representation + count symmetrization "
                         "(stated and proved as a lemma in REPORT.md)",
            "degree_systems": degrees,
            "count_primal": primal,
            "ai2_dual_count_form": ai2_infeasible,
            "b6_equation_16": {"D(a) <= 0 on all 81 configurations": True,
                               "maximum": str(max(b6_values)),
                               "expectations": b6,
                               "symbolic_identity": "E[D] = (1+q)(q^3 - 33 q^2 + 27 q - 3)",
                               "sympy_verified": True},
            "ai2_dual_full_table": full,
            "nw3_dual_count_form": nw3,
            "g_root_bracket": bracket}


def main():
    outputs = {
        "five_path.json": build_five_path(),
        "cycles.json": build_cycles(),
        "square.json": build_square(),
        "triangle.json": build_triangle(),
        "low_order_square.json": build_low_order(),
    }
    for name, payload in outputs.items():
        (HERE / name).write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")
        print("wrote", name)
    import hashlib
    import time
    entries = {}
    for path in sorted(HERE.iterdir()):
        if not path.is_file() or path.name == "MANIFEST.json":
            continue
        entries[path.name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                              "size": path.stat().st_size}
    (HERE / "MANIFEST.json").write_text(json.dumps(
        {"certificate_directory": "classification",
         "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "arithmetic": "exact integers and fractions.Fraction; floating point only for "
                       "LP discovery inside build_classification.py",
         "files": entries}, indent=1, sort_keys=True) + "\n")
    print("wrote MANIFEST.json:", len(entries), "files")


if __name__ == "__main__":
    main()
