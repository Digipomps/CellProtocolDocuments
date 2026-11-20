# Bilder til G1-GUI — Mistral-kvote for studentene (v1, 20.11.2026)

Rendret med den ekte web-rendereren i CellScaffold `272580b` (main 20.11): `Public/js/skeleton-runtime.js` og `Public/css/porthole-webo.css`, i Playwright/Chromium. Skeleton-JSON og testdata ligger i `../skeleton/render.js`. Kjør på nytt med `node skeleton/render.js <CellScaffold>/Public images`.

Hva er ekte, og hva er tegnet:
- Ekte: rendereren og elementtypene (VStack, HStack, Text, Button, List, TextArea). Fargene er Kallimachos-paletten fra `KallimachosAdvisorConfigurationFactory`.
- Tegnet: dataene (beløp, navn og svar) og nøkkelstiene `kallimachos.source.*`, `quota.*`, `notice.*` og `admin.*`. Cellene som skal svare på dem, finnes ikke ennå. Prisen på drift-siden er et eksempel, ikke Mistrals pris.
- Kildevelgeren («Hvem skal svare?») erstatter dagens tre knapper (Bare bibliotekaren / lokal / kapabel). Den bruker kildene fra PDD_formal-velger-modellkilde.
- Drift-siden er en mockup. I dag er `/admin/ai-usage` en Leaf-HTML-side og ikke et skeleton.
- Alle flatene er vanlige skeleton-elementer, så de skal kunne tegnes i Binding (Swift). Binding er ikke rendret her, fordi skycontaineren ikke har Swift. Det skjer i P5.

| Fil | Flate og tilstand |
|---|---|
| `kvote-fylt-{laptop,iphone}-v1.png` | Kallimachos med DiMy-hostet Mistral, kvote igjen, svar med kilde, modell og pris |
| `kvote-tom-{laptop,iphone}-v1.png` | Dagens kvote er brukt opp (`student_quota_exhausted_today`) |
| `ikke-student-{laptop,iphone}-v1.png` | Kontoen mangler studentrollen (`not_eligible`) |
| `rollestatus-ukjent-{laptop,iphone}-v1.png` | Statuslisten for rollen er for gammel (`role_status_unknown`) |
| `drift-{laptop,iphone}-v1.png` | Operatøren: modeller DiMy tilbyr, grenser og forbruk i dag |

Kjent avvik i dagens renderer: tekstfeltet blir mørkt i `view-mode`. Dagens Kallimachos bruker stilklassen `kallimachos-input`, som ikke er tatt med her. Det rettes i implementeringen.
