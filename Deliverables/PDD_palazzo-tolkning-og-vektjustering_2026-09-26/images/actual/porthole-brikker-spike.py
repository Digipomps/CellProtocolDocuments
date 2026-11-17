import json
from playwright.sync_api import sync_playwright
tags=["arancini","ris","safran","palermo","catania","gatemat","fritert"]
chip={"background":"#eef1f5","cornerRadius":10,"padding":4}
# S1: tags som barn av raden, wrap på lista
s1={"List":{"keypath":"reaction","childrenKeypath":"children","expandedStateKeypath":"expanded","selectionValueKeypath":"id","modifiers":{"wrap":True},
   "flowElementSkeleton":{"VStack":{"elements":[{"Text":{"keypath":"label","modifiers":{"fontStyle":"caption","backgroundKeypath":"chipBg","cornerRadius":10,"padding":4}}}]}}}}
d1={"reaction":[{"id":"r","label":"Registrert: Interessant · tolket som 7 emner","children":[{"id":"t"+t,"label":t,"chipBg":"#eef1f5"} for t in tags]}],"expanded":[]}
# S2: ett barn som har en innvendig liste med wrap
inner={"List":{"keypath":"tags","modifiers":{"wrap":True},"flowElementSkeleton":{"VStack":{"elements":[{"Text":{"keypath":"label","modifiers":{"fontStyle":"caption","background":"#eef1f5","cornerRadius":10,"padding":4}}}]}}}}
s2={"List":{"keypath":"reaction","childrenKeypath":"children","expandedStateKeypath":"expanded","selectionValueKeypath":"id",
   "flowElementSkeleton":{"VStack":{"elements":[{"Text":{"keypath":"label","modifiers":{"fontStyle":"caption"}}},inner]}}}}
d2={"reaction":[{"id":"r","label":"Registrert: Interessant · tolket som 7 emner","children":[{"id":"c","label":"","tags":[{"label":t} for t in tags]}]}],"expanded":[]}
html='<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/porthole-webo.css"><link rel="stylesheet" href="/admin-skeleton.css"></head><body style="width:360px;padding:12px"><main id="root"></main><script src="/runtime.js"></script></body></html>'
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,sk,data in [("S1",s1,d1),("S2",s2,d2)]:
        pg=b.new_page(viewport={"width":390,"height":420},device_scale_factor=2)
        def route(r):
            u=r.request.url
            if u.endswith("/runtime.js"): r.fulfill(path="runtime.js",content_type="application/javascript")
            elif u.endswith(".css"): r.fulfill(path=u.rsplit("/",1)[1],content_type="text/css")
            elif u.endswith("/"): r.fulfill(body=html,content_type="text/html")
            else: r.abort()
        pg.route("**/*",route); pg.goto("http://spike.test/")
        pg.wait_for_function("Boolean(window.HavenSkeletonRuntime?.createRenderer)")
        pg.evaluate("""([sk,data])=>{window.__a=[];const r=window.HavenSkeletonRuntime.createRenderer({rootElement:document.getElementById('root'),skeleton:sk,onAction:async(k,p)=>{window.__a.push(k)}});r.update(data);}""",[sk,data])
        rows=lambda: pg.evaluate("Array.from(document.querySelectorAll('.skeleton-list-row')).map(r=>r.dataset.depth+':'+r.textContent.trim())")
        res[name+"_lukket"]=rows(); pg.screenshot(path=f"{name}-lukket.png")
        pg.click(".skeleton-list-row-toggle:not(.is-leaf)")
        res[name+"_aapen"]=rows(); pg.screenshot(path=f"{name}-aapen.png")
        res[name+"_actions"]=pg.evaluate("window.__a")
        res[name+"_errors"]=[]
    b.close()
print(json.dumps(res,ensure_ascii=False,indent=1))
