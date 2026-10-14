import asyncio, os, sys
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

SINGLES = {
    "avsender-forhandsvisning-v1.png": "#s2",
    "avsender-oversikt-v1.png": "#s4",
    "mottaker-uten-haven-v1.png": "#r2",
    "mottaker-med-haven-v1.png": "#m2",
    "avslag-uten-konto-v1.png": "#r3",
    "hjelpechat-mottaker-v1.png": "#h1",
    "flytt-hjem-v1.png": "#r5",
}
STRIPS = {
    "stripe-avsender-v1.png": "#stripe-avsender",
    "stripe-mottaker-uten-v1.png": "#stripe-mottaker-uten",
    "stripe-mottaker-med-v1.png": "#stripe-mottaker-med",
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 2300, "height": 900}, device_scale_factor=2)
        await pg.goto("file://" + os.path.join(HERE, "invite.html"))
        await pg.wait_for_timeout(300)
        # overflow check: any .body whose scrollHeight exceeds clientHeight
        overflow = await pg.evaluate("""() => [...document.querySelectorAll('.frame')].filter(f => {
            const b = f.querySelector('.body'); return b && b.scrollHeight > b.clientHeight + 2;
        }).map(f => f.id + ':' + (f.querySelector('.body').scrollHeight - f.querySelector('.body').clientHeight))""")
        print("overflow:", overflow)
        for name, sel in SINGLES.items():
            await pg.locator(sel).screenshot(path=os.path.join(OUT, name))
        for name, sel in STRIPS.items():
            await pg.locator(sel).screenshot(path=os.path.join(OUT, name))
        await b.close()
    print("\n".join(sorted(os.listdir(OUT))))

asyncio.run(main())
