# Grafendringer v1–v3 (WP-C4)

Formål: Butler uten språkmodell skal treffe riktig hjelper eller flate for naturlige meldinger. Kjetil godkjente C4 2026-09-23: endringer uten godkjenning per diff, men hver endring begrunnes med feilende **trenings**rader, og holdout røres ikke.

Patchene: `HAVEN-Deploy/_handoff/BUTLER-MAALING/graf/graf-v{1,2,3}.patch` (v3 er summen). Filer: `PersonalCopilotCloudStore.swift` (hjelper-scorere, nektelse) og `ChatPurposeResourceRouter.swift` (formålsleksikon, ny node for avtaleverkstedet). Hver endring har en kommentar `graf-v1`/`graf-v2`/`graf-v3` i koden.

## Hva som ble endret, og hvorfor

| Endring | Versjon | Begrunnelse (treningsrader som feilet før) |
|---|---|---|
| Gjøremål/liste-fraser; «legg til gjøremål» er ikke invitasjon | v1, v2 | «legg til gjøremål», «Add this to my list.», «add 'renew visa' to my to-do list» ble invitasjon |
| Påminnelse med klokkeslett («vekk meg klokka 7», «ping me … around nine», «gi meg beskjed klokka 14») | v1, v2 | 9 av 10 H.reminder-treningsrader var stille eller spurte |
| Video: «video call», «start video», «on screen», «jump on a call right now» | v1 | 6 treningsrader, to av dem ble til kunstsalg-flaten |
| Møte: «a call … Wednesday», «samles … tidspunkt», «sitja ned … neste veke» | v1 | 4 treningsrader stille/spurte |
| Poll når gruppen ikke blir enig («flertallet», «la gjengen velge»); folkeavstemning og møtested er ikke poll | v1 | 5 H.poll-rader; 4 S.vote-rader ble poll |
| Idéfangst: «note it down», «fikk en tanke», «ikke la meg glemme»; «no idea» er ikke idé | v1, v2 | 9 H.idea-rader; «Everyone has … no idea how we'll ever agree» ble idéfangst |
| Feilmelding: «report a bug», «appen krasjer», «gjør ikke det den skal» | v1 | 9 H.workitem-rader |
| Lokal agent: rydde skrivebord/skjerm | v1 | 7 H.agent-rader stille |
| Koble til modell: «koble til modell», «api-nøkkel», «svarer rart»; ikke når brukeren spør om status | v1, v2, v3 | 8 H.onboarding-rader; to regresjoner i PromptPurposeLab rettet i v2 og v3 |
| Rådgiverpanel: «panel assessment», «flere sider», «kloke hoder», «trenger en vurdering» | v1, v2 | 6 H.advisory-rader |
| Behov for ny funksjon: «should build», «there's no way to», «knappen finnes ikke ennå» | v1 | 7 H.capability-rader (produktet spør først når funnet er av; se under) |
| Prosjekt: «samles et sted», «set up the workspace», «mapper på plass»; publisering er ikke prosjekt | v1 | 7 H.project-rader, 3 av dem ble kart-flaten |
| Invitasjon: «inn i samtalen», «med i tråden», «få inn Silje» | v1 | 6 H.invite-rader |
| Nektelse som hele ord («noter» er ikke «not»); «don't want to lose it» er en forespørsel | v1, v2 | «Noter en idé» ble undertrykt; «just had a thought …, don't want to lose it» ble stille |
| Leksikonfraser: publisering, musikk, diagram, entiteter, driftsstatus, dokumentasjon, program, kart, AI-leverandør, egen flate, nettverk | v1, v2 | S.*-rader stille eller feil flate (se tabellen) |
| Ny node: avtaleverkstedet (`purpose://agreement.terms.put-in-writing` → `cell:///AgreementWorkbench`) | v1 | 9 av 9 S.agreement-rader bommet; flaten fantes, men ingen node pekte dit |
| Nettverk: `PersonalMatchmaking` og `PublicProfileDirectory` som endepunkt for nettverksformålet | v1 | S.networking-rader gikk til entitetsflaten |

## Før og etter per etikett (top-1)

| etikett | trening før | trening etter | holdout før | holdout etter | treningsrader vunnet (id) |
|---|---|---|---|---|---|
| C.clarify | 1/9 | 1/9 | 2/3 | 2/3 |  |
| G.gap | 9/11 | 9/11 | 1/1 | 1/1 |  |
| H.advisory | 2/8 | 7/8 | 2/4 | 3/4 | k1-0036, k1-0135, k1-0233, k1-0331, k1-0332 |
| H.agent | 3/10 | 10/10 | 0/2 | 1/2 | k1-0028, k1-0030, k1-0127, k1-0129, k1-0228, k1-0325 … |
| H.capability | 0/7 | 0/7 | 0/5 | 0/5 |  |
| H.idea | 3/12 | 11/12 | 0/0 | 0/0 | k1-0008, k1-0009, k1-0107, k1-0206, k1-0207, k1-0304 … |
| H.invite | 4/10 | 9/10 | 1/2 | 1/2 | k1-0002, k1-0003, k1-0201, k1-0298, k1-0300 |
| H.meeting | 3/7 | 6/7 | 1/5 | 3/5 | k1-0122, k1-0221, k1-0320 |
| H.onboarding | 1/9 | 8/9 | 1/3 | 2/3 | k1-0033, k1-0132, k1-0229, k1-0231, k1-0328, k1-0329 … |
| H.poll | 2/7 | 6/7 | 1/5 | 1/5 | k1-0006, k1-0104, k1-0204, k1-0303 |
| H.project | 2/9 | 9/9 | 3/3 | 3/3 | k1-0015, k1-0113, k1-0114, k1-0212, k1-0213, k1-0311 … |
| H.reminder | 2/11 | 9/11 | 0/1 | 0/1 | k1-0020, k1-0021, k1-0218, k1-0219, k1-0316, k1-0317 … |
| H.todo | 0/8 | 3/8 | 0/4 | 0/4 | k1-0016, k1-0017, k1-0214 |
| H.video | 2/8 | 8/8 | 1/4 | 3/4 | k1-0027, k1-0126, k1-0223, k1-0224, k1-0225, k1-0322 |
| H.workitem | 0/9 | 9/9 | 0/3 | 1/3 | k1-0010, k1-0012, k1-0109, k1-0111, k1-0208, k1-0210 … |
| M.meta | 10/10 | 10/10 | 2/2 | 2/2 |  |
| N.none | 9/9 | 9/9 | 3/3 | 3/3 |  |
| S.admin | 1/11 | 7/11 | 0/1 | 1/1 | k1-0068, k1-0069, k1-0166, k1-0265, k1-0266, k1-0364 |
| S.agenda | 3/8 | 3/8 | 0/4 | 0/4 |  |
| S.agreement | 0/8 | 1/8 | 0/4 | 1/4 | k1-0248 |
| S.aigateway | 3/8 | 6/8 | 2/4 | 4/4 | k1-0071, k1-0169, k1-0170 |
| S.cellconfig | 1/9 | 8/9 | 1/3 | 2/3 | k1-0085, k1-0087, k1-0184, k1-0283, k1-0284, k1-0383 … |
| S.commerce | 0/11 | 0/11 | 0/1 | 0/1 |  |
| S.docs | 1/8 | 2/8 | 1/4 | 1/4 | k1-0340 |
| S.entity | 1/10 | 2/10 | 1/2 | 2/2 | k1-0262 |
| S.map | 2/9 | 3/9 | 1/3 | 1/3 | k1-0343 |
| S.meetplace | 0/10 | 0/10 | 0/2 | 0/2 |  |
| S.mermaid | 1/10 | 7/10 | 0/2 | 0/2 | k1-0062, k1-0063, k1-0160, k1-0259, k1-0260, k1-0358 |
| S.music | 1/6 | 3/6 | 0/6 | 0/6 | k1-0356, k1-0357 |
| S.networking | 0/10 | 4/10 | 0/2 | 0/2 | k1-0080, k1-0178, k1-0277, k1-0376 |
| S.profilepage | 2/9 | 6/9 | 0/3 | 1/3 | k1-0052, k1-0151, k1-0152, k1-0349 |
| S.publish | 0/10 | 6/10 | 0/2 | 1/2 | k1-0055, k1-0253, k1-0254, k1-0255, k1-0353, k1-0354 |
| S.vote | 0/5 | 0/5 | 0/7 | 0/7 |  |

Holdout: 16 vunnet, 0 tapt. Trening: 0 tapt. Negativer uten handling: 94 % før og etter.

## Det som ikke ble bedre, og hvorfor

- **H.capability** (0/12 før og etter på top-1): produktet spør med vilje før det lager en funksjonsforespørsel når kapabilitetsfunnet ikke er slått på. De fleste radene ender nå som «spurte, riktig blant valgene», som er riktig oppførsel.
- **S.commerce, S.meetplace, S.vote**: Arendalsuka-flatene publiseres i prod, men finnes ikke i testkjøringens katalog. De telles som graf-hull i denne målingen, ikke som bom. De må måles mot en katalog som har dem (neste runde).
- **C.clarify** (3/12): «fiks den greia fra i går» gir stillhet i stedet for et oppfølgingsspørsmål. Butler spør bare når den har et signal. Ikke rørt i v3; kandidat for neste runde.
- **Indirekte og lange meldinger** er fortsatt svakest. Det er her en språkmodell gjør mest, og her fraser hjelper minst.
