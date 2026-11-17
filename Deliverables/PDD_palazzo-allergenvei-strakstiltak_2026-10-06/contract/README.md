# Kontrakt — det tiltaket endrer i svaret fra gjestens side

Stier er relative til HAVEN-roten. `PS` står for `PalazzoScaffold`, `HD` for `HAVEN-Deploy/_handoff/HD-0077`.
Kontrakten er `haven.palazzo.communale.guest-concierge.v1`, svaret fra `POST /palazzo/api/ask`, `POST /palazzo/api/menu` og `POST /palazzo/api/beverages`. Den har 13 felt, og tiltaket legger ikke til eller tar bort noe felt. Ingen celle endres, og ingen keypath er ny.

## Ny verdi: `reason_code: allergy-referral`

Henvisningen. Den gis når spørsmålet har et ord fra listen (regel 1), og når oppslaget svarer med en merking (regel 2).

| Felt | Verdi |
|---|---|
| `schema` | `haven.palazzo.communale.guest-concierge.v1` |
| `status` | `requires-review` |
| `answer` | «Dette er ikke bekreftet i kunnskapsgrunnlaget. Jeg kan ikke gi et sikkert svar. Spør vertskapet, særlig om allergener, krysskontakt, åpningstider eller dagens tilgjengelighet.» |
| `citations` | tom liste |
| `citation_count` | `0` |
| `citation_summary` | «Ingen publiserbare kilder i dette svaret.» |
| `last_verified` | tom streng |
| `confidence` | `blocked` |
| `audience` | `guest` |
| `needs_human_review` | `true` |
| `warnings` | «Dette må bekreftes av personalet før svaret kan brukes. Ved alvorlig allergi eller krysskontakt må kjøkkenet alltid bekrefte før bestilling.», «Svaret bygger på et datert kunnskapsgrunnlag. Dagens meny, priser og tilgjengelighet må bekreftes av Palazzo.» |
| `route` | `native` |
| `reason_code` | `allergy-referral` |

Hele konvolutten står i `konvolutt-henvisning-20261006.json` ved siden av denne filen; testen T1 krever nettopp den. HTTP-koden er 200, også når kunnskapsgrunnlaget ikke lot seg laste eller tilgangen til det ble avvist: regel 1 står foran alt som spør oppslaget (før svarte tjenesten 503 og 403 da; lest i koden, ikke prøvd). Teksten og de to advarslene er avvisningens, uendret (`PS/Sources/App/Controllers/PalazzoCommunaleProjection.swift`, linje 11 og 58–62 på `a3fc5042`). Forskjellen fra en avvisning fra oppslaget er grunnkoden, og at henvisningen aldri har kilder.

Verdiene `reason_code` hadde fra før, står: `answered`, `requires-human-review`, `unverified-source`, `requires-norwegian-review`, `invalid-response`, `native-unavailable`.

## Ny linje først i `warnings` på publiserte svar

Gjelder svar med `status: answered` der ingen advarsel har ordet allergi eller allergen. Feltet `answer` endres ikke.

| Svarform | Linjen |
|---|---|
| Beskrivelsen av én rett | «Beskrivelsen er ikke en ingrediensliste. Spør personalet om allergener før du bestiller.» |
| Beskrivelsen av to eller tre retter | «Beskrivelsene er ikke ingredienslister. Spør personalet om allergener før du bestiller.» |
| Pizzalisten, drikkelisten, svaret om bordbestilling | «Spør personalet om allergener før du bestiller.» |
| Rettlisten | ingen ny; den har «Ved alvorlig allergi eller krysskontakt må personalet bekrefte før bestilling.» fra før |

Feilsvar (HTTP 4xx og 5xx, og svaret «Concierge er midlertidig utilgjengelig») får ingen linje.

## Det som ikke lenger forekommer

Et svar med « er merket med: » i `answer`. Kommer merkingen tilbake, er det med den nye allergenveien (F8).

## Loggen

Én linje per svar, som før: `concierge-formulering handling=<ask|menu|beverages> utfall=<kode>`. To nye koder:

| Kode | Når |
|---|---|
| `allergi-henvisning:ordliste` | Regel 1: spørsmålet hadde et ord fra listen. Oppslaget og modellen ble ikke kalt |
| `allergi-henvisning:merking` | Regel 2: oppslaget svarte med en merking. Modellen ble ikke kalt |

Linjen har aldri spørsmålet, og heller ikke ordet som traff.

## Den som leser kontrakten

Sidens skript (`PS/Public/js/palazzo-communale.js`) leser `status`, `answer`, `warnings`, `citations`, `needs_human_review`, `last_verified` og `confidence`. Det leser ikke `reason_code`. Utsettingens kontroll (`HD/mac/KJOR-4-test-utenfra.sh`) leser `status`, `needs_human_review`, `citation_count` og `answer` for «Hvilke pizzaer har dere?». Ingen av dem krever noe om `warnings`.
