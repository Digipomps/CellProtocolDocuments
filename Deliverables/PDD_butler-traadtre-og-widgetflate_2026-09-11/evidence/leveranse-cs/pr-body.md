Butler-arbeidsflaten og web-siden av skjelettrunden, bygget på CellProtocol-runden som nå er i main.

**Hva som er nytt**

- Butlers hjelpertre er et `Tree` med skop: å velge en node styrer loggen, tellerne og hva skrivefeltet skriver til.
- Butler Chat er en arbeidsflate: trepanel, chat og «Flaten rundt» side om side fra 1100 px, stablet under.
- Web-rendereren tolker layout likt med appen: Spacer tar ledig plass, stabler fyller bredden, TextArea-modifikatorene legges én gang, fast bredde krymper ikke i en rad, og en rad bryter linjen bare med `wrap: true`.
- `ComponentSurface.instanceIDKeypath` og layoutvariantenes `hidden`/`width` virker i web-rendereren, og runtime-dekoderen slipper dem gjennom.
- CellProtocol-pinnen er løftet til den merget runden, så paritetsmatrisens revisjonssjekk stemmer igjen.
- DiMyMicropayments og DiMyMint følger med: SwiftPM godtar bare ett revisjonskrav per pakke, og hver av dem bærer sitt eget krav til den under.

**Testet**

Bygg og tester er kjørt mot den ekte pinnen (ikke den lokale stioverstyringen): fokuserte tester grønne, og CI-filteret uten nye feil eller avbrudd. Formålstesten T-P1 (hjelpertreet i den levende chatten) er grønn mot lokal testvert, med skjermbilder i `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/evidence/`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011CHU13qBKbb5szsQQo53rW
