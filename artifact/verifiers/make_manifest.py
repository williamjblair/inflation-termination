#!/usr/bin/env python3
"""Write artifact/MANIFEST.json and artifact/SHA256SUMS over every file in the
artifact directory (excluding the two manifest files themselves)."""
import hashlib, json, os, pathlib, sys, time
if not __debug__:
    raise RuntimeError("Run without -O/-OO.")
root = pathlib.Path(__file__).resolve().parent.parent
entries = {}
for p in sorted(root.rglob("*")):
    if p.is_dir() or (p.parent == root and p.name in ("MANIFEST.json", "SHA256SUMS")) or "__pycache__" in p.parts:
        continue
    rel = p.relative_to(root).as_posix()
    entries[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "size": p.stat().st_size}
manifest = {
    "artifact": "inflation-nontermination",
    "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "frozen_identities": {
        "maintained_repository_revision": "768d404c631659574d9fad232c028df4f63fbc3b",
        "original_proof_source_sha256": "a38310645a78b5d9372ef55080899308e4ab4b84f57ee207e21979913f5e3bf4",
        "original_result_source_sha256": "834bd9c2c41bbe7a12d6e0873c4ed623336c7576a5ae7e291b070f2c06028334",
        "result_cert_0_candidate_snapshot_sha256": "25cab3a99a6b8541bfbf38f66c7a745e256f8c0a8badd1c0828f8b30f964eb92"
    },
    "files": entries,
}
(root / "MANIFEST.json").write_text(json.dumps(manifest, indent=1))
(root / "SHA256SUMS").write_text("".join(f"{v['sha256']}  {k}\n" for k, v in entries.items()))
print(f"manifest: {len(entries)} files")
