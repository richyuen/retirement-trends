"""Parse Census published poverty tables in ../raw into tidy CSVs in ../output.

Inputs (all from www2.census.gov, see README for URLs):
  raw/hstpov3.xlsx  Historical Poverty Table 3 (official, by age and race, 1959-2025)
  raw/hstpov5.xlsx  Historical Table 5 (ratio of income to poverty, all and 65+, 1970-2025)
  raw/p60_290/table_8_spm_hist.xlsx  SPM by age and race 2009-2025 (P60-290)
  effect-of-elements tables: P60-258 Table 5a, P60-261/265/268 Table A-6, P60-272/275 Appendix Table 6,
  P60-277/280 Table B-7, P60-283/287 Table B-6, P60-290 Table 5 (xlsx);
  P60-241 Table 3a/3b, P60-244/247 Table 5a/5b, P60-251 Table 5a, P60-254 Table 4a/4b (PDF, via pdftotext).
Outputs:
  output/opm_by_age_1959_2025.csv, output/opm_65plus_by_race.csv, output/near_poverty_65plus.csv,
  output/spm_vs_opm_by_age_2009_2025.csv, output/spm_65plus_by_race.csv, output/spm_element_effects_65plus.csv
"""
import os, re, glob, subprocess
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "raw")
OUT = os.path.join(HERE, "..", "output")

FOOT3 = {"2": "Vintage 2025 population controls", "3": "2020 Census-based controls",
         "4": "updated processing system (compare to 2018+)", "5": "2013 redesigned income questions (3/8 sample)",
         "6": "2013 traditional income questions (5/8 sample)"}


def num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if f != f else f


def parse_year(cell):
    m = re.match(r"^\s*(\d{4})\s*(?:\((\d+)\))?", str(cell))
    return (int(m.group(1)), m.group(2)) if m else (None, None)


def hstpov3():
    x = pd.read_excel(os.path.join(RAW, "hstpov3.xlsx"), header=None)
    rows, section = [], None
    for _, r in x.iterrows():
        y, fn = parse_year(r[0])
        if y is None:
            if isinstance(r[0], str) and r[0].strip() and not r[0].startswith(("Table", "(", "Year", "Note", "Source", "Foot")):
                section = r[0].strip()
            continue
        rows.append(dict(section=section, year=y, footnote=fn,
                         note=FOOT3.get(fn, "") if section == "All Races" else "",
                         u18_pct=num(r[4]), a18_64_pct=num(r[12]), a65_pct=num(r[16]),
                         a65_pop_k=num(r[14]), a65_poor_k=num(r[15])))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "opm_by_age_and_race_1959_2025_long.csv"), index=False)
    a = df[df.section == "All Races"].drop(columns="section")
    a.to_csv(os.path.join(OUT, "opm_by_age_1959_2025.csv"), index=False)
    race = df[df.section.isin(["White Alone, Not Hispanic", "Black Alone", "Asian Alone", "Hispanic (any race)",
                               "White, Not Hispanic", "Black", "Asian and Pacific Islander"])]
    race = race.assign(footnote=race.footnote.fillna("")).pivot_table(
        index=["year", "footnote"], columns="section", values="a65_pct").reset_index().sort_values("year", ascending=False)
    race.to_csv(os.path.join(OUT, "opm_65plus_by_race.csv"), index=False)
    return a


def hstpov5():
    x = pd.read_excel(os.path.join(RAW, "hstpov5.xlsx"), header=None)
    cuts = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
    rows = []
    for _, r in x.iterrows():
        y, fn = parse_year(r[0])
        if y is None:
            continue
        d = dict(year=y, footnote=fn)
        for j, c in enumerate(cuts):
            d[f"all_below_{int(c*100)}"] = num(r[1 + j])
            d[f"65_below_{int(c*100)}"] = num(r[8 + j])
        rows.append(d)
    df = pd.DataFrame(rows)
    df["65_100_to_150"] = (df["65_below_150"] - df["65_below_100"]).round(1)
    df["65_100_to_200"] = (df["65_below_200"] - df["65_below_100"]).round(1)
    df.to_csv(os.path.join(OUT, "near_poverty_65plus.csv"), index=False)
    return df


def spm_hist(opm):
    x = pd.read_excel(os.path.join(RAW, "p60_290", "table_8_spm_hist.xlsx"), header=None)
    rows, section = [], None
    for _, r in x.iterrows():
        c0 = str(r[0]).strip()
        if c0.isupper() and len(c0) > 3:
            section = c0
            continue
        m = re.match(r"^(\d{4})(\d?)$", c0.split(".")[0])
        if not m or num(r[1]) is None:
            continue
        rows.append(dict(section=section, year=int(m.group(1)), footnote=m.group(2) or None,
                         all_pct=num(r[4]), u18_pct=num(r[9]), a18_64_pct=num(r[14]),
                         a65_pct=num(r[19]), a65_moe=num(r[20]), a65_poor_k=num(r[17]), a65_pop_k=num(r[16])))
    df = pd.DataFrame(rows)
    note = {"3": "Vintage 2025 population controls", "4": "2020 Census-based controls",
            "5": "revised SPM methodology (2021 revision)", "6": "updated processing system",
            "7": "2013 redesigned income questions (3/8)", "8": "2013 traditional questions (5/8)",
            "9": "2010 Census-based controls"}
    df["note"] = df.footnote.map(note).fillna("")
    a = df[df.section == "ALL RACES"].drop(columns="section")
    # attach official 65+ for the same year/version
    o = opm.copy()
    omap = {}
    for _, r in o.iterrows():
        key = (r.year, {"2": "3", "3": "4", "4": "6", "5": "7", "6": "8"}.get(r.footnote, None))
        omap[key] = (r.a65_pct, r.u18_pct, r.a18_64_pct)
    def look(r, i):
        k = (r.year, r.footnote)
        if k in omap:
            return omap[k][i]
        if r.footnote in ("5", "9"):  # SPM-only footnotes: official has a single row
            return omap.get((r.year, None), (None,) * 3)[i]
        return omap.get((r.year, None), (None,) * 3)[i]
    a["opm_65_pct"] = a.apply(lambda r: look(r, 0), axis=1)
    a["opm_u18_pct"] = a.apply(lambda r: look(r, 1), axis=1)
    a["opm_18_64_pct"] = a.apply(lambda r: look(r, 2), axis=1)
    a["spm_minus_opm_65"] = (a.a65_pct - a.opm_65_pct).round(1)
    a.to_csv(os.path.join(OUT, "spm_vs_opm_by_age_2009_2025.csv"), index=False)
    race = df[df.section.isin(["WHITE ALONE, NOT HISPANIC", "BLACK ALONE", "ASIAN ALONE", "HISPANIC (ANY RACE)"])]
    race.assign(footnote=race.footnote.fillna("")).pivot_table(
        index=["year", "footnote"], columns="section", values="a65_pct").reset_index().sort_values("year", ascending=False) \
        .to_csv(os.path.join(OUT, "spm_65plus_by_race.csv"), index=False)
    return a


# ---------- effect of elements ----------
XLSX_EFFECT = [("P60-258 Table 5a", "p60_258/Table5a.xlsx"), ("P60-261 Table A-6", "p60_261/table6.xlsx"),
               ("P60-265 Table A-6", "p60_265/table6.xls"), ("P60-268 Table A-6", "p60_268/table6.xls"),
               ("P60-272 App. Table 6", "p60_272/table6.xlsx"), ("P60-275 App. Table 6", "p60_275/table6.xlsx"),
               ("P60-277 Table B-7", "p60_277/tableB-7.xlsx"), ("P60-280 Table B-7", "p60_280/tableB-7.xlsx"),
               ("P60-283 Table B-6", "p60_283/tableB-6.xlsx"), ("P60-287 Table B-6", "p60_287/tableB-6.xlsx"),
               ("P60-290 Table 5", "p60_290/table_5_spm_program_effect_rates.xlsx")]


def xlsx_effects():
    out = []
    for src, f in XLSX_EFFECT:
        x = pd.read_excel(os.path.join(RAW, f), header=None)
        title = " ".join(str(v) for v in x.iloc[:4, 0])
        year = None
        m = re.search(r"Rates: (\d{4})\s*\(", title.replace("\n", " "))
        if m and "and" not in title.split("Rates:")[1][:12]:
            year = int(m.group(1))
        for _, r in x.iterrows():
            c0 = str(r[0]).replace(".", "").strip()
            if re.fullmatch(r"\d{4}\d?", c0) and num(r[1]) is None:
                year, fn = int(c0[:4]), c0[4:]
                continue
            key = None
            if c0.startswith(("All people", "SPM rate")):
                key = "spm_rate"
            elif c0.startswith("Social Security"):
                key = "ss_effect"
            elif re.match(r"SSI\d?$", c0):
                key = "ssi_effect"
            elif c0.startswith(("Medical expenses", "MOOP")):
                key = "moop_effect"
            if key and year:
                out.append(dict(source=src, year=year, key=key, val=num(r[7]), moe=num(r[8])))
    return pd.DataFrame(out)


PDF_EFFECT = {  # report: list of (table label regex, year, version)
    "p60-241": [(r"Table 3a\.", 2010), (r"Table 3b\.", 2009)],
    "p60-244": [(r"Table 5a\.", 2011), (r"Table 5b\.", 2010)],
    "p60-247": [(r"Table 5a\.", 2012), (r"Table 5b\.", 2011)],
    "p60-251": [(r"Table 5a\.", 2013), (r"Table 5b\.", 2012)],
    "p60-254": [(r"Table 4a\.", 2014), (r"Table 4b\.", 2013)],
}


def pdf_effects():
    out = []
    for rep, tabs in PDF_EFFECT.items():
        pdf = os.path.join(RAW, "spm_reports_pdf", rep + ".pdf")
        txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
        lines = txt.splitlines()
        for lab, year in tabs:
            start = next(i for i, l in enumerate(lines) if re.match(r"^\s*" + lab, l)
                         and re.search(r"(?i)elements", " ".join(lines[i:i + 2])))
            seen = set()
            for l in lines[start:start + 60]:
                l2 = re.sub(r"(\d) \.(\d)", r"\1.\2", l)
                lab_txt = re.sub(r"[ .]+$", "", re.split(r"\s{2,}\d", l2.strip())[0]).strip(" .")
                nums = re.findall(r"(?<![\w.])\d+\.\d(?!\d)", l2)
                key = None
                if re.match(r"(Research SPM|SPM)\b", lab_txt):
                    key = "spm_rate"
                elif lab_txt.startswith("Social Security"):
                    key = "ss_excluded"
                elif lab_txt == "SSI":
                    key = "ssi_excluded"
                elif lab_txt == "MOOP":
                    key = "moop_excluded"
                if key and key not in seen and len(nums) >= 8:
                    seen.add(key)
                    out.append(dict(source=f"{rep.upper()} {lab.replace(chr(92), '').rstrip('.')}", year=year, key=key,
                                    val=float(nums[6]), moe=float(nums[7])))
    df = pd.DataFrame(out)
    # convert "rate excluding element" into effect = SPM rate - rate excluding (Census's later convention)
    res = []
    for (src, y), g in df.groupby(["source", "year"]):
        d = dict(zip(g.key, g.val))
        res.append(dict(source=src, year=y, key="spm_rate", val=d["spm_rate"], moe=None))
        for k in ("ss", "ssi", "moop"):
            if f"{k}_excluded" in d:
                res.append(dict(source=src, year=y, key=f"{k}_effect", val=round(d["spm_rate"] - d[f"{k}_excluded"], 1),
                                moe=None, excluded_rate=d[f"{k}_excluded"]))
    return pd.DataFrame(res)


def effects():
    a = xlsx_effects()
    b = pdf_effects()
    df = pd.concat([b, a], ignore_index=True)
    wide = df.pivot_table(index=["source", "year"], columns="key", values="val").reset_index()
    wide["current_year_of_report"] = False
    # mark the newest year in each report (first release of that year)
    for s, g in wide.groupby("source"):
        wide.loc[g.year.idxmax(), "current_year_of_report"] = True
    wide = wide.sort_values(["year", "source"])
    wide.to_csv(os.path.join(OUT, "spm_element_effects_65plus.csv"), index=False)
    return wide


def main():
    os.makedirs(OUT, exist_ok=True)
    opm = hstpov3()
    near = hstpov5()
    spm = spm_hist(opm)
    eff = effects()
    print("Official poverty 65+ (Table 3):",
          opm[opm.year.isin([1959, 1966, 1970, 1980, 1990, 2000, 2010, 2020, 2024, 2025])][["year", "footnote", "a65_pct", "u18_pct", "a18_64_pct"]].to_string(index=False))
    print("\nSPM vs OPM 65+ (P60-290 Table 8):")
    print(spm[["year", "footnote", "a65_pct", "opm_65_pct", "spm_minus_opm_65"]].to_string(index=False))
    print("\nNear poverty 65+ (Table 5), selected:")
    print(near[near.year.isin([1970, 1980, 1990, 2000, 2010, 2019, 2025])][["year", "footnote", "65_below_100", "65_below_150", "65_below_200", "65_100_to_150", "65_100_to_200"]].to_string(index=False))
    print("\nElement effects 65+ (current year of each report):")
    print(eff[eff.current_year_of_report][["year", "source", "spm_rate", "ss_effect", "ssi_effect", "moop_effect"]].to_string(index=False))


if __name__ == "__main__":
    main()
