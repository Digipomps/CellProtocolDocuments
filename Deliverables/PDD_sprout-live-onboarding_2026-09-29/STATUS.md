# STATUS

- surfaces: codex, scaffold, terminal
- tags: identity, security, sprout
- G1: godkjent 2026-09-29 — brukerens «Reparer det som må repareres» gjelder de konkret beskrevne feilene og reparasjonene fra foregående svar.
- G1-GUI: ikke relevant
- G2: godkjent 2026-09-29 — samme uttrykkelige reparasjonsinstruks; ingen ny myndighet eller produksjonsendring.
- G3: venter

## Oppdatert 2026-10-12

Historisk trustmigrering ble faktisk publisert 29.09; descriptor fornyet av HD0169
09.10 og nå gyldig til 27.10. Serverreparasjonen er merget i PR289 og finnes i
kjørende staging App 9ff06f8/CP b4100f5. Gamle kapasitetsblokkeringer er ikke lenger
aktive observasjoner. Ingen cache er slettet av denne reparasjonsrunden.

Dagens ekte Hetzner-test avdekket HTTP-runtimekrasj. Dette er rettet innen
terminal-/robusthetsformålet med prosesslevende sesjoner og nye socket-tester.
193 ordinære tester per plattform, fire socket-tester × 3 prosesser per plattform
og åtte CLI-prosessjekker per plattform består. Faktisk live CLI når invitasjon;
gjenopptakelse beholder nøklene og awaitingApproval. TESTRESULT.md og ACCEPT.md
inneholder evidens. Klientkandidat er lokal og testinstallert, ikke i main.

G3 venter fortsatt; ekte personlig passkey/fullføring er ikke utført.

## Utvidet brukeroppdrag 2026-10-13

Brukeren: «Gjør det som gjenstår. Med automatisk scaffold installasjon. mener du da å hente og installere scaffolds som oppfyller brukerens (scaffoldadmin) formål. Det må på plass». Dette utvider september-reparasjonen til formålsstyrt scaffold-installasjon. Ny konkret plan ligger i Sprout-kandidaten `docs/implementation/scaffold-install-20261013/PLAN.md`. Instruksen autoriserer implementasjon og isolert vertstest; ingen personlig passkey eller G3 er utledet.

Sprout-kandidat 63b258506790f995c81c922e29cce28afee1779c er committet lokalt og testinstallert separat på Hetzner. Formålsvalg, signert OCI-katalog, avhengigheter, verifisering og atomiske bildekvitteringer er implementert. Ekte offline-installasjon/repeat/status består; fersk GHCR-pull avvises av tilgangskontrollen. Offentlig katalog gir fortsatt404. Automatisk tjenesteaktivering gjenstår uttrykkelig; status er installed-not-started. HD-0142 post3–5 holder resten synlig.

Dagens samlede rapport er `sprout/docs/Sprout_Scaffold_Installasjon_2026-10-13.md` fra HAVEN-roten. G3 venter fortsatt.

## 2026-10-13 — Utvidet gjennomføringsbestilling

Kjetil: «Gjør ferdig det som gjenstår. Få automatisk tjenesteoppstart på plass, endringene inn i main og katalogen publisert. Test deretter hele installasjonsreisen på Hetzner.» Dette autoriserer det konkrete gjenstående kilde-, main-, katalog- og testløpet. Mål: én signert formålsplan fører til digest-verifisert OCI-bilde, ny lokal scaffold-eier og fungerende vedvarende tjeneste; retry/restart bevarer identiteten. G3/personlig passkey-aksept er ikke utført eller fabrikkert. Pågående bevis i sprout/implementation/sprout-service-20261013.

## Verifisert fremdrift 2026-10-13 kl.16:30 UTC

Sprout PR5 er merget til main35228b8299f3aada7bd48f8a9ae1b5224a49a995 med samme tre som grønn PR-CI38424101021. Signert v0.3.0 er publisert av grønn release38426015091. Begge plattformers bundle/signaturer er kontrollert; eksakt Linux-release er installert isolert på Hetzner og doctor består. Repoet er privat, så testen brukte autentisert nedlasting, signaturverifikasjon, SSH-overføring og SHA256-kontroll på verten. Anonym release-URL gir404; offentlig kildekode eller ny distribusjonskanal er ikke etablert.

Automatisk Linux-aktivering er implementert med ny lokal owner, canonical provisioning, privat generasjon, loopback-service, restart og formålsdiscovery. Server PR319 head308222d441142365b277f50e6c7fb91a5f49c949 har127 lokale regresjoner bestått med samtidige dependency-snapshots; korrigert Linux-CI38430298224 kjører. Første Linuxrunde var rød på9 metadatafixturefeil og1 asynkron cleanup-assert. Ingen produksjonskontroll er svekket. Main/image/katalog og faktisk ny serviceaksept gjenstår.

Eksisterende wildcard dekker sprout-test.digipomps.org. Egen443-proxy og gyldig sertifikat er målt eksternt; backend er foreløpig502. DNS-/brannmur-/registrarflytting trengs ikke for testen. G3/personlig passkey venter fortsatt som separat menneskelig flyt. Aktuell rapport: sprout/docs/Sprout_Scaffold_Installasjon_2026-10-13.md.


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
