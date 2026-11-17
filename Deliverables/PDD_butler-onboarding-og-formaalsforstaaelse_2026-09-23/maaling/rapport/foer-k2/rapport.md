Arbeidstre: `_wt-butler-maaling-20260923` @ `77a922bc`, endringer: 2 fil(er).
Korpusfiler: fixtures-v1.jsonl korpus-v1.jsonl korpus-v2.jsonl
Bygg: OK (32s).
Katalog: `maaling/katalog.json` (58 konfigurasjoner, 21 dokumenter, 0 sannhetskilder).
- `fixtures-v1`: 101 meldinger → 101 resultater (18s), 0 med feil
- `korpus-v1`: 396 meldinger → 396 resultater (50s), 0 med feil
- `korpus-v2`: 264 meldinger → 264 resultater (49s), 0 med feil
- `kallimachos-v1` (Kallimachos `matchPurposes`): 96 meldinger → 96 resultater (8s)

Regresjon (`PersonalChatPromptEvaluationTests|ButlerSignalMatcherTests|ChatPurposeResourceRouterTests`): exit 0, 93 bestått, 0 feilet.

## Poeng («foer-k2»)

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
| holdout | 100 (81+/6−) | 20 % [11 %–28 %] | 22 % | 23 % | 0.23 | 100 % | 24 % |
| trening | 296 (231+/30−) | 17 % [12 %–23 %] | 21 % | 19 % | 0.19 | 93 % | 23 % |
| alle | 396 (312+/36−) | 18 % [14 %–22 %] | 21 % | 21 % | 0.20 | 94 % | 23 % |
| enige (generator = tolk) | 373 (292+/36−) | 19 % [14 %–23 %] | 22 % | 22 % | 0.21 | 94 % | 25 % |

Utfall (alle): stille 139, riktig 93, spurte 71, feil handling 47, graf-hull 36, spurte, riktig blant valgene 10

| etikett | forventet | riktig | stille | spurte | feil handling | vanligste feil |
|---|---|---|---|---|---|---|
| H.capability | hjelper | 0/12 | 7 | 3 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×1; resource_match knowledge.demo.kallimachos ×1 |
| H.todo | hjelper | 0/12 | 3 | 5 | 4 | invite_person personal.chat.assist.invite ×4 |
| H.workitem | hjelper | 0/12 | 4 | 6 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×1; resource_match purpose:Central purpose-driven co-pilot chat ×1 |
| S.agreement | flate | 0/12 | 4 | 7 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.commerce | flate | 0/12 | 0 | 0 | 0 |  |
| S.meetplace | flate | 0/12 | 0 | 0 | 0 |  |
| S.networking | flate | 0/12 | 6 | 3 | 3 | resource_match personal.entity.relations.manage ×3 |
| S.publish | flate | 0/12 | 8 | 2 | 2 | project personal.chat.assist.project ×1; resource_match purpose:Musikkpublisering ×1 |
| S.vote | flate | 0/12 | 0 | 0 | 0 |  |
| S.admin | flate | 1/12 | 9 | 1 | 1 | todo personal.chat.assist.todo ×1 |
| S.mermaid | flate | 1/12 | 4 | 4 | 3 | resource_match purpose:Still ut og selg digitale kunstverk ×2; advisory_report personal.chat.assist.advisory-report ×1 |
| S.music | flate | 1/12 | 6 | 2 | 3 | resource_match purpose:Publiser sider og innlegg om deg, prosjektet eller organisasjonen ×2; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| H.onboarding | hjelper | 2/12 | 6 | 1 | 3 | resource_match personal.ai.gateway.configure ×3 |
| H.reminder | hjelper | 2/12 | 6 | 3 | 1 | schedule_meeting personal.chat.assist.meeting.schedule ×1 |
| S.cellconfig | flate | 2/12 | 5 | 5 | 0 |  |
| S.docs | flate | 2/12 | 3 | 5 | 2 | resource_match purpose:Dokumentskriving og samarbeid ×1; resource_match purpose://capability.construct-cellconfiguration ×1 |
| S.entity | flate | 2/12 | 4 | 5 | 1 | invite_person personal.chat.assist.invite ×1 |
| S.profilepage | flate | 2/12 | 5 | 4 | 1 | invite_person personal.chat.assist.invite ×1 |
| C.clarify | avklaring | 3/12 | 8 | 0 | 1 | project personal.chat.assist.project ×1 |
| H.agent | hjelper | 3/12 | 6 | 3 | 0 |  |
| H.idea | hjelper | 3/12 | 3 | 3 | 3 | guided_onboarding personal.chat.assist.guided-onboarding ×2; reminder personal.chat.assist.reminder ×1 |
| H.poll | hjelper | 3/12 | 6 | 2 | 1 | idea_capture personal.chat.assist.idea.capture ×1 |
| H.video | hjelper | 3/12 | 6 | 1 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×2 |
| S.agenda | flate | 3/12 | 8 | 0 | 1 | idea_capture personal.chat.assist.idea.capture ×1 |
| S.map | flate | 3/12 | 5 | 3 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| H.advisory | hjelper | 4/12 | 4 | 4 | 0 |  |
| H.meeting | hjelper | 4/12 | 6 | 2 | 0 |  |
| H.invite | hjelper | 5/12 | 3 | 2 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×1; resource_match knowledge.demo.kallimachos ×1 |
| H.project | hjelper | 5/12 | 2 | 1 | 4 | resource_match personal.chat.assist.spatial-query ×3; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.aigateway | flate | 5/12 | 2 | 4 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| G.gap | hull | 10/12 | 0 | 0 | 2 | invite_person personal.chat.assist.invite ×1; resource_match cellprotocol.docs.lookup ×1 |
| M.meta | meta | 12/12 | 0 | 0 | 0 |  |
| N.none | ingen | 12/12 | 0 | 0 | 0 |  |

Per style: dialekt 9 % (n=11), indirekte 11 % (n=132), kort 37 % (n=99), lang 9 % (n=33), normal 33 % (n=102), skrivefeil 25 % (n=8), to-behov 18 % (n=11)
Per lang: en 28 % (n=132), nb 21 % (n=264)

Eksempler på feil handling (det brukeren ville fått foreslått):

- `k1-0015` «vi har egentlig fem forskjellige tråder om dette nå, burde vel samles et sted» → resource_match personal.chat.assist.spatial-query (forventet H.project)
- `k1-0016` «legg til gjøremål» → invite_person personal.chat.assist.invite (forventet H.todo)
- `k1-0033` «butler svarer jo ingenting fornuftig ennå, mangler vel en modell koblet til eller noe» → resource_match personal.ai.gateway.configure (forventet H.onboarding)
- `k1-0039` «hver gang jeg skal dele et kart med en kunde må jeg ta skjermbilde, det er jo tungvint» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.capability)
- `k1-0044` «hvordan funker egentlig autentisering mellom celler, finnes det noe dokumentert» → resource_match purpose:Dokumentskriving og samarbeid (forventet S.docs)
- `k1-0056` «kan du gjøre det nye prosjektet synlig offentlig på haven» → project personal.chat.assist.project (forventet S.publish)
- `k1-0058` «last opp ny låt» → resource_match purpose:Publiser sider og innlegg om deg, prosjektet eller organisasjonen (forventet S.music)
- `k1-0063` «i keep drawing this architecture on a napkin, would be nice to have it properly as a chart» → resource_match purpose:Still ut og selg digitale kunstverk (forventet S.mermaid)
- `k1-0093` «det der prosjektet, du vet, bare gjør det ferdig» → project personal.chat.assist.project (forventet C.clarify)
- `k1-0101` «Jeg satt og pratet med en hyggelig dame fra Arbeiderpartiet i dag, og vi ble enige om at h» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.invite)
- `k1-0109` «Appen krasjer hver gang jeg trykker på kartet, kan du melde fra om det?» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.workitem)
- `k1-0113` «Vi i komiteen har bestemt oss for å sette i gang et skikkelig opplegg rundt frivillighetsd» → resource_match personal.chat.assist.spatial-query (forventet H.project)

### `korpus-v2` — 264 meldinger

| delmengde | n | top-1 (positive) | top-1 eller spurte riktig | R@3 | MRR | negativer uten handling | alt riktig |
|---|---|---|---|---|---|---|---|
| uavhengig-v2 | 264 (208+/24−) | 20 % [14 %–25 %] | 25 % | 25 % | 0.23 | 92 % | 25 % |
| alle | 264 (208+/24−) | 20 % [14 %–25 %] | 25 % | 25 % | 0.23 | 92 % | 25 % |
| enige (generator = tolk) | 261 (206+/24−) | 19 % [14 %–25 %] | 24 % | 25 % | 0.23 | 92 % | 25 % |

Utfall (alle): stille 79, riktig 66, feil handling 58, spurte 27, graf-hull 24, spurte, riktig blant valgene 10

| etikett | forventet | riktig | stille | spurte | feil handling | vanligste feil |
|---|---|---|---|---|---|---|
| H.capability | hjelper | 0/8 | 1 | 2 | 5 | resource_match knowledge.demo.kallimachos ×4; invite_person personal.chat.assist.invite ×1 |
| H.poll | hjelper | 0/8 | 6 | 2 | 0 |  |
| S.agreement | flate | 0/8 | 2 | 2 | 4 | resource_match purpose:Still ut og selg digitale kunstverk ×3; todo personal.chat.assist.todo ×1 |
| S.commerce | flate | 0/8 | 0 | 0 | 0 |  |
| S.entity | flate | 0/8 | 3 | 1 | 4 | invite_person personal.chat.assist.invite ×2; resource_match personal.chat.assist.spatial-query ×1 |
| S.map | flate | 0/8 | 4 | 2 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×2 |
| S.meetplace | flate | 0/8 | 0 | 0 | 0 |  |
| S.mermaid | flate | 0/8 | 3 | 4 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.music | flate | 0/8 | 5 | 2 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| S.publish | flate | 0/8 | 5 | 0 | 3 | resource_match knowledge.demo.kallimachos ×3 |
| S.vote | flate | 0/8 | 0 | 0 | 0 |  |
| H.agent | hjelper | 1/8 | 5 | 1 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| H.onboarding | hjelper | 1/8 | 2 | 1 | 4 | resource_match knowledge.demo.kallimachos ×3; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| H.workitem | hjelper | 1/8 | 2 | 3 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×1; resource_match knowledge.demo.kallimachos ×1 |
| S.profilepage | flate | 1/8 | 5 | 0 | 2 | resource_match purpose:Delt mediesamling ×1; resource_match personal.entity.relations.manage ×1 |
| H.invite | hjelper | 2/8 | 3 | 3 | 0 |  |
| H.reminder | hjelper | 2/8 | 4 | 1 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| H.todo | hjelper | 2/8 | 1 | 3 | 2 | invite_person personal.chat.assist.invite ×2 |
| H.video | hjelper | 2/8 | 3 | 0 | 3 | resource_match purpose:Still ut og selg digitale kunstverk ×3 |
| S.admin | flate | 2/8 | 3 | 1 | 2 | todo personal.chat.assist.todo ×2 |
| S.aigateway | flate | 2/8 | 3 | 2 | 1 | resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.cellconfig | flate | 2/8 | 1 | 1 | 4 | resource_match knowledge.demo.kallimachos ×1; invite_person personal.chat.assist.invite ×1 |
| S.docs | flate | 2/8 | 2 | 2 | 2 | invite_person personal.chat.assist.invite ×1; todo personal.chat.assist.todo ×1 |
| C.clarify | avklaring | 3/8 | 5 | 0 | 0 |  |
| H.advisory | hjelper | 3/8 | 3 | 0 | 2 | resource_match purpose:Still ut og selg digitale kunstverk ×2 |
| H.meeting | hjelper | 3/8 | 2 | 0 | 3 | resource_match purpose:Still ut og selg digitale kunstverk ×2; create_poll personal.chat.assist.poll ×1 |
| S.networking | flate | 3/8 | 3 | 0 | 2 | resource_match personal.entity.relations.manage ×1; resource_match knowledge.demo.kallimachos ×1 |
| H.idea | hjelper | 4/8 | 1 | 2 | 1 | resource_match personal.chat.assist.spatial-query ×1 |
| H.project | hjelper | 4/8 | 0 | 0 | 4 | todo personal.chat.assist.todo ×3; resource_match purpose:Still ut og selg digitale kunstverk ×1 |
| S.agenda | flate | 4/8 | 2 | 2 | 0 |  |
| G.gap | hull | 7/8 | 0 | 0 | 1 | schedule_meeting personal.chat.assist.meeting.schedule ×1 |
| M.meta | meta | 7/8 | 0 | 0 | 1 | resource_match knowledge.demo.kallimachos ×1 |
| N.none | ingen | 8/8 | 0 | 0 | 0 |  |

Per style: andrespråk 33 % (n=6), dialekt 31 % (n=13), diktert 25 % (n=8), indirekte 8 % (n=103), kort 56 % (n=34), lang 45 % (n=22), normal 41 % (n=37), skrivefeil 17 % (n=24), to-behov 12 % (n=17)
Per lang: en 21 % (n=132), nb 29 % (n=132)

Eksempler på feil handling (det brukeren ville fått foreslått):

- `k2-0005` «shower thought: klesbyttekveld istedenfor vanlig kjellerfest?? skriv det ned et sted før d» → resource_match personal.chat.assist.spatial-query (forventet H.idea)
- `k2-0007` «hver gang jeg prøver å laste opp logoen til foreninga fryser hele appen og jeg må restarte» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.workitem)
- `k2-0010` «we're kicking off the spring revue and need one place with all the tasks, people and deadl» → todo personal.chat.assist.todo (forventet H.project)
- `k2-0015` «trenger et styremøte neste uke med sindre, aurora og kaja, helst etter kl 16. og lavprio: » → create_poll personal.chat.assist.poll (forventet H.meeting)
- `k2-0017` «henrik sitter på lesesalen i oslo og må være med på styremøtet som starter nå, kan vi få h» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.video)
- `k2-0024` «should our club start charging a membership fee or will ppl just bail? want a proper pros/» → resource_match purpose:Still ut og selg digitale kunstverk (forventet H.advisory)
- `k2-0026` «can you guys add a way to split expenses? really miss that for our cabin trips» → invite_person personal.chat.assist.invite (forventet H.capability)
- `k2-0031` «kor e egentlig det lokalet på dragvoll vi ska vær i? vis mæ det på kartet» → resource_match purpose:Still ut og selg digitale kunstverk (forventet S.map)
- `k2-0033` «sponsoren vår vil ha noe skriftlig på at logoen deres er på genserne våre i ett år mot 15k» → resource_match purpose:Still ut og selg digitale kunstverk (forventet S.agreement)
- `k2-0035` «vil oppdatere profilsida mi, har nytt bilde og er ikek leder lenger» → resource_match purpose:Delt mediesamling (forventet S.profilepage)
- `k2-0037` «vil at innlegget mitt om frivillighet skal være åpent for alle på nettet, ikke bare folk s» → resource_match knowledge.demo.kallimachos (forventet S.publish)
- `k2-0042` «i need a flowchart-ish visual of how a new member goes from signing up to getting their ke» → resource_match purpose:Still ut og selg digitale kunstverk (forventet S.mermaid)

Full rapport per id: `rapport/foer-k2/rapport-2026-09-24-foer-k2.json`
