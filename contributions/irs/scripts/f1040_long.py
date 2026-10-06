"""Long series of Form 1040 retirement-contribution deductions and the saver's credit, 1975-2023.

Builds output/f1040_ira_keogh_deduction_long.csv and output/f1040_savers_credit.csv.

Sources (all IRS SOI):
  * 1975, 1980, 1983-1991: "Table A. Selected Income and Tax Items for Selected Years" in the SOI
    Individual Income Tax Returns complete reports (archive PDFs YYinar.pdf). These PDFs are scans with
    an OCR text layer; values were transcribed by hand below and cross-checked across reports
    (each year appears in 2-4 reports). They are NOT parsed here because the OCR is noisy.
  * 1992: 1992 report (92inar.pdf) Table A/Table 1.4 (IRA split into primary/secondary only).
  * 1993-1998: SOI Table 1.4 spreadsheets (93in14si.xls ... 98in14ar.xls).
  * 1999-2016: SOI historical Table 1 (histab1.xls).
  * 2017-2023: SOI Table 1.4 spreadsheets (17in14ar.xls ... 23in14ar.xls); saver's credit Table 3.3 (YYin33ar.xls).
Run: python3 -I f1040_long.py  (paths are resolved relative to this file)
"""
import os, re, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw', 'f1040')
OUT = os.path.join(ROOT, 'output')
SOI = 'https://www.irs.gov/pub/irs-soi/'

# ---------------------------------------------------------------- hand-transcribed archive values
# (returns, agi_k, wages_k, ira_returns, ira_k, keogh_returns, keogh_k, source, note)
ARCHIVE = {
 1975: (82229332, 947784873, 795399462, 1211794, 1436443, 595892, 1603788,
        '84inar.pdf, 85inar.pdf, 87inar.pdf Table A (1975 column)', 'Same values in all three reports.'),
 1980: (93902469, 1613731497, 1349842802, 2564421, 3430894, 568936, 2007666,
        '84inar.pdf, 87inar.pdf, 89inar.pdf Table A (1980 column)', '89inar OCR shows wages 1,349,942,902; 84/86/87 show 1,349,842,802 (used).'),
 1983: (96321310, 1942589865, 1644572655, 13613167, 32060627, 656038, 2937980,
        '84inar.pdf Table A (1983 column)', 'Only one report gives 1983; OCR-transcribed, not cross-checked.'),
 1984: (99438708, 2139904356, 1807137587, 15232856, 35374424, 648958, 4072409,
        '84inar.pdf and 85inar.pdf Table A (1984 column)', 'All returns: 84inar OCR reads 99,458,708, 85inar reads 99,438,708 (used). Keogh returns 648,958 per 84inar Table A (Table 1.4 OCR 648,956).'),
 1985: (101660287, 2305951483, 1928200978, 16205846, 38211574, 675822, 5181993,
        '85inar.pdf Table A; repeated in 87inar, 89inar, 91inar', 'IRA amount 38,211,574 in 85/87/89/91 reports (86inar shows 38,207,068).'),
 1986: (103045170, 2481681046, 2031025984, 15535531, 37758393, 773296, 6194617,
        '86inar.pdf Table A (1986 column); repeated in 87inar', ''),
 1987: (106996270, 2773824198, 2163905509, 7318727, 14065722, 759083, 6183441,
        '87inar.pdf Table A (1987 column)', 'Wages OCR "2,1163,905,509" read as 2,163,905,509 (6.5% above 1986 as printed).'),
 1988: (109708280, 3083019783, 2337984129, 6361421, 11881754, 814586, 6626908,
        '89inar.pdf, 91inar.pdf, 92inar.pdf Table A (1988 column)', 'Keogh amount 6,626,908 (91/92) vs 6,626,909 (89).'),
 1989: (112135673, 3256358156, 2449530553, 5824914, 10828694, 822363, 6326156,
        '89inar.pdf, 91inar.pdf Table A (1989 column)', ''),
 1990: (113717138, 3405427348, 2599401271, 5223737, 9858219, 824327, 6777645,
        '91inar.pdf Table A (1990 column); 90inar.pdf', ''),
 1991: (114730123, 3464524369, 2674260752, 4666078, 9030177, 840087, 6912855,
        '91inar.pdf Table A (1991 column); Keogh amount from 92inar.pdf Table A', ''),
 1992: (113604503, None, 2805703266, None, 6191865 + 2504195, 919187, 7592136,
        '92inar.pdf Table A (1992 column): primary IRA adjustment 4,036,901 returns/$6,191,865K; spouse 1,837,085/$2,504,195K',
        'IRA returns not published as a single total for 1992 (primary and spouse lines only); amount = primary + spouse. AGI not transcribed.'),
}

def num(v):
    if isinstance(v, (int, float)) and not pd.isna(v):
        return float(v)
    if isinstance(v, str):
        s = v.replace(',', '').replace('*', '').strip()
        try:
            return float(s)
        except ValueError:
            return None
    return None

def find_all_returns_row(df, start):
    for i in range(start, min(start + 12, len(df))):
        v = df.iat[i, 0]
        if isinstance(v, str) and v.strip().lower().startswith('all returns'):
            return i
    raise ValueError('All returns row not found after %d' % start)

def table14_vertical(fname, year):
    """1993-1998 Table 1.4 files: panels stacked vertically."""
    df = pd.read_excel(os.path.join(RAW, fname), sheet_name=0, header=None)
    r0 = find_all_returns_row(df, 0)
    rec = dict(returns=num(df.iat[r0, 1]), agi_k=num(df.iat[r0, 2]), wages_k=num(df.iat[r0, 4]))
    assert 'Salaries' in str(df.iat[r0 - 4, 3]) or 'Salaries' in str(df.iat[r0 - 3, 3]) or 'Salaries' in str(df.iat[r0 - 5, 3])
    prim = sec = tot = keo = None
    for i in range(len(df)):
        for j in range(df.shape[1]):
            v = df.iat[i, j]
            if not isinstance(v, str):
                continue
            if v.strip() == 'Primary IRA payments': prim = (i, j)
            elif v.strip() == 'Secondary IRA payments': sec = (i, j)
            elif v.strip() == 'IRA payments': tot = (i, j)
            elif v.strip() == 'Keogh plan': keo = (i, j)
    def cell(pos):
        r = find_all_returns_row(df, pos[0])
        return num(df.iat[r, pos[1]]), num(df.iat[r, pos[1] + 1])
    if tot:
        rec['ira_returns'], rec['ira_k'] = cell(tot); rec['ira_note'] = ''
    else:
        pn, pa = cell(prim); sn, sa = cell(sec)
        rec['ira_returns'] = None; rec['ira_k'] = pa + sa
        rec['ira_note'] = f'IRA returns not published as one total: primary {int(pn):,} returns/${int(pa):,}K, secondary {int(sn):,}/${int(sa):,}K; amount = sum.'
    rec['keogh_returns'], rec['keogh_k'] = cell(keo)
    return rec

def table14_wide(fname):
    """2016+ Table 1.4: one wide panel."""
    df = pd.read_excel(os.path.join(RAW, fname), sheet_name=0, header=None)
    r0 = find_all_returns_row(df, 0)
    cols = {}
    for i in range(2, 5):
        for j in range(df.shape[1]):
            v = df.iat[i, j]
            if isinstance(v, str):
                t = v.replace('\n', ' ').strip()
                if t == 'IRA payments': cols['ira'] = j
                elif t == 'Payments to a Keogh plan': cols['keogh'] = j
                elif t in ('Salaries and wages', 'Total wages') and 'wages' not in cols: cols['wages'] = j
    assert set(cols) == {'ira', 'keogh', 'wages'}, (fname, cols)
    return dict(returns=num(df.iat[r0, 1]), agi_k=num(df.iat[r0, 2]), wages_k=num(df.iat[r0, cols['wages'] + 1]),
                ira_returns=num(df.iat[r0, cols['ira']]), ira_k=num(df.iat[r0, cols['ira'] + 1]),
                keogh_returns=num(df.iat[r0, cols['keogh']]), keogh_k=num(df.iat[r0, cols['keogh'] + 1]), ira_note='')

def histab1():
    df = pd.read_excel(os.path.join(RAW, 'histab1.xls'), header=None)
    years = [int(y) for y in df.iloc[2, 1:]]
    lab = [str(x).strip() if isinstance(x, str) else '' for x in df[0]]
    def row_after(prefix, k):
        i = next(n for n, s in enumerate(lab) if s.startswith(prefix))
        return [num(v) for v in df.iloc[i + k, 1:]]
    data = dict(returns=row_after('All returns', 0), agi_k=row_after('Adjusted gross income (AGI)', 0),
                wages_k=row_after('Salaries and wages', 2), ira_returns=row_after('Individual Retirement Arrangements deduction', 1),
                ira_k=row_after('Individual Retirement Arrangements deduction', 2), keogh_returns=row_after('Keogh and self-employed retirement plans', 1),
                keogh_k=row_after('Keogh and self-employed retirement plans', 2), sc_returns=row_after('Retirement savings contributions credit', 1),
                sc_k=row_after('Retirement savings contributions credit', 2))
    return {y: {k: v[n] for k, v in data.items()} for n, y in enumerate(years)}

def savers_credit_33(y2):
    df = pd.read_excel(os.path.join(RAW, f'{y2:02d}in33ar.xls'), sheet_name=0, header=None)
    hit = [(i, j) for i in range(8) for j in range(df.shape[1]) if isinstance(df.iat[i, j], str) and 'Retirement savings' in df.iat[i, j]]
    i, j = hit[0]
    sub = [str(df.iat[k, j]) for k in range(i + 1, i + 5)]
    assert any('Number' in s for s in sub) and any('Amount' in str(df.iat[k, j + 1]) for k in range(i + 1, i + 5)), sub
    r = find_all_returns_row(df, i)
    return num(df.iat[r, j]), num(df.iat[r, j + 1])

def main():
    rows = []
    for y, (ret, agi, wag, irn, ira, kn, kk, src, note) in ARCHIVE.items():
        rows.append(dict(year=y, all_returns=ret, agi_k=agi, wages_k=wag, ira_ded_returns=irn, ira_ded_k=ira,
                         keogh_sep_simple_ded_returns=kn, keogh_sep_simple_ded_k=kk,
                         source='IRS SOI, Individual Income Tax Returns (complete report), ' + src + '; archive https://www.irs.gov/statistics/soi-tax-stats-archive-1954-to-1999-individual-income-tax-return-reports',
                         note='Hand-transcribed from OCR text of scanned PDF. ' + note))
    vert = {1993: '93in14si.xls', 1994: '94in14si.xls', 1995: '95in14ar.xls', 1996: '96in14si.xls', 1997: '97in14.xls', 1998: '98in14ar.xls'}
    for y, f in vert.items():
        r = table14_vertical(f, y)
        rows.append(dict(year=y, all_returns=r['returns'], agi_k=r['agi_k'], wages_k=r['wages_k'], ira_ded_returns=r['ira_returns'], ira_ded_k=r['ira_k'],
                         keogh_sep_simple_ded_returns=r['keogh_returns'], keogh_sep_simple_ded_k=r['keogh_k'],
                         source=f'IRS SOI Table 1.4 (all returns: sources of income, adjustments), TY{y}, {SOI}{f}', note=r['ira_note']))
    h = histab1()
    for y in range(1999, 2017):
        r = h[y]
        rows.append(dict(year=y, all_returns=r['returns'], agi_k=r['agi_k'], wages_k=r['wages_k'], ira_ded_returns=r['ira_returns'], ira_ded_k=r['ira_k'],
                         keogh_sep_simple_ded_returns=r['keogh_returns'], keogh_sep_simple_ded_k=r['keogh_k'],
                         source=f'IRS SOI Historical Table 1 (selected income and tax items), {SOI}histab1.xls', note=''))
    for y in range(2017, 2024):
        f = f'{y % 100:02d}in14ar.xls'
        r = table14_wide(f)
        rows.append(dict(year=y, all_returns=r['returns'], agi_k=r['agi_k'], wages_k=r['wages_k'], ira_ded_returns=r['ira_returns'], ira_ded_k=r['ira_k'],
                         keogh_sep_simple_ded_returns=r['keogh_returns'], keogh_sep_simple_ded_k=r['keogh_k'],
                         source=f'IRS SOI Table 1.4, TY{y}, {SOI}{f}', note='Wages = "Salaries and wages" (2022+: "Total wages") amount.'))
    # overlap check 1999 and 2016
    for y, f in [(1999, '99in14ar.xls')]:
        r = table14_vertical(f, y)
        print(f'check {y}: Table 1.4 IRA {r["ira_returns"]:.0f}/{r["ira_k"]:.0f} vs histab1 {h[y]["ira_returns"]:.0f}/{h[y]["ira_k"]:.0f}')
    r = table14_wide('16in14ar.xls')
    print(f'check 2016: Table 1.4 IRA {r["ira_returns"]:.0f}/{r["ira_k"]:.0f} vs histab1 {h[2016]["ira_returns"]:.0f}/{h[2016]["ira_k"]:.0f}')
    d = pd.DataFrame(rows).sort_values('year')
    d['pct_returns_ira_ded'] = (100 * d.ira_ded_returns / d.all_returns).round(2)
    d['ira_ded_pct_agi'] = (100 * d.ira_ded_k / d.agi_k).round(3)
    d['ira_ded_pct_wages'] = (100 * d.ira_ded_k / d.wages_k).round(3)
    d['avg_ira_ded_dollars'] = (1000 * d.ira_ded_k / d.ira_ded_returns).round(0)
    d['pct_returns_keogh_ded'] = (100 * d.keogh_sep_simple_ded_returns / d.all_returns).round(2)
    d['keogh_ded_pct_agi'] = (100 * d.keogh_sep_simple_ded_k / d.agi_k).round(3)
    d['definition'] = ('Form 1040 adjustment for deductible traditional-IRA contributions ("IRA payments"; returns, not persons; excludes Roth and nondeductible contributions) '
                       'and the self-employed SEP/SIMPLE/qualified (Keogh) plan deduction. Percent of all returns filed; percent of AGI less deficit; percent of salaries and wages on returns. Amounts in $ thousands, current dollars.')
    cols = ['year', 'all_returns', 'agi_k', 'wages_k', 'ira_ded_returns', 'ira_ded_k', 'pct_returns_ira_ded', 'ira_ded_pct_agi', 'ira_ded_pct_wages', 'avg_ira_ded_dollars',
            'keogh_sep_simple_ded_returns', 'keogh_sep_simple_ded_k', 'pct_returns_keogh_ded', 'keogh_ded_pct_agi', 'definition', 'source', 'note']
    d[cols].to_csv(os.path.join(OUT, 'f1040_ira_keogh_deduction_long.csv'), index=False)
    print(d[['year', 'ira_ded_returns', 'ira_ded_k', 'pct_returns_ira_ded', 'ira_ded_pct_agi', 'keogh_sep_simple_ded_k', 'keogh_ded_pct_agi']].to_string(index=False))

    sc = []
    for y in range(2002, 2017):
        r = h[y]
        sc.append(dict(year=y, savers_credit_returns=r['sc_returns'], savers_credit_k=r['sc_k'], all_returns=r['returns'],
                       source=f'IRS SOI Historical Table 1, {SOI}histab1.xls'))
    for y in range(2017, 2024):
        n, a = savers_credit_33(y % 100)
        ret = d.loc[d.year == y, 'all_returns'].iat[0]
        sc.append(dict(year=y, savers_credit_returns=n, savers_credit_k=a, all_returns=ret,
                       source=f'IRS SOI Table 3.3 (tax liability, tax credits), TY{y}, {SOI}{y % 100:02d}in33ar.xls; all returns from Table 1.4'))
    s = pd.DataFrame(sc)
    s['pct_returns'] = (100 * s.savers_credit_returns / s.all_returns).round(2)
    s['avg_credit_dollars'] = (1000 * s.savers_credit_k / s.savers_credit_returns).round(0)
    s['note'] = 'Retirement savings contributions credit (Form 8880), nonrefundable; counts returns claiming a credit that reduced tax (credit limited to tax liability).'
    s.to_csv(os.path.join(OUT, 'f1040_savers_credit.csv'), index=False)
    print(s[['year', 'savers_credit_returns', 'savers_credit_k', 'pct_returns', 'avg_credit_dollars']].to_string(index=False))

if __name__ == '__main__':
    main()
