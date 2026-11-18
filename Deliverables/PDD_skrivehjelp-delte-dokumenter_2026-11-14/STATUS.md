# STATUS — skrivehjelp delte dokumenter

- surfaces: binding, cell, gui, scaffold, skeleton, web
- tags: ai-gateway, collaboration, shared-document, writing

## Porter
- G1: godkjent 2026-11-15 (Kjetil: «G1 ok, følg anbefalingene», 02.08 Oslo)
- G1-GUI: godkjent 2026-11-18 (Kjetil: «G21-GUI G2 godkjent. Trenger paritet med Binding.», bilder v2)
- G2: godkjent 2026-11-18 (samme melding), med krav om paritet med Binding
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-11-18: Kjetil krever paritet med Binding. WP6b lagt til: dokumentchat og dokumentteksten (lesevisning) som vanlige skeleton-elementer, så alt utenom redigering i editoren virker i Binding. Om full native editor skal med, er spurt med beslutningskort 18.11.
- 2026-11-15: Panelet blir skeleton-elementer i stedet for egen web-kode, fordi Kjetil valgte at det skal virke i Binding nå (§6 spm. 3a). Bildene rendres på nytt fra skeleton-JSON.

## Logg
- 2026-11-14: opprettet
- 2026-11-14: iterasjon 1 av FORMAALSSPEC og 7 bilder; G1 og G1-GUI bedt om. Venter også på svar på §6 (modellrute, deling, Binding, påslag).
- 2026-11-15: G1 godkjent med anbefalingene i §6. Planbytte for GUI: panelet bygges av vanlige skeleton-elementer (§6 spm. 3a), så bildene v1 (tegnet HTML-panel) erstattes av v2 rendret fra panelets skeleton-JSON. G1-GUI bes om på v2.
- 2026-11-15: bilder v2 rendret fra skeleton-JSON, PLAN.md skrevet. G1-GUI og G2 bedt om.
- 2026-11-18: G1-GUI og G2 godkjent. Implementering startet.
