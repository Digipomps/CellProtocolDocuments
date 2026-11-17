# Referansebilder — G1-GUI, invitasjon → samtale

**Disse er mockups, ikke Porthole-preview.** Avsendersiden og «mottaker med HAVEN» bor i Binding
(Swift-fabrikker og skeleton), som ikke har en preview-loop for disse flatene. «Mottaker uten HAVEN»
er scaffoldets egen HTML (`VaporInviteLanding` / Leaf), ikke skeleton i det hele tatt. Bildene er
rendret fra én HTML-fil (`mockup/invite.html`) med Chromium i 390 pt bredde, 2× oppløsning, for å
avstemme forventningen før kode. De er akseptansereferanse for `test.gui.parity` ved P5.

Rendret 2026-09-24. G1-GUI godkjent av Kjetil 24.09 på v1-bildene; v2 av avsender-forhåndsvisningen kom til etterpå og venter for seg. Alle personer og adresser i bildene er oppdiktede (Vegar H., Anne B., Ola R.,
Kari S., `vegar…@…no`); ingenting kommer fra bokprosjektimporten.

## Bildene

| Fil | Flate | Tilstand | Formål |
|---|---|---|---|
| `stripe-avsender-v1.png` | Avsender, hele stripen | Butler-forslag → se før du sender → sendt → oversikt → samtale | Q, B, E, G, H |
| `stripe-mottaker-uten-v1.png` | Mottaker uten HAVEN, hele stripen | Lenke → hva som holdes om meg → ja/ikke nå/aldri → samtale i nettleser → ta det med deg | Q, F, G, N, P |
| `stripe-mottaker-med-v1.png` | Mottaker med HAVEN, hele stripen | Invitasjon i app → hva som holdes om meg → ja/ikke nå/aldri → samtale | Q, B, G, H, M |
| `avsender-forhandsvisning-v1.png` | Avsender | Rute 2: velg person, se hva jeg holder, se hva som sendes — **godkjent 24.09** | D, G |
| `avsender-forhandsvisning-v2.png` | Avsender | Rute 2 med skuffen «Private notater — sendes ikke» (formål R, lagt til etter G1-GUI) — venter | D, G, R |
| `avsender-oversikt-v1.png` | Avsender | Rute 4: sendt, besvart, utløpt — «besvart — ikke nå» uten skille | E, §6.5 |
| `mottaker-uten-haven-v1.png` | Mottaker uten HAVEN | Rute 2: feltene som faktisk holdes, med opphav | C, G |
| `mottaker-med-haven-v1.png` | Mottaker med HAVEN | Rute 2: samme felter, pluss «sier du ja» | C, G, M |
| `avslag-uten-konto-v1.png` | Mottaker uten HAVEN | Rute 3: ja / ikke nå / aldri — uten konto | F, E |
| `hjelpechat-mottaker-v1.png` | Mottaker uten HAVEN | Hjelpen svarer på tre spørsmål, og sier hva den ikke kan | I |
| `flytt-hjem-v1.png` | Mottaker uten HAVEN | Rute 5: midlertidig entitet tar med seg det som er sitt | P |

## Det bildene bestemmer — og som du godkjenner ved å godkjenne dem

Bildene tar noen valg som ikke står ordrett i FORMAALSSPEC. Godkjennes bildene, gjelder disse:

1. **Avsender får ikke vite at mottaker har åpnet.** Rute 1 hos mottaker sier «Kjetil får ikke beskjed
   om at du åpnet — bare hvis du svarer». Dagens `HavenInviteLifecycle` har en `opened`-tilstand som
   landingssiden setter. Bildet betyr at `opened` ikke vises for avsender (oversikten viser «Ikke
   besvart» til det kommer et svar). Det er en innsnevring av dagens oppførsel.
2. **Mottakeren ser nøyaktig feltene, med opphav og datoen for notatet** («En liste han la inn
   12. sep.»), og kan be om retting/sletting *før* svar og *uansett* svar. Det er formål C og G
   gjort synlig — og det betyr at kravflyten må virke uten konto.
3. **Tre svar, ett primærvalg.** «Ja» er primær; «Ikke nå» og «Aldri» er sidestilte sekundære med
   samme vekt, ikke en liten lenke. Nei skal være like lett som ja (konsept 5).
4. **«Hvem ser dette»-linjen står nederst på hvert bilde utenom selve samtalen**, der banneret
   øverst sier det samme. Én linje, alltid samme sted, alltid samme form.
5. **Samtalen i nettleseren tilbyr flytting én gang, som et kort under meldingene — ikke som en
   sperre.** Nykommeren kan bruke samtalen uten app så lenge de vil.
6. **Ved flytting forblir avsenderens notater avsenderens** (mottaker får en kopi); samtalen og
   kontakten flyttes. Det som ligger igjen er en peker. Dette er tolkningen av formål P.
8. **Private notater vises som en stiplet skuff merket «sendes ikke»** (v2). Mottakerbildene nevner den ikke, med vilje: mottakeren skal ikke få vite at den finnes (formål R, Kjetils valg 24.09).
7. **Ingen ord fra `ORDLISTE.md` forekommer i bildene.** «Tjenesten Kjetil bruker» står der
   scaffold ville stått; «det som er ditt» der entitetsdata ville stått.

## Dette kan dagens skeleton rendre (Binding-siden)

Kort, felt-rader, knapper, skillelinjer, lister, merkelapper, fargede meldingsbokser og
seksjonsoverskrifter — `VStack`/`HStack`, `Text`, `Button`, `Divider`, `List`, med modifierne
`background`, `cornerRadius`, `borderColor`, `foregroundColor`, `fontSize`, `fontWeight`, `padding`.
Chat-boblene finnes allerede i ChatCell sin presentasjon.

## RENDERINGSERKLÆRING

Bildene er mockups. Derfor står det her hva som **ikke** kan rendres slik bildene viser det. Listen
bygger på `SKELETON_UTVIDELSESFORSLAG_2026-09-15.md` (kildeverifisert 15.09) og er ikke sjekket på
nytt mot kode i dag.

1. **Knappehierarkiet (primær / sekundær / tertiær).** `styleRole` er i dag bare en
   `accessibilityIdentifier` (forslag F6). Primær kan gjøres med `background` + `foregroundColor`;
   den tertiære «lenke-knappen» (Ikke nå, Trekk tilbake, La det ligge) blir en vanlig knapp uten
   bakgrunn — nær nok, men ikke identisk.
2. **Felt-rader med høyrejustert verdi og en kildelinje under** (rute 2 hos alle). Det er `HStack`
   med to `Text` og en tredje under; høyrejusteringen krever `Spacer`/fast bredde og kan brytes ved
   lange verdier. Ingen `Table` finnes; forslag F1 (kolonner på List) ville gjort dette rent.
3. **Kursiv i hilsenen.** `fontStyle` går til de semantiske Font-rollene; egen kursiv finnes ikke
   som modifier (jf. F2 `fontDesign`). Hilsenen blir vanlig skrift i anførselstegn.
4. **«Hvem ser dette»-linjen med øye-ikon.** Ikonet forutsetter et `Image`/symbol-element med
   SF Symbol; er det ikke i dagens skeleton, blir det tekst i en avrundet boks — meningen holder.
5. **Stripene selv** er ikke en flate; de er fem bilder ved siden av hverandre. Ingen flate viser
   trinnene som en stripe.
6. **Mottaker uten HAVEN** er scaffold-HTML og kan rendres nøyaktig som vist — der gjelder ingen
   skeleton-grense. Hjelpechatten på den siden finnes ikke i dag (§0.2: unavailable) og er den
   største enkeltleveransen bak bildene.
7. **Rute 5 «Ta det med deg»** forutsetter flytting av entitetsdata mellom scaffolds, som ikke
   finnes (formål P, §2). Bildet viser hva som skal lages, ikke noe som kan rendres i dag.

## Kilde

`mockup/invite.html` + `mockup/render.py` (Playwright/Chromium). Endre HTML, kjør `python3 render.py`,
og bildene i denne mappen skrives på nytt med samme navn.
