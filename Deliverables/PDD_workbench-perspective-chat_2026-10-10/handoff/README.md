# Handoff til køeier og utfører — ikke innsendt

2026-10-11 · Status: G2-forslag, ingen køclaim, jobb-ID eller mottakskvittering.

## Omfang

De sju arbeidspakkene i PLAN.md tilhører samme leveranse. Codex eier kildearbeidet; Losen koordinerer eksisterende build-/merge-/deploykø. Den autoriserte Mac-/miljøutføreren kjører effekten. Ingen eier eller lane antas ledig fra eldre notater. Agreement #314 og Perspective/Flow har egne eiere og er ikke overtatt her.

## Før første jobb lages

1. Les STATUS.md og krev registrert G2. Kontroller at kilderevisjoner, Workbench-eier og miljø fortsatt stemmer.
2. Hent fersk køstatus og avklar lane/claim, berørte filer og avhengigheter med køeier. Bare claim-eier frigjør. En hvilken som helst hostclaim stopper deploy.
3. Opprett eller gjenbruk egnet rent managed worktree fra verifisert main; bevar eksisterende checkout-/arbeidstreinnhold. Bruk kodet filliste og forventet diffgrense.
4. Bind arbeidsordren til faktisk workItem, purposeRef, godkjent oppdrag, repository, baseSHA, executor, tillatte paths/handlinger, miljø, budsjett, outputplassering og commandID. Sensitive exports/credentials skal ikke legges i jobbtekst eller Git.
5. Bruk eksisterende autoriserte AgentD-jobbgrensesnitt. Nåværende Workbench-target har bare state/query; ingen write/submit-rett utledes fra targetlisten. Verifiser utførerens capabilities før en køknapp aktiveres.

## Krav til senere kjørbart skript

Ingen deploy-/byggskript eller submit er opprettet i denne P2-pakken. Ved implementering lages ett avgrenset, idempotent skript per faktisk jobb, med dry-run som standard og uttrykkelig execute-modus, synlig SHA/filliste/kapasitet/miljø og stoppbremser før mutasjon. Ingen kommentar etter en kommando og ingen Git-operasjoner gjennom Cowork-mount. Bruk repoets bounded Swift-/Xcode-wrappere; ingen ad hoc scratch-path. Jobben må kunne leses før den sendes.

Commit og push skilles i to køjobber når en diff-/tallbremse krever menneskelig vurdering. Etter rød kontroll, også kode 000, stoppes kjeden; ingen automatisk ny kjøring. En endring i committet test trenger avklaring før endring. Kun claimeier frigjør sin claim.

## Kvittering og gjenopptak

Registration er ikke submit. Workbench viser køet først med faktisk jobbreferanse fra utføreren. Persist attemptID før dispatch, og hent samme ID etter ukjent svar. Vis pending/unknown/denied korrekt. Oppfølging med ny attempt skjer først etter at forrige utfall er avklart eller en autorisert avklaring er registrert. Modellgenerert «done» er aldri kildebevis.

Køeiers mottak må navngi jobb, lane/claim-eier, avhengigheter og resultatdestinasjon. Byggkvitteringen inneholder sourceSHA, dependency pin, kommandoer, testantall/status og kapasitet; releasekvitteringen inkluderer PR/mergeSHA, immutable digest, miljø, deploy-/funksjonsprøve og rollbackbevis. Persondata og nøkler utelates fra delt kvittering.

## Ferdigmelding

Oppdater TESTRESULT.md og ACCEPT.md med faktisk evidens, ikke planpunktene fra dette dokumentet. Knytt PR-er, release og receipts til WorkItem og session; lagre minimal prosjektprojeksjon bare innenfor eksplisitt publikum. Root-testen og G3 er utestående inntil hele kjeden er demonstrert i prod.
