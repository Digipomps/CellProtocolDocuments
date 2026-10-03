# Trinn 5: status, pause og stopp over kontrollbroen

Menylinjen og HAVEN får se planlagte jobber og sette dem på pause eller stoppe dem. Opprett og endre fra HAVEN er en egen runde (E3).

## Rutene

Begge ligger i `AgentControlBridgeServer` på 127.0.0.1. De krever tokenet som `Authorization: Bearer`, slik ruten `commands/workbench` gjør. De eldre rutene tar tokenet i adressen; nye ruter skal ikke det, for da havner det i logger.

| Rute | Inn | Ut |
|---|---|---|
| `GET /scheduled-jobs` | ingenting | `haven.scheduled-jobs-status.v1` (`scheduled-jobs-status-v1.schema.json`, eksempel i `fixtures/status.example.json`) |
| `POST /scheduled-jobs/control` | `{"id": "<id>", "command": "pause" \| "resume" \| "stop"}` | Den nye tilstanden for jobben, i samme form som ett element i statuslista |

`POST` skriver `<id>.control.json` gjennom `ScheduledJobControlService.set`, samme funksjon som MCP-verktøyene og kommandolinjen bruker (`trinn4-jobber-og-godkjenning.md`, avsnittet om styring). Den godkjenner ingenting og kvitterer ingenting. `resume` på en jobb som aldri ble godkjent, lar den stå og vente. `stop` gjelder bare jobber som er bedt om, og kan ikke gjøres om. En fast hendelse kan settes på pause og startes igjen herfra; `stop` på en fast hendelse svarer 409.

Svarkoder: 401 uten gyldig token, 404 for ukjent id, 409 når kommandoen ikke gir mening i tilstanden jobben har (for eksempel `resume` på en stoppet jobb), 503 når tilstandsmappen ikke kan leses.

## Statuslista

- Lista har både de faste hendelsene fra `config.json` (`origin: config`) og jobbene fra `State/ScheduledJobs/` (`origin: requested`).
- `worker.state` er `running` når livstegnet er ferskere enn 180 sekunder, `stopped` når det er eldre, og `unknown` når `worker.json` mangler eller ikke kan leses.
- `readable: false` betyr at tilstanden ikke kunne leses. Da er `items` tom, og `unreadableReason` sier hvorfor. Menyen skal vise det som en feil, ikke som «ingen jobber».
- `when` og `action` er klartekst agenten har laget. Ingen stier til programmer, ingen argumenter, ingen sjekksummer.
- For en fast hendelse skriver `pause` og `resume` styringsfila under hendelsens id. Arbeideren følger den. `status` i `State/scheduled-events.json` får ingen nye verdier (se `trinn3-cron.md`).
- En fast hendelse som er stoppet med kommandoen `schedule-stop` fra før, står som `stopped` i lista. `resume` setter den i gang igjen: arbeideren setter `status` tilbake til `scheduled` med neste tidspunkt.
- Tittelen for en fast hendelse er `title` i `config.json`. Uten den vises id-en.

## Menylinjen (AP13)

Menyappen får en linje «Planlagte jobber» med en undermeny, slik bildene i `../images/` viser. Den leser `GET /scheduled-jobs` sammen med innboksen, hvert 20. sekund som i dag. Undermenyen per jobb viser siste utfall, neste tidspunkt, antall passerte tidspunkt og opphavet («Fast program · godkjent i policyen» eller «Bedt om av Claude · godkjent 12.10.»). Knappene er «Sett på pause» eller «Fortsett». En jobb som er bedt om, har også «Stopp». «Sett alle på pause» nederst setter hver hendelse og jobb på pause, én for én, gjennom samme rute. «Fortsett» henter ikke inn pausen: første kjøring er neste planlagte tidspunkt. Unntaket er en fast hendelse på intervall uten cron, som korrespondansesjekken: den har ikke noe rutenett og kjøres straks etter «Fortsett». Pausen telles ikke som passering i noen av tilfellene (`trinn4-jobber-og-godkjenning.md`, under styringen).

Pause og fortsett for faste hendelser står bare her, og på kommandolinjen. Sakene om faste hendelser har «Kvitter» og «Åpne», som i trinn 4.

Samtidig får sakene fra korrespondansevakten riktige titler. Når `markedBy` er `agent-korrespondansesjekk` eller `agent-korrespondansefrist`, lager agenten tittelen fra markørtypen: «Ulest post fra Vegar», «Korrespondansesjekken får ikke lest kjetil-vegar-d», «Tilgangen for kjetil-vegar-d går ut 30.10.». Markører fra Losen selv beholder «Post fra … venter på svar».

En eldre menyapp kjenner ikke ruten og viser ikke linjen. Sakene fra trinn 4 viser den uansett.
