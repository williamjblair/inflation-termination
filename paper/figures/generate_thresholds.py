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
    "font.family": "serif", "font.serif": ["STIXGeneral"],
    "mathtext.fontset": "stix", "font.size": 10.5, "axes.labelsize": 11,
    "axes.titlesize": 12, "axes.titleweight": "semibold",
    "axes.titlepad": 11, "axes.labelcolor": ".2", "axes.edgecolor": ".45",
    "xtick.color": ".3", "ytick.color": ".3", "axes.linewidth": .65,
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})
fig, axes = plt.subplots(1, 2, figsize=(6.25, 3.1), layout="constrained")
fig.get_layout_engine().set(w_pad=0.04, h_pad=0.06, wspace=0.14)
provenance = {"quantity": "t times the certified parity threshold", "sources": {}}
for ax, name, ceiling in zip(axes, ("square", "triangle"), (.49, 1.0)):
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
        ax.plot(ts, ys, color=color, linewidth=1.05, alpha=.8)
        ax.plot(ts, ys, linestyle="none", marker=marker, markersize=5,
                markerfacecolor="none" if hierarchy == "NW" else color,
                markeredgecolor=color, label=hierarchy, zorder=3)
        for t, lo, hi in zip(ts, los, his):
            if hi is not None:
                ax.vlines(t, t * float(lo), t * float(hi), color=color, linewidth=1.2)
        if name == "square" and hierarchy == "NW":
            ax.annotate("NW: lower bound", (2, ys[1]), xytext=(4.7, .46),
                        fontsize=8.5, ha="center", color=color,
                        arrowprops={"arrowstyle": "->", "color": color, "lw": .7,
                                    "connectionstyle": "arc3,rad=.15"})
    # All-order analytic guarantee of Theorems 4.3 and 4.4: q = B^(2/t) - 1, B = 16/15 or 9/8.
    base, label = (16 / 15, r"$t((16/15)^{2/t}-1)$") if name == "square" else (9 / 8, r"$t((9/8)^{2/t}-1)$")
    grid = [1 + 9 * k / 200 for k in range(201)]
    guarantee = [u * (base ** (2 / u) - 1) for u in grid]
    ax.plot(grid, guarantee, color=".4", linewidth=1, linestyle=(0, (4, 3)),
            label="All-order guarantee")
    ax.text(9.8, guarantee[-1] + ceiling*.045, label, fontsize=9, color=".35", ha="right")
    ax.set(xlim=(.6, 10.4), ylim=(0, ceiling), xlabel="Inflation order $t$",
           ylabel=r"Scaled threshold $t\,q_t^H$")
    ax.set_title("(a) Square ($C_4$)" if name == "square" else "(b) Triangle ($C_3$)", loc="left")
    ax.set_xticks([1, 2, 4, 6, 8, 10])
    ax.grid(axis="y", color=".91", linewidth=.6)
    ax.tick_params(length=3, width=.65)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, frameon=False, loc="outside upper center", ncol=3,
           fontsize=10, handlelength=2.3, columnspacing=2)
fig.savefig(HERE / "thresholds.pdf", metadata={"CreationDate": None, "ModDate": None})
plt.close(fig)
(HERE / "thresholds-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
