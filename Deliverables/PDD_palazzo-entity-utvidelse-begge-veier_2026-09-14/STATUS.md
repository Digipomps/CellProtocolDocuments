# STATUS — palazzo entity utvidelse begge veier

- surfaces: bridge, cell, gui, scaffold
- tags: bridge, entitet, identitet, palazzo

## Porter
- G1: godkjent 2026-09-14 (Kjetil: svar Q1–Q5 + «ja til (a)+(b) og til bildene»; §6 i iterasjon 3 er Astras sju beslutninger med Losens anbefaling som default)
- G1-GUI: godkjent 2026-09-14 (Kjetil: «ja … til bildene» — v1; tekster rettet til v2 etter Astra-audit, samme layout/flyt; v2 legges fram for bekreftelse)
- G2: godkjent 2026-09-15        (Kjetils valg i Valgbenken v-entity-g2 2026-09-15 09:22Z: alternativ a «Godkjenn G2/plassering» (PalazzoLinkOffer i PalazzoScaffold først), merket utført; PLAN.md: WP-S1 → WP-L → WP-C → D1/D2/D3/D5 → WP-G → WP-R)
- G3: venter

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-09-14: opprettet fra Kjetils tekst om Identity/Entity-utvidelse. Iterasjon 1 av FORMAALSSPEC; Astra-analyse (lesende) lagt i _losen-queue som `pz3-entity-utvidelse-astra-20260914`.
- 2026-09-14 kveld: Kjetil svarte Q1–Q5 (1: Losens forslag; 2: begge tilbyr, den som først ser riktig tilstand; 3: opplevelsen — trygt, ett trykk, forståelig; 4: beviset like sikkert som/sikrere enn Vipps; 5: celle). FORMAALSSPEC iterasjon 2 skrevet; seks G1-GUI-bilder rendret i images/ (mockups). Nytt spørsmål Q4′ (hva «like sikkert som Vipps» skal bety) må besvares før G1. Astra-brief utvidet.
- 2026-09-14 sent: Astra-analyse levert (pz3, 19:19Z). Kjetil ja til (a)+(b) og bildene → G1/G1-GUI. Astra fant at tre tekster i v1-bildene var usanne (custodial nøkler bor på Palazzos server; koblingsmetadata utveksles og HAVEN får rettigheter; revoke sletter ikke) → v2-bilder rendret med rettede tekster. Fire sikkerhetsforhold i bro/IdentityLink registrert i HAVEN-Deploy (HD-0080, HD-0081). PLAN.md skrevet; HD-0079 registrert for PDD-en.
- 2026-09-15 08:50Z: **Kjetil (via Valgbenken v-entity-core), ordrett:** «Ja til WP-S1 og WP-L i CellProtocol på egen gren og PR, med bridge-provenance, replay, fresh-auth, custodial-compromise og revoke-tester». Registrert som oppfylt approval-need på HD-0079 (need 2), HD-0080 og HD-0081. Codex-jobb `pz-wp-s1-bridge-provenance-20260915` (WP-S1, CellProtocol, ny worktree `_worktrees/cellprotocol-bridge-provenance`, gren `pdd/bridge-provenance`) lagt i kø. WP-L (HD-0081) køes etter WP-S1 er levert. **G2 for planen (need 1 på HD-0079, v-entity-g2) er fortsatt Kjetils ord** — Palazzo-WP-ene (WP-C, WP-D*, WP-G) venter på den.
- 2026-09-15 09:30Z: **G2 godkjent** — Kjetils valg i Valgbenken v-entity-g2 2026-09-15 09:22Z: alternativ a «Godkjenn G2/plassering» (PalazzoLinkOffer i PalazzoScaffold først), merket utført. Begge approval-needs på HD-0079 er nå oppfylt (G2 + CellProtocol-endring). WP-S1 (HD-0080) kjører i Codex-køen; WP-L (HD-0081) køes etter WP-S1; WP-C (PalazzoLinkOffer) kan planlegges.
- 2026-09-15: WP-S1 / HD-0080 levert 5fa0b96e718c418e2a2e306fd6b4f809231bc093, ikke pushet, på `pdd/bridge-provenance` i `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/cellprotocol-bridge-provenance` (ren worktree); 3 nye tester, 13 totalt, ikke kjørt (sandbox stoppet bygg etter 1,80 s); parse av 2 filer OK (0,17 s). PR-tekst: `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/HD-0080/PR-bridge-provenance.md`. CellScaffold-pinnen må oppdateres ved egen beslutning; WP-L / HD-0081 gjenstår.
- 2026-09-15 09:50Z: WP-S1 levert av Codex som `5fa0b96` i `_worktrees/cellprotocol-bridge-provenance` (gren `pdd/bridge-provenance`): `identityVault(for:)` gir alltid `BridgeIdentityVault` for identitet over broen; ingen legitim sti trengte `shared` (lokal signering bruker egen tillatelse, BridgeBase.swift:1438). Tester 0/13 kjørt — sandkassen uten nett. Kjetil kjører `HAVEN-Deploy/_handoff/VERKTOY/KJOR-SELV-cellprotocol-test.sh cellprotocol-bridge-provenance HAVEN-Deploy/_handoff/HD-0080/evidence --filter VaporBridgeTransportTests --run`, deretter push + PR (hans). PR-tekst: `HAVEN-Deploy/_handoff/HD-0080/PR-bridge-provenance.md`. WP-L (HD-0081) køes når testene er grønne.
- 2026-09-15: HD-0080 testrettelse `f141c53b4245f80f1badefe3ec8bbe0cdb0075b0` på `pdd/bridge-provenance` (ren worktree, ikke pushet): Kjetils kjøring på `5fa0b96` ga bygg exit 0 og 13 tester / 2 feil, samme catch-assertion for `.get` og `.response`; testen fanger nå nøyaktig `ProvenancePeerError.noPrivateKey` både rått og innpakket i `CombineHelpers.AsyncError.other` (`Sources/CombineHelpers/Publisher+Async.swift:84`), uten produktendring. Forventet 13/0; nye tester **ikke kjørt**, runneren stoppet før teststart med `sandbox_apply: Operation not permitted` (exit 1); parse exit 0. Bevis: `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/HD-0080/PR-bridge-provenance.md`.
