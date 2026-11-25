# TESTRESULT — Entitetsutvidelse som virker

Ført 2026-11-25. Alt under er kjørt på Linux i skyen (Docker `swift:6.1-noble`), mot
CellProtocol-grenen `claude/entitetsutvidelse-leveranse-1` (tre commits oppå `origin/main` `80f87ce`).
**Ikke kjørt på Mac ennå.** CellApple bygges ikke på Linux, så ankercellen i CellApple er skrevet,
men ikke kompilert. På Linux står CellVapor-ankeret inn for begge i ankertestene.
Grenen er ikke pushet og har ingen PR. Lappene ligger i prosjektfilene under
`masterhaven26/pdd-entitetsutvidelse-som-virker/cellprotocol-patches/`.

| Test | Formål | Status | Bevis |
|---|---|---|---|
| test.utvidelse.baseline | A0 | målt | [#baseline](#baseline) |
| test.utvidelse.agreement-linked | A1 | grønn på Linux | [#agreement-linked](#agreement-linked) |
| test.utvidelse.portable-admit | B1 | grønn på Linux | [#portable-admit](#portable-admit) |
| test.utvidelse.portable-negative | B1 | grønn på Linux | [#portable-negative](#portable-negative) |
| test.utvidelse.fresh-passkey | B2 | grønn på Linux | [#fresh-passkey](#fresh-passkey) |
| test.utvidelse.host-sets-audience | B2 | grønn på Linux | [#host-sets-audience](#host-sets-audience) |
| test.utvidelse.revoke-propagates, stale-status-denied | B3 | venter (WP4) | — |
| test.utvidelse.parity-fixtures, vocabulary, any-scaffold | C1–C3 | venter (WP5) | — |

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

## Kjøringer

| Kjøring | Tester | Feil |
|---|---|---|
| CellBase, filter `EntityLink\|EntityExtensionAgreement\|IdentityLink` | 52 | 0 |
| Ankertester (CellVapor-ankeret) | 30 | 0 |
