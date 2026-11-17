# Vektbenken som side

Siden Kjetil velger tallene på: https://claude.ai/artifact/839NLwdFpn8d3MwQBqgHhc

- `vektbenk.html`: kilden til siden. Formelen ligger i `model.js`, som er limt inn i siden.
- `verify.js`: kontrollerer `model.js` mot benkens rapport: `node verify.js ../vektbenk-v1.md`. 29.9 ga det 90 sett × 7 gjester, 630 av 630 like (tilbud, rekkefølge, summer til 1e-12, stengte artikler).
- Valget lagres i sidens database, i dokumentet `valg/gjeldende` (navn, tall, antall oppfylt, røde flagg, kommentar, tid). Losen leser det med ArtifactData og gir Codex WP6.
- Endres formelen i koden, må `model.js` rettes og `verify.js` kjøres mot en ny benkrapport før siden publiseres på nytt.
