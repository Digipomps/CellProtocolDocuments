# Handoff: rekkefølge og kommandoer

PDD `kryptert-korrespondanse-med-vedlegg-ut`, G2-artefakt, 07.10.2026. Dette er det som går til Codex og til køene på Macen, i rekkefølge. Ingen kommandoer her er ment for Kjetil. Codex-arbeidet legges inn av kø-tråden, i banen den tildeler i `_losen-queue/KOORDINERING.md`. Skriptjobber for staging og prøver legges inn av korrespondanse-tråden (Claude-tråden i prosjektet «HavenAgentD»), i bane b.

Hver bolk er merket **godkjent** eller **sperret**. En bolk som er sperret, legges ikke i noen kø. Bare korrespondanse-tråden endrer merket, og bare etter Kjetils ord, som føres ordrett i `STATUS.md` i oppgavemappen og i `_losen-queue/KOORDINERING.md`. Er denne fila, statuslinja i et oppdrag og `STATUS.md` uenige, gjelder `STATUS.md`, og ingenting startes før de er like.

Stier er fra HAVEN-mappen. Oppgavemappen er `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/`. Bolkene 1–6 er ikke standardvalgene S1–S10 i `FORMAALSSPEC.md`.

## Regler som gjelder alle bolkene

- **CellProtocol først.** Det som må inn i CellProtocol for at noe i HavenAgentD eller CellScaffold skal virke, går inn der og ut i en utgivelse først (Kjetil til kø-tråden 07.10).
- Ingenting til `main` uten Kjetils «merge» for den PR-en. Ingen utsetting til staging uten hans ja, og etter kø-trådens rekkefølge.
- Fra bolk 2 skyves hver gren til GitHub når den har en commit, slik at arbeidet finnes mer enn ett sted. Bolk 1 holdes lokalt, med forskjellen lagt som fil i oppgavemappen.
- Nye tester er røde før endringen og grønne etter. Ingen eksisterende test fjernes eller svekkes.
- Det Codex skriver, gjennomgås av Fabel (en uavhengig Claude-leser). Det korrespondanse-tråden skriver, gjennomgås av Astra (Codex). Rapporten fra gjennomgangen legges i `panel/` eller `evidence/`.
- Ingen nøkler, engangskoder, lenker eller ekte identitetsnumre i rapporter, logger eller bevis.
- `git` kjøres aldri gjennom den tilkoblede mappen fra skyen. Git og bygg går i køene på Macen.
- Skript for Macen skrives for bash 3.2 og følger skillen `haven-mac-shell-scripts`.

## Bolk 1 — prøve av innslipp med en avtale signert utenfor cellens prosess · **godkjent 07.10** (Kjetil: «A ja, B ja, C ja»)

- Oppdrag: `handoff/BOLK-1-OPPDRAG.md`.
- Repo: CellProtocol. Gren `codex/korr-innslipp-proeve-20261007` fra `origin/main` (`68069b6`, taggen `2026.9.5`), i eget arbeidstre. Lokalt: ingen push, ingen PR.
- Kø-tråden legger Codex-jobben i kø. Forslag til promptfil og jobbfil: `handoff/BOLK-1-KOEPROMPT.md`. Bestilt i `_losen-queue/KOORDINERING.md` 07.10.
- Ferdig når `handoff/BOLK-1-RAPPORT.md` og `handoff/BOLK-1-ENDRING.patch` finnes. Korrespondanse-tråden leser rapporten og forskjellen, lar en uavhengig leser kontrollere dem, og sier til Kjetil om prøven holder.
- Holder den ikke: saken går tilbake til Kjetil før noe annet bygges.

## Bolk 2 — cellen i CellProtocol · **godkjent 07.10** (G2: Kjetil kl. 19:57Z «1. ja … 4. gjør det så raskt som mulig»; bolk 1 holder etter `panel/KONTROLL-BOLK-1.md`, med MÅ 1 rettet i bolk 2)

- Oppdrag: `handoff/BOLK-2-OPPDRAG.md`. Lagt inn som Codex-jobb `a41` i bane a.

Det `PLAN.md` kaller trinn 2: eieren som deltaker også for vedlegg, innslipp, fornyelse og tilbakekall signert på eierens maskin, levering med Flow og `state`, og koden for vedlegg oppå ny hovedgren. Kjetil har sagt ja til at koden for vedlegg kan slås sammen med hovedgrenen før mottakerne har prøvd den, når funksjonsprøvene, en uavhengig gjennomgang og en lokal formålsprøve er grønne (svar B, 07.10). Selve sammenslåingen får eget «merge» fra ham. Oppdraget skrives når rapporten fra bolk 1 er lest, for formen på innslippet følger av den. Codex skriver, Fabel gjennomgår, og kø-tråden gir ut.

## Bolk 3 — klienten og vinduet i HavenAgentD · **sperret** (G2, og bolk 2 gitt ut)

Samme klient for eier og invitert, håndtrykk og abonnement over broen, oppsett fra én lenke, koden på seks sifre, og kortet under «Trenger deg» med lenke, godkjenning, fornyelse og tilbakekall. Først en liten prøve av abonnement over broen. Oppdraget skrives etter bolk 2. Codex skriver, Fabel gjennomgår. CellProtocol `2026.9.5`, med broen, ble tagget 07.10 kl. 15:04Z.

## Bolk 4 — staging i CellScaffold · **godkjent 07.10** (G2 og bolk 1 som holder; settes ikke ut før bolk 2 er gitt ut og bro-ruta er på staging)

Huse relasjonscellene, lagre vedlegg, rydde ved utløp. Korrespondanse-tråden skriver, Astra gjennomgår. Kan skrives mot et lokalt bygg av bolk 2, men settes ikke ut før bolk 2 er gitt ut og bro-ruta er på staging. Utsetting skjer med `haven-deploy`, på Kjetils ja, når kø-tråden sier det er plass.

## Bolk 5 — pakken · **sperret** (G2; bolk 3 på hovedgrenen; grønn hovedgren i HavenAgentD med PR #28 og #30 avgjort; macOS-versjonene til mottakerne; og en avtalt måte å prøve Intel på)

Én fil, signert og notarisert, bygget av Codex med `HavenAgentD/Packaging/build_pkg.sh` og `HavenAgentD/Packaging/notarize_pkg.sh`. Pakken må virke på Apple-prosessor og på Intel: Vegar har en M2, og Victoria har en Intel-Mac (Kjetil 07.10). Korrespondanse-tråden prøver den på en Mac uten HAVEN og teller håndgrepene.

## Bolk 6 — prøveparet, Kjetils Mac, Vegar og Victoria, og aksept · **sperret** (G2, og bolk 4 og 5)

Rekkefølgen står i `PLAN.md`, trinn 6 til 9. Trinn 9 (aksept, endringsforslaget til Book 33 og opprydding i den gamle kanalen) hører til denne bolken. Pakken sendes ikke til Vegar og Victoria før Kjetil har godkjent pakketeksten. At den sendes uten assistentidentiteten, har han sagt ja til (svar A, 07.10).

## Lesejobber som er kjørt (trenger ingen godkjenning: de endrer ingenting)

| Jobb | Skript | Utdata | Når |
|---|---|---|---|
| `b41-korr-ut-les-g2-grunnlag-20261007` | `HAVEN-Deploy/_handoff/KORR-UT/les-g2-grunnlag.sh` | `HAVEN-Deploy/_handoff/KORR-UT/maal/G2-GRUNNLAG-20261007.md` | 07.10 kl. 14:35Z |
| `b42-korr-ut-les-plass-staging-20261007` | `HAVEN-Deploy/_handoff/KORR-UT/les-plass-staging.sh` | `HAVEN-Deploy/_handoff/KORR-UT/maal/PLASS-STAGING-20261007.md` | 07.10 kl. 14:35Z |
