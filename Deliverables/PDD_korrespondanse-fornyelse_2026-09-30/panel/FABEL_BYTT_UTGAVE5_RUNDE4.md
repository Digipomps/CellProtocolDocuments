# Kontroll av fjerde runde i bytt-invitasjoner.sh (utgave 5, 06.10.2026)

## Dom
Ingen funn blokkerer. Jeg fant ingen vei der haven-deploy arver umask 077, der loggen blir åpen for andre,
der et merke blir `.brukt` uten at noe ble forsøkt, der noe startes to ganger, eller der linja legges
tilbake mens låsen holdes. `toerr-<stempel>` kan kjøres når eieren har sagt ja til root; `utfoer-<stempel>`
kan kjøres etter ny les/proevestart/toerr uten HINDER — ja, med forbeholdene i funn 1–2. De sju forrige merknadene er svart på.

## Funn, viktigst først
1. **[merknad] utfoer er aldri kjørt mot den ekte verten.** Lest i hodet (linje 16, 53–54) og test_bytt.py
   (linje 28–29): bare `les` og `proevestart` er kjørt mot verten (maal/LES-2, PROEVESTART-2, 18:26–18:28Z);
   «første kjøring der er den ekte testen». Kjørt: hele skytestrekka er grønn (hele-testrekka.log: «Ran 133
   tests … OK»), men den prøver en etterligning. Et forbehold ved å kjøre utfoer, ikke en feil i koden.
2. **[merknad] Prøvestarten beviser mindre enn den fulle deployen trenger.** Lest (linje 554–582) og kjørt
   (egen test, `ByttMedVentingIProevestarten…tar_like_lang_tid`, OK): med PROEVEVENT=5 kreves `PTOK<PROEVEVENT`,
   PTOK = startkallets sekunder + 1, så startkallet var ferdig (forbindelsen lukket, SSH-OPPSETT-1 linje
   5–18/34) før sudo kjørte, og skallet levde ≥5 s etter. Ikke bevist: at det lever de ~35 s en ekte deploy
   tar, og at ssh/logind er likt ved byttet. PROEVEFILER-1 viser ventingen (merke `.brukt` 18:27:42Z, logg
   18:27:48Z; og 17:06:48→53Z). Med PROEVEVENT=0 (testene) sier linja selv at prøven ikke viser dette.
   `-ge` er på trygg side (+1 dekker avrunding til hele sekund).
3. **[merknad] «mangler = ingen holder» er holdbart, med ett ufarlig vindu.** Lest i ekte haven-deploy
   (linje 73–75): mappe og låsefil lages FØR låsen tas, og /run tømmes ved omstart; finnes ikke fila, har
   ingen deploy passert linje 74. Eneste vindu: mellom linje 74 og 75 lever en deploy mens `laas_naa` ennå
   svarer «fri» — ufarlig, for den har ikke lest SET_ENV_FILE (linje 491+), og hd-claim + haven-deploys
   egen flock verner. Ikke dårligere enn før. Kjørt (egne flock/setpriv-forsøk, holder stoppet ved egen
   pid): kartet fri/mangler/holdt/ukjent stemmer. På verten (PROEVEFILER-1: mappe 711, fil 644) svarer
   `laas_naa`: fil finnes → fri/holdt, fil mangler → mangler (711 har o+x, ulikt 700 som gir ukjent).
4. **[merknad] tilbake_til_foer: ingen kombinasjon er dårligere enn i `…foer-runde4`.** Lest (linje
   859–890) mot diffen (196–241): `fri`/`mangler` → legg tilbake; `holdt` → ventes på uansett LAAS_LESBAR
   (inntil seks ventetider), så return 1; `ukjent`/tomt med LAAS_LESBAR=ja → return 1, med nei → videre «på
   sluttmerket alene». `mangler`, og at `holdt` nå ventes på selv ved LAAS_LESBAR=nei, er bedre enn før —
   forrige funn 3 er rettet. Linja legges aldri tilbake på `holdt`. I utfoer kan LAAS_LESBAR=nei bare komme
   av at første svar var `ukjent`: `holdt`/tomt før byttet er nå HINDER (linje 356–360) og stopper utfoer
   før claimen. Kjørt (egen test «mangler før / tomt etter», OK): «mangler» før byttet teller som svar.
5. **[merknad] umask-fiksen virker; produksjonsverdien er bekreftet utenfor testen.** Lest (linje 459,
   468–469): umask 077 settes bare i underskallet for loggen; skallet som kjører sudo har øktens umask.
   Kjørt (egen etterligning i bash og dash): logg 600, deploy startet med umask 0002, en fil deploy lager
   uten chmod ble 664. Kjørt (egen umask-test, OK): deploy noterer 0022 (testens økt), låsemappe 755, fil
   644, fire ops-filer 600. På verten er øktens umask 0002 → låsefil 664 (o+r, lesbar); låsemappen 711 kommer
   fra systemd, ikke haven-deploys mkdir, og er nok. Testen beviser arv av øktens umask; verdien 0002 er
   bare bekreftet av mitt eget forsøk.
6. **[merknad] Noen få endringsdeler mangler samlet dekning.** Lest: sekvenstestene (fake «laas-svar»)
   mater inn låsesvar uten å kjøre den ekte `laas_naa`; «ekte mangler/fri inne i en tilbakelegging» testes
   ikke ende-til-ende (bitene testes hver for seg). Vinduet mellom `FIL_LAGT_TILBAKE=true` og
   `FIL_SKREVET=false` (linje 914–915) kan ikke treffes av harnesset; rekkefølgen er nå snudd så et avbrudd
   der gir «STÅR FORTSATT» (trygt), og effekten er dekket av mutant + test. Vinduet linje 74–75 (funn 3) har
   verken test eller innsatt feil.

## Oppdragets spørsmål
**A. Diffen.** Kjørt: `diff -u` er byte for byte lik diff-skript.txt (uten de to hodelinjene), likeså
testdiffen. SHA-256 nå 2e0fac7c… (=SYNTAKS-4), før 425c9cee… (=SYNTAKS-3), haven-deploy = DEPLOY_SHA
339a03a4… Hvert stykke svarer til et oppdragspunkt; det eneste uoppførte er hodefiksen «et punktum og seks
tegn» (forrige funn 7), ren kommentar uten adferdsendring. Ingen endret oppførsel utenfor de nevnte stedene.
**B. Startkallet.** Kjørt (bash og dash, ufarlig kommando): lik oppførsel i begge. Logg 600; det som kjøres
får øktens umask; `>>` appender til en logg som finnes. Merke mangler → ikke-startet, tom logg igjen, intet
startet, ikke `.brukt`. Logg kan ikke lages → `&&` stopper `mv`, merket ikke `.brukt`, intet startet. `sleep`
feiler → haven-deploy kjøres ikke, sluttmerket får sleep-koden. `.brukt` betyr alltid at skallet ble startet.
Byttet og prøven bruker hvert sitt merke/logg — ingen dobbeltstart.
**C. Prøvestarten.** Se funn 2; `-ge` og +1 er riktige og konservative.
**D. Låsen.** Se funn 3–4. Ingen tilstand der `mangler` faller sammen med en levende deploy forbi linje 74.
**E. Testene.** Kjørte fire enkelttester (én om gangen, alle OK): umask-kravet, sleep-feil, «mangler før /
tomt etter», PTOK-vakten. De prøver det navnene sier og kan ikke bli grønne av annen grunn (leser umasken,
teller låsespørsmål, pinner melding og claim). Mutantdiffen (145, var 127) har nye feil for nettopp disse
stedene. Udekte biter: funn 6.
**F. Dom.** Se øverst. Blokkerer: ingen. Merknader: funn 1–6. Forrige rapports sju merknader: 1→funn 5,
2→funn 2, 3→funn 4, 4→nye laas-tester, 5→rekkefølge snudd (vindu udekt, funn 6), 6→`laas_naa` svarer nå
`mangler`, 7→hodet rettet. Alle svart på.

## Hva jeg leste og kjørte
Lest: hele skriptet og `…foer-runde4`, begge differ, hele ekte haven-deploy, test_bytt.py og testdiffen,
mutantlista og mutantdiffen, vert.sh, les-ssh-oppsett.sh, les-proevefiler.sh, runner.sh.koeen, forrige
rapport, forsoek-laas-mangler, og alle maal/-filene. Kjørt i arbeid/ på kopier (TMPDIR=arbeid/tmp, Python
3.9.23, bash og dash): diff-sammenlikning, start_kall-formen, flock/setpriv-forsøk med låsen, fire
enkelttester. Ingenting i kilder/ endret, ingen maskin kontaktet, ingen `pkill`/`killall`; bare egne
prosesser stoppet ved pid. Den lange feilinnsettingen er ikke rørt.
