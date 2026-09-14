#!/usr/bin/env python3
"""Plot certified parity-threshold intervals; never fit or extrapolate them.

Run from any directory with Python and matplotlib. The PDF is included in
the arXiv package, so compiling the manuscript does not require Python.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
plt.rcParams.update({
    "font.family": "serif", "font.size": 10, "axes.labelsize": 11,
    "axes.titlesize": 11, "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})
fig, axes = plt.subplots(1, 2, figsize=(6.25, 2.95), layout="constrained")
fig.get_layout_engine().set(w_pad=0.06, h_pad=0.06, wspace=0.12)
provenance = {"quantity": "t times the certified parity threshold", "sources": {}}
for ax, name, ceiling in zip(axes, ("square", "triangle"), (.46, 1.0)):
    path = ROOT / "artifact/certificates/exponent/certificates" / f"{name}.json"
    data = json.loads(path.read_text())
    provenance["sources"][str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    for hierarchy, color, marker in (("AI", "#245577", "o"), ("NW", "#A54F2A", "D")):
        rows = sorted((r for r in data["orders"] if r["hierarchy"] == hierarchy), key=lambda r: r["t"])
        assert [r["t"] for r in rows] == list(range(1, 11))
        ts = [r["t"] for r in rows]
        los = [Fraction(r["q_lo"]) for r in rows]
        his = [Fraction(r["q_hi"]) if r["q_hi"] is not None else None for r in rows]
        assert all(hi is None or lo < hi for lo, hi in zip(los, his))
        ys = [t * float(lo) for t, lo in zip(ts, los)]
        ax.plot(ts, ys, color=color, linewidth=.85, alpha=.8)
        ax.plot(ts, ys, linestyle="none", marker=marker, markersize=4.4,
                markerfacecolor="white" if hierarchy == "NW" else color,
                markeredgecolor=color, label=hierarchy, zorder=3)
        for t, lo, hi in zip(ts, los, his):
            if hi is not None:
                ax.vlines(t, t * float(lo), t * float(hi), color=color, linewidth=1.2)
        if name == "square" and hierarchy == "NW":
            ax.annotate("lower bound", (2, ys[1]), xytext=(2.7, .435),
                        fontsize=8, ha="center", color=color,
                        arrowprops={"arrowstyle": "-", "color": color, "lw": .65})
    ax.axhline(1/16, color=".4", linewidth=.8, linestyle=(0, (3, 3)))
    ax.text(9.7, 1/16 + ceiling*.02, "$1/16$", fontsize=8, color=".35", ha="right")
    ax.set(xlim=(.6, 10.4), ylim=(0, ceiling), xlabel="Inflation order $t$",
           ylabel=r"$t\,q_t^H$", title="Square ($C_4$)" if name == "square" else "Triangle ($C_3$)")
    ax.set_xticks([1, 2, 4, 6, 8, 10])
    ax.grid(axis="y", color=".9", linewidth=.5)
axes[1].legend(frameon=False, loc="upper left", fontsize=9)
fig.savefig(HERE / "thresholds.pdf", metadata={"CreationDate": None, "ModDate": None})
plt.close(fig)
(HERE / "thresholds-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
