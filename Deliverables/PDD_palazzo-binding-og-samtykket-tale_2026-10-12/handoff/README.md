# Handoff

G1 godkjent; G1-GUI og G2 venter. Ingen produktkode er endret i denne runden. Les PLAN, contract/meeting-v1.md, SOURCE-REVIEW og STATUS før implementering. Bevar eksisterende dirty arbeidstrær.

Design reproduseres med `python3 generate.py` fra denne mappen. Det overskriver bare egne syntetiske skeleton-fixtures og states.json. Renderer-assets er låst med hash i assets/provenance.json. Lokal server: `python3 -m http.server 8766 --bind 127.0.0.1`; åpne preview.html?state=<id> i nettleser. Skjermbilder tas ved 1280×900 og 390×844 via støttet nettleserverktøy. Ingen mikrofon eller ekstern tjeneste kalles. Offline bildelesing: åpne index.html direkte.

Knappemålingene gjelder callback fra renderer, ikke produktets autorisasjon eller funksjon. Første prøve hadde sirkulært metadataobjekt i loggeren; dette ble rettet ved bare å lagre meta.trigger og hele render-/handlingsrunden ble kjørt på nytt. Kanonisk resultat er render-evidence.json; ingen null-logg tolkes som bestått.

Ingen deploy-/mutasjonsskript leveres før målmiljø, scope og kandidat er konkrete. Slike skript må få dry-run som standard, idempotens og eksplisitt apply. Gate-/valideringsverktøyenes kjente kanoniske feil må omtales separat fra oppgavens egne tester.
