# HAVEN: intern kvalitets- og modenhetsvurdering

Dato: 2026-08-09
Status: internt arbeidsgrunnlag, ikke en markeds- eller produksjonsklarhetspåstand

## 1. Konklusjon

HAVEN er en stor og ujevnt verifisert kode- og dokumentasjonsbase. Enkeltdeler
har sterke kontrakter, tester og driftsprosedyrer, mens andre sentrale flater
mangler kontinuerlig testkjøring eller uavhengig interoperabilitetsbevis. Det er
derfor ikke kildegrunnlag for å klassifisere hele systemet som
«produksjonsklart» eller som én samlet alfa-/beta-fase.

Den mest forsvarlige prioriteringen er å lukke brukerblokkerende og
integritetskritiske feil, gjøre lokale testgater reproduserbare mens GitHub
Actions er kontoblokkert, og bevise minst én kryssruntime-kontrakt før den
offentlige begrepsflaten utvides videre.

## 2. Metode og evidensstatus

Dette dokumentet bruker tre evidensnivåer:

- **Kjørt i denne integrasjonen:** kommandoen ble kjørt fra det oppgitte
  arbeidstreet og resultatet kan gjentas.
- **Rapportert snapshot:** tallet eller utfallet kommer fra et navngitt lokalt
  dokument eller en tidligere kommandologg. Det kan være korrekt for den
  testede revisjonen, men er ikke nødvendigvis dagens tilstand.
- **Vurdering:** en begrunnet tolkning som må holdes adskilt fra måleresultatet.

Følgende er kjørt i denne integrasjonen:

- `node Tools/PurposeKnowledge/evaluate_purpose_cases.mjs`
- JSON-parse av den genererte evalueringsrapporten
- dokument- og diffkontroll

Følgende er ikke kjørt på nytt som del av denne integrasjonen:

- full `swift test` i CellProtocol, CellScaffold eller Binding
- full Playwright-suite mot staging
- produksjons- eller staging-deploy
- tilgjengelighet og innhold på offentlige verter

## 3. Snapshot av omfang og testflater

Tidligere lokal opptelling 2026-08-09 rapporterte følgende. Linjetall er
omfangsindikatorer, ikke kvalitetsmål, og språk-/generatorforskjeller gjør dem
uegnet som direkte sammenligning mellom repoer.

| Repo | Rapportert kildelinjer | Rapportert testlinjer | Rapportert testfunksjoner | Evidensmerknad |
| --- | ---: | ---: | ---: | --- |
| CellProtocol | 101 063 | 42 784 | 932 | tidligere lokal opptelling og testkjøring |
| CellScaffold | 315 637 | 114 879 | 1 960 | tidligere lokal opptelling; full suite ikke kjørt her |
| Binding | ca. 138 000 totalt | blandet i treet | 436 | tidligere lokal opptelling; full suite ikke kjørt her |
| PyCellProtocol | 4 646 | ikke oppgitt | ikke oppgitt | omfangstall alene |
| GoCellProtocol | 5 661 | ikke oppgitt | ikke oppgitt | omfangstall alene |
| RustCellProtocol | 6 803 | ikke oppgitt | ikke oppgitt | omfangstall alene |

En tidligere opptelling rapporterte også 35 bokkapitler, 9 maskinlesbare
kontrakter og 57 formål i kunnskapsbasen. Disse tallene viser bredde, men ikke
at innholdet er komplett, korrekt eller implementert.

Formålsevalueringen ble kjørt på nytt i denne integrasjonen. Den deterministiske
suiten har 56 fixtures. Resultatet i
`Tools/PurposeKnowledge/results/latest-purpose-eval.json` er den autoritative
maskinlesbare rapporten for denne kjøringen.

## 4. Kvalitetsfunn per lag

### CellProtocol

Tidligere lokal kjøring rapporterte grønn Swift-suite, og repoet har
wire-fixtures og resolverbasert autorisasjonslogikk. Dette er relevant positiv
evidens for den testede Swift-implementasjonen.

Det beviser ikke i seg selv protokollinteroperabilitet. Et sterkere bevis krever
at minst én uavhengig runtime leser og skriver de samme normative fixturene og
at avvik feiler lukket.

### CellScaffold

Det store antallet rapporterte tester er positivt, men verdien reduseres når
de ikke kjøres kontinuerlig. GitHub Actions-kjøringer ble 2026-08-08/09 observert
stanset før jobbstart av konto-/spending-limit-status. Det er en blokkering i
verifikasjonsinfrastrukturen, ikke bevis på kodefeil eller kodekvalitet.

Inntil kontoen kan rettes, skal en lokal workaround dokumentere nøyaktig commit,
kommandoer, miljøforutsetninger og resultater i hver berørt PR. Den workarunden
erstatter ikke langsiktig CI.

`CellScaffold/Documentation/Operations/Staging_Surface_Test_Report_2026-08-09.md`
rapporterer 38 passerte, 69 feilede og 12 ikke-kjørte Playwright-tester på den
revisjonen rapporten undersøkte. Rapporten beskriver blant annet atomisk
skeleton-swap og førstegangsprovisjonering som blokkerende funn. Disse funnene
skal behandles som revisjonsspesifikke regressjoner og verifiseres på nytt etter
fiks; de skal ikke omtales som uforanderlige egenskaper ved dagens deployment.

### Binding

Tidligere opptelling viser en betydelig testflate, men full suite og en
reproduserbar CI-gate er ikke etablert i dette vurderingsarbeidet. Siden Binding
er en direkte brukerflate, er dette et verifikasjonsgap som bør lukkes med en
avgrenset bygg-/testmatrise og dokumenterte plattformkrav.

### Dokumentasjon og formålskunnskap

Maskinlesbare kontrakter, navngitte Goals, success signals og verifikatorer gjør
dokumentasjonen mer testbar enn ren prosatekst. 56/56 i den deterministiske
formålssuiten viser at dagens resolver matcher dagens fixtures. Det viser ikke
at fixture-settet dekker virkelige brukere, motstridende interesser eller alle
språkvarianter.

### Drift

Repoene beskriver immutable images, readiness-gater, rollback og restore-proof.
Dette er relevante kontrollmekanismer. At prosedyrene finnes er likevel ikke
tilstrekkelig til å erklære tjenesten produksjonsklar; en slik vurdering krever
ferske deploy-/restore-bevis, observerbarhet, hendelseshåndtering og definerte
tjenestenivåer på den konkrete revisjonen.

## 5. Sammenligning med andre økosystemer

Solid, AT Protocol, MCP og dataspace-initiativer kan brukes som
orienteringspunkter, men de løser ulike problemer og har ulikt modenhets- og
styringsgrunnlag. Denne vurderingen gjør derfor ingen rangering av at HAVEN er
«rikere», «bedre» eller «mer disiplinert» enn dem.

En etterprøvbar sammenligning bør dele opp påstandene i minst:

- normativ spesifikasjon og konformanstest
- antall uavhengige interoperable implementasjoner
- identitets-, autorisasjons- og policygrenser
- styring, lisens og bidragsmodell
- dokumentert utrulling og brukerbevis

`Beslektede_Prosjekter_Brukerkontroll_Sammenligning_2026-08-09.md` er et
arbeidsgrunnlag for denne analysen, ikke en autoritativ markedsmåling.
Tidsfølsomme tall om brukere, apper, servere, stjerner, forks eller bidragsytere
skal ha dato og primærkilde før de publiseres.

## 6. Formålsgrafen: styrker og åpne hypoteser

Formålsgrafen knytter formål til observerbare Goals og verifikatorer. Det er en
konkret styrke fordi påstander om fremdrift kan knyttes til tester eller andre
navngitte bevis.

Tre åpne hypoteser bør undersøkes, ikke presenteres som ferdige funn:

1. **Motpart/adopsjon:** Grafen kan være sterkere på eierens og systemets mål
   enn på insentivet og integrasjonskostnaden for tjenesten eller virksomheten
   som må delta. Hypotesen bør testes ved å kartlegge alle aktive formål og
   intervjue minst én mulig mottaker.
2. **Kontinuitet:** Etterprøvbarhet mens én operatør er tilgjengelig dekker ikke
   nødvendigvis eksport, overtakelse eller gjenoppretting hvis operatøren
   forsvinner. Det trengs et eksplisitt kontinuitetsmål med restore-bevis.
3. **Kostnad:** `purpose://self-determination.data.exercisability` beskriver
   kontroll uten kostnad for personen. Grafen bør også navngi hvem som bærer
   utviklings-, lagrings- og verifikasjonskostnaden og hvordan kostnaden måles.

Statusverdier som `candidate` betyr at et formål er modellert, ikke at utfallet
er implementert eller oppnådd.

## 7. Modenhetsvurdering

Modenhet bør gis per avgrenset leveranse, ikke som én etikett for hele HAVEN:

| Område | Forsvarlig vurdering 2026-08-09 | Hva som mangler for neste nivå |
| --- | --- | --- |
| Swift protokollkjerne | omfattende intern implementasjon med rapportert testbevis | fersk full gate og uavhengig fixture-paritet |
| Scaffold-brukerflater | aktiv utvikling med rapporterte blocker-feil | grønne lokale/CI-gater og nye staging-bevis |
| Binding | aktiv utvikling, utilstrekkelig kontinuerlig verifisert her | reproduserbar plattformmatrise |
| Dokumentasjon/formål | omfattende og delvis maskintestbar | kildeproveniens, bruker-/motpartsvalidering |
| Drift | prosedyrer og operatørstyrte produksjonsflater finnes | ferske restore-, rollback- og SLO-bevis |
| Økosystem | ingen interoperabilitet dokumentert i denne vurderingen | ekstern eller uavhengig runtime/connector |

## 8. Prioritert rekkefølge

1. Reproduser og lukk førstegangsprovisjonering og atomisk skeleton-swap på
   nøyaktig målrevisjon.
2. Dokumenter lokale PR-gater mens GitHub Actions er kontoblokkert; gjenopprett
   kontinuerlig CI når konto-/spending-limit kan rettes.
3. Kjør én ikke-Swift-runtime mot normative Swift-fixtures og gjør avvik til
   blokkerende testfeil.
4. Etabler en avgrenset Binding-bygg-/testmatrise.
5. Legg til målbare kontinuitets-, motparts- og kostnadsmål i formålsgrafen når
   hypotesene er validert.
6. Avklar lisens for hvert offentlig repo. Fravær av eksplisitt lisens betyr
   normalt at gjenbruksrettigheter ikke er gitt, men valg av lisens og
   rettighetshavere er en eier-/juridisk beslutning og skal ikke automatiseres.

## 9. Grunnlag og begrensninger

- `CellScaffold/Documentation/Operations/Staging_Surface_Test_Report_2026-08-09.md`
- `Beslektede_Prosjekter_Brukerkontroll_Sammenligning_2026-08-09.md`
- `Book/haven_purpose_knowledge_base_v0.json`
- `Tools/PurposeKnowledge/fixtures/purpose_eval_cases.v0.jsonl`
- `Tools/PurposeKnowledge/results/latest-purpose-eval.json`

Rapporterte tellinger og tidligere testresultater må beholdes med revisjon og
kommandologg for å kunne oppgraderes til «kjørt i denne integrasjonen». Ingen
påstand i dette dokumentet alene godkjenner deploy, produksjonsklarhet,
regulatorisk status eller lisensvalg.
