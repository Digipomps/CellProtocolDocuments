# BRIEF til uavhengig gransking: utsettingen 30.09, fornyelsen av Vegars tilgang og svaret til Vegar

Du er «Fabel», en uavhengig gransker. Du skal ikke være enig for å være hyggelig. Finn det som er galt, mangler, eller er påstått uten belegg. Svar på norsk. Du skal bare lese filer i denne mappen, ikke endre noe og ikke kontakte noe utenfor.

## Bakgrunn

Kjetil eier HAVEN. «Losen» er en Claude-tråd som arbeider for ham. Flere tråder (Claude og Codex) arbeider i samme repoer og mot samme staging-vert. En annen Claude-tråd administrerer deploykøen (`HAVEN-Deploy`, `_losen-queue/KOORDINERING.md`).

30.09 hadde Kjetils korrespondansetilgang gått ut, og kollegaen Vegar fikk `recipient_not_allowed`. Losen bygde fornyelse av utløpt tilgang (commit `415ea3d2`), Kjetil sa «Ja, sett ut nå», og Losen satte den ut på staging samme kveld. 01.10 valgte Kjetil også fornyelse de siste sju dagene før fristen (commit `06f32050`, PR 277 mot `main`, ikke satt ut). 02.10 fant Losen deploykøens koordineringsregler for første gang.

Vegar har bedt om å få fornyet sin egen tilgang (`vegar-local-agent`) før den går ut 08.10. Victorias tilgang (`victoria-lille-robot`) har alt gått ut.

## Bevisene (alle i denne mappen)

- `E1-kildediff-feec2372-til-d83d9f6b.diff`: alt fornyelsen endret i kildene (ikke testene).
- `E2-utsetting-30-09-jobblogg.txt`: jobbloggen fra utsettingen, og målinger 02.10.
- `E3-kildeutdrag-invitasjoner-og-klient.txt`: utdrag fra server- og klientkilder, prosjektminnet, testresultater og Vegars meldinger.
- `E4-koordinering-del2-og-board.log`: `hd coord status`, køens tavle, siste del av `KOORDINERING.md`, disk og staging-helse.
- `E5-les-meg-og-koordinering-del1.log`: `_losen-queue/LES_MEG.md`, første del av `KOORDINERING.md` (reglene 1–6 og tabellen «Nå»), `runner.sh`.
- `E6-hd0141-og-staging-sha.log`: oppgaven HD-0141, hendelser, og hva køen tror står på staging.

## Det Losen har tenkt å si til Kjetil

Prøv hver påstand mot bevisene. Si for hver: holder, holder ikke, eller kan ikke belegges herfra.

- **K1.** Utsettingen 30.09 brøt regel 5 i `KOORDINERING.md`: den ble gjort uten egen claim, mens HD-0141 hadde claim på `cellscaffold-app-1` og nginx. Containeren ble startet på nytt minst to ganger.
- **K2.** Deploykøen tror staging kjører `feec2372`. Staging kjører `415ea3d2`.
- **K3.** Om utsettingen forstyrret HD-0141 sitt arbeid (blant annet byggbindingen), er ukjent.
- **K4.** Lagret tilstand er forenlig begge veier: en utgivelse uten fornyelseskoden leser tilstanden som `415ea3d2` har skrevet, og omvendt.
- **K5.** Utgivelsen 2026.9.4 (`fdcfe7a5`) har ikke fornyelseskoden. Settes den ut på staging før PR 277 er med i en utgivelse, slutter fornyelse av utløpte tilganger å virke der.
- **K6.** Enhver fornyelse (Vegar, Victoria) krever en fersk invitasjon i stagings miljøvariabel, og det betyr at containeren startes på nytt. Det er altså en vertsendring som trenger claim, og den kan ikke gjøres mens HD-0141 sin claim står.
- **K7.** Med det som står på staging nå (`415ea3d2`), kan en tilgang bare fornyes etter at den har gått ut. Fornyelse før fristen krever `06f32050`.
- **K8.** Invitasjonen må bære mottakerens enhets-ID, og den kjenner bare mottakeren selv (og serverens lagrede tilgang, som eieren ikke har noen flate for å lese).
- **K9.** Lokale Swift-bygg 30.09 og 02.10 gikk utenom `scripts/run_swift_bounded.sh` og diskregelen (regel 1 og 2).

## Det Losen har tenkt å gjøre og anbefale

- **A1.** Føre avviket inn i `KOORDINERING.md` som en egen rad (når Macen er tilbake), slik fila ber tråder om. Ikke gjøre flere vertsendringer selv.
- **A2.** Levere neste vertsendring (fornyelseskoden pluss invitasjoner for Vegar og Victoria) til deploykøen som én beskrevet jobb. Kø-tråden setter rekkefølgen, og Kjetil avgjør hvem som utfører.
- **A3.** Be Kjetil merge PR 277 når CI er grønn, slik at fornyelsen kommer med i neste utgivelse.
- **A4.** Svare Vegar nå (utkast under). Sending krever Kjetils ja.

## Utkast til svar til Vegar

> Hei Vegar,
>
> Takk for begge meldingene. Write-a-skill-meldingen kom fram, både den fra 29.09 og den dere sendte på nytt.
>
> **Fornyelsen.** Ja, vi fornyer tilgangen deres. Tre ting må du vite først:
>
> 1. Jeg trenger enhets-ID-en til profilen deres. Invitasjonen må bære den samme ID-en som dere meldte dere inn med, ellers avviser serveren den som en ny enhet. Kjør `haven-correspondence-mcp identity --profile <profilen deres>` og send meg `deviceID`. Viser kommandoen når tilgangsbeviset går ut (`expiresAt`), så send det også. Da vet vi klokkeslettet 08.10.
> 2. Klienten har ikke noe gyldig bevis fra dere kjører `setup` med den nye invitasjonen til Kjetil har godkjent og dere har kjørt `activate`. Vi avtaler derfor et tidspunkt der Kjetil sitter klar. Da er dere uten tilgang i noen minutter.
> 3. Invitasjonen må legges inn på staging, og det krever en omstart som står i kø bak et annet arbeid på verten. Jeg vet ikke ennå når det blir. Blir det ikke før 08.10, går tilgangen deres ut, og vi fornyer den rett etterpå. Den veien virker i dag. Det var slik Kjetils tilganger ble fornyet 30.09.
>
> Jeg sier fra når invitasjonen er klar, med forslag til tidspunkt.
>
> **bcd45de.** Vi har målt det samme som dere: commiten ligger bare på grenen `arendalsuka-navigationbar-icon-support` i CellProtocol. Den er ikke med i 2026.9.3 eller 2026.9.4 og ikke på `main`. CellScaffold `main` bruker ikke `icon:` ennå, så `main` bygger. Det er grenen deres som ikke bygger mot den pinnede utgivelsen. Kjetil har bestemt at endringen tas inn gjennom en egen formålsrunde, med tester mot både funksjon og formål før den går til `main` i CellProtocol. Runden er ikke startet ennå. Jeg melder fra når den er i gang.
>
> — Losen, for Kjetil

## Spørsmålene

- **P1.** Hvilke av K1–K9 holder ikke, eller er sterkere formulert enn bevisene tillater? Vær særlig streng med K4 (les diffen selv) og K6.
- **P2.** Finnes det en vei til å fornye Vegar og Victoria som Losen ikke har sett, og som er mindre inngripende enn en omstart av containeren, eller som ikke venter på HD-0141? Skill mellom det du kan belegge og det du gjetter.
- **P3.** Er A1–A4 riktig rekkefølge og riktig eierskap etter reglene i `KOORDINERING.md`? Hva bør Losen ikke gjøre selv? Er det noe i A1 som kan lage mer rot (for eksempel samtidig skriving i fila)?
- **P4.** Les utkastet til Vegar som mottaker. Lover det noe som ikke kan holdes? Er noe uklart, feil eller unødvendig? Mangler noe Vegar trenger for å gjøre sin del?
- **P5.** Hva er den største risikoen de neste seks dagene som ikke står i K1–K9?

## Svarformat

For hvert spørsmål: konklusjon først (én setning), deretter belegget. Hver påstand om bevisene merkes `[belagt: fil:linje]`. Det du ikke fant belegg for, merkes `[ikke belagt]`. Avslutt med tre korte lister: «Må rettes før Kjetil får dette», «Bør rettes», «Kan vente». Hold svaret under 700 ord per spørsmål.
