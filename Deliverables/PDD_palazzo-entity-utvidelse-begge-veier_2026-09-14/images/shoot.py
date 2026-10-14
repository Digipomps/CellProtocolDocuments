import asyncio, pathlib
from playwright.async_api import async_playwright
views = {
 'gjest-koble-tilbud-v2': 'tilbud',
 'gjest-koble-tilbud-forklart-v2': 'tilbud-forklart',
 'gjest-koble-venter-v2': 'venter',
 'gjest-koble-koblet-v2': 'koblet',
 'gjest-koble-aldri-v2': 'aldri',
 'haven-koble-tilbud-v2': 'haven-tilbud',
}
base = pathlib.Path(__file__).parent.resolve()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=2)
        page = await ctx.new_page()
        errors=[]
        page.on('pageerror', lambda e: errors.append(str(e)))
        for name, v in views.items():
            await page.goto(f'file://{base}/render.html?view={v}')
            await page.wait_for_timeout(400)
            await page.evaluate('document.fonts.ready')
            await page.screenshot(path=str(base/f'{name}.png'), clip={'x':0,'y':0,'width':390,'height':844})
            print('ok', name)
        print('pageerrors:', errors)
        await b.close()
asyncio.run(main())
