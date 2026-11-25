# Formålsspesifikasjon — entitetsutvidelse som virker

Oppgavemappe: `PDD_entitetsutvidelse-som-virker_2026-11-25` · Opprettet 2026-11-25 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

Kjetil 2026-11-23 12:46Z:

> Analyser og dokumenter entitetsutvidelsen. Poenget er at det skal være en friksjonsfri brukeropplevelse samtidig som det skal være sikkert. En entitet skal bare ha tilgang til sine egne celler og de man har fått tilgang til.

Kjetil 2026-11-25 09:09Z (delen om kartet):

> For å holde oversikt over utstrekning av egen entitet må entitetsdataene inneholde et kart i form av en graf over utstrekning av entitieten og hvor det er mulig å spørre om hjelp til formåls oppnåelse i HAVEN scaffolds. Dette må være en distribuert database hvor entitetens tilstedeværelse er kartlagt i hver scaffold - privat selvfølgelig - men med nødvendig cachet eller indeksert data fra andre scaffolds entiteten er tilstede på slik at man kan vite hva man har hvor man er, vite hvor man skal lete for å finne mer og å avgjøre om tilganget til et scaffold av en eller annen grunn et umulig eller trenger workaround for å gjenopprette tilgangen. Dette bør kunne håndteres godt med formål.

Kjetil 2026-11-25 09:50Z: «Ja til alle de tre åpne spørsmålene.» Jeg leste det som ja til de tre spørsmålene i analysen: lenken signeres med fersk passkey, statuslisten er høyst ti minutter gammel, og denne oppgaven startes med kartet i. Lesingen er sagt til Kjetil og ikke rettet.

**Funn om koden, ikke premisser.** Hans ord er at en entitet har tilgang til sine egne celler og de den har fått tilgang til. I dag gjelder det bare for én nøkkel om gangen: en avtale følger nøkkelen som signerte den, og en lenke gjelder bare på verten der den ble laget. Første alternativ i denne oppgaven er å endre koden slik at det hans ord sier, blir sant. Ingen gren bygger rundt begrensningen.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| En lenket nøkkel får eiermakt på verten der lenken er registrert | retrieved (Losen, lest 2026-11-25 på CellProtocol `origin/main` `12fa8bf`) | `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift` (`verifiedSameEntityLink`), `Sources/CellBase/Identity/IdentityLinkRegistry.swift` (`sameEntityLink`) |
| Lenkeregisteret er lokalt for hver vert og hver prosess | retrieved (samme lesing) | `IdentityLinkRegistry.swift` (`linksByOwner`, `restore`) |
| En avtale binder til nøyaktig den nøkkelen som signerte, så avtaler følger ikke med til en lenket enhet | retrieved 2026-11-23 på `b5f467a` (analysen, funn F1). Ikke lest på nytt på `12fa8bf` | Analysen https://claude.ai/artifact/MZbPNcKM387qAfQak9uhBS |
| Web-flyten `/link` godkjenner alltid hel lenke | retrieved (Losen, lest 2026-11-25 på CellScaffold `origin/main` `b049a6e1`) | `Sources/App/Controllers/VaporIdentityLink.swift` (`approvedScopes: [IdentityLinkScope.sameEntity]`) |
| Staging krever fersk passkey for lenker, og beviset bindes til forespørselens hash | retrieved (samme lesing) | `VaporIdentityLink.swift` (`verifyPasskeyAssertion`, `IdentityLinkRuntimePolicy.install`), `IdentityLinkCompletion.swift` (`validateApproval`) |
| Python og Go har ingen lenker i tilgangsavgjørelsen | retrieved 2026-11-23 (analysen, funn F5). Ikke lest på nytt | Analysen |
| Binding viser scopes CellBase ikke håndhever, og binder godkjenningen til feil hash | retrieved 2026-11-23 (analysen, funn F3 og F4). Binding er ikke lest på nytt. Rettes på greina `claude/extend-hash-v2` | Analysen, minnet om Safari-arbeidet |
| Entitetsdataene har en rot `scaffoldPresence` | retrieved (Losen, 2026-11-25, `12fa8bf`): roten står i `EntityTemplateRoots.anchorOwnedRoots`. Hva som skrives der i dag, er ikke lest | `Sources/CellBase/PersistingCells/EntityTemplateRoots.swift` |
| En tilbakekalling når andre verter | contradicted: `identityLinks.revoke` endrer bare registeret på verten der den kjøres | `EntityAnchorCell.swift` (`revokeIdentityLink`) |
| Staging oppfører seg som koden på `main` | unavailable: ingenting er målt på staging for denne oppgaven | — |

Ingen har lest: HavenAgentD sin innmelding, Binding etter 23.11, Go-koden utover eierløs celle.

## 1. Formålstre

Forkortelser: U = `purpose://candidate.entitetsutvidelse`, K = `purpose://candidate.entitetskart`.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.entitetsutvidelse.root | R Entiteten rekker det som er dens, fra alle sine nøkler | purpose://self-determination.data | En person som har lenket en ny enhet eller agent én gang, når fra den sine egne celler og de cellene entiteten har fått tilgang til, på alle verter der entiteten finnes. Ingen annen når dem. | test.utvidelse.e2e | candidate |
| purpose://candidate.entitetsutvidelse.agreements-follow-entity | A Avtaler følger entiteten | R | En avtale gitt til entiteten gjelder for alle entitetens hele nøkler, ikke bare den som signerte. | test.utvidelse.agreement-* | candidate |
| purpose://candidate.entitetsutvidelse.linked-key-under-agreement | A1 Lenket nøkkel bruker entitetens avtaler | A | En nøkkel med verifisert hel lenke får samme svar som nøkkelen som signerte avtalen, når den beviser sin egen nøkkel. Avgjørelsen sier hvilken lenke og hvilken avtale den bygget på. | test.utvidelse.agreement-linked | candidate |
| purpose://candidate.entitetsutvidelse.scoped-never-inherits | A2 Avgrenset lenke arver ingen avtaler | A | En avgrenset lenke får bare det lenken selv sier. Entitetens avtaler følger aldri med. | test.utvidelse.agreement-scoped-negative | candidate |
| purpose://candidate.entitetsutvidelse.portable-link | B Lenken følger med til neste vert | R | Lenken er et bevis nøkkelen bærer med seg. En vert som kjenner entiteten, godtar det uten ny seremoni. | test.utvidelse.portable-* | candidate |
| purpose://candidate.entitetsutvidelse.credential-admits | B1 Beviset slipper nøkkelen inn | B | En nøkkel viser `SameEntityIdentityLinkCredential` og beviser sin egen nøkkel. Verten godtar bare bevis utstedt av en nøkkel som allerede er entiteten der (eiernøkkel eller hel lenke i vertens anker). Alt annet avvises med kode. | test.utvidelse.portable-admit, test.utvidelse.portable-negative | candidate |
| purpose://candidate.entitetsutvidelse.issued-with-fresh-passkey | B2 Beviset utstedes bare med fersk passkey | B | Et bærbart bevis har passkey-bekreftelse over forespørselens hash. Verten setter selv forventet publikum og opphav, de leses aldri fra innsendt konvolutt. | test.utvidelse.fresh-passkey, test.utvidelse.host-sets-audience | candidate |
| purpose://candidate.entitetsutvidelse.status-list | B3 Tilbakekalling når alle verter på ti minutter | B | Entiteten fører en signert statusliste. En vert bruker en lenke bare når den har en statusliste som er høyst ti minutter gammel og ikke nevner lenken som trukket. Uten fersk liste: avvist, med kode som sier hvorfor. Verten der ankeret ligger, trenger ingen liste for sine egne lenker. | test.utvidelse.revoke-propagates, test.utvidelse.stale-status-denied | candidate |
| purpose://candidate.entitetsutvidelse.one-mechanism | C Én mekanisme, lik i Swift, Python og Go | R | Samme lenke gir samme svar i alle tre, og flatene viser bare det som håndheves. | test.utvidelse.parity-* | candidate |
| purpose://candidate.entitetsutvidelse.parity-fixtures | C1 Felles prøvesett | C | Ett sett signerte prøver (hel lenke, avgrenset lenke, trukket, utløpt, feil utsteder, kopiert post uten nøkkel) gir samme avgjørelse og samme kode i Swift, Python og Go. | test.utvidelse.parity-fixtures | candidate |
| purpose://candidate.entitetsutvidelse.one-vocabulary | C2 Ett ordforråd for hva en lenke gir | C | Det finnes én liste over scopes. Flaten for utvidelse i Binding og på web viser bare scopes CellBase håndhever, og ber aldri om andre. | test.utvidelse.vocabulary | candidate |
| purpose://candidate.entitetsutvidelse.frictionless | D Få håndgrep | R | Å lenke en enhet koster eieren ett sett håndgrep én gang. Neste vert koster ingen. | test.utvidelse.handgrips | candidate |
| purpose://candidate.entitetsutvidelse.handgrips-counted | D1 Håndgrep er talt for hver part | D | Tallet på håndgrep for eieren og for den nye enheten står i §3, talt fra bildene: første lenking, neste vert, fornyelse, tilbakekalling. Neste vert er null for begge. | test.utvidelse.handgrips | candidate |
| purpose://candidate.entitetsutvidelse.refusal-says-what-to-do | D2 En avvisning sier hva som skal til | D | Hver avvisningskode har en tekst i klart språk og ett neste steg, og flaten viser den. | test.utvidelse.refusal-texts, bilde (G1-GUI) | candidate |
| purpose://candidate.entitetskart.root | E Kart over entitetens utstrekning | R | Entiteten vet hva den har der den er, hvor den skal lete etter mer, og hva som er utilgjengelig. | test.entitetskart.* | candidate |
| purpose://candidate.entitetskart.signed-presence | E1 Hvert scaffold fører sin egen post | E | Hvert scaffold der entiteten finnes, skriver én signert post under `scaffoldPresence`: hvilke nøkler og lenker det kjenner, hvilke røtter og celler som finnes der, revisjon og tid. Scaffoldet er eneste forfatter av sin post. | test.entitetskart.presence | candidate |
| purpose://candidate.entitetskart.index-not-authority | E2 Indeks og kopi, aldri myndighet | E | Hvert scaffold har kopi av de andres poster med kilde, revisjon, hash og alder. Kartet svarer på «hvor», aldri på «får jeg lov». | test.entitetskart.cache-no-authority | candidate |
| purpose://candidate.entitetskart.help-for-purpose | E3 Hvor kan jeg be om hjelp | E | For et formål svarer kartet hvilke scaffolds som har celler eller tjenester som kan hjelpe, og hva som kreves for å bruke dem. | test.entitetskart.help-lookup | candidate |
| purpose://candidate.entitetskart.reachability | E4 Utilgjengelig sted og vei tilbake | E | Hvert sted har en tilstand: nåbart, ikke nåbart (med sist sett), lenke trukket, lenke utløpt, statusliste for gammel, nøkkel tapt. Hver tilstand har et gjenopprettingsformål med steg. | test.entitetskart.reachability | candidate |
| purpose://candidate.entitetskart.private | E5 Kartet er privat | E | Kartet leses bare med eierbevis eller hel lenke. En avgrenset lenke ser det aldri. Poster kopieres bare mellom entitetens egne scaffolds. | test.entitetskart.private | candidate |
| purpose://candidate.entitetskart.surface | E6 «Min entitet» viser kartet | E | En flate viser stedene, hva som ligger hvor, tilstanden for hvert sted og neste steg der noe er utilgjengelig. | bilde (G1-GUI), test.gui.parity | candidate |
| purpose://candidate.entitetsutvidelse.audit-leftovers | F Restene fra sikkerhetsrevisjonen er lukket | R | De tre restene fra revisjonen 2026-11-25 er borte. | test.utvidelse.leftover-* | candidate |
| purpose://candidate.entitetsutvidelse.proofs-not-in-template | F1 Malen til ankeret gir ikke `proofs` | F | Avtalemalen til EntityAnchor i CellVapor gir ikke `proofs`. Eksisterende kontrakter som bruker den, er talt og håndtert før endringen. | test.utvidelse.leftover-proofs | candidate |
| purpose://candidate.entitetsutvidelse.home-venue-passkey | F2 Hjemmescaffoldet lenkes med passkey | F | Eieren kan lenke hjemmescaffoldets identitet inn i ankeret fra en flate som henter passkey-bekreftelsen. | test.utvidelse.leftover-home-venue, bilde (G1-GUI) | candidate |
| purpose://candidate.entitetsutvidelse.anti.map-grants-nothing | Antiformål: kartet gir aldri tilgang | R | Ingen kodevei leser kartet for å avgjøre tilgang. | test.entitetskart.cache-no-authority | candidate |
| purpose://candidate.entitetsutvidelse.anti.no-wider-than-entity | Antiformål: utvidelsen når aldri mer enn entiteten | R | En lenket nøkkel når aldri en celle entiteten selv ikke når. | test.utvidelse.never-wider | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke formålsavgrensning og sikkerhetsnivå for egne agenter (F9 og F10). De står i `PDD_egen-agent-mcp_2026-11-20/FORMAALSSPEC-ITERASJON-2-UTKAST.md` og venter på sin egen G1.
- Ikke avgrenset lenke i seg selv. Den er bygget i CellProtocol #114. Her brukes den bare i negative tester og i prøvesettet.
- Ikke gjenoppretting av en tapt eiernøkkel. Kartet sier at nøkkelen er tapt og peker på gjenoppretting. Selve gjenopprettingen er en annen oppgave.
- Ikke organisasjoner og gruppeentiteter. De har egne oppgaver.
- Ikke utrulling. Staging går gjennom HAVEN-Deploy.

Kapabiliteter og avhengigheter oppgaven bygger på:

| Kapabilitet | Kilde | Avgrensning | Må virke før test? | Målt |
|---|---|---|---|---|
| Hel lenke gir tilgang på verten der den er registrert | CellProtocol `12fa8bf`, `EntityAnchorGenesisTests`, `EntityAnchorEnrollmentContractTests` | Bare samme vert og samme prosess | ja | Målt på Linux 2026-11-25 mot CellVapor-ankeret: 27 av 27 grønne (på greina til #117). macOS ikke kjørt |
| Lenker lages bare av den signerte seremonien, av entiteten selv | CellProtocol #117 (utkast), PyCellProtocol #5 (utkast), CellScaffold #514 (utkast) | Ikke flettet. B og F bygger på dem | ja | Linux grønt, macOS ikke kjørt |
| Avgrenset lenke | CellProtocol #114 (utkast) | Ikke flettet. Finnes ikke i Python og Go | ja, for A2 og C1 | Linux 12 av 12 grønne |
| Web-flyten `/link` med passkey på staging | CellScaffold `b049a6e1`, `VaporIdentityLink.swift` | Bare hel lenke | ja, for D og B2 | Ikke målt på staging i denne oppgaven. Sara-testen 2026-11-20 viste at invitasjon og innlogging virket; lenking av en ekstra enhet ble ikke prøvd der |
| Hva en lenket enhet får i dag på en annen vert | — | — | ja, det er utgangspunktet for B | Ikke målt. Lest i koden: ingenting, fordi registeret er lokalt |
| Hva en lenket enhet får i dag under en avtale gitt til eierens nøkkel | — | — | ja, det er utgangspunktet for A | Ikke målt. Lest i analysen: avvist |
| Rettelsen av hash og signatur i Binding | greina `claude/extend-hash-v2` | Eies av Safari-arbeidet | ja, for C2 i Binding | Ikke målt |
| Lenker i tilgangsavgjørelsen i Python og Go | finnes ikke | Må bygges her (C1) | — | — |

De to radene «ikke målt» for A og B måles før planen: én test i CellBase for hver, kjørt på `main`, som viser dagens svar.

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Måling av dagens svar for A og B | testutdata | `TESTRESULT.md#baseline` | — | nei |
| En lenket telefon leser et dokument entiteten har fått tilgang til gjennom en avtale | testutdata, så kjørende flate på staging | `TESTRESULT.md#agreement-linked` | — | nei |
| Samme telefon når entitetens celler på en annen vert uten ny lenking | testutdata | `TESTRESULT.md#portable-admit` | — | nei |
| En trukket lenke slutter å virke på den andre verten innen ti minutter | testutdata med tider | `TESTRESULT.md#revoke-propagates` | — | nei |
| Samme prøvesett, samme svar i Swift, Python og Go | testutdata, tre kjøringer | `TESTRESULT.md#parity-fixtures` | `contract/link-fixtures.v1.json` | nei |
| Håndgrep per part, talt fra bildene: eieren 3 trykk og 1 passkey én gang, den nye enheten 1 | tabell | `images/README.md` | bildene under | nei |
| Flaten «Koble til enhet» med avvisningstekster | bilde | `images/koble-enhet-*-v1.png` (10 bilder, ark `oversikt-koble-enhet-v1.png`) | `skeleton/koble-enhet.cellconfiguration.json` | nei |
| Flaten «Min entitet» med kartet: alt nåbart, ett sted utilgjengelig, én lenke trukket | bilde | `images/min-entitet-*-v1.png` (6 bilder, ark `oversikt-min-entitet-v1.png`) | `skeleton/min-entitet.cellconfiguration.json` | nei |
| Lenking av hjemmescaffoldet med passkey | bilde | `images/hjemmescaffold-*-v1.png` (3 bilder, ark `oversikt-hjemmescaffold-v1.png`) | `skeleton/hjemmescaffold.cellconfiguration.json` | nei |
| Kartet i entitetsdataene på to scaffolds, med kopi av hverandres post | testutdata | `TESTRESULT.md#entitetskart` | `contract/scaffold-presence.v1.json` | nei |

Håndgrep i dag, lest fra koden i `VaporIdentityLink.swift` og ikke talt på en skjerm: eieren lager en billett, den nye enheten sender forespørsel, eieren sammenligner ordene og godkjenner med passkey, den nye enheten fullfører. Det gjentas for hver vert. Talt fra bildene 2026-11-25 (`images/README.md`): eieren 3 trykk og 1 passkey, den nye enheten 1 håndgrep, én gang for alle steder.

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.

## Lærdommer du må lese før dekomponering
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.status-message-sent-before-the-documents-were-checked** (2026-10-06, minor): Dokumentene og meldingen til eieren 06.10 om kvelden skrev slutninger som målinger («haven-deploy ville blitt kjørt med umask 077», «skallet ventet fem sekunder: målt»), gjenga kontrollenes merknader som «en feil» og «alle rettet», utelot ett av fire svar der en vakt ble beskrevet, og ga et klokkeslett for når en kjøring ville være ferdig, uten grunnlag. Meldingen var sendt et kvarter før kontrollen av dokumentene.
    - forebygging: Dokumenter, LES-MEG ved siden av et skript og meldingen til eieren kontrolleres mot kildene av en som ikke har skrevet dem, før meldingen sendes. Ved hver påstand står det om den er målt, lest eller sluttet, og et tidsanslag gis som et spenn med grunnlaget. Test: kontrollrapporten er eldre enn meldingen, og rettelser gjort etter kontrollen er merket som ukontrollert.
- **lesson.commit-file-built-on-a-stale-copy-and-the-check-got-the-same-copy** (2026-10-06, major): README.md i commiten `c5058f49` fikk 172 endrede linjer (104 ut, 68 inn) der rundt 50 nye var ventet: tekst fra tre tidligere commiter falt ut.
    - forebygging: Hver fil i en commit-pakke bygges på git-objektet i foreldercommiten, og skriptet som committer, krever ventet antall linjer inn og ut per fil og stopper ellers. Kontrolltråden får commiten og finner grunnlaget selv. Test: skriptet stopper når forskjellen mot forelderen ikke er den ventede.
- **lesson.brake-file-written-after-the-chain-had-passed-the-brake** (2026-10-06, minor): Bremsefilen ble lagt 13 sekunder etter at kjedeskriptet hadde passert bremsesjekken foran pushen, så en commit med en kjent feil ble pushet.
    - forebygging: Et tall et menneske må lese før neste steg som ikke kan angres, deler kjeden i to jobber, eller skriptet krever tallet selv. Test: kjeden stopper foran pushen når commitens linjetall avviker fra det ventede.
- **lesson.check-ran-before-the-last-numbers-and-did-not-read-the-message** (2026-10-06, minor): Kontrollen av akseptdokumentet ble gjort før de 27 siste kallene var målt, og meldingen til eieren var ikke med. En ny kontroll rett før sending fant åtte ting, blant annet at meldingen la en svakhet til angrepet alene der råsvarene fra nett viste det samme.
    - forebygging: Den siste uavhengige kontrollen kommer etter at siste tall er ført inn, regner tallene på nytt fra råfilene og leser meldingen eieren får. Test: kontrollrapporten er yngre enn siste bevisfil og eldre enn meldingen.
- **lesson.early-return-rule-changed-what-happens-when-the-lookup-is-down** (2026-10-06, minor): Et spørsmål med et ord fra ordlisten får henvisningen (HTTP 200) også når oppslaget ikke kan nås, der andre spørsmål får 503 eller 403. Det sto verken i spesifikasjonen eller i en test.
    - forebygging: For hver regel som svarer før en avhengighet spørres, sier spesifikasjonen hva som skjer når avhengigheten er nede, og en test holder det fast. Test: en test der avhengigheten er tatt bort, med ventet svar for begge grener.
- **lesson.way-back-was-called-a-way-back-after-dry-runs-only** (2026-10-06, minor): Veien tilbake fra utsettingen er tørrkjørt to ganger, men selve byttet tilbake er aldri kjørt, der spesifikasjonen krever en vei som virker også når siden er nede.
    - forebygging: En vei tilbake er vist når byttet er kjørt, for eksempel mot en egen container med samme image. Ellers står den som «ikke vist» i planen eieren godkjenner. Test: bevis for et gjennomført bytte, eller linjen «ikke vist» i planen.
- **lesson.order-of-steps-changed-to-keep-a-promised-time** (2026-10-06, minor): Utgaven ble satt ut før rettelsen av README.md var committet, mot planen, fordi kontrollen av rettelsen tok 28 minutter der 15 var ventet.
    - forebygging: Planen sier hvilke steg som kan bytte plass når noe tar lengre tid, og kontroller får en hard tidsgrense. Test: hvert planbytte har en linje i STATUS.md med hva som tapes.
- **lesson.correction-to-a-list-removed-words-it-already-caught** (2026-10-06, minor): To rettelser i ordlisten ga nye hull: et unntak som ble sammenlignet etter at ø var brettet til o, tok bort «nøtte», og en innsnevring tok bort «tolererer».
    - forebygging: Hver utgave av en liste kjøres mot alle tidligere eksempler, både ord som skal treffe og ord som ikke skal, og eksemplene ligger som fikstur. Test: en fikstur med ett eksempelord per oppføring og en liste med ord som ikke skal treffe.
- **lesson.rewritten-draft-got-new-errors-where-it-was-rewritten** (2026-10-06, minor): Seks utkast til spesifikasjonen ble lest i fem kontrollrunder som fant 110 ting til sammen. Hver runde fant feil i det som var skrevet om etter den forrige.
    - forebygging: Etter en omskriving kontrolleres det omskrevne på nytt, og eieren får vite når siste utgave ikke er kontrollert. Tall fylles inn av kode. Test: dokumentet sier hvilken utgave kontrollen leste.
- **lesson.known-pitfall-repeated-in-a-small-follow-up-without-lookup** (2026-10-06, minor): Testen for avvik 4 sammenlignet to like svarkonvolutter med `XCTAssertEqual` og var rød mot riktig kode. Den grønne kjøringen fanget det før commit.
    - forebygging: `lookup` kjøres for hvert steg som skriver kode eller tester, også små oppfølginger, og oppgaven til kontrolltråden ber den holde testen mot lærdommene for taggene. Test: commit-trinnet stopper uten grønt bevis for nettopp filene som committes.
- **lesson.full-path-rule-passed-the-checker-in-descriptions-and-file-cards** (2026-10-06, minor): Meldingen som ba om G3, gikk gjennom kontrollskriptet for hele banen, men fem filer ble sendt som kort uten bane i sendingen, og dokumenter ble nevnt med en beskrivelse («akseptdokumentet») før banen sto.
    - forebygging: Hver fil som leveres i samtalen, står med hele banen i meldingen som følger med, og en beskrivelse av en fil får banen ved første nevning. Test: antall leverte filer er lik antall baner i meldingen.
- **lesson.status-did-not-say-status-or-what-to-do** (2026-10-06, major): Eieren 06.10 om statusen han fikk: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre.» Han skrev selv formålet og spurte hva som gjensto for å få prøvd med de to mottakerne.
    - forebygging: En statusmelding åpner med hvor formålet står for dem det gjelder, så det eieren skal gjøre i nummererte punkter, så leddene som gjenstår. Arbeid på et sidespor kalles et sidespor. Test: kontrolløren får eierens ord fra §0 og svarer på om første avsnitt sier hva mottakerne har fått.
- **lesson.few-steps-was-counted-for-the-recipient-and-not-for-the-owner** (2026-10-07, minor): Utkastet til G1 talte tre håndgrep for mottakeren og skrev «én gang per person» for eieren («ett trykk» i spesifikasjonen bak). Bildet viste to Touch ID per person og en kode å sammenligne, og rekkefølgen på eierens steg sto feil. Kontrollen før framlegget fant det.
    - forebygging: Der «få håndgrep» er et formål, telles håndgrepene for hver part, eieren først, per person og per runde, fra bildene og i rekkefølgen de skjer. Et steg som følger av et forslag, merkes som forslag. Test: et opptak på en ren maskin der håndgrepene er telt.
- **lesson.a-second-safeguard-hid-that-the-first-had-no-test** (2026-10-06, major): Én av 145 innsatte feil, kalt nr. 100 i filnavnene for omkjøringen («fila legges tilbake mens haven-deploy kanskje går»), ble ikke fanget, og alle 133 testene var grønne med den.
    - forebygging: To vern foran samme handling får hver sin test der det andre ikke kan svare. En innsatt feil som ingen test fanger, leses i utskriften før den regnes som ufarlig. Test: for hvert vern finnes et tilfelle der bare det vernet står mellom skriptet og handlingen.
- **lesson.deadline-request-left-out-what-follows-when-it-passes** (2026-10-06, minor): Utkastet til meldingen etter byttet ba eieren godkjenne to forespørsler innen 24 timer, uten å si at invitasjonen da er brukt opp og at en ny trengs (etter kontrollørens lesning: nytt bytte og ny omstart av staging), og uten steget etter: hans godkjenning av mottakernes egne forespørsler. Kontrollen før sending fant det.
    - forebygging: En forespørsel med frist sier hva som skjer når fristen går ut, og nevner hvert senere steg som er eierens. Test: kontrolløren spør for hver frist i meldingen «hva følger hvis den ikke holdes?» og «hva er hans neste steg etter dette?».
- **lesson.question-used-the-repos-words-and-came-back-as-a-question** (2026-10-07, minor): To av fem nummererte punkter til eieren kom tilbake som spørsmål: «Hva gjør assistentidentiteten?» og «Hva mener du med at vedlegg kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.»
    - forebygging: Et spørsmål til eieren bruker hans ord og sier hva en ting gjør før det spør om den. Test: kontrolløren leser hvert spørsmål, slik det blir sendt, som en som ikke kjenner repoet, og sier hvilke ord som må forklares.
- **lesson.shared-swiftpm-cache-lost-its-ownership-marker** (2026-10-08, minor): Første bygg i et nytt CellProtocol-arbeidstre stoppet etter 4 s: haven-swiftpm.sh exit 64, «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…».
    - forebygging: Byggeskript for en PDD setter HAVEN_SWIFTPM_CACHE_KEY=<pdd-slug> (egen cache) i stedet for å reparere den delte; koster ett kaldt bygg (6 min for CellProtocol). Test: skriptet skriver cache-key i rapporten.
- **lesson.xctest-stdout-export-interleaves-with-its-own-log** (2026-10-08, minor): En test printet 49 kB JSON til stdout mellom markører for at byggeskriptet skulle klippe den ut; fila ble ugyldig ved byte 49156 — XCTests egen «Test Case '…' passed»-linje lå midt inne i JSON-en.
    - forebygging: En test som skal levere data til et skript, skriver til en fil (NSTemporaryDirectory()) og printer bare stien; skriptet validerer JSON før det kopierer. Og: /usr/local/bin/python3 på Kjetils Mac er en x86-binær («Bad CPU type in executable») under launchd — bruk /usr/bin/python3 eller node i skript.
- **lesson.shared-cellresolver-fixture-unique-names** (2026-10-12, minor): Integrasjon kunne treffe en tidligere emitter selv om nytt registerkall ikke kastet.
    - forebygging: Bruk unike registreringsnavn i sharedInstance-fixtures, og mål actual loadCell/flow mot den nye cellen.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | `swift build` og `swift test` i CellProtocol og CellScaffold, `pytest` i PyCellProtocol, `go test ./...` i Go. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Hele eksisterende testmengde i berørte repo, antall før og etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff, kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.utvidelse.e2e | R | På staging og én vert til: lenk en telefon én gang, les en egen celle og en celle gitt ved avtale på begge verter. En fremmed nøkkel avvises begge steder. | TESTRESULT.md#e2e | venter |
| test.utvidelse.agreement-linked | A1 | CellBase-test med separate nøkkellagre: B gir entitet A en avtale signert av A sin eiernøkkel. A sin lenkede nøkkel leser. Avgjørelsen navngir lenke og avtale. | TESTRESULT.md#agreement-linked | venter |
| test.utvidelse.agreement-scoped-negative | A2 | Samme oppsett med avgrenset lenke: avvist. | TESTRESULT.md#agreement-scoped-negative | venter |
| test.utvidelse.portable-admit | B1 | To verter i samme test, hvert sitt register. Lenke laget på vert 1, bevis vist på vert 2, nøkkelen leser der. | TESTRESULT.md#portable-admit | venter |
| test.utvidelse.portable-negative | B1 | Bevis utstedt av fremmed nøkkel, bevis for en annen nøkkel, kopiert bevis uten privatnøkkel, utløpt bevis: alle avvist med hver sin kode. | TESTRESULT.md#portable-negative | venter |
| test.utvidelse.fresh-passkey | B2 | Bevis uten passkey-bekreftelse, og med bekreftelse over feil hash: avvist på en vert som krever den. | TESTRESULT.md#fresh-passkey | venter |
| test.utvidelse.host-sets-audience | B2 | Konvolutt med riktig signatur, men annet publikum eller opphav enn vertens: avvist. | TESTRESULT.md#host-sets-audience | venter |
| test.utvidelse.revoke-propagates | B3 | Trekk lenken på vert 1. Mål tiden til vert 2 avviser. Forventet under ti minutter. | TESTRESULT.md#revoke-propagates | venter |
| test.utvidelse.stale-status-denied | B3 | Vert 2 med statusliste eldre enn ti minutter: avvist med kode. Vert 1, der ankeret ligger: fortsatt tilgang. | TESTRESULT.md#stale-status-denied | venter |
| test.utvidelse.parity-fixtures | C1 | Kjør `contract/link-fixtures.v1.json` i Swift, Python og Go. Sammenlign avgjørelse og kode rad for rad. | TESTRESULT.md#parity-fixtures | venter |
| test.utvidelse.vocabulary | C2 | Skript som henter alle scopes flatene i Binding og web kan be om, og sammenligner med listen CellBase håndhever. Forventet: ingen utenfor. | TESTRESULT.md#vocabulary | venter |
| test.utvidelse.handgrips | D1 | Tell håndgrep fra bildene. Etter bygging: opptak på en ren maskin, talt på nytt. | images/README.md, TESTRESULT.md#handgrips | venter |
| test.utvidelse.refusal-texts | D2 | Hver avvisningskode i koden har en rad i teksttabellen. Skript sammenligner. | TESTRESULT.md#refusal-texts | venter |
| test.utvidelse.never-wider | antiformål | For hver celle i prøvesettet: en lenket nøkkel får aldri ja der eiernøkkelen får nei. | TESTRESULT.md#never-wider | venter |
| test.utvidelse.leftover-proofs | F1 | Malen har ikke `proofs`. Antall eksisterende kontrakter med `proofs` på staging er talt først. | TESTRESULT.md#leftover-proofs | venter |
| test.utvidelse.leftover-home-venue | F2 | På en vert med kravet om passkey: `link.anchor` med ekte bekreftelse lenker, uten gjør den ikke. | TESTRESULT.md#leftover-home-venue | venter |
| test.entitetskart.presence | E1 | To scaffolds skriver hver sin post. Signaturen verifiserer. En post signert av feil scaffold avvises. | TESTRESULT.md#entitetskart | venter |
| test.entitetskart.cache-no-authority | E2, antiformål | Legg en forfalsket post i kopien som sier at en nøkkel har tilgang. Tilgangsavgjørelsen er uendret. Søk i koden: ingen lesing av `scaffoldPresence` i tilgangsveien. | TESTRESULT.md#entitetskart | venter |
| test.entitetskart.help-lookup | E3 | Spør kartet om et formål som finnes på scaffold 2. Svaret navngir scaffold 2 og hva som kreves. | TESTRESULT.md#entitetskart | venter |
| test.entitetskart.reachability | E4 | Slå av scaffold 2, trekk en lenke, la en statusliste bli gammel. Kartet viser hver tilstand med neste steg. | TESTRESULT.md#entitetskart | venter |
| test.entitetskart.private | E5 | Avgrenset lenke og fremmed nøkkel leser `scaffoldPresence`: avvist. | TESTRESULT.md#entitetskart | venter |
| test.gui.parity | E6, D2, F2 | Bilde fra ekte tilstand mot godkjent bilde, samme størrelse. Knapper treffer ekte nøkkelstier. | ACCEPT.md#gui | venter |

## 6. Åpne spørsmål til Kjetil

1. **Gjelder A1 alle avtaler entiteten allerede har?** En avtale er i dag gitt til én nøkkel. Forslag: ja, alle avtaler gitt til en av entitetens hele nøkler gjelder for alle entitetens hele nøkler, også de som finnes fra før. Alternativet er at bare nye avtaler gjør det. Da må gamle avtaler signeres på nytt.
2. **Hvordan kommer kartpostene fra ett scaffold til et annet?** Forslag: entitetens egen lenkede klient bærer dem med seg når den besøker et scaffold. Da trenger ingen server å stole på en annen server. Alternativet er at scaffoldene snakker direkte sammen. Det er raskere, men krever tillit mellom servere.
3. **Hva skjer med en vert som ikke får hentet statuslisten?** Du har sagt høyst ti minutter. Forslag: da avviser verten lenkede nøkler til den får en fersk liste, og sier det i klart språk. Verten der ankeret ligger, er unntatt, fordi den selv vet hva som er trukket. Det betyr at en Mac uten nett fortsatt virker for sine egne lenker.
4. **Skal flaten «Min entitet» være med i første leveranse?** Forslag: ja, i enkel form, fordi kartet ellers ikke kan sees. Alternativet er data først og flate etterpå.

Sier du bare «G1 godkjent», gjelder de fire forslagene.

**Avgjort 2026-11-25:** Kjetil skrev «G1 godkjent». De fire forslagene gjelder: (1) alle avtaler, også de gamle, gjelder for alle entitetens hele nøkler; (2) entitetens egen lenkede klient bærer kartpostene mellom scaffolds; (3) en vert uten fersk statusliste avviser lenkede nøkler, unntatt verten der ankeret ligger; (4) «Min entitet» er med i første leveranse, i enkel form.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret |
|---|---|---|
| 1 | 2026-11-25 | Første tre. A og B fra analysens funn F1, C fra F3 til F7, E fra F11 i utkastet til iterasjon 2 for egne agenter, F fra restene i sikkerhetsrevisjonen. |
| 1 | 2026-11-25 | G1 godkjent av Kjetil. De fire forslagene i §6 er avgjort som foreslått. Treet er uendret. |
| 1 | 2026-11-25 | Bilder til G1-GUI: 19 bilder av tre flater, rendret med web-rendereren fra `skeleton/`. Håndgrep talt. To spørsmål i `images/README.md`. G1-GUI spurt. |
