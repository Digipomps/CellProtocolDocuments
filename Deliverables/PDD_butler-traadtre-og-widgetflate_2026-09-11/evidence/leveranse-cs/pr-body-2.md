Butler-arbeidsflaten og web-siden av skjelettrunden, bygget på CellProtocol-runden som nå er i main.

**Hva som er nytt**

- Butlers hjelpertre er et `Tree` med skop: å velge en node styrer loggen, tellerne og hva skrivefeltet skriver til.
- Butler Chat er en arbeidsflate: trepanel, chat og «Flaten rundt» side om side fra 1100 px, stablet under.
- Web-rendereren tolker layout likt med appen: Spacer tar ledig plass, stabler fyller bredden, TextArea-modifikatorene legges én gang, fast bredde krymper ikke i en rad, og en rad bryter linjen bare med `wrap: true`.
- `ComponentSurface.instanceIDKeypath` og layoutvariantenes `hidden`/`width` virker i web-rendereren, og runtime-dekoderen slipper dem gjennom.
- Pinnene er løftet til de merget rundene: CellProtocol `473357cf`, DiMyMicropayments `836ba8e6`, DiMyMint `af41630b`. SwiftPM godtar bare ett revisjonskrav per pakke, og hver av dem bærer sitt eget krav til den under, så de må flyttes samtidig.

**Hva CI fant, og hva som er rettet**

Første CI-runde var rød på to browser-bevis. Begge var regresjoner denne runden hadde innført, og begge er reprodusert lokalt før de ble rettet:

- *Globale lyttere på en avvist kandidat.* `porthole-skeleton-atomic-swap.spec.js` teller `document.addEventListener("keydown", …)` mens Porthole forkaster en kandidat-renderer. Målt: `{added: 1, removed: 1}` med denne grenen, `{0, 0}` med main. `createRenderer` la drag-lytterne på med én gang, mens presentasjonshåndtereren ventet på `mount`. Nå følger begge mount og fjernes i `destroy`.
- *Skrivefeltet under folden.* `butler-explicit-helper-placement.spec.js` krever at skrivefeltet ligger inne i vinduet. Målt på 1280×900: skallet var 1099 px høyt og skrivefeltets bunn lå på y=999. Arbeidsflaten fylte tre kolonner, og skallet vokste med dem. Skallet bindes nå til vindushøyden når en arbeidsflate er på siden, og rullefeltene som allerede fantes tar overflødet. Etter rettelsen: dokumentet 900 px, skrivefeltets bunn y=800.

Tre-delen av den samme spec-en drev fortsatt skuffen som denne runden erstattet — «Tråder»-knapp, `butler-helper-tree-rail`, «Lukk tre». På web ligger treet nå i sin egen kolonne. Delen beholder hver påstand den gjorde — brukeren når treet, skopet følger den valgte grenen, og valget overlever en omlasting — og når dem gjennom arbeidsflaten i stedet. Klikket på «Tråder» står bak en tilstedeværelsessjekk, så den dekker skuffen igjen når appbredden får den tilbake.

**Hva som fortsatt ikke virker**

`playwright/butler-chat-mobile.spec.js` er rød: skrivefeltet nås ikke på 375 px. Kontrollert med CSS-en både på og av — rød i begge tilfeller, altså brutt tidligere i runden av den stablede arbeidsflaten, ikke av rettelsene over. Den hører til appbredde-arbeidet (skjult tre via `hidden` i `SkeletonLayoutVariant`), som står åpent.

Det lokale CI-filteret (`ci/run-tests.sh`) kunne ikke kjøres i denne runden: diskvakten krever ≥40 GiB og ≥5 % ledig, og maskinen har 43 GiB av 927 GiB. Jobben som kjører filteret er rettet slik at en tom klassifisering ikke lenger teller som grønn.

**Testet**

Bygg og tester mot de ekte pinnene, ikke den lokale stioverstyringen: fokuserte tester grønne, plassering-spec-en grønn på både 1280×900 og 375, og naboene på samme flate — autoscroll, hjelpertreet, chat-layout — grønne. Formålstesten T-P1 er grønn mot lokal testvert, med skjermbilder og målinger i `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/evidence/`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011CHU13qBKbb5szsQQo53rW
