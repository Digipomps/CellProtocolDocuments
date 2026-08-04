# HAVEN-infosiden: formål, beslutninger og overlevering

Dato: 1. august 2026  
Omfang: offentlig nettsted under `Website/`  
Grunnlag: ekstern Claude-vurdering, kanonisk HAVEN-dokumentasjon, offentlig kode, primærkilder og tre uavhengige rådgivergjennomganger.

## Formål

### purpose://human-agency

En leser skal etter første skjerm kunne forklare at HAVEN undersøker digitale verktøy med mennesket som utgangspunkt, og kunne velge mellom en kort forklaring, et konkret bevis og en teknisk fordypning.

Mål:

- Første skjerm sier hvem HAVEN er for, hva som undersøkes og hva som ikke er ferdig.
- Tre innganger ender i forskjellige, konkrete neste steg.
- Statusfeltet skiller kode/test, prototyper og forskning.

Validering: strukturell og visuell kontroll i nettleser er påkrevd før publisering. En ekstern lesertest gjenstår.

### purpose://content.review-before-publish

Ingen offentlig påstand skal være sterkere enn kilden, testen eller modenhetsstatusen tillater.

Mål:

- Tekniske egenskaper peker til konkret kode eller test.
- Samfunnseffekter omtales som hypoteser eller forskningsretning.
- Implementert, testet, prototype, pilot og retning brukes som forskjellige tilstander.
- Motargument og begrensning står nær store påstander.

Validering: påstandsoversikt, målrettede komponenttester og tekstpålitelighetsanalyse.

Den deterministiske analysen fant ingen retoriske pressmønstre etter revisjon. Ti av tolv påstander fikk konkrete kildeankre; de to gjenværende er uttrykkelig merket som henholdsvis intern prototype og intern forskningsspesifikasjon uten offentlig effektbevis. Eksterne lenker krever fortsatt menneskelig kildeverifisering, som ble gjort separat i denne revisjonen.

### purpose://source.methodology.current

Kilder skal ligge nær påstanden, være daterte og skille ekstern problemforståelse fra HAVENs eget bevis.

Mål:

- Primærkilder brukes for standarder og organisasjonsdata.
- Kodebevis festes til en commit.
- Revisjoner og feil føres offentlig.

## Beslutninger etter Claude-rapporten

| Råd | Beslutning | Begrunnelse |
|---|---|---|
| Gjør agent-delegering til hovedfortelling | Moderert | Relevant brukssituasjon, men ikke dokumentert ende til ende og ikke HAVENs rotformål. Fikk egen artikkel og plass i førstesiden som bruksretning. |
| Definer målgrupper og neste steg | Innført | Tre innganger for utvikler, sikkerhetsansvarlig og eier av brukerreise. |
| Vis konkret bevis | Innført | Egen side med fire reproduserte komponenttester og festet commit. |
| Sammenlign med standarder | Innført | Nøytral matrise for OAuth/MCP, Verifiable Credentials, AuthZEN og CellProtocol. |
| Publiser organisasjon, personvern og rettelser | Innført | Egne sider; organisasjonsdata kontrollert i Brønnøysundregistrene. |
| Gi artiklene egne URL-er | Innført | 16 artikler med egen metadata og canonical-lenke; gamle fragmentlenker videresendes i klienten. |
| «OAuth støtter bare ett hopp» | Avvist | For grovt og ikke kildeholdbart. |
| «MCP fikk OAuth først i 2026» | Avvist | Feil tidsfesting og irrelevant som konkurransepåstand. |
| «Ingen utrullet protokoll støtter delegeringskjeder» | Avvist | Udokumentert absolutt påstand. |

## Viktige avgrensninger

- En kryptografisk signatur binder signert innhold til en nøkkel. Koblingen til person eller institusjon krever eget tillitsgrunnlag.
- En Agreement er en forespørsel eller mal; en Contract representerer faktisk, avgrenset autoritet.
- Resolveren er den tiltenkte håndhevingsgrensen, men hver integrert brukerreise må bevise at alle relevante handlinger faktisk går gjennom den.
- Konferanse-, profil- og tilgangsflater omtales som interne prototyper eller testscenarier. Den integrerte identitetsreisen er ikke klar for offentlig pilot.
- Demokrati, produktivitet og verdifordeling omtales som hypoteser eller forskning. Ingen ekstern effekt er dokumentert.
- Reelle betalinger skal i en eventuell første pilot håndteres av etablert betalingsleverandør. Intern verdi skal ikke gjøres overførbar, uttakbar eller allment anvendelig uten egen juridisk rute.

## Rådgiverinnspill

- Argumentgjennomgang: anbefalte tydelig verdiforslag, statusnærhet, motargument og ett bevisbart eksempel.
- Kilderevisjon: verifiserte organisasjonsdata, offentlig commit, testlinjer og standardkilder; avviste tre agent-relaterte absolutter.
- UX- og tilgjengelighetsgjennomgang: anbefalte egne artikkel-URL-er, brukbar navigasjon uten JavaScript, tastaturstøtte, større treffområder og målgruppetilpassede innganger.

## Bevis

Offentlig commit: `79740304167aa4f4daadd148c5a369e919d25a6a`

Reprodusert 1. august 2026:

- `testNonOwnerDeniedWithoutContract`
- `testNonOwnerAllowedWithSignedContract`
- `testRequesterCannotEscalateAgreementBeyondCellTemplate`
- `testStoragePermissionRequiresExplicitIdentityBoundSGrant`

Resultat: 4 tester, 0 feil. Dette er komponentbevis, ikke CI-, drifts- eller ende-til-ende-bevis.

## Åpne oppgaver

| Oppgave | Eier | Ferdig når |
|---|---|---|
| Offentlig rolle- og beslutningsoversikt | Stiftelsen Digipomps | Roller, habilitet og beslutningsvei er publisert. |
| Finansiering og interessekonflikter | Stiftelsen Digipomps | Datert oversikt er tilgjengelig fra `/om/`. |
| Retensjon for serverlogger | Drift | Faktisk lagringstid, tilgang og sletting er dokumentert og kontrollert. |
| Ekstern pilot | Produkt/identitet | Avgrenset flyt, identitetshåndtering, samtykke, testbevis og måleplan er godkjent. |
| Engelsk versjon | Redaksjon | Norsk påstandsgrunnlag er stabilt og oversettelsen er faglig kontrollert. |
| Lesertest | Redaksjon | Minst fem relevante lesere kan forklare idé, status og neste steg uten muntlig hjelp. |

## Lukkekriterium

Revisjonen er ferdig når internlenker, HTML/JS, mobil- og desktopvisning, kildehenvisninger, sikkerhetsheadere og den publiserte versjonen er kontrollert; åpne styrings- og pilotelementer skal forbli synlige som åpne oppgaver.
