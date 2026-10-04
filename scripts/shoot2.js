const { chromium } = require('playwright');
(async()=>{
  const browser = await chromium.launch();
  const ctx = await browser.newContext({viewport:{width:1280,height:900},reducedMotion:'reduce',colorScheme:'light'});
  const page = await ctx.newPage();
  await page.goto(encodeURI('file://'+require('path').resolve(__dirname,'..','output','Retirement account withdrawal trends.html')+''),{waitUntil:'load'});
  await page.waitForTimeout(500);
  for (const [id,name] of [['s-define','sec2'],['s-cash','sec6'],['f-timeline','fig1']]){
    const el = await page.$('#'+id); await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(100);
    const box = await el.boundingBox();
    await page.screenshot({path:`shots/${name}.png`, clip:{x:Math.max(0,box.x-10), y:box.y, width:Math.min(900,1280-box.x+10), height:Math.min(box.height,1250)}, fullPage:true});
  }
  await browser.close();
})();
