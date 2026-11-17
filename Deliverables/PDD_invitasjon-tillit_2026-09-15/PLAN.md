# PLAN — invitasjon og tillit

Oppgavemappe: `PDD_invitasjon-tillit_2026-09-15` · Skrevet 2026-09-24 · **G2 godkjent 2026-09-26**

G1 godkjent 2026-09-24. G1-GUI godkjent 2026-09-24 (v1-bildene; `avsender-forhandsvisning-v2.png`
med private notater venter for seg). Én arbeidspakke per bladformål, i avhengighetsrekkefølge.
Ingen pakke er «ferdig» før testene den navngir er grønne og utdataene ligger i `TESTRESULT.md`.
Et dokument om leveransen teller aldri som leveransen.

## 0. Tre ting du bør vite før du leser videre

**0.1 Målet for runde A er én ting: Kjetil inviterer Vegar, og de får en samtale.** Over invite og
chat, ikke correspondence (Kjetil 23.09). Alt i runde A er det som må være sant for at den testen skal
bety noe. Registrene (A1–A6, K, L) er ikke på veien dit og ligger i runde C. Flytting hjem (P) er
runde B, fordi den trenger runde A for å ha noe å flytte.

**0.2 Det meste finnes.** Brief-auditen i FORMAALSSPEC §0.2 (lest mot origin/main 23.09) sier at
billett, publisering, landing, kontaktforespørsel, butler-forslag og chat-invitasjon alle finnes og
er testet hver for seg. Runde A er derfor mindre nybygging og mer *håndheving*: gjøre det som
finnes til det formålene sier — ett svar synlig for avsender, utløp som virker overalt, gravstein,
grunnlag skilt fra private notater, ingen `opened` mot avsender — og så koble leddene i én kjede.
Det som faktisk ikke finnes: gravstein (E/F), hjelp på invitasjonssiden (I), «hva som holdes om deg»
på landing (G), flytting (P), og alt i runde C.

**0.3 Samme arbeidsmåte som entitetsdata runde 1.** Jeg skriver Swift; bygg og test kjøres på macOS
via idempotente skript i `handoff/` startet fra Finder (`pkg.std.codex-handoff`). Egne worktrees
per repo, aldri i det delte utsjekket, aldri git gjennom monteringen. Baseline er en ekte kjøring
mot `origin/main` før noe endres — og den var rød nedstrøms 22.09 av grunner utenfor denne oppgaven
(`PDD_entitetsdata-egen-kontroll/TESTRESULT.md#build`). WP0 avgjør om den fortsatt er det.

## 1. Rekkefølgen, og hvorfor

```
WP0 baseline (tre repoer, origin/main, ekte kjøring)
  │
  ├─ Runde A — kjeden Kjetil → Vegar
  │    WP1 M  avsender = domenets identitet        ─┐
  │    WP2 O  utløp håndheves overalt               ├─► WP6 B  ett objekt, to leveranser
  │    WP3 C+D grunnlag: uverifisert, med opphav, ─┤       │
  │            bare det som sendes                  │       ▼
  │    WP4 G+R hva som holdes = grunnlaget,        ─┘   WP7 H  aksept → to konvolutter → chat-invitasjon
  │            private notater forlater aldri              │
  │    WP5 E+F én melding, gravstein, «besvart —          ▼
  │            ikke nå», nei uten konto              WP8 N  direkte svar → forseglet entitet hos avsender;
  │                                                        app-svar → ingenting hos avsender
  │    WP9  I  hjelp på invitasjonssiden (kan ikke handle)
  │    WP10 J+Q flatene etter bildene, nåbarhet, paritet
  │    WP11 Kjetil–Vegar: kjeden kjørt av to ekte entiteter
  │
  ├─ Runde B — WP12 P  flytt hjem
  │
  └─ Runde C — registre
       WP13 A1 · WP14 K · WP15 L · WP16 A2 · WP17 A5 · WP18 A4 · WP19 A6 · WP20 A3
```

WP1–WP5 er uavhengige av hverandre og kan gå parallelt. WP6 trenger dem alle, fordi «samme
tilstand gjennom begge veier» bare kan testes når tilstandene er de rette. WP8 trenger WP7 (aksept)
og entitetsdata runde 2 (`admin-cannot-enter-foreign-cell`) — den negative testen er den samme.

## 2. Arbeidspakkene

Kolonnen «Utfører»: **Claude** = skriver kode og tester, kjører dem via `handoff/` på macOS;
**Codex** = bygger og retter i Xcode der SwiftUI/Leaf må sees kjørende; **Kjetil** / **Vegar** =
mennesker. «Repo» er der endringen lander.

| WP | purposeRef | Repo | Hva som gjøres | Tester (§5) | Utfører | Gir til §3 |
|---|---|---|---|---|---|---|
| **0** | `pkg.std.everything-works` | alle tre | Ren eksport av origin/main per repo (`git archive`), bygg + full test, tre ganger om noe er rødt. Er nedstrøms fortsatt rød (SkeletonEditor, swift-crypto): registreres som egen sak med eier, ikke omgås. | `test.build`, `test.regression` | Claude | `TESTRESULT.md#build` |
| **1** | M `sender-is-the-domain-identity` | CellProtocol, Binding | `invite.prepare` tar `identityDomain`; billettens `issuer` er domenets identitet; `acceptContactRequest` og chat-invitasjon avviser billett fra annen domeneidentitet til samme relasjon. | `test.invite.sender-is-domain-identity` | Claude | `#invite` |
| **2** | O `expires-by-itself` | CellProtocol, CellScaffold, Binding | `isExpired` håndheves på landing (`GET`), reply (`POST`), `acceptContactRequest` og chat-aksept; `ttlDays` 14 standard, klippes til 90; oversikten viser `expired`. | `test.invite.expired-is-dead` | Claude | `#invite` |
| **3** | C `claim-about-another` + D `minimum-for-the-send` | CellProtocol (post-form), Binding | Kontaktpost får `basis` (navn, endepunkt, `origin{file,date,column}`, `status: unconfirmed`) og `privateNotes` som to felt; import for invitasjon persisterer bare `basis`-feltene invitasjonen bruker. Kravflyt (rett/slett) som handling på posten, med spor. | `test.invite.claim-is-marked`, `test.invite.subject-can-erase`, `test.invite.minimum-persisted` | Claude | `#claim`, `#negative` |
| **4** | G `recipient-sees-what-is-held` + R `private-notes-never-leave` | CellProtocol, CellScaffold | Billetten bærer `basis`-feltene (ikke bare `greetingName`); landing og app viser dem som liste med opphav; sentinel i `privateNotes` finnes ikke i billett, publisering, kontaktforespørsel eller landing-HTML; `privateNotes` er ikke lesbar for AIGateway-ruter med egress. | `test.invite.shown-equals-held`, `test.invite.private-notes-never-leave` | Claude | `#claim`, `#negative` |
| **5** | E `no-automatic-reminders` + F `decline-without-account` | CellProtocol, CellScaffold, Binding | Reply på landing tar `decision: yes / notNow / never` uten entitet; `never` gir en signert gravstein (ny type `HavenInviteTombstone`) som `invite.prepare` sjekker før ny billett til samme endepunkt, og som overlever reimport; avsender ser `answered` for begge nei (ikke `declined`), og `opened` vises ikke; ingen jobb/timer sender melding nr. 2. | `test.invite.no-second-message`, `test.invite.tombstone-survives-reimport`, `test.invite.decline-without-entity`, `test.invite.sender-sees-answered-only` | Claude | `#negative`, `#invite` |
| **6** | B `one-object-two-deliveries` | CellProtocol | Samme signerte billett gjennom landing-vei og app-vei ender i samme `HavenInviteLifecycle` med samme `ticketID`; harness med to vaults (tilfeldige UUID-er — `MockIdentityVault` kolliderer). | `test.invite.same-object-both-paths` | Claude | `#invite` |
| **7** | H `acceptance-is-bilateral` + T `acceptance-carries-the-key-to-seal-to` | CellProtocol, CellScaffold | Et ja gir én `EntityBatchPersistEnvelope` per entitet (relasjon + avtale + chronicle) og en `ChatInvitationArtifact` fra avsender til mottakers identitet; mottakers aksept gjør ChatCell klar i `invitedIdentities`-modus. **Aksepten og kontaktforespørselen bærer nøkkelavtale-nøkkelen**, så avsender kan forsegle fra første melding. Ingen konvolutt uten eierbevis. | `test.invite.acceptance-two-envelopes`, `test.invite.sealed-to-invitee` | Claude | `#trace`, `#invite` |
| **8** | N `direct-reply-creates-a-sealed-entity-at-sender` | CellScaffold | Landing-ja uten app: scaffoldet oppretter EntityAnchor forseglet til nykommerens nøkkel (genesis, `trigger: .invitationReply`); avsender og admin nektes lesing/skriving/handlinger. App-ja: ingen ny anchor på scaffold. **Avhenger av entitetsdata runde 2 WP4.** | `test.invite.direct-reply-anchor-is-theirs`, `test.invite.app-reply-leaves-nothing-at-sender` | Claude | `#negative`, `#invite` |
| **9** | I `help-chat-cannot-send` | CellScaffold | Hjelp på invitasjonssiden: egen celle uten `send/accept/decline` i kontrakten, svarer fra billetten + faste tekster (ingen modell i runde A — modell er eierens valg og krever AIGateway, entitetsdata WP9–13). | `test.invite.chat-cannot-act` | Claude | `ACCEPT.md#help-chat` |
| **10** | J `ways-in-are-reachable` + Q `the-flow-reads-as-one-trustworthy-path` | Binding, CellScaffold | Avsenderflater (butler-forslag, forhåndsvisning m/ private notater, sendt, oversikt) og landing-HTML etter de godkjente bildene; ordlisten håndhevet; `SkeletonReachabilityAudit` grønn; paritet side om side. | `test.skeleton.no-unreachable-elements`, `test.invite.one-primary-action-per-screen`, `test.gui.parity`, `test.gui.load-time` | Codex (flater), Claude (audit) | `images/` ↔ `ACCEPT.md#parity` |
| **11** | B, H, M, N, Q | — | Kjetil inviterer Vegar via butler; Vegar svarer (a) på landing uten app, (b) i egen HAVEN; samtale i begge tilfeller. Skjermbilder fra begge sider + chronicle-spor. Kjøres først når WP0–WP10 er grønne (`lesson.corr-approval-surfaces-timed-out`). | `test.invite.kjetil-vegar-chain` | Kjetil, Vegar | `#kjetil-vegar` |
| **12b** | U `attachments-sealed-per-recipient` | CellProtocol | Vedlegg i ChatCell via `attachmentStreamV1`; innholdsnøkkel pakket per mottaker i meldingskonvolutten. Bygger på T. | `test.invite.attachment-sealed` | Claude | `#negative` |
| **12** | P `temporary-entity-can-move-home` | CellProtocol, CellScaffold, Binding | Handling `entity.moveHome`: eksport av nykommerens entitetsdata + chat-medlemskap + relasjon, signert av nykommeren, import i app-entitet, re-binding av ChatCell-medlemskap, peker igjen hos avsender. | `test.invite.move-home-carries-everything` | Claude | `#invite` |
| **13** | A1 `only-the-published-is-findable` | CellScaffold (`ContactRegistryCell`) | Oppslag på upublisert endepunkt = samme svar som ikke-eksisterende; ingen medlemskaps-keypath. | `test.invite.no-membership-oracle`, `test.invite.enumeration-refused` | Claude | `ACCEPT.md#no-directory`, `#negative` |
| **14** | K `lookup-carries-an-agreement-not-a-name` | CellProtocol, CellScaffold | Oppslag legitimeres av avtalebevis; verten persisterer avtale-id + tid, ikke identitet. | `test.invite.lookup-needs-agreement` | Claude | `#negative` |
| **15** | L `register-key-is-derived-per-register` | CellProtocol | `RegisterKey.derive(endpoint, registerID)`; klartekst avvises ved publisering. | `test.invite.register-key-unlinkable` | Claude | `#invite` |
| **16** | A2 `register-is-a-host-not-an-owner` | CellScaffold | Ratebegrensning per avtale; bulkuthenting synlig i vertens egen chronicle; oppføringer eies av den som la seg ut. | (A2-verifier: inspeksjon + ratetest) | Claude | `#negative` |
| **17** | A5 `minimum-both-ways` | CellProtocol | Forespørsel bærer `purpose://` + feltliste; svar telles felt for felt; uten formål → ikke besvart. | (A5 negativ test) | Claude | `#negative` |
| **18** | A4 `ask-instead-of-keep` | CellProtocol, Binding | Relasjon uten lokal kopi virker; lokal kopi har utløp og hentes på nytt. | (A4 test) | Claude | `#invite` |
| **19** | A6 `overlap-is-inferred-inside` | Binding | Overlapp regnes i butleren mot registre eieren har tilgang til; nettverks-/resolverfelle; tilgangsforespørsel som synlig handling. | `test.invite.overlap-is-local`, `no-read-from-foreign-cell`, `access-request-is-visible` | Claude | `#negative`, `#invite` |
| **20** | A3 `introduction-inside-an-agreed-relation` | CellProtocol | Introduksjon bare i relasjon med introduksjonsavtale; C ser A; B får hendelse først ved invitasjon. | `test.invite.introducer-sees-asker` (+ A3 negativ) | Claude | `#invite` |

## 3. Det som stanser oss, og hvem som eier det

Oppdatert 2026-09-24 kl. 13:45 etter «Fiks det som blokker»:

| Blokkering | Rammer | Eier | Status |
|---|---|---|---|
| Binding rød på origin/main | WP10, WP11 | — | **borte.** Var Binding 72f6a6c9 + et fastlåst worktree; Binding 8ce634f6 bygger grønt mot CellProtocol main og mot branchen (`PDD_entitetsdata…/handoff/runde1/downstream-20260924-134224.log`). |
| CellScaffold swift-crypto-konflikt | WP2, 5, 7, 8, 9, 13 | — | **borte.** Var en hardkodet DiMyMint-pin i skriptet; med CellScaffold sin egen pin (af41630) bygger den grønt begge veier. `lesson.downstream-pin-must-come-from-the-consumer`. |
| `pdd/entitetsdata-egen-kontroll` ikke pushet | WP8 | — | **pushet** som 94a4bed (e66b7f1 + merge av main 60bcf1d, 1248/1248). Utkast-PR #47 åpen for CI. **Merge er Kjetils ord** — til den er merget finnes genesis ikke på origin/main, og WP8 må bygge mot branchen. |
| Entitetsdata runde 2 WP4 (`admin-cannot-enter-foreign-cell`, to-entitets-harness) | WP8, WP6-harness | denne tråden | ikke startet — neste |
| Ingen vault-fabrikk med unike UUID-er i CellBase-tester | WP6, 8, 12, 20 | denne tråden (lages i WP6) | — |

## 4. Kontrakter, dataflyt, handoff (pakkeartefakter)

- `contract/invite_v1.json` — keypaths og aksjoner på `BindingInvitationCell`, landing-rutene på
  scaffold, chat-invitasjonsaksjonene, og de nye: `decision`, `HavenInviteTombstone`, `basis` /
  `privateNotes`, `entity.moveHome`. Fixtures positive/negative i `contract/fixtures/`,
  `check_fixtures.py` kjører grønt før G2 (`test.cell.contract-fixtures`).
- `dataflow.md` — kantene butler → InvitationCell → scaffold (publish/landing/reply/requests) →
  ContactEndpoint → ChatCell, med hvem som ser hva på hver kant.
- `handoff/rundeA/` — `preflight.sh`, `apply.sh` (dry-run), `verify.sh`, `commit.sh`,
  `downstream.sh`, `rundeA.command`, som i entitetsdata runde 1. Skrives ved oppstart av runde A.

## 5. Tall å forvente (fra rapporter, ikke fra kjøring — WP0 måler)

CellBaseTests: 1244 grønne 22.09 (entitetsdata `TESTRESULT.md#build`), hvorav ChatCellTests 48,
InvitationResidencyTests i Binding 45, ChatWorkbenchParityTests 47. Runde A legger til ≈ 14 tester,
runde B 1, runde C ≈ 12. `lesson.baseline-count-from-report-not-run`: tallene her er forventning.

## 6. Planbytter

- 2026-09-26: T lagt til WP7 (runde A) og U som WP12b (runde B) etter Kjetils spørsmål om vedlegg og kryptert last. Ingen rekkefølge endret. Byttes rekkefølgen, føres det i STATUS.md med dato og hvorfor.
