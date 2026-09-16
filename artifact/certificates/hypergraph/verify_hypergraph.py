#!/usr/bin/env python3
"""Exact verifier for the hypergraph termination audit (2026-09-16), Section 7 of the
paper.  EXPLORATION.md and AUDIT.md below are the undistributed research notes that
the audit corrected; the "repaired" reconstruction is Theorem 7.9 of the paper.
Stored records under certificates/ are compared, never rewritten.

Run from the repository root:
  python3 -B artifact/certificates/hypergraph/verify_hypergraph.py

Standard library only (fractions, itertools, json, random, hashlib).  No
floating point enters any check.  Every failure raises CertificateError and the
process exits with status 1; the module refuses to run under -O/-OO.

What is checked
---------------
S1  {123,124}, binary, order 2.  Explicit order-2 tables (4096 atoms): four
    tables produced by random rational models (one with O_3 constant, so the
    listing is padded), two distinct extreme points of the Navascues-Wolfe LP
    for one law and one for a law with O_3 constant (certificates/lp_S1.json,
    discovered by discover_lp.py with scipy and rationalized with flint, then
    re-checked here from scratch), and the midpoint of the two vertices.  For
    each table: normalization, invariance under the copy-index symmetry group,
    diagonal law P^{(x)2}, every injectable prescription, O_3 independent of
    O_4.  LP tables must violate the model inequality
    Gamma(O_v^i = O_v^j = o) >= P(O_v = o)^2 for two copies sharing a source
    copy, so they are certified not to come from any model; model tables must
    satisfy it.  Both reconstruction procedures are then run (EXPLORATION.md
    Theorem 5.3, and the repaired Theorem of AUDIT.md), the identity (star) is
    checked for every argument, and the finite model built from the conditional
    table law is pushed forward and compared atom by atom with P.
S2  {123,34,45}, binary, order 4 (the split source 123 carries two leaves).
    Witnesses are given implicitly by genuine models and by a mixture of the
    tables of two different models of the same law; every marginal the
    reconstruction needs is computed exactly by factorized summation over
    source copies.  Two instances have zero-probability leaf patterns.
S3  {1234,3456}, binary.  Exploration bound: order 4 (run at order 4).
    Repaired bound: order 2 (run at order 2 with explicit response tables).
    Also mixtures of two distinct models at both orders.
S4  star {bc,bl} with |O_c| = 3.  Exploration bound 3, repaired bound 2.
S5  {123,14,24}: the witness of Theorem thm:cycle (m=3, t=2) transported
    through the pair set {1,2,4} by Lemma 2.4(3).  Strict positivity,
    invariance, diagonal law, all 94 injectable sets and all 971 AI sets
    (through exact Walsh-Hadamard characters), and the violation of
    Lemma lem:quantrigidity that makes the target incompatible.
S6  Exhaustive census of reduced scenarios on 3, 4, 5 observers up to
    isomorphism: no scenario is both peelable to hyper-double-stars and
    pair-obstructed; the undecided four-observer scenario is exactly K_4^(3);
    the five-observer undecided list is recorded; and the seven-observer
    scenario {b12,b23,b45,b56} is peelable but not a hyper-double-star.
Negative controls: perturbed table, wrong law, order below bound, witness of a
different law, non-HDS scenario, and four corrupted transport tables, each of
which must be rejected for the stated reason.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

if not __debug__:
    raise SystemExit("verify_hypergraph.py refuses to run under -O/-OO")

HERE = Path(__file__).resolve().parent
ZERO = F(0)
ONE = F(1)


class CertificateError(Exception):
    pass


def need(ok, message):
    if not ok:
        raise CertificateError(message)


def prod(xs):
    out = ONE
    for x in xs:
        out *= x
    return out


# ===========================================================================
# 1. hypergraph scenarios
# ===========================================================================


class Scenario:
    """Labelled sources covering a finite vertex set (Definition 1.1)."""

    def __init__(self, name, sources, alphabets=None):
        self.name = name
        self.labels = [lab for lab, _ in sources]
        need(len(set(self.labels)) == len(self.labels), f"{name}: labels repeat")
        self.src = {lab: frozenset(vs) for lab, vs in sources}
        need(all(self.src[l] for l in self.labels), f"{name}: empty source")
        self.V = sorted(set().union(*self.src.values()))
        alphabets = alphabets or {}
        self.alph = {v: alphabets.get(v, 2) for v in self.V}
        self.Ev = {v: tuple(l for l in self.labels if v in self.src[l]) for v in self.V}

    def deg(self, v):
        return len(self.Ev[v])

    def centres(self):
        return frozenset(v for v in self.V if self.deg(v) >= 2)

    def is_connected(self):
        seen = {self.V[0]}
        frontier = [self.V[0]]
        while frontier:
            v = frontier.pop()
            for e in self.Ev[v]:
                for w in self.src[e]:
                    if w not in seen:
                        seen.add(w)
                        frontier.append(w)
        return len(seen) == len(self.V)

    def atoms(self):
        return list(itertools.product(*[range(self.alph[v]) for v in self.V]))

    def copies(self, T):
        return [(v, idx) for v in self.V
                for idx in itertools.product(range(T), repeat=self.deg(v))]

    def parents(self, var):
        v, idx = var
        return tuple(zip(self.Ev[v], idx))

    def row(self, r):
        return [(v, (r,) * self.deg(v)) for v in self.V]

    def injectable_sets(self, T):
        """All injectable sets, from the description W, iota (Definition 1.2)."""
        out = set()
        for k in range(1, len(self.V) + 1):
            for W in itertools.combinations(self.V, k):
                EW = sorted({e for v in W for e in self.Ev[v]})
                for iota in itertools.product(range(T), repeat=len(EW)):
                    ass = dict(zip(EW, iota))
                    out.add(frozenset((v, tuple(ass[e] for e in self.Ev[v])) for v in W))
        return out


def marginal(scen, P, verts):
    pos = [scen.V.index(v) for v in verts]
    out = defaultdict(F)
    for atom, p in P.items():
        out[tuple(atom[i] for i in pos)] += p
    return out


def check_law(scen, P, label):
    need(set(P) == set(scen.atoms()), f"{label}: law not on the full atom set")
    need(all(p >= 0 for p in P.values()), f"{label}: negative atom")
    need(sum(P.values()) == 1, f"{label}: law not normalized")


# ===========================================================================
# 2. finite models, and witnesses given by models (implicitly) or tables
# ===========================================================================


class Model:
    """Finite model: a law per source, a response kernel per vertex that
    receives ONLY the values of the sources at that vertex."""

    def __init__(self, scen, source_laws, responses):
        self.scen = scen
        self.source_laws = source_laws
        self.responses = responses
        for e in scen.labels:
            law = source_laws[e]
            need(all(p >= 0 for _, p in law) and sum(p for _, p in law) == 1,
                 f"{scen.name}: source law of {e} invalid")
        self._cache = {}

    def kernel(self, v, vals):
        key = (v, vals)
        if key not in self._cache:
            d = self.responses[v](vals)
            need(all(p >= 0 for p in d.values()) and sum(d.values()) == 1,
                 f"{self.scen.name}: response of {v} invalid")
            self._cache[key] = d
        return self._cache[key]

    def law(self):
        s = self.scen
        P = {a: ZERO for a in s.atoms()}
        for combo in itertools.product(*[self.source_laws[e] for e in s.labels]):
            w = prod(p for _, p in combo)
            if w == 0:
                continue
            val = {e: c[0] for e, c in zip(s.labels, combo)}
            dists = [self.kernel(v, tuple(val[e] for e in s.Ev[v])).items() for v in s.V]
            for choice in itertools.product(*dists):
                P[tuple(o for o, _ in choice)] += w * prod(p for _, p in choice)
        return P


class ModelWitness:
    """The order-T table of a model run on the inflated source family,
    accessed through exact marginals Gamma(fixed and free = beta)."""

    def __init__(self, model, T):
        self.model = model
        self.T = T
        self.memo = {}

    def joint(self, fixed, free):
        s = self.model.scen
        factors = [(var, val) for var, val in fixed.items()] + [(var, None) for var in free]
        parent = {}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for var, _ in factors:
            ps = s.parents(var)
            for c in ps:
                parent.setdefault(c, c)
            for c in ps[1:]:
                ra, rb = find(ps[0]), find(c)
                if ra != rb:
                    parent[ra] = rb
        comps = defaultdict(list)
        for f in factors:
            comps[find(s.parents(f[0])[0])].append(f)
        scalar = ONE
        free_parts = []
        for fs in comps.values():
            if all(val is not None for _, val in fs):
                key = tuple(sorted(fs))
                if key not in self.memo:
                    self.memo[key] = self._component(fs)[()]
                scalar *= self.memo[key]
                if scalar == 0:
                    break
            else:
                free_parts.append(self._component(fs))
        result = {(): scalar}
        order = []
        for part in free_parts:
            (vars_, table) = part["__vars__"], part["__table__"]
            new = {}
            for k1, p1 in result.items():
                for k2, p2 in table.items():
                    new[k1 + k2] = p1 * p2
            result = new
            order.extend(vars_)
        if scalar == 0:
            return {tuple(b): ZERO for b in itertools.product(
                *[range(s.alph[v]) for v, _ in free])}
        pos = [order.index(var) for var in free]
        out = defaultdict(F)
        for k, p in result.items():
            out[tuple(k[i] for i in pos)] += p
        for b in itertools.product(*[range(s.alph[v]) for v, _ in free]):
            out.setdefault(b, ZERO)
        return dict(out)

    def _component(self, fs):
        s = self.model.scen
        copies = sorted({c for var, _ in fs for c in s.parents(var)})
        idx = {c: i for i, c in enumerate(copies)}
        sched = defaultdict(list)
        for var, val in fs:
            sched[max(idx[c] for c in s.parents(var))].append((var, val))
        free_order = [var for k in range(len(copies)) for var, val in sched[k] if val is None]
        acc = defaultdict(F)
        assign = {}

        def rec(k, w, fd):
            if k == len(copies):
                for key, p in fd.items():
                    acc[key] += w * p
                return
            e, _ = copies[k]
            for value, p in self.model.source_laws[e]:
                if p == 0:
                    continue
                assign[copies[k]] = value
                w2 = w * p
                fd2 = fd
                ok = True
                for var, val in sched[k]:
                    d = self.model.kernel(var[0], tuple(assign[c] for c in s.parents(var)))
                    if val is not None:
                        pr = d.get(val, ZERO)
                        if pr == 0:
                            ok = False
                            break
                        w2 *= pr
                    else:
                        fd2 = {key + (o,): q * po for key, q in fd2.items()
                               for o, po in d.items() if po != 0}
                if ok:
                    rec(k + 1, w2, fd2)

        rec(0, ONE, {(): ONE})
        if not free_order:
            return {(): acc.get((), ZERO)}
        return {"__vars__": free_order, "__table__": dict(acc)}


class TableWitness:
    """An explicit table on all copied observations."""

    def __init__(self, scen, T, table):
        self.scen = scen
        self.T = T
        self.vars = scen.copies(T)
        self.pos = {v: i for i, v in enumerate(self.vars)}
        self.table = table

    def joint(self, fixed, free):
        fp = [(self.pos[v], val) for v, val in fixed.items()]
        fr = [self.pos[v] for v in free]
        out = defaultdict(F)
        for atom, p in self.table.items():
            if p and all(atom[i] == val for i, val in fp):
                out[tuple(atom[i] for i in fr)] += p
        for b in itertools.product(*[range(self.scen.alph[v]) for v, _ in free]):
            out.setdefault(b, ZERO)
        return dict(out)


class MixWitness:
    def __init__(self, parts):
        self.parts = parts
        need(sum(w for w, _ in parts) == 1, "mixture weights")

    def joint(self, fixed, free):
        out = defaultdict(F)
        for w, wit in self.parts:
            for k, p in wit.joint(fixed, free).items():
                out[k] += w * p
        return dict(out)


def model_table(model, T):
    s = model.scen
    vars_ = s.copies(T)
    copies = [(e, m) for e in s.labels for m in range(T)]
    table = defaultdict(F)
    for combo in itertools.product(*[model.source_laws[e] for e, _ in copies]):
        w = prod(p for _, p in combo)
        if w == 0:
            continue
        val = {c: x[0] for c, x in zip(copies, combo)}
        dist = {(): w}
        for var in vars_:
            d = model.kernel(var[0], tuple(val[c] for c in s.parents(var)))
            dist = {k + (o,): p * q for k, p in dist.items() for o, q in d.items() if q}
        for k, p in dist.items():
            table[k] += p
    return dict(table)


def check_nw_table(scen, T, table, P, label):
    vars_ = scen.copies(T)
    pos = {v: i for i, v in enumerate(vars_)}
    need(all(p >= 0 for p in table.values()), f"{label}: negative table entry")
    need(sum(table.values()) == 1, f"{label}: table not normalized")
    gens = [tuple([1, 0] + list(range(2, T)))]
    if T > 2:
        gens.append(tuple(list(range(1, T)) + [0]))
    for e in scen.labels:
        for g in gens:
            perm = [pos[(v, tuple(g[i] if scen.Ev[v][k] == e else i
                                  for k, i in enumerate(idx)))] for v, idx in vars_]
            for atom, p in table.items():
                image = [None] * len(atom)
                for i, x in enumerate(atom):
                    image[perm[i]] = x
                need(table.get(tuple(image), ZERO) == p,
                     f"{label}: table not invariant under source {e}")
    rows = [[pos[var] for var in scen.row(r)] for r in range(T)]
    diag = defaultdict(F)
    for atom, p in table.items():
        diag[tuple(atom[i] for r in rows for i in r)] += p
    for combo in itertools.product(scen.atoms(), repeat=T):
        key = tuple(x for a in combo for x in a)
        need(diag.get(key, ZERO) == prod(P[a] for a in combo),
             f"{label}: diagonal law is not P^(x){T}")


def failing_injectable(scen, T, table, P):
    """Return an injectable set whose marginal differs from P_{pi(S)}, or None."""
    wit = TableWitness(scen, T, table)
    for S in sorted(scen.injectable_sets(T), key=lambda S: (len(S), sorted(S))):
        S = sorted(S)
        got = wit.joint({}, S)
        want = marginal(scen, P, [v for v, _ in S])
        if any(got[k] != want.get(k, ZERO) for k in got):
            return S
    return None


def model_inequality_violation(scen, T, table, P):
    """Two copies at one vertex that share some but not all source copies are
    conditionally i.i.d. given the shared copies in any model table, hence
    Gamma(both = o) >= P_v(o)^2.  Return a violated instance, or None."""
    wit = TableWitness(scen, T, table)
    for v in scen.V:
        if scen.deg(v) < 2:
            continue
        idxs = list(itertools.product(range(T), repeat=scen.deg(v)))
        pv = marginal(scen, P, [v])
        for i1, i2 in itertools.combinations(idxs, 2):
            if not any(a == b for a, b in zip(i1, i2)):
                continue
            j = wit.joint({}, [(v, i1), (v, i2)])
            for o in range(scen.alph[v]):
                if j[(o, o)] < pv[(o,)] ** 2:
                    return (v, i1, i2, o, j[(o, o)], pv[(o,)] ** 2)
    return None


# ===========================================================================
# 3. the reconstruction procedures
# ===========================================================================


def reconstruct(scen, T, P, wit, variant, y, mode, label):
    """Run the reconstruction of a hyper-double-star and return the order bound
    it needs.  variant = 'exploration' lists the leaf block of every source
    (EXPLORATION.md Theorem 5.3); variant = 'repaired' lists only split sources
    and conditions on constant values for sources containing every centre
    (AUDIT.md Theorem R).  mode = 'explicit' builds the finite model with a
    central source carrying the response tables and pushes it forward;
    mode = 'marginal' pushes forward through the per-argument marginals of the
    table law, which is all the observed law of that model depends on."""
    Z = scen.centres()
    need(Z <= scen.src[y], f"{label}: Z not inside y")
    need(scen.is_connected(), f"{label}: reconstruction run on a connected scenario only")
    L = {e: tuple(sorted(scen.src[e] - Z)) for e in scen.labels}
    if variant == "exploration":
        inner = []
        listed = list(scen.labels)
    else:
        inner = [e for e in scen.labels if Z <= scen.src[e]]
        listed = [e for e in scen.labels if e not in inner]
        need(all(scen.src[e] & Z for e in listed), f"{label}: outer source in a connected HDS")
        if y in inner:
            inner.remove(y)
            inner.insert(0, y)
    size = {e: prod(F(scen.alph[l]) for l in L[e]) for e in scen.labels}
    bound = int(max([F(2)] + [size[e] for e in listed]))
    need(T >= bound, f"{label}: order {T} below the bound {bound}")

    PL = {e: marginal(scen, P, list(L[e])) for e in scen.labels}
    supp = {e: sorted(k for k, p in PL[e].items() if p > 0) for e in scen.labels}
    # step (i): the leaf law is the product of the block laws (Lemma 1.5)
    allL = [l for e in scen.labels for l in L[e]]
    PLall = marginal(scen, P, allL)
    for combo in itertools.product(*[list(PL[e]) for e in scen.labels]):
        key = tuple(x for c in combo for x in c)
        need(PLall.get(key, ZERO) == prod(PL[e][c] for e, c in zip(scen.labels, combo)),
             f"{label}: leaf blocks not independent")
    # step (ii): listings with padding, positions chosen coordinatewise
    xs = {e: supp[e] + [supp[e][0]] * (T - len(supp[e])) for e in listed}
    posf = {e: {val: xs[e].index(val) for val in supp[e]} for e in listed}
    padded = any(len(supp[e]) < T for e in listed)
    # the copied centre observations F_z(xi_z)
    varz = {}
    for z in sorted(Z):
        need(all(e in inner or e in listed for e in scen.Ev[z]), f"{label}: centre reads outer")
        Lz = [e for e in listed if z in scen.src[e]]
        for xi in itertools.product(*[supp[e] for e in Lz]):
            d = dict(zip(Lz, xi))
            varz[(z, xi)] = (z, tuple(posf[e][d[e]] if e in d else 0 for e in scen.Ev[z]))
    allvars = sorted(set(varz.values()))
    need(len(allvars) == len(varz), f"{label}: two table entries share a copy")
    zlist = sorted(Z)
    uvals = list(itertools.product(*[supp[e] for e in inner]))
    mu = {}
    for u in uvals:
        E = {}
        for e, ue in zip(inner, u):
            for m in range(T):
                for l, val in zip(L[e], ue):
                    E[(l, (m,))] = val
        for e in listed:
            for m in range(T):
                for l, val in zip(L[e], xs[e][m]):
                    E[(l, (m,))] = val
        GE = wit.joint(E, [])[()]
        want = prod(PL[e][ue] ** T for e, ue in zip(inner, u)) * \
            prod(PL[e][xs[e][m]] for e in listed for m in range(T))
        need(GE == want and GE > 0, f"{label}: Gamma(E_u) wrong or zero")
        if mode == "explicit":
            joint = wit.joint(E, allvars)
            mu[u] = {k: p / GE for k, p in joint.items() if p}
        # identity (star) for every argument
        for xil in itertools.product(*[supp[e] for e in listed]):
            dxi = dict(zip(listed, xil))
            vs = [varz[(z, tuple(dxi[e] for e in listed if z in scen.src[e]))] for z in zlist]
            if mode == "explicit":
                got = defaultdict(F)
                ip = [allvars.index(v) for v in vs]
                for k, p in mu[u].items():
                    got[tuple(k[i] for i in ip)] += p
            else:
                got = {k: p / GE for k, p in wit.joint(E, vs).items()}
                mu[(u, xil)] = got
            cond = {**dict(zip(inner, u)), **dxi}
            den = prod(PL[e][cond[e]] for e in scen.labels if e in cond)
            for beta in itertools.product(*[range(scen.alph[z]) for z in zlist]):
                atom = []
                num = ZERO
                # P(O_Z = beta, O_L = xi) with xi on inner and listed blocks
                fixedv = {}
                for e in scen.labels:
                    for l, val in zip(L[e], cond[e]):
                        fixedv[l] = val
                for z, b in zip(zlist, beta):
                    fixedv[z] = b
                num = sum(p for a, p in P.items()
                          if all(a[scen.V.index(v)] == val for v, val in fixedv.items()))
                need(got.get(beta, ZERO) == num / den,
                     f"{label}: identity (star) fails at u={u}, xi={xil}, beta={beta}")

    # step (iv): the model and its observed law
    if mode == "explicit":
        others = [e for e in inner if e != y]
        uprime = list(itertools.product(*[supp[e] for e in others]))
        ypart = [(xi_y, ) for xi_y in supp[y]]
        yvals = []
        for (xi_y,) in ypart:
            thetas_by_u = []
            for up in uprime:
                u = ((xi_y,) + up) if y in inner else up
                thetas_by_u.append(list(mu[u].items()))
            for choice in itertools.product(*thetas_by_u):
                yvals.append(((xi_y, tuple(k for k, _ in choice)),
                              PL[y][xi_y] * prod(p for _, p in choice)))
        need(len(yvals) <= 200000, f"{label}: central source too large")
        source_laws = {}
        for e in scen.labels:
            if e == y:
                source_laws[e] = yvals
            else:
                source_laws[e] = [(xi, PL[e][xi]) for xi in supp[e]]
        vpos = {v: i for i, v in enumerate(allvars)}

        def leaf_resp(l, e):
            def r(vals):
                val = vals[0]
                xi = val[0] if e == y else val
                return {xi[L[e].index(l)]: ONE}
            return r

        def centre_resp(z):
            def r(vals):
                got = dict(zip(scen.Ev[z], vals))
                xi = {e: (got[e][0] if e == y else got[e]) for e in scen.Ev[z]}
                up = tuple(xi[e] for e in others)
                theta = got[y][1][uprime.index(up)]
                xz = tuple(xi[e] for e in listed if z in scen.src[e])
                return {theta[vpos[varz[(z, xz)]]]: ONE}
            return r

        responses = {}
        for v in scen.V:
            if v in Z:
                responses[v] = centre_resp(v)
            else:
                (e,) = scen.Ev[v]
                responses[v] = leaf_resp(v, e)
        Q = Model(scen, source_laws, responses).law()
        recon = Model(scen, source_laws, responses)
    else:
        Q = {a: ZERO for a in scen.atoms()}
        for u in uvals:
            for xil in itertools.product(*[supp[e] for e in listed]):
                cond = {**dict(zip(inner, u)), **dict(zip(listed, xil))}
                w = prod(PL[e][cond[e]] for e in scen.labels)
                for beta, p in mu[(u, xil)].items():
                    a = [None] * len(scen.V)
                    for e in scen.labels:
                        for l, val in zip(L[e], cond[e]):
                            a[scen.V.index(l)] = val
                    for z, b in zip(zlist, beta):
                        a[scen.V.index(z)] = b
                    Q[tuple(a)] += w * p
        recon = None
    for a in scen.atoms():
        need(Q[a] == P[a], f"{label}: reconstructed model misses P at {a}")
    return {"bound": bound, "padded": padded, "model": recon}


# ===========================================================================
# 4. random rational models
# ===========================================================================


def random_model(scen, rng, latent, D=9, overrides=None):
    overrides = overrides or {}
    laws = {}
    for e in scen.labels:
        k = latent.get(e, 2)
        w = [rng.randint(1, D) for _ in range(k)]
        laws[e] = [(i, F(wi, sum(w))) for i, wi in enumerate(w)]
    responses = {}
    for v in scen.V:
        if v in overrides:
            responses[v] = overrides[v]
            continue
        tab = {}
        for vals in itertools.product(*[range(latent.get(e, 2)) for e in scen.Ev[v]]):
            w = [rng.randint(0, D) for _ in range(scen.alph[v])]
            if sum(w) == 0:
                w[0] = 1
            tab[vals] = {o: F(wi, sum(w)) for o, wi in enumerate(w)}
        responses[v] = (lambda tab: (lambda vals: tab[vals]))(tab)
    return Model(scen, laws, responses)


# ===========================================================================
# 5. certificate runs
# ===========================================================================

LOG = []


def log(msg):
    LOG.append(msg)
    print(msg, flush=True)


def run_S1():
    s = Scenario("S1={123,124}", [("a", (1, 2, 3)), ("b", (1, 2, 4))])
    T = 2
    rng = random.Random(20260916)
    instances = []
    for k in range(3):
        m = random_model(s, rng, {"a": 3, "b": 2} if k != 1 else {"a": 2, "b": 3})
        instances.append((f"model#{k}", m.law(), model_table(m, T), False))
    m = random_model(s, rng, {"a": 2, "b": 2}, overrides={3: lambda vals: {0: ONE}})
    instances.append(("model#3 (O_3 constant)", m.law(), model_table(m, T), False))
    data = json.loads((HERE / "certificates" / "lp_S1.json").read_text())
    lp = {}
    for rec in data["instances"]:
        P = {tuple(int(c) for c in k): F(v) for k, v in rec["law"].items()}
        table = {tuple(int(c) for c in k): F(v) for k, v in rec["table"].items()}
        lp[rec["name"]] = (P, table)
        instances.append((f"LP vertex {rec['name']}", P, table, True))
    (PA1, TA1), (PA2, TA2) = lp["A1"], lp["A2"]
    need(PA1 == PA2 and TA1 != TA2, "S1: LP vertices A1, A2 must share the law and differ")
    keys = set(TA1) | set(TA2)
    mixed = {k: (TA1.get(k, ZERO) + TA2.get(k, ZERO)) / 2 for k in keys}
    instances.append(("LP mixture (A1+A2)/2", PA1, mixed, True))
    for name, P, table, from_lp in instances:
        label = f"S1 {name}"
        check_law(s, P, label)
        check_nw_table(s, T, table, P, label)
        pr = marginal(s, P, [3, 4])
        p3, p4 = marginal(s, P, [3]), marginal(s, P, [4])
        need(all(pr[(i, j)] == p3[(i,)] * p4[(j,)] for i in range(2) for j in range(2)),
             f"{label}: O_3 and O_4 not independent (Proposition 5.1)")
        need(failing_injectable(s, T, table, P) is None, f"{label}: injectable prescription fails")
        bad = model_inequality_violation(s, T, table, P)
        if from_lp:
            need(bad is not None, f"{label}: LP table satisfies the model inequality")
        else:
            need(bad is None, f"{label}: model table violates the model inequality")
        wit = TableWitness(s, T, table)
        r1 = reconstruct(s, T, P, wit, "exploration", "a", "explicit", label + " [exploration]")
        r2 = reconstruct(s, T, P, wit, "repaired", "a", "explicit", label + " [repaired]")
        need(r1["bound"] == 2 and r2["bound"] == 2, f"{label}: order bounds")
        log(f"  PASS {label}: exact NW_2 table; both reconstructions reproduce P"
            + (" (listing padded)" if r1["padded"] else "")
            + (f"; not a model table: Gamma(O_{bad[0]}^{bad[1]}=O_{bad[0]}^{bad[2]}={bad[3]}) = {bad[4]} < {bad[5]}" if bad else ""))
    return len(instances)


def run_S2():
    s = Scenario("S2={123,34,45}", [("a", (1, 2, 3)), ("y", (3, 4)), ("c", (4, 5))])
    rng = random.Random(1602)
    count = 0
    specs = [
        ("model#0", {"a": 2, "y": 2, "c": 2}, None),
        ("model#1", {"a": 3, "y": 2, "c": 2}, None),
        ("model#2 (P_12(1,0)=0)", {"a": 3, "y": 2, "c": 2},
         {1: lambda vals: {int(vals[0] >= 2): ONE}, 2: lambda vals: {int(vals[0] >= 1): ONE}}),
    ]
    for name, lat, ov in specs:
        m = random_model(s, rng, lat, overrides=ov)
        P = m.law()
        label = f"S2 {name}"
        check_law(s, P, label)
        wit = ModelWitness(m, 4)
        r = reconstruct(s, 4, P, wit, "repaired", "y", "explicit", label + " [repaired=exploration]")
        need(r["bound"] == 4, f"{label}: bound")
        r0 = reconstruct(s, 4, P, wit, "exploration", "y", "explicit", label + " [exploration]")
        need(r0["bound"] == 4, f"{label}: bound")
        log(f"  PASS {label}: order-4 model witness; reconstruction reproduces P"
            + (" (listing padded)" if r["padded"] else ""))
        count += 1
        if name == "model#1":
            # a second, different model of the same law: the reconstructed one
            m2 = r["model"]
            need(m2.law() == P, f"{label}: second model law")
            mix = MixWitness([(F(1, 2), wit), (F(1, 2), ModelWitness(m2, 4))])
            r3 = reconstruct(s, 4, P, mix, "repaired", "y", "explicit", label + " mixture")
            log(f"  PASS {label} mixture of two distinct models' order-4 tables: reconstruction reproduces P")
            count += 1
    return count


def run_S3():
    s = Scenario("S3={1234,3456}", [("y", (1, 2, 3, 4)), ("b", (3, 4, 5, 6))])
    rng = random.Random(3456)
    count = 0
    for k, lat in enumerate([{"y": 2, "b": 2}, {"y": 3, "b": 2}]):
        m = random_model(s, rng, lat)
        P = m.law()
        label = f"S3 model#{k}"
        check_law(s, P, label)
        rr = reconstruct(s, 2, P, ModelWitness(m, 2), "repaired", "y", "explicit", label + " [repaired, order 2]")
        need(rr["bound"] == 2, f"{label}: repaired bound")
        try:
            reconstruct(s, 2, P, ModelWitness(m, 2), "exploration", "y", "marginal", label)
            raise CertificateError(f"{label}: exploration procedure accepted order 2")
        except CertificateError as exc:
            need("below the bound 4" in str(exc), str(exc))
        re = reconstruct(s, 4, P, ModelWitness(m, 4), "exploration", "y", "marginal", label + " [exploration, order 4]")
        need(re["bound"] == 4, f"{label}: exploration bound")
        log(f"  PASS {label}: repaired reconstruction at order 2 and exploration reconstruction at order 4 both reproduce P")
        count += 1
        if k == 0:
            m2 = rr["model"]
            need(m2.law() == P, f"{label}: second model law")
            for T, variant, mode in [(2, "repaired", "explicit"), (4, "exploration", "marginal")]:
                mix = MixWitness([(F(1, 3), ModelWitness(m, T)), (F(2, 3), ModelWitness(m2, T))])
                reconstruct(s, T, P, mix, variant, "y", mode, f"{label} mixture order {T}")
                log(f"  PASS {label} mixture of two distinct models at order {T} [{variant}]: reproduces P")
                count += 1
    return count


def run_S4():
    s = Scenario("S4=star{bc,bl}", [("y", ("b", "c")), ("f", ("b", "l"))], {"c": 3})
    rng = random.Random(44)
    count = 0
    for k in range(2):
        m = random_model(s, rng, {"y": 3, "f": 2})
        P = m.law()
        label = f"S4 model#{k}"
        check_law(s, P, label)
        r = reconstruct(s, 2, P, ModelWitness(m, 2), "repaired", "y", "explicit", label)
        need(r["bound"] == 2, f"{label}: repaired bound")
        try:
            reconstruct(s, 2, P, ModelWitness(m, 2), "exploration", "y", "explicit", label)
            raise CertificateError(f"{label}: exploration accepted order 2")
        except CertificateError as exc:
            need("below the bound 3" in str(exc), str(exc))
        reconstruct(s, 3, P, ModelWitness(m, 3), "exploration", "y", "explicit", label + " order 3")
        log(f"  PASS {label}: |O_c|=3; repaired reconstruction at order 2, exploration at order 3")
        count += 1
    return count


# ---------------------------------------------------------------------------
# S5: nontermination transported through a pair set
# ---------------------------------------------------------------------------


def fwht(vals):
    a = list(vals)
    h = 1
    while h < len(a):
        for i in range(0, len(a), 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a


def run_S5(target_q_scale=ONE, noiseless_table=False, skip_diagonal=False, correlated_fair=False):
    s = Scenario("S5={123,14,24}", [("a", (1, 2, 3)), ("b", (1, 4)), ("c", (2, 4))])
    T = 2
    m = 3
    q = F(1, 4 * m * m * T * T)
    eta = q / (32 * m)
    need(q == F(1, 144) and eta == F(1, 13824), "S5 parameters")
    vars_ = s.copies(T)
    n = len(vars_)
    need(n == 14, "S5 variable count")
    pos = {v: i for i, v in enumerate(vars_)}
    # cycle labels: S_0 = a (between 1 and 2), S_1 = c (between 2 and 4), S_2 = b (between 4 and 1)
    cyc = {"a": 0, "c": 1, "b": 2}
    N = m * T
    coords = [(w, i) for w in range(m) for i in range(T)]

    def H(sv):
        tot = ZERO
        for k in range(0, N + 1, 2):
            for S in itertools.combinations(range(N), k):
                tot += (-q) ** (k // 2) * prod(F(sv[i]) for i in S)
        return tot / 2 ** N

    clean = [ZERO] * (1 << n)
    hmin = None
    for sv in itertools.product((1, -1), repeat=N):
        h = H(sv)
        need(h > 0, "S5 auxiliary density not positive")
        hmin = h if hmin is None else min(hmin, h)
        sig = dict(zip(coords, sv))
        base = 0
        for var in vars_:
            v, idx = var
            if v == 3:
                continue
            sign = prod(F(sig[(cyc[e], i)]) for e, i in zip(s.Ev[v], idx))
            if sign < 0:
                base |= 1 << pos[var]
        fair = [pos[(3, (0,))], pos[(3, (1,))]]
        for bits in (((0, 0), (1, 1)) if correlated_fair else itertools.product((0, 1), repeat=2)):
            atom = base
            for p_, b in zip(fair, bits):
                atom |= b << p_
            clean[atom] += h / (2 if correlated_fair else 4)
    need(sum(clean) == 1, "S5 clean table not normalized")
    chi = fwht(clean)
    noisy_mask = sum(1 << pos[v] for v in vars_ if v[0] != 3)
    r = 1 - 2 * eta
    if not noiseless_table:
        chi = [c * r ** bin(F_ & noisy_mask).count("1") for F_, c in enumerate(chi)]
    table = [x / (1 << n) for x in fwht(chi)]
    need(sum(table) == 1, "S5 table not normalized")
    need(noiseless_table or correlated_fair or all(x > 0 for x in table), "S5 table not strictly positive")

    # the target: T_eta^{(x)3} Pi(-q,-q,-q) on (1,2,4), fair bit at 3; bit 1 = sign -1
    tri = {}
    for bits in itertools.product((0, 1), repeat=3):
        sg = [1 - 2 * b for b in bits]
        tri[bits] = (1 + (-q * target_q_scale) * sum(sg)) / 4 if sg[0] * sg[1] * sg[2] == 1 else ZERO
    need(sum(tri.values()) == 1 and all(p >= 0 for p in tri.values()), "S5 Pi law")
    ntri = defaultdict(F)
    for bits, p in tri.items():
        for flips in itertools.product((0, 1), repeat=3):
            w = prod(eta if f else 1 - eta for f in flips)
            ntri[tuple(b ^ f for b, f in zip(bits, flips))] += p * w
    P = {}
    for a in s.atoms():  # order 1,2,3,4
        P[a] = ntri[(a[0], a[1], a[3])] / 2
    check_law(s, P, "S5 target")
    need(all(p > 0 for p in P.values()), "S5 target not strictly positive")

    def charP(verts):
        idx = [s.V.index(v) for v in verts]
        return sum(p * (-1) ** sum(a[i] for i in idx) for a, p in P.items())

    # character closed form of thm:cycle for m=3
    for k in range(1, 4):
        for Fs in itertools.combinations((1, 2, 4), k):
            want = (-q * target_q_scale) ** (1 if k < 3 else 0) * r ** k
            need(charP(list(Fs)) == want, "S5 target characters")

    # invariance under the transposition of each source's copies
    for e in s.labels:
        perm = [pos[(v, tuple(1 - i if s.Ev[v][k] == e else i for k, i in enumerate(idx)))]
                for v, idx in vars_]
        for atom in range(1 << n):
            image = 0
            for i in range(n):
                if atom >> i & 1:
                    image |= 1 << perm[i]
            need(table[image] == table[atom], f"S5 not invariant under {e}")
    # diagonal
    rows = [[pos[v] for v in s.row(rr)] for rr in range(T)]
    diag = defaultdict(F)
    for atom in range(1 << n):
        diag[tuple((atom >> i) & 1 for rw in rows for i in rw)] += table[atom]
    for a1 in s.atoms():
        for a2 in s.atoms():
            need(skip_diagonal or diag[a1 + a2] == P[a1] * P[a2], "S5 diagonal law")
    chi_final = fwht(table)
    inj = s.injectable_sets(T)
    parents = [set(s.parents(v)) for v in vars_]
    n_inj = 0
    for S in inj:
        mask = sum(1 << pos[v] for v in S)
        need(chi_final[mask] == charP([v for v, _ in S]), f"S5 injectable set {sorted(S)}")
        n_inj += 1
    n_ai = 0
    for mask in range(1, 1 << n):
        members = [i for i in range(n) if mask >> i & 1]
        comp = {i: i for i in members}

        def find(x):
            while comp[x] != x:
                comp[x] = comp[comp[x]]
                x = comp[x]
            return x

        for i, j in itertools.combinations(members, 2):
            if parents[i] & parents[j]:
                comp[find(i)] = find(j)
        groups = defaultdict(list)
        for i in members:
            groups[find(i)].append(vars_[i])
        if all(frozenset(g) in inj for g in groups.values()):
            n_ai += 1
            want = prod(charP([v for v, _ in g]) for g in groups.values())
            need(chi_final[mask] == want, f"S5 AI set {members}")
    # incompatibility: Lemma lem:quantrigidity on the trace marginal
    W = charP([1, 2, 4])
    means = [charP([v]) for v in (1, 2, 4)]
    need(max(means) < -4 * (1 - W), "S5 target does not violate quantitative rigidity")
    log(f"  PASS S5 {{123,14,24}} order 2: 16384-atom strictly positive table, invariant, "
        f"diagonal P^(x)2, {n_inj} injectable sets and {n_ai} AI sets exact; "
        f"max mean {max(means)} < -4(1-W) = {-4 * (1 - W)}")
    return {"injectable": n_inj, "ai_sets": n_ai, "q": str(q), "eta": str(eta),
            "min_mean": str(max(means)), "rigidity_rhs": str(-4 * (1 - W)),
            "table_sha256": hashlib.sha256(
                "\n".join(str(x) for x in table).encode()).hexdigest()}


# ---------------------------------------------------------------------------
# S6: combinatorial census of reduced scenarios (exact, exhaustive)
# ---------------------------------------------------------------------------


def _antichains(n):
    subs = sorted(range(1, 1 << n), key=lambda m: -bin(m).count("1"))
    out = []

    def rec(i, chosen):
        if i == len(subs):
            cov = 0
            for c in chosen:
                cov |= c
            if cov == (1 << n) - 1:
                out.append(tuple(sorted(chosen)))
            return
        rec(i + 1, chosen)
        m = subs[i]
        if all((m & c) != m and (m & c) != c for c in chosen):
            rec(i + 1, chosen + [m])

    rec(0, [])
    return out


def _canon(H, n):
    def perm(m, p):
        return sum(1 << p[i] for i in range(n) if m >> i & 1)
    return min(tuple(sorted(perm(m, p) for m in H)) for p in itertools.permutations(range(n)))


def _reduce(H):
    H = set(H)
    return [e for e in H if not any(e != f and e & f == e for f in H)]


def _components(H):
    H = list(H)
    comps = []
    while H:
        c = [H.pop()]
        verts = c[0]
        changed = True
        while changed:
            changed = False
            for e in list(H):
                if e & verts:
                    c.append(e)
                    verts |= e
                    H.remove(e)
                    changed = True
        comps.append(c)
    return comps


def _is_hds(C):
    verts = 0
    for e in C:
        verts |= e
    Z = 0
    for v in range(verts.bit_length()):
        if verts >> v & 1 and sum(1 for e in C if e >> v & 1) >= 2:
            Z |= 1 << v
    return any(Z & e == Z for e in C)


def _peel_ok(H):
    """Absorption, components, deletion of the vertices lying in every source
    of a component (Theorem 3.2), until every component is a hyper-double-star."""
    for C in _components(_reduce(H)):
        if _is_hds(C):
            continue
        D = -1
        for e in C:
            D &= e
        if D == 0:
            return False
        C2 = [e & ~D for e in C if e & ~D]
        if C2 and not _peel_ok(C2):
            return False
    return True


def _is_double_star(vs, edges):
    if len(edges) != len(vs) - 1:
        return False
    adj = {v: set() for v in vs}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    def ecc(s):
        d = {s: 0}
        fr = [s]
        while fr:
            x = fr.pop(0)
            for y in adj[x]:
                if y not in d:
                    d[y] = d[x] + 1
                    fr.append(y)
        return max(d.values()) if len(d) == len(vs) else 10 ** 9

    return max(ecc(v) for v in vs) <= 3


def _pair_obstruction(H, n):
    for U in range(1, 1 << n):
        if any(bin(e & U).count("1") > 2 for e in H):
            continue
        edges = {tuple(i for i in range(n) if (e & U) >> i & 1) for e in H if bin(e & U).count("1") == 2}
        seen = set()
        for v in sorted({x for ed in edges for x in ed}):
            if v in seen:
                continue
            comp = {v}
            fr = [v]
            while fr:
                x = fr.pop()
                for a, b in edges:
                    for y, z in ((a, b), (b, a)):
                        if y == x and z not in comp:
                            comp.add(z)
                            fr.append(z)
            seen |= comp
            if not _is_double_star(comp, [ed for ed in edges if ed[0] in comp]):
                return U
    return None


def _fmt(H, n):
    return "{" + ",".join("".join(str(i + 1) for i in range(n) if e >> i & 1) for e in sorted(H, key=lambda e: [i for i in range(n) if e >> i & 1])) + "}"


EXPECTED_UNDECIDED = {
    3: [],
    4: ["{123,124,134,234}"],
    5: None,  # recorded in certificates/S6_census.json on first run and compared thereafter
}


def run_S6():
    record = {}
    for n in (3, 4, 5):
        classes = sorted({_canon(H, n) for H in _antichains(n)}, key=lambda H: (len(H), H))
        term = non = 0
        undecided = []
        peel_not_hds = 0
        for H in classes:
            t = _peel_ok(H)
            o = _pair_obstruction(H, n)
            need(not (t and o is not None), f"S6 conflict: {_fmt(H, n)} proved both ways")
            if t:
                term += 1
                if not all(_is_hds(C) for C in _components(_reduce(H))):
                    peel_not_hds += 1
            elif o is not None:
                non += 1
            else:
                undecided.append(_fmt(H, n))
        need(peel_not_hds == 0, f"S6: a peelable non-HDS scenario on {n} vertices (minimality argument says 7)")
        record[n] = {"classes": len(classes), "terminating": term, "nonterminating": non,
                     "undecided": sorted(undecided)}
        log(f"  PASS S6 n={n}: {len(classes)} reduced scenarios up to isomorphism; "
            f"{term} terminate (peeling to hyper-double-stars), {non} do not (pair set), "
            f"{len(undecided)} undecided, 0 conflicts")
    need(record[3]["undecided"] == [] and record[4]["undecided"] == ["{123,124,134,234}"],
         "S6: four-vertex undecided set is not exactly K_4^(3)")
    need(record[4]["classes"] == 20 and record[3]["classes"] == 5, "S6 class counts")
    path = HERE / "certificates" / "S6_census.json"
    need(path.is_file(), f"S6: missing required census record {path}")
    need(json.loads(path.read_text()) == json.loads(json.dumps(record)), "S6: census differs from record")
    # the counterexample to the exploration's Conjecture 7.2
    b, v1, v2, v3, v4, v5, v6 = (1 << i for i in range(7))
    H = [b | v1 | v2, b | v2 | v3, b | v4 | v5, b | v5 | v6]
    need(not _is_hds(H), "S6: {b12,b23,b45,b56} should not be a hyper-double-star")
    need(_peel_ok(H), "S6: {b12,b23,b45,b56} should peel to hyper-double-stars")
    need(_pair_obstruction(H, 7) is None, "S6: {b12,b23,b45,b56} has a pair obstruction")
    link = [e & ~b for e in H]
    comps = _components(link)
    need(len(comps) == 2 and all(len(C) == 2 and _is_hds(C) for C in comps), "S6: link is P_3 + P_3")
    log("  PASS S6 {b12,b23,b45,b56}: not a hyper-double-star, link P_3 + P_3, no pair obstruction")
    return record


def expect_failure(label, thunk, fragment):
    try:
        thunk()
    except CertificateError as exc:
        need(fragment in str(exc), f"negative control {label} failed for the wrong reason: {exc}")
        log(f"  PASS negative control {label}: rejected ({exc})")
        return
    raise CertificateError(f"negative control {label} was not rejected")


def negative_controls():
    s = Scenario("S1={123,124}", [("a", (1, 2, 3)), ("b", (1, 2, 4))])
    data = json.loads((HERE / "certificates" / "lp_S1.json").read_text())
    rec = data["instances"][0]
    P = {tuple(int(c) for c in k): F(v) for k, v in rec["law"].items()}
    table = {tuple(int(c) for c in k): F(v) for k, v in rec["table"].items()}
    # (1) break invariance: move mass from one atom to a symmetric partner's non-partner
    atoms = sorted(table)
    a0 = atoms[0]
    broken = dict(table)
    eps = broken[a0] / 2
    broken[a0] -= eps
    other = tuple(1 - x if i == 0 else x for i, x in enumerate(a0))
    broken[other] = broken.get(other, ZERO) + eps
    expect_failure("S1 perturbed table", lambda: check_nw_table(s, 2, broken, P, "neg1"), "neg1")
    # (2) witness for one law, reconstruction asked to reproduce another
    P2 = dict(P)
    k1, k2 = (0, 0, 0, 0), (1, 1, 0, 0)
    d = min(P2[k1], F(1, 1000))
    P2[k1] -= d
    P2[k2] += d
    expect_failure("S1 wrong law", lambda: reconstruct(s, 2, P2, TableWitness(s, 2, table),
                                                       "exploration", "a", "explicit", "neg2"), "neg2")
    # (3) order below the bound
    s2 = Scenario("S2={123,34,45}", [("a", (1, 2, 3)), ("y", (3, 4)), ("c", (4, 5))])
    m = random_model(s2, random.Random(7), {"a": 2, "y": 2, "c": 2})
    expect_failure("S2 order 2", lambda: reconstruct(s2, 2, m.law(), ModelWitness(m, 2), "repaired",
                                                     "y", "explicit", "neg3"), "below the bound 4")
    # (4) implicit witness of a different model
    m2 = random_model(s2, random.Random(8), {"a": 2, "y": 2, "c": 2})
    expect_failure("S2 witness of another law", lambda: reconstruct(s2, 4, m.law(), ModelWitness(m2, 4),
                                                                    "repaired", "y", "marginal", "neg4"), "neg4")
    # (5) a scenario that is not a hyper-double-star
    s5 = Scenario("{123,14,24}", [("a", (1, 2, 3)), ("b", (1, 4)), ("c", (2, 4))])
    m5 = random_model(s5, random.Random(9), {"a": 2, "b": 2, "c": 2})
    expect_failure("{123,14,24} not HDS", lambda: reconstruct(s5, 2, m5.law(), ModelWitness(m5, 2),
                                                              "repaired", "a", "marginal", "neg5"), "Z not inside y")
    # (6) transport with a mismatched target and with the noiseless table
    expect_failure("S5 target q doubled", lambda: run_S5(target_q_scale=F(2)), "S5")
    expect_failure("S5 noiseless table", lambda: run_S5(noiseless_table=True), "S5")
    expect_failure("S5 target q doubled, diagonal check skipped",
                   lambda: run_S5(target_q_scale=F(2), skip_diagonal=True), "S5 injectable set")
    expect_failure("S5 noiseless table, diagonal check skipped",
                   lambda: run_S5(noiseless_table=True, skip_diagonal=True), "S5 injectable set")
    expect_failure("S5 fair bits equal across copies, diagonal check skipped",
                   lambda: run_S5(correlated_fair=True, skip_diagonal=True), "S5 AI set")


def main():
    try:
        log("S1 {123,124}, binary, order 2")
        n1 = run_S1()
        log("S2 {123,34,45}, binary, order 4")
        n2 = run_S2()
        log("S3 {1234,3456}, binary")
        n3 = run_S3()
        log("S4 star with a ternary degree-one central vertex")
        n4 = run_S4()
        log("S5 transport of the triangle witness into {123,14,24}")
        rec5 = run_S5()
        log("S6 census of reduced scenarios on at most five observers")
        run_S6()
        log("negative controls")
        negative_controls()
    except CertificateError as exc:
        print(f"FAIL: {exc}", flush=True)
        sys.exit(1)
    path5 = HERE / "certificates" / "S5_transport_record.json"
    if not path5.is_file() or json.loads(path5.read_text()) != json.loads(json.dumps(rec5)):
        print(f"FAIL: S5 transport record missing or different from {path5}", flush=True)
        sys.exit(1)
    log(f"ALL CHECKS PASSED ({n1} + {n2} + {n3} + {n4} reconstruction instances, 1 transport certificate)")


if __name__ == "__main__":
    main()
