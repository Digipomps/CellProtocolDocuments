# TESTRESULT — Entitetsutvidelse som virker

Ført 2026-11-25. Alt under er kjørt på Linux i skyen (Docker `swift:6.1-noble`), mot
CellProtocol-grenen `claude/entitetsutvidelse-leveranse-1` (tre commits oppå `origin/main` `80f87ce`, pluss WP4 og
prøvesettet fra WP5 som ikke er committet), og mot lokale grener med samme navn i PyCellProtocol og gocellprotocol.
**Ikke kjørt på Mac ennå.** CellApple bygges ikke på Linux, så ankercellen i CellApple er skrevet,
men ikke kompilert. På Linux står CellVapor-ankeret inn for begge i ankertestene.
Grenen er ikke pushet og har ingen PR. Lappene ligger i prosjektfilene under
`masterhaven26/pdd-entitetsutvidelse-som-virker/cellprotocol-patches/`, `pycellprotocol-patches/` og `go-patches/`.

| Test | Formål | Status | Bevis |
|---|---|---|---|
| test.utvidelse.baseline | A0 | målt | [#baseline](#baseline) |
| test.utvidelse.agreement-linked | A1 | grønn på Linux | [#agreement-linked](#agreement-linked) |
| test.utvidelse.portable-admit | B1 | grønn på Linux | [#portable-admit](#portable-admit) |
| test.utvidelse.portable-negative | B1 | grønn på Linux | [#portable-negative](#portable-negative) |
| test.utvidelse.fresh-passkey | B2 | grønn på Linux | [#fresh-passkey](#fresh-passkey) |
| test.utvidelse.host-sets-audience | B2 | grønn på Linux | [#host-sets-audience](#host-sets-audience) |
| test.utvidelse.revoke-propagates | B3 | grønn på Linux, ikke committet | [#revoke-propagates](#revoke-propagates) |
| test.utvidelse.stale-status-denied | B3 | grønn på Linux, ikke committet | [#stale-status-denied](#stale-status-denied) |
| test.utvidelse.parity-fixtures | C1 | grønn i Swift, Python og Go | [#parity-fixtures](#parity-fixtures) |
| test.utvidelse.vocabulary, any-scaffold | C2, C3 | venter | — |

## baseline

WP0, på `origin/main` `80f87ce`, før noe var endret. En hel lenket nøkkel spør om en nøkkelsti
som entitetens eiernøkkel har avtale på:

```
ENTITY-EXTENSION agreement-linked: allowed=false path=deniedNoGrant code=agreement_or_proof_required
```

På en vert som ikke har sett lenkeseremonien, fantes det ingen inngang som tok imot beviset.
Svaret er det spesifikasjonen sa. Ingen stoppregel utløst.

Hele Linux-riggen: 1493 tester. 27 testtilfeller er røde på `main` fordi riggen mangler
fixturefiler (Commons, Skeleton WPR1, OID4VP, FileCrypto, InteropFixtures, OrganizationVault,
OwnerAttach, EntityRelationPerspective). De samme 27 er røde på grenen etter WP1. Ingen nye.

## agreement-linked

`Tests/CellBaseTests/EntityExtensionAgreementTests.swift`, 7 tester, 0 feil.

```
ENTITY-EXTENSION agreement-linked: allowed=true path=signedContract code=linked_identity_agreement
```

Dekker også: en avgrenset lenke får ikke avtalen, en trukket lenke mister den, en nøkkel fra en
annen entitet får den ikke, en organisasjon regnes ikke som samme entitet, og en kopi av
nøkkelbeskrivelsen uten privatnøkkel får den ikke.

## portable-admit

`EntityLinkAdmissionTests` (5), `EntityLinkAdmissionChallengeTests` (4) i CellBase og
`EntityAnchorLinkAdmissionTests` ved ankercellen.

```
ENTITY-EXTENSION portable-admit before: allowed=false path=deniedNoGrant
ENTITY-EXTENSION portable-admit after: allowed=true code=linked_identity_proof
```

Ved ankeret: verten deler ut en utfordring, tar imot beviset, lagrer lenken og kjenner nøkkelen
igjen etter omstart uten at beviset vises på nytt. Samme konvolutt en gang til avvises med
`link_admission_challenge_unknown_or_expired`. En lenke som er trukket på verten, kommer ikke
tilbake ved å vise beviset igjen. Utfordringen brukes én gang, lever fem minutter, og verten
holder høyst 256 ubesvarte.

**Åpent:** de to inngangene (`identityLinks.admissionChallenge`, `identityLinks.admit`) kan i dag
bare kalles av en nøkkel verten alt kjenner som entiteten. Hvordan en ukjent enhet når dem, er
spurt Kjetil 2026-11-25. Testene leverer beviset inn fra eierens økt.

## portable-negative

Hver avvisning har sin egen kode (`EntityLinkAdmissionTests.testEveryOtherProofIsRefusedWithItsOwnCode`
og ankertesten): fremmed utsteder `link_credential_issuer_is_not_the_entity`, bevis for en annen
nøkkel `link_presentation_holder_mismatch`, kopi uten privatnøkkel `link_presentation_invalid`,
utløpt `link_credential_expired`, avgrenset lenke `link_credential_not_whole`, feil domene
`link_credential_domain_not_approved`.

## fresh-passkey

`EntityLinkFreshPasskeyTests`, 6 tester, 0 feil.

```
ENTITY-EXTENSION fresh-passkey with evidence: admitted
ENTITY-EXTENSION fresh-passkey none: link_credential_fresh_auth_missing
ENTITY-EXTENSION fresh-passkey wrong hash: link_credential_fresh_auth_invalid: challenge does not match request hash
```

Bekreftelsen ligger inne i det signerte beviset. Settes den inn etterpå, ryker signaturen
(`link_credential_signature_invalid`). Seremonien avviser et bevis som bærer en annen bekreftelse
enn godkjenningen.

**Grense, sagt rett ut:** testene bruker en bekreftelse med riktig form, ikke en ekte
WebAuthn-signatur. Selve signaturen sjekkes av en funksjon verten installerer. Hva den kan
sjekke på en ny vert, avhenger av om verten kjenner passkeyens offentlige nøkkel. Det er ikke
bygget, og hører til koblingen i hver vert.

**Antakelse:** et bærbart bevis kan gjelde i høyst 30 dager. Uten at klienten ber om det, er
levetiden som før, fem minutter.

## host-sets-audience

`EntityAnchorLinkAdmissionTests.testTheHostNotTheEnvelopeSaysWhoTheHostIs`.

```
ENTITY-EXTENSION host-sets-audience cloud other audience: audienceMismatch(expected: "second-host.example", actual: "staging.haven.digipomps.org")
```

En konvolutt der alle signaturer holder, men som er laget for en annen vert eller et annet
opphav, avvises. Samme konvolutt laget for denne verten fullføres.

**Grense:** regelen gjelder når verten har satt publikum og opphav i
`IdentityLinkRuntimePolicy`. En vert som ikke har satt dem, leser fortsatt konvoluttens egne
verdier, som før. CellScaffold må sette dem ved oppstart; det er kobling, ikke en tilgangsregel.

## revoke-propagates

`EntityLinkStatusListTests.testARevokedLinkStopsWorkingOnTheNextHostWithinTenMinutes`. Klokken er registerets egen,
flyttet av testen. t er tiden siden vert 2 fikk sin første liste.

```
ENTITY-EXTENSION revoke-propagates t+0s no list: allowed=false code=linked_identity_status_list_stale
ENTITY-EXTENSION revoke-propagates t+0s fresh list: allowed=true code=linked_identity_proof
ENTITY-EXTENSION revoke-propagates t+60s revoked at home, old list: allowed=true code=linked_identity_proof
ENTITY-EXTENSION revoke-propagates t+601s no new list: allowed=false code=linked_identity_status_list_stale
ENTITY-EXTENSION revoke-propagates t+601s new list: allowed=false code=linked_identity_not_on_status_list
```

Lenken ble trukket på vert 1 ved t+60 s. Uten ny liste sluttet den å virke på vert 2 ved t+601 s, altså
9 minutter og 1 sekund etter trekkingen, og aldri senere enn 10 minutter. Med en ny liste slutter den straks.

**Funn som endret formen på listen:** en trukket enhet er fortsatt en hel nøkkel på vert 2 til listen blir
gammel, og kan i de minuttene signere et bevis for enda en nøkkel som vert 1 aldri ser. En liste over trukne
lenker kunne aldri nevnt den. Listen er derfor en liste over **gyldige** bevis, og bare **eiernøkkelen** kan peke
ut hvem som signerer den. Prøvd i `testALinkTheHomeHostNeverSawIsNeverUsableOnTheNextHost`:

```
ENTITY-EXTENSION status-list link the home never saw: allowed=false code=linked_identity_not_on_status_list
```

Ved ankercellen (`EntityAnchorLinkStatusTests`, 2 tester): `identityLinks.designateStatusAuthority` godtas bare
fra eiernøkkelen, `identityLinks.statusList` gir en signert liste, tilbakekalling tar beviset av listen, og
`identityLinks.acceptStatus` tar imot listen på neste vert.

**Antakelser:** listen signeres av en egen statusnøkkel i vertens nøkkelhvelv, pekt ut av eiernøkkelen én gang.
Hvordan listen kommer fra vert til vert er ikke bygget; etter G1 bærer entitetens egen klient den.

**Ikke committet:** fire av mine egne tester fra WP2 blir røde av denne pakken, fordi en lenke på neste vert nå
også trenger en fersk liste: `EntityLinkAdmissionTests` (3) og `EntityAnchorLinkAdmissionTests` (1). Etter
stoppregelen i PLAN.md er de ikke rørt. Kjetil er spurt 2026-11-25.

## stale-status-denied

`EntityLinkStatusListTests.testWithoutAFreshListTheNextHostRefusesAndTheHomeHostDoesNot`.

```
ENTITY-EXTENSION stale-status-denied admitted key, list 11 min old: own=allowed=false code=linked_identity_status_list_stale agreement=allowed=false code=linked_identity_status_list_stale
ENTITY-EXTENSION stale-status-denied key linked on this host, same moment: own=allowed=true code=linked_identity_proof agreement=allowed=true code=linked_identity_agreement
```

Hver annen liste avvises med egen kode (`testEveryOtherListIsRefusedWithItsOwnCode`): ukjent eiernøkkel, annen
entitet, signert av feil nøkkel, endret etter signering, datert fram i tid, for gammel ved mottak, eldre enn den
verten har, og eldre utpeking enn den verten har.

## parity-fixtures

`fixtures/entity-link/v1/link-fixtures.v1.json` lages av Swift-testen `EntityLinkParityFixturesTests`: 13 rader om
å slippe inn en lenke og 9 rader om statuslisten, signert med de offentlige testnøklene fra `fixtures/interop/v1`.
Filen er kopiert uendret til PyCellProtocol (`tests/fixtures/entity-link/v1/`) og gocellprotocol
(`interop/testdata/entity-link/v1/`).

| Språk | Rader | Samme svar og kode som raden sier |
|---|---|---|
| Swift (`EntityLinkParityFixturesTests`) | 22 | 22 |
| Python (`tests/test_link_admission_fixtures.py`) | 22 | 22 |
| Go (`interop/link_admission_test.go`) | 22 | 22 |

Hele Python-suiten: 352 bestått, 1 hoppet over. Hele Go-suiten: ok.

**Rekkevidde, sagt rett ut:** Python og Go har avgjørelsene som funksjoner (`interop/link_admission.py`,
`interop/link_admission.go`). Cellene i de to scaffoldene bruker dem ikke ennå, så `test.utvidelse.any-scaffold`
venter. `test.utvidelse.vocabulary` venter også; de to ordene for hel lenke står i dag ett sted i hvert språk.

## Kjøringer

| Kjøring | Tester | Feil |
|---|---|---|
| CellBase, filter `EntityLink\|EntityExtensionAgreement\|IdentityLink` | 52 | 0 |
| Ankertester (CellVapor-ankeret) | 30 | 0 |
| Etter WP4: `EntityLinkStatusListTests` | 4 | 0 |
| Etter WP4: ankertester | 32 | 6 påstander i 1 test fra WP2, som ventet |
| Etter WP4: CellBase, samme filter som over | 56 | 3 tester fra WP2 røde, som ventet |
| `EntityLinkParityFixturesTests` | 3 (1 hoppet over) | 0 |
