# PLAN — broen på i prod og staging

Oppgavemappe: `PDD_bro-paa-i-prod_2026-09-26` · Skrevet 2026-09-27 av Losen · **G2 godkjent 2026-09-27** (V1–V3 som anbefalt)

Grunnlag: `FORMAALSSPEC.md` (G1 godkjent 2026-09-27) og Astras trusselmodell `handoff/ASTRA-TRUSSELMODELL.md` (10 funn, 2 blokkerer). Planen lukker alle ti funnene eller sier hvor de er behandlet.

## 0. Hva dette innebærer, kort

Broen kan ikke bare slås på igjen. Astra fant at den gamle ruten slapp inn hvem som helst som sa «ready», og at ingen kanal i dag er bundet til en bevist identitet (F01). Derfor bygges broen på nytt med et **håndtrykk ved åpning**: klienten beviser identiteten sin ved å signere en utfordring fra serveren **lokalt, med sin egen nøkkel**. Serveren ser bare den offentlige nøkkelen. Etterpå er kanalen låst til den identiteten, og hver celle avgjør som før hva den får gjøre.

Det meste av arbeidet ligger i **CellProtocol**, fordi håndtrykket og låsingen må virke likt for alle scaffolds. CellScaffold får ruten, helsesjekken og kvotene. HavenAgentD og de andre klientene må lære håndtrykket; gamle klienter vil få «koblet til», men ikke «autentisert». Utrullingskjeden får en ekstern bro-probe, så broen aldri igjen kan forsvinne uten at en utrulling stopper.

## 1. Håndtrykket (figur)

Se `images/bro-haandtrykk-v1.png`. Tekstversjon:

```
Klient-scaffold (nøkkel lokalt)          TLS-proxy        CellScaffold /bridgehead/<publisher>/<broId>
  │ 1. åpner WSS, sjekker sertifikat ───────▶│──────────────▶│ 2. bare auth-meldinger tillatt, frist 10 s
  │ 3. hello: offentlig nøkkel + nonce ──────────────────────▶│
  │◀───────────────────────────────────── 4. challenge: servernonce, sesjon, utløp, rute
  │ 5. signerer LOKALT (openBridgeChannel, bundet til akkurat denne forbindelsen)
  │ 6. signatur ─────────────────────────────────────────────▶│ 7. verifiserer med offentlig nøkkel,
  │                                                            │    bruker utfordringen én gang
  │◀────────────────────────────────── 8. authenticated: sesjon, identitet, utløp
  │ 9. get/set/feed ─────────────────────────────────────────▶│ 10. requester = den beviste identiteten,
  │                                                            │     målcellen autoriserer som lokalt
```

Privat nøkkel forlater aldri klienten. Serveren lagrer ingen signatur som kan brukes igjen, og ingen nøkkel eller vault for brukeren.

## 2. Arbeidspakker (1:1 mot bladformålene)

| AP | Bladformål | Hva gjøres | Lukker Astra-funn | Test (FORMAALSSPEC §5) | Utfører |
|---|---|---|---|---|---|
| **AP1** | kanalen-er-bundet-til-identitet | CellProtocol: ny auth-profil `openBridgeChannel` (bygger på `IdentitySigningChallenge`-formatet og den offentlige signaturverifieren), tilstandsmaskin *uautentisert → utfordret → verifiserer → autentisert → lukket* foran all BridgeBase-dispatch, transcript bundet til forbindelse/generasjon/rute, engangsforbruk per forbindelse, uforanderlig requester for resten av kanalen. Gjelder dedikert og multiplex. | F01, F03, F06 | test.bro.auth-negative | Codex (Astra) |
| **AP2** | noklene-forblir-private | CellProtocol: transportadapterne Apple og Lightweight får samme grense som Vapor (en presentert deskriptor gir aldri lokal vault); minimal offentlig deskriptor i håndtrykket; ingen server-signer for brukeridentiteten; logging bare med årsakskoder. | F02, §5 | test.bro.noklene-private | Codex (Astra) |
| **AP3** | celleautoritet-uendret | Samme get/set/feed kjøres lokalt og over broen med feil requester, feil keypath, tilbakekalt kontrakt og `purpose://prompt.unknown` — lik avvisning. Ingen felt i håndtrykket gir rettigheter. | F06 | test.bro.celleautoritet | Codex (Astra) |
| **AP4** | robust | CellProtocol + CellScaffold: kanalutløp (5 min, fornyes av klienten), generasjon som ugyldiggjøres ved brudd, ny auth ved reconnect, ingen automatisk gjentakelse av skriveoperasjoner, sendfeil meldes oppover, kvoter før dyre operasjoner (per kilde, per identitet, globalt), heartbeat og kontrollert drain. Reconnect ≤ 30 s. | F04, F07, F10 | test.bro.robust | Codex (Astra) |
| **AP5** | kanalen-finnes | CellScaffold: registrert `/bridgehead/<publisher>/<broId>` med porten fra AP1 foran celleoppslag, lokalt rutekart (ikke rettigheter), kanonisk WSS-origin per miljø, bro-oppdagelsen annonserer bare den sikre ruten, ny CellProtocol-pin. Native-porthole røres ikke. | F05 (server), F08 | test.bro.probe, test.bro.ci-route | Codex (Astra) |
| **AP6** | aldri-stille-av-igjen | CellScaffold: `/health/ready` får en påkrevd `bridge`-del (rute, verifier, sesjonslager, kvoter) og svarer 503 uten den; CI starter appen og tester ruten, ikke tekstsøk. HAVEN-Deploy: ekstern probe før promotering — WSS → signert håndtrykk → én beskyttet celleoperasjon → ett forsøk uten bevis som skal avvises. Proxyen på verten kontrolleres (overskriver forwarded-headere, ingen direkte backend). | F08, F05 (proxy) | test.bro.deploy-gate | Codex (CS-delen), Losen (proxy og probe) |
| **AP7** | klientene-treffer | CellProtocol-resolveren (standardklienten), HavenAgentD relay og correspondence, bro-oppdagelsen og SkeletonParity-fiksturen lærer håndtrykket. HAVEN-appens kodevei identifiseres først og tas med. HavenAgentDs lokale token-bro forblir lokal. | F05 (klient), F09 | test.bro.klienter, test.bro.e2e | Codex (Astra) |
| **AP8** | aerlige-paastander | Gjennomgang av påstander siden 13.07 om kontakt med prod/staging (rapporter, PDD-er, prosjektdokumenter, morgenrapporter): over HTTP / over bro / uverifisert, med rettelse der påstanden var feil. | — | test.bro.paastander | Losen — kan starte nå |
| **AP9** | ingen-svake-ledd | Astra etter-gjennomgang to ganger: (a) CellProtocol-PR-en før merge til main, (b) hele kjeden i staging før prod, med faktisk proxykonfig og positive/negative resultater. Hvert funn rettes eller aksepteres skriftlig av Kjetil. | alle | test.bro.astra | Astra, Kjetil avgjør |
| **AP10** | root | Utrulling: staging først (probe grønn, HavenAgentD på Mac-en henter en verdi), så prod med samme image. | — | test.bro.e2e | Losen |

## 3. Rekkefølge

```
AP8 (Losen, nå) ─────────────────────────────────────────────────────────────┐
AP1 + AP2 + AP3 + AP4(CP-del)  ──▶ CP-PR ──▶ AP9a Astra ──▶ Kjetil: merge CP ──▶ AP5 + AP6(CS) + AP4(CS-del) ──▶ CS-PR
                                                                                      │
AP7 (klienter, parallelt når CP-API-et står) ─────────────────────────────────────────┤
                                                                                      ▼
                                              AP6 (proxy + probe) ──▶ staging ──▶ AP9b Astra ──▶ prod (AP10)
```

CellProtocol først, fordi både CellScaffold og klientene bygger på det. Din regel fra 18.09 gjelder: ny kapabilitet i CellProtocol testes mot funksjon og formål før den går til main — derfor Astra-gjennomgang og ditt ja før CP-merge.

## 4. Det du selv skal gjøre

1. **G2** på denne planen, og svar på de tre valgene i §5.
2. **Ja/nei til CP-merge** etter Astras første etter-gjennomgang (AP9a).
3. **Ta stilling til gjenstående funn** Astra ikke får lukket (om noen), skriftlig.
4. **G3**: se probe-resultatet og HavenAgentD-kjøringen mot prod.

Alt annet gjør Losen og Codex.

## 5. Valg som endrer planen

| # | Valg | Anbefalt | Alternativ |
|---|---|---|---|
| V1 | Etter åpning: kan en celle fortsatt be klienten om et snevert identitetsbevis (klienten signerer lokalt, bare for den ene cellen og den ene operasjonen), slik det virker i dag? | **Ja.** Minste riktige første leveranse (Astra §4). Nøkkelen er fortsatt bare hos klienten. | Nei: én signatur per kanal, og en ny intern beviskontekst i CellProtocol (`VerifiedRequesterContext`) så prod aldri ber om mer. Større endring i CellProtocol-runtime; kan tas som steg 2. |
| V2 | Stoler vi på TLS-proxyen og serverprosessen etter håndtrykket? | **Ja i første leveranse**, med proxyen herdet og kontrollert (AP6). Standard for WSS. | Hver kommando signeres ende-til-ende, så selv en overtatt proxy ikke kan endre dem. Betydelig større; eget formål senere. |
| V3 | Hvor ligger probe-identitetens private nøkkel (den som tester broen før hver promotering)? | **På Mac-en**, i en egen probe-identitet som køen bruker. Ikke brukerens nøkkel, ikke på verten. | GitHub Actions-hemmelighet — da ligger nøkkelen i skyen. |

## 6. Avhengigheter og risiko

- **Mac-disken**: ca. 110 GiB ledig 27.09; to Swift-bygg etter hverandre får plass. Ryddeskript: `HAVEN-Deploy/_handoff/RYDD/`.
- **Release 2026.9.2** (egen tråd) endrer CellProtocol-pinnen til tagger. AP5 må bruke den pinnen som gjelder når CS-PR-en lages; les `origin/main:Package.swift` da, ikke nå.
- **Gamle klienter** får 101, men aldri «autentisert», og blir avvist. Det er riktig oppførsel; klientene må oppdateres (AP7) før e2e.
- **Tidsbruk**: CP-delen er størst. Grovt anslag: CP-PR 1–2 døgn med CI og Astra, CS-PR 1 døgn, staging og prod ½ døgn. Anslag, ikke mål.

## 7. Forventningskontrakt (fra FORMAALSSPEC §3)

Uendret. Fremdrift telles bare som rader der: probe-utdata, HavenAgentD-kjøring, negative tester i CI, reconnect-måling, deploy-logg med stoppet/sluppet utrulling, påstandslisten, og PR-ene merget og rullet ut.

## 8. Tillegg etter G2 (2026-09-27)

- **Samme BridgeBase.** Det finnes én Swift-bro: CellProtocol `Sources/CellBase/Cells/Bridging/BridgeBase.swift`. Den brukes av CellScaffold (native-porthole, entity-data-ruten, AdminScaffold), HavenAgentD (lokal kontrollbro) og Binding. Prod (CP `473357cf`) og dagens main-pin i CellScaffold og HavenAgentD (`5609a9ad`) skiller seg bare med #49 (lås rundt beskrivelsesfeltene, 25.09). Transportene, `IdentitySigningChallenge` og bevisautorisasjonen er byte-like. Planen erstatter ikke BridgeBase; den legger håndtrykket foran dispatch i den.
- **AP5** skal gjenbruke mønsteret i CellScaffold `Sources/App/Controllers/VaporPersonEntityReadRoute.swift` (bevis før oppgradering, reservasjon, utløp), som finnes men ikke er registrert i prod — ikke lage en parallell mekanisme.
- **AP9** dekker også AdminScaffolds egen bridgehead (`Sources/ScaffoldKit/AdminScaffoldBridgeRoutes.swift`, admin-autentisert) og entity-data-ruten.
- **Utenfor denne PDD-en:** PyCellProtocol, RustCellProtocol og GoCellProtocol har egne broimplementasjoner. De må få samme håndtrykk for å kunne snakke med prod; det blir egen oppgave.
