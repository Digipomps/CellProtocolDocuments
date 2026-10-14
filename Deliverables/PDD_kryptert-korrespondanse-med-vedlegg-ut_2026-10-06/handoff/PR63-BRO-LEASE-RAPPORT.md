HODE: 7ebb4f5f76cdcda39a2abc2e42c8743a62a703b0
STATUS: LEVERT

# PR #63 — broens nøkkelbevis velger den lengstlevende aktive leasen

Grunnlag: rent arbeidstre på `36959ae4a114503b08ff85785e0d73f865d4758e`, gren
`codex/korr-relasjonscelle-20261007`. Overleveringens «Brofeilen: observert spor og
påvist mekanisme» og k6-diagnostikken er lest. Rettelsen er committet og pushet
på samme gren i eksisterende [PR #63](https://github.com/Digipomps/CellProtocol/pull/63).

## Rettelse og bevart autorisasjon

Bare `Sources/CellBase/Cells/Bridging/BridgeIdentityProofAuthorization.swift` og
`Tests/CellBaseTests/BridgeIdentityProofAuthorizationTests.swift` er endret i CP.
`permit` purger fortsatt utløpte leaser og filtrerer på utfordringens scope.
Valget prioriterer en lease uten utløp foran tidsbegrensede leaser; ellers velges
seneste monotone frist, deretter seneste veggklokkefrist. Ved like frister velges
laveste kommando-ID. Hash-/dictionaryrekkefølge avgjør dermed ikke valget.

`isCurrent`, `complete`, `reset`, generasjonen, identitets-/scopekontroller og
SET-leasens femsekundersgrense er uendret. Permit er fortsatt bundet til akkurat
den valgte leasen. Fullføring av denne leasen ugyldiggjør permit også når andre
leaser lever; reset ugyldiggjør gammelt permit selv ved gjenbruk av kommando-ID.
Ingen ny rettighet eller retry er lagt til.

## Testbevis

Alle lokale kjøringer gikk som skriptjobber i bane b, med eksisterende bounded
SwiftPM-runner og uendret kapasitetsvakt. Bevis ligger under
`HAVEN-Deploy/_handoff/KORR-UT/p6/`.

| Kontroll | Resultat | Bevis |
| --- | --- | --- |
| Rød først, produktkode fra 36959ae | 8 tester; exit 1. FEED/SET-regresjonen og likhetstesten røde; 236 assertion-feil | `red.log`, `red-result.txt` |
| Rettet autorisasjon | 8 tester, 0 feil, exit 0 | `green.log`, `green-result.txt` |
| Mutasjon tilbake til first(where:) | FEED/SET-regresjonen rød; exit 1, 241 assertion-feil. Rettet kilde gjenopprettet og bytekontrollert | `mutation.log`, `mutation-result.txt` |
| Fokusert bane b | 143 tester, 0 feil, exit 0 | `focused.log`, `focused-result.txt` |
| Full CP-byggport | build --build-tests --disable-automatic-resolution, exit 0 | `full-build.log` |
| Full CP-testport | test --disable-automatic-resolution --jobs 2, exit 0; 1642 beståtte, 5 hoppet over, 0 feil | `full.log`, `full-result.txt`, `full-counts.json` |
| Testet og committet innhold | Begge endrede filers SHA-256 uendret gjennom fullport, commit og push | `tested-files.json` |

FEED/SET-prøven bruker 256 forskjellige kommando-ID-par for samme scope. Hvert
permit må velge FEED, overleve SET-complete og bli ugyldig ved FEED-complete.
Andre nye prøver krever seneste frist blant 32 SET-leaser, utelukker fullførte og
utløpte leaser og kontrollerer deterministisk likhet samt reset/generasjon.
Eksisterende testmetoder og assertions er beholdt.

Fullportens total er 1647 XCTest-utfall: p5-referansen var 1638 beståtte og 5
hoppet over; de fire nye testene gir nå 1642 beståtte og samme fem hoppet over.
Fullporten brukte samme bygg-/testkommandoer som tidligere grunnmurport, men
beholdt det låste arbeidstreet uten sletting. Commiten inneholder ønsket
`Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.

## CI på eksakt publisert hode

Samlet PR-status er kontrollert mot HODE: **5/5 SUCCESS**, inklusive de fire
CP-portene og upstream-sync. PR er fortsatt OPEN og kladd.
Bevis: `ci.json` og `push-ci-result.txt` i samme bevismappe.

- [Persisted Cell file bounds](https://github.com/Digipomps/CellProtocol/actions/runs/37855410752/job/113578275762): SUCCESS.
- [regression](https://github.com/Digipomps/CellProtocol/actions/runs/37855410903/job/113578275854): SUCCESS.
- [Dispatch PyCellProtocol upstream sync](https://github.com/Digipomps/CellProtocol/actions/runs/37855406443/job/113578263216): SUCCESS.
- [bounded synthetic runtime matrix](https://github.com/Digipomps/CellProtocol/actions/runs/37855410890/job/113578276143): SUCCESS.
- [Vapor identity vault strict storage](https://github.com/Digipomps/CellProtocol/actions/runs/37855411038/job/113578276508): SUCCESS.

Arbeidstreet er rent og låst. Ingen merge, tag, sletting eller endring av
diskvakten. Denne leveransen beviser CP-rettelsen og dens porter; den gjør ikke
krav på en ny live korrespondanserunde, deploy eller nye installerere.
