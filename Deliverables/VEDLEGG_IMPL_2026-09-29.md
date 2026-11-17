# Vedlegg i korrespondansen — implementasjonsstatus

Rapportnavn følger bestillingen. Arbeidet og byggforsøket ble utført 2026-09-28.

**Status: stoppet ved rødt baseline-bygg, før implementasjon. Ingen vedleggskapabilitet er levert.**
Eierens instruks «Rødt: stopp» er fulgt. Denne rapporten er ikke en godkjenning av funksjonen.

## Mål

Bygge avtalebundne korrespondansevedlegg med automatisk valg mellom `reference`,
`fetchOnDemand` og `copy`; avsenderlagring; meldingsstyrt retensjon; metadata uten hash;
autentisert, chunket overføring; og negative tester for feil melding, feil avtale,
utløp og avbrudd. Avsenders original skal beholdes. Sletting av originalen skal verken
tilbys eller representeres som et valgfritt flagg.

## Påstander og belegg

| Påstand | Belegg og begrensning |
| --- | --- |
| Beslutningsfilen er lest og har prioritet. | `PDD_vedlegg-korrespondanse_2026-09-28/BESLUTNINGER_KJETIL_2026-09-28.md`, lest i eierens eksisterende dokumentarbeidsmappe. |
| Arbeidet er isolert fra eksisterende endringer. | Tre nye worktrees og grener; ingen eksisterende kildefiler er endret. |
| Byggforsøket feilet før kildekodekompilering. | SwiftPM feilet ved kompilering av pakkemanifestet, `exit=1`; se råloggen nedenfor. |
| Vedlegg er ikke implementert eller testet i denne runden. | Ingen kodeendringer eller nye tester. Bare denne rapporten og byggloggen committes. |
| Ingen ting er pushet eller slått sammen til main. | Kun lokale grener og dokumentcommit. |

Målene er ikke oppnådd. Det foreligger ingen påstand om fungerende mottakerhenting,
tilbakekall, opprydding, diskfullhåndtering eller leveranse av installer/budsjett.

## Bygg og stoppgrunn

Kommando kjørt i `HAVEN/_worktrees/cellprotocol-attachments`:

```sh
swift build --disable-sandbox
```

Utgangskode: **1**. Antall forsøk: **1**. Ingen testkommando ble startet etter feilen.

SwiftPM kunne ikke skrive til standard modulcache:

```text
error opening '/Users/kjetil/.cache/clang/ModuleCache/Swift-7JL1KBZ3A6V3.swiftmodule' for output: ... Operation not permitted
error: unable to load standard library for target 'arm64-apple-macosx14.0'
```

Loggen viser også at SwiftPMs konfigurasjons-, sikkerhets- og cachemapper i
brukerens Library ikke var skrivbare. Dette er en miljø-/sandkassefeil, ikke
evidens for en kildekodefeil eller en feilet funksjonstest. `--disable-sandbox`
opphevet ikke prosessens filsystembegrensning. Det ble ikke forsøkt å eskalere
tilgangen eller endre brukerens cachemapper.

Dette var **ikke `exit=64`**, så instruksen om venting og ett nytt forsøk på
eierskapsvakten kom ikke til anvendelse. Etter rødt ble det ikke bygget videre.

[Komplett bygglogg](VEDLEGG_IMPL_2026-09-29_evidence/cellprotocol-baseline-build.log).

## Verktøyflaten slik den faktisk er

Ingen nye verktøy er bygget. `CorrespondenceMCPService` har fortsatt:

- `correspondence_list_inbox`
- `correspondence_read_message`
- `correspondence_send_message`
- `correspondence_ack_message`

`send_message` kan fortsatt ikke henge et vedlegg på meldingen. Det finnes ingen
ny metadata- eller strømmetode i MCP-tjenesten.

Følgende er et **forslag for videre implementasjon**, ikke en implementert kontrakt:

| Verktøy | Foreslått virkning og autorisasjonsgrense |
| --- | --- |
| `correspondence_prepare_attachment(relationshipID, sourceFileRef, clientMessageID, purposeRef?, retentionSeconds?)` | Kontrollerer kilde og faktisk nåbarhet, reserverer meldingsbinding og returnerer navn, type, størrelse, valgt modus og begrunnelse. Autoriserer ikke sending, mottakernedlasting eller sletting av originalen. |
| `correspondence_send_message(..., preparedAttachmentID?)` | Publiserer tekst og vedleggsbinding sammen under den signerte avtalen. Autoriserer ikke installasjon, kjøring eller sletting av originalen. |
| `correspondence_list_attachments(relationshipID, messageID)` | Verifiserer og viser metadata uten å hente filbyte. Autoriserer ikke filhenting eller varig mottakerlagring. |
| `correspondence_fetch_attachment(relationshipID, messageID, attachmentID)` | Verifiserer melding, avtale, tilgang og utløp og henter gjennom en chunket strøm; gir bare et fullført resultat etter autentisert slutt. Autoriserer ikke installasjon, kjøring eller lagring utover meldingens levetid. |

Et MCP-svar skal ikke eksponere strømnøkkelen. Forslaget ovenfor fastsetter ennå
ikke resultattypen for en administrert mottakerstrøm. Det er ikke bygget en
`save_attachment`- eller `delete_sender_copy`-handling.

## Modusvalgets regel

Kravet fra beslutningen, **ennå ikke implementert**:

1. Begge parter når kilden og mottaker kan få avtalebundet lesetilgang:
   `reference`. Opprett lesetilgangen uten å flytte filbyte.
2. Mottaker når ikke referansen, men filen bor hos avsender og lagringen bæres
   der: `fetchOnDemand`. Mottakeren starter overføringen ved henting.
3. Filen er utenfor det en celle kan nå, eller kildelagringen bæres ikke av
   avsender: `copy`. Begrunnelsen må dokumentere hvorfor de andre modusene
   ikke kan brukes. Originalen beholdes uansett.

Avsender får ikke et fritt modusfelt. Nåbarhet og lagringsansvar må komme fra
faktisk kildeløsning og vertens policy, ikke ukontrollerte boolske MCP-argumenter.
Valgt modus og konkret begrunnelse må returneres til klienten. Lagring av et
meldingsvedlegg skal følge beslutningens avsendercelle, også når en ekstern
kilde må importeres som kopi.

## Testresultater enkeltvis

| Testkrav | Resultat |
| --- | --- |
| `reference` velges når begge når kilden; ingen filbyte flyttes | Ikke implementert; ikke kjørt |
| `fetchOnDemand` velges når bare avsender når kilden | Ikke implementert; ikke kjørt |
| `copy` velges for ekstern kilde eller manglende lagringsbæring | Ikke implementert; ikke kjørt |
| Mottaker får samme byte som avsender | Ikke implementert; ikke kjørt |
| Strøm bundet til melding A avvises under melding B | Ikke implementert; ikke kjørt |
| Strøm avvises under annen avtale | Ikke implementert; ikke kjørt |
| Vedlegg utilgjengelig etter meldingens utløp | Ikke implementert; ikke kjørt |
| Avbrudd gir feil og ingen halv fil presentert som komplett | Ikke implementert; ikke kjørt |
| Metadata leses uten filhenting og uten hash | Ikke implementert; ikke kjørt |
| Full disk midt i overføring | Ikke implementert; ikke kjørt |
| `swift build --disable-sandbox` i CellProtocol-worktree | Feil før kildekodekompilering, exit 1 |
| `swift test --disable-sandbox` i CellProtocol-worktree | Ikke kjørt etter stopp |
| Build/test i HavenAgentD-worktree | Ikke kjørt etter stopp |

## Full disk og avbrudd

Ingen overføring ble startet. Det er derfor **ikke målt** hvordan den bestilte
lagringssiden oppfører seg ved full disk eller avbrudd. Feilen i byggloggen er
tilgangsnekt til modulcache, ikke full disk.

Eksisterende `AttachmentStreamV1.open` krever autentisert slutt og returnerer
ikke klartekst før strømmen er verifisert. Dette er observert i kildekoden;
det er ikke en testkjøring fra denne runden. Metoden bufferer hele klarteksten
i minnet. Den eksisterende inkrementelle forsegleren er chunket, men det mangler
fortsatt integrasjon mot et minnebegrenset, transaksjonelt mottakersink for
bestillingen. Den skal bruke samme strømformat, ikke innføre et nytt.

Den nødvendige feilkontrakten er at skrivefeil, kort skriving, avbrudd, feil
autentisering eller manglende slutt ikke kan gi et fullført resultat. Deldata
må holdes privat og ryddes; eventuelle ryddefeil må rapporteres. Meldingsutløp
og tilbakekalt tilgang må også stoppe en pågående henting. Ingen av disse
lagringsgarantiene er levert eller verifisert her.

## Sprik mellom formålsspesifikasjon og beslutning

| Underlaget | Beslutningen som skal gjelde |
| --- | --- |
| G1-forslag, ikke godkjent for implementasjon | G1 er besvart; eierens bestilling autoriserer implementasjon. Ingen ny G1-runde kreves. |
| Fast leveringskopi anbefales | Alle tre moduser kreves; nåbarhet bestemmer. |
| Kryptert leveringslager hos relasjonscellens vert anbefales | Avsenders celle lagrer; mottaker henter. |
| Bevaringsvalg som kan overleve meldingen foreslås | Vedlegget dør med meldingens `retentionSeconds`; ingen egen levetid. |
| 100 MiB og 1 GiB foreslås som grenser | Ingen protokollgrense for samlet vedleggsstørrelse; disk- og tidsfeil må håndteres konkret. |
| Hash foreslås i metadata før nedlasting | Bare navn, type og størrelse; ingen hash før nedlasting. |
| Flere manifestfelter og reservasjoner foreslås | Minimumskravet er signert `messageID` + avtale-id, verifisert ved henting. Ekstra mekanismer må begrunnes av implementasjonen. |

Spørsmålet om sletting hos avsender er eksplisitt uavklart. Det er ikke
implementert, og det er ikke lagt inn noe flagg for det.

## Kildeobservasjoner og gjenstående arbeid

- `AttachmentStreamV1.swift` finnes på den lokale `origin/main`-referansen
  brukt nedenfor. Format og sealer skal gjenbrukes.
- `CorrespondenceEnvelopeClient` bruker allerede den felles konvoluttkoden.
  `CorrespondenceClient.validate` kontrollerer mottakernøkler mot signert avtale.
- `CorrespondenceCell.sendMessage` lager `messageID` etter mottak av konvolutten.
  Signert vedleggsbinding trenger en konkret mekanisme for å kjenne endelig ID
  før forsegling, med verifikasjon på mottakersiden.
- Den eksisterende cellen er relasjonsavgrenset. Avsenderlagring må kobles
  eksplisitt til avsenders celle; det kan ikke bare omdøpes fra det tidligere
  foreslåtte felles relasjonslageret.
- HavenAgentDs eksisterende CellProtocol-pin er
  `4107d27a691803897f7aca311573c194d89d1708`. Den er ikke oppdatert i denne runden.
- Gjenstår: all implementasjon, avtale-/kildeintegrasjon, verktøy, tester,
  minnebegrenset mottak, lagringsfeil, retensjon/opprydding og faktisk
  installer-/budsjettleveranse.

## Grener og worktrees

Alle tre lokale grener heter `codex/correspondence-attachments-20260929`.

| Repository | Worktree under HAVEN | Utgangspunkt | Endringer |
| --- | --- | --- | --- |
| CellProtocol | `_worktrees/cellprotocol-attachments` | `81601a6f835252aba7e99d43786fb5d67227c245` (lokal `origin/main`) | Ingen kodeendringer; ingen ny commit |
| HavenAgentD | `_worktrees/havenagentd-attachments` | `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98` | Ingen kodeendringer; ingen ny commit |
| CellProtocolDocuments | `_worktrees/documents-attachments` | `c8029847502fe007833d1ebd371bcb5adc01c3ae` | Rapport og bygglogg committes her |

Remote ble ikke oppdatert; `origin/main` ovenfor er den lokale referansen.
Eksisterende endringer i de opprinnelige arbeidsmappene er beholdt. Rapport og
rålogg kopieres også til den bestilte `CellProtocolDocuments/Deliverables/`-stien;
committen ligger i det isolerte dokument-worktreet. Beslutningsfilen og
formålsspesifikasjonen var eksisterende, usporet underlag og er ikke tatt med
i denne committen.

Underlagets SHA-256 ved lesing (dokumentproveniens, ikke vedleggsmetadata):

```text
BESLUTNINGER_KJETIL_2026-09-28.md
9fe5a2dbf9806b6f34c08e8f6aca4aa35884dd3cf30ecf77c6f642814b92d215
FORMAALSSPEC.md
28e84e5714b9afe4522bed4d7bf78559ff13e7d8ff17ab556c9e4630866dd926
```
