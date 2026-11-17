# ACCEPT — ordklasseramme i Swift (for G3)

Oppgavemappe: `CellProtocolDocuments/Deliverables/PDD_ordklasseramme-swift_2026-10-13` · 14. oktober 2026 · Losen

Forventning (FORMAALSSPEC §3) mot det som faktisk finnes. Bevis i `TESTRESULT.md`.

| Leveranse | Forventet | Faktisk | Bevis |
|---|---|---|---|
| Swift-pakke `PurposeFrameMatcher` | kilde, tester, data på egen gren | 12 filer i `commons/purpose-frame-matcher`, commit `2033ab7a` på `losen/purpose-frame-matcher-20261013`, ikke pushet; bare Foundation, ingen avhengigheter | `WP1-FERDIG`, git i arbeidstreet |
| Paritet mot Python | ≥ 1 100 meldinger, samme topp 1 | 2 095 rader, samme topp 3 og svar, største scoreavvik 5e-10 | `#parity`, to uavhengige kjøringer |
| DEV5-kurven | 0.729 ved 0 %, 0.796 ved 10 % | identisk med Python ved alle fire terskler | `#curve` |
| Databunt og ordklassetabell | kilde og sha256 | byte-identiske med fasiten; UD-lisensen (CC BY-SA 4.0) i filhodet og README; sha256 sjekkes i test | `#bundle`, `#pos` |
| Lukker ved tvil | under terskel gir unknown | 530 av 530 negativer gir unknown; tomme og emoji-meldinger gir unknown | `#fail-closed` |

## Formålene

| Formål | Verifier | Status |
|---|---|---|
| root | test.parity.top1, test.parity.curve | oppfylt |
| data-bundle | test.bundle.hash | oppfylt, med avvik 1 |
| pos-table | test.pos-table | oppfylt |
| matcher-port | test.parity.top1 | oppfylt |
| pos-frame | test.parity.curve | oppfylt |
| fail-closed | test.fail-closed | oppfylt, med avvik 1 |

## Avvik

1. **Bunten sjekkes ikke mot sha256 når den lastes.** Planen sa «sha256 sjekkes ved lasting» og «endret bunt gir feil». Pakken avviser feil skjema og feil tegnklasse ved lasting, og testen sjekker sha256, men en endret bunt med riktig skjema lastes uten feil. Dette står åpent i README. Rettelsen er liten (forventet sha256 i koden, sjekk i `init`, én test til).
2. **Linux er ikke kjørt.** Kjent fra G1: tas i CI ved neste port.
3. **Første uavhengige kjøring (pfm2) stoppet på køens skrivetak** før noen test kjørte. Ikke en feil i pakken; skriptet bruker nå `LANDING/uten-skrivetak.sh`.

## Ikke med (som avtalt i G1)

Kobling inn i Butler eller `ChatPurposeResourceRouter`, engelske erklæringer, Book 23, push.
