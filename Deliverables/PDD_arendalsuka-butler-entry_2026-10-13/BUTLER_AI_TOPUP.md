# Butler: språkmodellvalg og kjøpt AI-bruk

Status 2026-10-13. Kildeaudit og avgrenset retting, ikke deployet eller akseptert brukerflyt.

## Brukerens bestilling

> Vi må ha en god opplevelse med å knytte til en språkmodell til Butler chat. Når det dukker opp spørsmål basis butleren ikke klarer å tolke bør brukeren få forslag om å enten koble til en DiMy eid ai agent celle - kan være eid av meg når vi starter - eller kjøre igjennom oppsettet til ai agent cellen og legge inn egen api nøkkel. Jeg vil teste å gi Vegar en topup så han - og jeg når jeg tenker etter - kan sjekke hvordan det føles når man får spørsmål om å bruke eller sette opp en språkmodell i chat-en.

> Faktisk betalt saldo – avklar beløp før overføring

> Jeg kan f.eks godkjenne 100 kr så ser vi hvor langt vi kommer.

100kr er foreslått. Spørsmål om100kr totalt/50kr hver eller100kr hver er sendt og avventer svar. Ingen checkout, overføring, debitering eller tildeling er utført.

## Ønsket opplevelse — ennå ikke implementert

Når basis-Butler ikke tolker spørsmålet, behold spørsmålet og vis:

«Jeg trenger en språkmodell for å hjelpe med dette. Hvordan vil du fortsette?»

1. **Bruk DiMys AI-agent** — vis faktisk eier, modell, hvilke data som sendes, tilgjengelig brukskvote og kostnadsramme. Kjetils celle kan være første tilbud, men må identifiseres og gi gyldig tilgang til hver bruker.
2. **Sett opp egen språkmodell** — veiledet leverandør/modell → alias → separat hemmelig API-nøkkelfelt. Ikke legg hemmeligheten i chatlogg, sourceText, analyse eller dry-run.
3. **Fortsett uten språkmodell** — behold basis-Butler og spørsmålet.

Tilkobling er ikke samtykke til å sende hele samtalen eller automatisk betale. Etter oppsett/tilkobling kommer brukeren tilbake til det opprinnelige spørsmålet. Før første modellkall vises avgrenset tekst, mottaker og kostnad. Avbryt skal gi null kall og null trekk. Ingen automatisk påfylling.

## Kildeaudit

Codex hovedtråd leste relevante utsnitt av CellScaffold-kandidat2b65ca570bb4ec1e3b4be5b7102df6227d3e71d4. Uavhengig leser native_entry_review leste også installert Binding-revisjonc61629124b4a841db5217e442b23bbcd756a7055. Dette er ikke en fullstendig audit av alle filer.

| Del | Verifisert kilde | Hva den ikke beviser |
|---|---|---|
| Egen modell | CellScaffold/Sources/App/Cells/PersonalCopilot/GuidedOnboardingCell.swift: connect-language-model-v1 har provider, alias og secret-steg | Ikke lokal HAVEN-implementasjon eller faktisk sikker GUI-inntasting |
| Modellvalg på web | PersonalCopilotCloudStore.swift og PersonalCopilotCells.swift: provider register/select/confirm/invoke, samtykke og tillitspakke | Ingen operativ delt celle eller fungerende purpose-bound-payload |
| Delt agent | AIGatewayCell.swift: purpose-bound invoke krever full AIGatewayInvokeRequest og purposeBoundIntent | Generisk chat-payload ved CloudStore providerActionPayload gir ikke denne kontrakten |
| Kjøpt brukskvote | VaporPaymentResolution.swift, PaymentResolutionSupport.swift og TopUpCheckoutSupport.swift: beløpspakker inkluderer50kr/100kr; checkout knyttes til autentisert bruker og resourceID | Ingen dokumentert sponsorbetaling for en annen bruker |
| Native Butler | Binding/Binding/BootstrapView.swift og ChatWorkbenchParityCells.swift ved installertc6162912 registrerer lokal BindingPersonalChatHubCell | Serverdeploy erstatter ikke denne koden |
| Native modell | BindingRemoteLLMCell.swift vedc6162912 bruker RemoteLLM og prosessmiljønøkkel | Ikke tilkoblet DiMy-kvote eller gateway-onboarding |

En provider-descriptor gir oppdagelse, ikke Agreement, fungerende invoke-payload eller penger.

## Betalingsklassifisering og målt konfigurasjon

Eksisterende kjøpsmodell er ekstern betaling til DiMy for bruker-/ressursbundet brukskvote. Kildepolicy tillater ikke overførbar saldo, cash-out eller betaling til vilkårlig merchant. Å kjøpe brukstilgang til Vegar krever eksplisitt skille mellom betaler og mottaker; det kan ikke løses ved å skrive Vegar som betalingsmottaker i dagens checkout. Dette er kildeanalyse, ikke juridisk vurdering.

Lesende SSH-kontroll denne økten:

- Staging: Stripe secret-/webhook-variabler og filstier fraværende.
- Produksjon: nøkkelstier finnes, STRIPE_TOPUP_ENABLED erfalse. Filinnhold matcher ikke forventet Stripe live/test-prefix eller webhook-prefix. Ingen hemmeligheter skrevet til logg.
- Ingen betalingskonfigurasjon eller saldo er endret. Ingen live betalingsprosessortest gjennomført.

Stripe krever verifisert betalingsstatus før levering; retur til suksesside alene er utilstrekkelig: https://docs.stripe.com/checkout/fulfillment . Automatiserte betalingsprøver må bruke Stripe sitt testmiljø: https://docs.stripe.com/testing . Et eventuelt ekte kjøp fra Kjetil er separat fra automatiske testtransaksjoner.

## Avgrenset retting som er skrevet

Separat gren codex/butler-model-connection-20261013 bygger på den frosne onboarding-kandidaten. PersonalCopilotCloudStore velger nå connect-language-model-v1 for eksplisitt modelltilkobling og BYOK, med korrekt visningstittel og summary. Eksplisitt Arendalsuka-inngang beholder prioritet. Sju tilfeller er lagt til eksisterende PersonalCopilotV1Tests, inkludert nøkkelvarianter og eksplisitt lokal modell.

Swift frontend parse og git diff --check bestått. Testene er ikke kjørt. Rettingen er ikke committet, deployet eller bevis på hele ønsket flyt.

## Tester som må bli grønne før brukerforsøk

| Brukerutfall | Påkrevd bevis |
|---|---|
| No-match tilbyr begge modellveier | Faktisk klikkreise i web og installert HAVEN, uten modellkall før valg |
| Kjetils/DiMys delte celle virker for begge | Verifisert celleeier, separat Agreement/requester for hver bruker, godkjent route og formålsbundet request |
| Egen nøkkel er trygg | Hemmelig input er maskert og fraværende fra state/dry-run/chatlogg; lagring under riktig eier |
| Opprinnelig spørsmål bevares | Tilbake fra begge oppsett uten å sende spørsmålet automatisk |
| Reelt kjøp leverer riktig kvote én gang | Riktig betaler/mottaker/ressurs/beløp, signert betalt webhook, durable receipt og replay uten dobbeltkreditering |
| Kall har avgrenset kostnad | Pris/ramme før godkjenning, saldoavlesning etter kall, avbrudd og providerfeil gir korrekt nulltrekk/rollback |
| Native og web er private | Separate identiteter og friske sesjoner; ingen felles eier brukt som snarvei |

## Opprinnelig onboarding-oppdrag

HD-0224 fortsetter. Én godkjent GitHub-kjøring er startet på eksakt2b65ca57:
https://github.com/Digipomps/CellScaffold/actions/runs/38411283520 . Sist observert: Build every target pågår. Ingen ny CI-kjøring er startet for modellrettingen.

Native Library er låst opp, men faktisk lasting av ArendalsukaParticipantProgram feiler med signContract-avvisning selv med tilkoblet Bridge. Kildeaudit peker på vertseid lookup mot identityUnique-celle; årsaken må bevises med målrettet test før retting. Den valgfrie kunnskapsbasen er fortsatt deaktivert og database mangler; kuratert onboarding-taksonomi er separat.


## Klikkbar skisse

`butler-model-preview/index.html` og `butler-model-preview/choice.png` viser forslag til chatvalg. Dette er en selvstendig HTML-mockup, ikke dagens Skeleton eller native HAVEN. Nettleserklikk gjennom delt agent, egen nøkkel, avbryt og lokal fortsettelse bestod. Passordfelt er readonly eksempeldata; ingen reelle nøkler tas imot.390px-visning har ingen horisontal overflow. `butler-model-preview/result.json` dokumenterer avgrensningen. Ingen G1-GUI-godkjenning er gitt.
