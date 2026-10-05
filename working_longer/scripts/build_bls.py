"""Labor force participation and full/part-time work of older Americans, BLS CPS (LN) flat files.

Rebuild:
    python3 scripts/build_bls.py            # uses raw/ln_subset.tsv if present
    python3 scripts/build_bls.py --refresh  # re-downloads ln.data.1.AllData (~390 MB) to /tmp and re-extracts

Outputs (output/):
    lfpr_by_age_sex_annual.csv      long: year, sex, age band, LFPR (%), source (published series or computed from levels)
    lfpr_wide_both_sexes.csv        wide: year x age band, both sexes
    lfpr_wide_men.csv / _women.csv  wide by sex
    lfpr_check_published_vs_computed.csv   validation where both exist
    ft_pt_older_workers.csv         share of employed who usually work part time, 55+ (1986+) and 65+ (2009+)
    lfpr_bls_projections_2035.csv   BLS Employment Projections Table 3.3 (2005, 2015, 2025, 2035)
"""
import os, sys, subprocess
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(ROOT, "output")
SUBSET = os.path.join(RAW, "ln_subset.tsv")
ALLDATA_URL = "https://download.bls.gov/pub/time.series/ln/ln.data.1.AllData"
CONTACT = os.environ.get("BLS_CONTACT_EMAIL", "")  # BLS asks for a contact email; set it locally
UA = f"Mozilla/5.0 (research; {CONTACT})"

# Levels (thousands): population (00), labor force (10), employed (20); unadjusted, annual average = period M13.
# key: (measure, band, sex) -> series_id
LEVELS = {
    ("pop", "55-59", "0"): "LNU00000094", ("pop", "55-59", "1"): "LNU00000189", ("pop", "55-59", "2"): "LNU00000346",
    ("lf", "55-59", "0"): "LNU01000094", ("lf", "55-59", "1"): "LNU01000189", ("lf", "55-59", "2"): "LNU01000346",
    ("pop", "60-61", "1"): "LNU00000196", ("pop", "60-61", "2"): "LNU00000351",
    ("lf", "60-61", "1"): "LNU01000196", ("lf", "60-61", "2"): "LNU01000351",
    ("pop", "62-64", "1"): "LNU00000198", ("pop", "62-64", "2"): "LNU00000353",
    ("lf", "62-64", "1"): "LNU01000198", ("lf", "62-64", "2"): "LNU01000353",
    ("pop", "55-64", "0"): "LNU00000095", ("pop", "55-64", "1"): "LNU00000190", ("pop", "55-64", "2"): "LNU00000347",
    ("lf", "55-64", "0"): "LNU01000095", ("lf", "55-64", "1"): "LNU01000190", ("lf", "55-64", "2"): "LNU01000347",
    ("pop", "65+", "0"): "LNU00000097", ("pop", "65+", "1"): "LNU00000199", ("pop", "65+", "2"): "LNU00000354",
    ("lf", "65+", "0"): "LNU01000097", ("lf", "65+", "1"): "LNU01000199", ("lf", "65+", "2"): "LNU01000354",
    ("pop", "65-69", "0"): "LNU00024938", ("pop", "65-69", "1"): "LNU00000203", ("pop", "65-69", "2"): "LNU00000358",
    ("lf", "65-69", "0"): "LNU01024938", ("lf", "65-69", "1"): "LNU01000203", ("lf", "65-69", "2"): "LNU01000358",
    ("pop", "70-74", "0"): "LNU00024941", ("pop", "70-74", "1"): "LNU00024939", ("pop", "70-74", "2"): "LNU00024940",
    ("lf", "70-74", "0"): "LNU01024941", ("lf", "70-74", "1"): "LNU01024939", ("lf", "70-74", "2"): "LNU01024940",
    ("pop", "75+", "0"): "LNU00024942", ("pop", "75+", "1"): "LNU00015346", ("pop", "75+", "2"): "LNU00015349",
    ("lf", "75+", "0"): "LNU01024942", ("lf", "75+", "1"): "LNU01015346", ("lf", "75+", "2"): "LNU01015349",
    ("pop", "55+", "0"): "LNU00024230", ("pop", "55+", "1"): "LNU00024231", ("pop", "55+", "2"): "LNU00024232",
    ("lf", "55+", "0"): "LNU01024230", ("lf", "55+", "1"): "LNU01024231", ("lf", "55+", "2"): "LNU01024232",
    ("emp", "55+", "0"): "LNU02024230", ("emp", "55+", "1"): "LNU02024231", ("emp", "55+", "2"): "LNU02024232",
    ("emp", "65+", "0"): "LNU02000097", ("emp", "65+", "1"): "LNU02000199", ("emp", "65+", "2"): "LNU02000354",
}
# Published LFPR series (%), unadjusted, M13
RATES = {
    ("55-59", "0"): "LNU01300094", ("55-59", "1"): "LNU01300189", ("55-59", "2"): "LNU01300346",
    ("60-61", "1"): "LNU01300196", ("60-61", "2"): "LNU01300351",
    ("62-64", "1"): "LNU01300198", ("62-64", "2"): "LNU01300353",
    ("55-64", "0"): "LNU01300095", ("55-64", "1"): "LNU01300190", ("55-64", "2"): "LNU01300347",
    ("65+", "0"): "LNU01300097", ("65+", "1"): "LNU01300199", ("65+", "2"): "LNU01300354",
    ("65-69", "0"): "LNU01324938", ("65-69", "1"): "LNU01300203", ("65-69", "2"): "LNU01300358",
    ("70-74", "0"): "LNU01324941", ("70-74", "1"): "LNU01324939", ("70-74", "2"): "LNU01324940",
    ("75+", "0"): "LNU01324942", ("75+", "1"): "LNU01315346", ("75+", "2"): "LNU01315349",
    ("55+", "0"): "LNU01324230", ("55+", "1"): "LNU01324231", ("55+", "2"): "LNU01324232",
}
# Usual full-time / part-time employment (thousands)
FTPT = {
    ("ft", "55+", "0"): "LNU02524230", ("ft", "55+", "1"): "LNU02524231", ("ft", "55+", "2"): "LNU02524232",
    ("pt", "55+", "0"): "LNU02624230", ("pt", "55+", "1"): "LNU02624231", ("pt", "55+", "2"): "LNU02624232",
    ("ft", "65+", "0"): "LNU02500097", ("pt", "65+", "0"): "LNU02600097",  # annual-only series (period A01), 2009+
}
ALL_IDS = set(LEVELS.values()) | set(RATES.values()) | set(FTPT.values())
SEXNAME = {"0": "both", "1": "men", "2": "women"}


def refresh_subset():
    tmp = "/tmp/ln.data.1.AllData"
    if not os.path.exists(tmp):
        subprocess.run(["curl", "-sS", "-A", UA, "-o", tmp, ALLDATA_URL], check=True)
    n = 0
    with open(tmp) as f, open(SUBSET, "w") as g:
        g.write(f.readline())
        for line in f:
            if line.split("\t", 1)[0].strip() in ALL_IDS:
                g.write(line); n += 1
    print(f"extracted {n} rows for {len(ALL_IDS)} series -> {SUBSET}")


def load():
    d = pd.read_csv(SUBSET, sep="\t", dtype=str)
    d.columns = [c.strip() for c in d.columns]
    for c in d.columns:
        d[c] = d[c].str.strip()
    d = d[d.period.isin(["M13", "A01"])].copy()
    d["value"] = pd.to_numeric(d.value, errors="coerce")
    d["year"] = d.year.astype(int)
    return d.set_index(["series_id", "year"])["value"]


def get(v, sid):
    try:
        return v.loc[sid]
    except KeyError:
        return pd.Series(dtype=float)


def main():
    if "--refresh" in sys.argv or not os.path.exists(SUBSET):
        refresh_subset()
    v = load()
    os.makedirs(OUT, exist_ok=True)

    def level(measure, band, sex):
        if (measure, band, sex) in LEVELS:
            return get(v, LEVELS[(measure, band, sex)])
        if sex == "0" and (measure, band, "1") in LEVELS:  # both sexes = men + women
            return level(measure, band, "1") + level(measure, band, "2")
        if band == "55-61":
            return level(measure, "55-59", sex) + level(measure, "60-61", sex)
        return pd.Series(dtype=float)

    rows, checks = [], []
    bands = ["55-59", "60-61", "55-61", "62-64", "55-64", "65+", "65-69", "70-74", "75+", "55+"]
    for band in bands:
        for sex in "012":
            comp = (level("lf", band, sex) / level("pop", band, sex) * 100).dropna()
            pub = get(v, RATES[(band, sex)]) if (band, sex) in RATES else pd.Series(dtype=float)
            for yr in sorted(set(comp.index) | set(pub.index)):
                if yr in pub.index and pd.notna(pub.get(yr)):
                    val, src = pub[yr], "published " + RATES[(band, sex)]
                else:
                    val, src = round(comp[yr], 1), "computed from LF/pop levels"
                rows.append(dict(year=yr, sex=SEXNAME[sex], age=band, lfpr=val, source=src,
                                 pop_thous=level("pop", band, sex).get(yr)))
                if yr in pub.index and yr in comp.index:
                    checks.append(dict(year=yr, sex=SEXNAME[sex], age=band, published=pub[yr],
                                       computed=round(comp[yr], 2), diff=round(comp[yr] - pub[yr], 2)))
    lf = pd.DataFrame(rows)
    lf.to_csv(os.path.join(OUT, "lfpr_by_age_sex_annual.csv"), index=False)
    ck = pd.DataFrame(checks)
    ck.to_csv(os.path.join(OUT, "lfpr_check_published_vs_computed.csv"), index=False)
    order = ["55-61", "55-59", "60-61", "62-64", "55-64", "65+", "65-69", "70-74", "75+", "55+"]
    for s in ["both", "men", "women"]:
        w = lf[lf.sex == s].pivot(index="year", columns="age", values="lfpr")
        w[[c for c in order if c in w]].to_csv(os.path.join(OUT, f"lfpr_wide_{'both_sexes' if s == 'both' else s}.csv"))

    # Full-time / part-time
    ft_rows = []
    for band, sex in [("55+", "0"), ("55+", "1"), ("55+", "2"), ("65+", "0")]:
        ft, pt = get(v, FTPT[("ft", band, sex)]), get(v, FTPT[("pt", band, sex)])
        emp = level("emp", band, sex)
        for yr in ft.index:
            ft_rows.append(dict(year=yr, sex=SEXNAME[sex], age=band, ft_thous=ft[yr], pt_thous=pt[yr],
                                emp_thous=emp.get(yr), pt_share_pct=round(pt[yr] / (ft[yr] + pt[yr]) * 100, 1)))
    # 55-64 by subtraction (55+ minus 65+), 2009+
    ft55, pt55 = get(v, FTPT[("ft", "55+", "0")]), get(v, FTPT[("pt", "55+", "0")])
    ft65, pt65 = get(v, FTPT[("ft", "65+", "0")]), get(v, FTPT[("pt", "65+", "0")])
    for yr in ft65.index:
        f, q = ft55[yr] - ft65[yr], pt55[yr] - pt65[yr]
        ft_rows.append(dict(year=yr, sex="both", age="55-64 (55+ minus 65+)", ft_thous=f, pt_thous=q,
                            emp_thous=f + q, pt_share_pct=round(q / (f + q) * 100, 1)))
    ftpt = pd.DataFrame(ft_rows)
    # share of the whole age group working full time / part time (per 100 population)
    popmap = {("55+", "both"): level("pop", "55+", "0"), ("55+", "men"): level("pop", "55+", "1"),
              ("55+", "women"): level("pop", "55+", "2"), ("65+", "both"): level("pop", "65+", "0"),
              ("55-64 (55+ minus 65+)", "both"): level("pop", "55-64", "0")}
    ftpt["ft_pct_of_pop"] = [round(r.ft_thous / popmap[(r.age, r.sex)].get(r.year) * 100, 1) for r in ftpt.itertuples()]
    ftpt["pt_pct_of_pop"] = [round(r.pt_thous / popmap[(r.age, r.sex)].get(r.year) * 100, 1) for r in ftpt.itertuples()]
    ftpt.to_csv(os.path.join(OUT, "ft_pt_older_workers.csv"), index=False)

    # BLS projections table 3.3
    p = pd.read_html(os.path.join(RAW, "bls_projections", "table_3-3_lfpr_2005_2015_2025_2035.htm"))[0].iloc[:, :5]
    p.columns = ["group", "2005", "2015", "2025", "2035"]
    p = p.dropna(subset=["2005"])
    sexlab, recs = "both", []
    for _, r in p.iterrows():
        g = str(r.group).strip()
        if g.startswith("Men,"): sexlab = "men"
        elif g.startswith("Women,"): sexlab = "women"
        elif g.startswith("White"): break
        if g in ("55 to 64", "65 to 74", "75 and older", "55 and older"):
            recs.append(dict(sex=sexlab, age=g, **{k: float(r[k]) for k in ["2005", "2015", "2025", "2035"]}))
    proj = pd.DataFrame(recs)
    proj.to_csv(os.path.join(OUT, "lfpr_bls_projections_2035.csv"), index=False)

    # ---- summaries ----
    print(f"validation: {len(ck)} published-vs-computed pairs, max |diff| = {ck['diff'].abs().max():.2f} pp")
    wb = pd.read_csv(os.path.join(OUT, "lfpr_wide_both_sexes.csv"), index_col=0)
    yrs = [y for y in [1948, 1967, 1976, 1985, 1994, 2000, 2007, 2010, 2019, 2020, 2021, 2024, 2025] if y in wb.index]
    print("LFPR both sexes (%):")
    print(wb.loc[yrs, ["55-61", "62-64", "65+", "65-69", "70-74", "75+"]].to_string())
    for s in ["men", "women"]:
        w = pd.read_csv(os.path.join(OUT, f"lfpr_wide_{s}.csv"), index_col=0)
        print(f"LFPR {s} (%):"); print(w.loc[[y for y in [1948, 1976, 1985, 1994, 2000, 2019, 2025] if y in w.index], ["55-61", "62-64", "65+", "65-69", "70-74", "75+"]].to_string())
    print("Part-time share of employed (%):")
    print(ftpt.pivot(index="year", columns=["age", "sex"], values="pt_share_pct").loc[[1986, 1993, 1994, 2000, 2007, 2009, 2019, 2025]].to_string())
    print("Working full time / part time, % of population:")
    print(ftpt[ftpt.sex == "both"].pivot(index="year", columns="age", values=["ft_pct_of_pop", "pt_pct_of_pop"]).loc[[1986, 1994, 2009, 2019, 2025]].to_string())
    print("BLS projections:"); print(proj.to_string(index=False))


if __name__ == "__main__":
    main()
