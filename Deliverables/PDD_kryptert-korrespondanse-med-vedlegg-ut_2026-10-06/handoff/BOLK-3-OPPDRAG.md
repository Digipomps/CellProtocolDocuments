# Bolk 3 og 5 — oppdrag til Codex: klienten og godkjenningskortet i HavenAgentD, og nye installerere

PDD `kryptert-korrespondanse-med-vedlegg-ut`, 07.10.2026. Skrevet av korrespondanse-tråden (Claude-tråden i prosjektet «HavenAgentD»).

**Status: GODKJENT 07.10.2026.** G2 gitt kl. 19:57Z. Kjetil kl. 22:34Z, ordrett: «Jeg vil ha ferdig implementert, testet og deployet - og bygget nye installerere - når jeg står opp i morgen.» Macene: Vegar M2, Victoria Intel; macOS «vet ikke - men tror Tahoe».

Oppgavemappen: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/`. Stier er fra HAVEN-mappen. **Pakken sendes ikke til noen.** Ingen merge til `main` i denne jobben; korrespondanse-tråden henter Kjetils ja og merger.

## Grunnlag (les først)

- `FORMAALSSPEC.md` §1 (A1, A4, A5, A7, C1, C2, C3, C4, D3, D4) og §3; `PLAN.md` trinn 4 og 6.
- De godkjente bildene: `images/godkjenning-paa-macen-v1.png` (kortet under «Trenger deg» i adminvinduet til HAVEN Agent: forespørsel, kode på seks sifre, godkjenn med Touch ID/passord, forny, trekk tilbake) og `images/mottaker-oppsett-v1.png` (mottakerens oppsett fra én lenke med kode). Bygg det bildene viser; avvik står i rapporten med skjermbilde ved siden av bildet.
- `handoff/BOLK-2-RAPPORT.md`, avsnittet «HavenAgentD: kontrakten for bolk 3», og CellProtocol-grenen `codex/korr-relasjonscelle-20261007` (PR #63, head `7f87b8e`), særlig `Documentation/CorrespondenceRelationship.md`. Dette er protokollen klienten skal snakke.
- Dagens klient: `HavenAgentD/Sources/HavenCorrespondenceMCP/` på `main` (bare invitert part, bare `get`/`set`), vedleggsgrenen `codex/correspondence-attachments-20260930` (`a6bd163`), og adminvinduet `Sources/HavenAgentMenu/AdminWindow.swift` på `main`.

## Det som skal bygges (gren `codex/korr-klient-20261007` fra `origin/main` i HavenAgentD, eget arbeidstre `_worktrees/havenagentd-korr-klient-20261007`)

1. **Pinne:** HavenAgentD peker på CellProtocol-commiten `7f87b8e` (PR #63-hodet) mens du arbeider. Når fila `handoff/CP-TAG-KORR.txt` finnes, står taggen der; bytt pinnen til den taggen før PR-en åpnes. Finnes den ikke når alt annet er grønt, åpne PR-en som kladd med commit-pinnen og skriv det.
2. **Én klient for eier og invitert** (A1): samme kode og samme kommandoer for begge parter; eieren kan sende og hente tekst og vedlegg i sin egen celle. Vedleggskoden fra `a6bd163` tas inn og tilpasses (eierens vedlegg bruker cellens UUID som `agreementID`).
3. **Over broen** (A5): klienten åpner kanalen med håndtrykket fra CellProtocol #53 (`2026.9.5`) og bruker den for alle operasjoner; ingen annen vei. Først en liten prøve av abonnement over broen mot en lokal Vapor-vert i testen. Virker ikke abonnement over broen fra klienten, stopp der og skriv det.
4. **Ny post uten spørring** (A7): abonner på Flow `haven.correspondence`, åpne `message.stored`-konvolutten direkte; ved gjenkobling hent `state` og les det som mangler.
5. **Eierens side på Macen** (C2, C3, D3): relasjonscellen opprettes av eieren; invitasjon lages som én lenke + kode på seks sifre; når den inviterte melder seg, kommer et kort under «Trenger deg»; godkjenning, fornyelse og tilbakekall signeres med eierens nøkkel i nøkkelringen og krever Touch ID eller passord hver gang (`userPresence`). Agentens vanlige lesing og sending skal ikke kreve dialog. En prøvenøkkel for testidentiteter skal ikke åpne en vei rundt låsen for ekte identiteter.
6. **Mottakerens oppsett** (C1): fra lenken og koden til en virkende agent med høyst to håndgrep etter installasjonen.
7. **Ingen verdier i logg** (D4): ingen nøkler, koder, lenker eller meldingstekst i logger eller utskrifter.
8. **PR #28 og #30 i HavenAgentD:** les dem, si i rapporten om hver bør merges, lukkes eller tas inn i denne grenen, og gjør det som trengs for at `main` med denne grenen blir grønn i CI. Ikke merge noe selv.

## Prøver

- Nye tester røde før, grønne etter; alle eksisterende tester i HavenAgentD grønne. Bygg og test som skriptjobber etter banepolitikken i `_losen-queue/KOORDINERING.md`.
- **Lokal formålsprøve ende til ende:** en lokal Vapor-vert med relasjonscellen (fra CellProtocol-grenen), to agentprofiler med hvert sitt nøkkellager (prøvenøkler, ingen Touch ID), invitasjon, godkjenning, tekst og et vedlegg over 1 MB begge veier, ny post over Flow, fornyelse, tilbakekall. Utskriften (uten verdier) i `evidence/bolk3-formaalsproeve.txt`.
- Skjermbilde av kortet og av mottakerens oppsett ved siden av de godkjente bildene, i `evidence/`.

## Installererne (bolk 5)

Når alt over er grønt: bygg pakken fra en ren eksport av grenen (ikke fra arbeidstreet) med `HavenAgentD/Packaging/build_pkg.sh` og `notarize_pkg.sh`, `ARCHS="arm64 x86_64"`, laveste macOS slik at både Tahoe og eldre støttede versjoner virker (oppgi hvilken). Signert med Developer ID, notarisert, billett staplet, `spctl` godkjent. Regn ut `SHA256SUMS` og manifest på nytt **etter** stapling. Kontroller med `lipo -archs` at alle binærene har begge arkitekturer. Pakken og sjekksummene legges i `HavenAgentD/.build/korr-release-20261008/dist/`. Pakken prøves ikke på Intel her; skriv hva som er prøvd.

## Leveranse

`handoff/BOLK-3-RAPPORT.md`: tabell | Krav | Test | Utfall | Bevis |, PR-nummer og CI, pakkens filnavn, SHA-256, `spctl`-utskrift og arkitekturer, svar om #28 og #30, «Ikke vist». Kjørt og lest i kode holdes adskilt. Siste linje `STATUS: LEVERT` eller `STATUS: STOPPET — <grunn>`. Kjør `CellScaffold/scripts/haven_learn.py` for det som er gjenbrukbart.

## Regler

- HavenAgentD, og bare lesing i CellProtocol. Ingen endring i CellScaffold eller Binding. Ingen deploy, ingen sending.
- Ingen debug-bypass. Ingen eksisterende test fjernes eller svekkes. Ingen hemmeligheter, lenker, koder, IP-er eller brukerstier i rapport, commit, PR eller bevis.
- Skyv grenen når den har en commit; PR mot `main` som kladd når CI-klar.
- Er et krav umulig uten et valg Kjetil må ta, stopp ved det kravet, skriv alternativene, og lever resten.
