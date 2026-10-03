Arbeidstre: `_wt-butler-maaling-20260923` @ `77a922bc`, endringer: 4 fil(er).
Grafpatch: `BUTLER-MAALING/graf/graf-v2.patch` ().
Korpusfiler: fixtures-v1.jsonl korpus-v1.jsonl
Bygg: OK (29s).
Katalog: `maaling/katalog.json` (58 konfigurasjoner, 21 dokumenter, 0 sannhetskilder).
- `fixtures-v1`: 101 meldinger → 101 resultater (22s), 0 med feil
- `korpus-v1`: 396 meldinger → 396 resultater (55s), 0 med feil
- `kallimachos-v1` (Kallimachos `matchPurposes`): 96 meldinger → 96 resultater (7s)

Regresjon (`PersonalChatPromptEvaluationTests|ButlerSignalMatcherTests|ChatPurposeResourceRouterTests`): exit 1, 92 bestått, 1 feilet.
```text
AppTests.PersonalChatPromptEvaluationTests testDeterministicPromptSuiteRoutesExpectedComponentsWithoutSideEffects
```

## Poeng («graf-v2»)

### `fixtures-v1` — 101 meldinger

| delmengde | n | top-1 (positive) | top-1 eller spurte riktig | R@3 | MRR | negativer uten handling | alt riktig |
|---|---|---|---|---|---|---|---|
| fixtures | 101 (53+/35−) | 98 % [94 %–100 %] | 98 % | 100 % | 0.99 | 100 % | 99 % |
| alle | 101 (53+/35−) | 98 % [94 %–100 %] | 98 % | 100 % | 0.99 | 100 % | 99 % |

Utfall (alle): riktig 100, spurte 1

### `kallimachos-v1` — 96 meldinger

| delmengde | n | top-1 (positive) | top-1 eller spurte riktig | R@3 | MRR | negativer uten handling | alt riktig |
|---|---|---|---|---|---|---|---|
| holdout | 21 (18+/3−) | 17 % [0 %–33 %] | 17 % | 33 % | 0.28 | 100 % | 29 % |
| trening | 75 (67+/8−) | 36 % [24 %–48 %] | 36 % | 46 % | 0.40 | 62 % | 39 % |
| alle | 96 (85+/11−) | 32 % [22 %–42 %] | 32 % | 44 % | 0.38 | 73 % | 36 % |
| enige (generator = tolk) | 93 (82+/11−) | 32 % [22 %–41 %] | 32 % | 43 % | 0.37 | 73 % | 37 % |

Utfall (alle): feil handling 42, riktig 35, stille 19

| etikett | forventet | riktig | stille | spurte | feil handling | vanligste feil |
|---|---|---|---|---|---|---|
| purpose://project-work.project-portfolio | formaal | 0/5 | 3 | 0 | 2 | purpose purpose://digital-work.coordinate ×2 |
| purpose://questionnaire.delivery.consent | formaal | 0/5 | 1 | 0 | 4 | purpose purpose://project-work.share-selected-intent ×2; purpose purpose://event.meeting.draft-request ×1 |
| purpose://self-determination.data.duration | formaal | 0/5 | 2 | 0 | 3 | purpose purpose://event.agenda.recommendation ×1; purpose purpose://self-determination.data ×1 |
| purpose://contact.introduction | formaal | 1/5 | 1 | 0 | 3 | purpose purpose://contact.followup ×1; purpose purpose://event.meeting.draft-request ×1 |
| purpose://content.review-before-publish | formaal | 1/5 | 1 | 0 | 3 | purpose purpose://source.methodology.current ×1; purpose purpose://questionnaire.responses.analyze ×1 |
| purpose://event.meeting.draft-request | formaal | 1/5 | 2 | 0 | 2 | purpose purpose://contact.followup ×1; purpose purpose://content.review-before-publish ×1 |
| purpose://project-work.share-selected-intent | formaal | 1/5 | 0 | 0 | 4 | purpose purpose://project-work.current-status-and-outstanding ×3; purpose purpose://contact.followup ×1 |
| purpose://project-work.work-items | formaal | 1/5 | 1 | 0 | 3 | purpose purpose://digital-work ×1; purpose purpose://questionnaire.respondent.form ×1 |
| purpose://questionnaire.responses.analyze | formaal | 1/5 | 1 | 0 | 3 | purpose purpose://event.privacy-preserving-networking ×1; purpose purpose://questionnaire.respondent.form ×1 |
| purpose://contact.followup | formaal | 2/5 | 1 | 0 | 2 | purpose purpose://contact.communication ×1; purpose purpose://access.audit.privacy ×1 |
| purpose://digital-work.collect-structured-input | formaal | 2/5 | 2 | 0 | 1 | purpose purpose://grounding ×1 |
| purpose://event.schedule.change-request | formaal | 2/5 | 1 | 0 | 2 | purpose purpose://questionnaire.access.audit ×1; purpose purpose://contact.communication ×1 |
| purpose://access.audit.privacy | formaal | 3/5 | 0 | 0 | 2 | purpose purpose://questionnaire.access.audit ×1; purpose purpose://event.agenda.recommendation ×1 |
| purpose://event.agenda.recommendation | formaal | 3/5 | 1 | 0 | 1 | purpose purpose://project-work.current-status-and-outstanding ×1 |
| purpose://event.privacy-preserving-networking | formaal | 3/5 | 0 | 0 | 2 | purpose purpose://contact.followup ×1; purpose purpose://contact.communication ×1 |
| purpose://knowledge.explain-policy | formaal | 3/5 | 0 | 0 | 2 | purpose purpose://test.acceptance ×1; purpose purpose://prompt.unknown ×1 |
| purpose://project-work.current-status-and-outstanding | formaal | 3/5 | 2 | 0 | 0 |  |
| none | ingen | 8/11 | 0 | 0 | 3 | purpose purpose://source.methodology.current ×1; purpose purpose://contact.communication ×1 |

Per style: indirekte 9 % (n=34), kort 35 % (n=17), negativ 83 % (n=6), normal 54 % (n=39)
Per lang: en 46 % (n=39), nb 30 % (n=57)

Eksempler på feil handling (det brukeren ville fått foreslått):

- `kl1-003` «Vi hadde et rot med noen filer i går, og nå må jeg finne ut nøyaktig hvem som rørte hva.» → purpose purpose://questionnaire.access.audit (forventet purpose://access.audit.privacy)
- `kl1-006` «Jeg lovte å ta kontakt igjen etter møtet forrige uke, men det ble aldri noe av.» → purpose purpose://contact.communication (forventet purpose://contact.followup)
- `kl1-007` «Sett meg i kontakt med henne» → purpose purpose://contact.followup (forventet purpose://contact.introduction)
- `kl1-009` «Jeg trenger noen som kjenner riktig person der borte, kan du fikse det?» → purpose purpose://event.meeting.draft-request (forventet purpose://contact.introduction)
- `kl1-010` «Sjekk teksten før vi legger ut» → purpose purpose://source.methodology.current (forventet purpose://content.review-before-publish)
- `kl1-011` «Kan du lese gjennom referatet før vi legger det ut på nettsida?» → purpose purpose://questionnaire.responses.analyze (forventet purpose://content.review-before-publish)
- `kl1-020` «Kan du skrive et utkast til møte med statssekretæren under uka?» → purpose purpose://contact.followup (forventet purpose://event.meeting.draft-request)
- `kl1-024` «Jeg vil møte flere i køen her uten at alle skal kunne se hele CV-en min på skjermen.» → purpose purpose://contact.followup (forventet purpose://event.privacy-preserving-networking)
- `kl1-027` «Timeplanen vår kolliderer med noe annet jeg må rekke, så noe må vike.» → purpose purpose://questionnaire.access.audit (forventet purpose://event.schedule.change-request)
- `kl1-030` «Jeg skjønner ikke helt hvor grensa går for hva vi faktisk får gjøre med medlemslista.» → purpose purpose://test.acceptance (forventet purpose://knowledge.explain-policy)
- `kl1-037` «Del prosjektet med Ola» → purpose purpose://project-work.current-status-and-outstanding (forventet purpose://project-work.share-selected-intent)
- `kl1-038` «Kan du sende det utvalgte prosjektet til daglig leder for gjennomsyn?» → purpose purpose://project-work.current-status-and-outstanding (forventet purpose://project-work.share-selected-intent)

### `korpus-v1` — 396 meldinger

| delmengde | n | top-1 (positive) | top-1 eller spurte riktig | R@3 | MRR | negativer uten handling | alt riktig |
|---|---|---|---|---|---|---|---|
| holdout | 100 (87+/6−) | 36 % [25 %–46 %] | 39 % | 49 % | 0.48 | 100 % | 39 % |
| trening | 296 (249+/30−) | 61 % [55 %–68 %] | 64 % | 74 % | 0.72 | 93 % | 61 % |
| alle | 396 (336+/36−) | 55 % [50 %–60 %] | 57 % | 68 % | 0.66 | 94 % | 56 % |
| enige (generator = tolk) | 373 (313+/36−) | 57 % [51 %–62 %] | 59 % | 71 % | 0.69 | 94 % | 58 % |

Utfall (alle): riktig 221, stille 79, spurte 44, feil handling 31, graf-hull 12, spurte, riktig blant valgene 9

| etikett | forventet | riktig | stille | spurte | feil handling | vanligste feil |
|---|---|---|---|---|---|---|
| H.capability | hjelper | 0/12 | 1 | 9 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×1; resource_match knowledge.demo.kallimachos ×1 |
| S.agreement | flate | 0/12 | 0 | 0 | 0 |  |
| S.commerce | flate | 0/12 | 4 | 5 | 3 | resource_match personal.chat.assist.spatial-query ×3 |
| S.meetplace | flate | 0/12 | 6 | 1 | 5 | resource_match personal.chat.assist.spatial-query ×4; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.vote | flate | 0/12 | 6 | 2 | 4 | create_poll personal.chat.assist.poll ×3; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| C.clarify | avklaring | 3/12 | 8 | 0 | 1 | project personal.chat.assist.project ×1 |
| H.todo | hjelper | 3/12 | 3 | 3 | 3 | invite_person personal.chat.assist.invite ×1; reminder personal.chat.assist.reminder ×1 |
| S.agenda | flate | 3/12 | 4 | 5 | 0 |  |
| S.docs | flate | 3/12 | 3 | 4 | 2 | resource_match purpose:Dokumentskriving og samarbeid ×1; resource_match purpose://capability.construct-cellconfiguration ×1 |
| S.music | flate | 3/12 | 8 | 1 | 0 |  |
| S.entity | flate | 4/12 | 3 | 5 | 0 |  |
| S.map | flate | 4/12 | 5 | 3 | 0 |  |
| S.networking | flate | 4/12 | 2 | 3 | 3 | resource_match personal.entity.relations.manage ×3 |
| H.poll | hjelper | 7/12 | 4 | 1 | 0 |  |
| S.mermaid | flate | 7/12 | 2 | 2 | 1 | advisory_report personal.chat.assist.advisory-report ×1 |
| S.profilepage | flate | 7/12 | 3 | 1 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.publish | flate | 7/12 | 3 | 1 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| S.admin | flate | 8/12 | 2 | 1 | 1 | todo personal.chat.assist.todo ×1 |
| H.meeting | hjelper | 9/12 | 3 | 0 | 0 |  |
| H.reminder | hjelper | 9/12 | 1 | 1 | 1 | schedule_meeting personal.chat.assist.meeting.schedule ×1 |
| G.gap | hull | 10/12 | 0 | 0 | 2 | invite_person personal.chat.assist.invite ×1; resource_match cellprotocol.docs.lookup ×1 |
| H.advisory | hjelper | 10/12 | 2 | 0 | 0 |  |
| H.invite | hjelper | 10/12 | 0 | 1 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| H.workitem | hjelper | 10/12 | 2 | 0 | 0 |  |
| S.aigateway | flate | 10/12 | 0 | 2 | 0 |  |
| S.cellconfig | flate | 10/12 | 1 | 1 | 0 |  |
| H.agent | hjelper | 11/12 | 0 | 1 | 0 |  |
| H.idea | hjelper | 11/12 | 1 | 0 | 0 |  |
| H.onboarding | hjelper | 11/12 | 1 | 0 | 0 |  |
| H.video | hjelper | 11/12 | 1 | 0 | 0 |  |
| H.project | hjelper | 12/12 | 0 | 0 | 0 |  |
| M.meta | meta | 12/12 | 0 | 0 | 0 |  |
| N.none | ingen | 12/12 | 0 | 0 | 0 |  |

Per style: dialekt 64 % (n=11), indirekte 45 % (n=132), kort 70 % (n=99), lang 30 % (n=33), normal 66 % (n=102), skrivefeil 38 % (n=8), to-behov 55 % (n=11)
Per lang: en 61 % (n=132), nb 53 % (n=264)

Eksempler på feil handling (det brukeren ville fått foreslått):

- `k1-0039` «hver gang jeg skal dele et kart med en kunde må jeg ta skjermbilde, det er jo tungvint» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.capability)
- `k1-0044` «hvordan funker egentlig autentisering mellom celler, finnes det noe dokumentert» → resource_match purpose:Dokumentskriving og samarbeid (forventet S.docs)
- `k1-0056` «kan du gjøre det nye prosjektet synlig offentlig på haven» → resource_match knowledge.demo.kallimachos (forventet S.publish)
- `k1-0074` «kan du finne et sted vegar og jeg begge kan komme oss til for lunsj» → resource_match personal.chat.assist.spatial-query (forventet S.meetplace)
- `k1-0075` «jeg er på sentrum, victoria er på tyholt, må jo møtes et sted midt imellom» → resource_match personal.chat.assist.spatial-query (forventet S.meetplace)
- `k1-0083` «kan jeg stemme på forslaget om havneutbyggingen her i appen» → create_poll personal.chat.assist.poll (forventet S.vote)
- `k1-0093` «det der prosjektet, du vet, bare gjør det ferdig» → project personal.chat.assist.project (forventet C.clarify)
- `k1-0101` «Jeg satt og pratet med en hyggelig dame fra Arbeiderpartiet i dag, og vi ble enige om at h» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.invite)
- `k1-0115` «Legg til at jeg må huske å ringe rektor i morgen.» → invite_person personal.chat.assist.invite (forventet H.todo)
- `k1-0118` «Kan du minne meg på klokka ni i morgen om at jeg skal møte ordføreren?» → schedule_meeting personal.chat.assist.meeting.schedule (forventet H.reminder)
- `k1-0167` «Vi har hørt at flere i kommunen har opplevd at tjenestene har vært trege den siste uka. So» → todo personal.chat.assist.todo (forventet S.admin)
- `k1-0172` «Kan du foreslå et sted hvor jeg og Anne kan møtes for kaffe?» → resource_match personal.chat.assist.spatial-query (forventet S.meetplace)

Full rapport per id: `rapport/graf-v2/rapport-2026-09-24-graf-v2.json`
