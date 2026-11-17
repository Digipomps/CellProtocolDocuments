# Jobber som er klare for køen, men bevisst ikke lagt inn

Legges i `_losen-queue/inbox/` (begge filene, samme id) når forutsetningen under er oppfylt.

## visionos-h1-compile-probe

**Venter på:** Kjetils ja (§6 spørsmål 2 i `FORMAALSSPEC.md`). Han ba om fot i bakken før
implementering; en byggeprobe endrer ingenting i hovedtrærne (ren `git archive`-eksport i
`_h1-visionos-probe-<dato>/`), men opptar Mac-en i noen minutter og krever at visionOS-SDK er
installert i Xcode. Skriptet svarer selv `blocked` hvis SDK-en mangler.

**Måler:** hypotese H1 i `ANALYSE.md` §3 — «CellBase, CellApple og Binding kompilerer for xros
etter få, lokale rettelser». Resultatet er feil per fil, med macOS-baseline fra samme eksport
slik at et rødt HEAD ikke forveksles med visionOS-feil.
