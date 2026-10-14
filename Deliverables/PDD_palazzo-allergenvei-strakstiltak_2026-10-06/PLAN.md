# PLAN — palazzo allergenvei strakstiltak

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_palazzo-allergenvei-strakstiltak_2026-10-06` · Skrevet 6. oktober 2026 kl. 10:47–11:05 UTC, før noe i `PalazzoScaffold` er rørt.

Stier er relative til HAVEN-roten. `HD` står for `HAVEN-Deploy/_handoff/HD-0077`, `PS` for `PalazzoScaffold`, `CPD` for `CellProtocolDocuments`, og `PDD` for denne oppgavemappen. Alle klokkeslett er UTC. Formålene (S1–S5), testene (T0–T12) og stoppreglene er de som står i den godkjente spesifikasjonen, `PDD/FORMAALSSPEC.godkjent-G1-iterasjon1.md`. Planen legger ikke til og tar ikke bort noe der.

G2: Kjetil valgte «Auto, hele veien» 6. oktober (lest kl. 10:42). Teksten på valget var Losens: «Plan, tester, endring, angrep, push, CI, utsetting og måling. Endringen settes ut uten at du har sett planen eller tallene, hvis ingenting stopper meg. Rundt fem timer.»

## Kort

**Hva som skjer, i denne rekkefølgen.**

```
 1 Grunnlinjen     hele testmengden på a3fc5042, før noe er endret          GJORT kl. 10:56: 265 tester, 0 feil
 2 Svarene før     de målte spørsmålene gjennom koden slik den står          gir «før» til testen om uendrede svar
 3 Tester først    de nye testene inn, koden urørt                           de skal være RØDE (T1, T3, T5)
 4 Endringen       regel 1, 2 og 3, eksempelet, og resten av testene         hele testmengden GRØNN, ingen gammel test endret
 5 Angrepet        nytt blindt sett fra en tråd som ikke har sett listen     frosset, målt ÉN gang gjennom koden
        │  STOPP: en merking ut, eller et publisert svar uten linje om allergener
 6 Commit og CI    bare navngitte filer; push; GitHub bygger og tester       STOPP: rød to ganger på samme commit
 7 Lest før byttet claimene, loggen til utgaven som står, veien tilbake      STOPP: enhver claim på verten
 8 Utsettingen     HD/mac/deploy-vert-20261003.sh med egen claim             etter byttet ruller jeg ikke tilbake uten Kjetils ord
 9 Måling på nett  174 kall, 30 per ti minutter                              STOPP: en merking, eller et svar uten linjen
10 Dokumentene     TESTRESULT.md og ACCEPT.md, kontrollert av en egen tråd   så G3 hos Kjetil
```

**Hva Kjetil må gjøre.** Ingenting før G3, så lenge ingenting stopper meg. Stopper noe, sier jeg fra med én gang, med hva jeg ser og hva valgene er. Er Mac-en av eller uten nett, er det han som må få den på nett igjen.

**Veien tilbake finnes, og den avhenger ikke av at siden svarer.** Den står under «Veien tilbake». Den er tørrkjørt, og forutsetningene er lest på verten. Selve byttet tilbake er ikke kjørt. Den brukes bare på Kjetils ord.

**Planen er kontrollert av en uavhengig tråd (K6) etter at koden var skrevet.** Den fant én feil i planen og 18 andre ting; de står under «Etter kontrollen K6», og teksten her er rettet.

**Fire ting som ikke sto i spesifikasjonen.** De to første fant jeg da planen ble skrevet, de to siste kom fram under arbeidet og i kontrollen K6.

- Arbeidsmappene til testkjøringen i `/tmp` på Mac-en var halvt ryddet bort (i `.git` manglet blant annet `HEAD` og `config`; `FETCH_HEAD` og `index` fra 3. oktober sto igjen). Første forsøk på grunnlinjen kom derfor aldri til testene. Mappene er flyttet til side, ikke slettet, og grunnlinjen er kjørt fra bunnen: 265 tester, 0 feil (`HD/maal/STRAKSTILTAK-T0B-20261006.md`). Årsaken er ikke målt. Det er ikke stoppregelen «testmengden er rød»: testene hadde ikke kjørt.
- Rettelsen «amming bare som eget ord» (godkjent i G1, punkt 4) gjør at hvert ord som har «amming» i seg uten å være nettopp det ordet, ikke lenger treffer: «ammingen», «amminga», «fullamming», «ammingsperioden». «amming», «amme», «ammer», «ammet» og «ammende» treffer. Det legges fram ved G3 sammen med det angrepet viser.
- Regel 1 står foran alt som spør oppslaget. Når kunnskapsgrunnlaget ikke lar seg laste, svarte tjenesten før HTTP 503 på alt, og når tilgangen til det blir avvist, HTTP 403. Nå får et spørsmål med et ord fra listen henvisningen med HTTP 200 også da. Det følger av «Oppslaget spørres ikke» (S1), men spesifikasjonen sier det ikke, og ingen test går gjennom de to tilfellene: de er lest i koden, ikke prøvd. Det legges fram ved G3.
- XCTest førte ikke alle feilmeldingene i de røde kjøringene: 30, 28, 30 og 26 av 125 i T1, alltid de første radene. Årsaken er ikke funnet. Testene samler derfor avvikene selv og kaster én feil til slutt med tallet. Den kom fram i hver kjøring («T1: 125 av 125 …»).

## Arbeidspakker

Én pakke per bladformål, i den rekkefølgen de bygger på hverandre. Utfører er Losen for alle; kjøringen skjer på Mac-en (bruker kjetil) gjennom køen `_losen-queue`, bane d.

| Pakke | Formål | Hva det innebærer | Test som skal bli grønn | Leveranse (§3) |
|---|---|---|---|---|
| WP0 Grunnlinje | `purpose://quality.build-and-regression` | Hele testmengden på `a3fc5042` mot CellProtocol `81601a6f`, før noe endres | T0: 265 tester, 0 feil. **Gjort.** | `PDD/TESTRESULT.md#foer` |
| WP1 Tester først | `….failures-are-tests` (gjenbrukt) | De målte spørsmålene og svarene koden gir dem i dag, blir fiksturer. Testene T1, T3, T5 og T6 legges inn mens koden er urørt. T1, T3 og T5 skal være røde, T6 grønn. Blir en av de tre ikke rød, måler den ingenting, og jeg retter testen før koden røres | T1, T3, T5 røde; T6 grønn; de 265 gamle grønne | `PDD/TESTRESULT.md#roed-foerst` |
| WP2 Regel 1, ordlisten | S1 `….referral-for-listed-words` | Ny fil `PS/Sources/App/Services/PalazzoAllergiHenvisning.swift` med listen (utgave 6) og treff-funksjonen. I `PS/Sources/App/Controllers/PalazzoCommunaleFacade.swift`: etter at spørsmålet er kontrollert for tomt og for langt, og før oppslaget spørres, gir et treff henvisningen. Kallet teller mot grensen som andre kall | T1, T2, T4 | Listen i koden; `PDD/TESTRESULT.md#listen` |
| WP3 Regel 2, ingen merking | S2 `….no-marking-on-guest-page` | I `PS/Sources/App/Controllers/PalazzoCommunaleProjection.swift`: et svar fra oppslaget med « er merket med: » blir henvisningen, før noe annet vurderes. Grenen som slapp merkingen gjennom (linje 148–150), tas ut | T3 | `PDD/TESTRESULT.md#merking` |
| WP4 Regel 3, linjen | S3 `….answers-point-to-staff` | Samme fil: hvert publisert svar der ingen advarsel har ordet allergi eller allergen, får linjen først blant advarslene. Hvilken linje avgjøres av svarformen (én rett, flere retter, alt annet). Feltet `answer` røres ikke | T5 | `PDD/TESTRESULT.md#linjen`; bildene |
| WP5 Vanlige spørsmål | S4 `….ordinary-questions-unchanged` | Ingen kode. Testen holder svarteksten etter mot svarteksten før, for hvert målt spørsmål listen ikke fanger | T6, T9 | `PDD/TESTRESULT.md#uendret`, `#regression` |
| WP6 Eksempelet | S5 `….example-is-answerable` | Én tekst i `PS/Public/palazzo/index.html`, linje 76: «For eksempel: Hvilke pizzaer har dere?» | T7 | `PDD/ACCEPT.md#eksempel` |
| WP7 Grunnen i loggen | `….reason-in-log` (gjenbrukt) | Fasaden skriver `utfall=allergi-henvisning:ordliste` eller `utfall=allergi-henvisning:merking`. Linjen bygges uten spørsmålet. For at testen skal kunne lese linjen, får fasaden loggeren som parameter med dagens logger som standard | T4; utdrag fra vertens logg etter utsettingen | `PDD/TESTRESULT.md#logg` |
| WP8 Angrepet | `….independent-attack` (gjenbrukt) | En ny tråd får bare oppgaven, menyen og siden. Den får ikke listen, ikke det første blinde settet og ikke koden. Settet fryses med md5 før måling og måles én gang gjennom `POST /palazzo/api/ask` i Swift. De to snarveiene måles som to faste kall. Funnene blir tester | T8 | `PDD/maaling/` |
| WP9 På nett | roten; `purpose://gui.parity-with-approved-image` | Commit av bare navngitte filer, hele testmengden på det committede treet, push, CI, lesing før byttet, utsetting, måling av de 174 kallene, skjermbilder | T9, T10, T11 | Kjørende flate; `HD/maal/`; `PDD/ACCEPT.md` |
| WP10 Alt virker | `pkg.std.everything-works` | `PS/README.md` i samme commit. `HD/README.md`, `PDD/STATUS.md`, `PDD/TESTRESULT.md` og `PDD/ACCEPT.md` følger. En uavhengig tråd holder de to siste mot bevisfilene | T12 | `PDD/ACCEPT.md#docs`, `#status` |

## Det som endres i koden

| Fil | Endring |
|---|---|
| `PS/Sources/App/Services/PalazzoAllergiHenvisning.swift` | NY. Listen i utgave 6, treff-funksjonen, grunnkoden `allergy-referral` og de to utfallene til loggen |
| `PS/Sources/App/Controllers/PalazzoCommunaleFacade.swift` | Regel 1 i `ask`. Utfallet `allergi-henvisning:merking` når publiseringen har gitt henvisningen. Loggeren som parameter |
| `PS/Sources/App/Controllers/PalazzoCommunaleProjection.swift` | Regel 2 og regel 3. Ny funksjon som gir henvisningens konvolutt |
| `PS/Public/palazzo/index.html` | Eksempelet i spørrefeltet (linje 76) |
| `PS/README.md` | Tiltaket beskrevet, og at det er midlertidig |
| `PS/Tests/AppTests/PalazzoAllergiHenvisningTests.swift` | NY. T1, T3, T5, T6 og målingen av et sett gjennom fasaden. Kompilerer mot `a3fc5042` |
| `PS/Tests/AppTests/PalazzoAllergiOrdlisteTests.swift` | NY. T2, T4, og at henvisningen føres i aktiviteten og teller mot grensen. Trenger den nye kildefilen |
| `PS/Tests/AppTests/Fixtures/allergi-ordliste-utgave6-20261006.json` | NY. Kopi av referanselisten: hver oppføring, ett eksempelord per oppføring, og ord som skal og ikke skal treffe |
| `PS/Tests/AppTests/PalazzoAllergiAngrepTests.swift` | NY, etter at angrepet er målt. Det frosne settet som test |
| `PS/Tests/AppTests/Fixtures/allergi-henvisning-maalt-20261006.json` | NY. Hvert målt spørsmål, og om referanselisten treffer |
| `PS/Tests/AppTests/Fixtures/allergi-henvisning-foer-20261006.json` | NY. Svaret koden på `a3fc5042` gir hvert av dem, målt i trinn 2 |
| `PS/Tests/AppTests/Fixtures/allergi-angrep-blind2-20261006.json` | NY. Det frosne settet fra angrepet |

Ingen eksisterende testfil endres. Oppslaget (`PS/Sources/App/Cells/PalazzoConciergeCorpusCell.swift`), modellen og vakten (`PS/Sources/App/Services/PalazzoConciergePhrasing.swift`, `PS/Sources/App/Services/PalazzoAnthropicPhraser.swift`) røres ikke.

**Listen.** Utgave 6 er utgave 5 med de to rettelsene fra G1, punkt 4, og ingenting annet: «amming» treffer bare som eget ord, og unntaket «reactivat» er tatt ut. 134 oppføringer og 3 unntak. Referansen er `HD/maal/grunnlag-20261006/ordliste_strakstiltak.py`; utgave 5 ligger urørt ved siden av som `ordliste_strakstiltak_v5.py`. Swift-koden skal treffe nøyaktig som referansen. T2 holder dem mot hverandre på hvert målt spørsmål.

**Hvor regel 1 står.** I fasaden, foran oppslaget. Henvisningen gis derfor også om kunnskapsgrunnlaget ikke lot seg laste (før: HTTP 503, «Concierge er midlertidig utilgjengelig»), og om tilgangen til det ble avvist (før: HTTP 403). Henvisningen viser til personalet, og det er riktig også da. Det står ikke i spesifikasjonen og er ikke prøvd; se «Fire ting» over.

**Hvor regel 2 står.** Først i publiseringen, rett etter at svaret fra oppslaget er kontrollert for form. Et merkesvar blir henvisningen også når det ellers ville blitt avvist av en annen grunn. Gjesten leser samme tekst i begge tilfeller.

## Kjeden

Hvert trinn er en `skript`-jobb i køen. Filene som skal inn i `PS`, ligger i `HD/strakstiltak-20261006/` med md5 i `MD5.txt`, og hvert trinn kontrollerer md5 før det kopierer.

| Trinn | Skript | Hva det gjør | Stopper når |
|---|---|---|---|
| 1 | `HD/mac/strakstiltak-t0b-20261006.sh` | Grunnlinjen. Gjort | Testmengden er rød |
| 2 | `HD/mac/strakstiltak-kjede-20261006.sh foer` | Testfilen og fiksturen med spørsmålene inn; bare målingen kjøres; svarene skrives til `HD/maal/` og blir fiksturen «før» | Treet er ikke `a3fc5042`, eller har fremmede endringer. Da trinnet ble kjørt kl. 11:17, krevde det ikke at kildefilene var urørt (bare `roed` gjorde det); at de var det, står som md5 i `HD/maal/STRAKSTILTAK-SVAR-FOER-20261006.md`. Kravet er lagt inn i trinnet kl. 12:20 |
| 3 | `HD/mac/strakstiltak-kjede-20261006.sh roed` | Hele testmengden med de nye testene, koden urørt | En gammel test er rød; T1, T3 eller T5 er ikke rød |
| 4 | `HD/mac/strakstiltak-kjede-20261006.sh groenn` | Endringen og den andre testfilen inn; hele testmengden; de fire nettestene (`node --test`) | Noe er rødt |
| 5 | `HD/mac/strakstiltak-sett-20261006.sh <settet>` | Det frosne settet gjennom fasaden, én gang | Skriptet skriver tallene og stopper ikke selv. Jeg leser sluttlinjen: en merking ut, eller et publisert svar uten linje om allergener, stopper meg |
| 6 | `HD/mac/deploy-commit-20261003.sh`, så testmengden på det committede treet, så `HD/mac/deploy-push-20261003.sh` | Commit av filene i fillisten, push, CI | Commiten har andre filer enn listen; CI er rød to ganger |
| 6b | `HD/mac/strakstiltak-commit-push-readme-20261006.sh` | Lagt til 6. oktober etter feilen i `README.md` (se «README-feilen» sist i planen): egen commit med bare `README.md`, hele testmengden, push, CI. Kjøres etter målingen på nett | `README.md` i `a3fc5042` er ikke grunnlaget; forskjellen mot den er ikke bare tillegg; treet er ikke rent; CI er rød |
| 7 | `HD/mac/strakstiltak-les-foer-utsetting-20261006.sh` | Claimene, loggen til utgaven som står, og forutsetningene for veien tilbake. Endrer ingenting på verten; skriver to logger under `HD/evidence/` | Skriptet skriver det det leser og stopper ikke selv |
| 8 | `HD/mac/strakstiltak-utsett-20261006.sh <commit>` | Kjører trinn 7 på nytt, og stopper før noe er claimet eller rørt hvis det står en claim i `hd`, hvilken som helst, hvis utgaven som kjører, ikke er `a3fc5042`, eller hvis imaget for den verken ligger på verten eller finnes i GHCR. Ellers kjører det `HD/mac/deploy-vert-20261003.sh <commit>`, uendret, med egen claim. Raden i `_losen-queue/KOORDINERING.md` oppdateres før jobben legges i køen | Se «Stoppregler». Etter byttet gjør skriptet ingenting av seg selv |
| 9 | `HD/mac/strakstiltak-maal-nett-20261006.sh <liste>` | De 174 kallene, med grunnkode og advarsler for hvert svar | En merking; et publisert svar uten linjen |
| – | `HD/mac/strakstiltak-kjede-20261006.sh rydd` | Legger treet tilbake til `a3fc5042` hvis noe stopper før commit | – |

Utsettingens egen kontroll (`HD/mac/KJOR-4-test-utenfra.sh` og `HD/mac/maal-demoflater-20260930.sh`) stiller to spørsmål: «Hvilke pizzaer har dere?» og «Hva har dere som ikke er pizza?». Ingen av dem har et ord fra listen, og kontrollen krever ingenting om advarslene (lest i skriptene, linje 24–34 og 146–187). Tiltaket skal altså ikke gjøre den rød.

## Veien tilbake

Skriptet er `HD/mac/tilbake-vert-20261006.sh`. Det brukes bare på Kjetils ord.

```
 Utsettingsskriptet (HD/mac/deploy-vert-20261003.sh)      Veien tilbake (HD/mac/tilbake-vert-20261006.sh)
 ────────────────────────────────────────────────────     ───────────────────────────────────────────────
 claim                                                    claim (stopper bare for en annens claim på containeren)
 GHCR: henter imaget (root)                               henter bare hvis imaget ikke ligger på verten
 LESER SIDEN OVER HTTPS, stopper hvis ikke 200  ◄── her   (leser ikke siden)
 KJOR-2: PALAZZO_IMAGE i /opt/palazzo/.env (ops)          KJOR-2: samme steg, med imaget for a3fc5042
 KJOR-5: demoflatene og modellen (ops)                    (ikke med; verdiene står i /opt/palazzo/.env fra før)
 KJOR-3: docker compose up, venter på /health/ready       KJOR-3: samme steg
 kontroll utenfra                                         kontroll utenfra
 COMMITTED_VERIFIED, claimen slippes                      ROLLED_BACK_VERIFIED, claimen slippes
```

Hvorfor det gamle skriptet ikke virker når siden er nede: linje 80–85 leser `https://palazzo.digipomps.org/health/build` før byttet og stopper når svaret ikke er 200. Hvorfor det nye gjør det: de to stegene som bytter utgave (`HD/host/KJOR-2-ops-secrets-og-env.sh` og `HD/host/KJOR-3-ops-start-og-helse.sh`), kjøres som brukeren ops over ssh og leser ikke siden. De er de samme stegene, med samme argument, som hver utsetting har kjørt, sist 4. oktober kl. 19:45 med nettopp dette imaget.

| | Hva | Kilde |
|---|---|---|
| Lest på verten kl. 11:00 | Imaget for `a3fc5042` ligger lokalt på verten, og finnes i GHCR. Imaget for forrige utgave (`771f991e`) ligger der også. Tre eldre image som har kjørt på verten 2. og 3. oktober (`876e835e`, `311ba729`, `39d0657c`), ligger der ikke lenger: noe rydder bort image, og hva og når er ikke lest. Imaget for `a3fc5042` kan altså bli borte etter byttet. Da går veien tilbake gjennom GHCR som root, som krever nett fra verten, vertens token og 40 GiB ledig disk; kl. 11:00 var 49,0 GiB ledig. Ingen claim sto | `HD/maal/STRAKSTILTAK-LEST-FOER-1-20261006.md`; `HD/evidence/KJOR-3-ops-start-og-helse-20261003T153510Z.log` og de to eldre loggene samme sted |
| Tørrkjørt kl. 11:02, og på nytt kl. 12:27 etter rettelsene fra K6 | Skriptet uten `:utfoer`: claim, status, imaget på verten, og listen over stegene. Tørrkjøringen slutter før delen som bytter; den delen er lest (av meg, av K6 og av `bash -n`), ikke kjørt | `HD/maal/STRAKSTILTAK-TILBAKE-TOERR-1-20261006.md`, `HD/maal/STRAKSTILTAK-TILBAKE-TOERR-2-20261006.md` |
| Ikke kjørt | Selve byttet tilbake, og statusen `ROLLED_BACK_VERIFIED` i `hd`. Jeg kjører det ikke som prøve, fordi det endrer verten uten at det er bedt om | – |
| Virker ikke | Når verten selv eller nginx er nede, eller Mac-en ikke når verten over ssh | – |

Statusovergangene og kvitteringen i `hd` stopper ikke byttet: feiler en av dem, står det i utskriften, og byttet fortsetter. Tre ting stopper derimot skriptet før noe på verten er rørt: en annen oppgave eier en claim på samme container; skriptets egen claim lar seg ikke føre; eller Mac-en har ingen Python som `hd` kan kjøre med. Når ikke Mac-en verten over ssh etter tre forsøk, stopper det også, uten å ha rørt noe.

Feiler veien tilbake selv etter at claimen er tatt (`KJOR-2` eller `KJOR-3` feiler, eller kontrollen utenfra er rød etter byttet), blir claimen stående, og statusen settes til `HANDOFF_REQUIRED` hvis det lar seg gjøre. Da står det en claim på verten til den slippes, og stoppregelen «enhver claim» gjelder neste utsetting.

Stopper utsettingsskriptet selv før byttet, står siden som i dag, men `/opt/palazzo/.env` kan alt peke på den nye utgaven, og skriptets claim står. Da sier jeg fra og rører ikke mer, som det står i spesifikasjonen.

## Stoppregler

Ordrett fra den godkjente spesifikasjonen, «Det som stopper meg».

Før utsettingen stopper fem ting. Da står alt stille til Kjetil svarer, ingenting er satt ut, og siden står som i dag:

- Hele testmengden er rød før jeg har endret noe.
- En eksisterende test blir rød eller må endres.
- Angrepet finner en merking på gjestens side, eller et publisert svar uten en linje om allergener.
- CI (byggingen og testingen hos GitHub) er rød to ganger på samme commit.
- Det står en claim på verten, altså et merke om at noen arbeider der. Skriptet stopper bare for en claim på samme container, så jeg leser claimene selv rett før utsettingen og stopper for enhver.

Under og etter utsettingen kan tre ting skje. Jeg ruller ikke tilbake uten Kjetils ord, og jeg sier fra med én gang hva jeg ser:

- Den nye utgaven blir ikke frisk i selve byttet. Da kan siden være nede til det er rettet.
- Utsettingens egen kontroll er rød etter byttet, også når grunnen er et kall som aldri kom fram. Da står den nye utgaven på nett. Kontrollen kjøres ikke om igjen uten Kjetils ord.
- Målingen på nett viser en merking, eller et publisert svar uten en linje om allergener. Da står den nye utgaven på nett.

Fantes det ingen vei tilbake som virker når siden er nede, skulle jeg stoppet før utsettingen og spurt. Den finnes, med forbeholdene over.

## Dataflyt {#dataflow}

Hele tegningen står i `PDD/dataflow.md`. Kantene som endres:

| Kant | Fra → til | Kontrakt | Endres? |
|---|---|---|---|
| 1 | Gjest → `POST /palazzo/api/ask` | `haven.palazzo.communale.guest-concierge.v1` | nei |
| 1b | Spørsmålet → ordlisten → henvisningen | `PalazzoAllergiHenvisning.treffer` | NY (WP2) |
| 2 | Fasaden → oppslaget | `PalazzoCellAccess.set` | nei; kalles ikke når listen treffer |
| 3 | Oppslagets svar → publiseringen | `PalazzoCommunaleProjection.project` | ja (WP3, WP4) |
| 4 | Publisert svar → modellen og vakten | `PalazzoConciergePhrasing.rephrasedWithOutcome` | nei; kalles ikke for henvisningen |
| 5 | Utfallet → containerens logg | én linje, uten spørsmål og nøkkel | to nye utfall (WP7) |
| 6 | Svaret → gjest | samme 13 felt; ny verdi `reason_code: allergy-referral`; ny linje i `warnings` | ja (`PDD/contract/README.md`) |

## Tiden

Planen var ferdig kl. 11:05, 23 minutter etter at svarene ble lest (kl. 10:42). Anslaget fra spesifikasjonen står: målt på nett rundt kl. 16:00, hvis ingenting stopper. Sprekker det, sier jeg fra før den tid.

## Etter kontrollen K6 {#k6}

En uavhengig tråd (K6) leste koden, testene, veien tilbake, kjeden og denne planen kl. 11:38–12:17, etter at endringen var grønn og før noe var committet. Rapporten: `HD/maal/grunnlag-20261006/kontroll/K6-KODE.md`. 19 funn: 1 feil, 4 utelatt, 13 upresist, 1 ukontrollert. Ingen av dem gjaldt at koden gjør noe annet enn S1–S5 sier. K6 fant ingen vei for en merking ut på gjestens side og ikke noe publisert svar uten linjen, og holdt Swift-listen mot referansen oppføring for oppføring.

| Funn | Hva som er gjort |
|---|---|
| Feilen: planen sa at gamle image ikke ryddes bort på verten. Tre image fra 2. og 3. oktober er borte | Rettet under «Veien tilbake». Utsettingsskriptet leser rett før byttet at imaget ligger på verten eller finnes i GHCR |
| Regel 1 gir henvisningen også når grunnlaget ikke er lastet (før 503) eller tilgangen er avvist (før 403). Ikke i spesifikasjonen, ikke prøvd | Koden står, fordi S1 sier at oppslaget ikke spørres. Ført under «Fire ting», og legges fram ved G3 |
| XCTest førte ikke alle meldingene; årsaken er ikke funnet | Testene kaster tallet selv. Kommentarene i testfilene sier nå det som er målt, ikke en årsak. Henvisningens felter og antall kilder er med i det som kastes |
| «Også når modellen har formulert svaret» var bare prøvd for pizzalisten | Testen prøver nå også en rettbeskrivelse («Fortell om Vitello tonnato.»). Bare de to svarformene kan formuleres av modellen |
| Ni eksempelord prøvde ikke sin egen oppføring | Åtte er byttet til ord bare oppføringen fanger. Den niende, «krysskontamin», har ikke noe slikt ord: alt den fanger, fanger «kontamin» også |
| Veien tilbake: et ssh-glipp ble lest som «imaget mangler»; skriptet lot status og claim stå uten å si det | Skriptet prøver ssh tre ganger, og setter `HANDOFF_REQUIRED` når det avbryter etter at claimen er tatt. Tørrkjørt på nytt |
| Planens filliste manglet to filer; «stopper når» for to trinn var noe jeg gjør, ikke skriptene | Rettet i tabellene over. Utsettingen har fått et eget skript som stopper for enhver claim |
| Trinnet `foer` krevde ikke urørt kode | Kravet er lagt inn. I kjøringen kl. 11:17 var koden urørt (md5 i målingen) |
| De fire nettestene er kjørt etter endringen, ikke før, på Mac-en | «Før» er CI for `a3fc5042` 4. oktober, der de samme testene kjøres. De leser ikke teksten som er byttet |
| Småting: sitatet av valget, hva som manglet i `.git`, hva sidens skript leser, «kun lesing» | Rettet her, i `contract/README.md`, `dataflow.md` og `handoff/README.md` |

De røde kjøringene: fire i alt, alle med nettopp de fem ventede testene røde og de 265 gamle grønne. Testfilen ble rettet mellom dem (tellingen, så det som kastes, så funnene fra K6). Den siste, kl. 12:21, er kjørt med testfilen slik den committes: `HD/maal/STRAKSTILTAK-KJEDE-ROED-4-20261006.md`. De grønne: kl. 11:35 (279 tester, 0 feil), kl. 12:22 etter rettelsene i testene (279 tester, 0 feil), og kl. 12:29 med angrepet lagt til som test (280 tester, 0 feil), alle med de samme fem kildefilene (md5 i hver).

Angrepet ble målt én gang kl. 12:24–12:27, mellom den andre og den tredje grønne kjøringen: 180 spørsmål fra en tråd som ikke hadde sett listen, koden eller det første settet, frosset med md5 før måling (`HD/maal/grunnlag-20261006/blind-2/FROSSET.md`). Ingen merking og ikke noe publisert svar uten linjen. Listen fanget 50 av 60 om allergi og trygg mat, 6 av 20 som var skrevet for å unngå de vanlige ordene, og ga 3 av 60 vanlige spørsmål henvisningen (`HD/maal/STRAKSTILTAK-ANGREP-BLIND2-20261006.md`).

## README-feilen i `c5058f49` {#readme}

Lagt til 6. oktober kl. 13:34 UTC. Dette sto ikke i planen Kjetil ga G2 for. Det er en feil jeg gjorde i trinn 6, og det jeg gjorde med den.

**Hva som gikk galt.** Commiten `c5058f49` har koden, testene og siden slik de ble kontrollert og angrepet. `README.md` i den er feil. Filen jeg la i pakken, var bygget på en kopi i skyarbeidsområdet som var `README.md` slik den sto i `311ba729` (runde 2, før runde 2b). Jeg holdt aldri kopien mot filen i `a3fc5042`. Teksten fra de tre commitene etter `311ba729` falt bort: at vakten skriver teksten selv, den lukkede listen med spørsmål, og fire av de fem kjente grensene. Kontrollen K6 fant det ikke, fordi jeg viste den til samme kopi. De tre andre endrede filene var bygget på riktig grunnlag (lest fra git-objektene, og funnet på nytt av K7).

**Hva jeg gjorde.**

| | Hva | Hvor |
|---|---|---|
| Stoppet | La bremsefilen kl. 12:32:22 UTC. Den kom 13 sekunder for sent til å stoppe pushen | `HD/mac/STOPP-KJEDEN.brukt-20261006T123222Z` |
| Fant omfanget | Leste git-objektene uten å kjøre git: bare `README.md` er feil | `PDD/STATUS.md`, loggen kl. 12:32 |
| Rettet | `README.md` fra `a3fc5042` med strakstiltaket som rene tillegg: 71 linjer inn, ingen ut | `HD/strakstiltak-20261006/steg4/README.md` |
| Kontrollert | En uavhengig tråd (K7) fant selv hva filen var i `a3fc5042`, og holdt tilleggene mot koden: 0 feil, 11 upresise steder. Alle elleve er rettet (ti linjer til i `README.md`, meldingen og skriptet); rettelsene leses av kontrollen før G3 | `HD/maal/grunnlag-20261006/kontroll/K7-README.md` |
| Committes | Egen commit med bare `README.md`, hele testmengden, push og CI (trinn 6b), etter målingen på nett | `HD/mac/strakstiltak-commit-push-readme-20261006.sh` |

**Valget jeg tok, og hva det koster.** Jeg satte ut `c5058f49` kl. 13:19 UTC uten å vente på rettelsen. Først hadde jeg tenkt å vente (det står i `PDD/STATUS.md` kl. 12:44). Jeg byttet da kontrollen K7 tok lengre tid enn ventet, og ventingen ville skjøvet målingen forbi tiden Kjetil har fått. Det ferdige imaget har ikke `README.md` i seg, så tjenesten er den samme. Det som taper: utgaven på nett er ikke grenens hode etter rettelsen, og `README.md` i den utgaven er feil. Den som vil vite hva utgaven på nett gjør, skal lese `README.md` på grenens hode, ikke i `c5058f49`.

**Hva som hindrer det neste gang.** Før en fil i en pakke redigeres, holdes grunnlaget mot filen i commiten det skal bygges på (blob-id eller md5), og kontrolltråden får commiten å holde mot, ikke en kopi. Føres i læringsfangsten.
