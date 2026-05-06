import { chromium } from 'playwright';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, 'invite-chat-visual-reference.html');
const url = `file://${htmlPath}`;

const browser = await chromium.launch({ headless: true });

const desktop = await browser.newPage({ viewport: { width: 1440, height: 1280 }, deviceScaleFactor: 1 });
await desktop.goto(url);
await desktop.screenshot({
  path: path.join(__dirname, 'invite-chat-desktop-and-mobile.png'),
  fullPage: true
});

await desktop.locator('.phone').screenshot({
  path: path.join(__dirname, 'invite-chat-mobile-crop.png')
});
await desktop.close();

await browser.close();
