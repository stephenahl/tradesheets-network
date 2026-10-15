const { chromium } = require('playwright');
const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(process.cwd(), 'guide.html'));
  await p.pdf({ path: path.join(process.cwd(), 'Quick-Start-Guide.pdf'), format: 'Letter' }); await b.close(); })();
