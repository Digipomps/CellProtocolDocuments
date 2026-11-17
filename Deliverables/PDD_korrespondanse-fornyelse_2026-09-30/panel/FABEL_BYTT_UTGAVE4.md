# Fabels kontroll av `bytt-invitasjoner.sh`, utgave 4 (06.10.2026)

## Dom

`toerr` kan kjøres mot verten nå: den leser bare, og de to root-innloggingene kjører korte skript med sed, stat, grep og sha256sum. Den avgjør dessuten flere av punktene under som ikke kan avgjøres herfra.
`utfoer` bør ikke kjøres før funn 1 er rettet og funn 2 er målt: skriptet legger fila tilbake og frigir claimen i tre forløp der haven-deploy fortsatt kan gå, og sier da «staging står som før». Rettingen er liten og sitter på ett sted.
Etter det: ja, med forbeholdene i funn 3 til 6 og lista over det som bare verten kan vise.

## Funn, viktigst først

### Funn 1 (blokkerer): «sluttet» og «fikk ikke prosessnummer» fører til tilbakelegging og frigitt claim uten at det er kontrollert at haven-deploy ikke går

Sted: `bytt-invitasjoner.sh` linje 434–440 (ingen PID), 451–458 (vaktløkka avgjør «sluttet» med `[ -d /proc/$PID ]`), 473–476 («sluttet» → `tilbake_til_foer`), 386–407 (`tilbake_til_foer` legger fila tilbake FØR den ser på containeren, og godkjenner når containeren ennå er den gamle).

Tre forløp utløser det, alle kjørt i etterligningen (arbeid/forsoek.py, forsøk 1, 2 og 4):

1. ssh starter `nohup sudo … &` på verten, men svaret med `$!` kommer ikke fram (forbindelsen faller i det korte vinduet mellom start og ekko). Skriptet går til linje 437, legger fila tilbake, ser samme container-id, samme revisjon, samme liste, skriver «ok staging står som før», frigir claimen og slutter med kode 8. haven-deploy går videre uten claim, stopper og lager containeren på nytt (ca. 35 sekunder nede, uanmeldt). Leste haven-deploy fila før tilbakeleggingen, får containeren den nye lista mens fila har den gamle; neste utsetting setter da den gamle lista tilbake stille. Målt i forsøk 1: etter at skriptet sa «står som før», hadde verten ny container-id.
2. De siste logglinjene lander etter at prosessen er borte. Den ekte haven-deploy skriver alt gjennom `exec > >(tee -a …)` (haven-deploy linje 159); tee er en egen prosess, og linja «COMMITTED_VERIFIED» kan lande i `$LOGG` etter at sudo har avsluttet. Vaktløkka sjekker loggen først og `/proc` etterpå, så en poll i det vinduet gir «sluttet». Målt i forsøk 2 (tee forsinket): skriptet skrev «sluttet uten COMMITTED_VERIFIED», «Containeren ble aldri stoppet», la den gamle fila tilbake, fant ny container-id og lot claimen stå. Sluttilstand: ny liste i containeren, gammel liste i fila, altså det neste utsetting reverserer stille. Vinduet er i praksis millisekunder, men utfallet er den verste klassen, og rettingen koster nesten ingenting.
3. `/proc/<pid>` er ikke synlig for ops. Prosessen skriptet husker er sudo, som kjører som root. Er /proc montert med `hidepid=1` eller `2` (vanlig herding, ikke Ubuntu-standard), er `[ -d /proc/$PID ]` alltid falsk for ops, og skriptet sier «sluttet» ved første poll etter ti sekunder, mens haven-deploy er midt i stoppen. Målt i forsøk 4: fila lagt tilbake, «ok staging står som før», claim frigitt, haven-deploy går fortsatt. Etterligningen kan ikke vise dette, for der er `$PID` haven-deploy selv og sandkassen kjører som root.

Kostnad: claimen frigis mens en utsetting går; staging startes på nytt etter at skriptet har sagt at alt står som før; i forløp 1 og 2 kan fila og containeren ende med ulik liste med en utskrift som peker feil vei.

Retting (ett sted): før `tilbake_til_foer` kalles fra linje 438 og 475, må skriptet bevise at haven-deploy er ferdig, uavhengig av `/proc`. Enklest: la ops-skallet skrive et sluttmerke selv, `nohup sh -c 'sudo -n … ; echo "HAVEN_DEPLOY_SLUTT=$?"' > $LOGG 2>&1 < /dev/null &`, vent til merket står i loggen, sov noen sekunder og les loggen én gang til etter COMMITTED_VERIFIED og «ROLLBACK ferdig» før utfallet avgjøres. Mangler PID, skal `[ -f $LOGG ]` på verten regnes som «startet» og gå inn i den samme ventingen i stedet for å legge tilbake.

### Funn 2 (må måles før utfoer): om ops ser andres prosesser i /proc

Sted: samme som over. Én kommando som ops avgjør det: `[ -d /proc/1 ] && echo ser || echo ser-ikke` (PID 1 er root). Den hører hjemme i `toerr`, ved siden av `sudo -n -l`, slik at forutsetningen i vaktløkka blir en måling. Med rettingen i funn 1 forsvinner avhengigheten, og dette blir en merknad.

### Funn 3 (merknad): to flagg settes etter handlingen, så et signal i vinduet gir feil sluttmelding

Sted: linje 412–415 (`FIL_SKREVET=true` settes etter at root har byttet linja) og 325–326 (`CLAIM_TATT_HER=true` etter `hd coord claim`). `BYTTE_STARTET` (linje 433) er derimot satt før kallet, som er riktig.

Bash kjører en trap først når kommandoen som går er ferdig. Kommer SIGTERM mens ssh-kallet som skriver fila er i gang, fullføres skrivingen, trapen kjører, og `ved_slutt` ser `FIL_SKREVET=false`: den frigir claimen og skriver «fila under /etc/haven og containeren er ikke rørt» mens fila har den nye lista (målt, forsøk 3). Samme mønster ved claimen: claimen tas, skriptet sier bare «AVBRUTT (signal).», og claimen blir stående uten ord (målt, forsøk 6). Vinduet er ett til to sekunder per kjøring, og jobbkøen leverer ikke signalet (funn 6), så bare et manuelt `kill` treffer det. Retting: sett flagget før kallet, eventuelt som et eget «kanskje skrevet»-flagg som `ved_slutt` behandler som skrevet.

### Funn 4 (merknad): en feilende `hd coord status` leses som «ingen claimer»

Sted: linje 276–286. `|| feil` gjelder bare python-leddet i røret; feiler `hd` (låsen i `hdlib/cli.py` linje 762–765 gjelder også `coord status`), får python tom inndata, `except` gir `claims = []`, og skriptet skriver «claimer på verten: ingen». Målt i forsøk 5: med en claim fra HD-0077 på verten og en `hd` som feiler, sa `toerr` «ingen» og gikk ut med kode 0. I `utfoer` fanges det delvis av at `hd coord claim` også feiler, men bare når feilen varer. Retting: `set -o pipefail` rundt røret, eller lagre `hd`-utskriften i en variabel og kontroller koden.

### Funn 5 (merknad): ventetida på ti minutter er kortere enn det haven-deploy kan bruke

Sted: linje 66 og 451 (60 runder à 10 sekunder) mot haven-deploy linje 357 (`wait_ready` inntil 72 × 5 sekunder per fase), 571 (`docker stop -t 60`), 640 (omstart med ny `wait_ready`) og 414 (`wait_ready` også i rollback). I verste fall er haven-deploy lovlig i gang i nærmere tjue minutter. Da ender skriptet i tilstand (d) med claimen stående og fila urørt, som er trygt, men utfallet må leses og avsluttes for hånd selv om haven-deploy til slutt lykkes eller ruller rent tilbake. 05.10 tok det 35 sekunder, så dette treffer bare når readiness drar. Retting: hev taket til omtrent 25 minutter, eller la løkka vente på sluttmerket fra funn 1.

### Funn 6 (merknad, gjelder jobbkøen): vaktbikkja stopper ikke skriptet, bare skallet rundt det

Sted: `runner.sh.koeen` linje 181 (`( ulimit … && cd … && bash "$SKRIPT" … ) &`) og 195–200 (`kill -TERM -"$CHILD" || kill -TERM "$CHILD"`). Uten jobbkontroll er `$CHILD` ingen prosessgruppeleder, så det første `kill` feiler, det andre treffer bare subskallet, og `bash bytt-invitasjoner.sh` lever videre som foreldreløs med claimen og med utskrifta inn i leveransefila, mens køen skriver `EXIT=143`, kopierer en avkortet svarfil og går videre. Målt i forsøk 7 med bash 5.2 her; bash 3.2 på Macen har færre optimaliseringer, så jeg slutter at det er likt der. Testen `ByttSomHenger.test_stoppes_skriptet…` sender TERM rett til skriptet og viser derfor en vei køen ikke har. Skriptets egen TERM-trap er riktig; det er køen som ikke når fram.

### Funn 7 (merknad): sluttmeldingen etter en tilbakerulling når fila alt hadde den nye lista

Sted: linje 409–410 setter ikke `FIL_SKREVET`, så `tilbake_til_foer` (linje 405) og `ved_slutt` (linje 92) sier «staging står som før». Det er sant for denne kjøringen, men fila har den nye lista, og neste utsetting setter den i kraft. Linje 265 varslet det tidligere i utskrifta; sluttlinjene burde gjenta det. Dette er den eneste veien jeg finner der «fila ny, container gammel, alt står som før» er sant og sagt; de usanne variantene står i funn 1 og 3. Småting i samme område: `NEDE` (linje 464) sier «har vært nede» også når containeren fortsatt kan være nede.

### Funn 8 (merknad): fila endrer linjerekkefølge, og kopiene blir liggende

Sted: linje 356–357 skriver de andre linjene først og den nye linja sist, så nøkkelen flytter fra sin plass (trolig først, etter rekkefølgen i journalen 05.10) til slutten; haven-deploy bryr seg ikke om rekkefølgen. Linje 363 lager `$FIL.foer-<stempel>-<klokke>` og ingen fjerner den; hver kjøring som skriver legger igjen en kopi under /etc/haven med alle seks variablene, HAVEN_CREDENTIAL_MASTER_KEY medregnet, som root 600. Påstand 2 holder for innholdet i de fem andre linjene og deres innbyrdes rekkefølge, ikke for fila byte for byte. Mangler siste linjeskift i fila i dag, legger `grep -v` det på.

### Funn 9 (merknad): det synes ikke hva den nye lista tar bort

`lag-invitasjoner.sh` (linje 16–17 og 82) skriver bare de fire som fornyes nå. Containerens verdi i dag er 4115 tegn (maal/HAVEN-DEPLOY-PAA-VERTEN), som er mer enn fire invitasjoner. `toerr` viser navnene i den nye fila, men ingenting om hvem som står i lista som kjører, så den som godkjenner kan ikke se av utskrifta hvilke invitasjoner som forsvinner. Det er ikke en feil i byttet, men en manglende måling før beslutningen.

### Funn 10 (merknad): strykingen i `vis_logg` er regelbasert

Linje 447 skjuler `=` fulgt av 12 tegn eller mer, og tegnrekker på 40 eller mer. En FEIL-linje med en kort verdi ville slippe gjennom. Jeg har lest alle `die`-meldingene i den ekte sammenslåingen (haven-deploy linje 476–532): de skriver navn, aldri verdier, så dette er en restrisiko, ikke et observert hull.

## Påstandene i oppdraget

1. Riktig. haven-deploy linje 491–533 leser SET_ENV_FILE ved hver kjøring og erstatter den arvede linja; journalen 05.10 viser `satt: … HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 …; fil: /etc/haven/staging-correspondence-invites.env`. Utgave 3 ville blitt skrevet over.
2. Ikke målt. Seks navn følger av «satt:»-lista minus de to i SET_ENV i konfigen fra repoet; `toerr` måler det (linje 261). Se funn 8 om «byte for byte».
3. Holder for skriptets egen utskrift, ved lesing av hver `log`, `feil` og `echo`: det som vises er sjekksummer, navn, stier, antall og statusord. Den eneste verdien fra verten som gjengis rått er stien i SET_ENV_FILE (linje 240–242). Restrisiko i funn 10.
4. Holder med unntakene i funn 1 og 3, der utskrifta sier (a) eller (c) mens tilstanden er en annen.
5. Nei. Avvik som endrer utfallet: `$PID` er haven-deploy selv i etterligningen og sudo (root) på verten, og `/proc`-synlighet prøves ikke; loggen skrives rett i fila i etterligningen og gjennom tee på verten; etterligningen leser fila straks, den ekte etter flere sekunder forkontroll, som åpner vinduet i funn 1 forløp 1; svaret kan ikke gå tapt etter at jobben er startet i noen test; den falske `hd` har ingen lås; sandkassen rydder zombier først etter rundt to sekunder (PID 1 er `process_api`), mens systemd gjør det straks; køens TERM når ikke skriptet.
6. Mac-delen er bash 3.2-ren ved lesing: ingen arrays i skriptet selv, `read -d ''` har eksistert siden bash 2.04 og returnerer 1 ved EOF med innholdet satt (målt i bash 5.2 her, ikke på Macen). Vertsdelen er GNU: `stat -c`, `date -r`, `mktemp` med stimal, `sed -E` og `sha256sum` virker som skriptet venter (målt her, under «Hva jeg kjørte»).

## Den ekte `haven-deploy --env-only` mot det som er målt (C)

Før noe røres, og uten ROLLBACK-linjer (trapen settes først på linje 439), kan den stoppe på låsen (kode 75), manglende konfigfelt, `current` uten APP_BUILD_REVISION, bilde eller merkelapp som ikke stemmer, ikke-kanonisk APP_BUILD_TIMESTAMP, manglende mounts, manifest som ikke er signert for revisjonen (linje 246), `haven-manifest-provision --preflight` som ikke svarer «observed», og den offentlige statusfila som ikke er komplett eller peker på en annen revisjon eller et annet bilde (linje 272–286). Skriptet håndterer alle som «sluttet», og det er riktig, med forbeholdet i funn 1. Målingene gjør bilde, merkelapp, mounts, kommando og porter trygge; manifestrevisjonen og statusfila er ikke lest i dag, men ble skrevet av samme haven-deploy 05.10.
Etter trapen men før STOPPED kan den dø på arvet miljø, fingeravtrykk og mounts; rollbacken starter da bare den gamle containeren igjen og skriver «ROLLBACK ferdig», uten nedetid. Etter STOPPED er den eneste nye sjekken i env-only at emitter-filene er uendret mellom `fingerprint_pre` og `fingerprint_before` (linje 604); `IdentityNamedEmitters.json` ble endret 06.10 07:19 (maal/FINGERAVTRYKK), så runtime skriver den i drift, og en skriving under stoppen gir rollback med nedetid. Etter start og omstart gjelder `compare_after_start`, revisjonen som serveres, `RestartCount` og `publish_staging_status`; feiler statushjelperen, rulles en frisk kandidat tilbake (linje 655). Fila leses én gang, på linje 512–518, sekunder etter start, og røres ikke etterpå; låsen slippes når prosessen dør. Loggen på stdout har stier, fingeravtrykk og kvitteringen i JSON, ingen miljøverdier. `--env-only --preflight` er bekreftet ikke å være en tørrkjøring: MODE er tredje argument alene (linje 48–56).

## Tilbakeleggingen (D)

Kan fila legges tilbake mens haven-deploy bruker den: ja, i de tre forløpene i funn 1. Kan claimen frigis mens noe går: ja, i de samme. Finnes en vei der fila er ny, containeren gammel og skriptet sier at alt står som før: ja, usant i funn 3 (signal under skrivingen) og sant men lett å misforstå i funn 7. Veiene «rullet» og tidsavbrudd er riktige: ved «ROLLBACK ferdig» er haven-deploy ferdig med fila, og ved tidsavbrudd legges ingenting tilbake.

## Det jeg ikke kunne avgjøre uten verten (E)

- At root-innlogging med samme nøkkel virker; alle målingene i maal/ er gjort som ops. `toerr` avgjør det.
- At `/etc/haven/staging-correspondence-invites.env` finnes, eies av root, har rettighet uten skriverett for gruppe og andre, har seks variabler og nøkkelen én gang. `toerr` avgjør det.
- Om `/proc` er montert med hidepid (funn 2). Én kommando som ops avgjør det.
- At manifestet er signert for e5c3434… og at den offentlige statusfila er komplett og peker på samme revisjon og bilde-id. Feil her stopper haven-deploy før noe røres.
- At `sudo -n haven-deploy` rett fra et ssh-skall uten terminal oppfører seg som via systemd (`requiretty`, `use_pty`), og at logind ikke dreper sesjonens prosesser ved utlogging (`KillUserProcesses`); loggene fra 08.09 og 30.09 under /home/ops tyder på at nohup-veien har virket. `grep KillUserProcesses /etc/systemd/logind.conf` som ops ville sagt det.
- At `IFS= read -r -d ''` og resten av skriptet går i /bin/bash 3.2 på Macen; den første `toerr` kjører alle lesestiene og avgjør det.
- Hvor lang tid readiness tar i dag (funn 5).

## Hva jeg kjørte

Alt i `arbeid/` på kopier, med `TMPDIR` under `arbeid/`, Python 3.9 og bash 5.2 i skyen; ingenting i `kilder/` er endret, og ingen maskin er kontaktet.

- 13 av de 63 testene i `proeve-sky/test_bytt.py`, valgt rundt bytte, tilbakerulling, tilbakelegging og henging: alle grønne. Feilinnsettingen leste jeg fra `../hd0006-mutasjoner/slutt-bytt-utgave4.log` (ferdig 12:56Z): 64 av 64 fanget. Jeg kjørte den ikke selv.
- `arbeid/forsoek.py`, bygd på etterligningen i testfila: forsøk 1a/1b (svaret på startkallet går tapt, haven-deploy leser fila etter 0 og 3 sekunder), forsøk 2 (tee forsinket 9 sekunder), forsøk 3 (SIGTERM under root-skrivingen), forsøk 4 (`/proc` usynlig, haven-deploy henger), forsøk 5 (`hd coord status` feiler med en fremmed claim), forsøk 6 (SIGTERM under `hd coord claim`). Utfallene står i funn 1, 3 og 4.
- `arbeid/vakt-runner.sh` og `vakt-indre.sh`: etterligning av runnerens linje 181 og 195–200 (forsøk 7). Prosesstreet viste subskall og skript som to prosesser i samme gruppe; `kill -TERM -CHILD` feilet, `kill -TERM CHILD` ga rc 143 i runneren, og det indre skriptet fullførte uten signal.
- `arbeid/sen-tee.sh`: prosess død og zombie i to sekunder før loggen fikk COMMITTED_VERIFIED; viste også at sandkassen rydder zombier sent.
- GNU-kanter: `grep -c` på tom fil gir 0 med kode 1; `grep -c` på fil uten siste linjeskift teller én mer enn `wc -l`; `sha256sum` av tom inndata gir e3b0c442…, som er 64 tegn og derfor passerer lengdesjekkene på linje 199 og 259 men aldri likhetssjekkene; `stat -c %a` gir fire sifre på en fil med setuid, som mønsteret på linje 253 avviser; `mktemp` med stimal lager 600 root; sjekksummen av «K=v\n» er lik sjekksummen av en fil med den linja; `IFS= read -r -d ''` fra heredoc gir kode 1 og beholder siste linjeskift. bash kjører EXIT-trapen ved SIGTERM, så haven-deploys rollback kjører også om sudo drepes.

Ingen verdi som ser ut som en hemmelighet står i kildene; testfila bruker oppdiktede verdier, og målingene er strøket.
