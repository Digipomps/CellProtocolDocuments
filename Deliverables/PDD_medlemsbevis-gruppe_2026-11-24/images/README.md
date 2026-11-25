# G1-GUI-bilder — Signert medlemsbevis i en gruppeentitet

Rendret 2026-11-25 med den ekte web-rendereren i CellScaffold (`Public/js/skeleton-runtime.js`,
`porthole-webo.css`, `admin-skeleton.css`, CellScaffold `6e2f667`) via `skeleton/render.js`, samme
oppsett som i `PDD_informasjonssystemer-gruppeentitet`. Skjelett-JSON og tilstander ligger i `skeleton/`.
Bredder: laptop 1280, iPhone 390. Skriptet sjekker at forventet tekst finnes og at skjulte kort er skjult.

| Flate | Tilstand | Filer | Formål |
|---|---|---|---|
| Medlemsbevis (medlem) | velg vei: eID eller moderator | `medlem-velg-{laptop,iphone}-v1.png` | 2, 3, 6, 7 |
| Medlemsbevis | samtykke før eID: hva lagres og ikke | `medlem-samtykke-*` | 5a |
| Medlemsbevis | søknad venter på moderator | `medlem-venter-*` | 2 |
| Medlemsbevis | søknad avvist | `medlem-avvist-*` | 2 |
| Medlemsbevis | nummeret er allerede medlem → flytt (q2) | `medlem-allerede-*` | 3a |
| Medlemsbevis | godtatt, med vei og gyldighet; meld deg ut | `medlem-godtatt-*` | 1, 5 |
| Moderatorkø | to søknader, en flyttemelding, medlemsliste | `moderator-ko-*` | 2, 5 |
| Moderatorkø | ingen søknader | `moderator-tom-*` | 2 |
| Avstemming (eksempel) | én stemme per bevis, ett forsøk avvist | `avstemming-stemt-*` | 8 |

## Renderingserklæring — hva bildene ikke viser

- Alle keypaths under `membership.*`, `moderation.*` og `vote.*` er forslag. Ingen finnes i CellScaffold i dag.
- Binding (SwiftUI) er ikke rendret. Paritet mot Binding er en egen test (`test.gui.parity`).
- eID-innloggingen (ID-porten/test-IdP) og passkey-dialogen er systemflater og vises ikke.
- «Du kan ikke godta din egen søknad» vises bare på en rad der søkeren er moderatoren selv; ingen av radene i bildet er det.
- Statusfargen i en rad er én farge per kolonne; «meldte seg ut» kan ikke få egen farge uten en egen rad per tilstand.
- Navnene «Ola Student», «Kari Testesen», «Per Prøvesen» og «Testkonto 3» er fiktive testdata.
