# Bilder — venter på deg (G1-GUI v1 godkjent 2026-10-10; v2 legger til «Åpne»)

Rendret 2026-10-10 med CellScaffolds egen web-renderer fra origin/main 7678b2c3 (web-src/), Chromium headless 1193, av images/render.js fra skeleton/venter-paa-deg.skeleton.json (laget av images/gen_skeleton.py).
Eksempeldataene er fire av radene fra revisjonen 11:15Z, ikke hele lista.

Skissen tar bort: «I kø» og «Levert siste døgn» fra Oversikt, og kommentarskjemaet under «Spør».
v2: web-src/skeleton-runtime.js er origin/main med `urlKeypath` lagt til (diff mot skeleton-runtime.origin-main.js, 5+1 linjer). «Åpne» vises bare når «Hvor» er https; i v2 er det raden for HD-0207. Lenken blir et <a> med href fra raden (render-report.json → links). «Åpne» får lenkestilen og er litt større enn de andre knappene.

Knappetrykk i web-rendereren (render-report.json → behaviour): alle går til workItems.setStatus eller workItems.overview.ask med radens id.

```
MD5 (web-src/haven-localization.js) = e424e58703fc8b1514a29bf9ab045259
MD5 (web-src/porthole-webo.css) = 7747a044e4d8c5ce83a35fbcc2612480
MD5 (web-src/skeleton-runtime.js) = f24e5f98ecaad31bd6429a9a5b695227
MD5 (images/venter-paa-deg-app-fylt-v1.png) = 7582b175ec568277985ca1437c4bdcb4
MD5 (images/venter-paa-deg-web-foreldet-v1.png) = a88f5136a8d701e2370b0f58d26eb079
MD5 (images/venter-paa-deg-web-fylt-v1.png) = 5e2275681ce25dc2b7bbc06d8ad3db97
MD5 (images/venter-paa-deg-web-tom-v1.png) = 7ac3301b0cdab5818f63c609d11f9531
```
MD5 (images/venter-paa-deg-app-fylt-v2.png) = d82dcde7ec0da7d7bae39b7cf25d343f
MD5 (images/venter-paa-deg-web-foreldet-v2.png) = c0d4b8b85444217fe7cb12200b267fb5
MD5 (images/venter-paa-deg-web-fylt-v2.png) = 60f7190acac663c2407a26803ce6156a
MD5 (images/venter-paa-deg-web-tom-v2.png) = 7ac3301b0cdab5818f63c609d11f9531
MD5 (web-src/skeleton-runtime.js) = df01bfacb5375ae407d51f7c9e4193bb
