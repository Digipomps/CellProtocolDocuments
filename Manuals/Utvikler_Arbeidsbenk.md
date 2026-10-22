# Utvikler-arbeidsbenken

**Ett sted for prosjektene dine og arbeidet ditt.** Her fanger du idéer og feil,
bestemmer hva som skal gjøres, flytter arbeid fremover og godkjenner formål før
noe bygges.

> Sjekket mot koden på CellScaffold `main` 1884a0d (med #344), 22. oktober 2026
> (staging kjører 2026.10.12). Står det noe annet på skjermen enn her, er det
> skjermen som gjelder. Si fra, så retter vi manualen.

## Innhold

1. [Åpne arbeidsbenken](#1-åpne-arbeidsbenken)
2. [Se hvor du kan jobbe](#2-se-hvor-du-kan-jobbe)
3. [Få en idé eller feil inn før du glemmer den](#3-få-en-idé-eller-feil-inn-før-du-glemmer-den)
4. [Finne igjen en oppgave](#4-finne-igjen-en-oppgave)
5. [Bestemme hva som skal gjøres nå](#5-bestemme-hva-som-skal-gjøres-nå)
6. [Flytte arbeid fremover på tavla](#6-flytte-arbeid-fremover-på-tavla)
7. [Jobbe med én oppgave](#7-jobbe-med-én-oppgave)
8. [La hjelperen gjøre ryddejobben](#8-la-hjelperen-gjøre-ryddejobben)
9. [Lære hjelperen dine ord](#9-lære-hjelperen-dine-ord)
10. [Godkjenne formål før noe bygges](#10-godkjenne-formål-før-noe-bygges)
11. [Dele et prosjekt med noen](#11-dele-et-prosjekt-med-noen)
12. [Fra idé til levering](#12-fra-idé-til-levering)
13. [Følge med på et spillverksted](#13-følge-med-på-et-spillverksted)
14. [Endre selve flatene](#14-endre-selve-flatene)
15. [Ord du møter](#15-ord-du-møter)
16. [Det kan du ikke gjøre her ennå](#16-det-kan-du-ikke-gjøre-her-ennå)

## Kart over arbeidsbenken

Arbeidsbenken har elleve faner. Navnene kommer rett fra systemet, derfor er noen på
engelsk.

| Fane | Bruk den når du vil … |
|---|---|
| **Prosjekter** | se prosjektene du har tilgang til og åpne et arbeidsrom |
| **Formål** | lese, rette og godkjenne et formålstre |
| **Book 23** | lese de felles formålene i Book 23 og godkjenne eller avvise forslag til endringer |
| **Hjelper** | endre hva AI-hjelperen kan og hvordan den forstår deg |
| **Intake** | skrive inn en ny idé, feil eller oppgave |
| **All** | søke i alle oppgavene |
| **Board** | se alt på en tavle og dra kort mellom kolonner |
| **Triage** | sortere det som er nytt og se hva som blokkerer |
| **Active** | se det som pågår, feil og mangler |
| **Done** | se det som er ferdig, og lage en rask oppfølging |
| **Arbeidsflyt** | gå videre til portefølje, GitHub og drift |

På fanene Intake, All, Board, Triage, Active og Done står **AI-hjelperen** i en
egen kolonne til høyre.

Under fanene står **den valgte oppgaven** med detaljer. Den vises når du har
trykket på en oppgave i en liste.

---

## 1. Åpne arbeidsbenken

1. Logg inn på HAVEN.
2. Åpne Porthole og velg **Developer Workbench** i menyen.
   Du kan også gå rett til
   `/porthole?configurationName=Developer%20Workbench&configurationEndpoint=cell:///WorkItem`.
3. Fra **Idéer til handling** (idé-arbeidsrommet) kommer du hit med knappen
   **Til Developer Workbench**.

Arbeidsbenken viser bare det du selv eier og det andre har delt med deg.

## 2. Se hvor du kan jobbe

**Fanen Prosjekter.**

- **Tilgjengelige prosjekter** viser hvor mange prosjekter og porteføljer du
  har tilgang til. Hvert prosjekt har status, eier og **Neste steg**.
- Trykk **Åpne arbeidsrom** for å gå inn i et prosjekt. Knappen vises bare når
  du har lov til å åpne det.
- **Utilgjengelige porteføljer** teller delinger som ikke lenger gjelder, for
  eksempel fordi tilgangen er trukket tilbake eller har gått ut.
- Under **Arbeidsområder** åpner du **Min prosjektportefølje** for å lage egne
  prosjekter, og **Delinger og invitasjoner** for å dele eller ta imot (se
  [kapittel 11](#11-dele-et-prosjekt-med-noen)).

Tilgangen sjekkes på nytt hver gang du åpner noe. Har noen trukket tilbake en
deling, forsvinner prosjektet fra lista.

## 3. Få en idé eller feil inn før du glemmer den

**Fanen Intake.**

1. Skriv en kort **tittel**: hva det gjelder.
2. Beskriv det i det store feltet. For en feil: hva du forventet, hva som
   skjedde, og hvor.
3. Fyll inn **Prosjekt** og **Kilde** (for eksempel «staging-test» eller en
   lenke).
4. Trykk **Fang work item**.

Oppgaven havner i kolonnen **Inbox** på tavla. Kortet **Status** ved siden av
viser hvor mange oppgaver du har, hvor mange som er åpne, blokkert, feil,
funksjoner og mangler.

> **Tips:** Du trenger ikke vite prioritet eller type når du fanger noe. Det
> bestemmer du når du sorterer (kapittel 5).

## 4. Finne igjen en oppgave

**Fanen All.**

1. Skriv i søkefeltet. Du kan søke på tittel, ID, prosjekt, merkelapp, status
   eller prioritet.
2. Trykk **Enter** for å søke. Tøm feltet og trykk Enter for å se alt igjen.
3. Trykk på en oppgave for å åpne den (kapittel 7).

## 5. Bestemme hva som skal gjøres nå

**Fanen Triage.**

- **Triage-koe** (Triage-kø) viser oppgaver som venter på at noen tar stilling til dem.
- **Ready** viser det som er klart til å startes.
- **Risiko og blokkere** viser oppgaver som er blokkert, som venter på andre
  oppgaver, eller som andre oppgaver venter på.

Slik sorterer du en oppgave: trykk på den, og velg ny **status** og
**prioritet** i detaljene (kapittel 7). Vil du flytte mange på én gang, be
hjelperen om det (kapittel 8).

**Fanen Active** viser det som pågår, alle feil og alle mangler
(«implementation gaps») hver for seg. **Fanen Done** viser det som er ferdig
eller lagt bort.

## 6. Flytte arbeid fremover på tavla

**Fanen Board.** Tavla har én kolonne per status:

| Kolonne | Betyr |
|---|---|
| **Inbox** | nytt, ikke sortert |
| **Triage** | blir vurdert |
| **Ready** | klart til å starte |
| **In progress** | pågår |
| **Blocked** | står fast |
| **Done** | ferdig |
| **Won't do** | bestemt at det ikke skal gjøres |

- **Flytt et kort:** dra det til en annen kolonne. Er flyttingen ikke lov,
  sier kolonnen hvorfor.
- **Lag et kort rett i en kolonne:** skriv tittelen i feltet **Ny work item**
  øverst, og trykk **+ Kolonnenavn** nederst i kolonnen du vil ha det i.
- **Se detaljer:** trykk på kortet. Detaljene åpnes i en skuff ved kortet.
  Trykk **Lukk** for å lukke den.

## 7. Jobbe med én oppgave

Trykk på en oppgave i en hvilken som helst liste. Detaljene viser:

- **Type, status, prioritet og prosjekt** øverst.
- **Workflow** (status) og **Priority:** knapper for å endre dem. Bare de overgangene som
  er lov, vises.
- **Subtasks:** delstegene og om de er gjort.
- **Comments:** kommentarene.
- **Evidence:** lenker, testresultater og annen dokumentasjon.
- **Dependencies:** hva oppgaven venter på, og hva som venter på den.
- **Activity:** hva som har skjedd med oppgaven, og hvem som gjorde det.

> **Merk:** I dag kan du bare endre status og prioritet her. Kommentarer,
> delsteg og evidens kan du lese, men ikke legge til eller krysse av. Se
> [kapittel 16](#16-det-kan-du-ikke-gjøre-her-ennå).

## 8. La hjelperen gjøre ryddejobben

**Kolonnen ✨ Hjelper**, til høyre på arbeidsfanene. Hjelperen foreslår, du
bestemmer.

1. Velg et **sett** øverst. Settet bestemmer hva hjelperen kan gjøre. For å
   flytte oppgaver bruker du settet **Denne flaten**.
2. Skriv hva du vil ha gjort, for eksempel:
   - «flytt alt fra intake til triage»
   - «flytt den valgte til done»
3. Trykk **Send**.
4. Hjelperen viser et **forslag** med hver oppgave som endres og hvorfor.
   Ingenting er endret ennå.
5. Trykk **Utfør** for å gjøre det, eller **Forkast** for å la være.
6. Angrer du? Trykk **↶ Angre**. Da settes oppgavene tilbake.

Kan hjelperen ikke gjøre det du ber om, sier den hva som mangler. Trykk
**🛎️ Gi saken til Butler** for å sende saken videre. **🛎️ Butler** øverst åpner
Butler direkte.

**Dette kan hjelperen i dag:**

| Sett | Kan |
|---|---|
| **Denne flaten** | flytte oppgaver til en annen status |
| **Idéer til oppgaver** | (forberedt: lage og lenke oppgaver) |
| **Flater og GUI** | ingenting ennå |
| **Dokumentasjon** | ingenting ennå |

Hjelperen gjør alt som deg, med dine rettigheter. Den kan aldri gjøre mer enn
du selv har lov til.

## 9. Lære hjelperen dine ord

**Fanen Hjelper.**

- **Sett:** velg settet du vil endre. Lag et nytt med et navn og
  **+ Nytt sett**. Det nye settet bygger på det valgte og får de samme
  handlingene.
- **Rediger:** skriv instruksjoner med vanlige ord, for eksempel
  *«Når jeg sier «postkassa», mener jeg fanen intake.»*
  Trykk **Lagre som ny versjon**, eller **Forkast utkast**.
- **Tillatte handlinger** står under teksten. De kan ikke utvides ved å skrive
  instruksjoner. Teksten styrer bare hvordan hjelperen forstår deg.
- **Versjoner:** hver lagring blir en ny versjon. Trykk **↶ Gå tilbake hit**
  for å bruke en gammel tekst igjen. Endringen mot forrige versjon vises under.

Settene er dine. Ingen andre ser dem.

## 10. Godkjenne formål før noe bygges

**Fanen Formål.** Før noe bygges, beskriver vi *hva det skal oppnå* som et
formålstre. Du godkjenner formålene og målene, ikke koden.

1. Trykk **Vis treet** på treet du skal se på.
2. Treet går fra venstre mot høyre. Trykk på et formål for å se målet, tegnene
   på at det er nådd og hvordan det sjekkes.
3. Vil du si noe om et bestemt formål: trykk **Kommenter** i dialogen. Da
   havner koden (for eksempel `[A2]`) i kommentarfeltet.
4. Trykk **Godkjenn**, eller skriv hva du vil ha endret og trykk
   **Be om endringer**. Ber du om endringer, må du skrive en kommentar.

Beslutningen går til agenten som laget treet, og vises under **Beslutninger**.
Kommer det en ny versjon av treet, står porten på «venter» igjen.

**Rette treet:** trykk på et formål og velg **Rediger** for å endre tittel,
mål og tegn, **Legg til underformål** for et nytt formål under det, eller
**Fjern** for å ta bort formålet og alt under det (Book 23 endres ikke). Under
**Legg til underformål** søker du blant formålene i Book 23 og i treet, eller
skriver fritt og velger «Legg til … som nytt formål». Hver lagring gir en ny
versjon av treet, og porten står på «venter» igjen.

**Legge inn et tre selv:** lag `tree.json` fra FORMAALSSPEC §1 i PDD-mappen med
`purpose_dev.py tree`, lim den inn under **Legg inn et formålstre** og trykk
**Legg inn treet**. Samme `id` gir en ny versjon av samme tre.

**Fanen Book 23** viser de felles formålene som trærne bygger på. Book 23
endres aldri herfra: trykk på et formål for å foreslå en endring, et nytt
underformål eller fjerning. Forslagene står under **Forslag til Book 23** med
**Godkjenn**, **Avvis** og **Vis**. Et godkjent forslag føres inn i repoet for
hånd og står da som «innført».

## 11. Dele et prosjekt med noen

Gå til **Prosjekter → Delinger og invitasjoner**.

**Invitere:**

1. Velg rolle: **Viewer** (kan se) eller **Editor** (kan endre).
2. Fyll inn eierentiteten (for eksempel `entity://DiMy`), mottakerens entitet og
   **identity UUID**, hvor mange dager tilgangen skal vare, formålet med
   tilgangen og et kort notat.
3. Trykk **Utsted engangslenke**, og send lenken til mottakeren.

**Ta imot:** åpne lenken. Kom du ikke via lenken, lim inn koden under
**Innloes Invitasjon** og trykk **Innloes tilgang** (skjermen skriver dem uten
ø). Etterpå åpner du prosjektet under **Delt Workbench** på samme side, med
knappen **Aapne delt Workbench**.

**Audit** viser hvem som har fått og brukt tilgang.

> **Merk:** Du må kjenne mottakerens identity UUID i dag. Se kapittel 16.

## 12. Fra idé til levering

**Fanen Arbeidsflyt** viser veien et arbeid går, med en knapp til riktig sted
for hvert steg:

1. **Fang idéer og oppgaver** – idé-arbeidsrommet og oppgavelista.
2. **Planlegg og følg opp** – prosjektporteføljen med milepæler og releaser.
3. **Koble kode og verifikasjon** – GitHub-synkronisering. Her knytter du
   pull requests, kildeversjon og testresultater til oppgaven.
4. **Drift og deploy** – **Åpne Admin Workbench** tar deg til driftsflaten.
   Den krever administratorrolle. Se
   [Brukermanual – Admin-arbeidsbenken](Admin_Arbeidsbenk.md).

## 13. Følge med på et spillverksted

For mentorer. Under **Prosjekter → Spillverksted – siste økter** ser du de
siste øktene i spillprosjektet du følger: nivå, antall forslag, og hvor mange
som ble tatt i bruk, forkastet eller rullet tilbake. Det krever lesetilgang til
spillprosjektet.

## 14. Endre selve flatene

Vil du endre hvordan en flate ser ut, for eksempel flytte et panel eller legge
til en komponent, se [Brukermanual – Skeleton-redigering](Skeleton_Redigering.md).

## 15. Ord du møter

| Ord | Betyr |
|---|---|
| **Work item / oppgave** | én ting som skal gjøres: idé, feil, funksjon, dokumentasjon, beslutning eller mangel |
| **Intake / Inbox / new** | tre navn på det samme: nytt og ikke sortert |
| **Triage** | vurdere og sortere nye oppgaver |
| **Implementation gap** | noe som er beskrevet, men ikke bygget |
| **Evidence** | bevis: lenke, test, logg eller skjermbilde |
| **Formålstre** | hva noe skal oppnå, delt opp i mindre mål |
| **Port (G1, G2 …)** | et punkt der eieren må si ja før arbeidet går videre |
| **Sett** | en pakke med instruksjoner og tillatte handlinger for hjelperen |
| **Portefølje** | samlingen av prosjektene dine |

## 16. Det kan du ikke gjøre her ennå

| Du vil … | I dag | Hva du gjør i stedet |
|---|---|---|
| krysse av et delsteg | delstegene vises, men kan ikke krysses av | be agenten eller utvikleren oppdatere oppgaven |
| skrive en kommentar på en oppgave | kommentarer vises, men kan ikke skrives | skriv i beskrivelsen når du fanger oppgaven, eller be agenten |
| legge til evidens | evidens vises, men kan ikke legges til | legg lenken i beskrivelsen eller i kilden |
| la hjelperen kommentere eller sette prioritet | avvises med forklaring | sett prioritet selv i detaljene |
| invitere uten å kjenne mottakerens ID | ikke mulig | få identity UUID fra mottakeren |
| se hva som er deployet | ikke her | se Admin-arbeidsbenken og deploykvitteringene |
| dele fri tekst opp i formål med modellen | valget **Dekomponer … med modellen** finnes under **Legg til underformål**, men er ikke koblet til ennå | skriv formålene selv, eller be agenten lage treet |
| laste inn staging-testlista som oppgaver | knappen **Last inn funn som arbeidspunkter** finnes i **HAVEN Workbench**, ikke her | åpne HAVEN Workbench og trykk knappen der én gang |

---

**Kilde i koden** (for utviklere og dokumentasjonssøk): `CellScaffold/Sources/App/Cells/WorkItems/DeveloperWorkbenchConfiguration.swift`,
`ConfigurationCatalogCell.workItemTrackerConfiguration()`, `Sources/App/Cells/WorkbenchHelper/`,
`Sources/App/Cells/Purpose/PurposeReviewCell.swift`, `Sources/App/Cells/Purpose/PurposeKnowledgeCell.swift`, `Sources/App/Cells/WorkbenchAccess/`.
Celler: `cell:///WorkItem`, `cell:///WorkbenchHelper`, `cell:///PurposeReview`, `cell:///PurposeKnowledge`, `cell:///WorkbenchAccessGrant`.
Tekniske kontrakter: `CellScaffold/Documentation/Operations/Developer_Workbench_AI_Hjelper_2026-10-09.md` og
`Developer_Workbench_Formaalstre_2026-10-09.md`.
