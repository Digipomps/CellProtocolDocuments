# Bolk 3 og 5 — k9: main-pinne og CI grønn; signert universal2, Apple-avtale blokkerer notarisering

STATUS: BOLK 3 LEVERT. BOLK 5 IKKE FERDIG: Apple avviser notarisering med HTTP 403. Pakken er Developer ID-signert, men IKKE notarisert eller staplet.

## Kilde, pinne og PR

- K8-rapport er bevart byte-identisk som `handoff/BOLK-3-RAPPORT-k8.md`. SHA-256: `d1ce1c099d987c6ef3e7551c3f3f1d0c48695c24da1c373bffa6878cad80ac48`.
- Klientgren `codex/korr-klient-20261007`, endelig hode `d91408bcdb4329b03bbee78fb5ec65180564ad56`.
- CellProtocol `97b348483448fb29dfe089bd96ab4d4adb384a76` i manifest, lockfil og faktisk checkout; Sprout `7aea5b0f814e345021c14d2a5389c9880cb988e9`.
- Bestilt co-author er med i alle fire k9-commits. PR https://github.com/Digipomps/HavenAgentD/pull/32 er fortsatt kladd; beskrivelsen er oppdatert.
- Ingen klientendring for etikettrettingen var nødvendig: medlemsdescriptors bruker UUID og offentlige nøkkelmaterialer; menneskelige etiketter inngår ikke i dem.
- K6-diagnostikk er bevart utenfor commit og ren eksport.

## Tester og CI

Fjerde lokal fullport exit 0: 361 fullport-tester i 68 suiter, 8 Python-helpertester, 100/100 autentiserte Vapor-brotilfeller, daemon smoke og ressursstaging-fixture. Adapteren kjører i tillegg 14 fokuserte tester som allerede inngår i fullporten. Tidligere tallet 375 var utførelser, ikke 375 unike tester. K8-backupen er ikke omskrevet.

CI på eksakt endelig hode: https://github.com/Digipomps/HavenAgentD/actions/runs/37908650647 — SUCCESS. Xcode 26.3 kompilerte hele kandidaten; 361 tester i 68 suiter, 100/100 brotilfeller, smoke, runtime-staging og kildebevis bestod. Sammenligning av passerte suite- og testnavn viste ingen manglende lokal dekning i CI.

Tre smale kompatibilitetsrettelser var nødvendige etter første grønne lokale Xcode 27-port:

1. Eksplisitt weak capture i nested Flow-Task; CI avviste capture av ytre mutable weak self.
2. Tre muterende `group.next()`-awaits er skilt fra samme `#require`-assertions for eldre Swift Testing-makro. Timeout og kansellering beholdes.
3. CI-sample viste Foundation `waitUntilExit` etter avkortet CLI-utdata. Eksisterende smal ferdig-state-retting fra commit `784e93d` er brukt før lesing av terminationStatus. Opprinnelige feilkvitterings-, timeout- og kanselleringstester beholdes.

Ingen assertion er svekket eller fjernet; testdeadline er ikke hevet. De tre røde CI-forsøkene er bevart som årsaksbevis. Separat eksisterende manuell release-workflow feiler validering uten runner-jobb fordi `runner.temp` står i job-level env. Den er ikke dispatch-et eller endret; den grønne PR-testjobben er dokumentert separat.

## Pakken som faktisk finnes

`HavenAgentD/.build/korr-release-20261008/dist/HAVENAgentD-0.3.1-korr.20261009-universal2.pkg`

- Ren `git archive`-eksport av endelig klientcommit og eksakt pinnet Sprout; kildehash-manifest er bevart.
- Bundne release-bygg for arm64 og x86_64, deployment target macOS 13.0. Ingen Intel-kjøring eller kjøring på macOS 13 er hevdet.
- Fire binærer: haven-agentd, haven-agentd-mcp, haven-correspondence-mcp og sprout. Native adminvindu er ikke med.
- Begge arkitekturer kontrollert i hver binær før pakking og i utvidet sluttpayload; hver payload-SHA-256 samsvarer med signeringsmanifestet.
- Developer ID Application med hardened runtime og timestamp; alle fire signaturer verifisert. Installerpakke signert med Developer ID Installer og betrodd timestamp; pkgutil-signaturkontroll grønn.
- Relokert, signert daemon fra den utvidede pakkepayloaden bestod bounded smoke-test, exit 0. Production resources er med; testbundler er utelatt.
- SHA-256 for den SIGNERTE, IKKE STAPLEDE pakken: `bf3d4f05b5065e99a6c93eb7b6fcf7e451e2b73b3c0dbf5f2fcd8dc5edd7a7a3`.
- `SHA256SUMS`, payload-/ressurschecksums og `release-manifest.json` ligger ved pakken. Manifestet sier eksplisitt `notarized=false`, `stapled=false`, `nativeAdminIncluded=false`.

## Notariseringsstopp og videreføring

Apple notarytool returnerte HTTP 403 ved pre-submission: påkrevd avtale mangler eller er utløpt. Ingen Accepted-status eller staple er oppnådd. Teamets Account Holder må kontrollere/akseptere gjeldende avtale; Apples rollebeskrivelse krever Account Holder for oppdaterte avtaler: https://developer.apple.com/help/account/access/roles . Hvis kontoens avtaler allerede er gjeldende, må den vedvarende tjenesteavvisningen avklares med Apple; denne jobben har ikke inspisert kontosiden.

Ingen blind retry og ingen endring av signeringsidentiteter eller notary-profil. Etter bekreftet kontoretting kan samme uendrede pakke videreføres gjennom `HAVEN-Deploy/_handoff/KORR-UT/wp-k9-notarize-existing.sh`. Skriptet er skrevet og syntakskontrollert, men ikke kjørt: kontrollerer pakkehash/eksakt grønt PR-hode, notariserer, stapler, validerer staple/Gatekeeper og oppdaterer checksum/manifest. Ingen ombygging er nødvendig. SHA-256 må rapporteres på nytt etter staple; verdien over er ikke en ferdig notarisert leveranse.

## Native admin og øvrig manglende akseptanse

Native approval-signer og enhetstester er grønne. K3-native-adminutkast er utelatt fordi produkt-/GUI-akseptanse, ekte LAContext, innmelding og fornyelse etter utløp ikke er dokumentert grønt. Faktisk vert med tre separate vaults, Intel-kjøring og ren mottaker-Mac er fortsatt ikke verifisert. Pakken er ikke sendt eller installert hos mottakere.

## Disk, avgrensning og bevis

Uendret diskpolicy: minst 40 GiB OG 5 prosent etter 10 GiB reserve. Før fullport omkring 122 GiB ledig; etter pakkebygg 111,4 GiB og 101,4 GiB etter reserve, 10 prosent. Bounded-runner, delt cache-leie og to Swift-jobber beholdt. Ingen diskrydding var nødvendig. Første release-forsøk stoppet på køens soft file-size limit; andre brukte samme eksisterende byggdriverinnstilling som fullportjobbene. Ingen diskvaktendring.

Ingen CP-endring, merge, deploy, korrespondansesending eller manuell cache-/WIP-sletting. Egen midlertidig pakkemappe og oppgavens gh-loggcache er ryddet etter hash-verifisert bevaring. Kildeeksport, artefakt og råbevis beholdes.

Bevis relativt HAVEN-roten: `HAVEN-Deploy/_handoff/KORR-UT/bolk3/`, med `k9-verification-summary.json`, `k9-full-r4-private.log`, fire CI-logger, `k9-ci-r3-diagnostics.zip`, `k9-pr-ci-final.json`, `k9-package-private.log`, `k9-package-r2-private.log`, `k9-preserve-signed-private.log` og `k9-release-result.json`. Rålogger er privat lokal evidens og gjengis ikke her.

Læringsfangst: compilerforskjell, overlappende testtelling og Apples avtaleavslag er anvendt i `CellScaffold/.claude/skills/haven-git-workflow/SKILL.md`; oppdatert ZIP er bygget. Distribusjon til hjemmemappens skill-kopier ble nektet av filsystem-sandkassen og er fortsatt ufullført. Ingen falsk synced-status er satt.

Global læringskontroll `check --strict`: exit 1. Tre k9-læringer er applied men ikke synced på grunn av sandkassen; eldre åpne poster tilhører andre økter.
