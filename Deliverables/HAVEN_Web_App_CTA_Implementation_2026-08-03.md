# HAVEN webapp-CTA: implementerings- og beslutningslogg

Dato: 2026-08-03  
Oppgaveeier: Kjetil  
Status: review publisert; produksjonslenke til app blokkert

## Formål

- `purposeRef`: `purpose://gui.quality.functional-accessible`
- Related purpose: `purpose://human-agency`
- Intensjon: gi besøkende kortest mulig ærlige vei fra informasjonssiden til
  en offentlig HAVEN-app som faktisk kan åpnes eller installeres.
- Mål: `digipomps.org` viser nøyaktig én modenhetsriktig app-CTA på en
  verifisert produksjons-origin, uten ny fane og uten å fortrenge muligheten
  til å forstå HAVEN.
- Ferdig betyr: URL, modenhet, HTTPS, installasjonsflate og synlig brukerreise
  er kontrollert; CTA-en er aktivert fra ett konstantpunkt; tastatur, fokus,
  mobil og 200 % tekstzoom er kontrollert.

## Briefgransking

Briefen er ikke autoritativ. Statusene under er kontrollert 2026-08-03.

| Faktum | Revisjonsstatus | Grunnlag |
| --- | --- | --- |
| Informasjonsnettstedets produksjonsflate er `https://digipomps.org/`. | `retrieved` | `Website/DEPLOYMENT_STATUS.md`, DNS og HTTP 200 |
| Handoff-dokumentet oppgir ingen kanonisk produksjons-URL for appen. | `retrieved` | `CellScaffold/Documentation/HAVEN_Web_App_Install_Handoff_2026-08-03.md` |
| `haven.digipomps.org`, `app.haven.digipomps.org` og `app.digipomps.org` løser ikke i DNS. | `retrieved` | offentlig DNS-oppslag 2026-08-03 |
| `https://staging.haven.digipomps.org/` er den dokumenterte CellScaffold-flaten. | `retrieved` | `CellScaffold/README.md`, deploykonfigurasjon, DNS og HTTP 200 |
| Staging er ikke en gyldig installasjonsflate nå. | `retrieved` | `/install` gir 404; manifestet har tomt `name`/`short_name`; 192-, 512- og Apple-ikon gir 404 |
| Informasjonsnettstedet kan ikke utløse installasjon for en annen origin. | `retrieved` | plattformkildene og arkitekturgrensen i handoffen |

## Påstandsledger

| ID | Påstand | Type | Status |
| --- | --- | --- | --- |
| C1 | En offentlig app-CTA kan aktiveres nå. | `project_capability` | `blocked`: ingen dokumentert produksjons-URL eller installasjonsflate |
| C2 | Staging kan brukes som mål i mellomtiden. | `normative` | `contradicted`: oppgaven forbyr staging, og flaten er ikke installerbar |
| C3 | Aktivering fra ett konfigurert punkt reduserer risikoen for utdaterte eller sprikende lenker. | `causal` | `supported` som lokalt designvalg; må nettlesertestes |
| C4 | Heroen bør ha maks to handlinger. | `normative` | `supported`: aktiv app-CTA blir primær, «Forstå HAVEN» sekundær; testbeviset finnes allerede i neste seksjon |

## Valgt sikker implementasjon mens C1 er blokkert

1. Runtime-hentet JSON/JS er forkastet. Det ville gitt en ekstra nettverks- og
   JavaScript-avhengighet uten brukerverdi før en app-origin finnes.
2. Heroens ene aktiveringsblokk er merket `data-app-entry-state="blocked"`.
   Den beholder dagens to ærlige innganger og viser ingen skjult, deaktivert
   eller tom appknapp.
3. En read-only release-validator kontrollerer det statiske HTML-resultatet.
   Den avviser ukjent status, feil modenhetstekst, staging/lokal/review-host,
   ny fane og flere eller færre enn to hero-handlinger.
4. Når eier har dokumentert produksjonsflaten, legges en vanlig statisk lenke
   inn i den merkede blokken. App/demo blir primær og «Forstå HAVEN» sekundær.
   Testbeviset finnes allerede i neste seksjon.
5. Produksjonspublisering forblir blokkert til både app-origin og CTA-flyten er
   funksjonstestet.

## Beslutningslogg

- 2026-08-03: Ikke gjett produksjonsorigin.
- 2026-08-03: Ikke publiser staging som demo- eller installasjonsmål.
- 2026-08-03: Begge adjudikatorer avviste runtime-konfigurasjon som unødvendig
  kompleksitet og anbefalte statisk HTML uten JavaScript-avhengighet.
- 2026-08-03: Forbered ett markert, statisk aktiveringspunkt og en release-guard;
  behold nåværende offentlig hero til C1 kan dokumenteres.

## Åpent, med eier

- App-eier: oppgi og dokumenter kanonisk produksjons-origin og installasjonsside.
- App-eier: klassifiser flaten som offentlig app, offentlig demo eller
  hjemskjermklar demo.
- App-eier: lever appens manifest, ikoner, plattformflyt og fysiske enhetstester.
- Nettstedseier: aktiver og publiser CTA først etter vellykket ende-til-ende-test.

## Verifikasjon

- Offentlig DNS og HTTPS ble kontrollert 2026-08-03. Ingen produksjonsapp-origin
  ble funnet; `https://digipomps.org/` og testbeviset svarer HTTP 200.
- Den offentlige heroen viser fortsatt «Forstå HAVEN» og «Se et konkret
  testbevis» og ingen app-/installasjons-CTA.
- Det reviderte informasjonsstedet er publisert på den isolerte review-flaten
  `https://new.haven.digipomps.org/`, med egen docroot. Produksjonsflaten
  `https://digipomps.org/` er ikke endret.
- CSS, logo og heroillustrasjon svarer HTTP 200 på review-flaten og ble visuelt
  kontrollert i Chromium.
- Den statiske release-guarden passerer i blokkert tilstand.
- 8 enhetstester dekker blokkert tilstand, modenhetstekst, eksplisitt
  allowlist-origin, staging, preview/review, samme fane og maks to handlinger.
- Lokal Chromium-smoke passerer med JavaScript på og av, tilgjengelighetsnavn i
  nettleserens AX-tre, tastaturfokus, 200 % tekst og 390 px mobilbredde uten
  horisontal overflow.
- Ikke testet fordi app-CTA er blokkert: faktisk redirectmål, fysisk
  skjermleser, fysisk Android/iOS-installasjon og standalone-oppstart.
