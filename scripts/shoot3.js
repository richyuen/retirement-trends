const { chromium } = require('playwright');
(async()=>{
  const browser = await chromium.launch();
  const ctx = await browser.newContext({viewport:{width:1280,height:900},reducedMotion:'reduce',colorScheme:'light'});
  const page = await ctx.newPage();
  await page.goto(encodeURI('file://'+require('path').resolve(__dirname,'..','output','Retirement account withdrawal trends.html')+''),{waitUntil:'load'});
  await page.waitForTimeout(500);
  const t = await page.$$('#s-define .tbl-wrap');
  await t[0].screenshot({path:'shots/table1.png'});
  await (await page.$('#f-timeline')).screenshot({path:'shots/fig1.png'});
  const s = await page.$('#s-summary'); await s.screenshot({path:'shots/summary.png'});
  await browser.close();
})();
