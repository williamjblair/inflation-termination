#!/usr/bin/env python3
"""Fresh-directory replay runner for the inflation certificates.
Copies a certificate directory into a fresh temporary directory, runs one
command there, and records OS, architecture, Python, command, wall time, return
code, and SHA-256 of every input and output. Fails closed."""
import hashlib, json, platform, shutil, subprocess, sys, tempfile, time
from pathlib import Path
if not __debug__:
    raise RuntimeError("Replay runner must not run under python -O/-OO.")
HERE = Path(__file__).resolve().parent.parent
LOGS = HERE / "replay_logs"; LOGS.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def env():
    return {"os": platform.platform(), "architecture": platform.machine(), "python": sys.version,
            "python_flags": {"optimize": sys.flags.optimize}, "dependencies": "Python standard library only (fractions, json, itertools, re, pathlib)"}
def run(name, srcdir, extra_files, cmd, outputs=()):
    tmp = Path(tempfile.mkdtemp(prefix=f"replay-{name}-"))
    shutil.copytree(srcdir, tmp / "work", ignore=shutil.ignore_patterns("__pycache__"))
    for f in extra_files:
        shutil.copy(f, tmp / "work" / Path(f).name)
    inputs = {p.name: sha(p) for p in sorted((tmp / "work").iterdir()) if p.is_file()}
    t0 = time.time(); proc = subprocess.run(cmd, cwd=tmp / "work", capture_output=True, text=True); wall = time.time() - t0
    rec = {"name": name, "command": cmd, "cwd": "<fresh temporary directory>", "inputs_sha256": inputs, "return_code": proc.returncode,
           "wall_seconds": round(wall, 3), "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(), "stdout_tail": proc.stdout[-2500:],
           "stderr_tail": proc.stderr[-1500:], "outputs_sha256": {}, "environment": env(), "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    for o in outputs:
        p = tmp / "work" / o
        if p.exists(): rec["outputs_sha256"][o] = sha(p); shutil.copy(p, LOGS / f"{name}.{o}")
        else: rec["missing_output"] = o
    (LOGS / f"{name}.log").write_text(proc.stdout + ("\n[stderr]\n" + proc.stderr if proc.stderr else ""))
    (LOGS / f"{name}.json").write_text(json.dumps(rec, indent=2))
    if proc.returncode != 0 or "missing_output" in rec:
        raise SystemExit(f"REPLAY FAILED: {name} rc={proc.returncode}")
    return rec
if __name__ == "__main__":
    N = HERE / "certificates/nontermination"; E = HERE / "certificates/effective"; V = HERE / "verifiers"
    py = sys.executable
    plan = [
        ("nt-frozen-reconstruct-check", N, [], [py, "-B", "reconstruct.py", "--check"]),
        ("nt-frozen-check", N, [], [py, "-B", "check.py"]),
        ("nt-hardened-check", N, [V / "check_nontermination_hardened.py"], [py, "-B", "check_nontermination_hardened.py"]),
        ("nt-hardened-reconstruct-check", N, [V / "reconstruct_hardened.py"], [py, "-B", "reconstruct_hardened.py", "--check"]),
        ("eff-frozen-check", E, [], [py, "-B", "check.py"]),
        ("eff-hardened-check", E, [V / "check_effective_hardened.py"], [py, "-B", "check_effective_hardened.py"]),
        ("fan-check", HERE / "certificates/fan", [], [py, "-B", "verify_certificates.py"]),
        ("fan-check-optimized", HERE / "certificates/fan", [], [py, "-O", "-B", "verify_certificates.py"]),
        ("fan-independent-check", HERE / "certificates/fan", [V / "fan_independent_check.py"], [py, "-B", "fan_independent_check.py"]),
        ("classification-check", HERE / "certificates/classification", [], [py, "-B", "verify_classification.py"]),
    ]
    for name, d, extra, cmd in plan:
        r = run(name, d, [str(x) for x in extra], cmd)
        print(name, "rc", r["return_code"], "wall", r["wall_seconds"], "|", r["stdout_tail"].strip().splitlines()[-1][:120] if r["stdout_tail"].strip() else "")
