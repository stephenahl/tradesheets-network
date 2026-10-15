const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2000,height:1600}});
const fs=require('fs');for(const f of fs.readdirSync('.').filter(f=>f.startsWith('img_')&&f.endsWith('.html'))){await p.goto('file://'+process.cwd()+'/'+f);await p.screenshot({path:f.replace('.html','.png')});}
await b.close();})();
