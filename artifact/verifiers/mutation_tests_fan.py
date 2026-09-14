#!/usr/bin/env python3
"""Mutation tests for the fan certificate checker (explicit-exception checker;
must fail closed under normal and optimized interpreters)."""
import json, pathlib, shutil, subprocess, sys, tempfile
if not __debug__: raise RuntimeError("Run without -O/-OO.")
HERE = pathlib.Path(__file__).resolve().parent.parent; SRC = HERE/"certificates/fan"; PY = sys.executable
def run(mutate, flags=()):
    w = pathlib.Path(tempfile.mkdtemp(prefix="mut-fan-"))/"work"; shutil.copytree(SRC, w, ignore=shutil.ignore_patterns("__pycache__","*.zip"))
    if mutate: mutate(w)
    p = subprocess.run([PY,*flags,"-B","verify_certificates.py"], cwd=w, capture_output=True, text=True, timeout=600)
    return p.returncode, (p.returncode==0 and "Traceback" not in p.stderr and '"k": 4' in p.stdout)
def edit(w,f):
    d=json.loads((w/"certificates.json").read_text()); f(d); (w/"certificates.json").write_text(json.dumps(d))
def m_empty(w): (w/"certificates.json").write_text("")
def m_trunc(w): b=(w/"certificates.json").read_bytes(); (w/"certificates.json").write_bytes(b[:len(b)//2])
def m_atom(w): edit(w, lambda d: d["records"][0]["atoms"].__setitem__("000","32830/2097152"))
def m_order(w): edit(w, lambda d: d["records"][0].__setitem__("fan_rejecting_order", d["records"][0]["fan_rejecting_order"]-1))
def m_passing(w): edit(w, lambda d: d["records"][0].__setitem__("passing_order", d["records"][0]["passing_order"]+1))
def m_drop(w): edit(w, lambda d: d["records"].pop())
def m_sign(w): edit(w, lambda d: d["records"][1].__setitem__("finner_gap", "-"+d["records"][1]["finner_gap"].lstrip("-")))
def m_params(w): edit(w, lambda d: d["records"][0].__setitem__("epsilon","1/63"))
scen=[("control",None,(),True),("empty-proof",m_empty,(),False),("truncated-certificate",m_trunc,(),False),("corrupt-atom",m_atom,(),False),
      ("wrong-rejecting-order",m_order,(),False),("wrong-passing-order",m_passing,(),False),("missing-last-record-weaker-certificate",m_drop,(),True),
      ("wrong-sign-gap",m_sign,(),False),("wrong-parameters",m_params,(),False),
      ("python-O-control",None,("-O",),True),("python-O-corrupt-atom",m_atom,("-O",),False),("python-OO-corrupt-atom",m_atom,("-OO",),False),
      ("python-O-empty-proof",m_empty,("-O",),False)]
res, bad = [], []
for name,mut,flags,expect_ok in scen:
    rc,claims=run(mut,flags); ok=(rc==0 and claims) if expect_ok else (rc!=0 and not claims)
    res.append({"scenario":name,"rc":rc,"claims_pass":claims,"expected":"success" if expect_ok else "fail-closed","outcome_ok":ok})
    if not ok: bad.append(name)
    print(f"{'OK ' if ok else 'BAD'} {name:28s} rc={rc} claims_pass={claims}")
(HERE/"replay_logs/mutation-fan.json").write_text(json.dumps(res,indent=1))
if bad: raise SystemExit("MUTATION TESTS FAILED: "+", ".join(bad))
print("NOTE: removing a whole record yields a weaker but valid certificate (each record is checked independently; the record count is reported, not enforced)")
print("MUTATION_TESTS_FAN=PASS (fails closed on every corruption, also under -O/-OO)")
