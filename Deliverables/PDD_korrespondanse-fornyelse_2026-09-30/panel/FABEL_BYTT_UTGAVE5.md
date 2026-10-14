# Uavhengig kontroll av `bytt-invitasjoner.sh`, utgave 5 (06.10.2026, kontrollør: Fabel)

## Dom

`les-<stempel>` kan kjøres mot verten nå: bare ops, bare lesing; det eneste sporet den setter, er en linje i vertens auth-logg fra `sudo -n -l` og selve ssh-innloggingene.
`toerr-<stempel>` kan kjøres når eieren har sagt ja til root: de to root-blokkene er utgave 4 sine, bare pakket i en funksjon, med to nye leselinjer (`grep -n`, `ls`).
`utfoer-<stempel>` kan kjøres etter en `toerr` uten HINDER, med forbeholdene i E. Jeg fant ingen feil av samme klasse som funn 1 i utgave 4; ti merknader står under, og den første bør rettes før kjøring fordi den tar bort nettopp vakten funn 9 ba om.

## Funn, viktigst først (ingen blokkerer)

1. Merknad, linje 303: en liste `base64 -d` avviser helt, leses som «0 invitasjoner». `jq` får tom inndata, gir kode 0 og ingen linjer; `||`-grenen ser bare jq sin kode, så svaret blir `status=lest` uten linjer, og python-delen (310–343) regner 0 utløpte, 0 gyldige, ingen borte. Kjørt (arbeid/forsoek.py, forsøk A og A2, verdien «!!!!» og base64 av blanke tegn): `les` skrev «har 0 invitasjoner … 0 gjelder fortsatt», ingen HINDER, og `utfoer` gikk til `<!-- BYTTE FERDIG -->`. Utløses også om `tr '_-' '/+'` eller paddingen (302) skulle gi noe base64 ikke tar. Kostnad: vakten mot bortfall er borte i det tilfellet, og utskriften sier «0 invitasjoner» om en variabel som er 4115 tegn (maal/HAVEN-DEPLOY-PAA-VERTEN linje 22) uten ordet «kunne-ikke-pakkes-ut». Jeg slutter at ingen gyldig invitasjon går tapt av det: tjeneren gir også tom liste når dekodingen feiler (AssistantCorrespondenceCell.swift 1763–1772). Retting: `set -o pipefail` i `hoved()` eller dekod til en variabel og test koden før `jq`.
2. Merknad, linje 277–290: et ssh-kall som feiler akkurat på logind-spørsmålet, leses som «logind svarte ikke, og logind.conf har ingen linje», altså fri bane. Punktumet som skrives til slutt (`echo .`) kontrolleres ikke, i motsetning til verktøyspørsmålet (269–273), som gir HINDER når svaret mangler. Kjørt (forsøk D og D2): logind-feil gav ingen HINDER, verktøyfeil gav HINDER og `utfoer` stoppet med kode 5. Kostnad: lav, standard på Ubuntu er av. Retting: krev punktumet, som for verktøyene.
3. Merknad, linje 578–596: `ROT_TILBAKE` legger hele kopien tilbake, ikke linja. Endrer noen en annen variabel i fila mellom skrivingen og tilbakeleggingen (inntil 25 minutter), viskes den endringen ut stille. Kjørt (forsøk H: etterligningen av haven-deploy byttet `MVP_ADMIN_OPERATOR_USER_IDS` før STOPPED og rullet så tilbake): skriptet skrev «lagt tilbake» og «står som før», og linja hadde den gamle verdien. Kostnad: lav i dag, `haven-deploy-secret` er ikke installert (maal/HAVEN-VERKTOY linje 15) og claimen skal holde andre unna. Retting: bytt bare linja, med samme awk som i 565, eller stopp hvis de andre linjene i fila nå ikke er lik kopiens.
4. Merknad, linje 325 og 328: regexen for principal tar ikke «@» eller bokstaver utenfor ASCII, som tjeneren godtar (Cell.swift 2092–2098), og `fromisoformat` i Python 3.9 avviser brøkdeler av sekund med 1, 2, 4 eller 5 sifre. Begge gir «kan-ikke-leses» og HINDER, så `utfoer` stopper på en vert som er i orden, men taper ingenting. Kjørt (forsøk B: en principal med «@» gav HINDER). Dagens data treffes ikke: tjeneren og generatoren skriver tre sifre (Contracts.swift 287–291, maal/PROEVE-4-TOERR-2 linje 3–6). Se også C om Python-utgaven.
5. Merknad, linje 673 og 754–772: sluttmerket skrives når `sudo` returnerer. Dør `sudo` av SIGKILL mens haven-deploy lever videre som foreldreløs, står `HAVEN_DEPLOY_SLUTT=137` i loggen mens haven-deploy går, og fila legges tilbake (771). Jeg fant ingen vei dit i kildene (KillUserProcesses dreper hele sesjonen og kontrolleres; OOM-dreperen ville tatt noe større enn sudo), så dette er en restrisiko, ikke et forløp.
6. Merknad, linje 608–611: feiler lesingen av lista i `tilbake_til_foer`, sier meldingen «lista i containeren er ikke den som sto der før», ikke at den ikke kunne leses. Utfallet er riktig (fila røres ikke, claimen står), ordlyden peker feil.
7. Merknad, linje 566–567 og 589–590: fila får rettighet 600 etter skriving og tilbakelegging også når den hadde 640, 644 eller 400 (kjørt, arbeid/tmp/skriv2); kopien beholder opprinnelig modus (`cp -p`). Avbrytes `ROT_SKRIV` mellom `cp` (572) og `mv` (573), blir en `mktemp`-fil med alle variablene liggende under /etc/haven, og `kopier=` (406) teller den ikke.
8. Merknad, linje 479–483: `toerr` med lista alt i kraft viser ikke HINDER-listen (forsøk K). Ufarlig, siden `utfoer` da ikke gjør noe.
9. Merknad, linje 665–705: startmerkene `.kjoer.brukt` og `.kjoer.trukket` blir liggende i /home/ops etter hver kjøring, og `.kjoer` blir liggende når svaret på 665 går tapt. De skader ingen senere kjøring (MERKE er unikt per sekund), men mappen er alt full (maal/BYTTESKRIPT linje 8–68).
10. Merknad, køen: 25 minutters venting pluss inntil 15 ssh-kall etter den, hvert inntil 30–45 sekunder når verten svarer tregt, kan overstige 40 minutter. Da dreper vaktbikkja bare skallet (funn 6 i utgave 4, uendret), skriptet fullfører i leveransefila, men `svar.md` og `EXIT=143` blir feil.

## A. De ti funnene fra utgave 4

- Funn 1: rettet. Ferdig avgjøres bare av `HAVEN_DEPLOY_SLUTT=<kode>` (673, 725–736), tilbakelegging bare ved kode ulik 0 og 75 (762–772) eller beviselig aldri startet (668, 681, 698), og containeren kontrolleres før fila (603–611). `/proc` brukes ikke (test `test_root_brukes_bare…` 944). Rest: funn 5 over.
- Funn 2: bortfalt med funn 1; ikke lenger en måling som trengs.
- Funn 3: rettet. `CLAIM_TATT_HER=kanskje` (523), `FIL_SKREVET=kanskje` (642), `BYTTE_STARTET=kanskje` (672) settes før kallet, og `ved_slutt` (112–146) behandler kanskje som gjort. Holder ved lesing av alle grenene.
- Funn 4: rettet. Koden leses for seg (455–457), og et svar som ikke er en liste, stopper (462–463, 472).
- Funn 5: rettet. Fristen er klokkebundet, 1500 sekunder (720–721).
- Funn 6: ikke rettet, som oppgitt. Se funn 10 over om at 40 minutter ikke alltid holder.
- Funn 7: rettet. `FIL_HADDE_NY` sies i sluttlinjene (632–634), og `NEDE` sier «har hatt nedetid» (749).
- Funn 8: rettet for rekkefølgen (565, kontrollert med 571) og synliggjort for kopiene (439, 801). Kopiene fjernes fortsatt ikke; se funn 7 over om modus.
- Funn 9: rettet (295–364), med hullet i funn 1 over. `godtatt-bortfall.txt` virker som beskrevet (test 714–725).
- Funn 10: uendret, som oppgitt. En `die`-linje i haven-deploy 476 gjengir en fillinje uten «=» rått; det er en malformet linje, ikke en verdi.

## Påstandene i oppdraget

1. Holder, med merknadene over. 2. Holder: `exit 75` finnes bare ved låsen (haven-deploy 79, 83); kode 0 kommer bare fra `rollback` med `COMMITTED=1` (381), som settes rett før `COMMITTED_VERIFIED` (672–673); den andre `exit 0` er `--preflight` (306). 3. Holder, så langt jeg kan lese, med restrisikoen i funn 5. 4. Holder: alle tilstander der fila og containeren har hver sin liste, sies nå (633, 703, 761, 775, 777, 796). 5. Holder for innholdet (kjørt: linje på plass, andre linjer byte-like, siste linjeskift lagt til); modus og mtime endres. 6. Holder ved lesing av hver `log`, `feil` og `echo`: det som gjengis rått, er stien i SET_ENV_FILE (417, 419), revisjonsmerkelappen (238, 782), stat-felt, statusord og hasher. Fra lista kommer bare det regexen slipper gjennom. 7. Holder; sporene er `sudo -n -l` i auth-loggen og innloggingene. 8. Holder: kjørt med `ROT_SKRIV` kuttet på 83 steder, ingen endret fila, ingen rest; `hoved` uten argumenter stopper på `set -u`. 9. Nei; se C. 10. Holder ved lesing: ingen variabel rett foran ikke-ASCII (kjørt regex), ingen `case` inne i `$(…)`, ingen arrays på Mac-siden; `mawk 1.3.4` her er den Ubuntu har, og tok linja på 6 kB. Bash 3.2 er ikke kjørt. 11. Holder: `configuredInvites()` brukes bare i `onboardingPackage` (625) og `enroll` (709); grants ligger i tilstand, ikke i lista.

## B. Det nye, lest linje for linje

Startmerket (665–705): flyttingen er `rename`, så bare ett kall kan vinne. Kjørt (arbeid/tmp/start/race.sh): startkallet og tilbaketrekkingen samtidig i 40 runder, 29 startet og 11 trukket, ingen runde der begge trodde de vant. Et startkall som kommer fram etter trekkingen, finner ikke merket (test 1157). Får `ops` ikke skrive i /home/ops, stopper alt på 539 med claimen frigitt. `mv` over et navn som finnes, krever samme MERKE to ganger, som jeg ikke ser hvordan skjer; da stopper 563 uansett. Anførselstegnene: kjørt linje 673 gjennom en falsk ssh under både dash og bash; kommandoen kom fram som `nohup sh -c 'sudo -n … --env-only; echo "HAVEN_DEPLOY_SLUTT=$?"' > … & echo "startet $!"`, `$?` utvides først av `sh`, og loggen fikk `HAVEN_DEPLOY_SLUTT=3`.
Ventingen (715–742): et svar som feiler, er tomt eller mangler trailerlinja, telles ikke (kjørt med ni former for svar, bare «merke + logg-finnes» gir «sluttet»). En linje fra et startskall som skriver noe før kommandoen, ville gjort at merket aldri sees; utgave 3 sin `toerr` på Macen viser at verten ikke gjør det. `HAVEN_DEPLOY_SLUTT=` fra haven-deploy selv: den skriver aldri miljø eller argumenter (bare `log`/`die`, 137–138), så ordet kan bare komme fra ekkoet.
Lista som kjører (295–364): samme principal to ganger telles riktig (forsøk I), tom liste gir riktig «ingen borte» (forsøk J), dato uten sone og manglende felt gir HINDER (forsøk C3; `grantExpiresAt` som mangler, blir `null` og faller på regexen), manglende `principalID` blir principalen «null» og meldes borte. Hullet er funn 1.
HINDER (156–160, 512–516): kan stoppe `utfoer` på en vert i orden ved et forbigående ssh-brudd på verktøyspørsmålet eller listelesingen, ved principal-former tjeneren godtar (funn 4), og, etter hensikten, når lista på verten har gyldige invitasjoner som ikke står i den nye. Det siste vil trolig treffe første `utfoer`: lista fra 05.10 er på 4115 tegn og har 168 timers gyldighet, og den nye har bare de fire (lag-invitasjoner.sh 77). Eieren må kjøre `les` først og skrive `godtatt-bortfall.txt`.
Modus `les` (366–373): ingen root, ingen `hd`, ingen skriving (kjørt: `test_les_bruker_ikke_root…`).
Kopieringen (539–542): går gjennom samme ssh; en halv fil stoppes av sjekksummen (test 998), og den halve fila blir liggende i /home/ops som 600.

## C. Etterligningen mot det ekte

- Python: skriptets egne blokker kjører med `/usr/bin/python3`, som er 3.11 i skyen og 3.9.6 på Macen. Kjørt: 3.9 avviser «.81Z», 3.11 godtar. Testene prøver altså ikke datotolkingen slik Macen gjør den. `hd` prøves også med 3.11.
- `sudo` uten terminal: den falske gjør `exec`; den ekte er aldri kjørt slik (05.10 gikk via systemd, journalen i maal/HAVEN-DEPLOY-PAA-VERTEN). `requiretty` ville gitt kode 1, som skriptet håndterer som «sluttet» og legger tilbake; miljøet (HOME, PATH, LANG) under `sudo` er et annet enn under systemd, og `docker`/`jq`/`curl` finnes via `secure_path`.
- Loggen: ops lager den (600), root skriver gjennom arvet fd; ingen rettighetsfeil kan oppstå der, og `tee` gir samme etterslep som i etterligningen (ETTERVENT 744).
- `nohup sh -c` fra en ssh som lukkes: uten pty sender sshd ingen SIGHUP, og `nohup` setter SIG_IGN som arves gjennom `sudo`; logind kontrolleres. Etterligningen modellerer ikke sesjonsavslutning i det hele tatt.
- `docker inspect`: en stoppet container svarer med samme Id, Env og Labels; mellom `docker rename` (haven-deploy 615) og `docker create` (618) finnes ikke navnet, men skriptet leser ikke docker da. Etter en rullet-tilbake har navnet den gamle Id-en også når den gamle ikke kom opp; etterligningens «uverifisert» gir ny Id (test 262), så i virkeligheten legges fila tilbake der testen sier «ikke rørt», før helsekontrollen (628) stopper med claimen stående. Riktig, men annerledes enn testen viser.
- Den falske ssh kutter aldri et svar midt i; parseren er prøvd for hånd (over). Fjernskallet er dash i etterligningen; startlinja er prøvd under begge. Sandkassen er root, så skrivefeil i /home/ops og eierskap er ikke prøvd. Den falske `hd` har ingen lås.

## D. Det som ikke kan avgjøres uten verten

- At `sudo -n /usr/local/sbin/haven-deploy` går fra et ssh-skall uten tty, at `nohup`-prosessen overlever at forbindelsen lukkes, og at sluttmerket lander i loggen. Ett kall som ops avgjør alt, uten lås og uten endring: `nohup sh -c 'sudo -n /usr/local/sbin/haven-deploy staging xyz; echo "HAVEN_DEPLOY_SLUTT=$?"' > /home/ops/proeve.log 2>&1 < /dev/null &` og så lese loggen: ventet «FEIL: commit maa vaere 40-hex» og `HAVEN_DEPLOY_SLUTT=2` (haven-deploy 55, før låsen på 74).
- Hvilke principaler lista fra 05.10 har, og om de står i `godtatt-bortfall.txt`: `les` avgjør det.
- At root-innlogging virker, at fila eies av root med modus uten skriverett for gruppe og andre, har nøkkelen én gang og ingen doble: `toerr` avgjør det.
- At manifestet fortsatt er signert for revisjonen og at den offentlige statusfila er komplett (haven-deploy 244–286); feil her gir kode 1 før noe røres, og fila legges tilbake.
- Hva `busctl` svarer som ops, og om `/etc/systemd/logind.conf.d/` finnes: `les` viser det.
- At hele skriptet går i `/bin/bash` 3.2: første `les` på Macen kjører alle lesestiene.

## E. Dom, tre svar

1. `les`: ja.
2. `toerr`: ja, når eieren har sagt ja til to root-innlogginger som bare leser.
3. `utfoer`: ja, med forbehold: (a) rett funn 1, det tar ti linjer; (b) kjør prøvekallet i D først, så den første ekte `sudo`-kjøringen ikke er byttet; (c) kjør `les`, skriv `godtatt-bortfall.txt`, kjør `toerr` uten HINDER; (d) eieren har godtatt én omstart på ca. 35 sekunder.
Rettelser, viktigst først: funn 1 (pipefail i listelesingen); funn 2 (krev punktumet fra logind-spørsmålet); funn 3 (legg bare linja tilbake); funn 4 (utvid regexen til «@», og tolk datoen uten `fromisoformat` eller prøv med 3.9); funn 6 og 8 (ordlyd); funn 7 (rydd mktemp-fila i en `trap` i `ROT_SKRIV`).

## Hva jeg kjørte og leste

Alt i `arbeid/` på kopier, TMPDIR under `arbeid/tmp`, Python 3.9.23 som testkjører, bash 5.2, mawk 1.3.4, jq 1.7, coreutils 9.4. Ingenting i `kilder/` er endret, ingen maskin kontaktet. Seks av de 94 testene kjørt enkeltvis, alle grønne. `arbeid/forsoek.py` (forsøk A–K, utskrift i `arbeid/forsoek-utskrift.txt`), `arbeid/probe1.sh` (base64/jq), `arbeid/tmp/skriv2` (ROT_SKRIV og ROT_TILBAKE mot filer med kommentar, tom linje, nøkkel midt i og sist, uten siste linjeskift), `arbeid/tmp/kutt` (83 kutt), `arbeid/tmp/start` (linje 673 under dash og bash, kappløp 40 runder). Feilinnsettingen: `../hd0006-mutasjoner/slutt-bytt-utgave5.log` var tom da jeg skrev dette (15:43Z, mutant 68 av 100 i gang); jeg har ikke lest resultatet. Alle linjenumre gjelder `kilder/bytt-invitasjoner.sh` om ikke annet står.
