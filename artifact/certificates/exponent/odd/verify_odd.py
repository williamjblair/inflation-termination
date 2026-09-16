#!/usr/bin/env python3
"""Exact verifier for the odd-order and order-conversion certificates of the parity
thresholds (paper: Proposition prop:parityconversion and the paragraph after it).
Standard library only, no floating point in any check, refuses to run under -O.

Run from the repository root:  python3 -B artifact/certificates/exponent/odd/verify_odd.py
It imports ../verify_exponent.py and reads ../certificates/{triangle,square}.json.

Checks
  (1) Degree gap.  For m in {3,4} and t <= TMAX, recomputes D_NW(t) (t-fold sums of
      even-weight 0/1 vectors) and D_AI(t) (S even, 2 max k <= S, k_g <= t) and
      confirms the closed forms of NOTE.md, Proposition 1:
        m = 3:  D_AI \\ D_NW = { k in D_AI : S >= 2t + 2 }
        m = 4:  D_NW = { k in D_AI : S <= 2t + 2 min k } = { k in D_AI : t1 - k in D_AI }
      and the counting formula for m = 3.
  (2) Complement identity  C(t,k) K_{t-k}(a) = (-1)^a C(t,k) K_k(a)  (integers).
  (3) Containment  D_AI(s) subset D_NW(t)  iff  3s - [s odd] <= 2t  (s, t <= TMAX).
  (4) The order-3 triangle face at q = 1/5: two exact NW witnesses with AI-only
      moments -7/125 and 1/25, their mixture 2/5, 3/5 is an AI witness, and the
      certified NW dual of the 2026-09-14 artifact has polynomial (5q-1)(q+1)^2.
  (5) Extension threshold certificates in certificates/{triangle,square}.json (triangle
      t = 11, 12, 13, both hierarchies; square t = 11, AI), checked record by record
      by ../verify_exponent.py with an extension inventory in place of the t <= 10
      published inventory (both files are required, records must be exactly these),
      plus: at odd orders the AI and NW brackets are identical and the AI dual uses
      only NW keys; at even orders q_hi(AI) < q_lo(NW).
  (6) certificates/layers-triangle.json: brackets for NW + {(t,t,t)} and
      NW + {S = 2t+2 layer} at t = 4, 6.

Usage: python3 verify_odd.py
"""
import itertools, json, os, sys, time
from fractions import Fraction as F
from math import comb

if not __debug__:
    sys.stderr.write("verify_odd.py refuses to run with assertions disabled (-O)\n")
    raise SystemExit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import verify_exponent as V  # noqa: E402  (standard library only)

TMAX = 16
CHECKS = 0

# Records carried by the extension files beyond the published orders 1..10.
EXTENSION_RECORDS = {
    "triangle": {(t, h) for t in (11, 12, 13) for h in ("AI", "NW")},
    "square": {(11, "AI")},
}


def need(ok, msg):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise SystemExit("FAIL: " + msg)


def nw_set(m, t):
    evens = [v for v in itertools.product((0, 1), repeat=m) if sum(v) % 2 == 0]
    cur = {tuple([0] * m)}
    for _ in range(t):
        cur = {tuple(a + b for a, b in zip(c, v)) for c in cur for v in evens}
    return cur


def ai_set(m, t):
    return {k for k in itertools.product(range(t + 1), repeat=m)
            if sum(k) % 2 == 0 and 2 * max(k) <= sum(k)}


def check_degree_gap():
    for m in (3, 4):
        for t in range(1, TMAX + 1):
            nw, ai = nw_set(m, t), ai_set(m, t)
            need(nw <= ai, f"m={m} t={t}: NW not inside AI")
            if m == 3:
                need(ai - nw == {k for k in ai if sum(k) >= 2 * t + 2}, f"m=3 t={t}: gap form")
                need(nw == {k for k in ai if sum(k) <= 2 * t}, f"m=3 t={t}: NW form")
                cnt = sum(comb(J + 2, 2) for J in range(0, t - 1) if (J - t) % 2 == 0)
                need(len(ai - nw) == cnt, f"m=3 t={t}: gap count")
            else:
                need(nw == {k for k in ai if sum(k) <= 2 * t + 2 * min(k)}, f"m=4 t={t}: NW form")
                need(nw == {k for k in ai if tuple(t - x for x in k) in ai},
                     f"m=4 t={t}: complement form")
        print(f"  (1) degree gap closed forms: m={m}, t <= {TMAX}")


def check_complement():
    for t in range(1, TMAX + 1):
        S = V.sign_sum_table(t)
        for k in range(t + 1):
            for a in range(t + 1):
                need(S[t - k][a] == (-1) ** a * S[k][a], f"complement identity t={t}")
    print(f"  (2) C(t,k)K_(t-k)(a) = (-1)^a C(t,k)K_k(a) for t <= {TMAX}")


def check_containment():
    for m in (3, 4):
        ais = {s: ai_set(m, s) for s in range(1, 13)}
        nws = {t: nw_set(m, t) for t in range(1, 13)}
        for s in range(1, 13):
            for t in range(1, 13):
                inc = ais[s] <= nws[t]
                need(inc == (3 * s - (s % 2) <= 2 * t),
                     f"m={m}: containment D_AI({s}) in D_NW({t})")
    print("  (3) D_AI(s) subset D_NW(t) iff 3s - [s odd] <= 2t, m in {3,4}, s,t <= 12")


def moments_ok(m, t, keys, weights, q):
    perms = list(itertools.permutations(range(m)))
    S = V.sign_sum_table(t)
    V.check_primal(m, t, S, keys, weights, q, perms)
    return True


def kbar(m, t, key, weights):
    """exact symmetrized moment sum_abar V_abar kbar(key, abar)"""
    perms = list(itertools.permutations(range(m)))
    S = V.sign_sum_table(t)
    P = 1
    for g in range(m):
        P *= comb(t, key[g])
    tot = F(0)
    for ab, v in weights.items():
        tot += v * F(V.perm_sum(m, S, key, ab, perms), len(perms) * P)
    return tot


def check_face():
    m, t, q = 3, 3, F(1, 5)
    w1 = {(0, 0, 0): F(1, 1000), (0, 0, 1): F(27, 1000), (0, 0, 3): F(81, 1000),
          (0, 1, 2): F(243, 1000), (0, 1, 3): F(81, 200), (0, 2, 2): F(243, 1000)}
    w2 = {(0, 0, 0): F(1, 1000), (0, 0, 3): F(81, 1000), (0, 1, 1): F(81, 1000),
          (0, 1, 2): F(81, 500), (0, 1, 3): F(54, 125), (0, 2, 2): F(243, 1000)}
    nwkeys = sorted({tuple(sorted(k)) for k in nw_set(m, t)})
    aikeys = sorted({tuple(sorted(k)) for k in ai_set(m, t)})
    for w in (w1, w2):
        moments_ok(m, t, nwkeys, w, q)
    need(kbar(m, t, (2, 3, 3), w1) == F(-7, 125), "face witness 1 AI-only moment")
    need(kbar(m, t, (2, 3, 3), w2) == F(1, 25), "face witness 2 AI-only moment")
    mix = {}
    for w, lam in ((w1, F(2, 5)), (w2, F(3, 5))):
        for a, v in w.items():
            mix[a] = mix.get(a, F(0)) + lam * v
    moments_ok(m, t, aikeys, mix, q)
    art = os.path.join(HERE, "..", "certificates", "triangle.json")
    rec = [r for r in json.load(open(art))["orders"] if r["t"] == 3 and r["hierarchy"] == "NW"][0]
    coeffs = {tuple(k): F(v) for k, v in rec["dual_pieces"][0]["coefficients"]}
    perms = list(itertools.permutations(range(3)))
    V.check_dual(3, 3, V.sign_sum_table(3), coeffs, V.sorted_tuples(3, 3), perms)
    poly = V.dual_poly_coeffs(coeffs)
    need(poly == [F(-1), F(3), F(9), F(5)], "t=3 NW dual polynomial is (5q-1)(q+1)^2")
    need(all(tuple(sorted(k)) in set(nwkeys) for k in coeffs), "t=3 dual keys are NW keys")
    print("  (4) triangle t=3, q=1/5: AI-only moment ranges over at least [-7/125, 1/25] on the"
          " NW face; target 1/625; mixture 2/5,3/5 is an AI witness; NW dual <= 0 with"
          " E = (5q-1)(q+1)^2")


def validate_extension_inventory(data, name, max_order=None):
    """Bind an extension file to its scenario, cap and exact record list."""
    need(name in V.SCENARIOS and name in EXTENSION_RECORDS, f"unknown extension file: {name}")
    m, cap = V.SCENARIOS[name]
    need(data["scenario"] == name and data["cycle_length"] == m,
         f"{name}: scenario identity or cycle length mismatch")
    need(F(data["q_top"]) == cap, f"{name}: wrong parameter cap")
    seen = set()
    for rec in data["orders"]:
        key = (rec["t"], rec["hierarchy"])
        need(key not in seen, f"{name}: duplicate order/hierarchy record: {key}")
        need(type(rec["t"]) is int and rec["t"] > V.PUBLISHED_MAX_ORDER,
             f"{name}: extension record inside the published range: {key}")
        seen.add(key)
    need(seen == EXTENSION_RECORDS[name],
         f"{name}: extension records {sorted(seen)} differ from {sorted(EXTENSION_RECORDS[name])}")


def check_certificates():
    # verify_file checks the published inventory (t <= 10); the extension files carry
    # only higher orders, so bind them to their own exact inventory instead.
    V.validate_inventory = validate_extension_inventory
    for name in ("triangle", "square"):
        path = os.path.join(HERE, "certificates", f"{name}.json")
        need(os.path.isfile(path), f"missing required extension certificate: {path}")
        data, table = V.verify_file(path, None, log=lambda s: print("     " + s.strip()))
        m = data["cycle_length"]
        by = {(r["t"], r["hierarchy"]): r for r in data["orders"]}
        ts = sorted({r["t"] for r in data["orders"]})
        for t in ts:
            if (t, "AI") not in by or (t, "NW") not in by:
                continue
            ai, nw = by[(t, "AI")], by[(t, "NW")]
            if t % 2 == 1:
                need(ai["q_lo"] == nw["q_lo"] and ai["q_hi"] == nw["q_hi"],
                     f"{name} t={t}: odd-order brackets differ")
                nwkeys = {tuple(sorted(k)) for k in nw_set(m, t)}
                for piece in ai["dual_pieces"]:
                    need(all(tuple(k) in nwkeys for k, _v in piece["coefficients"]),
                         f"{name} t={t}: AI dual uses an AI-only key")
                print(f"     {name} t={t}: AI and NW brackets identical, AI dual uses NW keys only")
            else:
                need(F(ai["q_hi"]) < F(nw["q_lo"]), f"{name} t={t}: even order not separated")
                print(f"     {name} t={t}: q_hi(AI) = {ai['q_hi']} < {nw['q_lo']} = q_lo(NW)")
    print("  (5) extension order certificates verified (triangle t = 11..13, square t = 11 AI)")


def check_layers():
    path = os.path.join(HERE, "certificates", "layers-triangle.json")
    data = json.load(open(path))
    m, q_top = 3, F(data["q_top"])
    perms = list(itertools.permutations(range(3)))
    for rec in data["systems"]:
        t = rec["t"]
        nw = nw_set(m, t)
        extra = {tuple(k) for k in rec["extra_keys"]}
        ai = ai_set(m, t)
        if rec["system"] == "NW+balanced":
            need(extra == {(t, t, t)}, "balanced extra set")
        else:
            need(extra == {k for k in ai - nw if sum(k) == 2 * t + 2}, "layer extra set")
        keys = sorted({tuple(sorted(k)) for k in nw | extra})
        S = V.sign_sum_table(t)
        q_lo, q_hi = F(rec["q_lo"]), F(rec["q_hi"])
        w = {tuple(a): F(v) for a, v in rec["primal_weights"]}
        V.check_primal(m, t, S, keys, w, q_lo, perms)
        left = q_hi
        for piece in rec["dual_pieces"]:
            a, b = F(piece["interval"][0]), F(piece["interval"][1])
            need(a == left and a < b <= q_top, "layer dual interval chain")
            coeffs = {tuple(k): F(v) for k, v in piece["coefficients"]}
            need(all(k in set(keys) for k in coeffs), "layer dual key not prescribed")
            V.check_dual(m, t, S, coeffs, V.sorted_tuples(m, t), perms)
            poly = V.dual_poly_coeffs(coeffs)
            need(V.poly_eval(poly, a) > 0 and V.poly_eval(poly, b) > 0, "layer dual sign")
            need(V.distinct_roots_in(poly, a, b) == 0, "layer dual root")
            left = b
        need(left == q_top and q_lo < q_hi, "layer dual cover")
        print(f"     t={t} {rec['system']}: [{rec['q_lo']}, {rec['q_hi']}]")
    print("  (6) layer brackets verified")


def gauss_mul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def gauss_pow(x, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = gauss_mul(out, x)
    return out


def check_ideal_density():
    """sum_a Re prod_g C(t,a_g) p^(t-a_g) pbar^(a_g) prod_g K_(k_g)(a_g) = Re (i r)^S,
    p = (1 + i r)/2, for every k (balanced or not); q = r^2."""
    for m in (3, 4):
        for t in range(1, 5 if m == 4 else 6):
            S = V.sign_sum_table(t)
            for r in (F(1, 3), F(2, 5)):
                p, pb = (F(1, 2), r / 2), (F(1, 2), -r / 2)
                col = [gauss_mul(gauss_pow(p, t - a), gauss_pow(pb, a)) for a in range(t + 1)]
                for k in itertools.product(range(t + 1), repeat=m):
                    tot = F(0)
                    for a in itertools.product(range(t + 1), repeat=m):
                        z = (F(1), F(0))
                        mult = F(1)
                        for g in range(m):
                            z = gauss_mul(z, col[a[g]])
                            mult *= F(comb(t, a[g]) * S[k[g]][a[g]], comb(t, k[g]))
                        tot += z[0] * mult
                    target = gauss_pow((F(0), r), sum(k))[0]
                    need(tot == target, f"ideal density m={m} t={t} k={k}")
    print("  (7) Re prod_g Bin(t,(1+i sqrt q)/2) reproduces (-q)^(S/2) at every even S and 0 at odd S"
          " (m=3: t<=5, m=4: t<=4, sqrt q in {1/3, 2/5})")


def check_square_halves():
    art = os.path.join(HERE, "..", "certificates", "square.json")
    data = json.load(open(art))
    m = 4
    perms = list(itertools.permutations(range(m)))
    for rec in data["orders"]:
        if not rec.get("dual_pieces"):
            continue
        t, hier = rec["t"], rec["hierarchy"]
        coeffs = {tuple(k): F(v) for k, v in rec["dual_pieces"][0]["coefficients"]}
        comp = {tuple(sorted(t - x for x in k)): v for k, v in coeffs.items()}
        symmetric = comp == coeffs
        S = V.sign_sum_table(t)
        Dc = 1
        for v in coeffs.values():
            Dc = V.lcm(Dc, v.denominator)
        P = {k: comb(t, k[0]) * comb(t, k[1]) * comb(t, k[2]) * comb(t, k[3]) for k in coeffs}
        L = 1
        for v in P.values():
            L = V.lcm(L, v)
        num = {k: int(v * Dc) * (L // P[k]) for k, v in coeffs.items()}
        vanish = all(sum(num[k] * V.perm_sum(m, S, k, ab, perms) for k in coeffs) == 0
                     for ab in V.sorted_tuples(m, t) if sum(ab) % 2 == 1)
        need(symmetric == vanish, f"square t={t} {hier}: symmetry/vanishing mismatch")
        expected = (hier == "NW") or (t % 2 == 1)
        need(vanish == expected, f"square t={t} {hier}: odd-half vanishing pattern")
    print("  (8) square, t<=10: the first NW dual piece at every order and the AI dual at odd orders"
          " vanish on all configurations with odd total count; the AI dual at even orders does not")


def check_transfer():
    import glob
    files = sorted(glob.glob(os.path.join(HERE, "certificates", "*-transfer.json")))
    if not files:
        print("  (9) no transfer certificates")
        return
    for path in files:
        data = json.load(open(path))
        m, q_top = data["cycle_length"], F(data["q_top"])
        perms = list(itertools.permutations(range(m)))
        for rec in data["orders"]:
            t, hier = rec["t"], rec["hierarchy"]
            full = nw_set(m, t) if hier == "NW" else ai_set(m, t)
            keys = sorted({tuple(sorted(k)) for k in full})
            nwkeys = {tuple(sorted(k)) for k in nw_set(m, t)}
            S = V.sign_sum_table(t)
            q_lo, q_hi = F(rec["q_lo"]), F(rec["q_hi"])
            need(0 < q_lo < q_hi <= q_top, "transfer bracket order")
            w = {tuple(a): F(v) for a, v in rec["primal_weights"]}
            V.check_primal(m, t, S, keys, w, q_lo, perms)
            left = q_hi
            for piece in rec["dual_pieces"]:
                a, b = F(piece["interval"][0]), F(piece["interval"][1])
                need(a == left and a < b <= q_top, "transfer dual interval chain")
                coeffs = {tuple(k): F(v) for k, v in piece["coefficients"]}
                need(all(k in nwkeys for k in coeffs), "transfer dual uses a non-NW key")
                V.check_dual(m, t, S, coeffs, V.sorted_tuples(m, t), perms)
                poly = V.dual_poly_coeffs(coeffs)
                need(V.poly_eval(poly, a) > 0 and V.poly_eval(poly, b) > 0, "transfer dual sign")
                need(V.distinct_roots_in(poly, a, b) == 0, "transfer dual root")
                left = b
            need(left == q_top, "transfer dual cover does not reach q_top")
            print(f"     {data['scenario']} t={t} {hier}: q_lo = {rec['q_lo']} feasible,"
                  f" infeasible on [{rec['q_hi']}, q_top] by an NW-key dual")
    print("  (9) transfer certificates verified (an NW dual is an AI dual since D_NW is inside D_AI)")


def main():
    t0 = time.time()
    check_degree_gap()
    check_complement()
    check_containment()
    check_face()
    check_layers()
    check_ideal_density()
    check_square_halves()
    check_certificates()
    check_transfer()
    print(f"\nOK: {CHECKS} local checks and {V.CHECKS} verify_exponent checks passed"
          f" in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
