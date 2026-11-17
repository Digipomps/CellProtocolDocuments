# Formålsspesifikasjon — palazzo tolkning og vektjustering

Oppgavemappe: `PDD_palazzo-tolkning-og-vektjustering_2026-09-26` · Opprettet 2026-09-26 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

> ### Dette skal du avgjøre (G1)
> 1. **Det nye i CellProtocol main.** B krever at den innebygde listevisningen i appen (den som tegner skjermen i Binding) lærer å lukke og åpne en rad. Den koden ligger i CellProtocol, ikke i Binding som bildet sa. Du sa ja til B. Bekreft at det gjelder en endring på CellProtocol main, testet mot funksjon og formål før den landes.
> 2. **Hva et nytt trykk gjør med emnene.** Forslaget: siste trykk bestemmer om emnene teller for eller mot, og vekten glir bare i hvor sterkt. Alternativet: et motsatt trykk nullstiller og starter på nytt. Benken kjører begge (§6 spm. 2).
> 3. **Skal vekten bare styre rekkefølgen, eller også avgjøre om noe tilbys i det hele tatt?** I dag avgjør vekten ingenting. Ett positivt trykk med et felles emne er nok. Dette er min slutning, ikke noe du har sagt (§6 spm. 3).
> 4. **Tre avvik fra bildet du godkjente** (§3). Hvert har sin egen rute.
>
> Tallene velger du senere, fra benken. Figuren `images/vektjustering-forklart-v1.png` viser trykk → vekt → hva hun får.

## 0. Intensjon (ordrett) og brief-audit

> 2026-09-24, punkt 4 om at gjesten skal kunne se hvilke emner reaksjonen hennes ble tolket som:
> «Gjesten må ha mulighet til det men det bør i utgangpunktet ikke ta noe særlig plass.»
>
> 2026-09-26: «Har sett på G1-GUI. Vi går for B. Ved flere trykk på samme artikkel skal vektene justeres. Der må vi nok prøve oss fram litt med hvor mye et trykk skal justere. Som du erfarte er det noe menig som er mer absolutt enn annen.»
>
> 2026-09-26, svar på tre spørsmål:
> - Nytt positivt trykk etter «Ikke for meg» på samme artikkel: **«Ja, siste trykk gjelder»**.
> - Hva som er absolutt: **«Bare artikkelen»**. Emnene får negativ vekt som trekker ned annet innhold, men stenger det ikke.
> - Gjennomgang av husets emner før gjesten ser dem: **«Nei, de er gode nok»**.

<a id="audit"></a>

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Reaksjonsposten fryser artikkelens emner i det hun trykker. Normaliseringen gjør bare små bokstaver og fjerner duplikater. | retrieved | PalazzoScaffold::Sources/App/Cells/PalazzoEntityCell.swift (`entity.article.react`) og Sources/App/Models/PalazzoRememberModels.swift (`PalazzoTagLexicon.normalized`), `0b74f90` |
| Etter et trykk endrer ingenting seg på artikkelflaten i dag. | retrieved | PalazzoScaffold::Sources/App/Skeleton/PalazzoArticleConfigurationFactory.swift |
| `List.childrenKeypath` og `List.expandedStateKeypath` finnes i skjelettformatet. | retrieved | CellProtocol::Sources/CellBase/Skeleton/SkeletonDescription.swift (`SkeletonList`, U2 2026-09-05) |
| Porthole rendrer det. Løses ikke `expandedStateKeypath`, starter alt lukket. Barn rendres med **samme radmal** som forelderen, med innrykk. | retrieved | CellScaffold::Public/js/skeleton-runtime.js (`seedExpandedFromState`, `flattenListTree`), origin/main `6c70a59` |
| Den native rendereren som Binding bruker, har det ikke. | retrieved (git grep uten treff) | CellProtocol::Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift, origin/main |
| **Rettelse til G1-GUI-bildet:** bildet sa «arbeid i Binding». Den native listerendereren ligger i CellProtocol (CellApple), så endringen går til CellProtocol main. | retrieved | samme fil |
| Vekt per reaksjon: Vil smake 0.8, Interessant 0.5, Ikke for meg −1.0, egne ord 1.0. | retrieved | PalazzoScaffold::Sources/App/Models/PalazzoSignalGraph.swift |
| **Vekten påvirker ikke utfallet i dag.** Én positiv post med felles emne gir positiv dom, og én negativ post med felles emne gir veto for alt innholdet. | retrieved | PalazzoScaffold::Sources/App/Models/PalazzoSignalGraphMatcher.swift, `f548282` |
| Hvert trykk er en egen post, og trykk på samme artikkel stables. | retrieved | PalazzoSignalGraph.swift (én `Entry` per post) |
| Artikkelavvisningen bruker den **første** negative posten for artikkelen. Et senere positivt trykk opphever den ikke. Det strider mot «siste trykk gjelder». | retrieved | PalazzoSignalGraphMatcher.swift (`rejection = graph.entries.first { $0.negative && … }`) |
| Postene endres aldri. Grafen bygges på nytt fra den ordnede rekken, så justering kan beregnes uten å skrive om historikk. | retrieved | PalazzoSignalGraph.swift («Rebuild, never edit») |
| Vetofelle-rettingen er pushet, men ikke merget inn i `pdd/palazzo-2026-09-14`. | retrieved | HAVEN-Deploy/_handoff/PALAZZO-VETO/test-siste.md |
| Hvordan Binding-appen peker på CellProtocol-versjonen (pinnet revisjon eller lokal sti) | unavailable | Hentes i G2 før A1 planlegges ferdig |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-tolkning-og-vektjustering.root | Gjestens egne trykk styrer det hun får, og hun kan se hvordan | — | Om en artikkel er stengt, og om emnene teller for eller mot, følger det hun sist sa. Styrken justeres av flere trykk. Hun kan se hva hvert trykk ble tolket som. | Alle bladene under er grønne | candidate |
| …tolkning-synlig | Hun kan se tolkningen uten at den tar plass | root | Etter et trykk står én lukket rad under knappene. Emnene vises først når hun åpner raden. | A1–A4 | candidate |
| …native-tre-liste (A1) | Den native rendereren viser tre-lister som Porthole | tolkning-synlig | `CellListView` rendrer `childrenKeypath`: lukket når `expandedStateKeypath` gir tom liste eller ikke kan løses, med lokal åpne/lukke uten rundtur til cellen. Oppførselen er lik Porthole. | test.native.tree-list, test.native.tree-parity | candidate |
| …reaksjon-lesbar (A2) | Entitetscellen gir hennes gjeldende reaksjon på én artikkel | tolkning-synlig | GET `entity.article.reaction.<artikkelnøkkel>` gir 0 eller 1 rad `{label, children:[{label}]}`. Raden bygges fra hennes siste egne reaksjonspost for artikkelen og emnene som er frosset på den. Bare eieren får lese. | test.cell.reaction-row, test.cell.auth-negative | candidate |
| …artikkelflate (A3) | Artikkelflaten viser raden på riktig sted og holder den oppdatert | tolkning-synlig | Før første trykk vises ingen rad. Etter et trykk vises én lukket rad. Etter et nytt trykk viser raden den nye reaksjonen, i begge renderere. | test.skeleton.no-unreachable-elements, test.article.row-refresh | candidate |
| purpose://gui.parity-with-approved-image (A4) | Flaten ser ut som det godkjente bildet | tolkning-synlig | Skjermbilder av lukket og åpen rad ligger ved siden av `images/artikkel-tolkning-v1.png`. Kjente avvik er listet i §3. | test.gui.parity | pakke |
| …gjentatte-trykk-justerer | Flere trykk på samme artikkel justerer vektene i stedet for å stable dem | root | Trykkene på én artikkel blir én gjeldende vekt per artikkel. Hvor mye hvert trykk flytter vekten, velger Kjetil fra benken (B5). | B1–B5 | candidate |
| …siste-trykk-gjelder (B1) | Siste trykk avgjør om artikkelen er stengt, og om emnene teller for eller mot | gjentatte-trykk-justerer | Artikkelen er stengt bare når siste trykk på den er «Ikke for meg». Emnenes fortegn følger siste trykk, så raden og virkningen aldri peker hver sin vei. Modellen for styrken avgjøres i §6 spm. 2. | test.weights.last-tap-decides, test.weights.sign-follows-last | candidate |
| …veto-bare-artikkelen (B2) | «Ikke for meg» stenger bare artikkelen | gjentatte-trykk-justerer | Artikkelen er stengt. Emnene får negativ vekt som trekker ned annet innhold med felles emne, men ikke stenger det. | test.weights.veto-article-only | candidate |
| …vekt-avgjor (B3) | Vekten påvirker hva hun får. **Losens slutning, venter på §6 spm. 3** | gjentatte-trykk-justerer | Vekten styrer rekkefølgen på det hun tilbys. Om den også skal ha en terskel for å tilbys i det hele tatt, avgjør Kjetil. Terskel 0 er det samme som bare rekkefølge. | test.weights.threshold, test.weights.monotone | candidate — ikke avklart |
| …justering-parametrisert (B4) | Hvor mye et trykk justerer, er samlet på ett sted | gjentatte-trykk-justerer | Alle tallene (vekt per reaksjon, hvor langt et nytt trykk flytter vekten, negativ emnevekt, terskel) ligger i én navngitt struktur. Ingen tall ligger spredt i koden. | test.weights.policy-single-source | candidate |
| …vektbenk (B5) | Vi kan prøve oss fram | gjentatte-trykk-justerer | Simulerte gjester, hver med egne formål og en rekke trykk, kjøres gjennom **produksjonens** matcher for flere parametersett. Dagens oppførsel er med som referanse. Utdata er én tabell over hva hver gjest får under hvert sett. | test.maal.produksjonsvei, test.bench.inert-by-default, test.bench.has-null-reference | candidate |
| …prinsipper-holder | Prinsippene fra 24.9 gjelder fortsatt | root | Veto for artikkelen, «uavklart» ved ufullstendig søk, avvisningsminne (nå: siste trykk) og bare egne poster er dekket av tester. Eksisterende tester er grønne. | test.regression, test.principles | candidate |
| purpose://quality.build-and-regression | Alt virker | root | Se pakken pkg.std.everything-works. | test.build, test.regression | pakke |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en endring av hvordan huset merker artikler. Emnene vises slik huset skrev dem (Kjetil 26.9).
- Ikke kommentarposten. Emnene på den vises ikke, og vekten på egne ord er uendret.
- Ikke en endring i CellBase-runtimen eller `InterestPurposeWeightedSum`.
- Ikke valg av endelige tall. Benken viser utfallene, Kjetil velger, og valget skrives inn som standardverdier.
- Ikke endringer i Porthole, som allerede støtter tre-lister.
- Ikke et nytt oppsett i biblioteket ennå. Viser justeringsmodellen seg holdbar, foreslås den til `Tools/PurposePackages/` i P6.

Kapabiliteter og avhengigheter oppgaven bygger på:

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Vetofelle-rettingen `f548282` | PalazzoScaffold, grenen `codex/palazzo-vetofelle-20260924` | Palazzo-arbeidet bygger på denne grenen. Merge inn i `pdd/palazzo-2026-09-14` er Kjetils valg, og bør skje før arbeidet bygges oppå. | ja |
| Native tre-liste på CellProtocol main (A1) | CellProtocol::Sources/CellApple/… | Egen worktree fra origin/main, ikke den delte `../CellProtocol`. Må landes med `HAVEN-Deploy/_handoff/LANDING/land-cellprotocol.sh`, og CI må være grønn. Hele regresjonen dekker de andre brukerne av `CellListView`. Kjetils regel: testet mot funksjon og formål før main. Krever ja i boksen øverst. | ja, for A3/A4 |
| At PalazzoScaffold og Binding bygger mot en CellProtocol som har A1 | PalazzoScaffold::Package.swift. Binding: ukjent (se §0). | PalazzoScaffold har bygget mot den delte `../CellProtocol`, som står på en annen tråds gren, med GitHub som reserve. | ja, for A4 |
| Kjørende gjesteflate for paritet: Binding mot Palazzo via bro | lesson.scaffold-without-porthole-host-has-no-preview | Egen slice, ikke del av implementeringen | ja, for A4 |
| Rendereren leser lista på nytt etter trykket | ukjent, må testes | Leses den ikke på nytt, står raden stille. Da er A3 rød. | ja, for A3 |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Referansebilde: artikkel med raden lukket og åpen (variant B) | bilde | `images/artikkel-tolkning-v1.png` | godkjent 2026-09-26 («Vi går for B») | ja |
| Native tre-liste i CellApple, lukket og åpen | testutdata + skjermbilde | TESTRESULT.md#native-tree, `images/actual/` | Porthole-oppførselen | — |
| Artikkelflaten i Binding mot Palazzo: før trykk, lukket, åpen, etter nytt trykk | kjørende flate + skjermbilder | ACCEPT.md#parity | `images/artikkel-tolkning-v1.png` | — |
| Vektbenken: hva hver simulerte gjest får under hvert parametersett og med dagens oppførsel | fil | `maaling/vektbenk-v1.md` | — | du velger sett |
| Commit på CellProtocol main med grønn CI, og pushet Palazzo-gren | commit + CI | TESTRESULT.md#landing | — | — |

Kjente avvik fra det godkjente bildet. Hvert må godtas eller endres:

| # | Avvik | Hvorfor | Godkjent |
|---|---|---|---|
| 1 | **Emnene vises ikke som «brikker».** De blir én innrykket linje med tekst som brytes: «arancini · ris · safran · palermo · catania · gatemat · fritert». | En åpnet rad tegner underradene med samme mal som raden selv. Brikker krever et nytt element. Linjeantallet måles på iPhone-bredde og står i ACCEPT.md. | — |
| 2 | **Teksten for «Ikke for meg»** er «Registrert: Ikke for meg · tolket som mindre interesse for N emner». | Artikkelen er stengt, og emnene trekker ned annet innhold (B2). | — |
| 3 | **Raden viser siste trykk.** Styrken bak kan være justert av tidligere trykk, men fortegnet følger alltid det raden viser (B1). | Flere trykk justerer vekten. | — |

