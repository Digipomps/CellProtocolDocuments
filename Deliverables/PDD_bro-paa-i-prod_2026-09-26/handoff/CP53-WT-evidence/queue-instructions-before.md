# Losen → Codex jobbkø

Én gangs oppsett. Etter dette kan Losen sette i gang Codex-jobber uten at
Kjetil er postbud, og uten å møte 60-sekunders-taket på broen.

## Installer (kjøres én gang)

    ln -sf ~/Build/Digipomps/HAVEN/_losen-queue/org.digipomps.losen-queue.plist \
           ~/Library/LaunchAgents/org.digipomps.losen-queue.plist
    launchctl load ~/Library/LaunchAgents/org.digipomps.losen-queue.plist

Avinstaller:

    launchctl unload ~/Library/LaunchAgents/org.digipomps.losen-queue.plist

## Hva den kan og ikke kan

Kan: kjøre `codex exec` med en promptfil, i en katalog under HAVEN, i
`read-only`, `workspace-write` eller `workspace-write-net`.

`workspace-write-net` er `workspace-write` pluss nett **for nøyaktig den ene
jobben**. Runneren legger til `-c sandbox_workspace_write.network_access=true` selv; global
`~/.codex/config.toml` røres ikke, så ingen annen Codex-økt får nett av dette.
Hver slik kjøring står med `NETT=JA` i `logs/runner.log`, så en nettjobb kan
aldri skje stille. Bruk den bare når jobben faktisk må ut: `git push`, `gh`,
`ssh` til verten, `curl` mot et domene. Kjetil valgte denne veien 17.9;
nøkkelen `sandbox_workspace_write.network_access` er bekreftet mot
codex-cli 0.154.0-alpha.6.2 sin egen dokumentasjon (se
`HAVEN-Deploy/_handoff/HD-0077/KANAL-20260917.md`). Merk at nett ikke gir
tilgang til Docker-socketen — den er fortsatt nektet i sandkassen.

`skript` er den tredje modusen, lagt til 17.9 da Codex-kvoten gikk tom midt i
en deploy og køen stod uten utfører. Den kjører **én navngitt fil**, ikke en fri
kommandostreng: linje 5 må være en sti under `HAVEN-Deploy/_handoff/` som slutter
på `.sh` og finnes; `..` avvises; linje 6 kan gi ett argument. Codex er ikke
involvert, så modusen virker uavhengig av kvote. Hver kjøring står med
`SKRIPT=<sti>` i `logs/runner.log`, og leveransestien (linje 3) er påkrevd —
skriptets utskrift går dit og kopieres til `done/<id>.svar.md`.
**Linje 3 skal aldri være samme fil som skriptet selv skriver.** 26.09 pekte
natt-inventar linje 3 på INVENTAR.md, som skriptet også skrev og til slutt `cat`-et;
cat leste sin egen utdata i løkke, fila ble 52 GB og Mac-disken full (køen stanset
stille). Siden 27.09 kjører skript-jobber med `ulimit -f 2097152` (2 GiB per fil).
Se `HAVEN-Deploy/lessons/L-2026-09-26-mac-disk-full-stanser-koeen-stille.json`.

Hvorfor dette er smalere enn `workspace-write-net`, ikke bredere: en nettjobb gir
en språkmodell frie hender med Kjetils nøkler; en `skript`-jobb kjører nøyaktig
de bytene som står i en fil under versjonskontroll, som kan leses og diffes før
den kjøres. Vil du fjerne modusen igjen, er det én `case`-linje i `runner.sh`;
sikkerhetskopier ligger som `runner.sh.bak-*`.

Kan ikke: kjøre en vilkårlig shell-kommando oppgitt i jobbfilen. Jobbfilen
inneholder ingen kommando — bare arbeidskatalog, modus, leveransesti, frist og
(for `skript`) stien til en fil i allowlisten. Alt annet er promptekst til Codex.
Kataloger utenfor HAVEN avvises.

**Vaktbikkje.** Linje 4 kan sette en vegg-klokke-grense i minutter (standard 90).
Brytes den, avsluttes jobben og køen går videre. Den finnes fordi `docker ps`
hang i 49 minutter 17.9: launchd starter ikke en ny runner mens den gamle lever,
så foreldet-lås-regelen biter ikke i det hele tatt når en jobb henger.

## Jobbformat

To filer i `inbox/`, med samme id:

    inbox/<id>.job          linje 1: katalog relativt til HAVEN (tom = HAVEN-rot)
                            linje 2: read-only | workspace-write | workspace-write-net | skript
                            linje 3: leveransesti relativt HAVEN-rot (VALGFRI, men
                                     PÅKREVD for skript)
                            linje 4: VALGFRI frist i minutter (standard 90)
                            linje 5: for skript: sti til .sh under HAVEN-Deploy/_handoff/
                            linje 6: for skript: VALGFRITT ett argument
    inbox/<id>.prompt.md    prompten til Codex

Runneren kjører hvert 60. sekund, tar én jobb om gangen, og legger resultatet i
`done/<id>.svar.md` med `done/<id>.done` som ferdigmarkør. Feil havner i
`logs/<id>.stderr.log`.

## Sjekkliste før du legger inn en jobb

Tre jobbspesifikasjonsfeil på to dager hadde alle samme form: **sandkassen ble
strammet uten at leveransen fikk plass i den.** Runneren håndhever nå de to
første punktene, men listen gjelder uansett.

1. **Skal jobben skrive noe? Da er `workspace-write` obligatorisk.**
   3. sept.: `losen-entitet-design` kjørte `read-only` og kunne ikke lagre
   rapporten. 16 minutter analyse gikk tapt.

2. **Ligger leveransen under arbeidskatalogen?** Codex' skriverot er `cwd`.
   4. sept.: `losen-entitet-design-2` hadde cwd `CellProtocol`, men skulle
   skrive til `CellProtocolDocuments/Deliverables` — en søskenkatalog. Avvist
   som «writing outside of the project». **Sett cwd til HAVEN-rot med mindre
   du har en grunn til å snevre den inn.**

3. **Erklær leveransestien på linje 3.** Da avviser runneren jobben før den
   kjører hvis 1 eller 2 er brutt, og logger en advarsel etterpå hvis fila
   likevel ikke ble skrevet.

4. **Skriv jobben for macOS, ikke for Linux.** Losen redigerer fra en
   Linux-VM; runneren kjører på macOS. 3. sept. brukte runneren `flock`, som
   ikke finnes på macOS — den avsluttet stille hvert minutt i en halvtime.
   `bash -n` fanger syntaks, ikke manglende kommandoer.

5. **Én jobb, ett formål.** Blandede jobber gir svar der du ikke kan se hvilken
   del som feilet.

6. **Skriv promptfilen først og `.job` sist.** `.job` er signalet om at jobben er
   klar. 10. sept. ble `.job` skrevet 15 sekunder før promptfilen; runneren tok den
   i mellomrommet, avviste den («mangler promptfil»), og promptfilen ble liggende
   foreldreløs i `inbox/` — runneren ser bare `*.job`. Skriv `.job` som `mv` fra en
   tmp-fil i samme mappe. Lærdom: `lesson.queue-job-file-before-prompt`.

7. **Ber jobben om nett? Da er `workspace-write-net` obligatorisk.** 17. sept.
   målte pz5 at `ssh` og alle domener var stengt i `workspace-write`; det er
   sandkassens standard, ikke en feil. En jobb som skal pushe, snakke med gh
   eller ssh-e til verten må be om nett på linje 2 — ellers feiler den med
   `Operation not permitted` og ser ut som et tilgangsproblem.

9. **`skript`-jobber trenger OGSÅ promptfil.** Runneren sjekker promptfila for
   alle moduser før den ser på modusen (`runner.sh:77`). I skript-modus leses den
   ikke av noen, men mangler den, avvises jobben som «mangler promptfil». 19. sept.
   la Losen inn en skript-jobb uten, i den tro at den ikke trengtes; den ble fanget
   bare fordi en annen jobb holdt runneren opptatt. Skriv en kort promptfil som
   forklarer hva skriptet gjør — den blir liggende i `done/` som dokumentasjon.

11. **Bygger eller tester jobben Swift? Da må den heve filtaket selv.** Runneren setter
   `ulimit -f 2097152` rundt skript-jobber (lagt inn 26.09 etter en 52 GB loggfil). Et Swift-bygg
   treffer taket og drepes med SIGXFSZ — exit 153, «Filesize limit exceeded» — uten at SwiftPM får
   skrevet en feilmelding; loggen stopper på «[Starting]». Skriv derfor
   `ulimit -f unlimited 2>/dev/null || ulimit -f 20971520 2>/dev/null || true` før bygget, skriv
   `ulimit -f` ut i beviset, send byggloggen til fil og vis den med `tail`. Les alltid exitkoden og
   sjekk at produktet finnes før du sier at bygget gikk. Lærdom:
   `HAVEN-Deploy/lessons/L-2026-09-28-ko-ulimit-f-dreper-swift-bygg.json`.

10. **Nettlesertester går i `skript`-modus, ikke i Codex.** Codex sin macOS-sandkasse
   stopper Chromium ved oppstart (`MachPortRendezvousServer: Permission denied (1100)`),
   så Playwright kan ikke kjøre der — 19. sept. stoppet alle 10 testene i WP-R2b før
   testinnholdet. Samme kommando fra et skript under `HAVEN-Deploy/_handoff/` i
   `skript`-modus kjørte grønt (`10 passed`, 7 sek), fordi runneren kjører som
   Kjetils bruker utenfor Codex-sandkassen. Mønster:
   `HAVEN-Deploy/_handoff/WP-R/kjor-t-f3-web.sh`. La Codex skrive testene, og la en
   skript-jobb kjøre dem.

8. **Ingen bash-arrays i runneren.** macOS' `/bin/bash` er 3.2, og `"${arr[@]}"`
   på en TOM array med `set -u` er en fatal feil der. 17. sept. la Losen inn en
   slik ekspansjon; den virket for nettjobber (array med ett element) og drepte
   runneren for alle andre — Kjetils `verk-render` ble aldri kjørt, og feilen
   sto bare i `logs/launchd.err`. Testet nå med seks jobbtyper mot en kopi av
   runneren før den ble tatt i bruk.

11. **Ingen `case` inne i `$( )` i skript runneren kjører.** macOS' bash 3.2 leser
   `)` i et case-mønster som slutten på kommandosubstitusjonen og gir
   `syntax error near unexpected token`. 19. sept. stoppet `wp-b1b.sh` slik etter
   at testene hadde kjørt grønt — en linje som skulle skille kjente fra nye
   testfeil. `bash -n` i Claudes Linux-VM bruker nyere bash og fanger det ikke.
   Filtrer med `grep -v -x -F -e …` i stedet.

12. **Kontroller fila på Macen etter hver skriving fra skyen.** 19. sept. meldte
    skrivingen av `wp-b4.sh` «written», men runneren kjørte den gamle utgaven to minutter
    senere. Sjekk md5 (eller et kjent ord i fila) på Macen før `.job` legges i koeen.
    Årsak funnet samme dag: når samme fil i skyens outputs-mappe skrives til Macen på nytt,
    kan den forrige opplastede utgaven bli skrevet (mtime endres, innholdet ikke). Bruk et
    nytt filnavn i outputs for hver ny utgave (f.eks. `wp-b4-v3.sh`) og skriv det til den
    faste stien på Macen; kontroller md5 etterpå.

11. **Kjedede jobber: rent arbeidstre betyr «ingen sporede endringer og ingen fremmede filer», ikke «ingen
   usporede filer i det hele tatt».** 28. sept. stoppet Sindre-F1 (a2b) fordi forrige jobb (F2) hadde latt
   testrester ligge i `.hvelv-test-root/`; prompten sa bare «stopp hvis treet ikke er rent». Skriv i stedet:
   «Usporede testrester fra egne tidligere testkjøringer er ikke stoppgrunn: flytt dem til
   `_to_delete/<jobb-id>/` under HAVEN-roten og nevn det i rapporten. Stopp bare ved sporede endringer eller
   fremmede usporede filer.» Be også implementøren om at testene rydder etter seg. Lærdom:
   `L-2026-09-28-ko-prompter-som-krever-rent-arbeidstre-ma-unnta`.

## Baner (parallelle jobber), fra 28.09

Kjetil 28.09: «Kan du kjøre noe av utviklingsjobbene i køen paralellt?» Runneren kjører nå én **bane** per
innboksmappe: `inbox/` er bane `a` (standard, alle tråder), og hver `inbox-<navn>/` (bare a–z og 0–9) er en egen
bane. Banene kjører samtidig i samme runner-prosess; innen én bane går én jobb om gangen, alfabetisk, og mappen
leses på nytt før hver jobb. START-linjen i `logs/runner.log` har `bane=<navn>`.

- **To baner skal aldri jobbe i samme arbeidstre eller gren.** En kjede av jobber på samme PR hører i én bane.
  Første bruk: `inbox-b/` = bro-rekken for CellProtocol PR #53; `inbox/` = alt annet (bl.a. Sindre/CellScaffold #270).
- To Swift-bygg kan nå gå samtidig. Byggevakten sjekker diskplass før hvert bygg; blokkerer den, er svaret å rydde
  (`HAVEN-Deploy/_handoff/RYDD/`), ikke å omgå vakten.
- En ny bane tas med neste gang runneren starter (launchd, hvert 60. sekund når ingen runner lever).
- Testet før bruk på en kopi i Linux-VM-en med falsk codex: parallell start, skript med argument, fire
  avvisningstyper, lås mot ny runner, sen jobb i tom bane mens en annen bane er opptatt. `bash -n` ok.
  Ikke testet med macOS `/bin/bash` 3.2 (ingen arrays eller 4.x-konstruksjoner er brukt). Forrige versjon:
  `runner.sh.bak-20260928-baner`.
