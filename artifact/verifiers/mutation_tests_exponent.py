#!/usr/bin/env python3
"""Exercise threshold-checker failure handling and explicit partial coverage.

Run from the repository root with python3 -B artifact/verifiers/mutation_tests_exponent.py.
The full arithmetic replay is a separate invocation of verify_exponent.py.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / "certificates/exponent"


def edit(work, change):
    path = work / "certificates/square.json"
    data = json.loads(path.read_text())
    change(data)
    path.write_text(json.dumps(data))


def run(name, mutate=None, args=(), flags=(), success=False, partial=False):
    with tempfile.TemporaryDirectory(prefix="mutation-threshold-") as tmp:
        work = Path(tmp)
        shutil.copytree(SOURCE, work, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__"))
        if mutate:
            mutate(work)
        proc = subprocess.run([sys.executable, *flags, "-B", "verify_exponent.py", *args],
                              cwd=work, capture_output=True, text=True, timeout=120)
        claims_success = "OK (" in proc.stdout
        good = (proc.returncode == 0 and claims_success) if success else (
            proc.returncode != 0 and not claims_success)
        if success:
            good = good and (("OK (PARTIAL)" in proc.stdout) == partial)
        if not good:
            raise RuntimeError(f"{name}: unexpected result, rc={proc.returncode}\n"
                               f"{proc.stdout}\n{proc.stderr}")
        print(f"PASS {name}: rc={proc.returncode}, claims_success={claims_success}")


def main():
    short = ("--max-order", "1")
    run("partial-control", args=short, success=True, partial=True)
    run("empty-directory", lambda w: shutil.rmtree(w / "certificates"))
    for name in ("square", "triangle"):
        run(f"missing-{name}", lambda w, n=name: (w / f"certificates/{n}.json").unlink())
    run("missing-published-record", lambda w: edit(w, lambda d: d["orders"].pop()))
    run("duplicate-record", lambda w: edit(w, lambda d: d["orders"].append(d["orders"][0])))
    run("empty-records", lambda w: edit(w, lambda d: d.update(orders=[])))
    run("wrong-scenario", lambda w: edit(w, lambda d: d.update(scenario="triangle")))
    run("wrong-cycle", lambda w: edit(w, lambda d: d.update(cycle_length=3)))
    run("wrong-cap", lambda w: edit(w, lambda d: d.update(q_top="1/10")))
    run("unknown-hierarchy", lambda w: edit(w, lambda d: d["orders"][0].update(hierarchy="other")))
    run("out-of-range-order", lambda w: edit(w, lambda d: d["orders"][0].update(t=11)))
    run("missing-requested-partial-record", lambda w: edit(w, lambda d: d["orders"].pop(0)), args=short)
    run("partial-allows-unrequested-omission", lambda w: edit(w, lambda d: d["orders"].pop()),
        args=short, success=True, partial=True)
    run("invalid-zero-limit", args=("--max-order", "0"))
    run("invalid-excess-limit", args=("--max-order", "11"))
    run("corrupted-primal", lambda w: edit(w, lambda d: d["orders"][0].update(primal_weights=[])),
        args=short)
    for flag in ("-O", "-OO"):
        run(f"refuse-{flag}", args=short, flags=(flag,))
    print("MUTATION_TESTS_EXPONENT=PASS (19 cases; partial success is labeled)")


if __name__ == "__main__":
    main()
