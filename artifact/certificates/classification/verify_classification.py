#!/usr/bin/env python3
"""Exact verifier for the classification certificates.

Covers the five-path witness (B5 section 2.2), the cycle witnesses (B4/B5
section 4), the corrected square density (B6 sections 1-2), the triangle
analogue (AUDIT-NOTES B2(ii)) and the low-order square thresholds (B6
section 5).

Standard library only: fractions, itertools, json, hashlib.  Every arithmetic
operation is exact.  Every failure raises CertificateError; nothing is hidden
inside an ``assert`` and the module refuses to run under -O/-OO.

This file is an independent re-implementation: it imports nothing from
build_classification.py, and it reconstructs every witness from the published
definitions before comparing against the recorded certificate values.

Conventions (matching AUDIT-NOTES)
----------------------------------
* Signs are +-1; a stored bit 1 means the sign -1.  For the five-path endpoints
  A and E the stored bit is the {0,1} setting x resp. z of the target formula.
* TV distance is half the l1 distance.
* A global witness is a normalized nonnegative table on ALL copied observations.
* NW_t: invariance under independent permutations of each source's copy indices,
  plus the full diagonal law P^{(x)t}.
* AI_t: additionally every injectable set (a subset of one copied original
  scenario, i.e. one copy of each source) carries the target marginal, and every
  family of pairwise ancestrally-disjoint injectable sets carries the product
  joint law.  Injectable sets and AI families are enumerated by brute force from
  these definitions at every order checked.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction as F
from math import comb, gcd
from pathlib import Path

if not __debug__:
    raise RuntimeError(
        "verify_classification.py must run without -O/-OO so that no check can "
        "ever be elided."
    )

HERE = Path(__file__).resolve().parent


class CertificateError(Exception):
    """Raised the moment any exact check fails."""


def need(ok: bool, message: str) -> None:
    if not ok:
        raise CertificateError(message)


def frac(text) -> F:
    return F(str(text))


# ==========================================================================
# 1. scenarios, injectable sets, AI families
# ==========================================================================


class Scenario:
    """A pair-source scenario inflated to order t."""

    def __init__(self, name, vertices, incidence, sources, order):
        self.name = name
        self.vertices = list(vertices)
        self.sources = list(sources)
        self.t = int(order)
        self.incidence = {v: tuple(incidence[v]) for v in self.vertices}
        self.sidx = {g: i for i, g in enumerate(self.sources)}
        nodes = []
        for v in self.vertices:
            for copies in itertools.product(range(self.t), repeat=len(self.incidence[v])):
                nodes.append((v, tuple((self.sidx[g], c)
                                       for g, c in zip(self.incidence[v], copies))))
        self.nodes = nodes
        self.n = len(nodes)
        self.index = {nd: i for i, nd in enumerate(nodes)}
        self.vertex_of = [self.vertices.index(v) for v, _ in nodes]
        self.rootmask = []
        for _, roots in nodes:
            m = 0
            for g, c in roots:
                m |= 1 << (g * self.t + c)
            self.rootmask.append(m)

    def boundary(self, mask):
        out = 0
        for i in range(self.n):
            if mask >> i & 1:
                out ^= self.rootmask[i]
        return out

    def components(self, mask):
        rest = {i for i in range(self.n) if mask >> i & 1}
        comps = []
        while rest:
            seed = rest.pop()
            block = {seed}
            roots = self.rootmask[seed]
            grew = True
            while grew:
                grew = False
                for j in list(rest):
                    if self.rootmask[j] & roots:
                        block.add(j)
                        rest.discard(j)
                        roots |= self.rootmask[j]
                        grew = True
            comps.append(frozenset(block))
        return comps

    def injectable(self, block):
        seen_v = set()
        used = {}
        for i in block:
            v = self.vertex_of[i]
            if v in seen_v:
                return False
            seen_v.add(v)
            for g, c in self.nodes[i][1]:
                if used.setdefault(g, c) != c:
                    return False
        return True

    def vertex_mask(self, block):
        out = 0
        for i in block:
            out |= 1 << self.vertex_of[i]
        return out

    def node_mask(self, block):
        out = 0
        for i in block:
            out |= 1 << i
        return out

    def injectable_sets(self):
        """Brute force from the definition: choose one copy index per source,
        take the copied original scenario it selects, take all its nonempty
        subsets."""
        out = set()
        for choice in itertools.product(range(self.t), repeat=len(self.sources)):
            members = [i for i in range(self.n)
                       if all(choice[g] == c for g, c in self.nodes[i][1])]
            for size in range(1, len(members) + 1):
                for sub in itertools.combinations(members, size):
                    out.add(frozenset(sub))
        return sorted(out, key=lambda s: (min(s), sorted(s)))

    def ai_families(self):
        """Every family of pairwise ancestrally-disjoint injectable sets,
        including the empty family."""
        inj = self.injectable_sets()
        roots = []
        for block in inj:
            m = 0
            for i in block:
                m |= self.rootmask[i]
            roots.append(m)
        out = []

        def rec(start, used, chosen):
            out.append(tuple(chosen))
            for i in range(start, len(inj)):
                if roots[i] & used:
                    continue
                chosen.append(inj[i])
                rec(i + 1, used | roots[i], chosen)
                chosen.pop()

        rec(0, 0, [])
        return out

    def ai_masks(self):
        """Every mask whose shared-source-copy components are all injectable,
        by brute force over all 2**n masks."""
        need(self.n <= 20, f"ai_masks refuses n = {self.n}")
        out = []
        for mask in range(1 << self.n):
            comps = self.components(mask)
            if all(self.injectable(c) for c in comps):
                out.append((mask, comps))
        return out

    def diagonal_rows(self):
        rows = []
        for r in range(self.t):
            rows.append([self.index[(v, tuple((self.sidx[g], r) for g in self.incidence[v]))]
                         for v in self.vertices])
        return rows

    def copy_transpositions(self):
        gens = []
        for g in range(len(self.sources)):
            for c in range(self.t - 1):
                perm = []
                for v, roots in self.nodes:
                    new = []
                    for gg, cc in roots:
                        if gg == g:
                            cc = c + 1 if cc == c else (c if cc == c + 1 else cc)
                        new.append((gg, cc))
                    perm.append(self.index[(v, tuple(new))])
                gens.append((self.sources[g], c, perm))
        return gens


# ==========================================================================
# 2. exact table utilities
# ==========================================================================


def fwht(values):
    a = list(values)
    h = 1
    n = len(a)
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a


def setpartitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for parts in setpartitions(rest):
        for i in range(len(parts)):
            yield parts[:i] + [[first] + parts[i]] + parts[i + 1:]
        yield [[first]] + parts


def target_characters(target):
    """Exact character table of a target law given as Fractions."""
    den = 1
    for value in target:
        den = den * value.denominator // gcd(den, value.denominator)
    return [F(m, den) for m in fwht([int(value * den) for value in target])]


# ==========================================================================
# 3. one witness and every check on it
# ==========================================================================


class Witness:
    """A global table stored as {atom -> integer numerator} over one denominator."""

    def __init__(self, scenario, atoms, denominator, target, label, closed_form=None):
        self.scn = scenario
        atoms = dict(atoms)
        common = denominator
        for value in atoms.values():
            common = gcd(common, value)
        if common > 1:
            atoms = {w: v // common for w, v in atoms.items()}
            denominator //= common
        self.atoms = atoms
        self.den = denominator
        self.target = list(target)
        self.label = label
        self.closed_form = closed_form
        self.tm = target_characters(self.target)

    # -- probability ------------------------------------------------------
    def check_probability(self):
        need(sum(self.atoms.values()) == self.den,
             f"{self.label}: not normalized")
        need(all(v > 0 for v in self.atoms.values()),
             f"{self.label}: stored support contains a non-positive numerator")
        support = len(self.atoms)
        full = 1 << self.scn.n
        minimum = F(0) if support < full else F(min(self.atoms.values()), self.den)
        return {"copied_observations": self.scn.n,
                "global_atoms": full,
                "positive_atoms": support,
                "minimum_atom": str(minimum),
                "minimum_positive_atom": str(F(min(self.atoms.values()), self.den)),
                "full_support": support == full}

    # -- symmetry ---------------------------------------------------------
    def check_symmetry(self):
        count = 0
        for source, pos, perm in self.scn.copy_transpositions():
            for w, mass in self.atoms.items():
                dest = 0
                for i in range(self.scn.n):
                    if w >> i & 1:
                        dest |= 1 << perm[i]
                need(self.atoms.get(dest, 0) == mass,
                     f"{self.label}: not symmetric under source {source}, copies ({pos},{pos+1})")
            count += 1
        return count

    # -- diagonal law -----------------------------------------------------
    def check_diagonal(self, table=None):
        scn = self.scn
        nv = len(scn.vertices)
        rows = scn.diagonal_rows()
        positions = [rows[r][v] for r in range(scn.t) for v in range(nv)]
        diag = {}
        source = self.atoms if table is None else table
        for w, mass in source.items():
            dest = 0
            for k, pos in enumerate(positions):
                if w >> pos & 1:
                    dest |= 1 << k
            diag[dest] = diag.get(dest, 0) + mass
        cells = 0
        bad = []
        for cell in range(1 << (nv * scn.t)):
            expected = F(1)
            for r in range(scn.t):
                expected *= self.target[(cell >> (r * nv)) & ((1 << nv) - 1)]
            actual = F(diag.get(cell, 0), self.den)
            if actual != expected:
                bad.append((cell, str(actual), str(expected)))
            cells += 1
        if table is None:
            need(not bad, f"{self.label}: diagonal law fails, first {bad[:1]}")
        return cells, bad

    # -- characters -------------------------------------------------------
    def dense_characters(self):
        full = 1 << self.scn.n
        need(full <= 1 << 20, f"{self.label}: dense character table refused at n={self.scn.n}")
        dense = [0] * full
        for w, mass in self.atoms.items():
            dense[w] = mass
        arr = fwht(dense)
        return lambda u: F(arr[u], self.den)

    def characters(self):
        if self.closed_form is not None:
            return self.closed_form
        return self.dense_characters()

    # -- AI ---------------------------------------------------------------
    def check_ai_families(self, chi):
        """Every family of pairwise ancestrally-disjoint injectable sets."""
        scn = self.scn
        checked = 0
        singles = 0
        for family in scn.ai_families():
            union = 0
            for block in family:
                union |= scn.node_mask(block)
            expected = F(1)
            for block in family:
                expected *= self.tm[scn.vertex_mask(block)]
            actual = chi(union)
            need(actual == expected,
                 f"{self.label}: AI family {[sorted(b) for b in family]} gives "
                 f"{actual} not {expected}")
            checked += 1
            if len(family) == 1:
                singles += 1
        return {"ai_families_checked": checked, "injectable_set_characters": singles}

    def check_ai_masks(self, chi):
        """Brute-force mask enumeration; every AI set and every partition of its
        shared-source components into blocks with injectable union."""
        scn = self.scn
        ai = scn.ai_masks()
        checked = 0
        for mask, comps in ai:
            actual = chi(mask)
            for parts in setpartitions(list(range(len(comps)))):
                blocks = []
                ok = True
                for blk in parts:
                    union = frozenset().union(*[comps[b] for b in blk])
                    if not scn.injectable(union):
                        ok = False
                        break
                    blocks.append(union)
                if not ok:
                    continue
                expected = F(1)
                for union in blocks:
                    expected *= self.tm[scn.vertex_mask(union)]
                need(actual == expected,
                     f"{self.label}: AI mask {mask} split {[sorted(b) for b in blocks]} "
                     f"gives {actual} not {expected}")
                checked += 1
        return {"ai_sets": len(ai), "ai_prescriptions_checked": checked}

    # -- negative control -------------------------------------------------
    def negative_control(self):
        """Move one unit of mass between the two globally permutation-invariant
        atoms (all-zero, all-one).  Normalization and all symmetries survive;
        the diagonal law must reject."""
        allone = (1 << self.scn.n) - 1
        need(self.atoms.get(0, 0) >= 1,
             f"{self.label}: negative control needs mass on the all-zero atom")
        bad = dict(self.atoms)
        bad[0] -= 1
        if bad[0] == 0:
            del bad[0]
        bad[allone] = bad.get(allone, 0) + 1
        need(sum(bad.values()) == self.den, f"{self.label}: control broke normalization")
        need(all(v >= 0 for v in bad.values()), f"{self.label}: control broke nonnegativity")
        for source, pos, perm in self.scn.copy_transpositions():
            for w, mass in bad.items():
                dest = 0
                for i in range(self.scn.n):
                    if w >> i & 1:
                        dest |= 1 << perm[i]
                need(bad.get(dest, 0) == mass, f"{self.label}: control broke symmetry")
        cells, failures = self.check_diagonal(table=bad)
        need(failures, f"{self.label}: the corrupted table still passes the diagonal law")
        return {"mass_moved": str(F(1, self.den)),
                "normalization_preserved": True,
                "symmetry_preserved": True,
                "diagonal_cells_rejected": len(failures),
                "first_rejected_cell": failures[0][0]}


# ==========================================================================
# 4. densities and constructions
# ==========================================================================
#
# All complex arithmetic is exact in the ring Q[J]/(J^2 + q), J = i sqrt(q):
# an element is the pair (real part, coefficient of J).


def gmul(a, b, q):
    return (a[0] * b[0] - q * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gfamily(signs, q):
    """f_g = prod_i (1 + i sqrt(q) s_i) with s_i in {+1,-1}."""
    acc = (F(1), F(0))
    for s in signs:
        acc = gmul(acc, (F(1), F(s)), q)
    return acc


def density(groups, q, c):
    """W = Re prod_g f_g + c * sum_g (1 - Re f_g); c = 0 gives the plain
    Fourier density Re prod (1 + i sqrt(q) s)."""
    fs = [gfamily(g, q) for g in groups]
    prod = (F(1), F(0))
    for f in fs:
        prod = gmul(prod, f, q)
    return prod[0] + c * sum(F(1) - f[0] for f in fs)


def density_coefficient(sizes, q, c):
    """Closed-form Fourier coefficient of `density` on a character whose
    intersection with family g has size sizes[g]."""
    total = sum(sizes)
    if total == 0:
        return F(1)
    if total % 2:
        return F(0)
    base = (-q) ** (total // 2)
    return base if sum(1 for k in sizes if k) >= 2 else (1 - c) * base


def sizes_of(scn, rootbits):
    return [sum(1 for cpy in range(scn.t) if rootbits >> (g * scn.t + cpy) & 1)
            for g in range(len(scn.sources))]


def product_witness(scn, q, c, eta=None):
    """The global table of the density `density` pushed through
    O_v = product of the two auxiliary signs at v, optionally followed by an
    independent flip of probability eta on every copied observation."""
    nsrc = len(scn.sources)
    N = nsrc * scn.t
    raw = {}
    for bits in itertools.product((0, 1), repeat=N):
        groups = [[1 - 2 * bits[g * scn.t + cpy] for cpy in range(scn.t)]
                  for g in range(nsrc)]
        w = density(groups, q, c)
        if w == 0:
            continue
        mask = 0
        for i in range(scn.n):
            parity = 0
            rm = scn.rootmask[i]
            for k in range(N):
                if rm >> k & 1:
                    parity ^= bits[k]
            mask |= parity << i
        raw[mask] = raw.get(mask, F(0)) + w
    probs = {w: v / (1 << N) for w, v in raw.items()}
    den = 1
    for value in probs.values():
        den = den * value.denominator // gcd(den, value.denominator)
    atoms = {}
    for w, value in probs.items():
        num = value * den
        need(num.denominator == 1, "product witness numerator is not an integer")
        if num != 0:
            atoms[w] = int(num)
    if eta is None:
        return atoms, den

    p, r = eta.numerator, eta.denominator
    keep = r - p
    cur = [0] * (1 << scn.n)
    for w, v in atoms.items():
        cur[w] = v
    for bit in range(scn.n):
        step = 1 << bit
        nxt = [0] * len(cur)
        for w in range(len(cur)):
            nxt[w] = keep * cur[w] + p * cur[w ^ step]
        cur = nxt
    return {w: v for w, v in enumerate(cur) if v != 0}, den * r ** scn.n


def product_characters(scn, q, c, den_check=None, eta=None):
    factor = None if eta is None else (1 - 2 * eta)

    def chi(mask):
        value = density_coefficient(sizes_of(scn, scn.boundary(mask)), q, c)
        if factor is not None:
            value *= factor ** bin(mask).count("1")
        return value

    return chi


# -- five-path ------------------------------------------------------------


def five_path_scenario(t):
    return Scenario("P5", ["A", "B", "C", "D", "E"],
                    {"A": ("X",), "B": ("X", "L"), "C": ("L", "R"),
                     "D": ("R", "Z"), "E": ("Z",)},
                    ["X", "L", "R", "Z"], t)


def five_path_target(h):
    """P_h(x,b,c,d,z) = (1/32)[1 + bcd (1+h)/4 (1 + (-1)^(x+z))];
    bit 0 = x, bits 1,2,3 = the signs b,c,d (bit 1 meaning -1), bit 4 = z."""
    out = []
    for w in range(32):
        x = w & 1
        z = (w >> 4) & 1
        bcd = (-1) ** (((w >> 1) & 1) + ((w >> 2) & 1) + ((w >> 3) & 1))
        out.append(F(1, 32) * (1 + bcd * F(1 + h, 4) * (1 + (-1) ** (x + z))))
    return out


def five_path_witness(t):
    """gamma = 1/(4t), h = gamma^2 = 1/(16 t^2).
    H_t(u,v) = 2^{-2t} Re[prod_i (1 + i gamma u_i) prod_j (1 - i gamma v_j)],
    fair X_a, Z_e, fair masks r_i, s_j, fair private eps_{ij},
    A^a = X_a, B^{ai} = r_i u_i^{X_a}, D^{je} = s_j v_j^{Z_e}, E^e = Z_e,
    C^{ij} = r_i s_j (times eps_{ij} exactly when u_i != v_j)."""
    scn = five_path_scenario(t)
    h = F(1, 16 * t * t)
    scale = (16 * t * t) ** t
    den = (1 << (6 * t + t * t)) * scale
    atoms = {}
    idxA = [scn.index[("A", ((0, a),))] for a in range(t)]
    idxB = [[scn.index[("B", ((0, a), (1, i)))] for i in range(t)] for a in range(t)]
    idxC = [[scn.index[("C", ((1, i), (2, j)))] for j in range(t)] for i in range(t)]
    idxD = [[scn.index[("D", ((2, j), (3, e)))] for e in range(t)] for j in range(t)]
    idxE = [scn.index[("E", ((3, e),))] for e in range(t)]
    for ub in itertools.product((0, 1), repeat=t):
        for vb in itertools.product((0, 1), repeat=t):
            u = [1 - 2 * b for b in ub]
            v = [1 - 2 * b for b in vb]
            sigma = u + [-x for x in v]
            weight = gfamily(sigma, h)[0]
            num = weight * scale
            need(num.denominator == 1, "five-path density is not an integer multiple")
            num = int(num)
            if num == 0:
                continue
            for X in itertools.product((0, 1), repeat=t):
                for Z in itertools.product((0, 1), repeat=t):
                    for rb in itertools.product((0, 1), repeat=t):
                        for sb in itertools.product((0, 1), repeat=t):
                            r = [1 - 2 * b for b in rb]
                            s = [1 - 2 * b for b in sb]
                            base = 0
                            for a in range(t):
                                if X[a]:
                                    base |= 1 << idxA[a]
                                for i in range(t):
                                    sign = r[i] * (u[i] if X[a] else 1)
                                    if sign < 0:
                                        base |= 1 << idxB[a][i]
                            for e in range(t):
                                if Z[e]:
                                    base |= 1 << idxE[e]
                                for j in range(t):
                                    sign = s[j] * (v[j] if Z[e] else 1)
                                    if sign < 0:
                                        base |= 1 << idxD[j][e]
                            for eps in itertools.product((0, 1), repeat=t * t):
                                mask = base
                                for i in range(t):
                                    for j in range(t):
                                        sign = r[i] * s[j]
                                        if u[i] != v[j] and eps[i * t + j]:
                                            sign = -sign
                                        if sign < 0:
                                            mask |= 1 << idxC[i][j]
                                atoms[mask] = atoms.get(mask, 0) + num
    return scn, atoms, den, five_path_target(h), h


# -- cycles ---------------------------------------------------------------


def cycle_scenario(m, t):
    vertices = [f"V{v}" for v in range(m)]
    sources = [f"e{v}" for v in range(m)]
    incidence = {f"V{v}": (f"e{(v - 1) % m}", f"e{v}") for v in range(m)}
    return Scenario(f"C{m}", vertices, incidence, sources, t)


def cycle_target(m, q):
    """Fourier moments (-q)^{|dF|/2}; dF = edges meeting F oddly."""
    moments = []
    for Fmask in range(1 << m):
        bnd = sum(1 for e in range(m)
                  if ((Fmask >> e) & 1) ^ ((Fmask >> ((e + 1) % m)) & 1))
        moments.append((-q) ** (bnd // 2))
    den = 1
    for value in moments:
        den = den * value.denominator // gcd(den, value.denominator)
    return [F(x, den << m) for x in fwht([int(v * den) for v in moments])]


# -- square ---------------------------------------------------------------


def square_scenario(t):
    return Scenario("square", ["A", "B", "C", "D"],
                    {"A": ("x", "w"), "B": ("x", "y"), "C": ("y", "z"), "D": ("z", "w")},
                    ["x", "y", "z", "w"], t)


def square_target(q):
    """B6 section 1 sign table, bit 1 meaning the sign -1, bit order A,B,C,D."""
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


# -- triangle -------------------------------------------------------------


def triangle_scenario(t):
    return Scenario("triangle", ["A", "B", "C"],
                    {"A": ("x", "z"), "B": ("x", "y"), "C": ("z", "y")},
                    ["x", "y", "z"], t)


def triangle_target(q):
    """Pi(-q,-q,-q): (1 + x a + y b + z c)/4 on the parity face, 0 elsewhere."""
    out = []
    for w in range(8):
        a, b, c = [1 - 2 * ((w >> k) & 1) for k in range(3)]
        out.append(F(1 - q * (a + b + c), 4) if a * b * c == 1 else F(0))
    return out


def flip_target(target, nv, eta):
    cur = list(target)
    for bit in range(nv):
        nxt = [F(0)] * len(cur)
        step = 1 << bit
        for w in range(len(cur)):
            nxt[w] = (1 - eta) * cur[w] + eta * cur[w ^ step]
        cur = nxt
    return cur


# ==========================================================================
# 5. low-order square thresholds (B6 section 5)
# ==========================================================================
#
# Parity-forcing lemma (proved in REPORT.md).  For the parity-perfect target
# P_q every NW_t witness is supported on arrays satisfying
# A^{il} B^{ij} C^{jk} D^{kl} = 1 for all i,j,k,l, and every such array is
# A^{il} = x_i w_l, B^{ij} = x_i y_j, C^{jk} = y_j z_k, D^{kl} = z_k w_l for
# potentials unique up to flipping all of them.  Averaging over the two gauges
# and over the source-copy permutations reduces the witness to a distribution
# w_a on the four minus-sign counts a in {0..t}^4, whose observable characters
# are products of Krawtchouk ratios.


def krawtchouk(t, k, a):
    """E[product of k distinct signs from a family of t signs of which a are -1],
    the sign positions chosen uniformly."""
    num = sum((-1) ** j * comb(a, j) * comb(t - a, k - j) for j in range(k + 1))
    return F(num, comb(t, k))


def square_boundary_sets():
    """Source boundaries of the vertex subsets of the square."""
    inc = {"A": ("x", "w"), "B": ("x", "y"), "C": ("y", "z"), "D": ("z", "w")}
    out = set()
    for size in range(5):
        for sub in itertools.combinations("ABCD", size):
            cnt = {g: 0 for g in "xyzw"}
            for v in sub:
                for g in inc[v]:
                    cnt[g] += 1
            out.add(frozenset(g for g in "xyzw" if cnt[g] % 2))
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def nw_degree_tuples(t):
    """Degrees of the characters prescribed by the full diagonal law at order t:
    one boundary set per diagonal row."""
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


def ai_degree_tuples(t):
    """Degrees of the characters prescribed by AI_t, read off the brute-force
    enumeration of families of ancestrally-disjoint injectable sets."""
    scn = square_scenario(t)
    out = set()
    for family in scn.ai_families():
        mask = 0
        for block in family:
            mask |= scn.node_mask(block)
        out.add(tuple(sizes_of(scn, scn.boundary(mask))))
    return sorted(out)


def count_moment(t, k, w):
    return sum(weight * krawtchouk(t, k[0], a[0]) * krawtchouk(t, k[1], a[1])
               * krawtchouk(t, k[2], a[2]) * krawtchouk(t, k[3], a[3])
               for a, weight in w.items())


def expand_counts(t, w):
    """Rebuild the full 4t^2-bit global table from the count weights."""
    scn = square_scenario(t)
    probs = {}
    for bits in itertools.product((0, 1), repeat=4 * t):
        a = tuple(sum(bits[g * t + i] for i in range(t)) for g in range(4))
        weight = w.get(a, F(0))
        if weight == 0:
            continue
        mu = weight
        for g in range(4):
            mu /= comb(t, a[g])
        mask = 0
        for i in range(scn.n):
            parity = 0
            rm = scn.rootmask[i]
            for kk in range(4 * t):
                if rm >> kk & 1:
                    parity ^= bits[kk]
            mask |= parity << i
        probs[mask] = probs.get(mask, F(0)) + mu
    den = 1
    for value in probs.values():
        den = den * value.denominator // gcd(den, value.denominator)
    atoms = {}
    for mask, value in probs.items():
        num = value * den
        need(num.denominator == 1, "count expansion numerator is not an integer")
        if num != 0:
            atoms[mask] = int(num)
    return scn, atoms, den


def orbit_expand(scn, reps_and_numerators):
    """Spread each stored orbit coefficient over the whole orbit of the mask
    under the group generated by the source-copy transpositions."""
    gens = [perm for _, _, perm in scn.copy_transpositions()]

    def act(perm, mask):
        out = 0
        for i in range(scn.n):
            if mask >> i & 1:
                out |= 1 << perm[i]
        return out

    coeff = {}
    for rep, num in reps_and_numerators:
        orbit = {rep}
        frontier = [rep]
        while frontier:
            new = []
            for mask in frontier:
                for perm in gens:
                    image = act(perm, mask)
                    if image not in orbit:
                        orbit.add(image)
                        new.append(image)
            frontier = new
        for mask in orbit:
            coeff[mask] = coeff.get(mask, 0) + num
    return coeff


def poly_mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def ai_prescribed(scn, target):
    """Every AI set of scn with the value prescribed by the finest split."""
    tm = target_characters(target)
    out = {}
    for mask, comps in scn.ai_masks():
        value = F(1)
        for block in comps:
            value *= tm[scn.vertex_mask(block)]
        out[mask] = value
    return out


def compare(record, key, actual, label):
    need(key in record, f"{label}: certificate has no field {key}")
    stored = record[key]
    if isinstance(stored, str) or isinstance(actual, str):
        stored, actual = str(stored), str(actual)
    need(stored == actual,
         f"{label}: field {key} recorded as {record[key]!r} but recomputed as {actual!r}")


def check_common(w, record, label, ai_mode="both", require_ai=True):
    prob = w.check_probability()
    for key in ("copied_observations", "global_atoms", "positive_atoms",
                "minimum_atom", "minimum_positive_atom", "full_support"):
        if key in record:
            compare(record, key, prob[key], label)
    compare(record, "witness_denominator", str(w.den), label)
    compare(record, "symmetry_generators_checked", w.check_symmetry(), label)
    cells, _ = w.check_diagonal()
    compare(record, "diagonal_cells_checked", cells, label)
    chi = w.characters()
    out = dict(prob)
    if ai_mode in ("both", "masks"):
        masks = w.check_ai_masks(chi)
        if record.get("ai_sets") is not None:
            compare(record, "ai_sets", masks["ai_sets"], label)
        out.update(masks)
    if ai_mode in ("both", "families"):
        fams = w.check_ai_families(chi)
        if require_ai:
            compare(record, "ai_families_checked", fams["ai_families_checked"], label)
            compare(record, "injectable_set_characters", fams["injectable_set_characters"], label)
        out.update(fams)
    out["negative_control"] = w.negative_control()
    return out


# ==========================================================================
# 6. the five certificate documents
# ==========================================================================


def verify_five_path(doc):
    out = []
    for record in doc["orders"]:
        t = record["order"]
        label = record["label"]
        scn, atoms, den, target, h = five_path_witness(t)
        compare(record, "h", str(h), label)
        need(min(target) == (1 - h) / 64, f"{label}: target atoms below (1-h)/64")
        compare(record, "target_minimum_atom", str(min(target)), label)
        compare(record, "target_lower_bound_(1-h)/64", str((1 - h) / 64), label)
        w = Witness(scn, atoms, den, target, label)
        stats = check_common(w, record, label)
        # bilocal inequality, exact and squared
        fxz = {}
        for x in (0, 1):
            for z in (0, 1):
                num = sum(target[u] * (-1) ** (((u >> 1) & 1) + ((u >> 2) & 1) + ((u >> 3) & 1))
                          for u in range(32) if (u & 1) == x and ((u >> 4) & 1) == z)
                den_ = sum(target[u] for u in range(32) if (u & 1) == x and ((u >> 4) & 1) == z)
                fxz[(x, z)] = num / den_
        I = sum(fxz.values()) / 4
        J = sum(fxz[(x, z)] * (-1) ** (x + z) for x in (0, 1) for z in (0, 1)) / 4
        bil = record["bilocal"]
        compare(bil, "I", str(I), label)
        compare(bil, "J", str(J), label)
        slack = 1 - I - J
        need(slack < 0 or 4 * I * J > slack * slack,
             f"{label}: the bilocal inequality is not strictly violated")
        need(4 * I == 1 + h, f"{label}: (sqrt I + sqrt J)^2 != 1 + h")
        stats["bilocal"] = {"I": str(I), "J": str(J), "4IJ": str(4 * I * J),
                            "(1-I-J)^2": str(slack * slack),
                            "(sqrt(I)+sqrt(J))^2": str(4 * I), "1+h": str(1 + h),
                            "strictly_violated": True}
        stats["label"] = label
        out.append(stats)
    return out


def verify_cycles(doc):
    out = []
    for record in doc["records"]:
        m, t = record["m"], record["order"]
        label = record["label"]
        q = F(1, 4 * m * m * t * t)
        compare(record, "q", str(q), label)
        scn = cycle_scenario(m, t)
        atoms, den = product_witness(scn, q, 0)
        target = cycle_target(m, q)
        w = Witness(scn, atoms, den, target, label,
                    closed_form=product_characters(scn, q, 0))
        if scn.n <= 16:
            dense = w.dense_characters()
            need(all(dense(u) == w.closed_form(u) for u in range(1 << scn.n)),
                 f"{label}: closed-form characters disagree with the stored table")
        stats = check_common(w, record, label)
        tm = w.tm
        inc = record["incompatibility"]
        means = []
        for arc in inc["arcs"]:
            vm = 0
            for v in arc:
                vm |= 1 << v
            means.append(tm[vm])
        need(all(mu == -q for mu in means), f"{label}: arc means are not -q")
        compare(inc, "arc_means", [str(x) for x in means], label)
        compare(inc, "product_of_arc_means", str(means[0] * means[1] * means[2]), label)
        need(means[0] * means[1] * means[2] < 0, f"{label}: the product of arc means is not negative")
        allv = (1 << m) - 1
        need(tm[allv] == 1, f"{label}: the three arc products do not multiply to 1 almost surely")
        compare(inc, "E[V1 V2 V3]", str(tm[allv]), label)
        stats["label"] = label
        stats["arc_means"] = [str(x) for x in means]
        stats["product_of_arc_means"] = str(means[0] * means[1] * means[2])
        out.append(stats)
    return out


def minimum_density(m, t, q, c):
    """Exhaustive over all 2**(m t) sign assignments.  W depends only on the
    per-family minus-counts (immediate from f_g = (1+i sqrt q)^(t-a) (1-i sqrt q)^a),
    so the scan runs over count tuples with an explicit multiplicity audit that
    accounts for every assignment."""
    best = None
    covered = 0
    total = F(0)
    for counts in itertools.product(range(t + 1), repeat=m):
        groups = [[-1] * a + [1] * (t - a) for a in counts]
        value = density(groups, q, c)
        mult = 1
        for a in counts:
            mult *= comb(t, a)
        covered += mult
        total += mult * value
        if best is None or value < best:
            best = value
    need(covered == 1 << (m * t), "the count scan did not cover every assignment")
    need(total == covered, "the density does not average to 1 over the sign cube")
    return best, covered


def verify_square(doc):
    scn_spec = square_scenario
    report = {}
    scan = []
    for record in doc["positivity_scan"]:
        t = record["t"]
        q = F(1, 16 * t)
        compare(record, "q", str(q), f"square density t={t}")
        best, covered = minimum_density(4, t, q, 5)
        compare(record, "minimum_W", str(best), f"square density t={t}")
        compare(record, "assignments", covered, f"square density t={t}")
        need(best >= F(1, 3), f"square density t={t}: minimum below 1/3")
        scan.append({"t": t, "q": str(q), "assignments": covered,
                     "minimum_W": str(best), "at_least_1/3": True})
    report["positivity_scan"] = scan
    # the derived expansion against the Gaussian-rational product
    cross = []
    for record in doc["expansion_cross_check"]:
        t = record["t"]
        q = F(1, 16 * t)
        values = []
        for bits in itertools.product((0, 1), repeat=4 * t):
            groups = [[1 - 2 * bits[g * t + i] for i in range(t)] for g in range(4)]
            values.append(density(groups, q, 5))
        den = 1
        for value in values:
            den = den * value.denominator // gcd(den, value.denominator)
        coeffs = fwht([int(v * den) for v in values])
        for S in range(1 << (4 * t)):
            sizes = [sum(1 for i in range(t) if S >> (g * t + i) & 1) for g in range(4)]
            need(F(coeffs[S], den << (4 * t)) == density_coefficient(sizes, q, 5),
                 f"square expansion coefficient mismatch at t={t}, S={S}")
        compare(record, "characters", 1 << (4 * t), f"square expansion t={t}")
        cross.append({"t": t, "characters": 1 << (4 * t), "mismatches": 0})
    report["expansion_cross_check"] = cross
    unc = []
    for record in doc["uncorrected_density_at_all_plus"]:
        t = record["t"]
        q = F(1, 16 * t)
        groups = [[1] * t for _ in range(4)]
        old = density(groups, q, 0)
        new = density(groups, q, 5)
        compare(record, "uncorrected_W_at_all_plus", str(old), f"square uncorrected t={t}")
        compare(record, "corrected_W_at_all_plus", str(new), f"square uncorrected t={t}")
        need(old < 0 < new, f"square t={t}: the uncorrected density is not negative "
                            f"while the corrected one is positive")
        unc.append({"t": t, "uncorrected": str(old), "corrected": str(new),
                    "uncorrected_negative": True, "corrected_positive": True})
    report["uncorrected_density_at_all_plus"] = unc
    tables = []
    for pair in doc["tables"]:
        entry = {}
        for kind in ("plain", "flipped"):
            record = pair[kind]
            t = record["order"]
            label = record["label"]
            q = F(1, 16 * t)
            scn = scn_spec(t)
            target = square_target(q)
            # the target really is the parity family with the stated moments
            tm = target_characters(target)
            need(tm[1] == tm[2] == tm[4] == tm[8] == -q, f"{label}: target means are not -q")
            need(tm[15] == 1, f"{label}: target parity is not perfect")
            eta = None
            if kind == "flipped":
                eta = frac(record["eta"])
                need(eta == q / 64, f"{label}: eta is not q/64")
                target = flip_target(target, 4, eta)
            atoms, den = product_witness(scn, q, 5, eta=eta)
            w = Witness(scn, atoms, den, target, label,
                        closed_form=product_characters(scn, q, 5, eta=eta))
            dense = w.dense_characters()
            need(all(dense(u) == w.closed_form(u) for u in range(1 << scn.n)),
                 f"{label}: closed-form characters disagree with the stored table")
            stats = check_common(w, record, label)
            if kind == "flipped":
                need(stats["full_support"], f"{label}: the flipped witness is not full support")
                fm = w.tm
                EA, EB, EAB, EABCD = fm[1], fm[2], fm[3], fm[15]
                pneg = (1 - EABCD) / 2
                value = max(EA, EB, EAB) + 4 * pneg
                inc = record["incompatibility"]
                for key, actual in (("EA", EA), ("EB", EB), ("E[AB]", EAB),
                                    ("E[ABCD]", EABCD), ("P(ABCD=-1)", pneg),
                                    ("value", value)):
                    compare(inc, key, str(actual), label)
                need(value < 0, f"{label}: the max-moment certificate is not negative")
                stats["incompatibility_value"] = str(value)
            stats["label"] = label
            entry[kind] = stats
        tables.append(entry)
    report["tables"] = tables
    cases = []
    for record in doc["P_q_validity"]["cases"]:
        q = frac(record["q"])
        atom = 1 - 6 * q + q * q
        compare(record, "8*P(0000) = 1-6q+q^2", str(atom), f"P_q validity at q={q}")
        compare(record, "is_probability_law", atom >= 0, f"P_q validity at q={q}")
        need((atom >= 0) == ((3 - q) ** 2 >= 8),
             f"P_q validity at q={q}: not equivalent to q <= 3 - 2 sqrt 2")
        need(min(square_target(q)) >= 0 if atom >= 0 else min(square_target(q)) < 0,
             f"P_q validity at q={q}: the table disagrees with the atom test")
        cases.append({"q": str(q), "1-6q+q^2": str(atom), "probability_law": atom >= 0})
    report["P_q_validity"] = {"threshold": "q <= 3 - 2 sqrt 2 tested exactly as (3-q)^2 >= 8",
                              "cases": cases}
    return report


def verify_triangle(doc):
    report = {}
    scan = []
    for record in doc["positivity_scan"]:
        t = record["t"]
        q = F(1, 16 * t)
        compare(record, "q", str(q), f"triangle density t={t}")
        best, covered = minimum_density(3, t, q, 4)
        compare(record, "minimum_W", str(best), f"triangle density t={t}")
        compare(record, "assignments", covered, f"triangle density t={t}")
        need(best >= F(3, 5), f"triangle density t={t}: minimum below 3/5")
        scan.append({"t": t, "q": str(q), "assignments": covered,
                     "minimum_W": str(best), "at_least_3/5": True})
    report["positivity_scan"] = scan
    unc = []
    for record in doc["uncorrected_density_at_all_plus"]:
        t = record["t"]
        q = F(1, 16 * t)
        groups = [[1] * t for _ in range(3)]
        old = density(groups, q, 0)
        new = density(groups, q, 4)
        compare(record, "uncorrected_W_at_all_plus", str(old), f"triangle uncorrected t={t}")
        compare(record, "corrected_W_at_all_plus", str(new), f"triangle uncorrected t={t}")
        unc.append({"t": t, "uncorrected": str(old), "corrected": str(new),
                    "uncorrected_negative": old < 0, "corrected_positive": new > 0})
    report["uncorrected_density_at_all_plus"] = unc
    records = []
    for pair in doc["records"]:
        entry = {}
        for kind in ("plain", "flipped"):
            record = pair[kind]
            t = record["order"]
            label = record["label"]
            q = F(1, 16 * t)
            compare(record, "q", str(q), label)
            scn = triangle_scenario(t)
            target = triangle_target(q)
            tm0 = target_characters(target)
            need(tm0[1] == tm0[2] == tm0[4] == -q, f"{label}: target means are not -q")
            need(tm0[7] == 1, f"{label}: target parity is not perfect")
            eta = None
            if kind == "flipped":
                eta = frac(record["eta"])
                need(eta == q / 192, f"{label}: eta is not q/192")
                target = flip_target(target, 3, eta)
            chi = product_characters(scn, q, 4, eta=eta)
            if scn.n <= 12:
                atoms, den = product_witness(scn, q, 4, eta=eta)
                w = Witness(scn, atoms, den, target, label, closed_form=chi)
                dense = w.dense_characters()
                need(all(dense(u) == chi(u) for u in range(1 << scn.n)),
                     f"{label}: closed-form characters disagree with the stored table")
                stats = check_common(w, record, label)
                if kind == "flipped":
                    need(stats["full_support"],
                         f"{label}: the flipped triangle witness is not full support")
            else:
                w = Witness(scn, {0: 1}, 1, target, label, closed_form=chi)
                nv = 3
                rows = scn.diagonal_rows()
                cells = 0
                for sel in range(1 << (nv * t)):
                    mask = 0
                    expected = F(1)
                    for r in range(t):
                        sub = (sel >> (nv * r)) & 7
                        for vtx in range(nv):
                            if sub >> vtx & 1:
                                mask |= 1 << rows[r][vtx]
                        expected *= w.tm[sub]
                    need(chi(mask) == expected, f"{label}: diagonal character {sel}")
                    cells += 1
                compare(record, "diagonal_characters_checked", cells, label)
                fams = w.check_ai_families(chi)
                compare(record, "ai_families_checked", fams["ai_families_checked"], label)
                compare(record, "injectable_set_characters",
                        fams["injectable_set_characters"], label)
                stats = {"method": "exact Fourier characters (no stored table)",
                         "copied_observations": scn.n,
                         "diagonal_characters_checked": cells, **fams}
            if kind == "plain":
                need(tm0[1] * tm0[2] * tm0[4] == -q ** 3,
                     f"{label}: the product of the target means is not -q^3")
                stats["parity_rigidity"] = {
                    "means": [str(tm0[1]), str(tm0[2]), str(tm0[4])],
                    "E[ABC]": str(tm0[7]),
                    "product_of_means": str(tm0[1] * tm0[2] * tm0[4]),
                    "compatible_requirement": "a parity-perfect compatible triangle law has "
                                              "means (st, su, tu) whose product is (stu)^2 >= 0",
                    "violated": tm0[1] * tm0[2] * tm0[4] < 0}
            else:
                fm = w.tm
                EA, EB, EC, EAB, EABC = fm[1], fm[2], fm[4], fm[3], fm[7]
                pneg = (1 - EABC) / 2
                m8 = max(EA, EB, EAB) + 8 * pneg
                m4 = max(EA, EB, EAB) + 4 * pneg
                inc = record["incompatibility"]
                for key, actual in (("EA", EA), ("EB", EB), ("EC", EC), ("E[AB]", EAB),
                                    ("E[ABC]", EABC), ("P(ABC=-1)", pneg),
                                    ("max_plus_8P", m8), ("max_plus_4P", m4),
                                    ("product_of_means", EA * EB * EC)):
                    compare(inc, key, str(actual), label)
                need(m8 < 0, f"{label}: the certified max-moment value is not negative")
                stats["incompatibility"] = {
                    "certified_inequality": "B4 section 6 equation (20) with constant 8",
                    "max_plus_8P": str(m8), "max_plus_8P_negative": True,
                    "max_plus_4P": str(m4), "max_plus_4P_negative": m4 < 0,
                    "means": [str(EA), str(EB), str(EC)],
                    "product_of_means": str(EA * EB * EC),
                    "parity_error_P(ABC=-1)": str(pneg)}
            stats["label"] = label
            entry[kind] = stats
        records.append(entry)
    report["records"] = records
    return report


def kbar(t, key, a):
    perms = sorted({p for p in itertools.permutations(key)})
    total = F(0)
    for p in perms:
        value = F(1)
        for g in range(4):
            value *= krawtchouk(t, p[g], a[g])
        total += value
    return total / len(perms)


def verify_low_order(doc):
    report = {}
    degrees = {}
    for key, record in doc["degree_systems"].items():
        t = int(key)
        nw = nw_degree_tuples(t)
        ai = ai_degree_tuples(t)
        predicted = sorted(k for k in itertools.product(range(t + 1), repeat=4)
                           if sum(k) % 2 == 0 and 2 * max(k) <= sum(k))
        need(ai == predicted,
             f"AI degree characterisation fails at t={t}")
        need(set(nw) <= set(ai), f"NW degrees not inside AI degrees at t={t}")
        compare(record, "nw_degree_tuples", len(nw), f"degrees t={t}")
        compare(record, "ai_degree_tuples", len(ai), f"degrees t={t}")
        compare(record, "ai_minus_nw", [list(k) for k in sorted(set(ai) - set(nw))],
                f"degrees t={t}")
        degrees[key] = {"nw": len(nw), "ai": len(ai),
                        "ai_minus_nw": [list(k) for k in sorted(set(ai) - set(nw))]}
    report["degree_systems"] = degrees
    primal = []
    for record in doc["count_primal"]:
        q = frac(record["q"])
        name = record["hierarchy"]
        label = f"{name} at q={q}"
        degs = nw_degree_tuples(2) if name == "NW_2" else ai_degree_tuples(2)
        compare(record, "moment_equations", len(degs) + 1, label)
        if not record["feasible"]:
            need(name == "AI_2" and q == F(3, 20),
                 f"{label}: only AI_2 at q=3/20 may be recorded infeasible")
            primal.append({"hierarchy": name, "q": str(q), "feasible": False})
            continue
        w = {tuple(a): frac(value) for a, value in record["count_weights"]}
        need(all(value >= 0 for value in w.values()), f"{label}: negative count weight")
        need(sum(w.values()) == 1, f"{label}: count weights are not normalized")
        for k in degs:
            need(count_moment(2, k, w) == (-q) ** (sum(k) // 2),
                 f"{label}: count moment {k} is wrong")
        compare(record, "nonzero_count_tuples", len(w), label)
        scn, atoms, den = expand_counts(2, w)
        target = square_target(q)
        table = record["expanded_table"]
        wit = Witness(scn, atoms, den, target, label)
        stats = check_common(wit, table, label,
                             ai_mode="both" if name == "AI_2" else "none",
                             require_ai=(name == "AI_2"))
        chi = wit.characters()
        failing = []
        for family in scn.ai_families():
            union = 0
            expected = F(1)
            for block in family:
                union |= scn.node_mask(block)
                expected *= wit.tm[scn.vertex_mask(block)]
            if chi(union) != expected:
                failing.append(([sorted(b) for b in family], str(chi(union)), str(expected)))
        compare(table, "ai_families_failing", len(failing), label)
        if name == "AI_2":
            need(not failing, f"{label}: an AI family prescription fails")
        primal.append({"hierarchy": name, "q": str(q), "feasible": True,
                       "nonzero_count_tuples": len(w),
                       "positive_atoms": stats["positive_atoms"],
                       "minimum_positive_atom": stats["minimum_positive_atom"],
                       "diagonal_cells_checked": table["diagonal_cells_checked"],
                       "ai_families_failing": len(failing),
                       "first_failing_ai_family": failing[0] if failing else None})
    report["count_primal"] = primal
    # B6 equation (16)
    keys = [(0, 0, 1, 1), (0, 0, 2, 2), (0, 2, 2, 2), (1, 1, 2, 2), (2, 2, 2, 2)]
    weights = [F(-24), F(-6), F(8), F(24), F(1)]
    values = [F(-3) + sum(c * kbar(2, k, a) for k, c in zip(keys, weights))
              for a in itertools.product(range(3), repeat=4)]
    need(max(values) == 0, "B6 (16): D(a) does not have maximum 0")
    b6 = doc["b6_equation_16"]
    compare(b6, "maximum", str(max(values)), "B6 (16)")
    for qtext, stored in b6["expectations"].items():
        q = frac(qtext)
        exp = F(-3) + sum(c * (-q) ** (sum(k) // 2) for k, c in zip(keys, weights))
        need(str(exp) == stored, f"B6 (16): expectation at q={q} is {exp} not {stored}")
    # the polynomial identity, coefficient by coefficient, without sympy
    lhs = [F(-3), F(0), F(0), F(0), F(0)]
    for k, c in zip(keys, weights):
        lhs[sum(k) // 2] += c * (-1) ** (sum(k) // 2)
    rhs = poly_mul([F(1), F(1)], [F(-3), F(27), F(-33), F(1)])
    rhs = rhs + [F(0)] * (len(lhs) - len(rhs))
    need(lhs == rhs[:len(lhs)] and all(x == 0 for x in rhs[len(lhs):]),
         f"B6 (16): E[D] = {lhs} does not equal (1+q)(q^3-33q^2+27q-3) = {rhs}")
    orbit_values = {}
    for a in itertools.product(range(3), repeat=4):
        value = F(-3) + sum(c * kbar(2, k, a) for k, c in zip(keys, weights))
        orbit = tuple(sorted(min(tuple(sorted(a)), tuple(sorted(2 - x for x in a)))))
        orbit_values.setdefault(orbit, set()).add(str(value))
    report["b6_equation_16"] = {
        "configurations": 81, "maximum": str(max(values)),
        "all_nonpositive": True,
        "orbits": {",".join(map(str, k)): sorted(v) for k, v in sorted(orbit_values.items())},
        "expectation_polynomial_coefficients": [str(x) for x in lhs],
        "identity_(1+q)(q^3-33q^2+27q-3)": True,
        "expectations": {k: v for k, v in b6["expectations"].items()}}
    # count-form dual found by the builder's LP
    duals = {}
    for name, tt, qq in (("ai2_dual_count_form", 2, F(3, 20)),
                         ("nw3_dual_count_form", 3, F(1, 10))):
        record = doc[name]
        den = record["denominator"]
        const = frac(record["constant"])
        coeff = {tuple(int(x) for x in k.split(",")): frac(v)
                 for k, v in record["coefficients"].items()}
        allowed = set(nw_degree_tuples(tt)) if name.startswith("nw") else set(ai_degree_tuples(tt))
        for k in coeff:
            for p in itertools.permutations(k):
                need(p in allowed,
                     f"{name}: degree {p} is not prescribed by the hierarchy")
        counts = list(itertools.product(range(tt + 1), repeat=4))
        vals = [const + sum(c * kbar(tt, k, a) for k, c in coeff.items()) for a in counts]
        need(max(vals) <= 0, f"{name}: the dual functional is positive somewhere")
        compare(record, "maximum_value", str(max(vals)), name)
        compare(record, "configurations", len(counts), name)
        exp = const + sum(c * (-qq) ** (sum(k) // 2) for k, c in coeff.items())
        need(exp > 0, f"{name}: the prescribed expectation is not positive")
        compare(record, "expectation", str(exp), name)
        duals[name] = {"configurations": len(counts), "maximum_value": str(max(vals)),
                       "expectation": str(exp), "denominator": den, "infeasible": True}
    report["count_form_duals"] = duals
    # full-table dual
    record = doc["ai2_dual_full_table"]
    q = F(3, 20)
    scn = square_scenario(2)
    prescribed = ai_prescribed(scn, square_target(q))
    compare(record, "ai_sets", len(prescribed), "full-table dual")
    coeff = orbit_expand(scn, [(int(r), int(v)) for r, v in record["orbit_coefficients"]])
    for mask in coeff:
        need(mask in prescribed, f"full-table dual: mask {mask} is not an AI set")
    dense = [0] * (1 << scn.n)
    for mask, value in coeff.items():
        dense[mask] = value
    functional = fwht(dense)
    need(max(functional) <= 0,
         f"full-table dual: the functional is positive at some assignment")
    den = record["denominator"]
    compare(record, "maximum_functional_value", str(F(max(functional), den)), "full-table dual")
    exp = sum(F(value, den) * prescribed[mask] for mask, value in coeff.items())
    need(exp > 0, "full-table dual: the prescribed expectation is not positive")
    compare(record, "expectation", str(exp), "full-table dual")
    compare(record, "atoms_checked", 1 << scn.n, "full-table dual")
    report["ai2_dual_full_table"] = {
        "ai_sets": len(prescribed), "atoms_checked": 1 << scn.n,
        "maximum_functional_value": str(F(max(functional), den)),
        "expectation": str(exp), "infeasible": True}
    # g root bracket
    g = [F(-3), F(27), F(-33), F(1)]

    def gval(x):
        return sum(c * x ** i for i, c in enumerate(g))

    lo = frac("1324743/10000000")
    hi = frac("1324744/10000000")
    need(gval(lo) * gval(hi) < 0, "g has no sign change on the recorded bracket")
    compare(doc["g_root_bracket"], "g(1324743/10000000)", str(gval(lo)), "g bracket")
    compare(doc["g_root_bracket"], "g(1324744/10000000)", str(gval(hi)), "g bracket")
    report["g_root_bracket"] = {"lower": str(gval(lo)), "upper": str(gval(hi)),
                                "sign_change": True}
    return report


# ==========================================================================
# 7. driver
# ==========================================================================


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_manifest():
    path = HERE / "MANIFEST.json"
    if not path.exists():
        return {"manifest": "absent"}
    doc = json.loads(path.read_text())
    checked = 0
    for name, entry in doc["files"].items():
        target = HERE / name
        need(target.exists(), f"MANIFEST lists a missing file: {name}")
        digest = sha256(target)
        need(digest == entry["sha256"],
             f"MANIFEST: {name} hashes to {digest}, not {entry['sha256']}")
        need(target.stat().st_size == entry["size"], f"MANIFEST: wrong size for {name}")
        checked += 1
    present = {p.name for p in HERE.iterdir() if p.is_file() and p.name != "MANIFEST.json"}
    need(present == set(doc["files"]),
         f"MANIFEST does not list exactly the directory contents: "
         f"{sorted(present ^ set(doc['files']))}")
    return {"files_hashed": checked, "all_match": True}


def main():
    documents = {}
    for name in ("five_path.json", "cycles.json", "square.json", "triangle.json",
                 "low_order_square.json"):
        documents[name] = json.loads((HERE / name).read_text())
    result = {
        "status": "PASS",
        "scope": "exact rational verification of the classification certificates; "
                 "no floating point anywhere in this file",
        "inputs_sha256": {name: sha256(HERE / name) for name in documents},
        "manifest": verify_manifest(),
        "five_path": verify_five_path(documents["five_path.json"]),
        "cycles": verify_cycles(documents["cycles.json"]),
        "square": verify_square(documents["square.json"]),
        "triangle": verify_triangle(documents["triangle.json"]),
        "low_order_square": verify_low_order(documents["low_order_square.json"]),
    }
    print(json.dumps(result, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
