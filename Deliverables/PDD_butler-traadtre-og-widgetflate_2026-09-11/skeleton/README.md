# skeleton/ — skjelett-JSON bak referansebildene

Tomt ved G1-GUI (2026-09-12) med vilje: referansebildene i `../images/` er rendret fra Kjetils HTML-mockup, ikke fra Porthole, så det finnes ingen skjelett-JSON bak dem (`pkg.std.gui-surface` krever `skeleton/` «når Porthole-preview er brukt»; `../FORMAALSSPEC.md` §3 sier eksplisitt at bildene er mockups).

Fylles i to steg:
- kandidater med dagens format fra WP-K1 lander i `../skjelett/<del>.candidate.skeleton.json` (navnet valgt i Codex-jobbene `skjelett-gap-*-20260912`);
- endelige skjeletter som Porthole faktisk har rendret (WP-K3, iterasjon mot staging) lander her som `<del>.skeleton.json`, med tilhørende `../images/<del>-<flate>-<tilstand>-v<n>.png` fra Porthole.
