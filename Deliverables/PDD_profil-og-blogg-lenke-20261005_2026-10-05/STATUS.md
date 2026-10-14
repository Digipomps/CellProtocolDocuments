# STATUS - profil- og blogglenke paa musikkflaten

2026-10-05 · punkt 1 av seks Kjetil godkjente rekkefoelgen paa

## Bestillingen (Kjetils ord, tidligere)
«Vi kan legge inn en mulighet for aa lenke til en profil/blogg flate. Den kan
legges til i admin omraadet og dukke opp som en knapp oeverst et sted. Admin maa
kunne bestemme om den er aapen for alle eller med Agreement.»

## Porter
- G1: dekket av at Kjetil godkjente rekkefoelgen og sa «gjoer det naa» 2026-10-05
- G1-GUI: **GODKJENT av Kjetil 2026-10-06** («Profil-lenken er godkjent») - `images/profil-lenke-v1.png`
- G2/G3: ikke egne porter; dette er lite nok til aa gaa rett paa

## Skrevet (gren `pdd/profil-og-blogg-lenke`, av `origin/main` @ e5c34345)
- `MusicProfileLinkAccess` (`everyone` | `agreement`) og `MusicArtistFeaturedLink`
  (label, url, access) i `MusicPublishingSupport.swift`
- `featuredLink` paa `MusicArtistProfileRecord`, med i `asObject`
- `updateProfile` setter og fjerner lenka; tomt eller uleselig = fjern
- grant `rw--` for `featuredLink`
- **`publicProfile` holder adressen tilbake naar `access == .agreement`** og
  setter `urlWithheld: true`. Den offentlige profilen leses av hvem som helst; en
  port som gir fra seg maalet er ingen port.

Modellen er generell - den ligger i artistprofilcellen, ikke i Butterpop-flaten.

## Ikke skrevet
- Flaten: knappen i `butterpop_studio.leaf` og visningen i
  `butterpop-studio.js`. Venter paa G1-GUI.
- **Samtykkeflaten for avtale-varianten finnes ikke.** Det er null treff paa
  agreement-haandtering i `butterpop-studio.js`. Modellen holder adressen
  tilbake, men det er ingen flate som ber om samtykket enda. Eget arbeid.

## Ikke kompilert
Ingen Swift-toolchain i denne oekta. Maa gjennom kjoereren som AP1.

## 2026-10-06
- Foerste kjoering i Losen-koeen stoppet paa literal-gaten foer noe ble kompilert:
  `/usr/local/bin/python3.12: Bad CPU type in executable`. Ikke en feil i denne
  koden. Gaten er fikset paa egen gren (`fix/literal-gate-python-maa-kunne-kjoeres`,
  `2876c814`).
- Literal-gaten er kjoert i Losens VM mot denne grenen: groenn.
- **Testen vil ikke kjoere i CI.** Den ligger i `MusicPublishingCellsTests`, og hele
  den suiten staar i `ci/test-exclusions.txt`. Lokal kjoering i koeen er eneste
  sted den kjoerer inntil suiten er tilbake i CI.
- Ny jobb i koeen: `01-musikk-bygg-og-test` - bygg, test, og negativ kontroll med
  krav om riktig feilmelding.

## 2026-10-06 kveld - flaten er skrevet. Hvert punkt sier hvordan det er kjent.

Gren `pdd/profil-og-blogg-lenke`, fem commits paa `e5c34345`, tupp `03caf4e7`.

| Hva | Hvordan det er kjent |
|---|---|
| Modellen holder adressen tilbake bak en avtale | **Sett**: `testFeaturedLinkWithholds…` kjoert paa Kjetils Mac 06.10 21:44 mot `c7f28a9d` - bestaar, og feiler med «Adressen skal ikke ligge i den offentlige profilen» naar fiksen tas bort |
| Adressevalidering, og at en avvist lenke ikke fjerner den gamle (`a5b1e5b4`) | **Ikke kompilert.** Skrevet etter Mac-kjoeringen. Ligger i jobb 02 |
| Rutene `GET/POST …/workspace/profile…` (`a3e924a2`) | **Ikke kompilert, og har ingen Swift-test.** Rutetestene bor i `ButterpopStudioProductTests`, som er utelatt fra CI |
| Knappen oeverst og Profil-fanen (`03caf4e7`) | **Sett**: Playwright 1.55.1 i Losens skycontainer mot byte-like filer (sha256 sammenlignet) - 17 nye proever og 22 eksisterende, 39 av 39. Skjermbilder sammenholdt med det godkjente bildet |
| At proevene faktisk fanger feil | **Sett**: uten adressesjekken feiler seks; uten `urlWithheld` feiler tre |
| At det virker mot en ekte server, staging eller Binding | **Ikke sjekket** |

### Avvik fra det godkjente bildet
- Kortet ligger under en ny fane «Profil» i Studio. Bildet viste bare kortet.
- Velger artisten «Bare med avtale», viser skjemaet en advarsel: ingen kan aapne
  lenka ennaa. Bildet hadde den opplysningen som en roed note nederst.
- Paa telefon brytes topplinja i to rader, og seks faner legges tre og tre.

### Endringer som ikke sto i bestillingen
- Bare interne stier og https godtas som adresse. `javascript:` med flere avvises.
- `butterpop-statistics.spec.js` er oppdatert: eieren har seks faner, ikke fem.

### Neste
Jobb `02-profil-lenke-push-og-pr` i Losen-koeen: bygger og tester tuppen med negativ
kontroll, og pusher + aapner PR bare hvis det gaar gjennom.

## 2026-10-06 sent - gjennomgang foer push. Tre ting rettet, og tuppen er ny.

Tupp `4d382ee1` (seks commits paa `e5c34345`).

- **Playwright-proevene for lenka sto ikke i CI.** `butterpop-featured-link.spec.js`
  var verken i workflowen eller i `package.json`. Lagt i samme liste som
  `butterpop-queue` og `butterpop-mix-tidy` (`4d382ee1`). **Sett**: 39 av 39 med adressen
  CI bruker (`http://127.0.0.1:9089`), Playwright 1.55.1, filene sammenlignet med
  tuppen paa sha256.
- **`butterpop-statistics.spec.js` kjoeres i CI** (`npm run test:butterpop-statistics`),
  saa endringen fra fem til seks faner var noedvendig, ikke bare lokal.
- **Jobb 02 er endret etter at den ble armert**: fullt refspec paa push (det gamle
  kallet kunne havne paa `main` med et uvanlig git-oppsett - proevd i sandkasse), og en
  GNU-spesifikk `grep` i sluttsjekken er byttet ut.
- De tre siste Swift-commitene er fortsatt **ikke kompilert**. **Sett**: syntakssjekk
  med tree-sitter-swift ga ingen feilnoder i linjene grenen har lagt til. Det er ikke
  kompilatoren.
- **Rutene har fortsatt ingen Swift-test.** `MusicUsageStatisticsTests` kjoerer i CI og
  har moensteret (hel app, innlogget bruker, `app.test`). Ikke skrevet.
