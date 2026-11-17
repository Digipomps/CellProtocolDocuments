# HD-0154 — etter G1

G1 er godkjent av Kjetil 2026-10-02. G1-GUI og G2 avventer vurdering av bilder og PLAN.md. Ingen implementeringsjobb er sendt til køen.

1. Les FORMAALSSPEC.md, PLAN.md og STATUS.md fra denne PDD-mappen.
2. Gjennomgå bildene i images/; alle er lokalt rendret med eksempeldata. render-result.json dokumenterer fixturekontroller, ikke live funksjon.
3. Registrer G1-GUI/G2 bare ved brukerens eksplisitte ord. Installer ingen graf-target før riktig eier/grant er verifisert.
4. Etter godkjenning: mål kapasitet, les Losens KOORDINERING, oppdater Git-basis, velg eget arbeidstre og implementer i P1–P5-rekkefølge.
5. Ingen oppgave sendes automatisk av denne dokumentasjonen. Ingen CI, vertsclaim, deploy eller sletting er utført.

Preview-løperen renderer bare lokale fixtures og skriver bilder/resultat i sin egen mappe. Den bruker installert Chrome med en separat midlertidig profil; brukerens innloggede profil leses ikke. HTML-eksempelhandlinger er preview.* og har ingen MCP-/HTTP-/filsystemeffekt. Bundlet Playwrights headless-shell-revisjon manglet; ingen nettinstallasjon ble gjort.
