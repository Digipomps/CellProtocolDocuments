# Testresultat — verifisert 2026-10-12

## Build og regresjon

Sprout-kandidat basert på origin/main 7aea5b0; lokal gren
codex/sprout-onboarding-http-20261012. Bevis i
`sprout/implementation/sprout-onboarding-repair-20261012/` fra HAVEN-roten.

- `build-macos.log`: Swift 6.4, 187 XCTest + 6 Swift Testing, null feil, exit 0.
- `build-linux.log`: Swift 6.2.4, samme 193 tester, null feil, exit 0; statisk
  x86_64-swift-linux-musl CLI bygget med 2 jobber, 4 GiB og ingen byggnettverk.
- `http-network-{macos,linux}.log`: fire ekte socket-tester i tre ferske
  prosesser per plattform. Sekvensielle/samtidige svar, ingen cookie-replay,
  redirect-mål aldri kontaktet, deklarert/chunked overflow avbryter faktisk
  nettverket, eksplisitt avbrytelse bevarer fungerende neste kall.
- `cli-runtime-{macos,linux}/results.json`: åtte prosessjekker per plattform,
  bestått. Linux bruker den faktiske statiske binæren.
- Server: CellScaffold PR289, head f47256c, CI 37897241866 successful; se
  `HAVEN-Deploy/_handoff/HD-0142/evidence/ci-dNmfGQEH/run.json` og conclusion.txt.
  Ingen ny CI-kjøring startet i dagens klientrunde.

## Trust

Historisk signering/publisering fra 29.09 er dokumentert i
`sprout/implementation/sprout-onboarding-repair-20260929/{signing-result,publication-result,live-after}.json`.
Dagens `live-public-state.json` viser ny HD0169-descriptor publisert 09.10,
SHA ab3546b9..., gyldig til 27.10 kl. 12 UTC. CLI godtar den eksisterende eierpinnen.
Ingen ny trustpublisering eller produksjonsendring i dagens runde.

## Entity og autorisasjon

Uavhengige wire-fixtures og negative klienttester er del av 193-testerssuiten.
Serverens kontrollerte unresolved er målt live; runtime App 9ff06f8, CP b4100f5.
Ingen ekte passkey ble brukt. Syntetisk fullføring er ikke personlig godkjenning.

## Terminal

`terminal-before-fix.txt`: faktisk _MultiHandle-abort, exit 134.
`terminal-fixed-20261012.txt`: faktisk invitasjonsprompt, /pause, exit 0.
`live-resume-result.json`: ny live-kjøring exit 0, awaitingApproval,
2 eksisterende seed-filer byteuendret, ingen ekstra seed og invitasjonsprompt nådd.
`test-installation.json`: egen testkommando installert; ordinær release beholdt.

## Avgrensning

Full menneskelig ticket/request/passkey/complete/resolution-kjede er ikke målt.
Egendefinert injisert URLSession med ekte Linux-sockets er ikke sertifisert;
Foundation kan buffre 3xx-kropp før delegat, utenfor innsamlerens størrelsesgrense.
Automatisk scaffold-installasjon ligger utenfor denne godkjente reparasjonsspecen.

## PDD-validator

Kjørt12.10: exit1 på fem eksisterende globale lesson-referanser til den manglende noden `purpose://candidate.testflyt-verktoycelle.haven-lenke-begge-veier`. Disse er ikke endret her. Validatoren er ikke grønn; se `sprout/implementation/sprout-onboarding-repair-20261012/pdd-validation.txt`.

## Ny klientkandidat 2026-10-13

Den eldre avgrensningen ovenfor er utvidet av brukerens nye uttrykkelige oppdrag. Sprout commit63b258506790f995c81c922e29cce28afee1779c, Linux-binær SHA256e422e93108eb6d410cfb2fcf13fc88e534e4722465cbe42776cd765626d7ee3d.

Per OS: 217 registrerte XCTest, 4 nettverkstilfeller hoppes over i ordinær kjøring, 213 består; ytterligere6 Swift Testing består. 219 ordinære tester + de4 faktiske HTTP-testene separat (tre prosesser per OS) =223 unike Swift-tester. 26 nye installer/Docker-tester inngår. 10 nye scaffold CLI-prosesskontroller og8 eksisterende runtimekontroller består per OS. Terminal- og release-guard-skript består.

Sluttlogger: `sprout/implementation/sprout-scaffold-install-20261013/sprout-scaffold-reviewed-{macos,linux,host}.log`. `final-source-provenance.json` knytter kildearkiv og binær til commit. Eldre final-logger er ikke sluttbevis.

Live13.10 kl10:48:53UTC: App9ff06f8/CPb4100f5; offentlig katalog404, trustbeskrivelse200 og gyldighet til27.10 kl12UTC. Ekte bildeinstallasjon i offline-modus/repeat/status består uten endring av kjørende containere. Fersk GHCR-pull avvist og kvittering bytebevart. Ingen tjenesteoppstart eller ekte passkey-fullføring målt. Serverkandidatens siste testbevis legges i dagens samlede rapport etter avsluttet kontroll.

Samlet serverkandidat 9b9fa48f57bf8bef899e246c3ed75afa59004b28:111/111 macOS-tester består, inkl14 første-eier og9 katalog. Final4-output og separat eksisterende CI-coverageavvik finnes i `sprout/implementation/sprout-scaffold-install-20261013/`. Samtidssnapshot av dependencies manglet; reflog rekonstruksjon viser b4100f5 gjennom testkjøringen og bytte til f5ce802 fire sekunder etter avslutning. Ingen Linux bootstrap/startupaksept eller ny image/release.

## Signert service-CLI 2026-10-13 kl.16:30 UTC

Endelig Sprout PR-CI38424101021 grønn på Linux/macOS. Perplattform:223 registrerte XCTest,4 opt-in sockettester kjørt separat i3 prosesser;6 Swift Testing,31 Python-koordinatorregresjoner. Totalt229 unike Swift-tester, ikke et gjentakelsessummert antall. Release38426015091 grønn, v0.3.0 på main35228b8299f3aada7bd48f8a9ae1b5224a49a995. Alle36 publiserte assets har kontrollert hash/størrelse. Begge plattformenes manifester er i tillegg Cosign-verifisert med eksakt workflow SHA/ref/event/repo, SCT og transparenslogg aktivert.

Hetzners isolerte v0.3.0-binær har SHA256dc71d09a18346c2cc46391b5640f66726e90cdaad644bb0d166c2c0b57ba6da4. doctor exit0: Linux,x86_64,musl,cryptography passed. Identitet ble ikke lest/opprettet av doctor. Privat release404 uten innlogging ble løst for denne interne testen ved SSH-overføring av allerede verifiserte bytes; ingen offentlig nedlasting bevist. Bevis: sprout/implementation/sprout-service-20261013/deployment-audit/{RELEASE_VERIFICATION.md,published-cli-install.json,release-download-access.json}.

Server PR319s første CI hadde2738 testutførelser,10 feil,15 skips; øvrige workflowporter grønne. Korrigert kandidat308222d har127/127 lokale tester med identiske før/etter-checkouts under samme cachelease. Ny CI38430298224 pågår. Publisert server/katalog/ny installasjonsreise er ennå ikke målt. Den tidligere generelle GHCR-tilgangsblokkeringen er avklart via eksisterende godkjente credentials og wrapper-check; faktisk ny digest-pull venter bildet.


## Server main og grønn kandidat-CI — 2026-10-13 17:35 UTC

CellScaffold PR319 er merget som `53012726f0780acd791fecc0a62ee950e402dd59`; treet `2711a9b988eb70b11ec730d8b3344d67ef24018f` er identisk med reviewet/lokalt testet head308222d4 og GitHubs testede PR-merge. CI38430298224 er grønn:34 Swift-bolker,2739 rapporterte testtilfeller inkludert15 skips,0 feil;10 ekstra bridge-testkjøringer i5 prosesser og119 Playwright-tilfeller. Første røde forsøk er bevart som separat evidens.

Den etablerte image-workflowen er dispatch-et én gang på eksakt mergeSHA: run38439420109, ref `codex/sprout-release-20261013-53012726`. Image, katalog og full Hetzner-installasjon er fortsatt pending. Installasjonsaksept skal holdes adskilt fra autorisert native bro-operasjon, full formålsoppfyllelse og personlig passkey/G3. En separat offentlig intent-probe er reviewet og staged, men ikke kjørt.

Bevis i HAVEN-rotrelative `sprout/implementation/sprout-service-20261013/server-release-evidence/`: `merge-verification.json`, `pr-ci-second-final.json`, `pr-ci-second-swift-summary.json`, `release-runs-initial.json`, `INSTALLATION_ACCEPTANCE_SCOPE_REVIEW.md`. HD0142 har aktuelle test-/pin-/lokalbyggebehov verifisert og post6 lukket; image-/vert-/sluttaksept er ikke merket ferdig.

### Sprout-release 13. oktober 2026, 18:28 UTC — ny målt CI-blokkering

CellScaffold main53012726 kompilerte og passerte suite-dekning i release38439420109, men Swift-porten feilet i IdeaTaskWorkspaceTests.testPromoteIdeaToTodoAddsLabelsAndMovesIdeaToProject: umiddelbar selectedIdea.stage var inbox, forventet project. Dette er forskjellig fra de tidligere metadata-/native-drain-feilene. PR-CI38430298224 er fortsatt et bevart grønt resultat; det erstatter ikke denne røde utgivelsesporten. Ingen OCI-publisering, katalogendring eller testinstans hevdes fullført. Rotårsak for mulig foreldet asynkron tilstand undersøkes; ingen testassertion er svekket og ingen ny CI er startet. HD-0142 post10 registrert; validate2419 records/0problemer.

Rapport: sprout/docs/Sprout_Scaffold_Installasjon_2026-10-13.md. Bevis: https://github.com/Digipomps/CellScaffold/actions/runs/38439420109 . G3/personlig passkey er fortsatt ikke gjennomført.


## Lokal årsaksbekreftelse og rettelse — 2026-10-13 19:26 UTC

Fire deterministiske regresjoner feiler mot uendret main53012726: eldre Vault-respons ruller tilbake trinn/versjon, eldre Todo-respons kan overskrive nyere fullinnlasting eller feedoppdatering, og versjonshull fra tom tilstand mister ett av to notater. Samme fire tester og hele IdeaTaskWorkspaceTests består etter den avgrensede rettelsen: 33/33, null feil. Kilde-/testhash 471e6224/07fbcc6b, toolchain, 55 rene dependency-checkouts og cachelease er identiske før/etter green. Uavhengig evidensreview har ingen åpne konkrete funn. Ingen public API/pin/identitetspolicy er endret.

PR/CI, ny main-merge og bildepublisering gjenstår. Første release38439420109 er fortsatt feilende og publiserte ikke bilde. Ingen katalogkonfigurasjon eller ny testinstans på verten er utført. Ingen vertsclaim er aktiv fra denne oppgaven. Personlig aksept/G3 er fortsatt ikke gjennomført.


## AI-rekkefølgefeil årsaksbekreftet og rettet lokalt — 2026-10-13 20:44 UTC

PR320 CI38454986305 avsluttet med2743 rapporterte Swift-testtilfeller,1 feil og15 skips; alle33 IdeaTaskWorkspace-tester og alle3 nettlesersteg bestod. Publisering ble hoppet over. Ny feil var AIInvokeCompleted observert før AIInvokeStarted.

En kontrollert pause i første feed-write-autorisasjon gjenskaper faktisk omvendt meldingsrekkefølge og for tidlig providerinvokasjon på gammel AI-kode. En egen decoded-direct-test gjenskaper manglende runtimebinding. Den avgrensede rettelsen avventer fortsatt autorisasjon for faktisk requester ved hver melding og sender deretter synkront gjennom en privat runtimebundet emitter. Sluttporten består97/97 uten skips (AI58,Idea33,konsumenter6); kilde,55 rene avhengigheter,pins,toolchain og lease er identiske før/etter.

Bredprøven var rød:4 feilende AIAssistantThread-tilfeller/12assertions og4 opt-in-skips. En separat gammel-kode-baseline gjenskaper de samme4 feilene/12stedene og HTTP-endpoint-policyavvisningen. Denne eksisterende gjelden holdes eksplisitt adskilt; policy og CI-unntak er uendret. Uavhengig sluttreview har ingen åpne konkrete funn.

Main har nå flyttet fra53012726 tilbb30e642 gjennom annet arbeid; sourceagent integrerer ferskmain og verifiserer kombinasjonen før én oppdatert PR-CI. Serverimage/katalog/ny testinstans er fortsatt ikke levert. Ingen aktiv vertsclaim fra denne oppgaven. Personlig passkey/G3 er ikke gjennomført. Bevis: sprout/implementation/sprout-service-20261013/server-release-evidence/ai-lifecycle-fix/.


## Servermain godkjent; ny bildeutgivelse startet — 2026-10-13 22:04 UTC

PR320 er normalmerget som308fbd071bb5cd89dd46f07647e8744d9bd7b056 kl22:02:08UTC (14.oktober norsk tid). Tree5a1c33b7d3e178eda06edecdf5766622c44d0b50 er eksakt lik reviewet bb519b70 og faktisk testet synthetic37bcd251. Ferskmainbb30e642 ble integrert før98/98 lokalport; separate Idea8f732a50 og AI82b32baf er bevart.

Endelig PR-CI38465708862 er grønn:2747 rapporterte Swift-testtilfeller/0feil/15skips og120 browserpass. AI58/58,Idea33/33,firstowner15/15,kataloginstallasjon10/10 består. Alle tidligere røde kjøringer er bevart. Én ny workflow_dispatch er startet på eksakt mergeSHA:38475106635, refcodex/sprout-server-release-20261014-308fbd071bb5. Verifisering av faktiske OCI-digests, katalogpublisering og Hetzner-installasjon gjenstår. Ingen vertsclaim eller vertsmutasjon er startet i denne fasen. G3/personlig passkey er fortsatt ikke gjennomført.

HD0142 sourcecommit er oppdatert og konkret serverregresjonsbehov oppfylt; image-/disk-/koordineringsporter gjenstår. Evidens: sprout/implementation/sprout-service-20261013/server-release-evidence/ai-lifecycle-fix/. Release: https://github.com/Digipomps/CellScaffold/actions/runs/38475106635 .


## Publisert katalog og første ekte vertsinstallasjon — 2026-10-14 01:18 UTC

Release38475106635 terminalSUCCESS med2747rapporterte Swift-tilfeller/0feil/15skips og120browserpass, og alle3OCI-bilder verifisert. Main308fbd071bb5cd89dd46f07647e8744d9bd7b056 ble satt i staging gjennom etablertwrapper: committed_verified01:11:33UTC, webdigestsha256:5532b39c5688ad016d276eade2dc361e040d5385e7753b79ab7b5d3f3f3b0e63. Signertkatalog tilbyr purpose://operate-local-haven-agent, version2026.10.14+308fbd071bb5. Faktisk publisertSproutv0.3.0 verifiserte katalog/plan, menyvalg+ja, og autentisertonlinepull.

Serviceaktivering stoppet unsafe_directory_mode før instance/eier/keys: delt /var/lib/haven er allerede root0700, installasjonskoordinatoren forventet0755. Den delte sikkerhetsgrensen er bevart. Alle21andre kjørende tjenester uendret, stagingnybuildready,51.57GiB Dockerfree. Rootclaim frigjort ev_9233556039ae9b32 mens sourceagent lager minimaldedicatedroot/preflightpatch og nyCLIrelease. HD0142 PREPARING, post13pending. Fullaksept/restart/publicintent ikke bestått; personligpasskey/G3 fortsattikkeutført. Bevis: sprout/implementation/sprout-service-20261013/deployment-audit/staging-deploy-receipt-20261014.json, hetzner-installation-journey-20261014.log, installation-directory-diagnosis-20261014.json. Tidligere rødtforsøk bevares.


## 2026-10-14 02:07 UTC — published client, actual enrolled owner, production dependency gap

Sprout PR6/main4e563bb0 and v0.3.1 are published and strict signature-verified. Exact published Linux bytes installed on Hetzner and passed doctor. The real CLI purpose/menu/signature/pull/first-owner path passed, then canonical provisioning failed with `ScaffoldKit.AdminControlPlaneConfigurationError.missingPublicOrigin`. This is a red installation result, not full service acceptance.

The existing generation and owner are preserved under the dedicated Sprout root. A private baseline of original state and all19 entry hashes/metadata was saved on the host before repair. Other running services are unchanged against the pre-test snapshot; staging308 remains ready. The host claim was released; HD-0142 is PREPARING, post14 tracks required production dependencies.

Required next implementation: signed explicit web/admin/node-agent stack profiles, strictly enrolled separate Admin owner with no legacy key healing, real fresh signed node telemetry, validated callback-origin, and narrowly bounded enrolled-state upgrade preserving web owner/build/request binding. These are under source work and independent review, not implemented or accepted yet. Full restart/public endpoint/negative probe acceptance remains outstanding.

Evidence relative to HAVEN root: sprout/implementation/sprout-service-20261013/deployment-audit/hetzner-v031-installation-journey.log, v031-canonical-failure-diagnosis.json, preserved-v031-generation.json; service-root-fix-20261014/RELEASE_HANDOFF.md.
