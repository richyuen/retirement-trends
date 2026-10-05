"""Build IRS SOI early-distribution additional-tax series (stayinplan task 2026-10-04; extended by gapC 2026-10-05).

Inputs:
  - SOI Table 3.3 (Pub 1304), YYin33ar.xls TY1996, TY1998-2023 and 97in33.xls (TY1997), all in this folder.
    Source: https://www.irs.gov/pub/irs-soi/YYin33ar.xls (TY1997: https://www.irs.gov/pub/irs-soi/97in33.xls)
    Column used: "Penalty tax on qualified retirement plans" (= Form 1040 Schedule 2 line 8 in recent years,
    "Additional tax on IRAs or other tax-favored accounts"; TY2021 value 4,484,060 returns matches Pub 4801 TY2021
    p.27 exactly). Row "All returns, total". In TY1996-2001 the column sits in a lower panel of the sheet
    ("All other taxes"), not in the top header rows; the parser searches the whole sheet.
    The earliest Table 3.3 spreadsheet SOI posts is TY1996; nothing earlier is online at irs.gov.
  - Taxable IRA + taxable pension/annuity amounts (Form 1040): TY1996-1998 from SOI Table 1.4
    (96in14si.xls, 97in14.xls, 98in14ar.xls, "Total taxable IRA distributions" and "Pensions and annuities, taxable",
    All returns row); TY1999+ from notes/rmd_policy_tax_data.md Chart-ready series A and B (SOI / FRED / Pub 1304 / Pub 4801).
  - Form 5329 Part I line-item estimates (Pub 4801 and its predecessor "Estimated Data Line Counts", TY2003-2023),
    hard-coded below with page refs. TY2003-2008 publish only lines 3-4.
Outputs: ../../output/irs_early_distribution_penalty.csv and ../../output/irs_form5329_part1.csv
"""
import csv, glob, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'output')

# Form 1040 taxable IRA distributions and taxable pensions & annuities ($K)
taxable_ira = {1996: 45538743, 1997: 55182520, 1998: 74094367, 1999: 87140912, 2000: 98966627, 2001: 94327585,
               2002: 88219481, 2003: 88335605, 2004: 101672181, 2005: 112277199, 2006: 124705552, 2007: 147959327,
               2008: 162150226, 2009: 135202708, 2010: 194332950, 2011: 217319190, 2012: 230783461, 2013: 213602353,
               2014: 235005032, 2015: 253213041, 2016: 257507903, 2017: 286496949, 2019: 324971510, 2020: 284005168,
               2021: 408382461, 2022: 437775580, 2023: 438147938}
taxable_pen = {1996: 238786811, 1997: 259711251, 1998: 280650198, 1999: 304310714, 2000: 325827702, 2001: 338745409,
               2002: 357840960, 2003: 372931442, 2004: 394285849, 2005: 420144855, 2006: 450454465, 2007: 490581465,
               2008: 506269008, 2009: 523295800, 2010: 558540932, 2011: 581180358, 2012: 612544219, 2013: 638659076,
               2014: 663223262, 2015: 689991999, 2016: 693626543, 2017: 729187412, 2019: 784497673, 2020: 827597726,
               2021: 858038339, 2022: 911698884, 2023: 932130236}
taxable_2018_combined = 1087228437  # 2018 combined IRA+pension taxable line (Pub 4801 TY2018)
denom_src = {1996: 'https://www.irs.gov/pub/irs-soi/96in14si.xls', 1997: 'https://www.irs.gov/pub/irs-soi/97in14.xls',
             1998: 'https://www.irs.gov/pub/irs-soi/98in14ar.xls'}


def is_pen_header(v):
    return isinstance(v, str) and 'penalty tax on qualified' in v.lower().replace('\n', ' ')


def is_all_returns(v):
    return isinstance(v, str) and v.strip().lower().startswith('all returns')


def parse(f):
    df = pd.read_excel(f, header=None)
    # total returns: first "All returns" row, column 1
    first = next(i for i in range(len(df)) if is_all_returns(df.iat[i, 0]))
    tot = int(df.iat[first, 1])
    # penalty column: search whole sheet (TY1996-2001 put it in a lower panel)
    r0, col = next((i, j) for i in range(len(df)) for j in range(df.shape[1]) if is_pen_header(df.iat[i, j]))
    row = next(i for i in range(r0, len(df)) if is_all_returns(df.iat[i, 0]))
    return tot, int(df.iat[row, col]), int(df.iat[row, col + 1])


rows = []
files = sorted(glob.glob(os.path.join(HERE, '*in33ar.xls')) + glob.glob(os.path.join(HERE, '97in33.xls')))
for f in files:
    base = os.path.basename(f)
    yy = int(base[:2]); yr = (1900 if yy >= 90 else 2000) + yy
    tot, n, amt = parse(f)
    taxable = taxable_2018_combined if yr == 2018 else taxable_ira[yr] + taxable_pen[yr]
    note = ''
    if yr == 2020:
        note = 'CARES Act: CRDs exempt from 10% tax'
    elif yr == 2018:
        note = '2018: denominator = combined IRA+pension taxable line'
    elif yr <= 1998:
        note = f'denominator from SOI Table 1.4 ({denom_src[yr]})'
    rows.append({
        'tax_year': yr,
        'all_returns': tot,
        'returns_with_penalty_tax': n,
        'pct_of_all_returns_computed': round(100 * n / tot, 2),
        'penalty_tax_amount_thousand_usd': amt,
        'implied_penalized_distributions_billion_usd_computed': round(amt / 0.10 / 1e6, 1),
        'penalty_tax_per_100usd_taxable_ira_pension_distributions_computed': round(100 * amt / taxable, 3),
        'note': note,
        'source_url': f'https://www.irs.gov/pub/irs-soi/{base}',
    })
rows.sort(key=lambda r: r['tax_year'])
with open(os.path.join(OUT, 'irs_early_distribution_penalty.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# Form 5329 Part I (Additional tax on early distributions), SOI line-item estimates.
# (forms_filed, l1 returns, l1 $K, l2 returns, l2 $K, l3 returns, l3 $K, l4 returns, l4 $K, url, pdf pages)
# None = line not published that year. TY2003 amount page in p4801--2005 repeats the count page, so amounts are omitted.
P = 'https://www.irs.gov/pub/irs-prior/'
f5329 = {
 2003: (1310019, None, None, None, None, 1204919, None, 1199692, None, P + 'p4801--2005.pdf', '69 (counts only)'),
 2004: (1420645, None, None, None, None, 1199916, 11387977, 1183326, 1152233, P + 'p4801--2006.pdf', '58, 138'),
 2005: (1540846, None, None, None, None, 1095447, 10553068, 1082489, 1063973, P + 'p4801--2007.pdf', '67, 155'),
 2006: (1469483, None, None, None, None, 1185109, 11876673, 1184932, 1203007, P + 'p4801--2008.pdf', '68, 162'),
 2007: (1479094, None, None, None, None, 1193950, 13270709, 1185681, 1346454, P + 'p4801--2009.pdf', '67, 159'),
 2008: (1555643, None, None, None, None, 1234843, 13886804, 1225466, 1400346, P + 'p4801--2010.pdf', '71, 169'),
 2009: (1823910, 1452186, 19538845, 408897, 4707348, 1251019, 14831497, 1239998, 1503229, P + 'p4801--2011.pdf', '122-123'),
 2010: (2248795, 1762130, 24360307, 698210, 8344873, 1291460, 16015434, 1282186, 1610256, P + 'p4801--2012.pdf', '123-124'),
 2011: (2204937, 1671414, 22293534, 649615, 7179766, 1244696, 15113768, 1232500, 1517325, P + 'p4801--2013.pdf', '133-134'),
 2012: (2320131, 1706380, 22819432, 791396, 7659135, 1229552, 15160297, 1205886, 1526507, P + 'p4801--2014.pdf', '119-120'),
 2013: (2381823, 1669640, 23520908, 772196, 8267029, 1215507, 15253879, 1206104, 1540840, P + 'p4801--2015.pdf', '123-124'),
 2014: (2510510, 1837199, 24875706, 816942, 9010883, 1328005, 15864822, 1313958, 1594639, P + 'p4801--2016.pdf', '123-124'),
 2015: (2403290, 1650294, 24436592, 774554, 8712380, 1196134, 15724213, 1184816, 1578045, P + 'p4801--2017.pdf', '123-124'),
 2016: (2478312, 1670459, 24144927, 749543, 8638543, 1219361, 15506384, 1205095, 1558169, 'https://www.irs.gov/pub/irs-soi/16inlinecount.pdf', '139-140'),
 2017: (2344142, 1655273, 26977109, 793554, 10787076, 1165832, 16190033, 1142057, 1634677, P + 'p4801--2019.pdf', '127-128'),
 2018: (2501861, 1731906, 26887443, 787969, 9439520, 1258116, 17447923, 1239327, 1762775, P + 'p4801--2020.pdf', '133-134'),
 2019: (2581137, 1744375, 26119515, 747595, 9741192, 1273561, 16378322, 1269309, 1664419, P + 'p4801--2021.pdf', '123-124'),
 2020: (2590504, 1685945, 27466424, 987305, 18259286, 884241, 9207138, 868688, 930493, P + 'p4801--2022.pdf', '121-122'),
 2021: (2551270, 1556847, 25676915, 607967, 9124823, 1151337, 16540898, 1142430, 1664968, P + 'p4801--2024.pdf', '143-144'),
 2022: (2679325, 1667143, 28327509, 658908, 9985273, 1255846, 18339225, 1241259, 1848451, P + 'p4801--122024.pdf', '131-132'),
 2023: (2939286, 1916967, 132957756, 754282, 110788817, 1464637, 22165542, 1451618, 2238517, 'https://www.irs.gov/pub/irs-pdf/p4801.pdf', '131-132'),
}
NOTE_2023 = ('L1/L2 dollars as printed by SOI (verified pp.131-132) but implausible: L1 +$105B and L2 +$101B vs 2022 '
             'while L3/L4 and all aggregates move normally; avg excepted amount per excepting return $146.9K vs $15.2K '
             '(2022). Not a parsing or definition change; likely sample outlier/capture error. Use L3/L4 only.')
sched2 = {r['tax_year']: (r['returns_with_penalty_tax'], r['penalty_tax_amount_thousand_usd']) for r in rows}
out2 = []
for y, v in sorted(f5329.items()):
    ff, n1, a1, n2, a2, n3, a3, n4, a4, url, pg = v
    out2.append({
        'tax_year': y, 'form5329_forms_filed': ff,
        'l1_early_distributions_returns': n1, 'l1_early_distributions_thousand_usd': a1,
        'l2_excepted_returns': n2, 'l2_excepted_thousand_usd': a2,
        'l3_subject_to_tax_returns': n3, 'l3_subject_to_tax_thousand_usd': a3,
        'l4_additional_tax_returns': n4, 'l4_additional_tax_thousand_usd': a4,
        'excepted_share_of_l1_dollars_pct_computed': (round(100 * a2 / a1, 1) if a1 and y != 2023 else None),
        'l4_as_pct_of_schedule2_line8_amount_computed': (round(100 * a4 / sched2[y][1], 1) if a4 else None),
        'note': (NOTE_2023 if y == 2023 else
                 ('CRDs reported on Form 8915-E, not Form 5329 Part I' if y == 2020 else
                  ('Only lines 3-4 published' if y <= 2008 else ''))),
        'source_url': url, 'pdf_pages': pg,
    })
with open(os.path.join(OUT, 'irs_form5329_part1.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out2[0].keys())); w.writeheader(); w.writerows(out2)
print('ok', len(rows), len(out2))
