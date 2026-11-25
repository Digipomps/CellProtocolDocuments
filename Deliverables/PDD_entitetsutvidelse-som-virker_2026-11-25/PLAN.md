# PLAN — Entitetsutvidelse som virker (P2, venter på G2)

Grunnlag: FORMAALSSPEC.md iterasjon 2. **G1 godkjent av Kjetil 2026-11-25 12:49. G1-GUI godkjent 2026-11-25 15:14** («G1-GUI Godkjent. 1 ja 2 ja.»): «Trekk tilbake» spør én gang til uten passkey, og de tre ordene beholdes.

Kjetil, samme melding: «dette er generell funskjonalitet som alle scaffolds kan ha nytte av». Planen legger derfor alt i protokollbibliotekene, og ingenting i én bestemt vert. Se «Hvor koden havner».

## Dette skal du gjøre (Kjetil)

| Når | Hva | Hvorfor |
|---|---|---|
| Nå | Si **«G2 godkjent»**, eller «auto» for å la meg gå gjennom leveranse 1 uten flere spørsmål. | Ingen kode skrives før G2. |
| Før WP1 | Flette CellProtocol #114 (avgrenset lenke), eller si at den skal vente. | A2 og prøvesettet bruker avgrenset lenke. Uten den bygger jeg WP1 oppå greina til #114. |
| Underveis | Flette utkastene etter hvert som de er grønne på macOS: PyCellProtocol #5, CellScaffold #514, og de nye fra denne planen. | Jeg fletter aldri. |
| WP11 | Godkjenne med passkey på en ekte enhet, én gang, mens jeg tar opptaket som teller håndgrep. | Bare du har passkeyen. |
| WP11 | Si ja til at forespørselen til HAVEN-Deploy sendes. | Staging går bare gjennom Deploy. |
| Ved G3 | Lese `ACCEPT.md` og si «G3 godkjent» eller hva som er feil. | Bare ditt ord setter porten. |

## Hvor koden havner

| Sted | Hva | Hvem bruker det |
|---|---|---|
| **CellProtocol, `CellBase`** | Alle regler: avtale følger entiteten, bærbart bevis, statusliste, kartposter, avvisningskoder med tekst, og de to flatene som `CellConfiguration`-fabrikker. | Hver vert som bygger på CellProtocol: CellScaffold, Binding, og andre scaffolds. |
| CellProtocol, `CellVapor` og `CellApple` | De to ankrene kaller de samme reglene i CellBase. Ingen regel står to steder. | Server og app. |
| **PyCellProtocol** og **gocellprotocol** | Samme avgjørelse og samme koder, prøvd mot det samme prøvesettet. | Python- og Go-scaffolds. |
| CellScaffold | Bare tilkobling: passkey-verifikatoren som alt finnes, én rute for å hente statuslisten, menyoppføring, og ny pin. **Ingen tilgangsregel.** | Staging. |
| Binding | Menyoppføring og ett ordforråd for scopes. | Appen. |

Prøven på at det er felles: `test.utvidelse.any-scaffold` (ny, C3). Den samme ende-til-ende-prøven kjøres mot en Python-scaffold (`cellprotocol_scaffold`) som ikke har én linje fra CellScaffold. Og et skript viser at endringen i CellScaffold ikke inneholder noen tilgangsavgjørelse.

## Arbeidspakker (1:1 mot bladformål, i avhengighetsrekkefølge)

Utfører: **Claude (sky)** skriver kode og kjører Linux-testene i Docker (`swift:6.1-noble`), `pytest` og `go test`. **Mac** = macOS-kjøring på Kjetils Mac under `/Volumes/Backup/build`, etter tidsluke fra Deploy. **Kjetil** = bare radene i tabellen over.

### Leveranse 1 — avtaler og bærbar lenke

| WP | Bladformål | Hva det innebærer | Utfører | Gjør grønn | Leverer til §3 |
|---|---|---|---|---|---|
| WP0 | §2, de to radene «ikke målt» | To tester på uendret `main` som viser dagens svar: lenket nøkkel under en avtale gitt til eiernøkkelen, og lenket nøkkel på en annen vert. Antall tester før endring i hvert repo. | Claude (sky), så Mac | test.build, test.regression (grunnlinje) | `TESTRESULT.md#baseline` |
| WP1 | A1, A2, antiformål «aldri mer enn entiteten» | I tilgangsavgjørelsen i CellBase: en avtale gitt til en av entitetens hele nøkler gjelder for alle hele nøkler, også avtaler som finnes fra før. Avgjørelsen navngir lenke og avtale. Avgrenset lenke arver aldri. | Claude (sky), så Mac | test.utvidelse.agreement-linked, agreement-scoped-negative, never-wider | `#agreement-linked` |
| WP2 | B1 | `EntityLinkAdmission` i CellBase: en vert godtar `SameEntityIdentityLinkCredential` bare når utstederen alt er entiteten der, og nøkkelen beviser seg selv. Egne koder for fremmed utsteder, feil nøkkel, kopi uten privatnøkkel, utløpt. | Claude (sky), så Mac | test.utvidelse.portable-admit, portable-negative | `#portable-admit` |
| WP3 | B2 | Beviset bærer passkey-bekreftelsen over forespørselens hash. Verten setter selv publikum og opphav. Lukker resten fra E3 i revisjonen. | Claude (sky), så Mac | test.utvidelse.fresh-passkey, host-sets-audience | `#portable-admit` |
| WP4 | B3 | Signert statusliste: ankeret utsteder, verter henter, grense ti minutter, verten med ankeret er unntatt. Klokke injiseres i testene. | Claude (sky), så Mac | test.utvidelse.revoke-propagates, stale-status-denied | `#revoke-propagates` |
| WP5 | C1, C2, C3 | `contract/link-fixtures.v1.json` lages av Swift-testene. Samme avgjørelse bygges i PyCellProtocol og gocellprotocol og prøves rad for rad. Én scope-liste i CellBase. `test.utvidelse.any-scaffold` mot Python-scaffolden. | Claude (sky) | test.utvidelse.parity-fixtures, vocabulary, any-scaffold | `#parity-fixtures` |

### Leveranse 2 — kartet og flatene

| WP | Bladformål | Hva det innebærer | Utfører | Gjør grønn | Leverer til §3 |
|---|---|---|---|---|---|
| WP6 | E1, E2, E5, antiformål «kartet gir aldri tilgang» | `scaffoldPresence` i entitetsdataene: hvert scaffold signerer sin post, de andre har kopi med kilde, revisjon, hash og alder. Entitetens lenkede klient bærer postene mellom scaffolds. Leses bare med eierbevis eller hel lenke. `contract/scaffold-presence.v1.json`. | Claude (sky), så Mac | test.entitetskart.presence, cache-no-authority, private | `#entitetskart` |
| WP7 | E3, E4 | Oppslag «hvor kan jeg be om hjelp» for et formål. Seks tilstander per sted, hver med neste steg. | Claude (sky), så Mac | test.entitetskart.help-lookup, reachability | `#entitetskart` |
| WP8 | D1, D2, E6 | Fabrikker i CellBase for «Min entitet» og «Koble til enhet», byte-like med `skeleton/*.cellconfiguration.json`. `entityMap.state` og `enrollmentView` fra ekte data. Handlingene fra `images/render-report.json`. Avvisningstabell: hver kode har tekst og neste steg. Nytt bilde av bekreftelsen for «Trekk tilbake», rendret på samme måte og vist deg før G3. | Claude (sky), så Mac | test.utvidelse.refusal-texts, test.gui.parity (web), test.utvidelse.handgrips (fra bildene) | bildene, `ACCEPT.md#gui` |

### Leveranse 3 — rester og virkelig bruk

| WP | Bladformål | Hva det innebærer | Utfører | Gjør grønn | Leverer til §3 |
|---|---|---|---|---|---|
| WP9 | F1, F2 | `proofs` ut av malen til ankeret i CellVapor, etter at kontraktene som bruker den er talt. Lenking av hjemmescaffoldet går gjennom den samme seremonien som en ny enhet, med flaten fra bildene. | Claude (sky), så Mac. Tellingen på staging: forespørsel til Deploy | test.utvidelse.leftover-proofs, leftover-home-venue | `#leftover-*` |
| WP10 | C2 (Binding), integrasjon | CellScaffold: ny pin, rute for statuslisten, menyoppføring. Binding: menyoppføring og scope-listen fra CellBase. Bygg prøvd på Mac før noe går i kø til CI. | Claude (sky), Mac | test.build, test.regression, test.utvidelse.vocabulary (Binding) | PR-lenker |
| WP11 | R, D1 | Staging og Mac-en hjemme: lenk en telefon én gang, les en egen celle og en celle gitt ved avtale begge steder, trekk lenken og mål tiden. Opptak der håndgrepene telles. `TESTRESULT.md`, `ACCEPT.md`, lærdommer. | Kjetil (passkey) og Claude | test.utvidelse.e2e, handgrips (opptak), test.gui.parity, test.status-current | `#e2e`, `ACCEPT.md` |

## Rekkefølge

Som baner per aktør: `images/plan-v1.png`.

```
WP0 ─► WP1 ─► WP2 ─► WP3 ─► WP4 ─► WP5        leveranse 1
                      │
                      └────► WP6 ─► WP7 ─► WP8  leveranse 2
WP9 (F1 når som helst etter WP0, F2 etter WP3 og WP8)
WP10 etter WP5 og WP8 ─► WP11                  leveranse 3
```

Hver leveranse er egne PR-er: én i CellProtocol, én i PyCellProtocol, én i gocellprotocol. De åpnes som utkast og merkes klare når macOS er grønt.

## Stoppregler

Jeg stopper og sier fra til deg, uten å prøve igjen, når:

- en test som alt er sjekket inn må endres for at noe skal bli grønt,
- en sjekk i CI er rød, uansett årsak. Jobben kjøres ikke på nytt uten ditt ord,
- WP0 viser et annet svar enn spesifikasjonen sier at dagens kode gir,
- tellingen i WP9 viser at kontrakter på staging bruker `proofs` gjennom malen,
- noe i planen krever en tilgangsregel i CellScaffold eller en annen bestemt vert,
- en endring i skjelettformatet eller rendereren ser ut til å trengs.

## Kjøreregler

- Ingen `swift build` eller `swift test` på Mac-en uten tidsluke fra Deploy. Lange kjøringer går på Mac-en.
- macOS-CI koster penger. Hver gren bygges og testes på Linux i skyen og på Mac-en før den skyves til en PR som starter CI.
- Tilgang avgjøres bare av avtalevilkår, likt i Swift, Python og Go. Swift er førsteklasses i hver flyt.
- Ingen fletting, tagging eller utrulling fra meg.

## Ikke i denne planen

Formålsavgrensning og sikkerhetsnivå for egne agenter (iterasjon 2 av `PDD_egen-agent-mcp`, venter på egen G1), gjenoppretting av tapt eiernøkkel, gruppeentiteter, QR-kode i skjelettformatet, og native bilde fra Binding utover menyoppføringen.
