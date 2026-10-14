# Uavhengig statisk review

Reviewer: heldout_dialogue_cases, 2026-10-14, 3 min 18 sek. Ingen implementeringsfiler eller blindsett endret av reviewer. Ingen runtime-test utført av reviewer.

Funn fulgt opp i kandidaten:
- Nummererte definisjoner må også passere admission, ikke bare få scoreøkning.
- Negasjon må gjelde handlingen; «ingen begrensninger» fritar ikke en positiv handling.
- Norsk preposisjon «i» er ikke engelsk førsteperson.
- Alle modell-eide påstandsfelt må kontrolleres, inkludert purposeCandidates og partyLedger.
- Eksplisitt tilbakeviste sitater trenger positiv kontroll.
- Skjemaunntak må gjelde eksakte stier; ukjente felter fjernes også i nested records.
- Original råtekst må ikke omgå validerte data; bare renset JSON publiseres.

Valideringen er strukturell og dekker gjenkjennelige myndighetspåstander, ikke alle mulige semantiske omskrivninger. Bygg, scope/reload/sletting og faktisk Qwen-kjede må verifiseres separat.
