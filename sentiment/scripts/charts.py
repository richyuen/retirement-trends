"""Charts for the sentiment vs contributions README (PNG, light background)."""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "output")
BLUE, ORANGE, INK, INK2, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "lines.linewidth": 2})

a = pd.read_csv(os.path.join(OUT, "annual_panel.csv"), index_col="year").loc[1984:2025]

# Fig 1: levels as small multiples (no dual axis)
fig, ax = plt.subplots(3, 1, figsize=(8, 8.2), sharex=True)
ax[0].plot(a.index, a.ics, color=INK2)
ax[0].set_title("Michigan consumer sentiment index (annual average)", loc="left", color=INK, fontsize=11)
ax[1].plot(a.index, a.bea_dc_employee_pct_wages, color=BLUE)
ax[1].set_title("Employee DC contributions, % of all wages (BEA)", loc="left", color=INK, fontsize=11)
ax[2].plot(a.index, a.bea_dc_employer_pct_priv_wages, color=ORANGE)
ax[2].set_title("Employer DC contributions, % of private wages (BEA)", loc="left", color=INK, fontsize=11)
ax[1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}%"))
ax[2].yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.25))
ax[2].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.2f}%"))
fig.suptitle("Contributions trend up while sentiment trends down: the level correlation is spurious",
             x=0.01, ha="left", color=INK, fontsize=12, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(os.path.join(OUT, "fig1_levels.png"), dpi=150)

# Fig 2: year-to-year changes, employee DC vs sentiment
d = a[["ics", "bea_dc_employee_pct_wages", "bea_dc_employer_pct_priv_wages"]].diff().dropna()
fig, ax = plt.subplots(1, 2, figsize=(9, 4.2), sharex=True)
for x, col, c, t in [(ax[0], "bea_dc_employee_pct_wages", BLUE, "Employee DC contributions"),
                     (ax[1], "bea_dc_employer_pct_priv_wages", ORANGE, "Employer DC contributions")]:
    x.axhline(0, color=INK2, lw=0.8); x.axvline(0, color=INK2, lw=0.8)
    x.scatter(d.ics, d[col], s=36, color=c, edgecolor=SURF, linewidth=1.5, zorder=3)
    b = np.polyfit(d.ics, d[col], 1); xs = np.linspace(d.ics.min(), d.ics.max(), 10)
    x.plot(xs, np.polyval(b, xs), color=c, lw=1.5, ls="--")
    r = np.corrcoef(d.ics, d[col])[0, 1]
    x.set_title(f"{t}\nr = {r:.2f}, n = {len(d)} (1985-2025)", loc="left", color=INK, fontsize=10.5)
    x.set_xlabel("Change in sentiment index (points)")
    for yr in (2008, 2020, 2022):
        if yr in d.index:
            x.annotate(str(yr), (d.ics[yr], d[col][yr]), xytext=(4, 4), textcoords="offset points", color=INK2, fontsize=8)
ax[0].set_ylabel("Change, percentage points of wages")
fig.suptitle("Year-to-year changes: a weak link for employee contributions, none for employers",
             x=0.01, ha="left", color=INK, fontsize=12, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(OUT, "fig2_changes.png"), dpi=150)
print("ok")
