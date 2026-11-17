# Bolk 4 — stoppet før implementering

Relasjonscellene er **ikke implementert eller funksjonsprøvd i CellScaffold i denne jobben**. Ingen deploy eller installerbygg er utført. Oppdraget forbyr merge, deploy og vertsendring i bolk 4; disse stegene eies av kø-tråden. Denne rapporten er en stoppmelding, ikke en ferdig kodeleveranse.

## Konkret avhengighet og omfang

Nett-fetch av CellScaffold `origin/main` gav `381094bbb18e390bd8fd2b8955524b5fa3e4f9ea`. Separat, låst arbeidstre `_worktrees/cellscaffold-korr-staging-20261007`, gren `codex/korr-staging-20261007`, er opprettet fra denne basen. Ingen kildeendringer er gjort der.

På basen mangler `Sources/App/Services/ScaffoldBridgeRuntime.swift`; `Sources/App/Controllers/VaporBridgehead.swift` sier eksplisitt at ingen rute registreres, og den gamle bridgehead-ruta i `Sources/App/routes.swift` er kommentert ut. Andre WebSocket-ruter finnes, blant annet Sprout native-porthole; dette er **ikke** en påstand om at scaffoldet mangler alle broer. De er ikke påvist som korrespondansens avtalte autentiserte bro-rute.

HD-0190-kandidaten `hd0190/on-release-2026.9.7` på `d726890683d1ad0ccf0f0c70d290a1fb438f01cd` har `ScaffoldBridgeRuntime` og `AuthenticatedBridgeIngress`. Den er ikke integrert i `origin/main`. `_losen-queue/KOORDINERING.md`, kø-trådens innlegg 07.10 21:36Z, sier at HD-0190 ikke kan gå i 2026.9.8, men venter på neste CP-utgivelse med HD-0196. `Deliverables/PDD_bro-connect-kontekst_2026-10-07/STATUS.md` sier G1 venter og ingen implementering eller tester kjørt.

HD-0196s påviste signeringsgap gjelder browser-holder-adapteren. Det er **ikke påvist** at en ekstern klient med eget nøkkellager har samme gap. Stoppen her gjelder den avtalte bro-integrasjonen og utgivelsesbasen, ikke en ny konklusjon om at CellProtocols native bro er umulig å bruke. En ny, parallell bro-rute eller innlemming av den stoppede HD-0190-kandidaten er ikke utført.

`handoff/CP-TAG-KORR.txt` finnes ikke ved inventaret. CellProtocol `7f87b8e` og bolk-2-rapporten er lest; ingen pinne er endret, heller ikke på utgivelsesgren.

## Krav og prøver

| Krav | Test | Utfall | Bevis |
|---|---|---|---|
| Eier oppretter relasjonscelle over autentisert bro, stabil UUID og adresse | Lokal Vapor-opprettelse og omstart | Ikke kjørt; avtalte rute mangler på basen | `evidence/bolk4-staging-lokalt.txt`, kildeinventar |
| Vert uten deltakernes private nøkler, bare konvolutter | Nøkkel-/klartekstkontroll og negativt innslipp | Ikke kjørt i CellScaffold | Samme inventar; bolk-2-prøver er ikke vertsprøver |
| Krypterte vedlegg på datadisk, 10 GB terskel, tilbakekall rydder byte | Begge retninger over 1 MB; lavplass- og tilbakekallsprøve | Ikke implementert eller kjørt i denne bolken | Samme inventar |
| Utløp rydder konvolutter og vedlegg også etter omstart | Stopp før utløp, start etter utløp, kontroller disk | Ikke kjørt | Samme inventar |
| `/health/ready` viser relasjonscelle-/lagringsberedskap uten innhold | HTTP-readiness før/etter lagringsfeil | Ikke implementert eller kjørt | Samme inventar |
| Nye tester røde før, grønne etter; alle lokale bolker grønne | Bane b/c, eget byggområde og kapasitetsvakt | Ingen bygg/testjobber lagt; ingen grønn port hevdes | Samme inventar |
| Backupskript lokalt prøvd før utsetting | Backup/restore med kontroll av alle byte | Ikke skrevet eller prøvd; hostens nye lagringslayout er ikke etablert | Ingen backup-bevis |

## PR og CI

Ingen CellScaffold-commit, push, kladd-PR eller CI-kjøring. Grenen har bare basiscommiten. Det er ingen CI-klar kandidat å publisere. Ingen eksisterende test er endret, fjernet eller svekket. Andre repoers kode og arbeidstrær er ikke endret.

## Hva videre implementering og utsetting krever

1. Bro-/kø-tråden må levere og navngi den avtalte integrasjonsbasen med autentisert rute for eksterne korrespondanseklienter, inklusive abonnement. Ta stilling til om native korrespondanse kan integreres uavhengig av browser-holder-gapet; dette er ikke avgjort av inventaret.
2. Fortsett CellScaffold-implementeringen i den isolerte grenen. Bruk CP `7f87b8e` som oppdraget tillater inntil korrespondansetaggen er levert; koordiner utgivelsespinnen før endring på utgivelsesgren.
3. Etabler et varig datavolum for relasjonssnapshots og avsendernes krypterte vedlegg. Root skal komme fra vertskonfigurasjonen, ikke klientens input. Konkrete nye env-navn, volumstier, diskbruk og backup-layout er **ikke implementert eller målt**. HD-0190-kandidaten bruker `CELL_SCAFFOLD_BRIDGE_ORIGIN`; dette er lest kandidatkode, ikke dokumentasjon av en deployet rute.
4. Implementer lavplassavslag under 10 GB, varig lagring, omstartsopprydding og readiness. Kjør rødt/grønt og fullport gjennom b/c, lokal Vapor-prøve og lokalt backup/restore før kladd-PR/CI. Deretter går review, merge og staging gjennom kø-tråden.

## Ikke vist

Ingen relasjonsopprettelse over nett, datadisklagring, readiness-utvidelse, overføring, UUID-/historikkgjenoppretting, utløp etter omstart, lavplassavslag eller backup/restore. Ingen CI, stagingverifikasjon eller installerleveranse. Kildeinventaret erstatter ingen av disse prøvene.

STATUS: STOPPET — avtalte autentiserte bro-integrasjon er ikke tilgjengelig på main/avtalt utgivelsesbase; HD-0190 er utsatt av kø-tråden, implementering og alle funksjonsprøver gjenstår
