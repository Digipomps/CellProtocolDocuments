== maal-macos-skall: 2026-10-05T20:26:48Z, macOS 27.0, bash 3.2.57(1)-release ==
sprakinnstilling her: LANG=ikke satt LC_ALL=ikke satt LC_CTYPE=ikke satt
-- 1. ls -t: den nyeste forst?
   to filer som finnes:                                ny.json
   samme, i motsatt rekkefolge:                        ny.json
   pluss en som ikke finnes, med navn pa /Users:       gammel.json
   pluss en som ikke finnes, med navn pa ./ :          gammel.json
   pluss en som ikke finnes, med navn pa /zzz:         ny.json
   pluss to som ikke finnes (./ og /Users):            gammel.json
   (riktig svar er ny.json i alle linjene)
-- 2. en variabel rett foran et tegn utenfor ASCII, med og uten UTF-8
   LANG=(tom)        $P foran c2bb : kode 0, skrev [verdi??]
   LANG=(tom)        $P foran c3b8 : kode 0, skrev [verdi??]
   LANG=(tom)        $P foran e280a6 : kode 0, skrev [verdi???]
   LANG=(tom)        $P foran 2e : kode 0, skrev [verdi.]
   LANG=nb_NO.UTF-8  $P foran c2bb : kode 127, skrev /bin/bash: P?: unbound variable
   LANG=nb_NO.UTF-8  $P foran c3b8 : kode 127, skrev /bin/bash: P?: unbound variable
   LANG=nb_NO.UTF-8  $P foran e280a6 : kode 127, skrev /bin/bash: P?: unbound variable
   LANG=nb_NO.UTF-8  $P foran 2e : kode 0, skrev [verdi.]
   LANG=en_US.UTF-8  $P foran c2bb : kode 127, skrev /bin/bash: P?: unbound variable
   LANG=en_US.UTF-8  $P foran c3b8 : kode 127, skrev /bin/bash: P?: unbound variable
   LANG=en_US.UTF-8  $P foran e280a6 : kode 127, skrev /bin/bash: P?: unbound variable
   LANG=en_US.UTF-8  $P foran 2e : kode 0, skrev [verdi.]
   (tegnene er vist som byte: c2bb er hoyre anforselstegn, c3b8 er o med strek, e280a6 er tre prikker, 2e er punktum)
   med klammer, LANG=nb_NO.UTF-8: [verdi??]
-- 3. set -u og en tom "$@"
   for a in "$@" uten argumenter:        kode 0, gikk
   kommando med "$@" uten argumenter:    kode 0, gikk
   kommando med ${1+"$@"}:              kode 0, gikk
-- 4. det bash her ikke har
   mapfile -t a < /dev/null                     kode 127, /bin/bash: mapfile: command not found
   x=AB; echo "${x,,}"                          kode 1, /bin/bash: ${x,,}: bad substitution
   declare -A m; m[a]=1; echo "${m[a]}"         kode 0, declare: -A: invalid option
   echo "${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}" kode 0, 3.2
-- 5. [ a -nt b ]
   ny -nt gammel: ja
   gammel -nt ny: nei
   gammel -nt en som ikke finnes: ja
   en som ikke finnes -nt gammel: nei
   to med samme tid: den andre -nt den forste: nei
-- 6. sprakinnstillinger med UTF-8 pa denne maskinen (de forste)
   en_US.UTF-8
   C.UTF-8
   nb_NO.UTF-8
Ferdig. Ingenting er endret.
