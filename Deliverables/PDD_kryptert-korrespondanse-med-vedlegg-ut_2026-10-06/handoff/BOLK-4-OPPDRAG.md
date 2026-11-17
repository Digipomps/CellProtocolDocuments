# Bolk 4 — oppdrag til Codex: relasjonscellene på staging (CellScaffold)

PDD `kryptert-korrespondanse-med-vedlegg-ut`, 07.10.2026. Skrevet av korrespondanse-tråden (Claude-tråden i prosjektet «HavenAgentD»). Korrespondanse-tråden skulle skrive denne bolken selv; for å rekke Kjetils frist skriver Codex, og korrespondanse-tråden lar en uavhengig leser gå gjennom.

**Status: GODKJENT 07.10.2026.** G2 gitt kl. 19:57Z. Kjetil kl. 22:34Z, ordrett: «Jeg vil ha ferdig implementert, testet og deployet - og bygget nye installerere - når jeg står opp i morgen.» **Ingen merge, ingen utsetting i denne jobben**; det går gjennom kø-tråden etter Kjetils ja.

## Grunnlag

- `FORMAALSSPEC.md` §1 A2, A3, A6, B2 og §2 rad 8, 9 og 12; `PLAN.md` trinn 5; `handoff/BOLK-2-RAPPORT.md` og CellProtocol PR #63 (`codex/korr-relasjonscelle-20261007`, head `7f87b8e`).
- Det som finnes i CellScaffold i dag for den gamle kanalen: `Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift`, `Sources/App/Controllers/VaporAssistantCorrespondence.swift`, `configure.swift`. Den gamle kanalen skal ikke brytes av denne endringen, men får ikke nytt arbeid.
- Bro-ruta (HD-0190) og utgivelsene eies av bro-tråden og kø-tråden (`_losen-queue/KOORDINERING.md`). Les deres siste innlegg før du starter, og bygg oppå det som er på `main` eller i den gjeldende utgivelsesgrenen.

## Det som skal bygges (gren `codex/korr-staging-20261007` fra `origin/main` i CellScaffold, eget arbeidstre `_worktrees/cellscaffold-korr-staging-20261007`)

1. **Huse relasjonscellene** (A2, A3): en eier kan opprette en relasjonscelle på staging over broen; verten lagrer den med stabilt UUID, gjenoppretter den etter omstart, og gir den en adresse klienten kan nå over den autentiserte broen. Verten har ingen nøkkel som kan slippe inn et medlem eller åpne en konvolutt. Cellen tar bare imot konvolutter.
2. **Vedlegg** (B2): krypterte vedlegg lagres i avsenderens undercelle på datadisken; nytt vedlegg avvises når disken har under 10 GB ledig; utløp og tilbakekall fjerner bytene.
3. **Utløp** (A6): utløpte konvolutter og vedlegg fjernes også etter omstart av verten.
4. **Helse:** `/health/ready` viser om relasjonscellene og lagringen er klare, uten innhold.
5. **Pinne:** CellScaffold peker på CellProtocol-commiten `7f87b8e` mens du arbeider; når `handoff/CP-TAG-KORR.txt` finnes, bytt til taggen der. Følg kø-trådens regel om at pinnen bare endres i samme utgivelse som de andre trådene har avtalt; skriv i KOORDINERING før du endrer den på en utgivelsesgren.

## Prøver

- Nye tester røde før, grønne etter; den lokale porten i CellScaffold (alle bolker) grønn, med skriptene og banene i `_losen-queue/KOORDINERING.md`.
- Ende-til-ende mot lokal Vapor: eier oppretter celle, slipper inn en prøveidentitet, tekst og vedlegg over 1 MB begge veier, omstart av verten, historikk og vedlegg er der, utløp fjerner alt. Utskrift (uten verdier) i `evidence/bolk4-staging-lokalt.txt`.
- Sikkerhetskopi av korrespondansetilstanden før utsetting: skriv skriptet (`HAVEN-Deploy/_handoff/KORR-UT/`) og prøv det lokalt; kjør det ikke mot staging.

## Leveranse

`handoff/BOLK-4-RAPPORT.md` med tabell | Krav | Test | Utfall | Bevis |, PR-nummer (kladd) og CI, hva utsettingen krever (env, volum, disk), og «Ikke vist». Siste linje `STATUS: LEVERT` eller `STATUS: STOPPET — <grunn>`.

## Regler

- CellScaffold. Ingen endring i CellProtocol, HavenAgentD eller Binding. Ingen deploy, ingen vertsendring.
- Ingen debug-bypass; ingen eksisterende test fjernes eller svekkes; ingen hemmeligheter, IP-er eller brukerstier i rapport, commit eller PR.
- Skyv grenen når den har en commit; PR som kladd når CI-klar.
