# TESTRESULT — invitasjon og tillit

## #build

### WP0 — baseline 2026-09-26 (etter #47 og #50 på CellProtocol main)

Ren måling i `~/Build/pdd-check/` med pinner lest fra CellScaffold sin Package.swift. Logg:
`wp0-20260926-131311.log` (kjørt via entitetsdata sitt `downstream.sh`).

| Prosjekt | Mot CellProtocol main 7577d74 | Mot d9bd69f (runde 2-branchen, samme innhold) |
|---|---|---|
| CellScaffold @ 6f5b99ef (DiMyMint 1d75a2d, Micro a65e202) | **Build complete** (58,5 s) | **Build complete** |
| Binding @ 8ce634f6 | **BUILD SUCCEEDED** | **BUILD SUCCEEDED** |

CellProtocol main selv: 1262/1262 CellBaseTests på d9bd69f (entitetsdata TESTRESULT.md#runde2).
Baseline er grønn. Runde A kan starte fra 7577d74.

## #rundeA

### Del 1 — CellProtocol, WP1–WP5 (2026-09-26 kl. 13:40–13:47)

Kjørt av `handoff/rundeA/rundeA.sh --go` i et ferskt worktree fra origin/main 7577d74. Logg:
`rundeA-run-20260926-134004.log` (+ `.full.log`, `.full.log.new`, `.full.log.alle`).

| Trinn | Resultat |
|---|---|
| Patch (`rundeA.patch`) mot 7577d74 | passer, 5 endrede + 3 nye filer |
| `swift build` | OK |
| `HavenInviteRoundATests` (ny) | **15/15**, 0 feil |
| Hele `CellBaseTests` | **1277 kjørt, 2 hoppet over, 0 feil** (siste «Executed»-linje, jf. lesson.green-gate-must-read-the-last-summary-line) |
| Commit / branch | a82e9f4 på `pdd/invitasjon-runde-a` |
| PR | https://github.com/Digipomps/CellProtocol/pull/51 (utkast, CI avgjør) |

Hva testene dekker, per WP (alle med to simulerte entiteter, egne vaults, tilfeldige UUID-er):

| WP | Test (§5) | Bevis |
|---|---|---|
| 1 M | `test.invite.sender-is-domain-identity` (halvdel) | `identityDomain` («id») ligger under billettens signatur; bytte av domene etter signering gir `bad_signature`; billett uten «id»/«bs» (eldre app) dekoder og verifiserer fortsatt |
| 2 O | `test.invite.expired-is-dead` (CellProtocol-delen) | standard 14 d, maks 90 d; billett som påstår 91 d avvises som `ttl_too_long` selv med gyldig signatur; utløpt billett avvises på publisering, kontaktforespørsel og svar (`ticket_expired`); publisering må være enig med billetten om `expiresAt` |
| 3 C+D | `test.invite.claim-is-marked` | `HavenContactBasisV1`: felt er `unconfirmed` med opphav; ukjent nøkkel, fritekst og flerlinje avvises; bekreft/slett per felt |
| 4 G+R | `test.invite.shown-equals-held`, `test.invite.private-notes-never-leave` | billetten bærer nøyaktig grunnlaget (rekkefølge likegyldig, ett felt mer/mindre = ulikt); sentinel fra `privateNotes` finnes ikke i token, publisering, kontaktforespørsel, endepunkt-payload eller e-posttekst |
| 5 E+F | `test.invite.tombstone-survives-reimport`, `test.invite.sender-sees-answered-only` (CellProtocol-delen) | «aldri» → verifiserbar gravstein som nekter ny billett fra samme utsteder til samme mottaker, overlever billettens utløp og JSON-rundtur; utsteder kan ikke si «aldri» på mottakers vegne; endret/flyttet svar avvises; «ikke nå» er ikke gravstein; avsender ser `published/answered/expired/revoked` — aldri `opened`, og «ikke nå» = «aldri» |
| T (½) | `test.invite.sealed-to-invitee` (første halvdel) | `ChatInvitationAcceptance.inviteeKeyAgreementKey` og `HavenInviteContactRequest.senderKeyAgreementKey` ligger under signaturen; byttet nøkkel avvises; identiteten avsender bygger fra aksepten kan forsegles til |

**Ikke dekket ennå (del 2, CellScaffold + Binding, starter når #51 er på main):** landing viser grunnlaget; `POST reply` tar `decision`; scaffoldet skriver gravstein og nekter publisering mot den; 410 på utløpt; sender-status-ruten serverer `HavenInviteSenderReport`; Binding `invite.prepare` tar `identityDomain`, bygger `basis` fra kontaktposten, sjekker gravstein før ny billett, og oversikten viser bare `answered`. `test.invite.no-second-message` (ingen jobb/timer) og `test.invite.decline-without-entity` (landing uten konto) hører til del 2.

## #invite
Se #rundeA (del 1). Del 2 kommer.

## #negative
Se #rundeA (del 1): ttl_too_long, ticket_expired, bad_signature ved tukling, forfalsket «aldri», fritekst i grunnlag.

## #trace
(ikke kjørt ennå)

## #kjetil-vegar
(ikke kjørt — krever WP0–WP10 grønne)
