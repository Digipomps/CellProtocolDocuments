# Rollesimulering — skjema og bruk

Hver rolle er én fil i `roles/`. En rolle er en **principal** og en liste
**formål**. Et formål er en handling mot den kjørende serveren, tilgangen den
forventer, og den observerbare tilstanden som ville bevise at formålet ble nådd.

```jsonc
{
  "role": "personale",
  "principal": "staff:{staff_id}",          // {navn} fylles av --env navn=verdi
  "purposes": [{
    "purposeRef": "purpose://candidate.…",
    "title": "Kelneren ser gjestens allergener når gjesten har delt dem",
    "calibration": "positive",              // eller "null" — se under
    "action": {"method": "POST", "path": "/api/staff/brief",
               "json": {"value": {"guestCell": "{consenting_guest_cell}"}}},
    "expect": {
      "access": "allowed",                  // eller "denied"
      "state": {"path": "value.shared#", "op": "gte", "value": 5}
    },
    "stop_is": "riktig",                    // valgfri forhåndsklassifisering
    "why": "…",                             // påkrevd når stop_is er satt
    "null_principal_may_reach": true        // se nullkjøringen
  }]
}
```

`state.path` er punktsti med `[i]` for indeks og `#` til slutt for lengde.
`op`: `eq`, `ne`, `gte`, `contains`, `each_eq`.

## Tre regler som ikke skal mykes opp

**Kalibrering først.** Hver rolle erklærer ett formål den *sikkert* kan nå
(`calibration: positive`) og ett den *sikkert* ikke kan (`calibration: null`).
Begge kjøres før alt annet. Kommer det sikre tilbake som stoppet, eller det
forbudte som oppnådd, er det aktøren som er i stykker — ikke systemet — og resten
av rapporten leses ikke. Et instrument som ikke er vist å skille de to utfallene,
produserer utfall uansett.

**Ikke evaluert er aldri oppnådd.** Et formål er OPPNÅDD bare når
tilstandssjekken faktisk kjørte og var sann. Tomt svar, manglende felt, timeout:
UKLASSIFISERT.

**Et stopp er riktig eller feil, aldri bare rødt.** Kjøringen klassifiserer
aldri et stopp selv. `stop_is` i rollefila er en menneskelig avgjørelse tatt på
forhånd; alt annet uventet blir UKLASSIFISERT og feiler kjøringen til noen har
skrevet hvilket det er.

## Nullkjøringen

`--null-principal guest:<fersk-id>` kjører hele listen på nytt med en gyldig
principal uten grants. Alt den når, som ikke er merket
`null_principal_may_reach`, er laget av harnessen eller ruten — ikke av verden.
Merkingen er for formål enhver principal lovlig kan nå: egen tilstand, og
offentlige flater som publisert innhold. Unntakene listes i rapporten, så de kan
etterprøves i stedet for å være stille.

## Kjøre

```bash
# mot en kjørende Palazzo
python3 run_roles.py --base-url http://127.0.0.1:8080 --token "$PALAZZO_GATEWAY_TOKEN" \
    --env guest_id=… other_guest_id=… staff_id=… agent_id=… \
          guest_cell=… consenting_guest_cell=… article_id=… agreement_id=… \
    --null-principal guest:$(uuidgen) --out RAPPORT_$(date +%F).md

# mot fixturen, som tester aktøren og ikke Palazzo
python3 selftest.py
```

Exit: 0 ren · 2 kalibrering feilet · 5 personvernlekkasje · 3 nullekkasje ·
4 uklassifiserte. Sjekkes i den rekkefølgen — etter alvorlighet, ikke tallverdi.

## Hva `selftest.py` er og ikke er

Åtte kjøringer mot `fixture_server.py`, én per måte en harness kan ta feil.
Grønn selftest sier **ingenting om Palazzo**. Den sier at instrumentet reagerer.
Det er halvparten som kan etableres uten et kjørende scaffold, og halvparten det
er verdiløst å oppdage sent.
