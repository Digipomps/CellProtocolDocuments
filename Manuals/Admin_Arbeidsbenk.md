# Admin-arbeidsbenken

**Her ser du om HAVEN er frisk, hva som kjører, og hvem som har tilgang.** Du
godkjenner også korrespondanse og invitasjoner her, og finner veien til
adminflatene for hvert produkt.

> Sjekket mot koden på CellScaffold `main` 2181841 (med #348), 27. oktober 2026.
> De nye undertitlene fra #348 kommer på staging med neste release. Står det noe annet på skjermen enn her, er det
> skjermen som gjelder. Si fra, så retter vi manualen.

Arbeidsbenken heter **Kontrollplan** i menyen. Fra Utvikler-arbeidsbenken
kommer du hit med knappen **Admin-arbeidsbenken** (fanen Prosjekter, kortet
**Fra idé til levering**). Før neste staging-release heter knappen **Åpne
Admin-arbeidsbenken** og står i fanen Arbeidsflyt.

## Innhold

1. [Komme inn](#1-komme-inn)
2. [Sjekke at alt er friskt](#2-sjekke-at-alt-er-friskt)
3. [Finne ut hvilken versjon som kjører](#3-finne-ut-hvilken-versjon-som-kjører)
4. [Se hva som bruker CPU, minne og lagring](#4-se-hva-som-bruker-cpu-minne-og-lagring)
5. [Vurdere opprydding](#5-vurdere-opprydding)
6. [Kontrollere hvem som har tilgang](#6-kontrollere-hvem-som-har-tilgang)
7. [Godkjenne korrespondanse](#7-godkjenne-korrespondanse)
8. [Invitere og fornye korrespondansedeltakere](#8-invitere-og-fornye-korrespondansedeltakere)
9. [Finne adminflaten for et produkt](#9-finne-adminflaten-for-et-produkt)
10. [Skrive et driftsnotat med AI](#10-skrive-et-driftsnotat-med-ai)
11. [Se hva utviklerne jobber med](#11-se-hva-utviklerne-jobber-med)
12. [Deploye en ny versjon](#12-deploye-en-ny-versjon)
13. [Ord du møter](#13-ord-du-møter)
14. [Det kan du ikke gjøre her ennå](#14-det-kan-du-ikke-gjøre-her-ennå)

## Kart over arbeidsbenken

Menyen til venstre er lik på alle sidene.

| Meny | Side | Bruk den når du vil … | Rolle |
|---|---|---|---|
| Kontrollplan | **Oversikt** | se om alt er friskt | observer |
| | **Drift** | se vert, prosesser, lagring og deploy-klarhet | observer, operator for knappene |
| | **Sikkerhet og tilgang** | se hvem som har tilgang | security |
| | **Produktadmin** | finne adminflaten for et produkt | observer |
| | **Copilot** | skrive et driftsnotat med AI | observer + AI-oppsett |
| | **Utviklingsstatus** | se utviklingsarbeid og hva som venter på deg | observer |
| Godkjenning | **Korrespondanse** | godkjenne forespørsler om å skrive til deg | eier |
| | **Invitasjoner** | invitere og fornye deltakere | eier |

Øverst på hver side står **miljøet** (for eksempel staging) og når dataene sist
ble oppdatert. Sjekk alltid miljøet før du konkluderer.

---

## 1. Komme inn

1. Gå til `/admin` på miljøet du vil se, for eksempel
   `https://staging.haven.digipomps.org/admin`.
2. Logg inn. Du havner på **Oversikt**.

**Roller.** Det finnes tre roller. **operator** og **security** gir også
**observer**; operator og security gir ikke hverandre.

| Rolle | Gir deg |
|---|---|
| **observer** | se oversikt, lagring, historikk og livssyklus |
| **operator** | i tillegg oppdatere vertsmålinger og prosessoversikt, og se deploy-klarhet |
| **security** | se tilgangspolicy, utstedere, revokeringer og agentnøkler |

Rollene gis av den som drifter serveren. Mangler du tilgang til en side i
kontrollplanet, viser den et panel **Tilgang mangler** med knappen
**Be om tilgang**. Den registrerer en forespørsel; den gir ikke tilgang, og
«Forespørsel registrert» betyr ikke at noen har godkjent den. Si også fra til
driftsansvarlig hvilken rolle du trenger og hvorfor.

> **Viktig:** Hvis kontrollplanet ikke svarer, viser siden et banner om det.
> Da vises ingen tall i stedet for gamle tall. Tomme felter betyr «ukjent»,
> ikke «null».

## 2. Sjekke at alt er friskt

**Oversikt.**

- **Readiness** øverst sier om tjenesten er klar.
- **Identitet** sier om byggeinformasjonen er komplett.
- **Snapshot-alder i sekunder** sier hvor gamle dataene er. Et høyt tall
  betyr at innsamlingen henger etter.
- **Operativt sammendrag** og **Collector-status** viser om
  datainnsamlingen virker.
- **Nodeflåte** og **Plasseringsråd** viser maskinene og hvor ny last bør
  legges.
- **Snapshot-lager** viser hvor dataene lagres.

Ser noe galt ut, gå videre til **Drift**.

## 3. Finne ut hvilken versjon som kjører

- **Oversikt → Releaseidentitet** viser **Miljø**, **Byggerevisjon** (git-sha)
  og **Image-digest**.
- **Drift → Deployment readiness** viser **Applikasjonsrevisjon** og om
  tjenesten er klar.

Hvert miljø viser bare seg selv. For å sammenligne staging og prod må du åpne
`/admin` på begge. Releasenavnet (for eksempel 2026.10.12) vises ikke her i
dag; sammenlign byggerevisjonen med deploykvitteringen.

## 4. Se hva som bruker CPU, minne og lagring

**Drift.**

1. Trykk **Oppdater vertsmålinger** for ferske tall for maskinen (krever
   operator).
2. Trykk **Hent prosessoversikt** for de 20 tyngste prosessene (krever
   operator).
3. Les panelene:
   - **Prosesser:** kommando, CPU, minne og tråder.
   - **CPU-belastning**, **Nodeflåte** og **Plasseringsråd.**
   - **Lagringskapasitet** og **Lagringsfotavtrykk.**
   - **Prosessminne over tid** og **Lagring over tid.**
   - **Resolver og lager:** hvor mange celler som er i bruk.

## 5. Vurdere opprydding

**Drift → Cell-livssyklus** og **Oppryddingskandidater** viser celler og data
som kan ryddes.

Det er bare beslutningsgrunnlag. Det finnes ingen sletteknapp. Opprydding
gjøres av driftsansvarlig, med en egen godkjenning.

## 6. Kontrollere hvem som har tilgang

**Sikkerhet og tilgang** (krever security).

- **Adgang og rollepolicy:** reglene for hvem som kan få tilgang og hvem som
  kan utstede den.
- **Trusted issuers:** hvem vi stoler på som utstedere.
- **Credential-revokering:** tilganger som er trukket tilbake, av hvem og
  hvorfor.
- **Tilgangsforespørsler:** hvem som har bedt om hvilken rolle, til hva og
  hvorfor.
- **Betrodde agentnøkler:** nøklene til agentene som får jobbe på serveren.

Siden er bare for å lese. Å gi, endre eller trekke tilbake tilgang gjøres i en
egen, kvittert arbeidsflyt. Se kapittel 14.

## 7. Godkjenne korrespondanse

**Godkjenning → Korrespondanse.** Her ser du hvem som ber om å få skrive til
deg.

Hver forespørsel viser **entitet**, **nøkkel**, når den kom, og når den går ut.
Trykk **Godkjenn** for å si ja.

En godkjenning gir et tidsavgrenset adgangsbevis bundet til nøkkelen som vises.
Den gir ikke tilgang til innhold, og ikke rett til å handle på dine vegne.
Alle avgjørelser lagres med tid og hvem som tok dem.

## 8. Invitere og fornye korrespondansedeltakere

**Godkjenning → Invitasjoner.**

**Invitere en ny:**

1. Under **Ny deltaker**: skriv navnet du kjenner deltakeren igjen på, og en
   **Principal-ID** (bokstaver, tall og `. _ : @ -`).
2. Velg hvem deltakeren **kan skrive til**, hvor lenge **lenken** gjelder
   (timer) og hvor lenge **tilgangen** varer (dager).
3. Trykk **Lag invitasjon**.
4. Kopier lenken under **Ny lenke – kopier den nå**. Den vises bare én gang.
   Trykk **Jeg har kopiert lenken**.
5. Send lenken på en kanal du stoler på.

Lenken gir bare rett til å *be om* tilgang. Du godkjenner selve forespørselen
under **Korrespondanse** (kapittel 7).

**Fornye:** under **Tilganger** trykker du **Lag fornyelseslenke** på en
tilgang som **fornyes snart** eller er **utløpt**. Det går fra sju dager før
tilgangen går ut. Lenken gjelder i sju dager og gir 30 nye dager.

**Utstedte lenker** viser lenker som ikke er brukt ennå.

## 9. Finne adminflaten for et produkt

**Produktadmin** er en innholdsliste, ikke en superadmin. Hvert produkt har
egne regler for tilgang.

- **Din CellProtocol-myndighet** viser om du er registrert som administrator
  for denne serveren, og hvor lenge.
- **Tjenesteadministrasjon:** Utviklingsstatus, meldingsadgang og brukskvote,
  adminkatalogen og spørreskjemaadmin.
- **Produktarbeidsflater:** konferanse, publisering, arrangement og
  RAG-prompter.

## 10. Skrive et driftsnotat med AI

**Copilot** lager et utkast til for eksempel en hendelsesrapport ut fra notater
du selv skriver. AI-en får ikke se noe fra kontrollplanet automatisk.

1. Under **AI-oppsett**: sjekk **Status**. Står det at noe mangler, følg
   **Neste steg**.
2. Trykk **Bruk sikker ops-instruks** første gang.
3. Skriv det du har observert under **Notater**. Ta bort passord, nøkler,
   persondata og rå logger.
4. Trykk **Lag rådgivningsutkast**.
5. Utkastet vises under **Siste utkast**. Les det før du bruker det.

**Legitimasjonsalias** er navnet på en nøkkel som allerede ligger på serveren.
Skriv aldri selve nøkkelen her.

## 11. Se hva utviklerne jobber med

**Utviklingsstatus** (`/admin/development`) viser utviklingsarbeidet sortert
etter formål: **Pågår**, **I kø**, **Blokkert**, **Trenger Kjetil** og
**Nylig levert**. Siden er bare for å lese.

For å jobbe med oppgavene, bruk
[Utvikler-arbeidsbenken](Utvikler_Arbeidsbenk.md).

## 12. Deploye en ny versjon

Ikke her. Admin-arbeidsbenken viser om tjenesten er klar, men starter ikke en
deploy og sier ikke at en deploy er gjort.

En deploy gjøres i den kvitterte deployflyten. Den har lås, kapasitetssjekk,
backup, funksjonell test etter omstart og plan for å rulle tilbake. Etterpå kan
du sjekke byggerevisjonen her (kapittel 3).

## 13. Ord du møter

| Ord | Betyr |
|---|---|
| **Kontrollplan** | delen av HAVEN som passer på at tjenestene kjører |
| **AdminScaffold** | tjenesten som samler inn driftsdata |
| **Readiness** | om tjenesten er klar til å ta imot brukere |
| **Snapshot** | et øyeblikksbilde av driftsdata |
| **Byggerevisjon / git-sha** | hvilken versjon av koden som kjører |
| **Image-digest** | fingeravtrykket til den nøyaktige pakken som kjører |
| **Nodeflåte** | maskinene HAVEN kjører på |
| **Credential** | et bevis på at du har en rolle eller tilgang |
| **Revokering** | at en tilgang er trukket tilbake |
| **Agentnøkkel** | nøkkelen en AI-agent bruker for å få jobbe på serveren |

## 14. Det kan du ikke gjøre her ennå

| Du vil … | I dag | Hva du gjør i stedet |
|---|---|---|
| se staging og prod side om side | ett miljø om gangen, uten releasenavn | åpne `/admin` på begge, og bruk deploykvitteringen |
| deploye eller rulle tilbake | ikke her | bruk deployflyten |
| få en adminrolle | **Be om tilgang** registrerer bare en forespørsel | si fra til driftsansvarlig, som gir rollen |
| gi eller trekke tilbake tilgang | bare lesing | egen kvittert arbeidsflyt via driftsansvarlig |
| slette gamle data eller celler | ingen sletteknapp | be driftsansvarlig, med godkjenning |
| se testlista for staging | finnes ikke i admin | i [Utvikler-arbeidsbenken](Utvikler_Arbeidsbenk.md#2-se-hvor-du-kan-jobbe): **Prosjekter → Min arbeidsbenk → Last inn funn og staging-testlista** |

---

**Kilde i koden** (for utviklere og dokumentasjonssøk): `CellScaffold/Sources/App/Cells/Admin/AdminWorkspaceConfigurationFactory.swift`,
`Sources/App/Cells/Agent/CorrespondenceApprovalConfigurationFactory.swift`,
`Sources/App/Cells/Agent/CorrespondenceInvitationsConfigurationFactory.swift`,
`Sources/App/Controllers/VaporAdminMVP.swift` (`/admin`, `/admin/development`), `Resources/Views/admin_development.leaf`.
Roller settes med `MVP_ADMIN_OBSERVER_USER_IDS`, `MVP_ADMIN_OPERATOR_USER_IDS` og `MVP_ADMIN_SECURITY_USER_IDS` på serveren (`Services/MVPAdminAccess.swift`). Kontrollplanets egne sider krever i tillegg AdminScaffold-rollebevis (`identity.proofs.scaffold.roles.admin.*`); tilgangspanelet er beskrevet i `Documentation/Operations/Admin_Access_Banner.md`.
