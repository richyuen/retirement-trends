import re, json
import os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
R=os.path.join(ROOT,'data','recovered_irs')+'/'
def result(fn):
    t=open(R+fn).read().split('### RESULT\n',1)[1]
    s=t.split('\n\n(captured at origin')[0].strip()
    return json.loads(s) if s.startswith('"') else s
# ---- IRS SOI Table 4 by age 2004-2023
age={}
for line in result('js_559.txt').strip().split('\n')[1:]:
    p=[x.strip() for x in line.split('|')]
    y=int(p[0]); g=p[1]
    age.setdefault(y,{})[g]=dict(wn=int(p[2]),wa=int(p[3]),hn=int(p[4]),fa=int(p[5]))
years=sorted(age)
print("years",years[0],years[-1],len(years))
groups=['u60','60-64','65-69','70-74','75-79','80+']
# incidence: withdrawers per 100 year-end holders
print("\nIncidence (withdrawers per 100 EOY holders)")
print("year  "+"  ".join(f"{g:>6}" for g in groups+['60-69','70+','all']))
inc={}
for y in years:
    row=[100*age[y][g]['wn']/age[y][g]['hn'] for g in groups+['60-69','70+','all']]
    inc[y]=[round(v,1) for v in row]
    print(y," ".join(f"{v:7.1f}" for v in row))
# rates: W(t)/FMV(t-1) and W(t)/FMV(t)
print("\nRate W/prior-year-end FMV (%), then W/same-year-end FMV (%)")
print("year  "+"  ".join(f"{g:>6}" for g in groups+['60-69','70+','all']))
rate_prior={}; rate_same={}
for y in years:
    rs=[100*age[y][g]['wa']/age[y][g]['fa'] for g in groups+['60-69','70+','all']]
    rate_same[y]=[round(v,2) for v in rs]
    if y-1 in age:
        rp=[100*age[y][g]['wa']/age[y-1][g]['fa'] for g in groups+['60-69','70+','all']]
        rate_prior[y]=[round(v,2) for v in rp]
        print(y,"P"," ".join(f"{v:7.2f}" for v in rp))
    print(y,"S"," ".join(f"{v:7.2f}" for v in rs))
# shares of withdrawal dollars and of withdrawers by age
print("\nShare of withdrawal dollars: u60 / 60-69 / 70+ ; share of withdrawers 70+ ; avg withdrawal 60-69, 70+")
for y in years:
    a=age[y]; T=a['all']['wa']; N=a['all']['wn']
    print(y, f"{100*a['u60']['wa']/T:5.1f} {100*a['60-69']['wa']/T:5.1f} {100*a['70+']['wa']/T:5.1f} | {100*a['70+']['wn']/N:5.1f} | {1000*a['60-69']['wa']/a['60-69']['wn']:,.0f} {1000*a['70+']['wa']/a['70+']['wn']:,.0f} | totalW ${T/1e6:,.1f}B N {N/1e6:.2f}M holders {a['all']['hn']/1e6:.2f}M FMV ${a['all']['fa']/1e9:.2f}T")
# ---- Table 1 by type
t1={}
for line in result('js_563.txt').strip().split('\n')[1:]:
    p=line.split('|'); y=int(p[0]); k=p[1]
    def n(x):
        try: return float(x)
        except: return None
    t1.setdefault(y,{})[k]=dict(wn=n(p[2]),wa=n(p[3]),hn=n(p[4]),fa=n(p[5]),prior=n(p[6]))
print("\nTraditional IRA: withdrawers/holders %, W/prior FMV %, W $B ; Roth: same")
for y in sorted(t1):
    tr=t1[y]['trad']; ro=t1[y]['roth']
    def f(d):
        if not d['wn']: return "   n/a"
        a=100*d['wn']/d['hn']; b=(100*d['wa']/d['prior']) if d['prior'] else float('nan')
        return f"{a:5.1f}% {b:5.2f}% ${d['wa']/1e6:6.1f}B n={d['wn']/1e6:5.2f}M"
    print(y,"trad",f(tr)," | roth",f(ro))
json.dump(dict(age=age,inc=inc,rate_prior=rate_prior,rate_same=rate_same,t1=t1),open(os.path.join(ROOT,'data','irs_derived.json'),'w'))
# ---- rollovers by age TY2023 (from js_331)
txt=result('js_331.txt')
rows={}
for line in txt.split('\n'):
    p=line.split('|')
    if len(p)>=16 and re.match(r'^(All taxpayers|Under 20|\d\d under \d\d|80 and over)',p[0]):
        num=lambda s: float(re.sub(r'[^0-9.]','',s) or 0)
        rows[p[0]]=dict(roll_n=num(p[8]),roll_a=num(p[9]),conv_n=num(p[10]),conv_a=num(p[11]),wn=num(p[12]),wa=num(p[13]),hn=num(p[14]),fa=num(p[15]),filers=num(p[1]))
    if 'Table 8' in line: break
T=rows['All taxpayers']
print("\nTY2023 rollovers by age: $B, share of $, n (000), avg $")
for k,v in rows.items():
    print(f"{k:14s} ${v['roll_a']/1e6:7.1f}B {100*v['roll_a']/T['roll_a']:5.1f}% n={v['roll_n']/1e3:7.1f}K avg=${1000*v['roll_a']/max(v['roll_n'],1):,.0f} | conv ${v['conv_a']/1e6:5.1f}B | filers {v['filers']/1e6:.1f}M; IRA holders/filers {100*v['hn']/v['filers']:.1f}%")
s=lambda ks,f: sum(rows[k][f] for k in ks)
o55=['55 under 60','60 under 65','65 under 70','70 under 75','75 under 80','80 and over']; o60=o55[1:]
print("2023 share of rollover $: 55+ %.1f%%  60+ %.1f%%  55-69 %.1f%% ; share of rollover taxpayers 55+ %.1f%% 60+ %.1f%%"%(100*s(o55,'roll_a')/T['roll_a'],100*s(o60,'roll_a')/T['roll_a'],100*s(o55[:3],'roll_a')/T['roll_a'],100*s(o55,'roll_n')/T['roll_n'],100*s(o60,'roll_n')/T['roll_n']))
print("2023 conversions: 60+ share %.1f%%"%(100*s(o60,'conv_a')/T['conv_a']))
json.dump(rows,open(os.path.join(ROOT,'data','irs_2023_table4.json'),'w'))
