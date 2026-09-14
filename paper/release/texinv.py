#!/usr/bin/env python3
r"""Mechanical invariance check for a prose-only editing pass on LaTeX sources.

Usage: texinv.py snapshot <dir> <file.tex>...   -> writes <dir>/<basename>.json
       texinv.py check    <dir> <file.tex>...   -> compares and reports differences

The invariant: the ordered sequence of (a) math segments ($...$, $$...$$, \[...\], and the
bodies of equation/align/gather/multline environments, starred or not), (b) \label, \ref,
\eqref, \cite (with optional argument) tokens, (c) \begin{...}/\end{...} environment names,
(d) \section/\subsection/\paragraph commands with their titles, (e) \input/\providecommand
lines. Prose between these may change freely. Exit code 1 on any difference.
"""
import json, re, sys, pathlib

MATH_ENVS = r"equation|align|gather|multline|eqnarray|alignat|flalign"

def tokens(text):
    text = re.sub(r"(?m)(?<!\\)%.*$", "", text)  # strip comments
    out = []
    pat = re.compile(
        r"(?P<disp>\$\$.*?\$\$)"
        r"|(?P<bra>\\\[.*?\\\])"
        r"|(?P<env>\\begin\{(" + MATH_ENVS + r")\*?\}.*?\\end\{\2\*?\})"
        r"|(?P<inl>(?<!\\)\$(?:\\.|[^$\\])*\$)"
        r"|(?P<ref>\\(?:label|ref|eqref|cite|autoref|Cref|cref)(?:\[[^\]]*\])?\{[^}]*\})"
        r"|(?P<be>\\(?:begin|end)\{[^}]*\})"
        r"|(?P<sec>\\(?:section|subsection|subsubsection|paragraph)\*?\{[^}]*\})"
        r"|(?P<misc>\\(?:input|providecommand|newcommand|renewcommand|usepackage|providecommand)[^\n]*)",
        re.S)
    for m in pat.finditer(text):
        kind = m.lastgroup
        s = m.group(0)
        s = re.sub(r"\s+", " ", s).strip()
        out.append([kind, s])
    return out

def main():
    mode, d, files = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3:]
    d.mkdir(parents=True, exist_ok=True)
    bad = 0
    for f in files:
        p = pathlib.Path(f)
        snap = d / (p.name + ".json")
        toks = tokens(p.read_text())
        if mode == "snapshot":
            snap.write_text(json.dumps(toks))
            continue
        old = json.loads(snap.read_text())
        if old != toks:
            bad += 1
            print(f"DIFF {f}: {len(old)} tokens before, {len(toks)} after")
            n = min(len(old), len(toks))
            for i in range(n):
                if old[i] != toks[i]:
                    print(f"  first difference at token {i}:\n    before: {old[i]}\n    after:  {toks[i]}")
                    break
            else:
                extra = old[n:] or toks[n:]
                print(f"  tail differs: {extra[:2]}")
        else:
            print(f"ok   {f}")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
