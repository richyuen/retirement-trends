const { chromium } = require('playwright');
const path='file://'+require('path').resolve(__dirname,'..','output','Retirement account withdrawal trends.html')+'';
(async()=>{
  const browser = await chromium.launch();
  const errs=[];
  async function run(name, opts, tasks){
    const ctx = await browser.newContext(opts);
    const page = await ctx.newPage();
    page.on('console', m=>{ if(m.type()==='error') errs.push(name+': '+m.text()) });
    page.on('pageerror', e=>errs.push(name+' PAGEERROR: '+e.message));
    await page.goto(encodeURI(path), {waitUntil:'load'});
    await page.waitForTimeout(600);
    await tasks(page);
    await ctx.close();
  }
  const mode=process.argv[2]||'all';
  if(mode==='all'||mode==='checks'){
    await run('desktop-light',{viewport:{width:1280,height:900},reducedMotion:'reduce',colorScheme:'light'}, async page=>{
      const info = await page.evaluate(()=>({
        badRefs:[...document.querySelectorAll('sup.r.bad')].map(e=>e.textContent),
        refs:document.querySelectorAll('#reflist li').length,
        emptyCharts:[...document.querySelectorAll('.chart')].filter(c=>!c.querySelector('svg')).map(c=>c.dataset.chart),
        figs:document.querySelectorAll('figure.fig').length,
        overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        height: document.documentElement.scrollHeight,
        words: document.querySelector('main').innerText.split(/\s+/).length
      }));
      console.log('INFO desktop', JSON.stringify(info));
      await page.screenshot({path:'shots/top-desktop.png', clip:{x:0,y:0,width:1280,height:900}});
      const figs = await page.$$('figure.fig');
      for(let i=0;i<figs.length;i++){ await figs[i].scrollIntoViewIfNeeded(); await page.waitForTimeout(120); await figs[i].screenshot({path:`shots/fig-${String(i+1).padStart(2,'0')}.png`}); }
    });
    await run('phone-light',{viewport:{width:390,height:800},deviceScaleFactor:1,reducedMotion:'reduce',colorScheme:'light'}, async page=>{
      const info = await page.evaluate(()=>({overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth, wide:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+1 && !e.closest('.tbl-wrap')}).slice(0,8).map(e=>e.tagName+'.'+e.className+':'+Math.round(e.getBoundingClientRect().right))}));
      console.log('INFO phone', JSON.stringify(info));
      await page.screenshot({path:'shots/top-phone.png', clip:{x:0,y:0,width:390,height:1500}, fullPage:true});
      for(const id of ['f-overall','f-irsage','f-vgsplit','f-balrate','f-rmdsplit']){ const f=await page.$('#'+id); await f.scrollIntoViewIfNeeded(); await page.waitForTimeout(120); await f.screenshot({path:`shots/phone-${id}.png`}); }
    });
    await run('desktop-dark',{viewport:{width:1280,height:900},reducedMotion:'reduce',colorScheme:'dark'}, async page=>{
      await page.screenshot({path:'shots/top-dark.png', clip:{x:0,y:0,width:1280,height:900}});
      for(const id of ['f-agegrp','f-vgsplit','f-rollage']){ const f=await page.$('#'+id); await f.scrollIntoViewIfNeeded(); await page.waitForTimeout(120); await f.screenshot({path:`shots/dark-${id}.png`}); }
    });
  }
  if(mode==='all'||mode==='motion'){
    await run('motion',{viewport:{width:1280,height:900},colorScheme:'light'}, async page=>{
      // scroll through page to trigger entrances, toggles, table buttons
      const h = await page.evaluate(()=>document.documentElement.scrollHeight);
      for(let y=0;y<h;y+=700){ await page.evaluate(v=>window.scrollTo(0,v),y); await page.waitForTimeout(160); }
      await page.waitForTimeout(1200);
      const btns = await page.$$('.chart .btn');
      for(const b of btns){ try{ await b.click({timeout:1500}); await page.waitForTimeout(60);}catch(e){ errs.push('click fail '+e.message.split('\n')[0]) } }
      await page.waitForTimeout(900);
      const st = await page.evaluate(()=>({tables:document.querySelectorAll('.chart table').length, hiddenPlots:[...document.querySelectorAll('.chart .plot')].filter(p=>p.hidden).length}));
      console.log('INFO motion', JSON.stringify(st));
      // hover test on a line chart
      await page.evaluate(()=>window.scrollTo(0,0));
    });
  }
  console.log('ERRORS', JSON.stringify(errs,null,1));
  await browser.close();
})();
