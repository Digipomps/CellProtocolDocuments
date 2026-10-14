# Dommerbenken runde 2 — streng fasit (2026-09-15)

Bakgrunn: runde 1 (15 oppgaver, 197 svar, `dommer_2026-09-14_eksport.json`) ga «ja» på alle rader.
Med alle kandidater dømt relevante får kandidat 6 (tekst+perspektiv+skop) og kandidat 1 (TF-IDF)
samme R+@10 — fasiten skiller ikke, og motorvalget (WP4a) kan ikke avgjøres av den.
Kjetils valg i Valgbenken (v-dommer-2, alternativ a, 09:30Z): døm 5 oppgaver på nytt, strengt.

## Hva runde 2 er

- Samme artefakt (Dommerbenken, `BiCsaiwuLH6XhpyQXSq36c`), versjon 2. Runde 1 ligger urørt i samlingen `dommer`.
- Fem oppgaver — de der de to motorene er mest uenige om topp-10 (overlapp 4–6 av 10):
  `PDD_arbeidsko-ai-utforere_2026-09-07` (16 rader), `PDD_innholdsvern-lyd-20260909_2026-09-10` (16),
  `PDD_formaalsregister-som-graf_2026-09-11` (15), `PDD_haven-visionos_2026-09-10` (14),
  `PDD_palazzo-gjestebestilling_2026-09-03` (14). 75 rader totalt.
- Radene er unionen av k6- og k1-topp-10, i **fast tilfeldig rekkefølge** per oppgave (`rekkefolge` i
  `dommer_runde2_oppgaver.json`), så plasseringen røper ikke hvilken motor som rangerte høyt.
- «Nei» er standard. Bare to knapper: «Ville endret noe» (ja) og «Usikker». Et ja krever en begrunnelse
  («hva ville blitt annerledes») før oppgaven kan låses med «Ferdig — resten er nei».
- Kriteriet står øverst med forventning 0–3 ja per oppgave, og med forklaringen på hvorfor runde 1 ikke kunne skille.

## Hvor svarene havner

Artefaktets database, samling `dommer2`, ett dokument per oppgave:
`{oppgave, runde: 2, svar: {n: "ja"|"?"}, grunn: {n: tekst}, ferdig, notat, sekunder, rekkefolge, oppdatert}`.
Rader som ikke står i `svar` er nei. Bare oppgaver med `ferdig: true` inngår i fasiten.

## Slik leses den inn i målingen

1. Eksporter samlingen `dommer2` til `maaling/dommer_runde2_eksport.json` (Claude, `read_db`).
2. Positive par = (oppgave, ref) der `svar[n] == "ja"` og `ferdig` er true; `?` holdes utenfor (verken positiv eller negativ).
3. Kjør `maaling/evaluer.py` med denne fasiten mot kandidat 1 og kandidat 6 (samme k som før); rapporter R+@10 og MRR+ per kandidat og differansen med CI.
4. Er ja-andelen fortsatt > 50 % av radene, sier fasiten ingenting — da er alternativ b (blind parvis) neste.

Kilde for radene: `dommer_oppgaver.json` (runde 1) → `dommer_runde2_oppgaver.json` (utvalg + rekkefølge). Sidekilden: `dommerbenk_runde2.html`.
