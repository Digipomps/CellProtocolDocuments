# Plangraf — referansebilder (iterasjon 1, HTML-mockup)

Elleve tilstander, web (1900×1100) og app (780×1688) — 22 filer. Bygget som HTML/CSS og
skjermbildet med Playwright, **ikke** Porthole-rendret ekte skjelett. Hvert bilde har et
`MOCKUP`-vannmerke i hjørnet av samme grunn — dette er "slik det skal se ut", ikke bevis på at
komponentene finnes i dagens renderer. Det beviset bygges parallelt av Codex, se
`../evidence/plangraf-porthole/CAPABILITET_RAPPORT.md` når den jobben er ferdig.

Innholdet i kortene er ekte, gjenkjennelig data fra 14. sept. (HD-0069/HD-0072-status, denne
PDD-ens egen G1) — ikke oppdiktede tall — nettopp for at du skal kunne sjekke bildene mot noe du
selv vet er riktig.

## Bildene

| Fil (web / app) | Viser | Dekker successSignal |
|---|---|---|
| `plangraf-{web,app}-graf-fylt-v1.png` | To lanes, seks kort, statusfarger (good/pending/blocked/idea), avhengighetsmerke mellom kort | E1 |
| `plangraf-{web,app}-graf-tom-v1.png` | Tom linse med forklart fravær, ikke en tom flate uten grunn | E1 (`lesson.empty-list-must-not-look-like-calm`) |
| `plangraf-{web,app}-graf-kildefeil-v1.png` | Banner: utdatert kilde + motstridende status mellom PLAN og STATUS, ingen grønn boks konstrueres | E5 |
| `plangraf-{web,app}-drilldown-v1.png` | Åpnet kort: purposeRef, gjør, tester, artefakter, eier/utfører adskilt, kildehenvisning | E2 |
| `plangraf-{web,app}-utfor-for-v1.png` | Før trykk: mål, grant, når/hva/hvorfor-du/etterpå | E3 |
| `plangraf-{web,app}-utfor-kjorer-v1.png` | Startet med kjørings-ID, ikke levert ennå | E3 |
| `plangraf-{web,app}-utfor-etter-v1.png` | Levert med ekte artefaktbevis (gjenbruker dagens faktiske HD-0072-resultat: `exit=64`) | E3 |
| `plangraf-{web,app}-utfor-blokkert-v1.png` | Avvist med reell grunn (broen ikke bekreftet), ingen knapp later som den kjørte | E3 |
| `plangraf-{web,app}-forklaring-v1.png` | Forklaringspanel ved valgt punkt, med kildehenvisning | E4 |
| `plangraf-{web,app}-forklaring-feil-v1.png` | Forklarer utilgjengelig, med Prøv igjen | E4 |
| `plangraf-{web,app}-forklaring-festet-v1.png` | Festet forklaring, merket utdatert etter kildeendring | E4 |

## Elementkart — komponenter mockupen forutsetter

Dette er **ønskelisten** fra mockup-siden, ikke en bekreftet skjelett-kontrakt. Reell kartlegging
mot `SkeletonDescription.swift` gjøres av den parallelle Codex-jobben:

- **Lane** — navngitt rad med kort
- **Kort** — WP-ID, tittel, notat, statuschip (farge + tekst), utførerprikk, avhengighetslinje
- **Banner** — advarsel øverst i canvas (kildefeil/blokkert-tilstander)
- **Drilldown-panel** — sidepanel (web) / bunn-ark (app) med felt-liste (nøkkel/verdi)
- **Handlingspanel** — samme panelform, med knapperad og kjøringsstatus (spinner, levert, blokkert)
- **Forklaringspanel** — samme panelform, med festet-merke og utdatert-merke

Ingen av disse er bekreftet som `SkeletonElement`-case i dag. Se
`../contract/plangraf-renderer.md` for status når kapabilitetsrapporten er lest.
