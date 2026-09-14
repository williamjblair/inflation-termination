#!/usr/bin/env python3
"""Mutation tests for the inflation certificate checkers (frozen and hardened).
A scenario passes when the checker FAILS CLOSED (nonzero exit, no PASS report)
on a corrupted input; the control must pass. The frozen checkers use bare
`assert`, so under python -O/-OO they skip every check and report PASS on
corrupted input: those scenarios are recorded as documented defects, closed by
the hardened copies."""
import json, pathlib, shutil, subprocess, sys, tempfile
if not __debug__:
    raise RuntimeError("Run without -O/-OO.")
HERE = pathlib.Path(__file__).resolve().parent.parent
N = HERE / "certificates/nontermination"; V = HERE / "verifiers"; PY = sys.executable

def fresh(hardened):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="mut-nt-")) / "work"
    shutil.copytree(N, tmp, ignore=shutil.ignore_patterns("__pycache__"))
    if hardened:
        shutil.copy(V / "check_nontermination_hardened.py", tmp / "check.py")
    return tmp

def run(hardened, mutate, flags=()):
    w = fresh(hardened)
    if mutate: mutate(w)
    p = subprocess.run([PY, *flags, "-B", "check.py"], cwd=w, capture_output=True, text=True, timeout=600)
    claims = p.returncode == 0 and '"status": "PASS"' in p.stdout
    return p.returncode, claims

def edit(w, name, f):
    d = json.loads((w / name).read_text()); f(d); (w / name).write_text(json.dumps(d))
def m_truncated(w): b = (w / "t2-full-lp.json").read_bytes(); (w / "t2-full-lp.json").write_bytes(b[: len(b) // 2])
def m_empty(w): (w / "t2-defect.json").write_text("")
def m_corrupt_witness(w): edit(w, "t2-defect.json", lambda d: d["target_atoms"].__setitem__("000", "1/2"))
def m_wrong_order(w): edit(w, "t2-defect.json", lambda d: d.__setitem__("order", 3))
def m_missing_branch(w): edit(w, "t3-defect.json", lambda d: d["outputs"].pop())
def m_wrong_sign(w):
    def f(d):
        rows = {r["assignment"]: r for r in d["entries"]}
        rows["1" * 12]["numerator"] -= 1; rows["0" * 12]["numerator"] += 1   # normalization-preserving corruption
    edit(w, "t2-full-lp.json", f)
def m_negative_entry(w):
    def f(d):
        d["entries"][0]["numerator"] = -d["entries"][0]["numerator"] - 1; d["entries"][1]["numerator"] += 2 * d["entries"][0]["numerator"] * -1
    edit(w, "t2-full-lp.json", f)
def m_wrong_root_law(w): edit(w, "t1-defect.json", lambda d: d["root_law"].__setitem__("p_one", "1/3"))
def m_bad_support(w): edit(w, "t2-defect.json", lambda d: d["outputs"][0]["value_one_iff_all_zero"].pop())
def m_control_not_rejected(w):
    # make the negative control identical to the good vector: the checker must then fail (it requires rejection)
    shutil.copy(w / "t2-full-lp.json", w / "t2-corrupted-negative-control.json")

scen = []
for label, hard in (("frozen", False), ("hardened", True)):
    scen += [
        (f"{label}:control", hard, None, (), "ok"),
        (f"{label}:truncated-certificate", hard, m_truncated, (), "fail"),
        (f"{label}:empty-proof", hard, m_empty, (), "fail"),
        (f"{label}:corrupt-witness-atom", hard, m_corrupt_witness, (), "fail"),
        (f"{label}:wrong-order", hard, m_wrong_order, (), "fail"),
        (f"{label}:missing-branch", hard, m_missing_branch, (), "fail"),
        (f"{label}:wrong-sign-normalized-corruption", hard, m_wrong_sign, (), "fail"),
        (f"{label}:negative-entry", hard, m_negative_entry, (), "fail"),
        (f"{label}:wrong-root-law", hard, m_wrong_root_law, (), "fail"),
        (f"{label}:bad-support", hard, m_bad_support, (), "fail"),
        (f"{label}:negative-control-not-rejected", hard, m_control_not_rejected, (), "fail"),
        (f"{label}:python-O-corrupt-witness", hard, m_corrupt_witness, ("-O",), "known-defect" if not hard else "fail"),
        (f"{label}:python-OO-corrupt-witness", hard, m_corrupt_witness, ("-OO",), "known-defect" if not hard else "fail"),
    ]
results, bad, known = [], [], []
for name, hard, mut, flags, expect in scen:
    rc, claims = run(hard, mut, flags)
    if expect == "known-defect":
        fo = (rc == 0 and claims); known.append((name, fo))
        results.append({"scenario": name, "rc": rc, "claims_pass": claims, "expected": "known-defect: frozen bare asserts are stripped under -O", "fails_open": fo, "outcome_ok": True})
        print(f"KNOWN-DEFECT {name:46s} rc={rc} claims_pass={claims} fails_open={fo}"); continue
    ok = (rc == 0 and claims) if expect == "ok" else (rc != 0 and not claims)
    results.append({"scenario": name, "rc": rc, "claims_pass": claims, "expected": expect, "outcome_ok": ok})
    if not ok: bad.append(name)
    print(f"{'OK ' if ok else 'BAD'} {name:46s} rc={rc} claims_pass={claims}")
(HERE / "replay_logs/mutation-nontermination.json").write_text(json.dumps(results, indent=1))
print("KNOWN DEFECTS (frozen under -O/-OO):", known)
if bad: raise SystemExit("MUTATION TESTS FAILED: " + ", ".join(bad))
print("MUTATION_TESTS_NONTERMINATION=PASS (hardened checker fails closed on every mutation)")
