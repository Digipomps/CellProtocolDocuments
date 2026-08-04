# Personlig onboarding: verdi, butler-persona og kapabilitetsstige

- Dato: 2026-07-20
- Status: plan; bygger på implementert Slice 1+2 fra
  `CoPilot_HAVEN_Onboarding_Privacy_Architecture_2026-07-13.md` og den
  implementerte Personal Butler-profilen i Binding
  (`PersonalButlerProfileAndProactivity_2026-07-13.md`)
- Beslutningseier: Kjetil

## Konklusjon

Onboardingen skal gjøres om fra et samtykke-først-løp til et verdi-først-løp i
fire akter: (1) butleren viser verdi før den ber om noe, (2) brukeren døper og
former butlerens personlighet med levende forhåndsvisning, (3) en eksplisitt
kapabilitetsstige viser at butleren gjør mer og bedre arbeid når brukeren
legger på mer AI-kapabilitet, og (4) grunnmuren (personvern, autoritet,
modellpolicy) bekreftes som i dag. Nesten hele runner-, profil- og
policy-infrastrukturen finnes allerede; planen er i hovedsak et nytt script,
noen nye profil-felter, én ny kapabilitetsstige-flate og parity/verifisering.

Dette løser samtidig åpent valg nr. 5 fra 2026-07-13-dokumentet: «butler» blir
produktbegrep, ikke bare en valgbar persona. Det valget bekreftes av Kjetil
før Slice A starter.

## Formål og mål

| Formål | Goal | Baseline | Target | Evidens |
| --- | --- | --- | --- | --- |
| `purpose://human-agency` | Brukeren forstår HAVENs verdi gjennom demonstrasjon, ikke tekst. | Onboarding åpner med consent-kort. | Første konkrete verdi-demonstrasjon innen 60 sekunder fra første åpning (Arendalsuka-kriteriet); brukeren kan etterpå beskrive med egne ord hva HAVEN gjør for hen. | Klikk-gjennom med stoppeklokke + kontrollspørsmål i script. |
| `purpose://preference.owner-controlled` | Brukeren eier butlerens navn og personlighet. | `displayName` + `interactionStyle` finnes; ingen persona-forming eller forhåndsvisning. | Navn, arketype, tonetrekk og stilnotat lagres owner-local; brukeren ser en deterministisk forhåndsvisning av «slik svarer {navn}» før bekreftelse. | Profil-cell-tester + skeleton-flate. |
| `purpose://access.audit.privacy` | Mer kapabilitet endrer kvalitet, aldri autoritet eller personvernpolicy. | Prinsippet er dokumentert og håndhevet i policy-porten. | Hvert stigetrinn i onboardingen går gjennom eksisterende policy-port, tillitspakke og samtykke; ingen snarveier for demo-formål. | Policy-tester + negative assertions. |
| kapabilitetstransparens (under `purpose://human-agency`) | Brukeren forstår at ytelse kommer av synlige byggeklosser. | `functionalLevel` finnes i Binding, men vises ikke i onboarding. | Brukeren kan peke på sitt nåværende trinn og si hva neste trinn låser opp, knyttet til sitt eget deklarerte formål. | Kontrollspørsmål i script + stige-flate. |

## Repo-sannhet

### Det som finnes og gjenbrukes

- `GuidedOnboardingCell` (CellScaffold) med allowlistede scripts, dry-run,
  eksplisitt bekreftelse, gap-drevet gjenopptakelse og hjelpemodus.
  `personal-copilot-foundation-v1` dekker allerede navn, formål, innhold,
  interesser, samhandlingsstil, læringspolicy og providerpolicy.
  `haven-foundation-v1` dekker de tre prinsipp-bekreftelsene.
- `PersonalAssistantProfileCell`: owner-scoped, persistent profil med
  tillitspakker og samtykker (Slice 2-policy-porten er implementert).
- Binding `BindingPersonalChatHubCell` med `chatHub.state.butler`:
  `profile` (navn, stilnotat), `capabilities` (functionalLevel:
  `basic_chat` → `guided_local` → `model_assisted` →
  `contextual_model_assisted`), `proactivity`, `support`, `sync`.
  Owner-signert preferansesync mellom enheter finnes.
- `ChatScopedAIProviderRouter` + deterministisk policy-port foran rangering;
  ingen automatisk lokal-til-ekstern fallback.
- Model Toolbox Advisory (2026-06-11) med åtte modellklasser som
  kapabilitetsstigen kan hente ærlige beskrivelser fra.

### Hull denne planen lukker

1. Onboardingen åpner med bekreftelser, ikke med demonstrert verdi.
2. Personlighet er i dag bare ett picker-valg (`interactionStyle`); det finnes
   ingen tonetrekk, stilnotat-forming eller forhåndsvisning av persona.
3. Kapabilitetsstigen finnes som runtime-snapshot i Binding, men er usynlig i
   onboarding og har ingen flate som viser hva hvert trinn låser opp eller
   hvordan brukeren legger til kapabilitet.
4. Det finnes ingen kobling mellom brukerens deklarerte formål (steg 2 i
   dagens script) og eksemplene som forklarer verdien av mer kapabilitet.

## Produktdesign: fire akter

### Akt 1 - Verdi først (mål: under 60 sekunder)

Butleren presenterer seg uten navn: «Jeg er butleren din i HAVEN. Jeg har ikke
noe navn ennå - det bestemmer du om et øyeblikk.» Deretter demonstrerer den én
til to konkrete, lokale, side-effect-frie handlinger valgt fra det som faktisk
er synlig i scope (for eksempel: vise hvilke tjenester som finnes, lage et
utkast til en huskeliste, forklare et skjermbilde brukeren ser på). Alt i Akt 1
er deterministisk eller lokalt; ingen provider-kall, ingen skriving.

Regel: ingen bekreftelse, intet samtykke og ingen skjema-utfylling før brukeren
har sett minst én demonstrasjon.

### Akt 2 - Dåpen: navn og personlighet

Utvider dagens navnesteg til en persona-sekvens:

1. **Navn** (finnes): owner-local visningsnavn; ingen Identity, ingen
   autoritet.
2. **Arketype** (finnes som `interactionStyle`): butler, samarbeidspartner,
   direkte rådgiver eller nøktern assistent.
3. **Tonetrekk** (nytt): 2-4 trekk fra en avgrenset liste (for eksempel
   formell/uformell, kortfattet/utdypende, tørrvittig/nøytral,
   forsiktig/direkte). Avgrenset liste, ikke fritekst, slik at forhåndsvisning
   kan være deterministisk.
4. **Stilnotat** (nytt, valgfritt): kort fritekst som lagres i profilens
   eksisterende stilfelt.
5. **Forhåndsvisning** (nytt): samme eksempelsvar rendret med valgt navn,
   arketype og tonetrekk - deterministisk malbasert, ikke modellgenerert,
   siden providerpolicy ennå ikke er satt. Brukeren kan justere og se på nytt
   før bekreftelse.

Prinsippet fra 2026-07-13 står fast og gjentas i flaten: navn og personlighet
endrer presentasjon, aldri hva butleren har lov til å gjøre.

### Akt 3 - Kapabilitetsstigen: «Slik blir {navn} smartere»

Kjernen i det nye kravet. En egen flate + scriptsteg som viser:

| Trinn | Runtime-nivå | Byggeklosser (Model Toolbox-klasse) | Hva det låser opp - eksempel knyttet til brukerens deklarerte formål |
| --- | --- | --- | --- |
| 0 | `basic_chat` | Deterministiske lokale regler (klasse 1) | Faste svar, navigasjon, skjema-hjelp. Alltid privat, virker offline. |
| 1 | `guided_local` | + guidede scripts, purpose-graf, helpers (klasse 1) | Guidet oppsett og hjelp steg for steg. Fortsatt uten språkmodell. |
| 2 | `model_assisted` | + lokal språkmodell (klasse 2-3) | Fri formulering, oppsummering, utkast. Merk ærlig begrensning: Apple Foundation Models støtter ikke norsk; norsk kvalitet krever annen lokal modell eller trinn 4. |
| 3 | `contextual_model_assisted` | + scoped RAG over egne Cells (klasse 4) | Svar som bruker brukerens eget innhold med kildehenvisning. |
| 4 | ekstern med samtykke | + ekstern frontier-modell via tillitspakke (klasse 5-8) | Dyp resonnering, koding, multimodalt. Krever fersk tillitspakke, datakategorisamtykke og per-kall-kvittering. |

Designregler for stigen:

- Eksemplene på hvert trinn genereres fra brukerens eget deklarerte formål fra
  Akt 2/dagens formålssteg: «Du sa du ville ha hjelp med X. Med bare lokale
  regler kan {navn} ...; med en lokal modell kan {navn} ...; med en ekstern
  modell du godkjenner kan {navn} ...».
- Stigen viser gjeldende trinn fra det eksisterende
  `capabilities`-snapshotet, aldri en «intelligensscore». Språket er «gjør mer
  mulig» og «kan øke kvaliteten», ikke «blir smartere-garanti» - i tråd med
  claim C2 (narrowed) fra Binding-dokumentet: antall providere er ikke bevis
  på kvalitet eller tilgjengelighet.
- «Legg til kapabilitet»-knappene ruter inn i de eksisterende flytene:
  lokal modell via Binding/HAVENAgentD-oppsett, ekstern provider via
  policy-port + tillitspakke + samtykke. Onboardingen får ingen egen snarvei.
- Demonstrasjon av trinnforskjell i selve onboardingen skjer uten eksterne
  kall: en forhåndslaget side-om-side-sammenligning (samme spørsmål besvart på
  trinn 0/1 vs. trinn 2/3) merket tydelig som eksempel, ikke live resultat.
  Live demonstrasjon av trinn 4 kan først skje etter at providerpolicy og
  samtykke er satt - og da som et ordinært, kvittert kall.
- Mer kapabilitet utvider aldri autoritet eller personvernpolicy; det står
  eksplisitt i flaten.

### Akt 4 - Grunnmur og kontrollspørsmål

Dagens steg beholdes: nødvendig innhold, interesser, læringspolicy,
providerpolicy og de tre HAVEN-prinsipp-bekreftelsene. Kontrollspørsmålet
utvides fra dagens formulering til også å dekke stigen: onboarding er ferdig
når brukeren kan uttrykke (a) hva hen vil oppnå, (b) hva butleren heter og
hvordan den skal opptre, og (c) hvilket kapabilitetstrinn den står på nå og
hva som ville løftet den - eller brukeren eksplisitt hopper over.

## Datamodell- og kontraktsendringer

1. **Nytt script** `personal-butler-onboarding-v2` i `GuidedOnboardingCell`
   (allowlistet; `personal-copilot-foundation-v1` beholdes uendret for
   kompatibilitet). Nye steg: verdi-demonstrasjon (side-effect-fri,
   acknowledgement-basert), tonetrekk, stilnotat, persona-forhåndsvisning
   (bekreftelsessteg), kapabilitetsstige-gjennomgang og utvidet
   kontrollspørsmål.
2. **Profilutvidelse** i `PersonalAssistantProfileCell` og speilet i
   Binding-profilens felt-allowlist for sync:
   `personaTraits: [String]` (avgrenset vokabular, versjonert som
   `personal-assistant.persona-traits.v1`) og gjenbruk av eksisterende
   stilfelt for stilnotatet. Rå fritekst utover stilnotatet lagres ikke.
3. **Stige-lesemodell**: en avledet, side-effect-fri projeksjon som slår
   sammen `functionalLevel`-logikken og synlige provider-descriptorer til
   `{ currentRung, rungs[], nextActions[] }`. Ingen ny autoritet; kun lesing
   av det som allerede er synlig i requesterens scope. CellScaffold og
   Binding skal dele samme trinn-definisjoner (delt kontrakt, ikke to
   parallelle definisjoner).
4. **Ingen nye toppnivåfelter i `CellConfiguration`** og ingen nye
   skeleton-elementtyper. Stige- og persona-flatene bygges med dagens
   `Section`, `List`, `Text`, `TextField`, `TextArea`, `Button`, `Toggle`,
   `Picker`, `Tabs` og visibility, i tråd med Slice 3-avgrensningen fra
   2026-07-13. Krever et ønske noe utover dette, stoppes det og avklares
   først.

## Implementeringsskiver

### Slice A - Script og profil (CellScaffold)

- `personal-butler-onboarding-v2` med stegene over; dry-run/confirm-kontrakt
  som i dag.
- `personaTraits`-felt med avgrenset vokabular + validering; deterministisk
  malbasert forhåndsvisningsgenerator (ren funksjon, testbar).
- Stige-lesemodellen som avledet projeksjon.
- Tester: allowlist, dry-run før skriving, persistens/reload, ugyldige
  tonetrekk avvises, forhåndsvisning er deterministisk for samme input,
  stige-projeksjon uten provider-kall (`providerInvoked=false`).

### Slice B - Flater i Porthole (skeleton først)

- Persona-flate (dåpen) og kapabilitetsstige-flate som CellConfiguration
  bygget med eksisterende elementer; alle keypaths validert mot komplette
  Explore-kontrakter.
- Iterer via runtime preview/commit i Porthole før eventuell Swift
  factory-promotering.
- Verdi-demonstrasjonene i Akt 1 velges fra en kuratert, side-effect-fri
  liste per scope (konferanse, personlig, gjestevisning).

### Slice C - Binding-paritet og native butler

- Samme onboarding-løp rendres i Binding; parity-matrise for de nye flatene
  (binding-skeleton-parity-testing).
- `chatHub.state.butler.profile` viser persona-trekkene; preferansesync
  utvides med `personaTraits` i felt-allowlisten (samme signerte
  pakkekontrakt som i dag).
- Stigeflaten i Binding leser det eksisterende capability-snapshotet;
  «legg til lokal modell»-handlingen peker på Binding/HAVENAgentD-oppsettet.

### Slice D - Verifisering og måling

- Funksjonell klikk-gjennom av hele løpet som ny bruker og som gjest
  (haven-functional-service-verification), inkludert stoppeklokke på
  60-sekunderskriteriet.
- Claim-review av all onboarding-tekst (haven-claim-review): ingen
  «100 % privat»-påstander utenfor testbar lokal modus, ingen
  kvalitetsgarantier for modeller, ærlig norsk-begrensning for Apple FM.
- Målingsplan for claim C3 (åpen hypotese fra 2026-07-13): oppgavefullføring,
  antall korreksjoner og brukertilfredshet per kapabilitetstrinn, slik at
  «mer kapabilitet ga bedre hjelp» kan dokumenteres i stedet for påstås.

## Claim ledger

| ID | Påstand | Type/styrke | Vurdering |
| --- | --- | --- | --- |
| P1 | Verdi-først-åpning gir bedre forståelse av HAVEN enn consent-først. | predictive, speculative | Open hypothesis; måles med kontrollspørsmål og fullføringsrate. Motargument: demonstrasjon før rammeforklaring kan forvirre; avbøtes med at Akt 1 er side-effect-fri. |
| P2 | Persona-forming med avgrenset vokabular + deterministisk forhåndsvisning gir eierskap uten skjult profilering. | normative + project capability, moderated | Supported av eksisterende C1-adjudikering i Binding-dokumentet; nye felter følger samme sanitiserings- og allowlist-regime. |
| P3 | En eksplisitt kapabilitetsstige gjør sammenhengen «mer AI-kapabilitet → mer/bedre hjelp» tydelig uten å love kvalitet. | causal, moderated | Arver C2 (narrowed): stigen viser hva som blir mulig og at kvalitet kan øke; den påstår ikke at flere descriptorer er kvalitet, og demonstrasjoner i onboarding er merkede eksempler, ikke live bevis. |
| P4 | Stigetrinn kan legges til uten å svekke policy-porten. | security/project capability, assertive | Supported by design: alle «legg til»-handlinger ruter inn i eksisterende port, tillitspakke og samtykke; onboardingen har ingen egen eskaleringsvei. Verifiseres med negative tester. |

## Åpne beslutninger (Kjetil)

1. **«Butler» som produktbegrep**: planen antar ja (løser åpent valg nr. 5 fra
   2026-07-13). Bekreft.
2. **Persona-omfang**: skal tonetrekk kunne inkludere humor/emoji-nivå, eller
   holdes til formalitet/lengde/direkthet i v2? Anbefaling: start smalt.
3. **Demonstrasjon av trinn 4**: er forhåndslagede, merkede eksempler
   tilstrekkelig i onboarding, eller ønskes en valgfri live-demo rett etter at
   providerpolicy + samtykke er satt? Anbefaling: forhåndslagede eksempler i
   v2; live-demo som ordinært kvittert kall etterpå.
4. **Gjestevisning**: skal gjester (Arendalsuka) få Akt 1 + en lesebar stige
   uten profilskriving, med dåpen forbeholdt eiere? Anbefaling: ja.

## Akseptansekriterier

- Første verdi-demonstrasjon skjer innen 60 sekunder, uten samtykkekort først,
  og uten sideeffekter eller provider-kall.
- Brukeren har gitt butleren navn, arketype og tonetrekk, sett en
  deterministisk forhåndsvisning og bekreftet eksplisitt; alt lagres
  owner-local og kan endres, eksporteres og slettes.
- Kapabilitetsstigen viser korrekt gjeldende trinn fra runtime-snapshotet, og
  hvert trinn forklarer med brukerens eget formål hva som låses opp.
- Ingen «legg til kapabilitet»-vei går utenom policy-port, tillitspakke,
  samtykke eller kvittering; `localOnly` holder eksterne providere ute av
  rangeringen som før.
- Mer kapabilitet endrer aldri autoritet, grants eller personvernpolicy, og
  flaten sier det eksplisitt.
- Parity mellom Porthole og Binding for begge nye flater er dokumentert i en
  parity-matrise; klikk-gjennom som ny bruker og gjest er verifisert med
  artefakter.
- All onboarding-tekst har passert claim-review; norsk-begrensningen for
  lokal Apple FM er nevnt der den er relevant.
