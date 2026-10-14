STATUS: STOPPET — arvet capacity/timeout i admin-broens feed-test; retting går utenfor alternativ 1

# HD-0196 h2 — bro-signering og avgrenset strict-vault-endring

CP-delen er levert i kladd-PR med grønn grunnmur og CI. Den avgrensede CellScaffold-koden er bevart lokalt; ekte T1 og de nye strict-testene passerer, men samlet AdminNonOwnerBridgeTests er ikke grønn. Den feilende feed-fixturen feiler også med originale HD-0190-vaultfiler og CP-main før h2. Oppdragets stoppregel gjelder: ingen transport-/kvotereparasjon, test-svekkelse eller endring utenfor alternativ 1.

## Hoder og publisering

| Kandidat | Eksakt hode / grunnlag | Status |
|---|---|---|
| CP-base | 97b348483448fb29dfe089bd96ab4d4adb384a76 | Ferskt origin/main før kode |
| CP h2 | 503f6882db16160a8709277e957d70f343414777 | Pushet; [kladd-PR #65](https://github.com/Digipomps/CellProtocol/pull/65), CI 5/5 SUCCESS |
| CellScaffold-base | d726890683d1ad0ccf0f0c70d290a1fb438f01cd | HD-0190-basen |
| CellScaffold h2 | 83985fcb07ec4cf9968c842682746a772e080f5f | Lokal commit, ikke pushet; ingen ny PR eller GitHub-CI |
| Separat kopi av [#286](https://github.com/Digipomps/CellScaffold/pull/286) | 1e0634fed4baf9ff07dbaf5278345f31b53f6a02 + lokal h2-diff og eksakt CP503f688-pinne | Kopien er ikke committet eller testet; originalgrenen er urørt |

CP-commit har bestilt Co-Authored-By-trailer. Ingen merge, tag, deploy eller installerbygg.

## Endringen

Endelig API ble skrevet i PLAN før kode. IdentityVaultProtocol har nytt faktisk krav `signMessageForIdentity(messageData:identity:bridgeConnectContext:)` med legacy-default. CP utsteder en ikke-Codable engangskontekst fra et lokalt holder-håndtak, validerer eksakt transcript og tilbakekaller ved cancel, Task-kansellering, close/renew, feil og terminal avslutning. Offentlige snapshots/decoding bærer ikke holder-tokenet; resolverens beviste lokale requester-kopi beholder det.

Adapteren eier sitt token privat. Bare direkte retur fra den eksisterende possession-validerte bind-inngangen får det; offentlige identitetsoppslag gjør ikke det. Gammel adapter-inngang avviser all kanonisk connect-signering, også med korrekt home. Ny inngang kontrollerer nøyaktig token/binding og videresender samme strict principal og levende kontekst uten tidlig consume.

BrowserClientIdentityVault gjentar home/fingerprint etter siste await og konsumerer konteksten på sin egen actor umiddelbart før uendret synkron privat signer. DEBUG-only interne barrierer og nøkkelkallteller instrumenterer dette punktet. Privat signeringsfunksjon, nøkkelvalg, lagringskode og wire-format er uendret. Dette er avgrenset til §6 Q1: kode som allerede har hele holder-håndtaket eller direkte full underlying-vault-tilgang er ikke prosessisolert av API-et.

## Målt verifikasjon

Tallene er per kjøring; fokus/eksperimenter legges ikke til fullportens antall.

| Kjøring | Resultat |
|---|---|
| CP API-rød på main | Compile exit1: nye typer manglet; ingen runtime-telling |
| CP finalfokus | 29 tester, 0 feil, exit0 |
| CP fire guard-mutanter + to eksterne compile-prober | Alle seks forventet exit1; navngitte røde tester/access-/Decodable-avslag, kilde-MD5 gjenopprettet |
| CP full grunnmur på 503f688 | Build/test exit0; 1671 unike utførelser = 1666 bestått + 5 skip, 0 feil |
| CP CI på samme hode | 5/5 SUCCESS, inkludert ordinær macOS-regresjon og Thread Sanitizer |
| Ekte CS baseline, bare CP-pinne endret | AdminScaffold/testmål bygger; to eksisterende tester kjørt, begge feiler, tre failure-events, exit1 |
| Første CS fokus etter h2 | 31 parent-tilfeller: 29 bestått, 1 skip, 1 feilende test med 2 failure-events; exit1. Alle sju nye strict-tester rapporterte grønt, men lagringskontrollen var da ikke tilstrekkelig: filtilhørighet var ikke eksplisitt verifisert; en senere relativ-prefix-guard feilet |
| Ekte T1 i dette fokusløpet | Parent passerer; seed, web-restart og admin-restart kjører hver én child-test med 0 feil |
| Actual-strict siste-consume-mutant | Test exit1, forventet tellerfeil: ett ekstra privat nøkkelkall etter cancel. Kilde-MD5 gjenopprettet |
| Første sluttkontroll med non-vacuity-assert på 6e8d2eb2 | 9 tester, 1 feil, exit1: relativ-prefix-guard gjenkjente ikke vault-filen. Dette beviste ikke at snapshot var tomt |
| Sluttkontroll r2 på c3e68b29 | 9 tester, 1 feil, exit1; async oppstart alene løste ikke filtilhørighetsasserten |
| Sluttkontroll r3 på 83985fcb / CP503f688 | 9 tester, 0 feil, exit0; sju strict + to T1/kontroll. Tre web-child-faser hver 1/0 |
| Full CS-port / #286-kopi | Ikke kjørt etter konstatert stoppvilkår; verken 32/32 eller 33/33 erklæres grønn |

CP-fulltellingen omfatter CellBaseTests 1642, HavenCommonsTests 26 og CellNearbyTests 3. De fem skipped inngår i 1671; siste bundle-footer alene er ikke totaltallet.

## Stoppvilkåret og kausalkontroll

`testRevocationStopsExistingOverviewFeed` gir «Paired bridge delivery failed» og senere timeout. Fixturen bruker Vapor-owner og Ephemeral-visitor, ikke nettleser-vaulten. Bare diagnostisk utskrift av den fangede feilen ble lagt til midlertidig; ingen assertion ble endret. To separate kildekontroller målte:

| CP-kilde | CS-vaultfiler | Målt resultat |
|---|---|---|
| h2 503f688 | Originale d7268906-filer | Én test, to failure-events, exit1; fanget feil `capacity` |
| main 97b3484 før h2 | Originale d7268906-filer | Samme feil, én test, to failure-events, exit1 |

Alle midlertidige kildeendringer ble gjenopprettet og MD5-verifisert. Dette viser at feilen er arvet fra det bestilte grunnlaget. Den presise avvisningsgrenen er ikke fastslått: brokoden bruker blant annet `capacity` for både stopped og full in-flight-vakt. Kvoter ble ikke økt. Samlet admin-regresjon kan derfor ikke erklæres grønn innen denne leveransen. Den siste avgrensede kontrollen erstatter ikke det feilende samlede fokusløpet.

## T1–T8 og praktiske grenser

| Ref | Evidens / grense |
|---|---|
| T1 | Funksjonelt rød på uendret konsument, grønn etter i ekte restartkjede med tre webfaser med entry/observer og egen browser-principal |
| T2 | Actual-source direkte adapterkall med full/manglende/feil home, annen nøkkel, decode/snapshot/lookup/ferskt token gir 0 ekstra nøkkelkall; legitim positiv kontroll gir 1 |
| T3 | CP captured-context parallelt engangsopptak og signeringsfeil/retry; actual-source åtte samtidige operasjonsforsøk gir ett opptak |
| T4 | CP eksakt token/data/endpoint/principal/transcript-binding, fire isolerte guard-mutanter røde; actual-source annen nøkkel og holder-substitusjon avvist |
| T5 | Actual-source cancel før opptak = 0, opptak før cancel = 1 med tilbakeholdt proof; Task-cancel og monotont utløp med bakoverhopp av wall-clock = 0. CP faktisk close/renew, fire interleavings, grønne |
| T6 | Legacy-default/existential og eksisterende CP Auth/regresjon grønne; CS origin-/transportkontroller grønne, men eksisterende feed-regresjon feiler også før h2. Hele CS paths/fullport er ikke vist |
| T7 | Actual-source strict home/nøkkel-avslag og bytehash-sammenligning av lagring; ingen context i Identity-encoding. Sluttkontroll brukte vaultens egen persistedVaultFileURL og kanoniske URL-er, bekreftet filtilhørighet og sammenlignet tre filers bytehash før/etter. Diagnostikk: tre filer, source/fixture-root matcher, faktisk vault-fil finnes. Tidlig årsaksgjetning om async-overstyring/tomt snapshot ble ikke bekreftet. |
| T8 | Normal-import ekstern CP-fixture, public snapshot/ferskt token avvist; init/decode compile-prober avvist. Actual adapter UUID-lookup gir ikke oppstartskapabilitet |

Lokale consumer-løp brukte koordinerte DiMy-kildearkiver på eksakte 2026.9.4-hoder, med testing-only Mint-manifestkobling til lokal Micropayments. CP-kilden var eksakt oppgitt hode; tredjeparts-pinnene viste ingen drift. Canonical lock ble gjenopprettet etter override-løpene. Remote/publisert consumer-resolusjon og consumer-CI er ikke kjørt. Den eksisterende release-policyen krever CP-utgivelsestag; den er ikke endret for å godta denne bestilte head-pinnen.

Ikke vist: full CS-port, grønn bolk32/full33 i #286-kopien, samlet grønn admin-regresjon, prod/staging eller installer. Kø-tråden trenger en separat avklaring/retting av den arvede feed-fixturen/transportfeilen før disse portene kan fullføres; h2 endrer ikke den grensen.

## Bevis og læringsfangst

Bevisprefiks: `HAVEN-Deploy/_handoff/HD-0196/h2/`. Se `cp-ci-final.json`, `cp-full-counts.json`, `green-final.log`, `experiment-*.log`, `scaffold-baseline-queue.md`, `scaffold-focused-counts.json`, `strict-admission-mutant-queue.md`, `feed-baseline-queue.md`, `feed-baseline97-queue.md` `strict-final-queue.md`, `strict-final-r2-queue.md` og `strict-final-r3-queue.md`. Grunnmurlogger: `HAVEN-Deploy/_handoff/GRUNNMUR/logg-503f6882db/`.

Tre læringer er fanget og anvendt i kanon: offentlige oppslag må ikke utstede holder-token, capacity alene identifiserer ikke avvisningsgrenen, og lagringssammenligning må verifisere den faktiske filen med kanoniske URL-er. Alle tre ZIP-er er bygget. Hjemmemappesync ble nektet av sandkassen; det er ikke markert synced. Koordineringsmilepæler er appendet med backup og MD5-kontroll. Diskvakten og cache-grensene ble ikke overstyrt; cap-advarsler ble vurdert, uten cache-sletting.
