# Bolk 2 — oppdrag til Codex: relasjonscellen i CellProtocol, med vedlegg, klar for PR

PDD `kryptert-korrespondanse-med-vedlegg-ut`, 07.10.2026. Skrevet av korrespondanse-tråden (Claude-tråden i prosjektet «HavenAgentD»).

**Status: GODKJENT 07.10.2026.** G2 er gitt. Kjetil, ordrett, kl. 19:57Z: «1. ja 2. ja 3. vet ikke - men tror Tahoe  4. gjør det så raskt som mulig.» Punkt 1 er G2 for `PLAN.md`; punkt 4 er at merge, pakke og sending skal skje så raskt som mulig. Tidligere samme dag, svar B: koden for vedlegg kan slås sammen med hovedgrenen før Vegar og Victoria har prøvd den, når funksjonsprøvene, en uavhengig gjennomgang og en lokal formålsprøve med to prøveidentiteter er grønne. **Selve merge får eget ord fra Kjetil. Denne jobben merger ikke.**

Oppgavemappen: `CellProtocolDocuments/Deliverables/PDD_kryptert-korrespondanse-med-vedlegg-ut_2026-10-06/`. Stier er fra HAVEN-mappen.

## Hva dette er til

Kjetil og hver av Vegar og Victoria skal skrive til hverandre i én relasjonscelle (`CorrespondenceCell`), kryptert, med vedlegg begge veier. Cellen kjører på staging, som ikke har noen nøkkel som åpner en konvolutt eller slipper inn et medlem. Kjetil eier cellen og er selv part; nøklene hans ligger på Macen hans. Godkjent i G1: `FORMAALSSPEC.md` (iterasjon 3), formålene A1, A3, A4, A7, B1, C3 og D3. Les §0 (A6–A10, A18–A22) og §1 der før du begynner.

## Utgangspunkt

1. Bolk 1: `handoff/BOLK-1-RAPPORT.md`, `handoff/BOLK-1-ENDRING.patch`, lokal gren `codex/korr-innslipp-proeve-20261007` (`8dfbd3f0`). Innslipp med en avtale signert utenfor cellens prosess virker der: valgfri `targetCellUUID` i `Contract`, dekket av signaturen, og `GeneralCell.acceptExternallySignedAgreement(_:for:)`.
2. Den uavhengige lesingen av bolk 1: `panel/KONTROLL-BOLK-1.md`. **Hvert MÅ-punkt der rettes i denne bolken, med en test.** BØR-punkter rettes eller begrunnes i rapporten.
3. Vedleggsgrenen `codex/correspondence-attachments-20260930` i CellProtocol (`9420e7d`, bygger på `81601a6`), bare lokal. Beskrevet i `CellProtocolDocuments/Deliverables/VEDLEGG_IMPL_3_2026-09-30.md`. Formålene og Kjetils svar for vedlegg står i `CellProtocolDocuments/Deliverables/PDD_vedlegg-korrespondanse_2026-09-28/` og gjelder som de er.

## Det som skal bygges

Ny gren `codex/korr-relasjonscelle-20261007` fra `origin/main` (`68069b6`, taggen `2026.9.5`), i eget arbeidstre `_worktrees/cp-korr-relasjonscelle-20261007`. Ta inn bolk 1 og vedleggsgrenen (cherry-pick eller rebase; løs konflikter mot `main` slik den er nå), og bygg:

1. **Innslipp signert på eierens maskin** (A3, A4, C2). Bolk 1-veien, rettet etter kontrollen, er den eneste veien et medlem kommer inn i en relasjonscelle på en vert uten eierens nøkkel. Den signerte avtalen gir den inviterte cellens adresse, medlemmenes offentlige krypteringsnøkler og nøyaktig rettighetene i malen (`CorrespondenceAgreementTemplates.swift`), og er bundet til én celle. `.ownerApprovalRequired` endres ikke. Verten kan ikke selv slippe inn noen.
2. **Fornyelse og tilbakekall signert på eierens maskin** (C3). Fornyelse: en ny eiersignert avtale med senere utløp erstatter den gamle for samme subjekt og celle; medlems- og kontraktlistene vokser ikke. Tilbakekall: et eiersignert tilbakekall (bundet til celle, subjekt og avtale, med tidspunkt, ikke gjenbrukbart) som verten tar imot og som fjerner medlemmet, kontraktene og subjektets tilgang til vedlegg. Verten kan ikke trekke tilbake noe på egen hånd ut over det som finnes i dag for eieren. **Tilbakekallet skal vare** (MÅ 1 i `panel/KONTROLL-BOLK-1.md`): i bolk 1 kan et medlem som er fjernet, legge fram den samme kontrakten igjen og komme inn til den utløper, og en fjerning mens innslippet venter på nøkkelbeviset går tapt. Tilbakekallet lagres varig i cellen og kontrolleres både i `acceptExternallySignedAgreement` og i `authorizationContracts(for:)`, og innslippet kontrollerer det på nytt rett før `installAuthorization`. Test: tilbakekall, så ny framlegging av den gamle kontrakten, avvises; tilbakekall under et ventende innslipp gir ikke medlem; tilbakekallet står etter omstart av cellen fra lagret tilstand.
3. **Eieren som full deltaker** (A1, B1). Eieren kan sende og lese tekst og sende og hente vedlegg i sin egen celle, med samme operasjoner og samme klientprotokoll som den inviterte. I dag kan bare den inviterte sende vedlegg (A10 i §0: `authorizeAttachment`/`performAttachment` krever at avsenderen har en avtale). Mottakernøklene tas fra cellens medlemmer, ikke bare fra avsenderens avtale. Eieren må bevise nøkkelen sin for hver handling, som i dag.
4. **Levering med Flow og historikk med `state`** (A7). Ny post, kvittering og vedleggshendelser går ut på Flow-emnet `haven.correspondence` til medlemmene, uten at noen spør. Hendelsen inneholder ikke klartekst og ikke mer enn ytterdelen av konvolutten allerede viser. Historikken hentes med `state`/innboksen, bare for medlemmer. En ikke-medlem som abonnerer, får ingenting.
5. **Utløp fjerner alt** (A6): når en melding utløper, forsvinner hele konvolutten og vedleggene som hører til den, uten at noen må lese innboksen først. Det som finnes for dette på vedleggsgrenen, beholdes og testes.
6. **Ingen agent slipper inn noen** (D3): ingen operasjon gir en agent eller verten mulighet til å signere innslipp, fornyelse eller tilbakekall uten eierens private nøkkel.

## Prøver (alle røde før endringen der det gir mening, grønne etter)

- Funksjonstester i nye filer under `Tests/CellBaseTests/`, én per krav over, og alle avvisningene fra bolk 1 (a–h) også mot relasjonscellen.
- **Lokal formålsprøve** (Kjetils regel 18.09: nye kapabiliteter prøves mot funksjon og formål før de går til hovedgrenen). Tre adskilte sammenhenger med hvert sitt nøkkellager: E (eierens nøkler), H (huser cellen, ingen nøkler), I (den inviterte). E slipper inn I; tekst og ett vedlegg på over 1 MB går begge veier; ny post kommer til mottakeren over Flow uten spørring; E fornyer I og trekker så I tilbake, og I får deretter ingenting. Utskriften (uten nøkler og ekte identiteter) legges i `evidence/bolk2-formaalsproeve.txt` i oppgavemappen. Samme prøve skal kunne kjøres med én kommando, dokumentert i rapporten.
- Hele testmengden i CellProtocol på Macen med `HAVEN-Deploy/_handoff/GRUNNMUR/wp-cellprotocol-grunnmur.sh codex/korr-relasjonscelle-20261007`. Oppgi tallene.

## Slik gjøres det på denne Macen

- Bygg og tester som skriptjobber etter banepolitikken i `_losen-queue/KOORDINERING.md` (bane b for korte, bane c for fullport), med skript under `HAVEN-Deploy/_handoff/KORR-UT/` etter mønsteret i `HAVEN-Deploy/_handoff/KORR-UT/wp-korr-admission-focused.sh` og `wp-korr-admission-full.sh`. Promptfil først, så jobbfil via `.tmp` og `mv`. Se i `done/`, `running/` og innboksene før et jobbnummer brukes.
- Følg regel 1–3 i `_losen-queue/KOORDINERING.md` og punkt 11 i `_losen-queue/LES_MEG.md`.
- Ikke rør hovedarbeidstreet i CellProtocol, `a35`-arbeidstreet eller andre arbeidstrær.
- **Når hele testmengden er grønn:** skyv grenen til GitHub og åpne en PR mot `main` i `Digipomps/CellProtocol` som **kladd** (draft), med tittel «Korrespondanse: relasjonscelle med innslipp signert av eier, Flow-levering og vedlegg». Beskrivelsen: hva Kjetil ser før og etter, hvordan formålsprøven kjøres, og en lenke til rapporten. Følg CI til den er grønn; ved rød CI av kodegrunn, rett og skyv på nytt. Rød CI som også er rød på `main`, noteres.
- **Ingen merge, ingen tag, ingen pinnendring, ingen deploy.**

## Leveranse

`handoff/BOLK-2-RAPPORT.md` i oppgavemappen. Øverst en tabell: | Krav | Test | Utfall | Bevis (kommando, exit-kode, antall tester) |. Deretter: PR-nummer og commit, CI-status, hvordan hvert MÅ-punkt fra `panel/KONTROLL-BOLK-1.md` er rettet, hva klienten i HavenAgentD må endre for å bruke dette (operasjonsnavn, nyttelast, Flow-hendelser; dette er grunnlaget for bolk 3), og «Ikke vist». Skill mellom **kjørt** og **lest i kode**. Skriv «vet ikke» der det er sant. Siste linje: `STATUS: LEVERT` eller `STATUS: STOPPET — <grunn>`.

Kjør `CellScaffold/scripts/haven_learn.py` for det som er gjenbrukbart, eller `none --reason`.

## Regler

- Bare CellProtocol. Ingen endring i HavenAgentD, CellScaffold eller Binding.
- Ingen debug-bypass; `CellBase.debugValidateAccessForEverything` av i testene, og testene feiler hvis den er på.
- Ingen eksisterende test fjernes eller svekkes.
- Private nøkler bare i testenes egne nøkkellagre. Ingen nøkler, tokener, IP-adresser, brukerstier eller ekte identiteter i rapport, commit, PR eller bevis. Stier relative til repoet.
- Er et krav over umulig uten et valg Kjetil må ta, stopp ved det kravet, skriv valget med alternativene i rapporten, og lever resten.
