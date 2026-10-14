# STATUS — palazzo rollesimulering

- surfaces: cell, scaffold, python
- tags: formaal, palazzo, roller, test, tilgang

## Porter
- G1: godkjent 2026-09-09        (formålsspesifikasjon godkjent av Kjetil)
- G1-GUI: ikke relevant        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: venter        (PLAN.md skrevet 2026-09-09; WP1–WP9 levert, WP10 venter på Kjetil, WP11 ikke startet)        (plan godkjent; arbeidspakker 1:1 mot bladformål)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-08: opprettet
- 2026-09-09: WP8 utvidet: generator som utleder agentrollen fra en tillitspakke, demonstrert mot WebFetch-fixturen. Stier i PLAN.md rettet til repo-relative etter Kjetils regel; egen kø-jobb `repo-path-konvensjon-20260909` for konvensjonen på tvers.
- 2026-09-09: **G1 godkjent av Kjetil.** PLAN.md skrevet. WP1–WP9 levert i PalazzoScaffold/Tests/Roles (5 rollefiler, 26 formål, aktør, fixture, selftest 8/8 grønn). WP10 (første ekte kjøring, før Sicilia G7) venter på kjørende server.
- 2026-09-09: iterasjon 3 — Kjetil svarte på tre av spørsmålene i §6: fem roller (agent med nå), kjøring før Sicilia G7, personale-kalibrering via staff/brief. Venter fortsatt G1.
- 2026-09-09: iterasjon 2 — §2b kalibrering av aktøren lagt til (positiv/null-referanse, nullkjøring, ikke-evaluert-er-ikke-oppnådd, forhåndsregistrert referanse for modellvarianten). Fortsatt G1: venter.
- 2026-09-15: Kjetil: de fire rollene er riktig sett. Prinsipp: roller er en label på hvilke tilganger man skal ha — ikke autoritative; cellene er. Rolledefinisjonen kan brukes til skript/funksjonalitet som hjelper brukeren å få riktige tilganger. Historien til Andre (familiefølelsen fra fire perspektiver): PalazzoComunaleScaffold/docs/Historie_Familien_Palazzo_2026-09-15.html + artifact.
