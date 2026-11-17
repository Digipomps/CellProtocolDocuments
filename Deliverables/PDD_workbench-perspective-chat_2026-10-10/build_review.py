"""Build review facts from the completed offline renderer evidence."""
import hashlib, html, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
report=json.loads((ROOT/'images/render-report.json').read_text())
cases=report['cases']; shots=json.loads((ROOT/'skeleton/shots.json').read_text())
assert len(cases)==len(shots)==54
assert {x['name'] for x in cases}=={x['name'] for x in shots}
assert all(not x['errors'] and not x['dom']['unsupported'] and not x['dom']['componentErrors'] for x in cases)
assert all(x['dom']['width']==x['dom']['scrollWidth'] for x in cases)
minimum=min(c['ratio'] for x in cases for c in x['dom']['contrast'])
assert minimum>=4.5
actions=sum(len(x['actions']) for x in cases)
unique=sorted({a['keypath'] for x in cases for a in x['actions']})
mounted=[x for x in cases if 'mountPayloadIsolation' in x]
assert len(mounted)==2 and all(x['mountPayloadIsolation'] for x in mounted)
assert len([x for x in cases if 'draftSaveGap' in x])==2

manifest=[]
for shot in shots:
    p=ROOT/'images'/(shot['name']+'.png');data=p.read_bytes()
    manifest.append(dict(path='images/'+p.name,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
(ROOT/'images/image-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

inventory=[]
for key in unique:
    examples=[a for x in cases for a in x['actions'] if a['keypath']==key]
    a=examples[0]
    inventory.append(dict(keypath=key,observations=len(examples),examplePayload=a['payload'],
                          mount=a.get('meta',{}).get('mount'),
                          contractStatus='design-candidate; live Explore/backend verification pending'))
(ROOT/'images/action-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')

readme=f'''# Referansebilder for G1-GUI

2026-10-10. **Designkandidat med syntetiske data. G1 er godkjent; G1-GUI venter.**

Start med [bildegalleriet](../GUI_GALLERY.html). Klikk et bilde for original størrelse.
Bildene er gjengitt med CellScaffolds uendrede web-renderer fra
`7678b2c3d293978b5b179cdcada5e843f17c5b73`. Dette er ikke skjermbilder fra produksjon.

| Kontroll | Målt resultat |
|---|---|
| Rendringer | {len(cases)} (27 lys, 27 mørk) |
| JS-/unsupported-/komponentfeil | 0 |
| Horisontal overflyt | 0 ved de prøvde breddene |
| Tekstkontrast | Minst {minimum:.2f}:1 for målte synlige Text, etiketter og kontrolltekster |
| Registrerte kontrollhandlinger | {actions}, fordelt på {len(unique)} keypaths |
| Separate mount-/session-payloads | Kontrollert i lys og mørk komponentprøve |
| Skriv → Send/Lagre | Integrasjonsgap påvist; fersk tekst følger ikke knapp-payload automatisk |

Kontrastmålingen bruker beregnede CSS-farger mot nærmeste ugjennomsiktige bakgrunn.
Den er ingen full tilgjengelighetsrevisjon: fokus, skjermleser, placeholder-kontrast,
alle hover-tilstander, touchbruk og native rendering er ikke komplett kontrollert.
Smal visning er Chromium ved 390 px med `touch`-kapabilitet, **ikke SwiftUI/Binding-bevis**.

## Kilder og stil

Fire frosne filer lastes: skeleton-runtime.js, haven-localization.js, porthole-webo.css
og developer-workbench.css. Den eksporterte theme-aliasfilen lastes ikke.
Kildehashene står i [renderer/manifest.json](../renderer/manifest.json).

| Kilde | MD5 |
|---|---|
'''
for entry in json.loads((ROOT/'renderer/manifest.json').read_text()):
    readme+=f"| {entry['path']} | `{entry['md5']}` |\n"
readme+='''
`candidate.css` er en eksplisitt kandidat-utvidelse: tomme valgfrie List-plasser uten
synlig boks, felter som fyller plassen, én TextArea-ramme, flat sidemeny og nowrap
for deklarerte HStack-rader. Rendererfilene er ikke endret.
Alle innholdstekster, knapper og felt i produktbildet kommer fra Skeleton og fixture.
Den grå «DESIGNKANDIDAT»-stripen kommer fra harnessens HTML.

Vi har ikke skjult varsler fra en innlogget side: ingen live side er brukt. Hele
innholdsrammen gjengis med fullPage. Portholes globale navigasjon/editor er ikke med
i denne isolerte flateprøven. Smal navigasjon skjules via Skeleton layoutVariant;
bilder av smal bredde gjelder bare den selvstendige chatten.

## Grenser

Alle nye actions er designkontrakter. De er **ikke** dokumentert som implementerte
Explore-handlinger. Knappetrykk registreres lokalt og utfører ingenting. Menyer kan
åpnes og felter kan fylles i testharnessen; navigasjon mellom kandidatbilder, faktisk
søk/filtrering, modellkall, lagring, kø, merge og deploy er ikke koblet til backend.
Backend skal validere gjeldende filter-/preview-revisjon og faktisk requester.

Se [GUI_REVIEW.md](../GUI_REVIEW.md) for godkjenningsomfang og implementeringsgap.
`render-report.json` inneholder rå mål, payloads og gap-prober. `action-inventory.json`
er en kompakt liste. `image-manifest.json` låser akkurat bildefilene som fremlegges.

## Reprodusere

Fra denne leveransemappens rot, med eksisterende Playwright installert:

```sh
python3 generate.py
node render.js
python3 build_review.py
```

Harness støtter `NODE_PATH` til et eksisterende Playwright-miljø og `CHROMIUM_PATH`
til en allerede installert Chromium. Ingen npm-installasjon, Swift-bygg, server,
ekstern nettverksforespørsel eller GitHub Actions trengs. Alle nettverksforespørsler
fanges og besvares fra lokal fil eller avbrytes. En lokal Chromium-prosess kan kreve
OS-/sandbox-godkjenning. Testen bruker en isolert midlertidig profil.
'''
(ROOT/'images/README.md').write_text(readme)

review=f'''# GUI-gjennomgang — Workbench hjelpechat

2026-10-10. G1 godkjent. **Dette er P1-GUI, ikke implementering eller deploy.**

## Det Kjetil tar stilling til

Godkjenning gjelder de gjengitte kandidatbildene i [galleriet](GUI_GALLERY.html),
med bytehashene i `images/image-manifest.json`: layout, lys/mørk stil, innganger,
perspektiv-/modellvalg, egne pakker, kontekst, deling, historikk og feiltilstander.
G1-GUI venter fortsatt. En GUI-godkjenning betyr ikke at backend, rettigheter eller
produksjonsklarhet er godkjent; G2-plan og G3-akseptanse gjenstår.

| Flate | Kandidater |
|---|---|
| Developer Workbench + hjelpechat | Tom, fylt, frakoblet/uavklart køstatus; lys/mørk |
| Selvstendig hjelpechat | Tom, fylt, frakoblet, blokkert merge, ekstern modell; lys/mørk |
| Butler-innbygging | Tom, fylt, frakoblet; lys/mørk |
| Egne perspektivpakker | Ny, fylt, versjonskonflikt; navn, formål, instruksjoner, skills/kontekst, deling |
| Kontekst og skills | Valgte/tilgjengelige kilder og skills; lys/mørk |
| Del pakkeversjon | Konkrete referanser, versjon, publikum og avslag; lys/mørk |
| Ekstern modell | Mottaker, eksempelmodell, valgte utdrag, avslag og lokal vei; lys/mørk |
| Historikk | Privat, prosjektets delte hendelse, ingen treff, utilgjengelig; lys/mørk |
| Skeleton-komponent | To uavhengige mounts/samtaler; lys/mørk |
| Smal bredde | Selvstendig chat tom/fylt/frakoblet, 390 px; lys/mørk |

Alle person-, prosjekt-, modell- og jobbeksempler er syntetiske. «Tillatt rute»,
«lokal modell», tidsstempler og tilgangsstatus er eksempeltilstand, ikke verifisert
tilgang eller aktuelle leverandørvalg. Butler-rammen er også en kandidat, ikke en
påstand om dagens Butler-side. Den samme hjelpechat-Skeletonen brukes i de tre
vertsflatene per tema; det er ikke laget en separat React-chat.

## Kontroll som faktisk er utført

{len(cases)} offline rendringer, {actions} registrerte kontrollhandlinger på {len(unique)}
keypaths. Ingen registrerte JS-/unsupported-/komponentfeil eller horisontal overflyt.
Laveste målte tekstkontrast er {minimum:.2f}:1; måleavgrensning står i `images/README.md`.
Alle synlige knapper og felt i hver rendring er aktivert/fylt og alle picker-valg
registrert. Dette er dispatch-bevis, ikke bevis på en utført domenehandling.

Komponentprøven kontrollerte forskjellige strenger med forskjellige mount-ID-er
ved Ctrl+Enter, og session-ID-er på Send. Direkte innsetting av fixture-projeksjon
viste at et perspektivvalg kan oppdateres uten å endre den andre velgeren, og at
to mounts kan vise et felles perspektiv mens lokale utkast bevares. Dette beviser
ikke ekte session-synkronisering, Flow, replay eller backendisolasjon.

## Konkrete implementeringskrav fra prøven

1. **Skriv → Send/Lagre:** vanlig TextArea-input huskes lokalt; i denne isolerte
   rendereren sendte klikk på Send og Lagre bare den konfigurerte ID/revisjonen.
   Ny tekst manglet. Dette ble målt i begge temaer. Host-adapteren/cellekontrakten
   må sende ferske feltverdier atomisk med riktig mount, session og forventet
   revisjon. Samme krav gjelder typed search/title; disse to siste forløpene er
   ikke påstått funksjonelt testet. Ingen rendererendring er implementert her.
2. **Explore og actions:** `helper.*` i kandidaten er et foreslått bindingssett.
   Eksisterende Helper `ask`, `selectSet`, `saveSet` osv. må bevisst gjenbrukes eller
   utvides. Det nye settet er ikke validert mot en live Explore-manifest og skal
   ikke importeres som en ferdig operativ konfigurasjon.
3. **Velgere/forhåndsvisning:** søk sender en queryID, deling en previewID/revisjon.
   Backend må lese gjeldende valg, binde dem til samme bruker og avvise en foreldet
   forhåndsvisning. Valg alene autoriserer ingen deling eller ny modellrute.
4. **Hendelser og lagring:** kommando → autorisert varig endring → hendelse →
   projeksjon. Aktiv modellturn fryser kontekst/pakke; reconnect henter snapshot+
   etterslep. Replay kjører ingen effekt. Dette er godkjente krav, ikke funksjoner
   implementert av bildeharnessen.
5. **Privat/felles:** rå samtale holdes privat; prosjektet får bare eksplisitte
   minimale hendelser/utdrag. Tilgang må håndheves også for søk, counts, snippets,
   cache og embeddings. Ingen privacy-/rettighetstest mot backend er kjørt her.
6. **Autoritative kvitteringer:** køstatus leses med samme commandID ved usikkert
   utfall. AgentRun er en projeksjon, ikke en utfører. Merge og deploy trenger
   verifisert kilde/head/mandat og riktige effektceller. Ingen jobber er startet.

`SOURCE_AUDIT.md` og `SURFACE_ACTIONS.md` er grunnlaget for dagens kildegrenser og
hvor øvrige handlinger hører hjemme. Disse bildene erstatter ikke hele Board,
Configuration Studio, Agreement eller Admin-GUI. De flatenes konkrete endringer
må ha egne godkjente referansebilder dersom G2-arbeidet endrer dem.

## Videre kontroll

Swift-fabrikk må senere sammenlignes kanonisk med godkjent JSON, og faktisk
backend-state må rendres og sammenlignes med de godkjente bildene. Native Binding,
autentisert Porthole, tilgjengelighet og hele idé→prod-forløpet må testes før G3.
Ingen produktkode, build, CI, PR, merge eller deploy er gjort av denne GUI-leveransen.

Uavhengig gjennomgang: se `GUI_INDEPENDENT_REVIEW.md` når etterkontrollen er ferdig.
'''
(ROOT/'GUI_REVIEW.md').write_text(review)

titles=[('workbench-filled','Developer Workbench'),('packages-filled','Egne perspektivpakker'),
        ('context-filled','Kontekst og skills'),('share-filled','Del en bestemt versjon'),
        ('model-context-filled','Mottaker og datagrunnlag'),('history-filled','Privat historikk'),
        ('history-shared','Prosjektets historikk'),('butler-filled','Inne i Butler'),
        ('standalone-empty','Selvstendig chat'),('standalone-error','Frakoblet / usikkert utfall')]
blocks=[]
for slug,title in titles:
    figures=''.join(f'<figure data-theme="{theme}"><a href="images/{slug}-{theme}.png"><img loading="lazy" src="images/{slug}-{theme}.png" alt="{html.escape(title)} — {theme}"></a><figcaption>{"Lys" if theme=="light" else "Mørk"}</figcaption></figure>' for theme in ['light','dark'])
    blocks.append(f'<section><h2>{html.escape(title)}</h2><div class="pair">{figures}</div></section>')
other=''.join(f'<li><a href="images/{x["name"]}.png">{html.escape(x["name"])}</a></li>' for x in shots)
gallery='''<!doctype html><html lang="nb"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Workbench hjelpechat — GUI-kandidat</title><style>
body{margin:0;background:#f5f5f7;color:#1d1d1f;font:16px/1.5 -apple-system,BlinkMacSystemFont,sans-serif}
main{max-width:1500px;margin:auto;padding:28px}h1{letter-spacing:-.6px}h2{font-size:23px;margin-top:40px}.note{max-width:950px}
nav{position:sticky;top:0;background:#f5f5f7ed;padding:12px 0;z-index:2;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
button,a{color:#0068d6}button{font:inherit;background:white;border:1px solid #999;border-radius:7px;padding:7px 14px;cursor:pointer}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%;border:1px solid #d4d4db;border-radius:8px}figcaption{margin-top:5px;color:#62626b}
details{margin-top:30px}li{margin:5px 0}[hidden]{display:none!important}@media(max-width:700px){.pair{grid-template-columns:1fr}main{padding:16px}}
</style><main><h1>Workbench hjelpechat</h1><p class="note">Designkandidat for G1-GUI. G1 er godkjent. Bildene viser planlagt brukerflate med eksempeldata, rendret i dagens Skeleton-renderer. Ingen modellkall, lagring, jobb eller deploy utføres.</p>
<p class="note"><strong>Kjent implementeringsgap:</strong> Send/Lagre må få med det nyeste tekstutkastet. Testen påviser at dette ikke skjer automatisk i den isolerte rendereren.</p>
<nav><button onclick="choose('both')">Begge temaer</button><button onclick="choose('light')">Lys</button><button onclick="choose('dark')">Mørk</button><a href="GUI_REVIEW.md">Omfang og kontroll</a><a href="images/README.md">Bevis og gjenskaping</a></nav>
'''+''.join(blocks)+f'<details><summary>Alle {len(shots)} bilder, inkludert avslag og smal bredde</summary><ul>{other}</ul></details>'+'''
</main><script>function choose(t){for(const f of document.querySelectorAll('figure'))f.hidden=t!=='both'&&f.dataset.theme!==t;for(const p of document.querySelectorAll('.pair'))p.style.gridTemplateColumns=t==='both'?'':'1fr'}</script></html>'''
(ROOT/'GUI_GALLERY.html').write_text(gallery)
facts=dict(cases=len(cases),actions=actions,uniqueActions=len(unique),minimumTextContrast=minimum,
           images=len(manifest),bytes=sum(x['bytes'] for x in manifest),knownIntegrationGaps=report['knownIntegrationGaps'])
(ROOT/'images/review-facts.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(facts,ensure_ascii=False))
