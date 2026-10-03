STATUS: LEVERT — målt («graf-v3-k2»); se maaling/rapport/graf-v3-k2/

# Måling «graf-v3-k2» — Butlers AI-løse vei

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-butler-maaling.sh graf-v3-k2` 2026-09-24T02:43:29Z.

Arbeidstre: `_wt-butler-maaling-20260923` @ `77a922bc`, endringer: 4 fil(er).
Grafpatch: `BUTLER-MAALING/graf/graf-v3-k2.patch` ().
Korpusfiler: fixtures-v1.jsonl korpus-v1.jsonl korpus-v2.jsonl
Bygg: OK (29s).
Katalog: `maaling/katalog.json` (58 konfigurasjoner, 21 dokumenter, 0 sannhetskilder).
- `fixtures-v1`: 101 meldinger → 101 resultater (19s), 0 med feil
- `korpus-v1`: 396 meldinger → 396 resultater (55s), 0 med feil
- `korpus-v2`: 264 meldinger → 264 resultater (51s), 0 med feil
- `kallimachos-v1` (Kallimachos `matchPurposes`): 96 meldinger → 96 resultater (8s)

Regresjon (`PersonalChatPromptEvaluationTests|ButlerSignalMatcherTests|ChatPurposeResourceRouterTests`): exit 0, 93 bestått, 0 feilet.

## Poeng («graf-v3-k2»)

### `fixtures-v1` — 101 meldinger

| delmengde | n | top-1 (positive) | top-1 eller spurte riktig | R@3 | MRR | negativer uten handling | alt riktig |
|---|---|---|---|---|---|---|---|
| fixtures | 101 (14+/35−) | 100 % [100 %–100 %] | 100 % | 100 % | 1.00 | 100 % | 61 % |
| alle | 101 (14+/35−) | 100 % [100 %–100 %] | 100 % | 100 % | 1.00 | 100 % | 61 % |

Utfall (alle): riktig 62, graf-hull 39

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
| holdout | 100 (81+/6−) | 40 % [28 %–51 %] | 46 % | 57 % | 0.56 | 100 % | 40 % |
| trening | 296 (231+/30−) | 66 % [61 %–72 %] | 70 % | 79 % | 0.78 | 93 % | 61 % |
| alle | 396 (312+/36−) | 59 % [53 %–64 %] | 64 % | 73 % | 0.72 | 94 % | 56 % |
| enige (generator = tolk) | 373 (292+/36−) | 61 % [56 %–67 %] | 65 % | 76 % | 0.75 | 94 % | 58 % |

Utfall (alle): riktig 222, stille 69, spurte 36, graf-hull 36, feil handling 19, spurte, riktig blant valgene 14

| etikett | forventet | riktig | stille | spurte | feil handling | vanligste feil |
|---|---|---|---|---|---|---|
| H.capability | hjelper | 0/12 | 1 | 9 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×1; resource_match knowledge.demo.kallimachos ×1 |
| S.commerce | flate | 0/12 | 0 | 0 | 0 |  |
| S.meetplace | flate | 0/12 | 0 | 0 | 0 |  |
| S.vote | flate | 0/12 | 0 | 0 | 0 |  |
| S.agreement | flate | 2/12 | 5 | 5 | 0 |  |
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
| H.onboarding | hjelper | 10/12 | 2 | 0 | 0 |  |
| H.workitem | hjelper | 10/12 | 2 | 0 | 0 |  |
| S.aigateway | flate | 10/12 | 0 | 2 | 0 |  |
| S.cellconfig | flate | 10/12 | 1 | 1 | 0 |  |
| H.agent | hjelper | 11/12 | 0 | 1 | 0 |  |
| H.idea | hjelper | 11/12 | 1 | 0 | 0 |  |
| H.video | hjelper | 11/12 | 1 | 0 | 0 |  |
| H.project | hjelper | 12/12 | 0 | 0 | 0 |  |
| M.meta | meta | 12/12 | 0 | 0 | 0 |  |
| N.none | ingen | 12/12 | 0 | 0 | 0 |  |

Per style: dialekt 64 % (n=11), indirekte 45 % (n=132), kort 70 % (n=99), lang 30 % (n=33), normal 67 % (n=102), skrivefeil 38 % (n=8), to-behov 55 % (n=11)
Per lang: en 62 % (n=132), nb 53 % (n=264)

Eksempler på feil handling (det brukeren ville fått foreslått):

- `k1-0039` «hver gang jeg skal dele et kart med en kunde må jeg ta skjermbilde, det er jo tungvint» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.capability)
- `k1-0044` «hvordan funker egentlig autentisering mellom celler, finnes det noe dokumentert» → resource_match purpose:Dokumentskriving og samarbeid (forventet S.docs)
- `k1-0056` «kan du gjøre det nye prosjektet synlig offentlig på haven» → resource_match knowledge.demo.kallimachos (forventet S.publish)
- `k1-0093` «det der prosjektet, du vet, bare gjør det ferdig» → project personal.chat.assist.project (forventet C.clarify)
- `k1-0101` «Jeg satt og pratet med en hyggelig dame fra Arbeiderpartiet i dag, og vi ble enige om at h» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.invite)
- `k1-0115` «Legg til at jeg må huske å ringe rektor i morgen.» → invite_person personal.chat.assist.invite (forventet H.todo)
- `k1-0118` «Kan du minne meg på klokka ni i morgen om at jeg skal møte ordføreren?» → schedule_meeting personal.chat.assist.meeting.schedule (forventet H.reminder)
- `k1-0167` «Vi har hørt at flere i kommunen har opplevd at tjenestene har vært trege den siste uka. So» → todo personal.chat.assist.todo (forventet S.admin)
- `k1-0179` «Jeg kjenner nesten ingen her i år, siden de fleste av mine gamle kjente har sluttet i poli» → resource_match personal.entity.relations.manage (forventet S.networking)
- `k1-0180` «Jeg står bare alene og kjenner ingen i denne folkemengden.» → resource_match personal.entity.relations.manage (forventet S.networking)
- `k1-0197` «Jeg lurer på om det blir finvær eller regn i morgen. Da vet jeg om jeg skal ta med meg par» → invite_person personal.chat.assist.invite (forventet G.gap)
- `k1-0215` «Remind me... actualy just add 'renew visa' to my to-do list for this week.» → reminder personal.chat.assist.reminder (forventet H.todo)

### `korpus-v2` — 264 meldinger

| delmengde | n | top-1 (positive) | top-1 eller spurte riktig | R@3 | MRR | negativer uten handling | alt riktig |
|---|---|---|---|---|---|---|---|
| uavhengig-v2 | 264 (208+/24−) | 28 % [23 %–35 %] | 32 % | 36 % | 0.34 | 88 % | 31 % |
| alle | 264 (208+/24−) | 28 % [23 %–35 %] | 32 % | 36 % | 0.34 | 88 % | 31 % |
| enige (generator = tolk) | 261 (206+/24−) | 28 % [22 %–34 %] | 32 % | 36 % | 0.34 | 88 % | 31 % |

Utfall (alle): riktig 83, stille 74, feil handling 50, spurte 25, graf-hull 24, spurte, riktig blant valgene 8

| etikett | forventet | riktig | stille | spurte | feil handling | vanligste feil |
|---|---|---|---|---|---|---|
| H.capability | hjelper | 0/8 | 2 | 1 | 5 | resource_match knowledge.demo.kallimachos ×4; invite_person personal.chat.assist.invite ×1 |
| H.poll | hjelper | 0/8 | 6 | 2 | 0 |  |
| S.commerce | flate | 0/8 | 0 | 0 | 0 |  |
| S.entity | flate | 0/8 | 2 | 2 | 4 | invite_person personal.chat.assist.invite ×2; resource_match personal.chat.assist.spatial-query ×1 |
| S.map | flate | 0/8 | 4 | 3 | 1 | todo personal.chat.assist.todo ×1 |
| S.meetplace | flate | 0/8 | 0 | 0 | 0 |  |
| S.music | flate | 0/8 | 5 | 1 | 2 | todo personal.chat.assist.todo ×1; resource_match knowledge.demo.kallimachos ×1 |
| S.publish | flate | 0/8 | 5 | 0 | 3 | resource_match knowledge.demo.kallimachos ×3 |
| S.vote | flate | 0/8 | 0 | 0 | 0 |  |
| H.agent | hjelper | 1/8 | 5 | 1 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| S.agreement | flate | 1/8 | 2 | 2 | 3 | resource_match purpose:Still ut og selg digitale kunstverk ×2; todo personal.chat.assist.todo ×1 |
| H.invite | hjelper | 2/8 | 3 | 3 | 0 |  |
| H.workitem | hjelper | 2/8 | 2 | 3 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| S.admin | flate | 2/8 | 3 | 1 | 2 | todo personal.chat.assist.todo ×2 |
| S.aigateway | flate | 2/8 | 3 | 2 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.cellconfig | flate | 2/8 | 1 | 1 | 4 | resource_match knowledge.demo.kallimachos ×1; invite_person personal.chat.assist.invite ×1 |
| S.docs | flate | 2/8 | 2 | 2 | 2 | invite_person personal.chat.assist.invite ×1; todo personal.chat.assist.todo ×1 |
| S.mermaid | flate | 2/8 | 3 | 2 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| C.clarify | avklaring | 3/8 | 5 | 0 | 0 |  |
| H.advisory | hjelper | 3/8 | 3 | 0 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×2 |
| H.meeting | hjelper | 3/8 | 2 | 0 | 3 | resource_match purpose:Still ut og selg digitale kunstverk ×2; create_poll personal.chat.assist.poll ×1 |
| H.onboarding | hjelper | 3/8 | 2 | 0 | 3 | resource_match knowledge.demo.kallimachos ×2; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| H.reminder | hjelper | 3/8 | 3 | 1 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.profilepage | flate | 3/8 | 3 | 0 | 2 | resource_match purpose:Delt mediesamling ×1; resource_match personal.entity.relations.manage ×1 |
| H.idea | hjelper | 4/8 | 1 | 2 | 1 | resource_match personal.chat.assist.spatial-query ×1 |
| H.project | hjelper | 4/8 | 0 | 0 | 4 | todo personal.chat.assist.todo ×3; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.agenda | flate | 4/8 | 2 | 2 | 0 |  |
| S.networking | flate | 4/8 | 3 | 0 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| H.todo | hjelper | 5/8 | 1 | 2 | 0 |  |
| G.gap | hull | 7/8 | 0 | 0 | 1 | schedule_meeting personal.chat.assist.meeting.schedule ×1 |
| H.video | hjelper | 7/8 | 1 | 0 | 0 |  |
| M.meta | meta | 7/8 | 0 | 0 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| N.none | ingen | 7/8 | 0 | 0 | 1 | schedule_meeting personal.chat.assist.meeting.schedule ×1 |

Per style: andrespråk 67 % (n=6), dialekt 38 % (n=13), diktert 25 % (n=8), indirekte 13 % (n=103), kort 71 % (n=34), lang 45 % (n=22), normal 49 % (n=37), skrivefeil 17 % (n=24), to-behov 18 % (n=17)
Per lang: en 27 % (n=132), nb 36 % (n=132)

Eksempler på feil handling (det brukeren ville fått foreslått):

- `k2-0005` «shower thought: klesbyttekveld istedenfor vanlig kjellerfest?? skriv det ned et sted før d» → resource_match personal.chat.assist.spatial-query (forventet H.idea)
- `k2-0010` «we're kicking off the spring revue and need one place with all the tasks, people and deadl» → todo personal.chat.assist.todo (forventet H.project)
- `k2-0015` «trenger et styremøte neste uke med sindre, aurora og kaja, helst etter kl 16. og lavprio: » → create_poll personal.chat.assist.poll (forventet H.meeting)
- `k2-0024` «should our club start charging a membership fee or will ppl just bail? want a proper pros/» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.advisory)
- `k2-0026` «can you guys add a way to split expenses? really miss that for our cabin trips» → invite_person personal.chat.assist.invite (forventet H.capability)
- `k2-0033` «sponsoren vår vil ha noe skriftlig på at logoen deres er på genserne våre i ett år mot 15k» → resource_match purpose:Still ut og selg digitale kunstverk (forventet S.agreement)
- `k2-0035` «vil oppdatere profilsida mi, har nytt bilde og er ikek leder lenger» → resource_match purpose:Delt mediesamling (forventet S.profilepage)
- `k2-0037` «vil at innlegget mitt om frivillighet skal være åpent for alle på nettet, ikke bare folk s» → resource_match knowledge.demo.kallimachos (forventet S.publish)
- `k2-0042` «i need a flowchart-ish visual of how a new member goes from signing up to getting their ke» → resource_match purpose:Still ut og selg digitale kunstverk (forventet S.mermaid)
- `k2-0043` «er med i linjeforeninga, klatregruppa og studentradioen og mister totalt oversikten. vil s» → resource_match personal.chat.assist.spatial-query (forventet S.entity)
- `k2-0045` «jeg har tatt over ansvaret for foreningens instans nå, vil se om alt bak kulissene faktisk» → todo personal.chat.assist.todo (forventet S.admin)
- `k2-0057` «jeg har lyst til å lage vår egen side i HAVEN for utstyrsutlån, med liste over tauene og s» → resource_match knowledge.demo.kallimachos (forventet S.cellconfig)

Full rapport per id: `rapport/graf-v3-k2/rapport-2026-09-24-graf-v3-k2.json`
