import pickle,csv
out,est=pickle.load(open('nb.pkl','rb'))
rows=[]
NB='https://download.bls.gov/pub/time.series/nb/ (series {})'
for (y,g,pt),d in sorted(out.items()):
    a=d.get('access',('',''));p=d.get('part',('',''));t=d.get('takeup',('',''))
    sids=';'.join(x[1] for x in (a,p,t) if x[1])
    rows.append(dict(year=y,group=g,plan_type=pt,access_pct=a[0],participation_pct=p[0],takeup_pct=t[0],takeup_note='published',reference='March',method_note='NCS nb database (2010+), broadened access definition in effect since 2009',source_url=NB.format(sids)))
def add(y,g,pt,a,p,t,url,tn='published',mn=''):
    if t is None: t=round(100*p/a); tn='Computed = participation/access (rounded published %s; approximate)'
    rows.append(dict(year=y,group=g,plan_type=pt,access_pct=a,participation_pct=p,takeup_pct=t,takeup_note=tn,reference='March',method_note=mn,source_url=url))
pre='Pre-2009 access definition (narrower; BLS broadened definition of access to retirement benefits in March 2009 release) - not strictly comparable with 2009+'
U03='https://www.bls.gov/ebs/publications/pdf/bulletin-2573-january-2005-employee-benefits-in-private-industry-in-the-united-states-2002-2003.pdf (Tables 1-2, March 2003 recalculated)'
for g,ar,pr,ad,pd in [('all private industry',57,49,51,40),('full-time',67,58,60,48),('part-time',24,18,21,14),('establishments <100 workers',42,35,38,31),('establishments 100+ workers',75,65,65,51)]:
    add(2003,g,'all retirement',ar,pr,None,U03,mn=pre); add(2003,g,'defined contribution',ad,pd,None,U03,mn=pre)
U04='https://www.bls.gov/ebs/publications/pdf/employee-benefits-in-private-industry-in-the-united-states-march-2004.pdf (Tables 1-2)'
for g,ar,pr,ad,pd in [('all private industry',59,50,53,42),('full-time',68,60,62,50),('part-time',27,20,23,14),('establishments <100 workers',44,37,40,32),('establishments 100+ workers',77,67,68,53)]:
    add(2004,g,'all retirement',ar,pr,None,U04,mn=pre); add(2004,g,'defined contribution',ad,pd,None,U04,mn=pre)
U05='https://www.bls.gov/ebs/publications/pdf/employee-benefits-in-private-industry-in-the-united-states-march-2005.pdf (Tables 1-2)'
for g,ar,pr,ad,pd in [('all private industry',60,50,53,42),('full-time',69,60,62,50),('part-time',27,19,23,14),('establishments <100 workers',44,37,40,32),('establishments 100+ workers',78,67,69,53)]:
    add(2005,g,'all retirement',ar,pr,None,U05,mn=pre); add(2005,g,'defined contribution',ad,pd,None,U05,mn=pre)
U06='https://www.bls.gov/ebs/publications/pdf/employee-benefits-in-private-industry-in-the-united-states-march-2006.pdf (Tables 1, 2, 6)'
for g,ar,pr,tr,ad,pd,td in [('all private industry',60,51,85,54,43,79),('full-time',69,60,86,63,51,80),('part-time',29,21,72,25,16,65),('establishments <100 workers',44,37,84,41,33,81),('establishments 100+ workers',78,67,85,70,54,77)]:
    add(2006,g,'all retirement',ar,pr,tr,U06,mn=pre); add(2006,g,'defined contribution',ad,pd,td,U06,mn=pre)
U07='https://www.bls.gov/ebs/publications/pdf/employee-benefits-in-private-industry-in-the-united-states-march-2007.pdf (Table 1)'
for g,ar,pr,tr,ad,pd,td in [('all private industry',61,51,84,55,43,77),('full-time',70,60,85,64,50,79),('part-time',31,23,73,27,18,65),('establishments <100 workers',45,37,82,42,33,79),('establishments 100+ workers',78,66,85,70,53,76)]:
    add(2007,g,'all retirement',ar,pr,tr,U07,mn=pre); add(2007,g,'defined contribution',ad,pd,td,U07,mn=pre)
U08='https://www.bls.gov/news.release/archives/ebs2_08072008.htm (Table 1, private industry columns)'
for g,a,p,t in [('all private industry',61,51,83),('full-time',71,60,85),('part-time',32,23,73),('establishments <100 workers',45,37,81),('establishments <50 workers',41,34,82),('establishments 50-99 workers',58,45,79),('establishments 100+ workers',79,67,85),('establishments 100-499 workers',73,60,83),('establishments 500+ workers',87,76,87)]:
    add(2008,g,'all retirement',a,p,t,U08,mn=pre)
U09='https://www.bls.gov/news.release/archives/ebs2_07282009.htm (Table 1, private industry columns)'
for g,a,p,t in [('all private industry',67,51,77),('full-time',76,61,80),('part-time',39,22,55),('establishments <100 workers',53,36,69),('establishments <50 workers',48,33,69),('establishments 50-99 workers',66,46,69),('establishments 100+ workers',83,68,82),('establishments 100-499 workers',79,61,77),('establishments 500+ workers',88,77,88),('lowest 25% wage',43,23,52),('highest 25% wage',84,75,89)]:
    add(2009,g,'all retirement',a,p,t,U09,mn='First year of broadened access definition (BLS: "The NCS has broadened the definition of access to retirement benefits")')
rows.sort(key=lambda r:(r['plan_type'],r['group'],r['year']))
f='/mnt/project-files/retirement-withdrawals/dc_policy/output/bls_ncs_access_participation.csv'
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=['year','group','plan_type','access_pct','participation_pct','takeup_pct','takeup_note','reference','method_note','source_url'])
w.writeheader(); w.writerows(rows); print(len(rows))
# establishments offering
with open('/mnt/project-files/retirement-withdrawals/dc_policy/raw/stateira/ncs_establishments_offering.csv','w') as g:
    g.write('year,group,provision,pct_establishments_offering,source\n')
    names={'370':'all retirement','372':'defined contribution'}
    for (y,gr,pc),v in sorted(est.items()): g.write(f'{y},{gr},{names[pc]},{v},https://download.bls.gov/pub/time.series/nb/\n')
