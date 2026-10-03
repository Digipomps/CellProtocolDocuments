Dette er en rekonstruksjon 29.09.2026 til Kjetils godkjenning som G1-delta; G1/G2 ble gitt 21.09 på en tom §3, og dette dokumentet endrer verken den historien, spesifikasjonen eller noen port.

# Forslag til §3 — palazzo-signalgraf

Dokumentet skiller mellom hva som ble bestilt før arbeidet, hva som ble bestilt underveis, og hva leveransebevisene faktisk viser. «Levert» nedenfor er en kildebasert vurdering av den navngitte leveransen, ikke Kjetils godkjenning. Alle `Godkjent`-felt er `nei`. Ingen bygg, tester, deploy, commit eller push er utført i denne rekonstruksjonen.

## 1. Kildene og tidsgrensen

Stier skrevet som kode er relative til HAVEN-roten; klikkbare fillenker er relative til dette dokumentet. Linjenumre viser filene lest 29.09.2026, med særskilt nummerering for det historiske handoffet H0.

| ID | Kilde | Hva som er gjenfunnet, og tidsgrunnlag |
|---|---|---|
| F | [FORMAALSSPEC.md](FORMAALSSPEC.md), §0, linje 8–10 | Intensjonen ordrett. §1 har bare kandidat-ID med tom tittel, forelder, Goal og verifier, linje 18–20; §3 har én tom rad, linje 35–41. Begge tomrom er også bevart i natt1-loggen, ikke bare i dagens fil. |
| H0 | [Handoff_Codex_Signalgraf_og_Deploy_2026-09-21.md](../../../PalazzoScaffold/docs/Handoff_Codex_Signalgraf_og_Deploy_2026-09-21.md), **opprinnelig 133-linjers versjon** | Hele teksten er gjenfunnet i første lesing i Codex-økt `01a0c5ee-14b7-7470-8d1e-549b33d4403b`, JSONL-linje 22, verktøyresultat datert **21.09 kl. 21:45:38.705 UTC**. Dette er før S0-commiten kl. 21:46:07 UTC og før grafendringene. Ordrett kopi med originale linjenumre står i vedlegg A nedenfor. Linje 1–99 er identiske med dagens handoff. |
| H1 | Samme handoff, dagens 163 linjer | Identisk tekst er gjenfunnet ved innledende lesing i natt1b, økt `01a0c610-1239-7e60-ad9a-4ea490992f90`, JSONL-linje 23, **21.09 kl. 22:22:36.199 UTC**, før brorettelsen. Her er S6b og ny §6 kommet til. Første Git-innsjekking av handoffet er først `8afafa67`, 22.09 kl. 01:04:30 norsk tid; filnavnets dato alene beviser derfor ikke opprinnelig innhold. |
| R | [REVISJON_2_MATCHEPLAN_2026-09-17.md](../Formaal_Perspective_Signalmatching_Revisjon_2026-09-11/REVISJON_2_MATCHEPLAN_2026-09-17.md), §9, linje 106–146 | Datert referat av de fem svarene, med utsagn gjengitt som ordrette der de finnes. Linje 108 sier at svarene ble lest fra artefaktets lager 21.09. Valgene er dessuten gjengitt i H0 før arbeidet. Referatet er tilgjengelig; originalens lagrede svar er ikke gjenfunnet. |
| M | Matchebenken, originalt svaruttrekk | **Kilde mangler:** ingen original svarfil, artefakt-ID/URL eller lesbart lagringsuttrekk er gjenfunnet i de undersøkte prosjektfilene. R §9 er referatet, ikke en uavhengig kontroll av originalen. Ingen sitater tilskrives en direkte lesing av M. |
| S | [STATUS.md](STATUS.md), linje 7–10 og 21 | G1/G2 og «plan = handoff», samt natt1/natt2-fordelingen. Dagens 21 linjer samsvarer med teksten bevart i `_losen-queue/logs/natt1-signalgraf-20260921.stderr.log`, linje 9069–9089, fra nattkjøringen 21.–22.09. Ingen senere planbytter er innført i STATUS. |

**Tidsregelen brukt her:** §3-forslaget bygger på H0 og de andre førkildene, ikke på resultatrapporten eller dagens utvidede handoff alene. H1 brukes som bevis på en **senere bestilling før broarbeidet**, ikke som et opprinnelig G1/G2-løfte. Dermed blir S6b verken skrevet bakover inn i §3 eller feilaktig kalt «aldri lovet». Tidspunktet da Kjetil ga det nye bro-ordet kan ikke fastslås sikkert: H1 linje 109 sier «21.09 kl. 22», mens H0 fortsatt har den gamle porten ved 23:45 norsk tid. De tidsstemplede lesingene fastslår versjonsrekkefølgen, ikke tidspunktet for samtalen.

Den tomme kontrakten er historisk dokumentert også i natt1-loggen: linje 8904–8944 gjengir F fra overskrift til den blanke §3-raden. Det er ikke grunnlag for å omtolke G1/G2 til en godkjenning av den rekonstruerte tabellen.

## 2. Hva førkildene faktisk lover

Hvert sitat nedenfor er et utdrag, ikke en ny formulering av løftet. H0 finnes i sin helhet i vedlegg A, slik at også vilkårene rundt utdragene kan kontrolleres.

| Kildeanker | Sitat og linjenummer | Hva det bærer, og grensen for det |
|---|---|---|
| K01 | F linje 10: «Vi skal ha signal matching over alt - vi går altså for det store. Codex skal først få Interest- og Purpose-noder med vekter, og så deploye palazzo scaffoldet (deployes i natt, vises i morgen).» | Noder/vekter og deploy; tidsforventning natt/morgendag. Ingen konkret GUI-referanse eller testbar definisjon av «over alt». H0 linje 28–29 avgrenser Palazzo som første produkt og krever CellProtocols typer. |
| K02 | R linje 112: «**adapter nå**»; H0 linje 46: «`PalazzoOneLayerTagMatcher` fjernes når erstatteren er grønn — én motor.» | Adapter nå og fjerning av gammel matchevei etter verifisert erstatter. Ikke et løfte om bedre treffkvalitet; R linje 142 krever at valget ikke fremstilles som en ytelses- eller kvalitetspåstand. |
| K03 | R linje 113: «**skjuler retten på gjestens egen flate**»; H0 linje 47: «Huset får aldri vite noe.» | Negativ dom får privat virkning. H0 S3 presiserer observerbare data- og eventkrav. |
| K04 | R linje 114, også H0 linje 48: «Når det har blitt et formål skal formålet ha et Goal — da skal den spises.» | Hensikt skiller Interest fra Purpose; Goal gjelder at retten spises. R linje 120 nevner bestilling eller ja til treff. H0 S4 åpner særskilt for et rapportert `nil`-avvik; det opphever ikke at Kjetils ord er sterkere. |
| K05 | R linje 115: «Der avtalene lagres rått kan det være dictionary. Listen med revisjonskjede er referanser til spesifikke avtaler.»; H0 linje 49: «(Berører ikke i natt.)» | Bindende avklaring av form, uttrykkelig utsatt som implementeringsarbeid i denne leveransen. Ingen ny §3-rad for avtalelagring. |
| K06 | R linje 116: tilhørighet som oppfylt formål = «**ja**»; H0 linje 50: «I natt: bare gjør det *mulig* (Purpose med Goal + oppfyllelsesmarkering), ikke bygg måltallet.» | Tilrettelegging gjennom S4 nå. Selve måltallet er utsatt, ikke en manglende nattleveranse. |
| K07 | H0 linje 75: «Commit dem først som egen commit «HD-0077: bro-diagnose og fixtures (arbeidstre 20.09)»»; linje 78–80: «Baseline før / endring: kjør hele suiten og skriv antall og røde til rapporten» (linjeskift markert med `/`). | Bevare 20.09-arbeidet i egen commit og måle faktisk baseline; ≈127/2 røde var en forventning, ikke resultatkrav. |
| K08 | H0 linje 94: «én `EntityRepresentation` per gjest («meg»)»; «Kantene er `Weight<T>`; vekter: skrevet med egne ord 1.0, «Vil smake» 0.8, «Interessant» 0.5, «Ikke for meg» negativ»; «**Postene forblir sannheten**»; «grafen bygges deterministisk fra postene ved lasting og ved hver append». | Privat graf, vekter, deterministisk replay og kantproveniens. Samme linje tillater persistens bare når eksisterende Codable bærer det og krever rapportert avvik mot redigerbar graf. |
| K09 | H0 linje 95: «med `hops` ≥ 2»; «Kandidatmengde = interest + purpose + interaction, `source == "self"`»; «Dom: `positive` / `negative` / `undecided` (budsjett/TTL)»; ««Vil smake» på pistasj + rett tagget pistasj → ett treffkort». | Konkret reaksjon→treff-løfte, tre dommer, to hopp og forklaring fra gjestens provenance med dato. Ikke generell, semantisk fri gjenkjenning av enhver interesse. |
| K10 | H0 linje 96: «`guest.configuration` utelater retter/artikler med negativ dom for **denne** gjesten; ingen post, ingen event, ingen `content.*`-side ser det.»; «en annen gjest ser retten». | Privat filtrering uten sideeffekter av dommen; kilden tillater Palazzo-proveniens som polaritetsmekanisme hvis motoren ikke bærer polaritet. |
| K11 | H0 linje 97: «Ved `approveMatchGrant(.action)` eller bestilling: `Interest` forfremmes til `Purpose` med Goal.»; «la `goal` være `nil`, hold målteksten i Palazzo-tilstand og **skriv det som avvik**»; «finnes det ikke et slikt hendelsespunkt i dag, legg en `entity.purpose.fulfil`-keypath, eierstyrt». | Promotering, Goal og oppfyllelse, med uttrykkelig fallback. «Servert til gjesten» i denne linjen er svakere enn «spist» i K04. |
| K12 | H0 linje 98: «`insight.interests`/`insight.purposes`/`avoid` avledes av grafen (samme svarform som i dag — kontraktstester må stå).»; «Ny eierstyrt `entity.graph` (get) som returnerer noder, kanter, vekter og provenance for **gjestens egen** graf — det er det Kjetil viser i morgen.» | Projeksjoner og konkret GET-flate for demonstrasjon. Kilden angir ikke en graftegning, et skjermbilde eller en godkjent klientreise. |
| K13 | H0 linje 98: «`validateAccess` på alle nye keypaths; negative tester (feil requester, feil keypath).»; linje 119–120: «ingen no-op-stubber; Explore-audit for appen / grønn» og «ingen `print` av gjestedata» (linjeskift markert med `/`). | Tilgangskontroll og kontrollbevis. H0 linje 52 forbyr språkmodell, personnode i fellesregister og at treff gir rettighet. |
| K14 | H0 linje 99: «`docs/Remember_contract_2026-09-07.md` oppdateres (Last verified against code), ny `docs/Signalgraf_2026-09-21.md` (hva som er noder, vekter, provenance, hva som er avledet vs. redigert, avvik).» | To navngitte kontraktdokumenter. |
| K15 | H0 linje 124–129: «`docs/Rapport_Signalgraf_2026-09-21.md`: rå utdata før/etter» og «`TESTRESULT.md` i / `CellProtocolDocuments/Deliverables/PDD_palazzo-signalgraf_2026-09-21/` med ankre `#build #regression / #graf #match #negativ #hensikt #projeksjon #auth`» (linjeskift markert med `/`). | Rapport med typer/revisjon, lagring, polaritet, Goal-avvik, filliste og eventuell push-SHA; TESTRESULT på avtalt sted med åtte ankre. |
| K16 | H0 linje 100: «**Commit + push** på `pdd/palazzo-2026-09-14`» og «Push utløser CI som bygger imaget.»; linje 117: «fila sier **`stopp`** eller finnes ikke → **ikke push**; fullfør S0–S6, rapporter, og stopp». | Betinget S7, ikke et ubetinget natt1-løfte om push. H0 hadde en svarfil-port; H1 erstattet den senere med brorettelse og grønn suite uten skip. |
| K17 | H0 linje 101: «Deploy til `palazzo.digipomps.org`»; «**Ikke din** — kjøres av skript-jobben `natt2` etter deg (HD-0077 KJOR-0…4). Du skal ikke røre verten.» | Deploy hører til samlet intensjon, men utfører/eier er natt2, ikke grafjobben. |
| K18 | S linje 9: «plan = handoff»; linje 21: «Køjobber natt1 (Codex, graf) og natt2 (skript, deploy HD-0077).» | Kobler den godkjente planen til handoffet og bekrefter ansvarsdelingen. S gir ingen ekstra konkrete produktleveranser. |

**Utsatt, ikke bortforklart:** H0 linje 103–104 setter taksonomiforsoning, `PurposeRegistry`, tillitspakke som `proofs`, tilhørighetsmåltall, Porthole-fjernlasting og CellProtocol #35 utenfor nattens arbeid. Kjetils «over alt» og vektet tilhørighet står som videre intensjon; kildene gir ikke en fullstendig akseptansekontrakt for hele HAVEN. Det blir derfor ingen slike nye leveranser i tabellen. S6b-endringen behandles separat i §5.

## 3. Forventningskontrakt — forslag, ikke vedtatt

`Referanse` peker på forventningen, ikke på et etterkonstruert godkjent resultat. `Hvor` konkretiserer plasseringen kilden angir; navn på nye implementasjonsfiler brukes som bevis først i §4. Samme L-ID brukes rad for rad i målingen.

| Leveranse | Type | Hvor | Referanse | Godkjent | Kilde |
|---|---|---|---|---|---|
| **L01 / S0:** 20.09-arbeidet bevart i egen commit før grafendringene. | fil / Git-commit | `PalazzoScaffold`, `pdd/palazzo-2026-09-14` | H0 §5, navngitte filer og commitmelding | nei | K07, H0:71–76,93 |
| **L02 / S0:** Faktisk full baseline med antall og navngitte feil, samt byggresultat. | testutdata | Rapporten og TESTRESULT; råloggplassering ikke fastsatt i førkilden | H0 §5 og §7 | nei | K07, K15, H0:78–80,124–129 |
| **L03 / S1:** Privat gjestegraf med EntityRepresentation, Interest/Purpose, Weight, 1.0/0.8/0.5/negativ, ordnede autoritative poster, deterministisk rebuild og kantproveniens; betinget cache/persistens rapporteres. | fil | `PalazzoEntity`-cellens tilstand i PalazzoScaffold | H0 S1 | nei | K01, K08, H0:94 |
| **L04 / S2:** Én CellProtocol-basert matcher; egne reaksjoner/interesser/formål/tekst kan gi to-hopps treff, tre dommer og kilde-/datoforklaring; pistasjreaksjon gir ett treffkort; gammel matcher fjernes, tester bevares. | fil / testutdata | `PalazzoSignalGraphMatcher`, PalazzoScaffold | H0 S2; `testSiciliaReactionGivesMatch` | nei | K02, K09, H0:46,95 |
| **L05 / S3:** Negativ dom skjuler retter/artikler bare for riktig gjest, uten nye domsposter eller events eller endring hos huset; annen gjest beholder retten. | fil / testutdata | `guest.configuration` og gjestens innholdsprojeksjon | H0 S3 | nei | K03, K10, H0:47,96 |
| **L06 / S4:** Interest blir Purpose ved hensikt/handling, med Goal for servert/spist rett; eventuell `goal=nil` og manglende bestillingsbane må oppgis som avvik. | fil | Gjesteentitetens handling-grant-/hensiktsbane | R valg 3 og H0 S4; **spist/servert-forskjellen beholdes** | nei | K04, K11, R:114,120; H0:48,97 |
| **L07 / S4:** Oppfyllelse kan markeres ved servering, eller via eierstyrt `entity.purpose.fulfil` når serveringspunkt mangler. | fil / testutdata | Gjesteentiteten | H0 S4; tilrettelegging, ikke tilhørighetsmåltall | nei | K06, K11, H0:50,97 |
| **L08 / S5:** `insight.interests`, `insight.purposes` og `avoid` avledes fra samme graf med bevart svarform. | fil / testutdata | Eksisterende insight-keypaths | H0 S5, eksisterende kontraktstester | nei | K12, H0:98 |
| **L09 / S5:** Eierstyrt GET `entity.graph` med noder, kanter, vekter og provenance, som grunnlag for demonstrasjonen «i morgen». | fil / kjørende flate (GET) | Gjestens egen entitet | H0 S5. Visuell referanse: **kilde mangler; intet godkjent bilde eller klientoppsett er angitt**. | nei | K01, K12, F:10; H0:98 |
| **L10 / S5 og porter:** `validateAccess`, negative requester-/keypath-tester, grønn Explore-audit; ingen no-op-handler, gjestedatalogging, språkmodell eller felles personnode; treff gir ikke rettighet. | fil / testutdata | Nye keypaths og berørte Palazzo-kilder | H0 S5 og §6 | nei | K13, H0:52,98,119–120 |
| **L11 / S6:** Oppdatert Remember-kontrakt og ny Signalgraf-beskrivelse, datert og med mekanismer og avvik. | fil | `PalazzoScaffold/docs/Remember_contract_2026-09-07.md` og `docs/Signalgraf_2026-09-21.md` | H0 S6 | nei | K14, H0:99 |
| **L12 / S6:** Rapport med rå før-/etterresultater, per-slice gjort/avvik, brukte CP-typer og revisjon, lagring, polaritet, Goal, filliste og eventuell push-SHA. | fil / testutdata | `PalazzoScaffold/docs/Rapport_Signalgraf_2026-09-21.md` | H0 §7 | nei | K15, H0:124–129 |
| **L13 / S6:** TESTRESULT på avtalt sted med de åtte navngitte ankrene. | fil / testutdata | Denne PDD-mappens `TESTRESULT.md` | H0 §7 | nei | K15, H0:127–129 |
| **L14 / S7:** Betinget signalgraf-commit og push på oppgitt gren, med bestilt melding; CI bygger image. | Git-commit / testutdata / image | `PalazzoScaffold`, `pdd/palazzo-2026-09-14`, image-CI | H0 S7 og opprinnelig §6. Senere vilkår/endret utfører dokumenteres separat. | nei | K16, H0:100,108–117 |
| **L15 / S8:** PalazzoScaffold deployet på `palazzo.digipomps.org`, via HD-0077 KJOR-0…4; **natt2 er utfører**. | kjørende flate | `https://palazzo.digipomps.org` | H0 S8, F «deployes i natt, vises i morgen» | nei | K01, K17, K18, H0:101; S:9,21 |

## 4. Måling mot leveransen som kan dokumenteres 29.09

Bevisgrunnlaget er eksisterende kilder og kjøringer, ikke en ny prøve av dagens arbeidstre eller server. Palazzo-kildene `PalazzoSignalGraph.swift`, `PalazzoSignalGraphMatcher.swift`, `PalazzoEntityCell.swift`, `PalazzoSignalGraphTests.swift` og `PalazzoBridgeheadTests.swift` er kontrollert mot implementasjonscommiten `8afafa67` og har ingen senere diff i disse filene. Arbeidstreet som helhet har andre, ucommittede endringer; 145-testresultatet sertifiserer derfor ikke hele arbeidstreet 29.09. Workflowet har senere Node/UI-tillegg, men samme CP-pin på linje 46.

Bevisforkortelser:

- **T** = [TESTRESULT.md](TESTRESULT.md); natt1-resultatene står først, sluttstatus i linje 166–194.
- **E0** = [signalgraf-evidence](../../../PalazzoScaffold/docs/signalgraf-evidence/), natt1.
- **E1** = [bro-evidence](../../../PalazzoScaffold/docs/bro-evidence/), natt1b; **E1-test** = [final-test.txt](../../../PalazzoScaffold/docs/bro-evidence/final-test.txt).
- **TS** = [PalazzoSignalGraphTests.swift](../../../PalazzoScaffold/Tests/AppTests/PalazzoSignalGraphTests.swift).
- **G** = [PalazzoSignalGraph.swift](../../../PalazzoScaffold/Sources/App/Models/PalazzoSignalGraph.swift); **Mch** = [PalazzoSignalGraphMatcher.swift](../../../PalazzoScaffold/Sources/App/Models/PalazzoSignalGraphMatcher.swift); **C** = [PalazzoEntityCell.swift](../../../PalazzoScaffold/Sources/App/Cells/PalazzoEntityCell.swift).
- **RS** = [Rapport_Signalgraf_2026-09-21.md](../../../PalazzoScaffold/docs/Rapport_Signalgraf_2026-09-21.md); **RB** = [Rapport_Bro_2026-09-21.md](../../../PalazzoScaffold/docs/Rapport_Bro_2026-09-21.md).

| Rad | Status | Faktisk leveranse og bevis | Begrensning / udekket del |
|---|---|---|---|
| L01 | **levert** | Git-objekt `516e2d2ee6e446d08174a9d642f5eea12cdd051d`, 21.09 kl. 23:46:07 norsk tid, har nøyaktig S0-meldingen og de fem navngitte 20.09-filene samt fire skeleton-fixturefiler. T:6 og RS:91 bekrefter. | Dette er bevaring av tidligere arbeid, **ikke signalgrafens implementasjonscommit**. Senere bro-/workflowendringer til samme filer må vurderes som senere arbeid. |
| L02 | **levert** | E0 `baseline-build.txt` og `baseline-test.txt`; sistnevnte linje 1213–1215: **127 tester, 8 feilregistreringer**, tre røde tester. T:44–55 navngir to brotester og G5 med Intel-Python-feil. | «≈127 med 2 røde» i H0 var en forventning. Faktisk baseline skal ikke pyntes til 2 røde tester. |
| L03 | **levert** | G:37–116 bygger de lovede nodene, vektene, source-filteret og kantene; C:67,90,404 viser lasting/cache/append-rebuild. TS:14–36 kontrollerer vekter, provenance og replay; TS:513ff. cache-roundtrip. E1-test:1229,1290 er grønne. | Grafen er avledet fra poster; cachen er ikke sannhet. Dette er den eksplisitte S1-løsningen med rapportert avvik fra Book 37, ikke levering av en redigerbar autoritativ graf. Se RS:133–140. |
| L04 | **levert** | Mch:35–67 bruker `Signal`/`WeightedGraphRuntime` og tre dommer; Mch:72–94 gir kilde-/datoforklaring. TS:39–101 tester to hopp, budsjett og HTTP-reaksjon→ett pistasjkort. E1-test:1231,1233,1342 grønne. Git-diff `516e2d2e..8afafa67` fjerner gammel matcher fra `PalazzoMatchModels.swift` og omskriver eksisterende tester. | Beviser den spesifiserte lokale taggbanen. Ingen dokumentert generell kvalitetsgevinst eller utrulling «over alt». Tillegg som undertrykker gjentatte forslag er skilt ut i §6. |
| L05 | **levert** | C:883–901 filtrerer gjestens publiserte innhold. TS:104–164 har to gjester, faktiske data-/HTTP-kall, feedkontroller og uendrede poster/events/signaler; E1-test:1254 grønn. Taggløse artikler, omtagging og gamle grants dekkes også, jf. RB:101–104. | Tester av konfigurasjonsbindinger og dataflyt er ikke skjermbilder av en faktisk klient. «Ingen event» gjelder selve dommen/lesingen; eksplisitt reaksjon er fortsatt en privat post/event, TS:127–135. |
| L06 | **delvis** | C:323–334,1031,1082 promoterer ved action-grant. TS:167–196 bevarer Interest til handling, ingen promotering ved bare innsyn og én Purpose. E1-test:1166 grønn. | **Goal er ikke levert som Goal-objekt:** TS:195 krever uttrykkelig `nil`; G:183–189 returnerer `goal:null`. Målteksten er «Retten er servert til gjesten» (G:41), ikke bevis for «spist». Ingen gjesteknyttet bestillingsbane er levert, jf. RS:149–154 og T:125–127. H0 tillot fallback, men den sterkere Kjetil-formuleringen er fortsatt udekket. |
| L07 | **levert** | C:295–319 har eierstyrt, idempotent `entity.purpose.fulfil` og private oppfyllelsesposter. TS:197–222 viser oppfyllelse og disklasting; TS:300–314 avviser ukjent Purpose/Interest/tom verdi. E1-test:1166,1195 grønne. | Levert **som den bestilte fallbacken**. Det er gjestens attestasjon, ikke automatisk serveringshendelse eller uavhengig bevis for at retten er spist. Tilhørighetsmåltallet er uttrykkelig utsatt. |
| L08 | **levert** | C:1549–1552 bruker grafens projeksjoner. TS:229–257 kontrollerer de eksakte svarnøklene og graf etter disklasting; E1-test:1209 grønn. T:129–145 angir også eksisterende Sicilia-kontrakter og GUI-kontrakttester. | «GUI-kontrakttest» betyr her Swift-konfigurasjon, ikke visuell klientverifikasjon. |
| L09 | **delvis** | GET er implementert i C:147–161; G:172–200 returnerer noder, kanter og provenance. TS:229–257 og E1-test:1209 beviser eierlesing og diskreplay. Ny brotest er grønn, E1-test:87. | API-/testdelen er levert. Ingen førkilde angir bilde/klientoppsett, og ingen faktisk demonstrasjon av **gjestens private graf i en klient** er dokumentert. T:144–145 sier uttrykkelig at visuell Porthole/Binding-kjøring ikke er utført. Den lovede «viser i morgen»-delen er ikke funnet bevist. |
| L10 | **levert** | C:159–160,310–314 kaller `validateAccess`, krever eier og utfører reell handling. TS:261–314 har feil requester/keypath/payload; E1-test:1195,1218,1227 grønne. E1 `explore-audit.json`:9–12 viser **103 komplette kontrakter, 0 feil, 0 advarsler**. G og Mch bruker lokale noder/motor; RB:108–113 rapporterer ingen nye skip, gjestedatalogging eller modellkjede. | Dette er bevis for berørte nye baner og kontrollert kode, ikke en generell sikkerhetssertifisering av alle HAVEN-tjenester. |
| L11 | **delvis** | Begge filer finnes, er endret i `8afafa67` og har `Last verified against code: 2026-09-22`. Signalgraf-dokumentet beskriver vekter, motor, polaritet, lagring og Goal-avvik; Remember:104–116 beskriver nye kontrakter. | Remember-kontraktens linje **3 og 70** oppgir fortsatt CP `b5b7282…`, mens sluttprøven og workflowet bruker `0f688b57…`. Dokumentet er levert, men revisjonshenvisningen er ikke à jour med sluttleveransen. Ingen dokumentrettelse gjøres her. |
| L12 | **levert** | RS har baseline, per-slice-tabell, CP-typer/filstier/revisjon, mekanismer, avvik og filliste (linje 16–195). Datert tillegg linje 198–226 peker til RB med brorettelse, endelig SHA og push. | Historiske «ingen push»/kopieringsblokkeringer er beholdt med merket senere tillegg; de beskriver natt1, ikke slutten av natt1b. `slice-state.md` i E0 er også en historisk natt1-status. |
| L13 | **levert** | T finnes nå på avtalt sted med alle åtte ankre (linje 13,36,73,88,103,118,129,147) og datert sluttstatus. Bytes er identiske med E0-kopien av TESTRESULT. Sluttens **145/0** er bekreftet i E1-test:1482–1484. | E0 `final-test.txt`:1416–1418 har **142/2**, ikke 145/0. De to kjøringene må ikke blandes. De opprinnelige blankettestene i F §5 er ikke dermed alle avstemt; tabellen her rekonstruerer bare de tillatte førkildene. |
| L14 | **levert** | `8afafa67be40326e0ac3997d5d785165dd5b4de7` har den bestilte signalgrafmeldingen; dokumentasjonscommit `2c4d8fea340ed72121a3bc1644dd30d9b52b3308` følger. RB:233–238 oppgir push. HD-0077 `GHCR-DEPLOY-VERIFIED-20260922.log`:5–14 bekrefter remote/CI på **2c4d8fea**, grønn imagekjøring **35665895552** og publisert image. | Natt1 stoppet korrekt ved sin opprinnelige svarfil-port; natt1b fullførte etter senere bestilling. Resultatet oppfyller også den senere strengere porten, men det er ikke bevis på at den sto i opprinnelig G2. |
| L15 | **levert** | HD-0077 [GHCR-DEPLOY-VERIFIED-20260922.log](../../../HAVEN-Deploy/_handoff/HD-0077/evidence/GHCR-DEPLOY-VERIFIED-20260922.log):28–74 viser nøyaktig image, frisk container, KJOR-3/4 og fullføring **22.09 kl. 06:21:27 UTC / 08:21:27 norsk tid**. [UTENFRA-20260922T062126Z.md](../../../HAVEN-Deploy/_handoff/HD-0077/evidence/UTENFRA-20260922T062126Z.md):3–21 har 11 grønne kontroller, servert app **2c4d8fea…** og CP **0f688b57…**. | Levert av deploykjeden etter natt2s første mislykkede forsøk, ikke av natt1/natt1b. Tidsløftet «i natt» har ingen klokkeslettfrist; fullføringsbeviset er fra neste morgen. Om dette var tidsnok til visningen kan ikke avgjøres fra kildene. Offentlige endepunkter og auth-avslag beviser ikke personlig signalgraf-/gjestereise eller at Kjetil fikk vist den. Ingen påstand om nåværende servertilstand 29.09. |

### Revisjonskjeden og hva 145 tester dekker

1. `516e2d2e` bevarer eldre bro-/CI-arbeid; grafen kom etterpå.
2. Natt1: CP-pin `b5b7282…`; 127/8 før, 142/2 etter. Ingen push. E0 er råbeviset for dette, også når en fil heter `final-test.txt`.
3. Natt1b: CellProtocol [PR #43](https://github.com/Digipomps/CellProtocol/pull/43), kandidat `3edc9165…`, squash-merge **`0f688b57e6e976482c2c045bed2cf13040a2fad2`**. PR-ens merge-status/SHA er kontrollert mot GitHub 29.09 og lokalt Git-objekt; arkivert kvittering står i E1 `cellprotocol-merge.json`:1. Merge kl. 23:01:10 UTC 21.09 = 01:01:10 norsk tid 22.09.
4. [.github/workflows/palazzo-image.yml](../../../PalazzoScaffold/.github/workflows/palazzo-image.yml):46 har `CELLPROTOCOL_REF_DEFAULT` lik denne mergede SHA-en. Pinendringen finnes i `8afafa67`; E1 `provenance.json`:2–17 knytter gammel pin, ny pin, base og implementasjonscommit sammen.
5. E1-test viser **145 tester, 0 feil, 0 skip** lokalt for Palazzo. HD-0077 [CI-LINUX-20260922.md](../../../HAVEN-Deploy/_handoff/HD-0077/evidence/CI-LINUX-20260922.md):3–17 binder også Linux-resultatet 145/0 til `2c4d8fea`, samme CP-pin og rålogg. CellProtocols egne CI-resultater er en annen suite: 1193 tester, 0 feil, **1 eksisterende skip**, RB:149–157; den lokale hele CP-suiten hadde Keychain-feil og 8 skip, RB:194–205. Disse tallene er ikke slått sammen eller omtalt som en helt grønn lokal CP-suite.
6. Det grønne imaget ble deretter deployet av HD-0077-kjeden. Første natt2 stoppet på urent tre (`_losen-queue/done/natt2-deploy-20260921.svar.md`:1–4); retry stoppet på GHCR `unauthorized` (`natt2-deploy-retry-20260922.svar.md`:15820–15829). Disse er faktiske mellomstopp, men ikke siste leveransestatus. Morgenkvitteringen i L15 er senere.

## 5. Bestilt underveis: S6b, ikke et opprinnelig løfte

H0 forbød endring av CellProtocol (linje 52) og manglet S6b. H1 linje 100 bestiller derimot: «**Broen rettes** slik at hele suiten er grønn mot revisjonen CI pinner (§6).» H1 linje 109–111 gjengir Kjetils krav om rettelse, push og feilfri deploy; linje 122–129 krever egen CP-gren med funksjons-/formålstester, merge og pinbump hvis feilen ligger der, uten skip eller svekkede tester. H1s tekst ble lest før brorettelsen; `_losen-queue/done/natt1b-bro-fiks-20260921.prompt.md`:1 gjentar bestillingen.

**Status: levert mot tilleggsbestillingen.** RB:12–29 peker på resolverens eierbevis som årsak; PR #43 og lokal commit `0f688b57` inneholder rettelsen samt positive/negative brotester. RB:52–68 beskriver både reell resolver og to BridgeBase-ender. Ny Palazzo-test avviser hus og kopiert gjesteidentitet mot egne data/graf, E1-test:87. Pinbump, 145/0 og push er dokumentert over. Dette er verken et uautorisert «aldri lovet»-tillegg eller et krav som sto i opprinnelig §3.

H1 §9 nevner også WP7-dispatcher og senere jobber (linje 149–163). De var ikke med i H0, og er en separat verktøyjobb, ikke en rekonstruert Palazzo-signalgrafleveranse. Ingen WP7-rad er føyd til §3.

## 6. Levert, men aldri lovet

«Aldri lovet» betyr her: **intet forhåndsløfte funnet i de tillatte kildene**, ikke en påstand om alt som noen gang er sagt. Følgende leverte tillegg blir ikke §3-rader:

| Tillegg | Førkilde for dette særskilte løftet | Leveransebevis / avgrensning |
|---|---|---|
| Positiv artikkelreaksjon undertrykker senere anbefaling av **samme artikkel** som ny oppdagelse. | **Kilde mangler.** H0 S2 lover reaksjon→match og pistasjrett, men fastsetter ikke denne særskilte utelukkingsregelen. | Mch:53–59; Signalgraf-dokumentet:63–67 beskriver den. Levert kodeatferd, ikke funnet som eget førkrav eller separat navngitt test i rapporten. |
| Allerede valgt innhold foreslås ikke på nytt fra den nye Purpose-posten. | **Kilde mangler.** H0 S4 lover promotering/Goal/oppfyllelse, ikke undertrykking av nye anbefalinger etter valg. | Mch:49–50; TS:223–225 har uttrykkelig assertion; E1-test:1166 består. Dette er en ekstra produktregel som Kjetil kan ta stilling til. |
| CellProtocol-livssyklustesten venter nå på faktisk utlasting og krever at levende instans er fjernet. | **Kilde mangler for en egen livssyklusleveranse.** H1 krever grønn suite, men beskriver ikke dette nye konkrete testarbeidet. | `0f688b57`, diff i `Tests/CellBaseTests/CellLifecycleTests.swift` rundt linje 259, legger til venting og assertion uten runtimeendring. RB:70–75 forklarer CI-timingfeilen. Teknisk tilleggsarbeid for å få et pålitelig kontrollresultat; ikke ny Palazzo-produktfunksjon. |

Cachepersistens, polaritet i Palazzo, `entity.purpose.fulfil`, duplikat-ID-/omtaggingsregresjoner og strengere tilgangstester føres **ikke** som nye selvstendige løfter: cache og fallback er uttrykkelig tillatt i H0; de øvrige er implementering/kontroll av lovet provenance, privat negativ dom og tilgang. Swift-crypto-oppdateringen og valg av system-Python er dokumenterte byggtilpasninger (T:33–34,54–55), ikke nye brukerleveranser. UI-/conciergeendringene i senere `c3320b9`/`0b74f90` er et annet arbeid og brukes ikke til å fylle signalgrafens opprinnelige kontrakt.

## 7. Lovet, ikke levert

Listen skiller manglende funksjon fra manglende bevis. En delvis rad over kan ha både levert funksjon og en udekket rest her.

| Udekket rest | Løfte / rad | Hva som mangler, med bevis |
|---|---|---|
| Goal som faktisk uttrykker/representerer oppfyllelse av «da skal den spises». | K04/K11, L06 | `Purpose.goal` er `nil`, også eksplisitt i testen TS:195. Det finnes måltekst om **servert** og eierattestasjon, ikke et levert Goal-objekt eller dokumentert spising. H0 tillater et rapportert avvik; Kjetil må avgjøre om denne fallbacken oppfyller nattens akseptanse eller skal stå som rest. En grønn test som krever `nil` kan ikke brukes som bevis for at Goal-løftet er oppfylt. |
| Hensikt via en gjesteknyttet bestilling og automatisk markering ved servering. | H0:97, L06–L07 | Handlingsgrant fungerer. Bestillings-/serveringskobling finnes ikke ifølge T:125–127 og RS:149–154; eier-keypath er den leverte fallbacken. Det er ingen ekstra mangel ved fallbackimplementasjonen, men den fulle forretningsbanen er ikke levert. |
| Faktisk demonstrasjon av gjestens private graf «i morgen». | F:10, H0:98, L09 | GET-data og testbaner finnes. Klient, visualisering og gjennomført visning er ikke dokumentert; T:144–145 avgrenser eksplisitt. HD-0077 [UI-OG-HAVEN-20260922.md](../../../HAVEN-Deploy/_handoff/HD-0077/evidence/UI-OG-HAVEN-20260922.md):17–21,50–72 skiller senere offentlig UI fra fortsatt uavklart personlig gjeste-/kelnerreise. Fravær av visningsbevis er ikke bevis for at ingen privat visning fant sted. |
| Tidsløftet «deployes i natt, vises i morgen» er ikke bekreftet oppfylt. | F:10, H0:10–12, L15 | Første forsøk og retry stoppet; fullført deploy er dokumentert 22.09 kl. 08:21 norsk tid. Ingen presis klokkefrist eller tidspunkt for den planlagte visningen finnes i disse kildene. Dette er et udekket tids-/visningsbevis, ikke en konklusjon om at deployfunksjonen mangler eller at en bestemt klokkefrist ble brutt. |
| Kontraktdokumentasjon med korrekt slutt-revisjon. | H0:99, L11 | Remember-kontrakten har fortsatt `b5b7282…` i begge «Last verified»-henvisningene, mot sluttpin `0f688b57…`. Dokumentene finnes; dette er en presis rest i kvaliteten på leveransen. |

Avtalepostmigrering, tilhørighetsmåltall, en autoritativ redigerbar entitygraf, taksonomiforsoning, `PurposeRegistry`, `proofs` og Porthole-fjernlasting skal **ikke** listes som brutte løfter for denne natten når H0 uttrykkelig utsetter eller avgrenser dem. De langsiktige intensjonene er fortsatt uavklart; de er ikke erklært oppfylt.

## 8. Kildehull og forhold Kjetil må kunne se før G3

- Matchebenkens originale lagrede svar mangler. R §9 og H0 dokumenterer hva Losen skrev at Kjetil svarte; originalen kan kontrollere om referatet er dekkende.
- Forskjellen mellom Kjetils Goal/spist og handoffets nil/servert-fallback må behandles som en synlig akseptansebeslutning. Den kan ikke fjernes ved å omformulere løftet til akkurat det testen måler.
- Kilden sier ikke hvordan GET-grafen skulle vises. Det finnes ikke grunnlag for å finne på et godkjent bilde eller en klientreise nå. Manglende visningsbevis står åpent.
- F §1 har fortsatt ikke et utfylt formålstre/verifier, og F §5 har generiske rader som ikke er avstemt her. Rekonstruksjon av §3 alene retter ikke hele PDD-prosessen eller dokumenterer at «alle avledede tester» i den opprinnelige malen er oppfylt.
- S har ingen datert planendring for H1/natt1b og ingen leveransestatus etter 21.09. Den beholdes uendret; rekonstruksjonen viser versjonsbyttet i stedet for å skrive det bort.

**Læring for videre behandling av denne PDD-en:** sammenlign alltid H0 med H1 før et utsagn kalles «lovet før arbeid». Handoffets filnavn og første Git-commit gir ikke tilstrekkelig tidsbevis; den bevarte verktøylesingen viste at S6b kom senere. Sammenlign dessuten riktig rålogg med riktig revisjon: E0 `final-test.txt` er 142/2, mens E1 `final-test.txt` er 145/0. Dette skillet skal bevares ved senere G1-delta-/G3-behandling.

## Vedlegg A — opprinnelig handoff H0, ordrett

Kopien nedenfor kommer fra det tidsstemplede verktøyresultatet beskrevet i §1, ikke fra tilbakeføring av dagens fil. Prefikset `H0:nnn` er lagt til for sitering. Etter siste linje i originalen fulgte `git status`-utdata; disse er ikke del av handoffet og er utelatt. Kopien legges inn uten å endre kildefilen.

H0-kopiens SHA-256 (uten linjeprefiks, med avsluttende linjeskift): `2452887d36df8a30cba374a74b37ef866f30e0f2a2b3a569a089c0f52db71762`.

```text
H0:001 # Handoff til Codex — signalgraf i PalazzoScaffold, deretter deploy (2026-09-21)
H0:002
H0:003 Skrevet av Losen (Claude) 21.09 kveld på bestilling fra Kjetil. Stier er relative til HAVEN-roten
H0:004 der ikke annet står. **Alt som står som kodeatferd er lest i kilden**; det jeg ikke har kunnet lese
H0:005 på nytt er merket. Dette dokumentet er både kontekst og bestilling: §1–§4 er det du må vite, §5 er
H0:006 arbeidet, §6 er portene, §7 er rapporten. Slicene er merket **GODKJENT** eller **STOPP**.
H0:007
H0:008 ## 0. Bestillingen, ordrett
H0:009
H0:010 > Vi skal ha signal matching over alt — vi går altså for det store. Codex skal altså først få
H0:011 > `Interest`- og `Purpose`-noder med vekter, og så deploye palazzo scaffoldet. [Deployes i natt,
H0:012 > Kjetil viser det i morgen.]
H0:013
H0:014 ## 1. Formålet — mål alt mot dette
H0:015
H0:016 Palazzo Comunale bruker HAVEN for å gi gjestene **familiefølelse**, dekomponert 05.09 i tre delformål:
H0:017 **F1 tillit** (det gjesten vil holde for seg selv, blir hos gjesten — som mekanisme, ikke løfte),
H0:018 **F2 kjent og sett** (kelneren vet navn, sist besøk, hva gjesten sa), **F3 overrasket** (gjesten får
H0:019 noe hun ikke ba om, som treffer, og som alltid kan forklares med hennes egne ord).
H0:020
H0:021 Kjetils grunn for «det store» (21.09, ordrett): «Matching av formål og interesser er en viktig ting i
H0:022 HAVEN, skal hjelpe oss med å finne hva vi vil ha uten nødvendigvis å vite navnet. Vi skal bruke det
H0:023 som å insentivere positiv adferd ved å ha muligheten publisere at en annen entitet leverte på de
H0:024 formålene den hevdet den ville levere på. Dette kan brukes til både selskaper og personer — og i
H0:025 tillegg prosesser. … Signal matching er en gjennomgående funksjonalitet i hele CellProtocol. Det
H0:026 behøver nødvendigvis ikke å være store matchinger men kommer til å brukes over alt.»
H0:027
H0:028 Så: Palazzo er **første sted** signalgrafen tas i bruk i et produkt. Det skal gjøres slik at det
H0:029 generaliserer — ingen Palazzo-egen matchemodell, CellProtocols typer.
H0:030
H0:031 ## 2. Hva som er gjort før deg (så du ikke gjør det om igjen)
H0:032
H0:033 | Når | Hva | Hvor |
H0:034 |---|---|---|
H0:035 | 05.09 | Vurdering + beslutninger D1–D5: matching kjører i **gjestens** entitet; over grensen går dom + forklaring gjesten har godkjent + tillitspakke; to grants (innsyn, handling) som signert Agreement; Palazzo betaler | `PalazzoComunaleScaffold/docs/Vurdering_Signalmatching_Familietilhorighet_2026-09-05.md` §9 |
H0:036 | 07.09 | «Husk det jeg sa»: husets signaler (`PalazzoContentSignal`), treffkort i gjestens entitet, to grants, tillitspakke, kelnerlinje. 82 tester | `PalazzoScaffold` (`PalazzoMatchModels.swift`, `PalazzoEntityCell.swift`), `docs/Remember_contract_2026-09-07.md` |
H0:037 | 07.–08.09 | Sicilia-artikler: artikler med godkjente tagger, reaksjoner **Vil smake / Interessant / Ikke for meg** som poster, `insight.avoid`, antiformål «aldri at du leste». GUI-fabrikker. Bridgehead-publisering (G7). 105 tester | `PalazzoSiciliaTests.swift`, `PalazzoSiciliaGUITests.swift`, `PalazzoArticleConfigurationFactory.swift` |
H0:038 | 11.09 | Revisjon: `Purpose`/`Interest` **er** allerede `PerspectiveNodeImpl` med `match(signal:)` i CellProtocol; motoren finnes (`Signal`, `WeightedGraphRuntime`, `MatchStrategyPlanner`, `HitCollector`); men ingen produktformål er i grafen, og Palazzo har sin egen signalmodell (R4) | `CellProtocolDocuments/Deliverables/Formaal_Perspective_Signalmatching_Revisjon_2026-09-11/REVISJON.md` |
H0:039 | 16.09 | Entitydata-beslutninger (Book 37 §7, **ikke implementert**): Interest/Purpose/EntityRepresentation er noder i én vektet graf; `EntityRelationInterests`/`purposeRefs` erstattes av grafen; tillit måles som oppfylt formål (vektet); bevis = `proofs` med keypaths | `CellProtocolDocuments/Book/37_EntityData.md`; Astras audit `…/ENTITYDATA_ASTRA_AUDIT_2026-09-16.md` |
H0:040 | 17.09 | Revisjon 2 av matcheplanen. **Funn:** matcheren ser ikke reaksjonene (§4 under) | `…/Formaal_Perspective_Signalmatching_Revisjon_2026-09-11/REVISJON_2_MATCHEPLAN_2026-09-17.md` |
H0:041 | 17.–20.09 | HD-0077 deploy-kjede: `/health/ready`, `/health/build`, Dockerfile, CI `palazzo-image.yml` (push til `pdd/**` publiserer image til GHCR), host-skript for vhost/secrets/container, test fra utsiden. Gren `pdd/palazzo-2026-09-14` @ `93afbd6` | `HAVEN-Deploy/_handoff/HD-0077/README.md` |
H0:042 | 21.09 | Kjetils fem valg i Matchebenken (§3) | `REVISJON_2_MATCHEPLAN_2026-09-17.md` §9 |
H0:043
H0:044 ## 3. Beslutninger som binder deg (Kjetil, 21.09)
H0:045
H0:046 1. **Adapter nå.** Palazzos matching skal gå på CellProtocols `Signal`/`PerspectiveNode`-typer. `PalazzoOneLayerTagMatcher` fjernes når erstatteren er grønn — én motor.
H0:047 2. **Negativ dom skjuler retten på gjestens egen flate.** Huset får aldri vite noe.
H0:048 3. **Interesse → formål ved hensikt.** Ordrett: «Purpose er en interest's *executive branch*. Jeg vil smake — det kan være en interesse — men jeg har som hensikt å gjennomføre det — er et formål. Når det har blitt et formål skal formålet ha et Goal — da skal den spises.» Altså: «Vil smake» = `Interest`. Når gjesten sier ja til et treff (handling-grant) eller bestiller, forfremmes det til `Purpose` med Goal «retten er servert/spist».
H0:049 4. **Avtaleposter:** `signedAgreementEntity.records` er en ordnet liste av *referanser*; selve avtalene kan ligge som dictionary på UUID. (Berører ikke i natt.)
H0:050 5. **Tilhørighet måles som vektet formålsoppfyllelse** i relasjonen gjest↔hus. I natt: bare gjør det *mulig* (Purpose med Goal + oppfyllelsesmarkering), ikke bygg måltallet.
H0:051
H0:052 Stående regler: CellProtocol røres **ikke** i natt (Kjetils regel 18.09: nye kapabiliteter der skal være testet mot funksjon og formål før main). Ingen test fjernes eller svekkes — se §6 for det ene unntaket som krever Kjetils ord. Ingen språkmodell i kjeden. Ingen personnode i noe fellesregister. Et treff er aldri en rettighet.
H0:053
H0:054 ## 4. Funnet du skal lukke først
H0:055
H0:056 `PalazzoOneLayerTagMatcher.match` (`Sources/App/Models/PalazzoMatchModels.swift:93`):
H0:057
H0:058 ```swift
H0:059 let eligible = records.filter { $0.kind == .interaction && $0.source == "self" }
H0:060 ```
H0:061
H0:062 Reaksjonene skrives (`Sources/App/Cells/PalazzoEntityCell.swift:246`) som `wantToTaste → .purpose`,
H0:063 `interesting`/`notForMe → .interest` (sistnevnte med `attributes.polarity = "negative"`), bare kommentar
H0:064 → `.interaction`. Trykker gjesten «Vil smake» på pistasjartikkelen, kan det **aldri** bli et treff.
H0:065 Bare gjester som har *skrevet* noe kan bli overrasket. Spørrebanen (`insight.interests`/`avoid`)
H0:066 virker. `PalazzoMatch.Verdict` har `negative`/`undecided`, men ingen kode produserer dem (grep over
H0:067 `Sources/` = 0). Registrert som HD-0098; adapteren som HD-0099; hensikt-skillet som HD-0116.
H0:068
H0:069 ## 5. Arbeidet — slicer
H0:070
H0:071 Arbeid i `PalazzoScaffold` på grenen `pdd/palazzo-2026-09-14`. Arbeidstreet har **ucommittede**
H0:072 endringer fra 20.09 (`PalazzoBridgehead.swift`, `PalazzoBridgeheadTests.swift`,
H0:073 `PalazzoG5SeedDryRunTests.swift`, `PalazzoSiciliaGUITests.swift`, `.github/workflows/palazzo-image.yml`,
H0:074 og usporet `Tests/AppTests/Fixtures/skeleton/`). De er en annen tråds arbeid mot bro/CI. **Ikke
H0:075 kast dem.** Commit dem først som egen commit «HD-0077: bro-diagnose og fixtures (arbeidstre 20.09)»
H0:076 så treet er rent, og la dem være.
H0:077
H0:078 **Bygg og test:** `swift build --disable-sandbox` / `swift test --disable-sandbox`. Baseline før
H0:079 endring: kjør hele suiten og skriv antall og røde til rapporten (forventet ≈ 127 med 2 røde
H0:080 bridgehead-tester mot CellProtocol main, se §6).
H0:081
H0:082 **CellProtocol-typene du skal bruke** ligger i `CellProtocol/Sources/CellBase/PurposeAndInterest/`:
H0:083 `PerspectiveNodeImpl`, `Interest`, `Purpose`, `EntityRepresentation`, `Weight<T>`, `Signal`
H0:084 (`relationship`, `weight`, `tolerance`, `token`, `ttl`, `hops`, `localVariables`), `HitCollector`,
H0:085 `WeightedGraphRuntime`, `MatchStrategyPlanner`, `PurposeInterestAdjacencyIndex`. **Verifiser navnene
H0:086 mot revisjonen CI pinner** (`CELLPROTOCOL_REF_DEFAULT` i `.github/workflows/palazzo-image.yml`, i dag
H0:087 `b5b7282`) — jeg siterer dem fra revisjonen 11.09 og Astras audit 16.09, ikke fra egen lesing i dag.
H0:088 Merk fra auditen: `EntityRepresentationDataCodec` og `nodeIdentifier`-bevaring i Codable er
H0:089 **ucommittet** i CellProtocol og finnes ikke på main. Bygg derfor ikke på dem.
H0:090
H0:091 | # | Slice | Status |
H0:092 |---|---|---|
H0:093 | S0 | Baseline + commit av 20.09-treet (over) | GODKJENT |
H0:094 | S1 | **Gjestens graf.** I `PalazzoEntity`-cellens tilstand: én `EntityRepresentation` per gjest («meg»), `Interest`-noder for hver godkjent tagg/artikkel gjesten har reagert på eller skrevet om, og `Purpose`-noder ved hensikt (§3.3). Kantene er `Weight<T>`; vekter: skrevet med egne ord 1.0, «Vil smake» 0.8, «Interessant» 0.5, «Ikke for meg» negativ (se S3). **Postene forblir sannheten** (append-only, ordnet, provenance); grafen bygges deterministisk fra postene ved lasting og ved hver append, og persisteres bare hvis CellProtocol-mains Codable gjør det uten den ucommittede kodeken — ellers ikke, og det skrives i rapporten som avvik («grafen er avledet, ikke redigert» er motsatt av Book 37 §5, og rettes når entitydata-beslutningene lander i CellProtocol). Provenance per kant (post-id) holdes i Palazzo-tilstand siden `Weight` ikke bærer metadata. | GODKJENT |
H0:095 | S2 | **Matcheren.** Ny `PalazzoSignalGraphMatcher` som bygger `Signal` fra husets `PalazzoContentSignal` (tagger → node-referanser) og matcher mot gjestens graf med CellProtocols motor (`match(signal:)` / `WeightedGraphRuntime`), med `hops` ≥ 2 så en tagg som ligger én kant unna (artikkel → tagg → rett) gir treff. Kandidatmengde = interest + purpose + interaction, `source == "self"`. Dom: `positive` / `negative` / `undecided` (budsjett/TTL). Forklaring bygges fra provenance: «Fordi du skrev/trykket «…» <dato>». `PalazzoOneLayerTagMatcher` slettes når S2s tester er grønne; testene som brukte den skrives om, ikke fjernes. Akseptanse HD-0098: `testSiciliaReactionGivesMatch` — «Vil smake» på pistasj + rett tagget pistasj → ett treffkort. | GODKJENT |
H0:096 | S3 | **Negativ dom.** «Ikke for meg» gir `negative`. Sjekk om CellProtocols `Signal`/`HitCollector` bærer polaritet; bruk den om den finnes, ellers hold polaritet i Palazzos provenance og avled dommen der — skriv hvilket. Effekt (§3.2): `guest.configuration` utelater retter/artikler med negativ dom for **denne** gjesten; ingen post, ingen event, ingen `content.*`-side ser det. Test: husets event-logg og `content.signals` er uendret etter en negativ dom; gjestens meny mangler retten; en annen gjest ser retten. | GODKJENT |
H0:097 | S4 | **Hensikt → formål.** Ved `approveMatchGrant(.action)` eller bestilling: `Interest` forfremmes til `Purpose` med Goal. `Purpose.goal` er `CellConfiguration?` — lag et minimalt Goal-objekt som uttrykker «servert til gjesten» hvis det er billig; er det ikke billig i natt, la `goal` være `nil`, hold målteksten i Palazzo-tilstand og **skriv det som avvik** (ikke fak det). Oppfyllelse markeres når retten registreres servert (finnes det ikke et slikt hendelsespunkt i dag, legg en `entity.purpose.fulfil`-keypath, eierstyrt). | GODKJENT |
H0:098 | S5 | **Projeksjoner og demo-flate.** `insight.interests`/`insight.purposes`/`avoid` avledes av grafen (samme svarform som i dag — kontraktstester må stå). Ny eierstyrt `entity.graph` (get) som returnerer noder, kanter, vekter og provenance for **gjestens egen** graf — det er det Kjetil viser i morgen. `validateAccess` på alle nye keypaths; negative tester (feil requester, feil keypath). | GODKJENT |
H0:099 | S6 | **Docs + rapport.** `docs/Remember_contract_2026-09-07.md` oppdateres (Last verified against code), ny `docs/Signalgraf_2026-09-21.md` (hva som er noder, vekter, provenance, hva som er avledet vs. redigert, avvik). Rapport §7. | GODKJENT |
H0:100 | S7 | **Commit + push** på `pdd/palazzo-2026-09-14` — bare hvis hele suiten er grønn eller rød *kun* på det §6 tillater. Commit-melding «Signalgraf: Interest/Purpose-noder med vekter, én motor (HD-0098, HD-0099, HD-0116)». Push utløser CI som bygger imaget. | GODKJENT — betinget av §6 |
H0:101 | S8 | Deploy til `palazzo.digipomps.org` | **Ikke din** — kjøres av skript-jobben `natt2` etter deg (HD-0077 KJOR-0…4). Du skal ikke røre verten. |
H0:102
H0:103 Ikke i natt: taksonomi-forsoning, `cell:///PurposeRegistry`, tillitspakke som `proofs`, måltallet
H0:104 for tilhørighet, Porthole-lasting fra fjernt scaffold (HD-0078), CellProtocol #35.
H0:105
H0:106 ## 6. Portene
H0:107
H0:108 **Grønn suite** før push. Det finnes én kjent rød flekk: `PalazzoBridgeheadTests.testBridgeheadGuestVsHouse`
H0:109 og `testBridgeheadReaction` feiler mot CellProtocol main `b5b7282` fordi bro-fiksene ligger i
H0:110 CellProtocol PR #35 som ikke er på main (`HAVEN-Deploy/_handoff/HD-0077/BRO-MOT-MAIN-20260920.md`).
H0:111 CI pinner `b5b7282` og kjører `swift test`, så rød suite = intet image = ingen deploy.
H0:112
H0:113 **Kjetils regel er at ingen test fjernes eller svekkes.** Derfor: du får **ikke** skippe eller endre
H0:114 disse to på egen hånd. Losen har lagt spørsmålet til Kjetil (§8). Handling avhenger av svaret hans,
H0:115 lest fra `HAVEN-Deploy/_handoff/HD-0077/KJETIL-SVAR-BRO-TESTER.md` hvis fila finnes når du kommer til S7:
H0:116 - fila sier **`XCTSkip`** → merk nøyaktig disse to med `throw XCTSkip("Venter CellProtocol #35 på main — HD-0077")`, ingen andre, og skriv det i rapporten;
H0:117 - fila sier **`stopp`** eller finnes ikke → **ikke push**; fullfør S0–S6, rapporter, og stopp. Da deployer `natt2` ingenting (den sjekker CI-status og stopper med FEIL).
H0:118
H0:119 Andre porter: alle nye handlere kaller `validateAccess`; ingen no-op-stubber; Explore-audit for appen
H0:120 grønn (`Tools/Explore` som i G7-rapporten); ingen `print` av gjestedata.
H0:121
H0:122 ## 7. Rapporten
H0:123
H0:124 `docs/Rapport_Signalgraf_2026-09-21.md`: rå utdata før/etter (antall tester, røde med navn), per
H0:125 slice gjort/avvik, hvilke CellProtocol-typer som faktisk ble brukt (med filsti og revisjon), om grafen
H0:126 persisteres eller avledes, om polaritet kom fra CellProtocol eller Palazzo, om Goal ble
H0:127 `CellConfiguration` eller `nil`, filliste, og commit-SHA hvis pushet. `TESTRESULT.md` i
H0:128 `CellProtocolDocuments/Deliverables/PDD_palazzo-signalgraf_2026-09-21/` med ankre `#build #regression
H0:129 #graf #match #negativ #hensikt #projeksjon #auth`. Svar i køen kun med rapporten.
H0:130
H0:131 ## 8. Åpent hos Kjetil (Losen har spurt)
H0:132
H0:133 Bro-testene i §6. Alt annet er avgjort.
```

## Kort vurdering

Forslaget er tilstrekkelig konkret til at Kjetil kan **nekte G3 med presise grunner**, og til å godkjenne eller korrigere et G1-delta rad for rad. Det er **ikke et fullstendig grunnlag for ubetinget G3**: Goal-/bestillingsresten, hva «vise grafen» skulle innebære og tilhørende demonstrasjonsbevis, samt avstemmingen mot de tomme formåls-/testfeltene må avklares; Matchebenken-originalen mangler også. Deployen er dokumentert levert av natt2-kjeden neste morgen, uten bevis for den planlagte visningen. Ingen port er satt.
