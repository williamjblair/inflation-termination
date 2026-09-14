#!/usr/bin/env python3
"""Build a flattened, self-contained arXiv source package without shell escape."""
import re
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
DEST = HERE / "arxiv-src"


def flatten(path, stack=()):
    if path in stack:
        raise ValueError(f"Recursive input: {path}")
    source = path.read_text()
    def replace(match):
        child = PAPER / (match.group(1) + ".tex")
        return flatten(child, stack + (path,))
    return re.sub(r"\\input\{([^}]+)\}", replace, source)


def main():
    source = flatten(PAPER / "main.tex")
    if "\\input{" in source or "/Users/" in source:
        raise ValueError("Package contains unresolved inputs or an absolute local path")
    with tempfile.TemporaryDirectory(prefix="inflation-arxiv-") as tmp:
        work = Path(tmp)
        (work / "main.tex").write_text(source)
        shutil.copy(PAPER / "references.bib", work)
        (work / "figures").mkdir()
        shutil.copy(PAPER / "figures/thresholds.pdf", work / "figures")
        result = subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
             "-pdflatex=pdflatex -no-shell-escape %O %S", "main.tex"],
            cwd=work, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (HERE / "arxiv-build.log").write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError("Standalone compilation failed; see arxiv-build.log")
        log = (work / "main.log").read_text(errors="replace")
        if re.search(r"undefined|Overfull|multiply defined", log, re.I):
            raise RuntimeError("Standalone PDF has unresolved references or overflow")
        DEST.mkdir(exist_ok=True)
        (DEST / "figures").mkdir(exist_ok=True)
        for name in ("main.tex", "main.bbl", "references.bib", "main.pdf"):
            shutil.copy(work / name, DEST / name)
        shutil.copy(work / "figures/thresholds.pdf", DEST / "figures")
        with tarfile.open(HERE / "arxiv-src.tar.gz", "w:gz") as archive:
            for name in ("main.tex", "main.bbl", "references.bib", "figures/thresholds.pdf"):
                archive.add(DEST / name, arcname=name)
    print("ARXIV_PACKAGE_OK: flattened sources, bibliography, vector figures; no shell escape")


if __name__ == "__main__":
    main()
