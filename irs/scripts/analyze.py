"""IRS SOI IRA tables: revision check, rollover-flag reconciliation, Form 1040 comparison, TY2024 status.

Inputs (all under irs/raw/ unless noted):
  raw/irs_soi/YYin01ira.xls[x]  SOI IRA Table 1 (by type of plan), TY2004-2023
  raw/irs_soi/YYin04ira.xls[x]  SOI IRA Table 4 (by age), TY2004-2023
  raw/irs_soi/22in01iraci.xlsx  95% confidence intervals for TY2022 Table 1
  raw/irs_soi/22in05ira.xlsx, 22in06ira.xlsx  TY2022 Tables 5/6 (contributions), June 2026 vintage
  raw/ici/ret_26_q2_data.xls    ICI "The US Retirement Market, Second Quarter 2026" data, Table 11
  ../data/recovered_irs/js_559.txt, js_563.txt, js_386.txt  earlier extractions (read-only)
  Publication 4801 PDFs (too large for raw/): path in env P4801_DIR (default: scratch); if absent the
  hard-coded Form 1040 line 4a values below are used (each with file + page).

Outputs: irs/output/*.csv, *.json. Run: python irs/scripts/analyze.py
"""
import csv, json, os, re, subprocess, sys
import openpyxl, xlrd, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
IRS = os.path.dirname(HERE)
ROOT = os.path.dirname(IRS)
RAW = os.path.join(IRS, 'raw', 'irs_soi')
OUT = os.path.join(IRS, 'output')
REC = os.path.join(ROOT, 'data', 'recovered_irs')
P4801_DIR = os.environ.get('P4801_DIR', '/tmp/claude-0/-home-user/c85909ce-0f00-574a-b15f-202e4f154f6a/scratchpad/irs')
os.makedirs(OUT, exist_ok=True)


def num(v):
    s = re.sub(r'[*,\s$]', '', str(v if v is not None else ''))
    try:
        f = float(s)
    except ValueError:
        return None
    return None if f != f else f


def read_rows(path):
    """Return the first sheet as a list of rows (python values), 0-based, plus a cell-address helper."""
    if path.endswith('.xls'):
        sh = xlrd.open_workbook(path).sheet_by_index(0)
        return [[sh.cell_value(r, c) for c in range(sh.ncols)] for r in range(sh.nrows)]
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    return [[c.value for c in row] for row in ws.iter_rows()]


def col_letter(i):
    s = ''
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def cell(r, c):
    return f'{col_letter(c)}{r + 1}'


def find_cols(rows):
    """Locate header row and the 'Rollovers', 'Withdrawals', 'fair market value' column starts."""
    for i, r in enumerate(rows):
        txt = [str(x or '') for x in r]
        if any(re.search('Withdrawals', t) for t in txt):
            w = next(j for j, t in enumerate(txt) if re.search('Withdrawals', t))
            f = next(j for j, t in enumerate(txt) if j > w and re.search('fair market', t, re.I))
            ro = next(j for j, t in enumerate(txt) if re.match(r'\s*Rollovers', t))
            cv = next(j for j, t in enumerate(txt) if re.search('Roth conversions', t))
            return i, ro, cv, w, f
    raise ValueError('header not found')


def fname(y, t):
    for ext in ('xlsx', 'xls'):
        p = os.path.join(RAW, f'{y % 100:02d}in{t:02d}ira.{ext}')
        if os.path.exists(p):
            return p
    return None


AGE_U60 = re.compile(r'^(Under 15|Under 20|15 under 20|20 under 25|25 under 30|30 under 35|35 under 40|40 under 45|45 under 50|50 under 55|55 under 60)$', re.I)
SINGLE = {'60 under 65': '60-64', '65 under 70': '65-69', '70 under 75': '70-74', '75 under 80': '75-79', '80 and over': '80+'}


def parse_table4(y):
    p = fname(y, 4)
    rows = read_rows(p)
    h, ro, cv, w, f = find_cols(rows)
    g = {k: dict(wn=0, wa=0, hn=0, fa=0, rn=0, ra=0, cn=0, ca=0) for k in ['all', 'noage', 'u60', '60-64', '65-69', '70-74', '75-79', '80+']}
    cells = {}
    for i in range(h + 1, len(rows)):
        lab = re.sub(r'\s+', ' ', str(rows[i][0] or '')).strip()
        if not lab:
            continue
        key = None
        if re.match('^All taxpayers', lab, re.I):
            key = 'all'
        elif re.match('^No age', lab, re.I):
            key = 'noage'
        elif AGE_U60.match(lab):
            key = 'u60'
        elif lab in SINGLE:
            key = SINGLE[lab]
        elif re.match(r'^(\[|\*|Note|Source|n\.a|N/A)', lab, re.I):
            break
        if key:
            r = rows[i]
            vals = dict(wn=num(r[w]), wa=num(r[w + 1]), hn=num(r[f]), fa=num(r[f + 1]), rn=num(r[ro]), ra=num(r[ro + 1]), cn=num(r[cv]), ca=num(r[cv + 1]))
            for k, v in vals.items():
                g[key][k] += v or 0
            if key != 'u60':
                cells[key] = dict(row=i + 1, wn=cell(i, w), wa=cell(i, w + 1), hn=cell(i, f), fa=cell(i, f + 1), rn=cell(i, ro), ra=cell(i, ro + 1))
    for a, parts in {'60-69': ['60-64', '65-69'], '70+': ['70-74', '75-79', '80+']}.items():
        g[a] = {k: sum(g[p][k] for p in parts) for k in g['all']}
    g = {k: {kk: int(round(vv)) for kk, vv in v.items()} for k, v in g.items()}
    return g, cells, os.path.basename(p)


def parse_table1(y):
    p = fname(y, 1)
    rows = read_rows(p)
    h, ro, cv, w, f = find_cols(rows)
    out = {}
    for i in range(h + 1, len(rows)):
        lab = re.sub(r'\s+', ' ', str(rows[i][0] or '')).strip()
        key = None
        if re.match('^Total', lab, re.I): key = 'total'
        elif re.match('^Traditional', lab, re.I): key = 'trad'
        elif re.match('^Roth', lab, re.I): key = 'roth'
        elif re.match('^SEP', lab, re.I): key = 'sep'
        elif re.match('^SIMPLE', lab, re.I): key = 'simple'
        if key and key not in out:
            r = rows[i]
            out[key] = dict(wn=num(r[w]), wa=num(r[w + 1]), hn=num(r[f]), fa=num(r[f + 1]), rn=num(r[ro]), ra=num(r[ro + 1]), cn=num(r[cv]), ca=num(r[cv + 1]), contrib_n=num(r[1]), contrib_a=num(r[2]),
                            _cells=dict(row=i + 1, ra=cell(i, ro + 1), wa=cell(i, w + 1), fa=cell(i, f + 1), ca=cell(i, cv + 1), contrib_a=cell(i, 2)))
    # vintage line
    src = ''
    for r in rows:
        for x in r:
            if isinstance(x, str) and 'Individual Retirement Arrangements Study' in x:
                src = re.search(r'Study,\s*([A-Za-z]+ \d{4})', x).group(1)
    return out, os.path.basename(p), src


def recovered(fn):
    t = open(os.path.join(REC, fn)).read().split('### RESULT\n', 1)[1]
    s = t.split('\n\n(captured at origin')[0].strip()
    return json.loads(s) if s.startswith('"') else s


YEARS = list(range(2004, 2024))
T4 = {}; T4cells = {}; T4file = {}
T1 = {}; T1file = {}; T1vint = {}
for y in YEARS:
    T4[y], T4cells[y], T4file[y] = parse_table4(y)
    T1[y], T1file[y], T1vint[y] = parse_table1(y)

# ---------------------------------------------------------------- 1. revision check vs js_559 / js_563
rev = []
old559 = {}
for line in recovered('js_559.txt').strip().split('\n')[1:]:
    p = [x.strip() for x in line.split('|')]
    old559.setdefault(int(p[0]), {})[p[1]] = dict(wn=int(p[2]), wa=int(p[3]), hn=int(p[4]), fa=int(p[5]))
n_cells = n_diff = 0
for y in YEARS:
    for g, d in old559[y].items():
        for k in ['wn', 'wa', 'hn', 'fa']:
            new = T4[y][g][k]; old = d[k]; n_cells += 1
            diff = new - old
            if diff != 0:
                n_diff += 1
            rev.append(dict(table='Table 4 (by age)', file=T4file[y], year=y, group=g, field=k, js559_value=old, current_value=new, diff=diff,
                            pct_diff=round(100 * diff / old, 4) if old else '', cell=T4cells[y].get(g, {}).get(k, 'sum of rows')))
with open(os.path.join(OUT, 'revisions_js559_table4_vs_current.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rev[0])); wr.writeheader(); wr.writerows(rev)
rev559_summary = dict(cells_compared=n_cells, cells_different=n_diff, max_abs_diff=max(abs(r['diff']) for r in rev))

rev1 = []
for line in recovered('js_563.txt').strip().split('\n')[1:]:
    p = line.split('|'); y = int(p[0]); k = p[1]
    for fld, idx in [('wn', 2), ('wa', 3), ('hn', 4), ('fa', 5)]:
        old = num(p[idx]); new = T1[y].get(k, {}).get(fld)
        if old is None and new is None:
            continue
        rev1.append(dict(table='Table 1 (by type)', file=T1file[y], year=y, type=k, field=fld, js563_value=old, current_value=new,
                         diff=(new - old) if (old is not None and new is not None) else '', cell=T1[y][k]['_cells'].get(fld, '') if k in T1[y] else ''))
with open(os.path.join(OUT, 'revisions_js563_table1_vs_current.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rev1[0])); wr.writeheader(); wr.writerows(rev1)
rev563_summary = dict(cells_compared=len(rev1), cells_different=sum(1 for r in rev1 if r['diff'] not in ('', 0, 0.0)))

# ---------------------------------------------------------------- 2. current Table 4 series in irs_derived.json structure (+ rollovers)
groups = ['u60', '60-64', '65-69', '70-74', '75-79', '80+', '60-69', '70+', 'all']
inc = {y: [round(100 * T4[y][g]['wn'] / T4[y][g]['hn'], 1) for g in groups] for y in YEARS}
rate_prior = {y: [round(100 * T4[y][g]['wa'] / T4[y - 1][g]['fa'], 2) for g in groups] for y in YEARS if y - 1 in T4}
rate_same = {y: [round(100 * T4[y][g]['wa'] / T4[y][g]['fa'], 2) for g in groups] for y in YEARS}
t1_out = {y: {k: {kk: vv for kk, vv in v.items() if kk != '_cells'} for k, v in T1[y].items()} for y in YEARS}
json.dump(dict(note='Re-parsed from IRS SOI files downloaded 2026-10-04 (see irs/raw/irs_soi_manifest.csv). Same keys as data/irs_derived.json; '
                    'age groups add rn/ra (rollovers: taxpayers, $K) and cn/ca (Roth conversions). Amounts in $ thousands. '
                    'Group order for inc/rate arrays: ' + ','.join(groups) + '. TY2022-2023 are a new SOI series (revised methodology, June 2026).',
               files=dict(table4=T4file, table1=T1file), vintage_table1=T1vint, group_order=groups,
               age=T4, inc=inc, rate_prior=rate_prior, rate_same=rate_same, t1=t1_out),
          open(os.path.join(OUT, 'irs_soi_ira_2004_2023_current.json'), 'w'), indent=1)

# ---------------------------------------------------------------- 3. rollover flag: vintages of TY2022
ici_old = recovered('js_386.txt')
m = re.search(r'\n2022\|([\d.,]+)\|([\d.,]+)\|([\d.,]+)\|([\d.,]+)\|([\d.,]+)', ici_old)
ici_old22 = dict(contributions=num(m.group(1)), rollovers=num(m.group(2)), conversions=num(m.group(3)), withdrawals=num(m.group(4)), assets=num(m.group(5)))
ici_new = pd.read_excel(os.path.join(IRS, 'raw', 'ici', 'ret_26_q2_data.xls'), sheet_name='Table 11', header=None)
ici_rows = {}
for i, r in ici_new.iterrows():
    try:
        yr = int(float(r[0]))
    except (ValueError, TypeError):
        continue
    vals = [num(x) for x in r[1:] if num(x) is not None]
    ici_rows[yr] = (i + 1, vals)
ci = read_rows(os.path.join(RAW, '22in01iraci.xlsx'))
def ci_range(rw, c):
    a, b = re.findall(r'[\d,]+', ci[rw][c]); return num(a), num(b)
tr22, tot22 = T1[2022]['trad'], T1[2022]['total']
roll = []
def add(src, file, cellref, measure, value_bn, note=''):
    roll.append(dict(source=src, file=file, cell=cellref, measure=measure, value_billion=round(value_bn, 1), note=note))
add('ICI IRA Investor Database data file (pre-June-2026 vintage)', 'https://www.ici.org/files/2026/tax-year-2023-rpt-ira-traditional-data.xlxs (as extracted in data/recovered_irs/js_386.txt)', 'Figure A.26, row 2022, Rollovers', 'Traditional IRA rollovers 2022', ici_old22['rollovers'], 'Cites "ICI and IRS SOI"; built from the Feb-2025 SOI TY2022 release (former methodology)')
add('ICI Research Perspective 32(7), June 2026 (released 3 Jun 2026)', 'https://www.ici.org/system/files/2026-06/per32-07.pdf', 'p.4 text + note 21 ("See Internal Revenue Service, Statistics of Income Division 2025")', 'Rollovers to traditional IRAs 2022 (rounded)', 670.0, 'Cites the SOI 2025 web release')
add('IRS SOI Table 1, TY2022 (June 2026, revised methodology)', '22in01ira.xlsx', tr22['_cells']['ra'], 'Traditional IRA rollovers 2022', tr22['ra'] / 1e6)
add('IRS SOI Table 1, TY2022 (June 2026, revised methodology)', '22in01ira.xlsx', tot22['_cells']['ra'], 'All-IRA rollovers 2022', tot22['ra'] / 1e6)
lo, hi = ci_range(6, 6)
add('IRS SOI Table 1CI, TY2022 (June 2026)', '22in01iraci.xlsx', 'G7', 'Traditional rollovers 2022, 95% CI', lo / 1e6, f'upper bound {hi/1e6:.1f}; ICI 669.8 lies above it')
lo, hi = ci_range(5, 6)
add('IRS SOI Table 1CI, TY2022 (June 2026)', '22in01iraci.xlsx', 'G6', 'All-IRA rollovers 2022, 95% CI', lo / 1e6, f'upper bound {hi/1e6:.1f}')
r22 = ici_rows[2022]
add('ICI, The US Retirement Market, Q2 2026 data (posted 17 Sep 2026)', 'https://www.ici.org/statistical-report/ret_26_q2_data.xls', f'Table 11, row {r22[0]} (2022), Rollovers', 'Traditional IRA rollovers 2022 (ICI current)', r22[1][1], 'ICI has adopted the June-2026 SOI figure')
r23 = ici_rows[2023]
add('ICI, The US Retirement Market, Q2 2026 data', 'ret_26_q2_data.xls', f'Table 11, row {r23[0]} (2023), Rollovers', 'Traditional IRA rollovers 2023 (ICI current)', r23[1][1])
add('IRS SOI Table 1, TY2023 (June 2026)', '23in01ira.xlsx', T1[2023]['trad']['_cells']['ra'], 'Traditional IRA rollovers 2023', T1[2023]['trad']['ra'] / 1e6)
for y in (2020, 2021):
    add(f'IRS SOI Table 1, TY{y} ({T1vint[y]})', T1file[y], T1[y]['trad']['_cells']['ra'], f'Traditional IRA rollovers {y}', T1[y]['trad']['ra'] / 1e6, f'ICI old and new files both show {ici_rows[y][1][1]}')
with open(os.path.join(OUT, 'rollover_2022_flag_reconciliation.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(roll[0])); wr.writeheader(); wr.writerows(roll)

# Side-by-side of all five ICI traditional-IRA flow items, 2022: old ICI vintage vs current IRS/ICI
side = []
for item, old, new_irs, cellref in [
        ('contributions', ici_old22['contributions'], tr22['contrib_a'] / 1e6, tr22['_cells']['contrib_a']),
        ('rollovers', ici_old22['rollovers'], tr22['ra'] / 1e6, tr22['_cells']['ra']),
        ('Roth conversions (Roth row)', ici_old22['conversions'], T1[2022]['roth']['ca'] / 1e6, T1[2022]['roth']['_cells']['ca']),
        ('withdrawals', ici_old22['withdrawals'], tr22['wa'] / 1e6, tr22['_cells']['wa']),
        ('year-end assets', ici_old22['assets'], tr22['fa'] / 1e6, tr22['_cells']['fa'])]:
    side.append(dict(item=item, ici_old_vintage_bn=old, irs_jun2026_bn=round(new_irs, 1), irs_cell_22in01ira=cellref, change_bn=round(new_irs - old, 1), change_pct=round(100 * (new_irs - old) / old, 1)))
with open(os.path.join(OUT, 'traditional_ira_2022_vintage_comparison.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(side[0])); wr.writeheader(); wr.writerows(side)

# Table 5 (contributions) cross-vintage evidence: CRS R48051 (Dec 2025) quoted the earlier TY2022 Table 5
t5 = read_rows(os.path.join(RAW, '22in05ira.xlsx')); t6 = read_rows(os.path.join(RAW, '22in06ira.xlsx'))
vint5 = dict(crs_old_trad_n=4989322, crs_old_trad_avg=4510, crs_old_roth_n=10036960, crs_old_roth_avg=3482,
             jun2026_trad_n=t5[6][1], jun2026_trad_amt_K=t5[6][2], jun2026_roth_n=t6[6][1], jun2026_roth_amt_K=t6[6][2],
             cells='22in05ira.xlsx B7:C7; 22in06ira.xlsx B7:C7')

# ---------------------------------------------------------------- 4. Form 1040 line 4a vs SOI IRA-study withdrawals
F1040 = {  # gross IRA distributions, Form 1040 line 4a, all returns: (returns, amount $K, file, PDF page of returns, PDF page of amounts)
    2019: (16495748, 379260994, 'p4801--2021.pdf (Pub 4801 Rev. 12-2021, TY2019)'),
    2020: (14205309, 353034392, 'p4801--2022.pdf (Pub 4801 Rev. 11-2022, TY2020)'),
    2021: (16635357, 473451893, 'p4801--2024.pdf (Pub 4801 Rev. 2-2024, TY2021)'),
    2022: (17355700, 497467733, 'p4801--122024.pdf (Pub 4801 Rev. 12-2024, TY2022)'),
    2023: (17839121, 505480278, 'p4801.pdf (Pub 4801 Rev. 6-2026, TY2023)'),
}
URL4801 = {2019: 'https://www.irs.gov/pub/irs-prior/p4801--2021.pdf', 2020: 'https://www.irs.gov/pub/irs-prior/p4801--2022.pdf',
           2021: 'https://www.irs.gov/pub/irs-prior/p4801--2024.pdf', 2022: 'https://www.irs.gov/pub/irs-prior/p4801--122024.pdf',
           2023: 'https://www.irs.gov/pub/irs-pdf/p4801.pdf'}


def page_of(pdf, needle_num):
    """Return the first page whose text holds '4a ... IRA distributions ... <needle>' (verifies the constant)."""
    try:
        n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    except Exception:
        return None
    s = f'{needle_num:,}'
    for p in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout
        if re.search(r'4a\s+IRA distributions[ .]*4a\s+' + re.escape(s), t):
            return p
    return None


cmp_rows = []
for y, (nret, amt, src) in F1040.items():
    pdf = os.path.join(P4801_DIR, src.split(' ')[0])
    pg_n = page_of(pdf, nret) if os.path.exists(pdf) else None
    pg_a = page_of(pdf, amt) if os.path.exists(pdf) else None
    t = T1[y]['total']
    soi_w = t['wa']; soi_c = t['ca'] or 0
    cmp_rows.append(dict(
        tax_year=y,
        f1040_line4a_returns=nret, f1040_line4a_amount_K=amt, f1040_source=src, f1040_url=URL4801[y],
        f1040_pdf_page_returns=pg_n if pg_n else 'not re-checked', f1040_pdf_page_amounts=pg_a if pg_a else 'not re-checked',
        soi_ira_withdrawers=int(t['wn']), soi_ira_withdrawals_K=int(soi_w), soi_file=T1file[y], soi_cell=t['_cells']['wa'], soi_vintage=T1vint[y],
        soi_roth_conversions_K=int(soi_c), soi_conv_cell=t['_cells']['ca'],
        gap_withdrawals_vs_4a_pct=round(100 * (soi_w / amt - 1), 2),
        gap_withdrawals_plus_conversions_vs_4a_pct=round(100 * ((soi_w + soi_c) / amt - 1), 2)))
with open(os.path.join(OUT, 'form1040_vs_soi_ira_withdrawals_2019_2023.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(cmp_rows[0])); wr.writeheader(); wr.writerows(cmp_rows)

# ---------------------------------------------------------------- 5. TY2024 status
status = dict(checked_utc='2026-10-04',
              landing_page='https://www.irs.gov/statistics/soi-tax-stats-accumulation-and-distribution-of-individual-retirement-arrangements',
              landing_reviewed='12-Jun-2026', latest_tax_year_listed=2023,
              probes={u: 404 for u in ['https://www.irs.gov/pub/irs-soi/24in01ira.xlsx', 'https://www.irs.gov/pub/irs-soi/24in04ira.xlsx', 'https://www.irs.gov/pub/irs-soi/24in01ira.xls']},
              whats_new='https://www.irs.gov/statistics/soi-tax-stats-whats-new (reviewed 29-Sep-2026): no TY2024 IRA release announced; upcoming releases listed to 27 Oct 2026 do not include IRAs',
              ty2024_released=False)
json.dump(status, open(os.path.join(OUT, 'ty2024_status.json'), 'w'), indent=1)

json.dump(dict(rev559=rev559_summary, rev563=rev563_summary, ici_old22=ici_old22, vintage_table5=vint5), open(os.path.join(OUT, 'summary.json'), 'w'), indent=1, default=str)

# ---------------------------------------------------------------- print
print('Table 1 vintages:', {y: T1vint[y] for y in YEARS})
print('js_559 vs current:', rev559_summary)
print('js_563 vs current:', rev563_summary)
for r in rev:
    if r['diff'] != 0:
        print('  DIFF559', r)
for r in rev1:
    if r['diff'] not in ('', 0, 0.0):
        print('  DIFF563', r)
print('\nRollover flag'); [print(' ', r) for r in roll]
print('\nTraditional IRA 2022, ICI old vintage vs IRS June 2026'); [print(' ', r) for r in side]
print('Table 5/6 vintages', vint5)
print('\nForm 1040 comparison')
for r in cmp_rows:
    print(r['tax_year'], r['f1040_line4a_amount_K'], r['soi_ira_withdrawals_K'], r['gap_withdrawals_vs_4a_pct'], r['gap_withdrawals_plus_conversions_vs_4a_pct'], 'pages', r['f1040_pdf_page_returns'], r['f1040_pdf_page_amounts'])
