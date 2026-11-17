# Akseptanse — «Husk det jeg sa»

Dato: 2026-09-07

## ways-in

- Husets taggflyt nås via `GET /api/content/configuration`, `GET /api/content/tags/pending`, `POST /api/content/tags/approve`, `POST /api/content/tags/skip`, `POST /api/content/tags/select` og `POST /api/content/tags/edit`.
- Gjestens treff nås via `POST /api/entity/match/refresh`, `GET /api/entity/match/pending`, `GET /api/entity/match/expired`, `GET /api/entity/match/shared`, `POST /api/entity/match/open`, `POST /api/entity/match/dismiss`, `POST /api/entity/match/decide` og `POST /api/entity/match/revoke`.
- Match-samtykke produseres av `PalazzoConsentConfigurationFactory` med konkret `matchID` i payloaden.
- Huset mottar og lister strengt validerte pakker via `POST /api/house/remember/receive`, `GET /api/house/remember/list` og `POST /api/house/remember/revoke`.
- Kelnerens trygge visning ligger i `staff.state.lastBrief.remembered` og produseres av `PalazzoStaffConfigurationFactory`.
- `PalazzoScaffoldInfoCell` annonserer de nye konfigurasjonene og signalene for discovery.

Fabrikkene er strukturtestet av `testHuskSkeletonFactoriesUseReachableConcreteActions`: alle formålshandlinger er konkrete og tilgjengelige, samtykke inneholder ingen uerstattet `$matchID`, og taggredigering bruker eksplisitt List-selection-fallback.

## stubs

Ingen ny kontrakt-handler er levert som en stille no-op. Avviste kall returnerer konkret `denied`/HTTP 403 eller et navngitt feilobjekt; den avviklede `insight.query.interests.match` returnerer eksplisitt `status:"deprecated"` og `replacedBy:"match.*"` uten `matches` eller `score`.

## docs

- `PalazzoScaffold/README.md` beskriver signal-, match-, samtykke-, pakke-, hus- og tilbakekallingsflyten.
- `PalazzoScaffold/docs/Remember_contract_2026-09-07.md` beskriver keypaths, autorisasjon, allowlist og regresjonskommandoer.
- Begge er merket `Last verified against code: 2026-09-07`.

## status

`STATUS.md` er oppdatert 2026-09-07 med S0–S9 ferdig, sluttresultat 82/82 tester og S10s Docker-miljøblokkering. G3 er ikke egen-godkjent; den står `venter` til Kjetil tar portbeslutningen.

## parity

S11 er uttrykkelig `BLOKKERT` i handoffen og er ikke utført. Ingen skjermbilde- eller lastetidsakseptanse hevdes. De seks skeleton-fixturene er i stedet kontrollert mot tilgjengelige renderer-semantikker og strukturtestet; valgene står i sluttrapporten.

## Losens uavhengige verifisering (2026-09-07, etter Codex-rapporten)

Kontrollert i kildekoden via mount, ikke fra rapporten:

| §3-rad | Forventet | Faktisk | Evidens |
|---|---|---|---|
| Treffkort / samtykke / delt / feil / hus-tagger / kelner (bilder) | Porthole-paritet mot `images/*-v1.png` | **Ikke målt** — S11 blokkert; bare strukturtest (`testHuskSkeletonFactoriesUseReachableConcreteActions`) | rapport §`_verify_in_porthole` |
| `contract/` | keypaths og allowlist som i kontrakten | Allowlist i `PalazzoMatchModels.swift:146–148` = nøyaktig de 10 nøklene i kontrakten; `match.pending`/`match.expired` er `validateAccess` + `requesterIsOwner` (`PalazzoEntityCell.swift:489–500`); matcheren filtrerer `kind == .interaction && source == "self"` (`PalazzoMatchModels.swift:94`); `insight.query.interests.match` returnerer `status: deprecated` + `replacedBy`, ingen `matches`/`score` (`PalazzoEntityCell.swift:282–283`) | grep 2026-09-07 |
| `dataflow.md` | hver kant i en kontrakt | ruter for content/tags/signals, entity/match/*, house/remember/* finnes i `routes.swift` (ACCEPT #ways-in) | rapport §S8 |
| Testutdata | alle ankre | TESTRESULT.md har alle 15 ankre; `#deploy` = blocked | TESTRESULT.md |
| Kjørende flate (e2e) | seed → treffkort → ja → kelnerlinje | HTTP-e2e grønn i testsuiten (`testHuskE2E`); **ikke** vist i Porthole/Binding | TESTRESULT.md#e2e |
| Deploy | staging-image bygger, `GET /api/content/signals` svarer | **blocked**: Codex-sandkassen når ikke `docker.sock`. Registrert som HAVEN-Deploy **HD-0012** (eier: Kjetil) med tre poster: commit, build, up+curl | `HAVEN-Deploy/queue/tasks/HD-0012.json` |

Avvik som ble funnet og hvordan de ble håndtert:
1. Baseline var 68 tester (ikke 48 som i PLAN) og **ikke grønn** — 3 feil i `PalazzoIdentityLinkTests` pga. rekursiv dokumentrot i `configure.swift`. Rettet i pakken (`CELL_VAULT_DOCUMENT_ROOT`). PLAN-tallet kom fra rapporten 03.09, ikke fra en kjøring → lesson.
2. Testkommandoen krever nå ingen miljøprefiks (verifisert i rapportens sluttkjøring).
3. `PalazzoConsentRequest.Kind` som raw enum + `matchID`-felt i stedet for associated value — bakoverkompatibel snapshot-dekoding; godtatt.
4. Verifikasjon delt mellom pakkemodell og husets receive-grense — alle kontrakt-sjekker kjøres; godtatt.

Ikke godkjent av Losen på Kjetils vegne: G3. Åpent for G3: S11 paritet (bilder) og HD-0012 (deploy).
