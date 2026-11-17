# FORMÅLSSPEC — lokal kapabilitet

Iterasjon 1 · 2026-09-29 · **venter på G1**

## P0 — hva Kjetil sa

> «Vi skal se på om vi kan lage funksjonalitet for å avvikle konserter live også.
> Tanken er at vi kan styre andre programmer f.eks. på en Mac laptop for å skru av
> og på lydstrømmer — synkronisert — som en DJ-app, f.eks. mixxx. Styre video-
> strømmer, route lydkanaler på macen. Det er interessant å lage virtuelle digitale
> instrumenter også. Har lyst til å se om vi etterhvert kan bygge en Apple Vision
> versjon av flaten. Kan være at vi trenger native funksjonalitet i HAVEN app også,
> men vi bør lage det som generell kapabilitet som komponenter ikke bloate med med
> masse programflate — det kan vi laste ned fra et scaffold som kan peke til
> kapabilitet som ligger lokalt og tilgjengelig fra HAVEN app.»

Den siste setningen er bestillingen. Resten er hva den skal brukes til.

## Tre spor, som ikke skal blandes

Kjetil har åpnet tre ting de siste dagene. De henger sammen, men de har hvert sitt
formål og hver sin risiko.

| Spor | Hva | Status |
|---|---|---|
| **A — generell musikkpublisering** | flere utgivere enn Butterpop, profil/blogg knyttet til utgivelser, arrangement (vernissage, slippfest). Scaffold eller eget target. | retning gitt, ikke dekomponert |
| **B — lokal kapabilitet** | *denne spec-en*. Live-avvikling, styre programmer og lyd/video på en maskin, virtuelle instrumenter, Vision-flate. | P0 skrevet |
| **C — innholdsvern lyd** | kryptering, HLS, tre vernnivåer. | G1+G2 godkjent, AP1 skrevet |

Spor B er det eneste med reelle ukjente. A er i hovedsak omorganisering av noe som
finnes. C er i gang.

## Funn: mye av spine-en finnes allerede

Før noen foreslår ny mekanikk. Dette er lest i kontrakter og doc-kommentarer, ikke
i implementasjonen — det må etterprøves.

- **`HAVENAgentCapabilityBrokerCell`** (CellScaffold, 627 linjer) har allerede
  `capability.evaluate`, `registration.report`, `registration.clear`, og en
  følgecelle `HAVENAgentSetup` med `setup.inspect`, `setup.install.prepare`,
  `setup.draft.artifactReference`, `setup.draft.sha256`,
  `setup.draft.signingEvidence`.
  **Det er nesten ordrett «last ned kapabilitet fra et scaffold, verifisert».**
  Men den brokerer i dag om HAVEN-*agenten* er installert og registrert — ikke
  vilkårlige lokale kapabiliteter.
- **`KallimachosCapabilityIndex`** er et lesbart register over hvilke kapabiliteter
  som finnes i kildetreet. Doc-kommentaren sier selv: indeksen er *bevis på hva som
  finnes*, ikke en tilgangsavgjørelse, og kallere må fortsatt løse endepunktet og
  sjekke grants. Den disiplinen er altså allerede skrevet ned.
- **`CapabilityInvitationProofSupport`** knytter kapabilitet til invitasjon, ressurs,
  endepunkt og gruppepolicy.

**Hypotese å teste, ikke konklusjon:** dette er sannsynligvis en *utvidelse* av en
mekanisme som finnes, ikke en ny mekanisme.

## P1 — formålsdekomponering

**At det skal finnes:** En celle eller flate skal kunne peke på en kapabilitet som
ligger lokalt på en maskin, og bruke den, uten selv å bære programflaten.

Hva det skal løse — hvert punkt er et eget formål, og hvert av dem kan svikte alene:

| # | Formål | Måles på |
|---|---|---|
| **F1** | `kapabilitet.komponenten-forblir-tynn` | En komponent som bruker lydruting inneholder ikke lydruting. Komponentens avhengigheter endrer seg ikke når en ny kapabilitet tas i bruk. |
| **F2** | `kapabilitet.den-finnes-eller-sier-fra` | En flate som ber om noe som ikke er der, sier det. Den feiler ikke stille og later ikke som. Samme familie som `manifestet.navnene-lyver-ikke` fra innholdsvernet. |
| **F3** | `kapabilitet.makt-over-maskinen-er-gitt-ikke-antatt` | Å rute lyd eller styre et program på noens maskin er en makt. Den skal komme av et grant, være avgrenset til det den trenger, kunne trekkes tilbake, og etterlate spor. **Uten dette er dette en plugin-arkitektur, ikke HAVEN.** |
| **F4** | `kapabilitet.tiden-eies-lokalt` | Maskinen eier klokka. HAVEN sier hva som skal skje og hvem som får utløse det; maskinen bestemmer nøyaktig når. Se risiko R1. |
| **F5** | `kapabilitet.samme-celle-flere-verter` | Samme celle treffer en kapabilitet på Mac, i HAVEN-appen og senere på Vision, uten å vite hvilken. |
| **F6** | `kapabilitet.kan-hentes-ikke-bare-forhaandsinstalleres` | Kapabiliteten kan lastes ned fra et scaffold, med verifiserbar herkomst. Ser ut til å finnes i `setup.install.prepare` allerede. |

## Risiko som må avgjøres tidlig

### R1 — synkronisering er ikke det samme som styring, og det er der dette knekker

Kjetil skrev «synkronisert» nesten i forbifarten. Det er den vanskelige delen.

En DJ-app trenger beat-nøyaktighet: noen få millisekunder. Et cue-bytte tåler
kanskje noen titalls. En rundtur gjennom celleløsning, grant-sjekk og nett er
30–150 ms, og *ujevn* — jitteret er verre enn forsinkelsen.

**Per-hendelse fjernstyring kan derfor ikke være arkitekturen.** Det vil se ut til
å virke på skrivebordet og rakne på en scene.

Det som kan virke: HAVEN sender **planen på forhånd** — et cue-ark med tidspunkter —
og den lokale kapabiliteten kjører den mot sin egen klokke. Derfor F4.

Dette er en påstand fra meg som bør valideres uavhengig før den legges til grunn.

### R2 — fire ting med samme navn

«Kapabilitet» dekker her fire problemer som ikke ligner hverandre:

| | Hva | Hvor vanskelig |
|---|---|---|
| **Styre** et program som finnes (Mixxx, video) | snakke med noe annet | håndterbart — Mixxx har MIDI/OSC |
| **Rute** lydkanaler på macOS | OS-nivå, trolig virtuell lydenhet | egen tillatelsesflate, eget driverproblem |
| **Lage** lyd — virtuelle instrumenter | sanntids lydtråd | et helt annet fag. Ingen nett, ingen venting, ingen allokering i lydtråden |
| **Vise** — Apple Vision | **ikke et kapabilitetsspørsmål** | Vision er en ny renderer for skjelettet, ved siden av CellApple/Binding. Det hører hjemme i renderer-sporet, ikke her |

At Vision kan flyttes ut av bunken er i seg selv en forenkling.

### R3 — dette hullet finnes allerede, og vi står i det nå

Losen kan skrive filer i de mountede repoene, men ikke kjøre noe på Mac-en.
`_losen-queue` er en håndlaget lokal kapabilitet: en prosess på maskinen som
utfører det en fjern part ber om. Den er bygget fordi mekanismen i denne spec-en
ikke finnes ennå.

Det betyr at F1–F4 har en **ekte, daglig bruker allerede**, uavhengig av konserter.
Det er en billig måte å prøve mekanismen på noe vi kjenner.

## Førsteprøven jeg foreslår

Ikke Mixxx. Ikke Vision. Én kapabilitet, hele veien, på noe som er lite nok til at
feilen er synlig:

> En HAVEN-flate ber om kapabiliteten «kjør en navngitt kommando i dette repoet på
> denne maskinen». Den finnes eller sier fra. Den krever et grant som er avgrenset
> til ett repo og kan trekkes tilbake. Hver kjøring etterlater spor.

Det er Losen-køen, men som kapabilitet i stedet for som hjemmesnekret mappe. Den
øver F1, F2, F3 og F6 på én gang, og den har en bruker fra dag én.

Synkronisering (F4) er ikke med i førsteprøven med vilje. Det er et eget problem og
bør få sin egen prøve når mekanismen står.

## Hva som ikke er besvart

- Spor A — scaffold eller eget target for musikk/profil/portefølje. Venter.
- Hvor kapabiliteter *bor*: i HAVEN-appen, som egne prosesser, eller begge.
- Om `HAVENAgentCapabilityBroker` faktisk kan utvides, eller bare ser slik ut
  utenfra. Må leses ordentlig.
- Statistikkoppgaven: skal den anonyme gjennomspillingstelleren bygges i det hele
  tatt, når den ikke kan sikres.
