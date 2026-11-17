STATUS: KLAR TIL Å STARTE — venter på Kjetils ja til WP-S (CellProtocol #46)

# A3 og A4 — det som gjenstår etter WP-S

A3 (synlig onboarding-modus) og A4 (hemmelig nøkkelfelt) bygger på de nye skjelettfeltene. De kan ikke
leveres før `placeholderKeypath`/`secureKeypath` finnes i CellProtocol main og CellScaffold peker på den
versjonen. Kjetils regel: CellProtocol main først når han har sett testene (PR #46, utkast).

## Når #46 er godkjent

1. CellProtocol #46 → main. CellScaffold: pin-bump til den commiten + web-runtime-PR #256.
2. **A4, hub-tilstand** (`PersonalCopilotCloudStore.chatState`): projiser fra GuidedOnboarding-økten til
   `chatHub.state.composer.placeholder` (stegets `promptTemplate`) og `chatHub.state.composer.secret`
   (`step.isSecret`). Ingen nøkkelverdi i tilstanden, bare flagget.
3. **A3, Butler-konfigurasjonen** (`PersonalCopilotConfigurationFactory`, komponisten ved linje ~1696):
   `placeholderKeypath: "chatHub.state.composer.placeholder"`, `secureKeypath: "chatHub.state.composer.secret"`,
   og en stripe over skrivefeltet med synlighetsregel på `chatHub.state.onboarding.active`:
   «Onboarding pågår · <tittel> · steg x av n · Avbryt onboarding» (som `images/butler-onboarding-steg-v1.png`).
4. **Svaret går til onboardingen, ikke chatten**: `chatHub.prompt.submit` sjekker aktiv økt og sender til
   `onboarding.answer`. Et hemmelig svar skrives aldri til transkriptet; der står bare «nøkkel lagret».
5. Tester: `test.onb.noekkel-aldri-i-logg` (nøkkelen finnes ikke i transkript, `state`, `get`-svar eller logg),
   `test.gui.parity` (web + native), Playwright-bilde mot G1-GUI-mockupene.

## A1 — årsaken til «GuidedOnboardingCell is not available»

- Sonde 2026-09-23 23:50Z (`handoff/A1-SONDE.md`): prods logg siste 14 t har **ingen** `owner_restore_failed`
  og ingen onboarding-linjer. Eierløs gjenoppretting er dermed lite sannsynlig som årsak.
- Leveranse 2 (A2) gir feilen en kode: `guided_onboarding_not_registered` (resolveren fant ikke cellen eller
  den er ikke Meddle), `…_denied` eller `…_step_rejected` (set kastet). Etter at A2 er i prod: ett klikk på
  «Koble til modell», så sier koden hvilken av de tre det er.
