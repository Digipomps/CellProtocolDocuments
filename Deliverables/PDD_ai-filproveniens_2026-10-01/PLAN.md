# Implementeringsplan — HD-0154

2026-10-02. G1 er godkjent. G1-GUI og G2 er godkjent av Kjetil 2026-10-02: «Jeg godkjenner G1-GUI/G2». Implementering startet. Formål og omfang følger FORMAALSSPEC.md.

## Rekkefølge og ansvar

| Pakke | purposeRef | Utfører | Endring og verifiserbar leveranse | Tester |
|---|---|---|---|---|
| P1 Metadata og tilgang | purpose://candidate.ai-filproveniens.privacy | Codex | Versjonert metadata-/hendelseskontrakt, eier/vert/volum/attempt-identitet, tillatte jobbområder, eksplisitt proveniens og dekningsgrad. Hver innsamler og hver grafoperasjon avviser feil eier/scope. | test.provenance.auth, test.cell.contract-fixtures |
| P2 Registrering fra faktiske jobber | purpose://candidate.ai-filproveniens.capture | Codex | Koble registrering før opprettelse og ved slutt/feil/avbrudd til AgentD, bounded bygg og vertens deploy-wrapper. Registrer opprettelsesbevis og før/etter-kontroll; mistede hendelser skal gi ufullstendig dekning. | test.provenance.capture, test.handoff.dry-run |
| P3 Eksisterende graf | purpose://candidate.ai-filproveniens.graph | Codex | Eierstyrt import fra lokal hendelseskø til GraphStore; rekkefølge/deduplisering, atomisk persistens og gjenoppbygging. Les tilbake antall/relasjoner og kontroller skippedCount. | test.provenance.replay, test.provenance.auth |
| P4 Bevaring og ryddekandidater | purpose://candidate.ai-filproveniens.retention | Codex | Klassifiser aktiv/beholdes/kan vurderes/ukjent/slettet med forklaring og fersk kontroll av lease, jobb, mount, prosess, Git/recovery/identitet og avhengigheter. Kobles til eksisterende ryddevakt. | test.provenance.retention |
| P5 Workbench og levering | purpose://candidate.ai-filproveniens.visibility | Codex; Losen koordinerer release | Flate med maskin/disk/prosjekt/jobb/status, opphav, måletid og dekning. Relasjonsliste må fungere selv når grafvisningen ikke gjør det. Eksakt kode-/test-/releasebevis følger eksisterende kø. | test.provenance.overview, test.gui.parity, build/regression/docs/status |

P1 går først. P2 kan produsere lokalt bevis før P3 er tilgjengelig. P4 trenger ferske opplysninger fra P2/P3; fravær er aldri bevis for at noe er ubrukt. P5 bruker kontrakten og de godkjente bildene.

## Konkrete integrasjonspunkter

- HavenAgentD/Sources/HavenAgentRuntime/JobCompletionService.swift: executeAgentJob før runner.run, normal completion, CancellationError og startup-recovery. Gjenbruk jobID, attempt, originator og workspace-policy. Registrer også daemonens egne rapport-/artefaktmapper.
- HavenAgentD/Sources/HavenAgentRuntime/AgentJobRegistrationStore.swift: behold validert arbeidsrot og symlink-kontroll. artifactPaths er forventede resultater, ikke sensorbevis.
- CellProtocol/Scripts/haven-swiftpm.sh: når cache opprettes, lease tas/frigis, barn avsluttes og cleanup_on_exit kjører. Delt cache får én artefaktidentitet og flere used_by-relasjoner. Eksisterende kapasitets- og slettevern beholdes.
- CellScaffold/scripts/run_swift_bounded.sh: formidle jobb- og prosjektidentitet til den delte løperen, uten å innføre en ny scratch-path eller et konkurrerende cache-system.
- CellScaffold/scripts/production/haven-deploy: registrer EVIDENCE-mappen og artefakter med deploy-transaksjonen som jobbidentitet, inkludert rollback/avbrudd. Metadata hentes fra tillatte felter; old-container.json, miljø og kommandolinjer skal ikke kopieres inn i grafen.
- CellScaffold/Sources/App/Cells/Graph/GraphStoreCell.swift: gjenbruk noder/kanter og graph.workbench.applyUpdates. Transaksjonsgrense og hendelsescheckpoint må dekke en komplett oppdatering; eksakt løsning velges mot integrasjonsbasen og testes med avbrudd.
- CellScaffold/Sources/App/Cells/WorkItems/DeveloperWorkbenchConfiguration.swift og tilhørende modell/Explore-kontrakt: bind ny oversikt til autoriserte projeksjoner. preview.*-handlingene i skissen er lokale fixtures og skal ikke lanseres som produktkontrakt.
- CellScaffold/Public/js/skeleton-runtime.js: rett avviket mellom SVG-linjers viewBox-skalering og HTML-noders prosentkoordinater i nettverksvisningen. Test brede, kvadratiske og smale visninger med avstand mellom kantendepunkt og nodesentrum. Ikke endre globale protokollregler for å rette GUI-geometri.

Kildebasis: lokal CellScaffold origin/main fdcfe7a566ae4e73febbba464edb190e9e9cea08; lokal HavenAgentD origin/main ea558ba1af63caa48cd76253ea1cb588f37aa084. Disse er kildeaudit, ikke garanti for dagens remote main. Oppdater Git-basis og samordne med PR273/HD-0155, PR25/HD-0156 og skills/HD-0157 før kodearbeid. Eget arbeidstre/gren med codex/-prefiks; ikke muter andre jobbers arbeidstrær.

## Registrering og datakvalitet

Innsamleren bygger på observerte opprettelser og registrerte skrivere. En forskjell mellom før- og etterinventar alene beviser ikke hvilken prosess som skrev filen, særlig ved samtidige jobber. Slike funn får observed_during og ukjent created_by. Egen arbeidsrot/lease gir en avgrenset attribusjonskontekst; opphav må fortsatt ha et konkret bevis.

Registrerte skrivere gir hendelser ved opprettelse, endring og flytting. Kontrollinventar av tillatte røtter oppdager hull; plattformobservasjon av filhendelser vurderes som støtte, ikke som bevis for fullstendig fangst av alle kortlevde filer. Droppede hendelser, avbrutt scan og endringer utenfor registrerte røtter vises som ufullstendig/utenfor dekning. Symlinks følges ikke ut av roten. Inode alene er ikke varig identitet; identiteten inkluderer vert, volum og opprettelsesgenerasjon. Flytting over filsystem krever ny artefakt med eksplisitt proveniens.

Append-only hendelser lagres lokalt med begrenset størrelse, tilgang og retensjon. En full eller utilgjengelig kø skal gi synlig degradert proveniens og hindre ryddeklassifisering, uten å gjøre en ellers vellykket produksjonsdeploy mislykket. Frakoblet graf hindrer ikke en registrert jobb. Grafen skal kunne bygges opp igjen fra beholdte hendelser/snapshot. Delvis import må ikke kvitteres som komplett.

## GUI som skal godkjennes

Se images/README.md og forhåndsvisningen i index.html. Filer og mapper, Relasjoner og Bevaring er rendret med eksisterende Porthole-renderer og eksisterende Workbench-tema. Lys/mørk, fylt/tom/forbindelsesfeil og mobil er bevart. Alle tall og filnavn i bildene er eksplisitte eksempeldata.

Relasjonslisten er godkjenningsgrunnlaget. Nåværende grafvisning har et målt geometriavvik; evidence/network-before.png viser feilen. Den grafiske varianten skal først erstatte eller supplere listen etter retting og separat visuell kontroll. Ingen ny stil- eller skjelettmotor er nødvendig for den viste listen. Native Binding-paritet er ikke målt.

## Verifikasjon før CI og deploy

1. Kontrakt-/redaksjonsfixtures lokalt: feil eier/rot, symlink-utgang, ukjent opphav, lang sti og metadata med potensielle hemmeligheter. Ingen kopiering av filinnhold, prompts, miljø eller argv.
2. Syntetisk jobb på Mac og Linux oppretter, endrer, flytter, gjenbruker sti og avslutter med suksess/feil/avbrudd. Sammenlign faktisk kontrollinventar og observerte hendelser. Korte transiente filer og samtidige skrivere må gi ærlig dekning.
3. Spool og graf: samme eventID med samme/ulikt innhold, duplikater, rekkefølgebytte, reconnect og feil midt i lagring. Checkpoint og graf må aldri hevde mer enn det som er varig lagret.
4. Retensjon: aktiv jobb/lease/mount/prosess/avhengighet og manglende metadata blokkerer kandidat; regenererbart, avsluttet og fullt kontrollert materiale kan bli forslag. TTL gir aldri slettekommando i denne funksjonen.
5. Faktisk GUI: korrekt eier, filter, detalj, relasjonsnavigasjon, antall/størrelser uten dobbelttelling, tom/frakoblet tilstand, restart og autorisasjonsavslag. Sammenlign mot godkjent bilde.
6. Kjør ci/check-value-literals.sh før push. Swift kun via kapasitets-/leasebeskyttet bounded runner med to jobber; ingen prøvebygg når marginen er for lav. Bevar eksakte testlogger og siste totalsammendrag. Shell/Python/JS-fixtures først; Linux-kompatibilitet lokalt før Actions.
7. PR per berørt repo, med eksakt testet head og ingen lokal-path-drift i Package.resolved. Losen koordinerer release og vertsclaim. Staging krever backup/rollback, immutable image og funksjons-/restartkvittering; prod krever eksisterende godkjennings- og releaseflyt. Ingen gitt release eller dato loves her.

## Avhengigheter og konkrete begrensninger

- 2026-10-02 svarer agent_workbench_targets igjen, men viser kun kjetil2-staging-work og kjetil2-staging-projects med state/query. remoteAccessVerified=false. Graf-target og tilhørende grant er ikke etablert eller verifisert.
- Kapasitet må måles på nytt før bygg/deploy. Tall fra 2026-10-01 er historikk, ikke en fersk gate.
- HD-0158: fem eksisterende ugyldige formålsreferanser gir rød global PDD-validering. Ikke endre kanon for å skjule dem.
- Køinventaret er gammelt. Ikke bruk det som kilde til dagens prodversjon; hent health/build eller receipt ved release.

## Tilbakerulling

Slå av innsamling/projeksjon via en avgrenset konfigurasjonsbryter uten å miste eksisterende jobb-/bygg-/deploysemantikk. Behold hendelsene for feilsøking; ingen automatisk rydding av spool før retention er godkjent. Gjenopprett graf fra verifisert snapshot ved migrering. GUI-fanen kan rulles tilbake uavhengig av jobbkjøringen. Ingen sletteoperasjon er del av denne leveransen.

## Verifisert læring for GUI-arbeidet

L-2026-10-02-graph-geometry-needs-visual-verification: Ikke godkjenn en nettverksgraf fordi antall noder stemmer eller SVG finnes. Sammenlign linjenes skjermkoordinater med nodesentrene i både bred og smal flate, og test etter zoom/pan. Den nåværende kildekoden bruker SVG viewBox uten eksplisitt preserveAspectRatio mens HTML-nodeposisjonene bruker prosent av hele flaten. Nettverksbildet fra denne økten viser avviket. En etterfølgende separat tallmåling stoppet ved oppstart av Chrome (SIGABRT/EPERM); ingen numerisk avstand er derfor hevdet. Den beståtte GUI-kontrollen gjelder relasjonslisten, ikke den feilende nettverksgeometrien.
