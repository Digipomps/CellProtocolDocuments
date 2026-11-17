# PLAN — testmatrise og APNs-chat

Oppgavemappe: `PDD_testmatrise-og-apns-chat_2026-09-29` · G1 godkjent 2026-10-06 · Plan iterasjon 1 (venter på G2)

> G2 settes bare av Kjetils ord. Etter G2 teller bare artefakter fra `FORMAALSSPEC.md §3` som fremdrift (`lesson.plan-instead-of-delivery`).

## 0. Fire ting du bør vite før du leser videre

**0.1 Det meste av APNs-sporet kan gjøres nå; chat-sporet venter på invitasjonen.** Token-registrering (T5.1), payload (T5.2), «bare den inviterte» (T5.3) og trykk-åpner-billetten (T5.4) er uavhengige av hverandre og av chatten, og kan bygges og testes mot en stub-transport uten noe fra Apple. T1, T2, T3 og delen av T5.4 som viser en invitasjon avhenger av *runde A del 2* (CellScaffold + Binding) og *WP7* (aksept → to envelopes → ChatCell) i invitasjons-PDD-en. Der en test trenger noe som ikke finnes, står den `blocked: avhenger av <WP>`, aldri grønn.

**0.2 Én test kan bare Kjetil gjøre grønn:** T5.5, det ekte sandbox-varselet. Den trenger `APNS_*`-miljø på skyscaffoldet, en Xcode-bygd app med push-entitlement og et enhets-token. Jeg leser aldri nøkkelen. Alt annet er laget slik at T5.5 bare er et bytte fra stub-transport til ekte transport.

**0.3 Ingen ny GUI bygges her.** G1-GUI står som «ikke relevant». Trykk på varselet åpner den invitasjonsflaten som invitasjons-PDD-en leverer (WP10, bilder godkjent 24.09). Oppdager vi at appen trenger en ny flate, stopper vi og tar det som eget G1-GUI.

**0.4 Plan er ikke levering.** Når G2 er satt er første leveranse `contract/` + `handoff/baseline.sh` kjørt (WP0–WP1), ikke flere dokumenter.

## 1. Rekkefølgen, og hvorfor

```
 Fase 1 — kan gjøres nå (ingenting blocked)
   WP0  baseline (ren eksport av origin/main)
   WP1  T5.2 payload + kontrakt        ──┐
   WP2  T5.1 token hører til entiteten ──┼─▶ WP3  T5.3 bare den inviterte
   WP5  T6   snapshot (kjørt 04.10: lukkes med testbevis)
   WP6  to/tre lokale scaffolds side om side
   WP8a admin-cannot-enter-other-scaffold (gjenbruker entitetsdata-fixtures)
 Fase 2 — når invitasjonen (runde A del 2 + WP7) er grønn
   WP4  T5.4 trykk åpner verifisert invitasjon
   WP7  T1  tre brukere på ett scaffold
   WP8b T2  samme samtale mellom to scaffolds
   WP9  T3  prod-røyktest (lesing) + staging-kjede med testkelner
   WP10 T4  enhetsprofiler + iPhone-sjekkliste
 Fase 3 — krever Kjetil
   WP11 T5.5 ekte sandbox-varsel
   WP12 matrise, docs, regresjon, læring
```

Hvorfor slik: fase 1 gir alt som kan bevises uten chat og er det en som kan feile tidlig (kontrakt, signering, målgruppesjekk). WP6 må måles før T2 planlegges videre på det: i dag er «to scaffolds med egen eier/vault/port side om side» *recalled*, ikke målt (`FORMAALSSPEC.md §0.1`).

## 2. Arbeidspakkene

«Utfører»: **Claude** = skriver kode og tester og kjører dem via `handoff/` på Macen; **Codex/Xcode** = bygger og kjører der simulator eller Xcode trengs; **Kjetil** = det bare han kan. «Repo» er der endringen lander. Etter hvert grønt bygg legges en commit-pakke (`lesson.branch-is-empty-after-eight-work-packages`): hash leses etter push og limes inn i TESTRESULT.

| WP | purposeRef | Repo | Hva som gjøres | Tester (§5) | Utfører | Gir til §3 |
|---|---|---|---|---|---|---|
| **0** | `pkg.std.everything-works` | CellProtocol, CellScaffold, Binding | `handoff/baseline.sh`: ren eksport av origin/main per repo (`git archive`, ikke det delte arbeidstreet), bygg + full test; rødt kjøres tre ganger før noe konkluderes; nedstrøms-pinner leses fra forbrukerens egen `Package.resolved`. Tall oppgis som «forventet ≈ N (fra kilde, dato)», aldri som fasit. | `test.build`, `test.regression` | Claude (script), Macen kjører | `TESTRESULT.md#build`, `#regression` |
| **1** | `…apns.payload-carries-no-content` (T5.2) | CellScaffold | `InviteApnsPayload`: bygger `{aps:{alert:{title,body}}, haven:{k:"invite",id}}` fra en billett-ID og *ingenting annet*; `PushSendRequest`-bygger for invitasjon; verifiser at ticketID-mønsteret i kontrakten stemmer med det `invite.prepare` faktisk lager (åpent punkt i kontrakten). Golden fixtures fra `contract/`; sentinel i avsendernavn/basis/melding finnes ikke i noen byte. | `test.apns.payload-has-no-content`, `test.cell.contract-fixtures` | Claude | `#apns`, `#contract` |
| **2** | `…apns.token-belongs-to-an-entity` (T5.1) | CellProtocol (typer + verifier), CellScaffold (`PushRegistryCell`), Binding | `HavenPushRegistration` + signert verifisering i CellProtocol (samme mønster som #51); `PushRegistryCell` lagrer entitet/miljø/bundle-ID/token uten navn og har `register`/`revoke`; Binding signerer med entitetens egen nøkkel og kaller `push.register` i stedet for konferanse-registreringen *for invitasjonsbruk* (konferanse-flyten røres ikke). Designvalg til G2: typene i CellProtocol, ikke bare i CellScaffold, fordi appen og scaffoldet må dele signaturformatet. | `test.apns.token-registration-signed`, `test.apns.token-revoke`, `test.cell.auth-negative` | Claude, Codex/Xcode (Binding-bygg) | `#apns`, `#auth` |
| **3** | `…apns.only-who-was-invited-is-pushed` (T5.3) | CellScaffold | `InvitePushDispatcher`: sender bare hvis (a) billetten er publisert og gyldig, (b) publiseringen navngir en entitet (`audienceEntity`, løst opp av WP13) som har aktiv registrering, (c) ingen gravstein fra samme utsteder til samme audience. Alle andre utfall logges internt (`no_registration`, `wrong_audience`, `token_revoked`, `ticket_expired`, `ticket_revoked`, `tombstoned`) og er **ikke synlige for avsender** — testet ved at `HavenInviteSenderView` er lik uansett utfall. Stub-transport. | `test.apns.wrong-audience-not-pushed`, `test.apns.tombstone-blocks-push`, `test.apns.expired-not-pushed` | Claude | `#apns` |
| **4** | `…apns.tap-opens-the-invitation` (T5.4) | Binding | Appen tar imot `haven.k/id`, henter billetten fra scaffoldet (samme GET som landing), verifiserer med `HavenInviteVerifier`, åpner invitasjonsflaten; ugyldig billett → feilflate; **ingen auto-aksept**; payload brukes bare til å vite *hvilken* billett. Verifiseringsdelen kan testes nå; flaten og GET-veien **avhenger av runde A del 2 + WP10 i invitasjons-PDD-en**. | `test.apns.tap-opens-verified-invitation` | Claude (logikk), Codex/Xcode (flate) | `#apns` |
| **5** | `…nothing-uncommitted-is-lost` (T6) | alle fire | Allerede kjørt 04.10: fire wip-grener pushet, «uberørt: JA», hash lest etter push. Gjenstår: føre `test.push.*` inn i `TESTRESULT.md#push` med utdata og filliste for det som ble holdt ute; commit og push *denne* PDD-mappen (mitt eget) som egen gren fra Macen. | `test.push.snapshot-no-disturbance`, `test.push.no-secrets`, `test.push.hash-read-after-push` | Claude (Macen kjører) | `#push` |
| **6** | `…two-scaffolds-one-conversation` (grunnlag for T1/T2) | CellScaffold | `handoff/two-scaffolds.sh`: 2–3 lokale instanser med egen port, eier, vault og lagring; start/stopp på PID vi selv startet. **Først måles det** at de kjører side om side (`/health` på begge) — ellers noteres hvorfor ikke. | (grunnlag; måling i `#cross-scaffold`) | Claude, Macen | `handoff/two-scaffolds-*.log` |
| **7** | `…same-scaffold-collaboration` (T1) | CellProtocol (harness), CellScaffold | Tre `SimulatedEntity` (tilfeldige UUID-er, egne vaults) inviterer/aksepterer/snakker i én invitasjonschat; C kan ikke lese A↔B. Nøkkelavtale og aksept-signatur kan testes nå; «ChatCell klar» **avhenger av invitasjons-PDD WP7**. | `test.matrise.same-scaffold-three` | Claude | `#same-scaffold` |
| **8a** | `…two-scaffolds-one-conversation` (T2, del 1) | CellScaffold | Admin på scaffold 1 nektes lesing/skriving/handlinger i celler på scaffold 2 (gjenbruker entitetsdata-fixtures og to-entitets-harnessen); den positive motsatsen: en Agreement åpner nøyaktig sitt omfang. Kjøres i begge oppsett (`lesson.location-is-not-ownership`). | `test.matrise.admin-cannot-enter-other-scaffold` | Claude | `#cross-scaffold` |
| **8b** | `…two-scaffolds-one-conversation` (T2, del 2) | CellScaffold, CellProtocol | A på scaffold 1 inviterer B på scaffold 2 (fra WP6); ja gir chat med samme meldinger på begge sider, forseglet til hver mottakers nøkkel. **Avhenger av runde A del 2 + WP7.** | `test.matrise.cross-scaffold-chat` | Claude | `#cross-scaffold` |
| **9** | `…prod-to-palazzo-staff` (T3) | CellScaffold, script | (a) `handoff/prod-smoke.sh`: bare GET mot prod — helse og at oppslag av et *ikke-publisert* endepunkt gir samme svar som et ikke-eksisterende (A1). Ingen POST. **Kjøres ikke før Kjetil har sagt ja til lesing fra prod.** (b) Staging-kjede med en testkelner-entitet merket som test: **avhenger av at Palazzo-vert/miljø er funnet (§6.1 i spec) og av runde A del 2.** | `test.matrise.prod-readonly-smoke`, `test.matrise.staging-waiter-chain` | Claude; Kjetil (ja til prod, Palazzo-vert) | `#prod-smoke`, `#palazzo` |
| **10** | `…same-suite-on-every-device` (T4) | Binding, CellProtocol | Enhetsprofiler som *data* (plattform, destinasjon, hva som finnes av nøkkelchain): `mac-app`, `ios-sim-iphone`, `ios-sim-ipad`, `linux-client` (klient uten UI); `handoff/matrix.sh <profil>`; `handoff/iphone-sjekkliste.md` med forventet observasjon per steg. Xcode-/simulatorkjøring via Codex/Macen (`lesson.codex-sandbox-cannot-build-cellscaffold`: lange bygg som detached script, ikke arbeidskø). | `test.matrise.device-profiles`, `test.matrise.iphone-checklist` | Claude (profiler, script, sjekkliste), Codex/Xcode (kjøring), Kjetil (iPhone) | `#devices`, `handoff/iphone-sjekkliste.md` |
| **11** | `…apns.real-sandbox-send` (T5.5) | CellScaffold, script | Bytt stub-transport mot ekte; ett varsel til Kjetils iPhone via `api.sandbox.push.apple.com`; Apple svarer 200 + `apns-id`; varselet vises; trykk åpner appen. **Blokkert til Kjetil har: satt `APNS_*` på skyscaffoldet, bygd appen med push-entitlement fra Xcode, og gitt token (appen registrerer det selv via WP2).** Bundle-ID er ikke avklart. | `test.apns.real-sandbox-send` | Kjetil (oppsett), Claude (script, logg) | `#apns-real` |
| **12** | `pkg.std.everything-works`, `purpose://candidate.testmatrise.root`, `…cloud-scaffold-starts-a-chat-on-a-phone` (T5 er forelder: grønn når T5.1–T5.4 er grønne og T5.5 er grønn eller `blocked` med grunn) | alle | Samle `TESTRESULT.md#matrise` (scenario × miljø × enhet × resultat, `blocked` med grunn); full regresjon mot main; docs i samme endring med «Last verified against code»; STATUS.md; lærdommer inn i registeret. | `test.build`, `test.regression`, `test.docs-updated`, `test.status-current` | Claude | `#matrise`, `ACCEPT.md` |
| **13** | `…invite.resolve-recipient-to-an-entity` (ny, 06.10) | CellProtocol (`audienceEntity` i `HavenInvitePublication`, valgfritt, signert, kodes bare når satt), CellScaffold (invitasjonscelle), Binding (butler) | Når avsenderen skriver et navn eller et endepunkt, slår invitasjonscellen opp om det finnes en entitet: (a) i avsenderens egne relasjoner, (b) i registre i scaffolds eid av andre (bare via avtale, aldri som katalog), (c) ellers: ingen treff. Treff → billetten publiseres med `audienceEntity`, og push er mulig. **Flere mulige treff → butleren spør avsenderen; vi velger aldri selv.** Ingen treff → ingen push; mottakeren får veien inn i HAVEN via landing (invitasjonsflyten som finnes) slik at de kan svare og delta i chat. 13a (egne relasjoner) kan bygges nå; 13b (andres registre) **avhenger av invitasjons-PDD WP13 `no-membership-oracle` og WP14 `lookup-needs-agreement`**; 13c bruker eksisterende landing. | `test.invite.resolve-own-relations`, `test.invite.resolve-ambiguous-asks`, `test.invite.unresolved-falls-back-to-landing`, `test.apns.unresolved-not-pushed` (13b: `test.invite.resolve-other-scaffold-by-agreement` — blocked) | Claude | `#resolve` |

## 3. Det som stanser oss, og hvem som eier det

| Stans | Stanser | Eier | Status |
|---|---|---|---|
| Invitasjon runde A del 2 (landing, reply, gravstein, 410, sender-status i CellScaffold + Binding) | WP4 (flate/GET), WP7, WP8b, WP9b, T5-kjeden til chat | invitasjons-PDD (Claude) | ikke skrevet. Foreslår at den tas rett etter fase 1 her |
| WP7 i invitasjons-PDD (aksept → to envelopes → ChatCell) | WP7, WP8b, WP9b | invitasjons-PDD | ikke skrevet |
| Palazzo-vert/miljø og kelner-identitet | WP9b | Kjetil | **åpent** — svaret på «hvor kjører Palazzo?» er ikke gitt; vi bruker testentitet og leser bare prod |
| Ja til lesing fra prod | WP9a | Kjetil | ikke gitt som eget ja til selve skriptet |
| `APNS_*` på skyscaffold, push-entitlement, bundle-ID, token | WP11 | Kjetil | ikke satt |
| Mac-ens `/usr/local/bin/python3` ødelagt | alle script som bruker python | Kjetil (valgfritt) | omgått: script velger `/usr/bin/python3` |

## 4. Kontrakter, dataflyt, handoff (pakkeartefakter)

- `contract/apns_invite_v1.json` + `contract/fixtures/{positive,negative}` + `contract/validate_contract.py` — **finnes (utkast)**; `python3 contract/validate_contract.py` ga 06.10 «RESULT: 11 grønne, 0 røde», med riktig feilgrunn på hver negative fixture. Utkastet er ikke implementert i noen kode.
- `dataflow.md` — kanter E1–E14, merket ny/finnes.
- `handoff/README.md` — rekkefølge, hva som er planlagt og hva som finnes, hva Kjetil må gjøre selv.

## 5. Tall å forvente (fra rapporter, ikke fra kjøring — WP0 måler)

Fra #51 (26.09): HavenInviteRoundATests 15/15, CellBaseTests 1277/0 feil på CellProtocol main 81601a6. Gjeldende main er nå 253b4af (ikke målt). Binding- og CellScaffold-tallene er ikke målt i denne PDD-en; WP0 skriver dem. Forventet nye tester her: ≈ 30–40 (T5.1–T5.4 ≈ 20, T1/T8a ≈ 8, profiler ≈ 4–8) — et anslag, ikke en fasit.

## 6. Planbytter

- 2026-10-06: plan skrevet etter G1.
- 2026-10-06 (etter G2): **WP13 lagt til, WP2/WP3 endret.** Funn ved lesing av `HavenInviteTicket`/`HavenInvitePublication`: en invitasjon er adressert til en endepunkt-hash, ikke en entitet, så «audience-token treffer» (spec T5.3) kan ikke avgjøre hvilken telefon som er den inviterte, og en entitet som selv oppgir en hash kan få en fremmeds varsel. Kjetils regel (chat 06.10): invitasjonscellen skal slå opp navn/endepunkt mot en entitet — i egne relasjoner eller registre i andres scaffolds — og når ingen HAVEN-tilstedeværelse finnes skal mottakeren få en vei inn i HAVEN for å svare og delta i chat. Konsekvens: push adresseres til den oppslåtte entiteten (`audienceEntity` i signert publisering), registreringen bærer ingen endepunkt-hash, flere treff gir spørsmål til avsender, ingen treff gir landing og ingen push. Kontrakt 1.1.0-draft og dataflyt (E4b) oppdatert.

## 7. Status per arbeidspakke (06.10, etter fase 1)

| WP | Status | Bevis |
|---|---|---|
| 0 baseline | **ferdig** | TESTRESULT.md `#build`, `#regression`; `handoff/baseline-20261006-140714/` |
| 1 payload + kontrakt (T5.2) | **ferdig** (gren, ikke merget) | `InviteApnsPush.swift` + 9 tester grønne; kontrakt 1.2.0, validator 12/0 |
| 2 token hører til entiteten (T5.1) | **ferdig** (gren, ikke merget) | `HavenPushRegistration.swift` (CellProtocol, 17 tester) + `PushRegistryService`/`FilePushRegistryStore` (CellScaffold, 3 tester). **Ikke gjort:** Vapor-rutene `POST /push/register` og `/push/revoke` og Binding-siden (signert registrering fra appen) |
| 3 bare den inviterte (T5.3) | **ferdig** (gren, ikke merget) | `HavenInvitePushPlanner` (14 tester) + `InvitePushDispatcher` (8 tester). **Ikke gjort:** kobling fra `publish`-ruten i `VaporInviteLanding` til dispatcheren; tombstone-ledgeren er ikke persistert i scaffoldet ennå (kommer med invitasjon runde A del 2), så dispatcheren tar den som parameter |
| 4 tap åpner invitasjon (T5.4) | ikke startet | avhenger av runde A del 2 |
| 5 T6 push | **ferdig** | TESTRESULT.md `#push` |
| 6 to/tre lokale scaffolds | skript skrevet, **ikke kjørt** | `handoff/two-scaffolds.sh` |
| 7 T1 tre på samme scaffold | ikke startet | |
| 8a admin kommer ikke inn på annen scaffold | ikke startet | |
| 8b T2 chat | blocked | runde A del 2 + invitasjons-WP7 |
| 9 prod read-only / staging | blocked | Kjetils eget ja; Palazzo-vert |
| 10 enhetsprofiler + iPhone | profiler, `matrix.sh`, sjekkliste skrevet; **ikke kjørt** | `handoff/profiles/`, `matrix.sh`, `iphone-sjekkliste.md` |
| 11 ekte sending (T5.5) | blocked | Kjetil: APNS_*, entitlement, token, bundle-ID |
| 12 matrise/docs/regresjon | pågår | denne tabellen, TESTRESULT.md |
| 13a egne relasjoner | **delvis**: `audienceEntity` i signert publisering + beslutning ved manglende/ugyldig entitet ferdig; selve oppslaget i invitasjonscellen ikke skrevet | planlegger- og dispatcher-testene |

**Rekkefølgen for utgivelse:** CellProtocol-grenen merges og får ny tagg → CellScaffold løfter pinnen og får de to `try`-rettelsene → Binding. Før det kan ingenting av dette brukes i en deployet scaffold.
