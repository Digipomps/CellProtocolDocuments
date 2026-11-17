# GUI-gjennomgang — Workbench hjelpechat

2026-10-10. G1 godkjent. **Dette er P1-GUI, ikke implementering eller deploy.**

## Det Kjetil tar stilling til

Godkjenning gjelder de gjengitte kandidatbildene i [galleriet](GUI_GALLERY.html),
med bytehashene i `images/image-manifest.json`: layout, lys/mørk stil, innganger,
perspektiv-/modellvalg, egne pakker, kontekst, deling, historikk og feiltilstander.
G1-GUI ble godkjent 2026-10-11; se `evidence/g1-gui-approval.json`. En GUI-godkjenning betyr ikke at backend, rettigheter eller
produksjonsklarhet er godkjent; G2-plan og G3-akseptanse gjenstår.

| Flate | Kandidater |
|---|---|
| Developer Workbench + hjelpechat | Tom, fylt, frakoblet/uavklart køstatus; lys/mørk |
| Selvstendig hjelpechat | Tom, fylt, frakoblet, blokkert merge, ekstern modell; lys/mørk |
| Butler-innbygging | Tom, fylt, frakoblet; lys/mørk |
| Egne perspektivpakker | Ny, fylt, versjonskonflikt; navn, formål, instruksjoner, skills/kontekst, deling |
| Kontekst og skills | Valgte/tilgjengelige kilder og skills; lys/mørk |
| Del pakkeversjon | Konkrete referanser, versjon, publikum og avslag; lys/mørk |
| Ekstern modell | Mottaker, eksempelmodell, valgte utdrag, avslag og lokal vei; lys/mørk |
| Historikk | Privat, prosjektets delte hendelse, ingen treff, utilgjengelig; lys/mørk |
| Skeleton-komponent | To uavhengige mounts/samtaler; lys/mørk |
| Smal bredde | Selvstendig chat tom/fylt/frakoblet, 390 px; lys/mørk |

Alle person-, prosjekt-, modell- og jobbeksempler er syntetiske. «Tillatt rute»,
«lokal modell», tidsstempler og tilgangsstatus er eksempeltilstand, ikke verifisert
tilgang eller aktuelle leverandørvalg. Butler-rammen er også en kandidat, ikke en
påstand om dagens Butler-side. Den samme hjelpechat-Skeletonen brukes i de tre
vertsflatene per tema; det er ikke laget en separat React-chat.

## Kontroll som faktisk er utført

54 offline rendringer, 926 registrerte kontrollhandlinger på 43
keypaths. Ingen registrerte JS-/unsupported-/komponentfeil eller horisontal overflyt.
Laveste målte tekstkontrast er 4.99:1; måleavgrensning står i `images/README.md`.
Alle synlige knapper og felt i hver rendring er aktivert/fylt og alle picker-valg
registrert. Dette er dispatch-bevis, ikke bevis på en utført domenehandling.

Komponentprøven kontrollerte forskjellige strenger med forskjellige mount-ID-er
ved Ctrl+Enter, og session-ID-er på Send. Direkte innsetting av fixture-projeksjon
viste at et perspektivvalg kan oppdateres uten å endre den andre velgeren, og at
to mounts kan vise et felles perspektiv mens lokale utkast bevares. Dette beviser
ikke ekte session-synkronisering, Flow, replay eller backendisolasjon.

## Konkrete implementeringskrav fra prøven

1. **Skriv → Send/Lagre:** vanlig TextArea-input huskes lokalt; i denne isolerte
   rendereren sendte klikk på Send og Lagre bare den konfigurerte ID/revisjonen.
   Ny tekst manglet. Dette ble målt i begge temaer. Host-adapteren/cellekontrakten
   må sende ferske feltverdier atomisk med riktig mount, session og forventet
   revisjon. Samme krav gjelder typed search/title; disse to siste forløpene er
   ikke påstått funksjonelt testet. Ingen rendererendring er implementert her.
2. **Explore og actions:** `helper.*` i kandidaten er et foreslått bindingssett.
   Eksisterende Helper `ask`, `selectSet`, `saveSet` osv. må bevisst gjenbrukes eller
   utvides. Det nye settet er ikke validert mot en live Explore-manifest og skal
   ikke importeres som en ferdig operativ konfigurasjon.
3. **Velgere/forhåndsvisning:** søk sender en queryID, deling en previewID/revisjon.
   Backend må lese gjeldende valg, binde dem til samme bruker og avvise en foreldet
   forhåndsvisning. Valg alene autoriserer ingen deling eller ny modellrute.
4. **Hendelser og lagring:** kommando → autorisert varig endring → hendelse →
   projeksjon. Aktiv modellturn fryser kontekst/pakke; reconnect henter snapshot+
   etterslep. Replay kjører ingen effekt. Dette er godkjente krav, ikke funksjoner
   implementert av bildeharnessen.
5. **Privat/felles:** rå samtale holdes privat; prosjektet får bare eksplisitte
   minimale hendelser/utdrag. Tilgang må håndheves også for søk, counts, snippets,
   cache og embeddings. Ingen privacy-/rettighetstest mot backend er kjørt her.
6. **Autoritative kvitteringer:** køstatus leses med samme commandID ved usikkert
   utfall. AgentRun er en projeksjon, ikke en utfører. Merge og deploy trenger
   verifisert kilde/head/mandat og riktige effektceller. Ingen jobber er startet.

`SOURCE_AUDIT.md` og `SURFACE_ACTIONS.md` er grunnlaget for dagens kildegrenser og
hvor øvrige handlinger hører hjemme. Disse bildene erstatter ikke hele Board,
Configuration Studio, Agreement eller Admin-GUI. De flatenes konkrete endringer
må ha egne godkjente referansebilder dersom G2-arbeidet endrer dem.

## Videre kontroll

Swift-fabrikk må senere sammenlignes kanonisk med godkjent JSON, og faktisk
backend-state må rendres og sammenlignes med de godkjente bildene. Native Binding,
autentisert Porthole, tilgjengelighet og hele idé→prod-forløpet må testes før G3.
Ingen produktkode, build, CI, PR, merge eller deploy er gjort av denne GUI-leveransen.

Uavhengig gjennomgang: se `GUI_INDEPENDENT_REVIEW.md` når etterkontrollen er ferdig.
