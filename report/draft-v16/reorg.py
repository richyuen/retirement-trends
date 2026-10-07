"""Build the v16 reorganized draft from report/parts into report/draft-v16/parts. Re-runnable."""
import re, os, shutil, sys
R='/mnt/project-files/retirement-withdrawals/report'
src=open(R+'/parts/20-body.html',encoding='utf-8').read()
head=open(R+'/parts/10-head.html',encoding='utf-8').read()

def sub1(pat,rep,s,flags=0):
    n=len(re.findall(pat,s,flags))
    assert n==1,(pat[:60],n)
    return re.sub(pat,rep,s,flags=flags)

# ---- split ----
m0=src.index('<section id="s-summary">'); m1=src.rindex('</section>')+len('</section>')
pre,mid,post=src[:m0],src[m0:m1],src[m1:]
secs={b:a for a,b in re.findall(r'(?s)(<section id="(s-[a-z]+)">.*?</section>)',mid)}
old=['s-summary','s-define','s-rules','s-who','s-rate','s-cash','s-plans','s-roll','s-survey','s-micro','s-stay',
     's-laws','s-contrib','s-income','s-long','s-work','s-health','s-ltc','s-ss','s-ready','s-debt','s-poverty',
     's-db','s-annuity','s-watch','s-notes','s-sources']
assert list(secs)==old,list(secs)

# ---- content moves (written with OLD section numbers; renumbered below) ----
plans,stay,ann=secs['s-plans'],secs['s-stay'],secs['s-annuity']
# 1. Section 7's TSP paragraph duplicates Section 11; fold its unique detail into Section 11's sentence.
plans=sub1(r'<p>The federal Thrift Savings Plan shows a similar change.*?</p>\n','',plans,re.S)
stay=sub1(r'Under the old rules, 49% of people who separated in 2012 had closed their accounts by the end of 2013: 41% through a full withdrawal and 8% through an automatic cash-out of a small balance\.',
  'Under the old rules, about half of the people who separated in 2012 still had their account at the end of 2013 (49% had taken no action and 2% only a partial withdrawal), 41% had withdrawn in full, mostly as a cash lump sum, and 8% had received an automatic cash-out of a small balance.',stay)
# 2. Section 7's annuity paragraph moves to the annuities section.
ap=re.search(r'<p>Annuities play almost no part\..*?</p>\n',plans,re.S).group(0)
plans=plans.replace(ap,'<p>Annuities play almost no part in these choices (Section 24).</p>\n')
ap=ap.replace('<p>Annuities play almost no part. A 2016','<p>Retirees leaving DC plans rarely choose one. A 2016')
ann=sub1(r'(<p>Plan rules decide most annuity choices\..*?</p>\n)',lambda m:m.group(1)+ap,ann,re.S)
# 3. Section 11 becomes a subsection of Section 7, after the retention evidence.
body=re.search(r'(?s)<h2>.*?</h2>\n(.*)</section>',stay).group(1)
body=sub1(r'<p>Section 7 shows more retirement-age money staying in employer plans, but nearly all of that evidence comes from recordkeepers',
  '<p>Nearly all of the evidence above comes from recordkeepers',body)
body='<h3 class="sub">Beyond the recordkeepers</h3>\n'+body
plans=sub1(r'(<h3 class="sub">Plan design moved with it)',lambda m:body+m.group(1),plans)
plans=plans.replace('<h2><span class="n">7</span>Employer plans after retirement</h2>','<h2><span class="n">7</span>Employer plans after retirement: staying in the plan</h2>')
secs['s-plans'],secs['s-annuity']=plans,ann
del secs['s-stay']

secs['s-notes']=sub1(r'Section 10 was added on 4 October 2026 from the tabulations described above, Sections 11, 12, 14 and 15 the same day, Sections 16 to 24 on 5 October 2026 and Section 13 on 6 October 2026, from further tabulations and published sources\.',
  'The microdata section and later sections were added on 4–6 October 2026 from the tabulations described above, further tabulations and published sources, and the report was reorganized into parts on 6 October 2026.',secs['s-notes'])
# ---- new order and parts ----
PARTS=[('Background',['s-summary','s-define','s-rules']),
 ('Withdrawals and rollovers',['s-who','s-rate','s-cash','s-plans','s-roll','s-survey','s-micro']),
 ('Saving for retirement',['s-contrib','s-ready','s-laws']),
 ('Income in retirement',['s-income','s-ss','s-db','s-annuity']),
 ('What the money has to cover',['s-long','s-work','s-health','s-ltc']),
 ('Older households’ finances',['s-debt','s-poverty']),
 ('Outlook and reference',['s-watch','s-notes','s-sources'])]
new=[s for _,l in PARTS for s in l]
smap={old.index(s)+1:new.index(s)+1 for s in new}; smap[11]=new.index('s-plans')+1

# ---- figure/table maps from new order ----
joined='\n'.join(secs[s] for s in new)
fmap={int(o):i+1 for i,o in enumerate(re.findall(r'<p class="fig-no">Figure (\d+)</p>',joined))}
tmap={int(o):i+1 for i,o in enumerate(re.findall(r'<caption>Table (\d+)\.',joined))}
assert len(fmap)==46 and len(tmap)==15,(len(fmap),len(tmap))

LIST=r'(\d+(?:(?:–| to | and |, )\d+)*)'
def remap(nums,mp):
    parts=re.split(r'(–| to | and |, )',nums); ns=[int(p) for p in parts[0::2]]; seps=parts[1::2]
    if any(s in ('–',' to ') for s in seps):
        new_=[mp.get(n,n) for n in ns]
        assert all(b-a==ns[i+1]-ns[i] for i,(a,b) in enumerate(zip(new_,new_[1:]))),('range broken',nums,new_)
        return ''.join(str(x)+(seps[i] if i<len(seps) else '') for i,x in enumerate(new_))
    new_=sorted(mp.get(n,n) for n in ns)
    return ''.join(str(x)+(seps[i] if i<len(seps) else '') for i,x in enumerate(new_))
def renum(s):
    s=re.sub(r'(?<!, )(?<!Poverty )(Sections? )'+LIST,lambda m:m.group(1)+remap(m.group(2),smap),s)
    s=re.sub(r'(?<!, )(Figures? )'+LIST,lambda m:m.group(1)+remap(m.group(2),fmap),s)
    s=re.sub(r'(?<!, )(?<!Poverty )(?<!from )(Tables? )'+LIST+r'(?![.]\d)',lambda m:m.group(1)+remap(m.group(2),tmap),s)
    s=re.sub(r'<span class="n">(\d+)</span>',lambda m:'<span class="n">%d</span>'%smap[int(m.group(1))],s)
    return s
# fig-no lines were remapped by the generic rule (not preceded by comma); check later
for k in new: secs[k]=renum(secs[k])

# ---- summary findings: reorder to follow the sections ----
summ=secs['s-summary']
ol=re.search(r'(?s)<ol class="findings">\n(.*?)</ol>',summ)
items=re.findall(r'(?s)  <li>.*?</li>\n',ol.group(1)); assert len(items)==21,len(items)
key=lambda t:t.split('</strong>')[0]
order_hint=['Withdrawals follow','Incidence is rising','Raising the RMD age','Withdrawal rates are low','Full cashouts',
 'Rollovers are the largest','More retirement-age money','Surveys see','The household microdata',
 'Saving in accounts rose','About a third of working-age','Laws that change defaults',
 'Account withdrawals are replacing','Social Security’s retirement fund','Defined benefit pensions','Few retirees turn',
 'Retirement horizons','People work and claim','Health and long-term care','Older households carry','Official poverty']
pick=[]
for h in order_hint:
    c=[t for t in items if h in key(t)]; assert len(c)==1,(h,len(c)); pick.append(c[0])
assert sorted(pick)==sorted(items)
summ=summ.replace(ol.group(1),''.join(pick)); secs['s-summary']=summ

# ---- data notes: general notes first, then by section, Method last ----
notes=secs['s-notes']
ul=re.search(r'(?s)<ul>\n(.*?)</ul>',notes)
lis=re.findall(r'(?s)  <li>.*?</li>\n',ul.group(1))
def nkey(t):
    if '<strong>Method.' in t: return (99,0)
    if '<strong>Vanguard cohorts.' in t: return (7,1)
    if '<strong>Rollovers in 2022' in t: return (8,1)
    m=re.search(r'\(Sections? (\d+)',t)
    return (int(m.group(1)),0) if m else (0,lis.index(t))
lis2=sorted(lis,key=lambda t:(nkey(t),lis.index(t)))
notes=notes.replace(ul.group(1),''.join(lis2)); secs['s-notes']=notes

# ---- assemble with part headings ----
out=[]
for i,(pname,l) in enumerate(PARTS):
    out.append('<p class="part" id="p-%d"><span>Part %d</span>%s</p>'%(i+1,i+1,pname))
    out+= [secs[s] for s in l]
mid2='\n\n'.join(out)

# TOC
toc_items=[]
for i,(pname,l) in enumerate(PARTS):
    toc_items.append('    <li class="part">%s</li>'%pname)
    for s in l:
        t=re.search(r'<li><a href="#%s"><span class="n">\d+</span>(.*?)</a></li>'%s,pre).group(1)
        if s=='s-plans': t='Employer plans: staying in'
        toc_items.append('    <li><a href="#%s"><span class="n">%d</span>%s</a></li>'%(s,new.index(s)+1,t))
pre2=re.sub(r'(?s)(<nav class="toc"[^>]*>\n  <h2>Contents</h2>\n  <ol>\n).*?(  </ol>)',lambda m:m.group(1)+'\n'.join(toc_items)+'\n'+m.group(2),pre)
pre2=sub1(r'<p class="meta">.*?</p>',
  '<p class="meta">Data through 2025 where available · Compiled 3 October 2026 · Expanded 4–6 October 2026 · Reorganized into parts 6 October 2026</p>',pre2)

body2=pre2+mid2+post
# CSS for parts
css=('.toc li.part{font:500 .66rem/1.3 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:.75rem 0 .15rem;break-after:avoid}\n'
 '.toc li.part:first-child{padding-top:.1rem}\n'
 '.prose p.part{font:500 .72rem/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--accent);margin:3.4rem 0 .5rem}\n'
 '.prose p.part span{color:var(--muted);margin-right:.8em}\n'
 '.prose p.part:first-child{margin-top:0}\n')
head2=head if '.toc li.part' in head else head.replace('.toc a{color',css+'.toc a{color',1)
assert '.toc li.part' in head2

D=R+'/draft-v16'; os.makedirs(D+'/parts',exist_ok=True)
open(D+'/parts/10-head.html','w',encoding='utf-8').write(head2)
open(D+'/parts/20-body.html','w',encoding='utf-8').write(body2)
shutil.copy(R+'/parts/30-script.html',D+'/parts/30-script.html')
print('sections',len(new),'figs',len(fmap),'tables',len(tmap))
print('section map',{old[o-1] if o!=11 else 's-stay':n for o,n in sorted(smap.items())})
