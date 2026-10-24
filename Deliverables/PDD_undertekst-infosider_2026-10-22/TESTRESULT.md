# TESTRESULT — undertekst infosider (P4)

Kjørt 2026-10-22 i Cowork-VM-en på klonen `/home/claude/cellprotocoldocuments`, gren `claude/undertekst-infosider-20261022`. «Før» er `git archive origin/main` (ad91600) pakket ut i en midlertidig mappe. Alt under er faktisk utdata, limt inn uendret (bortsett fra at `exit=` er lagt til av kjøreskriptet). Tester som ikke kan kjøres før utrulling står som `blocked` med grunn.

## test.build {#build}
Formål: purpose://quality.build-and-regression. Statisk nettsted, intet bygg; vakten er bygget.

Etter (gren):
```
OK: HAVEN app-entry er blocked; heroen har to handlinger.
exit=0
```

Før (origin/main ad91600):
```
OK: HAVEN app-entry er blocked; heroen har to handlinger.
exit=0
```

Resultat: **grønn**. Heroen er uendret, så vakten gir samme svar før og etter.

## test.regression {#regression}
Formål: purpose://quality.build-and-regression.

Før (origin/main ad91600):
```
........
----------------------------------------------------------------------
Ran 8 tests in 0.006s

OK
exit=0
```

Etter (gren):
```
........
----------------------------------------------------------------------
Ran 8 tests in 0.004s

OK
exit=0
```

Resultat: **grønn**, 8 tester før og 8 etter, ingen nye tester (ingen ny logikk).

## test.text-present {#text}
Formål: purpose://candidate.undertekst-infosider.forside / .artikkel / .oversikt.

```
Website/index.html:235:          <h2>Din grense, båret av fellesskapet.</h2>
Website/artikler/mennesket-forst/index.html:7:  <meta name="theme-color" content="#f4f3ee"><meta property="og:title" content="Mennesket først betyr ikke mennesket alene – HAVEN"><meta property="og:description" content="Din grense, båret av fellesskapet."><meta property="og:type" content="article"><meta property="og:image" content="/assets/haven-control-loop-20260803.webp">
Website/artikler/mennesket-forst/index.html:17:      <p class="standfirst">Din grense, båret av fellesskapet: HAVEN begynner ved individets grense, men grensen må bæres av et økosystem som gjør gode valg enkle og misbruk vanskelig.</p>
Website/artikler/index.html:99:            <p>Din grense, båret av fellesskapet: råderetten må støttes av rettigheter, trygge standardvalg, fellesskap og ansvarlige institusjoner.</p>
exit=0
```

Antall filer med treff: 3 (forventet 3: `Website/index.html`, `Website/artikler/index.html`, `Website/artikler/mennesket-forst/index.html`). Artikkelen har to treff (ingress og `og:description`), slik utgivelsesnotatet forventer ved `curl`-kontrollen.

Resultat: **grønn**.

## test.docs-updated {#docs}
Formål: purpose://quality.docs-in-same-change.

```
15:      <div class="article-meta"><span class="tag">Verdigrunnlag</span><span class="tag">Prinsipp</span></div><p class="article-date">Sist faglig gjennomgått 22. oktober 2026.</p>
```

`Website/RELEASE_NOTE_2026-10-22.md` finnes i samme endring. Evidensen føres også i ACCEPT.md#docs ved G3.

Resultat: **grønn** (dokumentdelen; selve ACCEPT.md skrives ved G3).

## test.status-current {#status}
Formål: purpose://quality.work-is-visible. STATUS.md-loggen er oppdatert i samme commit som denne filen; portene står som `venter` fordi Kjetil ikke har gitt ordet. Kontrolleres mot mappen ved G3.

Resultat: **grønn** per 2026-10-22.

## test.gui.reference-image-exists {#gui-reference}
Formål: purpose://gui.expectation-agreed-before-build. Filer i `images/`:

```
etter-artikkel.png
etter-artikkeloversikt-kort.png
etter-forside-seksjon-mobil.png
etter-forside-seksjon.png
for-artikkel.png
for-artikkeloversikt-kort.png
for-forside-seksjon-mobil.png
for-forside-seksjon.png
```

Fire etter-bilder, hvert med sitt før-bilde. Mobilbildene ble tatt om igjen i runde 2 fordi toppmenyen la seg over seksjonen i et elementskjermbilde (se `images/README.md`).

Resultat: **grønn** for «bildene finnes»; **Kjetils godkjenning (G1-GUI) venter.**

## test.gui.parity {#parity}
Formål: purpose://gui.parity-with-approved-image.

Resultat: **blocked** — krever at Kjetil har rullet ut (RELEASE_NOTE_2026-10-22.md). Tas som skjermbilder av https://digipomps.org/ , /artikler/ og /artikler/mennesket-forst/ i samme viewporter og legges i ACCEPT.md#parity.

## Ikke relevante
- test.gui.load-time, test.skeleton.no-unreachable-elements, test.skeleton.purpose-actions-reachable: ikke relevante, begrunnet i FORMAALSSPEC §5.
