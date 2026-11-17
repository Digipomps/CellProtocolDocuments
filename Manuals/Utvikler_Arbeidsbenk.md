# Utvikler-arbeidsbenken

**Ett sted for prosjektene dine og arbeidet ditt.** Her fanger du idéer og feil,
bestemmer hva som skal gjøres, flytter arbeid fremover og godkjenner formål før
noe bygges.

> Sjekket mot koden på CellScaffold `main` 918b516 (med #351), 27. oktober 2026.
> Det som er nytt med #351 (seks faner, filterknapper på tavla, norske
> kolonnenavn, fanen Ny) kommer på staging med neste release. Til da ser du
> de elleve gamle fanene der. At hjelperen forstår «vurderes» og «fast»,
> kommer med #352. Står det noe annet på skjermen enn her, er det
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

Arbeidsbenken har seks faner.

| Fane | Bruk den når du vil … |
|---|---|
| **Oppgaver** | se alt på tavla, filtrere, søke og dra kort mellom kolonner |
| **Ny** | skrive inn en ny idé, feil eller oppgave |
| **Prosjekter** | se prosjektene dine, sette opp arbeidsbenken, dele, og gå videre fra idé til levering |
| **Formål** | lese, rette og godkjenne et formålstre |
| **Book 23** | lese de felles formålene i Book 23 og godkjenne eller avvise forslag til endringer |
| **Hjelper** | endre hva AI-hjelperen kan og hvordan den forstår deg |

På fanene Oppgaver og Ny står **AI-hjelperen** i en egen kolonne til høyre.

Under fanene står **den valgte oppgaven** med detaljer. Den vises når du har
trykket på et kort på tavla.

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

**Fanen Prosjekter.** Til venstre står prosjektene og veien fra idé til
levering. Til høyre står din egen arbeidsbenk, deling og spillverksted.

**Prosjektene dine**

- Viser hvor mange prosjekter og porteføljer du har tilgang til. Hvert
  prosjekt har status, eier og **Neste steg**.
- Trykk **Åpne arbeidsrom** for å gå inn i et prosjekt. Knappen vises bare når
  du har lov til å åpne det.
- **Utilgjengelige porteføljer** teller delinger som ikke lenger gjelder, for
  eksempel fordi tilgangen er trukket tilbake eller har gått ut.

**Min arbeidsbenk**

- **Sett opp min arbeidsbenk** lager det du trenger for å komme i gang første
  gang. Det er trygt å trykke igjen.
- **Last inn funn og staging-testlista** legger funnene og punktene fra
  staging-testlista inn som oppgaver på tavla. Punkter som alt finnes, blir
  oppdatert, ikke lagt inn to ganger.
- Under knappene står hva som skjedde sist, og hva du kan gjøre etterpå.
- Knappene virker bare på din egen arbeidsbenk. På en arbeidsbenk som er delt
  med deg, vises de ikke.

**Deling**

- **Delinger og invitasjoner**: del et prosjekt eller ta imot en invitasjon
  (se [kapittel 11](#11-dele-et-prosjekt-med-noen)).
- **Min prosjektportefølje**: lag og ordne egne prosjekter.

Tilgangen sjekkes på nytt hver gang du åpner noe. Har noen trukket tilbake en
deling, forsvinner prosjektet fra lista.

## 3. Få en idé eller feil inn før du glemmer den

**Fanen Ny.**

1. Skriv en kort **tittel**: hva det gjelder.
2. Beskriv det i det store feltet. For en feil: hva du forventet, hva som
   skjedde, og hvor.
3. Fyll inn **Prosjekt** og **Kilde** (for eksempel «staging-test» eller en
   lenke).
4. Trykk **Lagre oppgaven**.

Oppgaven havner i kolonnen **Innboks** på tavla. Kortet **Status** ved siden av
viser hvor mange oppgaver du har, hvor mange som er åpne, blokkert, feil,
funksjoner og mangler.

> **Tips:** Er du alt på tavla, kan du lage en oppgave rett i en kolonne
> uten å bytte fane. Se [kapittel 6](#6-flytte-arbeid-fremover-på-tavla).
> Du trenger ikke vite prioritet eller type når du fanger noe. Det bestemmer
> du når du sorterer (kapittel 5).

## 4. Finne igjen en oppgave

**Fanen Oppgaver**, søkefeltet over tavla.

1. Skriv i søkefeltet. Du kan søke på tittel, ID, prosjekt, merkelapp, status
   eller prioritet.
2. Trykk **Enter**. Tavla viser bare kortene som passer, og tallene på
   filterknappene teller bare dem.
3. Tøm feltet og trykk Enter for å se alt igjen.
4. Trykk på et kort for å åpne oppgaven (kapittel 7).

## 5. Bestemme hva som skal gjøres nå

**Fanen Oppgaver**, filterknappene over tavla. Hver knapp viser hvor mange
oppgaver som passer. Trykk på en knapp for å se bare dem. Trykk **Alle** for å
se alt igjen.

| Knapp | Viser |
|---|---|
| **Alle** | alt |
| **Trenger vurdering** | det som står i Innboks eller Vurderes |
| **Pågår** | det som pågår |
| **Feil** | åpne feil |
| **Mangler** | åpne mangler (noe som er beskrevet, men ikke bygget) |
| **Blokkert** | det som står fast, og åpne oppgaver som venter på en annen oppgave |
| **Ferdig** | det som er ferdig eller droppet |

Valget huskes for deg. Andre som ser samme tavle, får sitt eget valg.

Slik sorterer du en oppgave: trykk **Trenger vurdering**, trykk på et kort, og
velg ny **status** og **prioritet** i detaljene (kapittel 7). Eller dra kortet
til en annen kolonne. Vil du flytte mange på én gang, be hjelperen om det
(kapittel 8).

## 6. Flytte arbeid fremover på tavla

**Fanen Oppgaver.** Tavla har én kolonne per status:

| Kolonne | Betyr |
|---|---|
| **Innboks** | nytt, ikke sortert |
| **Vurderes** | blir vurdert |
| **Klar** | klart til å starte |
| **Pågår** | noen jobber med det |
| **Fast** | står fast |
| **Ferdig** | ferdig |
| **Droppet** | bestemt at det ikke skal gjøres |

**Ferdig** og **Droppet** er smale og viser bare hvor mange oppgaver de har.

- **Flytt et kort:** dra det til en annen kolonne. Er flyttingen ikke lov,
  sier kolonnen hvorfor.
- **Lag et kort rett i en kolonne:** skriv tittelen i feltet **Tittel på ny
  oppgave** over tavla, og trykk **+ Ny i …** nederst i kolonnen du vil ha
  det i, for eksempel **+ Ny i Klar**.
- **Se detaljer:** trykk på kortet. Detaljene åpnes i en skuff ved kortet.
  Trykk **Lukk** for å lukke den.

## 7. Jobbe med én oppgave

Trykk på en oppgave i en hvilken som helst liste. Detaljene viser:

- **Oppgave:** type, status, prioritet og prosjekt øverst.
- **Status** og **Prioritet:** knapper for å endre dem. Bare de overgangene
  som er lov, vises.
- **Ansvar og plan:** hvem som har oppgaven, hvilket team, merkelapper og
  frist.
- **Avhengigheter:** hva oppgaven venter på, og hva som venter på den.
- **Kommentarer:** det andre har skrevet om oppgaven.
- **Delsteg:** de mindre stegene og om de er gjort.
- **Evidens:** lenker, testresultater og annen dokumentasjon.
- **Aktivitet:** hva som har skjedd med oppgaven, og hvem som gjorde det.

**Krysse av et delsteg:** trykk **Kryss av** ved delsteget. Det blir merket
**✓ Gjort**. Var det feil, trykk **Åpne igjen**.

**Skrive en kommentar:**

1. Trykk **Skriv kommentar** under Kommentarer.
2. Skriv kommentaren i feltet som kommer fram, og trykk Enter.
3. Trykk **Send kommentar**. Kommentaren vises under Kommentarer.

> **Merk:** Evidens kan du lese her, men ikke legge til ennå. Se
> [kapittel 16](#16-det-kan-du-ikke-gjøre-her-ennå).

## 8. La hjelperen gjøre ryddejobben

**Kolonnen ✨ Hjelper**, til høyre på fanene Oppgaver og Ny. Hjelperen foreslår, du
bestemmer.

1. Velg et **sett** øverst. Settet bestemmer hva hjelperen kan gjøre. For å
   flytte oppgaver bruker du settet **Denne flaten**.
2. Skriv hva du vil ha gjort, for eksempel:
   - «flytt alt fra innboks til vurderes»
   - «flytt den valgte til ferdig»

   Bruk gjerne navnene på kolonnene. Hjelperen forstår også de engelske
   navnene (inbox, triage, done …).
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
  *«Når jeg sier «postkassa», mener jeg kolonnen Innboks.»*
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

Gå til **Prosjekter → Deling → Delinger og invitasjoner**.

**Invitere:**

1. Velg rolle: **Viewer** (kan se) eller **Editor** (kan endre).
2. Fyll inn eierentiteten (for eksempel `entity://DiMy`), mottakerens entitet og
   **identity UUID**, hvor mange dager tilgangen skal vare, formålet med
   tilgangen og et kort notat.
3. Trykk **Utsted engangslenke**, og send lenken til mottakeren.

**Ta imot:** åpne lenken. Kom du ikke via lenken, lim inn koden under
**Innløs invitasjon** og trykk **Innløs tilgang**. Etterpå åpner du prosjektet
under **Delt arbeidsbenk** på samme side, med knappen **Åpne delt
arbeidsbenk**.

**Audit** viser hvem som har fått og brukt tilgang.

> **Merk:** Du må kjenne mottakerens identity UUID i dag. Se kapittel 16.

## 12. Fra idé til levering

**Fanen Prosjekter**, kortet **Fra idé til levering**. Det viser veien et
arbeid går, med én knapp for hvert steg:

1. **Fang idéer og oppgaver** – **Idé-arbeidsrommet**, der idéer modnes før de
   blir oppgaver. Nye oppgaver lager du i fanen **Ny**.
2. **Planlegg i porteføljen** – **Åpne porteføljen** med milepæler og releaser.
3. **Koble kode og tester** – **GitHub-synk**. Her knytter du pull requests,
   kildeversjon og testresultater til oppgaven.
4. **Se hva som kjører** – **Admin-arbeidsbenken** tar deg til oversikten der
   du ser om tjenesten er frisk og hvilken versjon som kjører. Den krever en
   administratorrolle. Se
   [Brukermanual – Admin-arbeidsbenken](Admin_Arbeidsbenk.md).

## 13. Følge med på et spillverksted

For mentorer. Under **Prosjekter → Spillverksted – siste økter** (til høyre) ser du de
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
| **Innboks** | nytt og ikke sortert. I eldre tekster heter det intake, inbox eller new |
| **Vurderes** | oppgaven blir vurdert og sortert. Engelsk: triage |
| **Fast** | oppgaven står fast. Engelsk: blocked |
| **Mangel** | noe som er beskrevet, men ikke bygget. Engelsk: implementation gap |
| **Evidence** | bevis: lenke, test, logg eller skjermbilde |
| **Formålstre** | hva noe skal oppnå, delt opp i mindre mål |
| **Port (G1, G2 …)** | et punkt der eieren må si ja før arbeidet går videre |
| **Sett** | en pakke med instruksjoner og tillatte handlinger for hjelperen |
| **Portefølje** | samlingen av prosjektene dine |

## 16. Det kan du ikke gjøre her ennå

| Du vil … | I dag | Hva du gjør i stedet |
|---|---|---|
| legge til evidens | evidens vises, men kan ikke legges til | legg lenken i beskrivelsen eller i kilden |
| la hjelperen kommentere eller sette prioritet | avvises med forklaring | sett prioritet selv i detaljene |
| invitere uten å kjenne mottakerens ID | ikke mulig | få identity UUID fra mottakeren |
| se hva som er deployet | ikke her | se Admin-arbeidsbenken og deploykvitteringene |
| dele fri tekst opp i formål med modellen | valget **Dekomponer … med modellen** finnes under **Legg til underformål**, men er ikke koblet til ennå | skriv formålene selv, eller be agenten lage treet |
| se ferdige eller droppede oppgaver én og én | kolonnene Ferdig og Droppet viser bare antallet | søk etter oppgaven i Work Item Tracker eller HAVEN Workbench |

---

**Kilde i koden** (for utviklere og dokumentasjonssøk): `CellScaffold/Sources/App/Cells/WorkItems/DeveloperWorkbenchConfiguration.swift`,
`ConfigurationCatalogCell.developerWorkbenchTaskBoard()` / `developerWorkbenchNewTask()` / `developerWorkbenchOwnerCard()`, `Sources/App/Cells/WorkItems/WorkItemCell.swift` (`board.setFilter`), `Sources/App/Cells/WorkbenchHelper/`,
`Sources/App/Cells/Purpose/PurposeReviewCell.swift`, `Sources/App/Cells/Purpose/PurposeKnowledgeCell.swift`, `Sources/App/Cells/WorkbenchAccess/`.
Celler: `cell:///WorkItem`, `cell:///WorkbenchOwnerSetup`, `cell:///WorkbenchHelper`, `cell:///PurposeReview`, `cell:///PurposeKnowledge`, `cell:///WorkbenchAccessGrant`.
Tekniske kontrakter: `CellScaffold/Documentation/Operations/Developer_Workbench_AI_Hjelper_2026-10-09.md` og
`Developer_Workbench_Formaalstre_2026-10-09.md`.
