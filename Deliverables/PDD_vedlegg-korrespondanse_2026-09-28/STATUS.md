# Status — vedlegg i korrespondansen

Dato: 2026-09-28. Oppdrag: kun G1-materiale. Beslutningsgrunnlaget er [FORMAALSSPEC.md](FORMAALSSPEC.md).

- G1: venter — Kjetil har ikke godkjent formålsforslaget.
- G1-GUI: ikke-aktuelt — denne leveransen inneholder ingen GUI-flate.
- G2: ikke-startet — ingen implementeringsplan er godkjent.
- G3: ikke-startet — ingen kapabilitet er implementert eller funksjonstestet her.
- surfaces: cell, terminal
- tags: correspondence, attachment, crypto, retention, mcp

Det er skrevet to Markdown-dokumenter. Ingen Swift eller skjemaer er skrevet eller endret, og ingen commit, push, deploy eller korrespondansesending er utført. Eksisterende endringer i de delte arbeidstrærne er beholdt. Dokumentene er lokale og ikke publisert.

## Målt og lest i denne jobben

«Kildekontrollert» betyr at kildekoden er lest, ikke at atferden er kjørt. Søkene brukte `grep`/Git fordi `rg` ikke var installert i shellmiljøet. Ingen private meldinger eller vedleggsfiler ble hentet.

| ID | Påstand / måling | Resultat og avgrensning | Kilde |
|---|---|---|---|
| M1 | Antall MCP-filer og vedleggstreff | 8 kildefiler, 0 case-insensitive treff på `attachment`, både i lokal mappe og lokal `origin/main`. Bekrefter gapet i denne adapteren, ikke alle mulige lagringssystemer. | HavenAgentD `Sources/HavenCorrespondenceMCP/`; `find`, `grep -Rni`, `git ls-tree`, `git grep -n -i`. |
| M2 | Send-signatur | Kildekoden har `relationshipID`, `subject`, `content`, `purposeRef`, `clientMessageID`, `retentionSeconds`; ingen filfelt. Den tilkoblede MCP-deklarasjonen har `recipientID` i stedet. Ingen sending ble utført for å sammenligne runtime. | [CorrespondenceMCPService.swift](../../../HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceMCPService.swift), linje 97–111 og 164–172; tilkoblet `correspondence_send_message`-deklarasjon. |
| M3 | 16 KiB tekstgrense | Grensen ble ikke funnet i undersøkte `CorrespondenceMCPService`, `CorrespondenceClient`, `CorrespondenceEnvelope` eller `CorrespondenceCell`, heller ikke ved målrettet grensesøk. Det er ikke bevis for at ingen annen/deployet komponent håndhever den. | Samme kilde som M2; M4/M5/M7 nedenfor. Søkeord bl.a. `16384`, `16 * 1024`, `16 KiB`, `maximumContent`, `contentTooLarge`. |
| M4 | Meldingskryptering | Lokal wrapper kaller delt `CorrespondenceEnvelopeUtility` for signering, forsegling, åpning og verifikasjon. Wrapper kontrollerer celle/medlemskap og AAD-kontekst. Ingen integrert vedleggsbeskrivelse. | [CorrespondenceEnvelopeClient.swift](../../../HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceEnvelopeClient.swift), 28–75; [CorrespondenceEnvelope på kontrollert main](https://github.com/Digipomps/CellProtocol/blob/81601a6f835252aba7e99d43786fb5d67227c245/Sources/CellBase/Cells/Correspondence/CorrespondenceEnvelope.swift), 181–265. |
| M5 | Mottakernøkler og tilgang | Medlemsnøklene sammenlignes med signatarer i den signerte avtalen. Klienten krever nøyaktig dagens fire grants; nye vedleggshandlinger kan ikke bare legges til i MCP. | [CorrespondenceClient.swift](../../../HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceClient.swift), 382–414 og 493–559; [avtalemal på main](https://github.com/Digipomps/CellProtocol/blob/81601a6f835252aba7e99d43786fb5d67227c245/Sources/CellBase/Cells/Correspondence/CorrespondenceAgreementTemplates.swift). |
| M6 | Strømbyggekloss på main | De oppgitte typene og `sealChunk`/`finish` finnes. Header har `suiteID`, `version`, `chunkSize`; AAD binder innrammingen, ikke melding/avtale. Innholdsnøkkelen må distribueres utenfor strømformatet. `open` samler hele klarteksten i `Data`. Formatet har ikke en egen total filgrense. | [AttachmentStreamV1.swift på kontrollert main](https://github.com/Digipomps/CellProtocol/blob/81601a6f835252aba7e99d43786fb5d67227c245/Sources/CellBase/Crypto/AttachmentStreamV1.swift), 26–65, 82–179, 193–201 og 214–263; [byggeklossens dokumentasjon](https://github.com/Digipomps/CellProtocol/blob/81601a6f835252aba7e99d43786fb5d67227c245/Docs/AttachmentStreamV1.md). |
| M7 | Meldings-ID og utløp | Cellen genererer `messageID` etter at ferdig kryptert konvolutt er sendt inn. Standardretention er 30 dager, maksimum 90. Utløp fjerner poster ved celleoperasjoner; dette dokumenterer ikke tidsstyrt fysisk sletting, backup-rydding eller vedleggsrydding. `ack` setter kvittering, ikke filkvittering. | [CorrespondenceCell på kontrollert main](https://github.com/Digipomps/CellProtocol/blob/81601a6f835252aba7e99d43786fb5d67227c245/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift), 17–32, 318–411 og 455–476. |
| M8 | Eksisterende kryptotester | Testkilden omfatter rundtur, grensestørrelser, tampering, rekkefølge, feil nøkkel, slutt og inkrementell sealer. Den er lest, ikke kjørt. Ingen ytelses- eller mottakertest utført. | [AttachmentStreamV1Tests på kontrollert main](https://github.com/Digipomps/CellProtocol/blob/81601a6f835252aba7e99d43786fb5d67227c245/Tests/CellBaseTests/AttachmentStreamV1Tests.swift). |
| M9 | Avhengighetspinner | Lokal HavenAgentD `Package.swift` pinner `4107d27…`, hvor strømfilen ikke finnes. HavenAgentD lokal `origin/main` pinner `5609a9a…`, hvor den finnes. «Finnes på CellProtocol main» betyr dermed ikke at enhver lokal klient bygger med den. | `git show origin/main:Package.swift` i HavenAgentD; `git cat-file -e <pin>:Sources/CellBase/Crypto/AttachmentStreamV1.swift` i CellProtocol. |
| M10 | PDD-regler og formålsforankring | Book 35, lokal PDD-ferdighet, mal og `purpose_dev.py lookup` lest/kjørt. Fire pakker valgt; konkrete lærdommer brukt i §4. Ingen nye formålsreferanser eller registerendringer. | [Book 35](../../Book/35_Purpose_Driven_Development_Workflow.md), [mal](../../Prompts/Purpose_Driven_Dev_Spec.md), [PDD-ferdighet](../../.claude/skills/haven-purpose-driven-dev/SKILL.md), [Book 23](../../Book/23_Purpose_Knowledge_Base.md). |

Kildehenvisninger til lokale Swift-filer gjelder observerte kilderevisjoner under. De undersøkte HavenAgentD-filene for service, klient og envelope-wrapper hadde ingen diff mot lokal `origin/main`. `CorrespondenceMCPProtocol.swift` avviker fra main rundt stdio-vakthund; det er ikke brukt til å hevde runtime-paritet. CellProtocols korrespondansefiler har lokale endringer, så fakta om dem er lest med `git show origin/main:<fil>`.

## Revisjoner og nettkontroll

| Repository | Lokal HEAD ved kontroll | Lokal `origin/main` ved kontroll | Nettkontroll |
|---|---|---|---|
| CellProtocol | `561d34a7ea785c087bd6036921f60debe6bace4a` | `81601a6f835252aba7e99d43786fb5d67227c245` | GitHub API GET for `refs/heads/main` returnerte samme `81601a6…` 2026-09-28. |
| HavenAgentD | `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98` | `a9da717453ef3061d288fb5abbb29135c17fc720` | GitHub-connectorens GET ga 404. Ingen konklusjon om fravær eller aktuell remote main; lokal ref er merket som lokal. |
| CellProtocolDocuments | `c8029847502fe007833d1ebd371bcb5adc01c3ae` | Ikke brukt som implementasjonsgrunnlag | Arbeidskopiens PDD-dokumenter og registre er brukt; flere er lokale/endret fra før. |

Kontrollert nettressurs: [CellProtocol main-ref](https://api.github.com/repos/Digipomps/CellProtocol/git/ref/heads/main). Ingen fetch, checkout, reset, commit eller push ble gjort. Leseoperasjoner har ikke oppdatert lokale Git-referanser. Nettkontroll ble brukt for kildeferskhet; dette er ingen ekstern kryptografisk revisjon.

## Opplyst av eieren — ikke selvstendig målt her

| ID | Opplysning | Hvordan den brukes |
|---|---|---|
| O1 | To leveranser har stoppet på fem dager: installerpakken til Vegar og LilleRobot, og et budsjettvedlegg. | Behovet er bestillingsgrunnlag. Ingen logger, pakker, budsjett eller privat korrespondanse er gjennomgått for å rekonstruere hendelsene. |
| O2 | `content` har tak på 16 KiB. | Beholdt som separat tekstkrav i forslaget; håndhevende komponent er åpen, jf. M3. |
| O3 | Nye kapabiliteter skal prøves mot både funksjon og formål før main; én source of truth er eierregel. | Bindende arbeidskrav, ikke noe denne analysen forsøker å bevise statistisk. |

## Antatt eller anbefalt — ikke målt og ikke besluttet

| ID | Antakelse/anbefaling | Hvorfor den kan være riktig | Hva som kan vise at den er feil / hvem avklarer |
|---|---|---|---|
| A1 | Fast filversjon passer begge leveransene. | Pakke og budsjett kan trenge en bestemt versjon. | Budsjettet er kanskje et levende samarbeid. Kjetil avklarer D1/D8. |
| A2 | Én fil per melding er tilstrekkelig. | Dekker en enkel pakke eller ett budsjett uten sammensatt publisering. | Leveransene kan bestå av flere nødvendige filer. Kjetil avklarer D4. |
| A3 | 100 MiB/fil, 1 GiB/relasjon og 8 KiB manifest er passende. | Gir eksplisitte, begrensede budsjetter å diskutere og teste. | Faktiske størrelser, minne og lagringsformat er ukjent. Utfører må måle; Kjetil fastsetter grensene. |
| A4 | Relasjonscellens vert bør lagre leveringskopien. | Unngår avhengighet av avsenders maskin etter publisering. | Vertskapasitet, backup eller driftsansvar kan gjøre alternativ bedre. Kjetil/driftsansvarlig avklarer D2. |
| A5 | 1 times kladd, 24 timers sletting på kjørende vert og 5 minutter etter omstart er akseptabelt. | Konkrete frister kan prøves. | Lange opplastinger eller strengere slettebehov kan kreve andre tall. Kjetil avgjør D2. |
| A6 | Mottakeren bør kunne beholde egen kopi ved uttrykkelig valg. | Installer- og budsjettbruk kan vare lenger enn meldingen. | Partenes lagringsavtale kan forby det. Kjetil avgjør D3; eksisterende grants antas ikke å gi denne retten. |
| A7 | Signert manifest med reservert messageID er riktig integrasjon. | Binder strøm, avsender og avtale til én publisering; gjenbruker eksisterende krypto. | Eksakt kanonisk format, avtaleversjonsbevis, sluttreservasjon og idempotens er ikke spesifisert som kjørbar kontrakt eller testet. Kjetil godkjenner retningen i D6; neste fase må bevise den. |
| A8 | De faktiske klientene kan tilby autoriserte lokale filvalg og asynkrone overføringer. | Trengs for å holde store filer utenfor MCP-tekst og modellkontekst. | Lokal filtilgang, klientstøtte og timeout-forløp er ikke undersøkt. Må avklares før implementasjon, jf. D7. |

## Vurdering av premissene

Behovet er legitimt som bestilling (O1), og integrasjonsgapet er kildekontrollert (M1/M2/M4). Påstanden «byggeklossen finnes» er støttet av M6. Slutningen «det er bare å koble den på» ville derimot være for sterk: M5–M7 viser manglende tilgangskontrakt, meldingsbinding og livsløp; M6 viser også minnebegrensningen. Anbefalingen om filkopi støttes av praktisk begrunnelse, men er fortsatt åpen fordi A1 og A4 ikke er bekreftet.

Kontrollstatus for bestillingens fakta: `retrieved` for åtte filer/null treff og kryptobyggekloss; `retrieved` med kildekonflikt for selector-navnet; `unavailable` for selvstendig dokumentasjon av 16 KiB-håndheving og de to historiske hendelsene. Ingen er lukket på hukommelse alene. Alle anbefalinger A1–A8 er åpne med navngitt beslutnings-/avklaringsansvar.

Formåls-/argumentmetodens kvalitetsdiagnostikk brukes her på en enkel forfatteranalyse, uten å påstå at et rådgiverpanel er kjørt: Q1 kildeendringer er sporet til M2/M3/M6/M9; Q2 blandet vurdering følger evidensen (både bekreftelser og forbehold); Q3 kildekontrollerte fakta er M1–M10, antakelser står separat; Q4 integrasjonsgapet består uansett valg mellom fil og referanse; Q5 ingen anbefaling er definert slik at både bestått og feilet test bekrefter den; Q6 ingen virkelig kontrafaktisk prøve er kjørt; Q7 ingen motivanalyse av personer; Q8 alle åpne valg har eier; Q9 alternativenes begrunnelser er analytikerens, ikke uavhengig motpartsvurdering; Q10 ingen eierpreferanse er ført som teknisk bevis. Dette er avgrensninger, ikke en kvalitetsscore.

## Dokumentkontroll og avslutning

D0: **Dokumentleveransen er ferdig med et dokumentert validatorforbehold.** Egenkontrollen fant alle syv bladformål med mål og test, alle seks spørsmål med anbefaling/begrunnelse, verktøysignaturer og D1–D8 som åpne eiervalg. Alle lokale lenkemål finnes. Ingen produktmål F1–F7 er merket oppnådd. T1–T7 er en plan for senere prøving, ikke testresultater.

| Kontroll | Faktisk resultat |
|---|---|
| `purpose_dev.py gates Deliverables/PDD_vedlegg-korrespondanse_2026-09-28` | Exit 0. G1 står `venter`, G1-artefakt finnes, senere porter er ikke startet. Manglende G2/G3-artefakter er forventet for dette oppdraget. Maskinell formålssammensetning står `unverified`; det er ikke opprettet en JSON-komposisjon. |
| `purpose_dev.py validate Deliverables/PDD_vedlegg-korrespondanse_2026-09-28` | Exit 1: fem referansefeil i felles lærdomsregister og 18 advarsler om manglende komposisjon i Book 23. Ingen av feilene peker på denne oppgavemappen. |
| `purpose_dev.py validate` uten oppgavemappe | Exit 1 med de samme fem feilene og 18 advarslene. Dette avgrenser feilene til felles registergrunnlag; det er ikke reparert som del av dette oppdraget. |
| Fil-/lenkekontroll | De to leveransefilene og alle lokale Markdown-lenkemål finnes. Ingen uutfylte `TODO`/`TBD`-markører eller daterte portgodkjenninger i dokumentene. |
| Git-kontroll | Oppgavemappen står som untracked. Dokumentrepoets HEAD er fortsatt `c8029847502fe007833d1ebd371bcb5adc01c3ae`. `git diff --check` kontrollerer ikke innholdet i untracked-filer og brukes derfor ikke som bevis for disse filenes innhold. |

De fem registerfeilene er at `lesson.sketch-assumed-a-renderer-it-did-not-have`, `lesson.maxwidthinfinity-also-stretches-height`, `lesson.wrap-gives-each-item-its-ideal-width`, `lesson.empty-list-keeps-its-slot` og `lesson.text-field-sends-a-string` peker til den manglende referansen `purpose://candidate.testflyt-verktoycelle.haven-lenke-begge-veier`. Full PDD-validering er dermed **ikke grønn**. D0 dokumenterer dette; den godkjenner verken registeret eller G1 på eierens vegne.

Eierens neste steg er å vurdere D1–D8 i FORMAALSSPEC. Denne leveransen stopper her etter den uttrykkelige bestillingen om G1-materiale. Den starter ingen implementeringsjobb og sender ingen forespørsler til mottakerne.
