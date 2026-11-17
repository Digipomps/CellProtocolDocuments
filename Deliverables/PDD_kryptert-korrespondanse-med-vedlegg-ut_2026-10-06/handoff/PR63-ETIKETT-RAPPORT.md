HODE: fe799b6003bd379a3014a81b345b1eeb63c218f8
STATUS: LEVERT

# PR #63 — usignerte identitetsfelt

Jobb: p7-korr-usignert-etikett-20261009. Utgangspunkt:
7ebb4f5f76cdcda39a2abc2e42c8743a62a703b0. Gren:
`codex/korr-relasjonscelle-20261007`.

## Rettelsen

Kontraktens issuer og subject bygges om til offentlige øyeblikksbilder før
`agreement.accept` installerer kontrakt og medlem og før `join.decide` lagrer
kontrakten i innmeldingsvedtaket. `displayName` er UUID, `properties` er tom og
`homeVaultReference` er fjernet. Offentlige nøkkelmaterialer beholdes; eksisterende
kontroller mot signert signatar, eier og presenterende identitet gjelder fortsatt.

`inviteIdentities` bruker kanoniske signatarer før avtalen signeres. Lokal
`addAgreement` bruker den nye `GeneralCell.localContractIdentityDescriptor`-hooken
for avtalens eier, signatarer og medlem, og for kontraktens offentlige issuer.
Standardimplementasjonen beholder andre cellers oppførsel; bare CorrespondenceCell
overstyrer policyen. Den opprinnelige levende identiteten beviser nøkkelkontroll
og signerer. Avtalen omskrives aldri etter signering. Identifiserende metadata
inne i en eksternt signert avtale avvises før installasjon.

Ingen nye rettigheter eller endret signaturformat. Eksisterende binding til celle,
domene, issuer, subject, nøkkelbevis, utløp, tilbakekall og grants beholdes.

## Testbevis

| Kontroll | Resultat |
| --- | --- |
| Rød på 7ebb4f5: endret usignert subject/issuer-metadata etter gyldig eiersignatur | Akseptert, men koding kastet `identifyingMetadataNotAllowed` |
| Rød på 7ebb4f5: invitasjon av vault-identitet med ekte navn | Invitert, men koding kastet `identifyingMetadataNotAllowed` |
| Korrigerte regresjoner: ekstern aksept, vault-invitasjon og lokal avtale | 3 bestått, 0 feil; koding, gjenoppretting og medlemsadgang verifisert |
| Mutasjon: fjern `snapshot.displayName = snapshot.uuid` | Alle tre regresjoner røde; rettelsen gjenopprettet byte for byte |
| Fokusert bane b, med join-ledger og endret signert avtale | 148 bestått, 0 feil |
| Full CP-port, bane c | 1 647 bestått, 5 hoppet over, 0 feil; referansen var 1 642 bestått |
| CI på eksakt publisert hode | 5/5 SUCCESS; PR #63 fortsatt OPEN |

Fem nye tester dekker ekstern aksept, navngitt vault-invitasjon, lokal avtale,
kanonisering før join-ledger-lagring og avvisning av endret signert avtale.
Gjenopprettede kontrakter verifiserer fortsatt kryptografisk signatur.

Commit inneholder:
`Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.

Bevis ligger relativt HAVEN-roten i `HAVEN-Deploy/_handoff/KORR-UT/p7/`:
`red.log`, `green.log`, `mutation.log`, `focused.log`, `full-build.log`, `full.log`,
`full-counts.json`, `tested-files.json`, `ci.json` og `watch-ci-result.txt`. Rå bygglogger er ikke gjengitt her.

## Avgrensning

Ingen merge, deploy, release-tag eller nye installerere i p7. Disse tilhører
korrespondanse-trådens videre løp etter PR #63. Ingen endring av diskvakten eller
manuell sletting. Den pålagte bundne runneren brukte sin eksisterende cachepolicy.

## Læringsfangst

L-2026-10-09-correspondence-admission-must-canonicalize er anvendt og synkronisert
til `cellprotocol-identity-capability-security`. Kanonen er
`CellScaffold/.claude/skills/cellprotocol-identity-capability-security/SKILL.md`.
Den globale `haven_learn.py check --strict` er fortsatt rød med 7 eldre åpne
poster og 17 eldre ikke-distribuerte poster fra andre økter; p7-posten er ferdig.

## CI-kvittering

- [Persisted Cell file bounds](https://github.com/Digipomps/CellProtocol/actions/runs/37895236246/job/113704975746): SUCCESS.
- [regression](https://github.com/Digipomps/CellProtocol/actions/runs/37895236341/job/113704975847): SUCCESS.
- [Dispatch PyCellProtocol upstream sync](https://github.com/Digipomps/CellProtocol/actions/runs/37895234543/job/113704971925): SUCCESS.
- [bounded synthetic runtime matrix](https://github.com/Digipomps/CellProtocol/actions/runs/37895236297/job/113704975591): SUCCESS.
- [Vapor identity vault strict storage](https://github.com/Digipomps/CellProtocol/actions/runs/37895236350/job/113704975795): SUCCESS.

Push er verifisert mot PR #63s eksakte headRefOid. De fem committed-filene
samsvarer med SHA-256-manifestet fra den grønne fullporten. Arbeidstreet er rent.
Den første overvåkeren mistet nettforbindelsen; den samme CI-kjøringen ble
fulgt videre uten ny workflow-dispatch eller rerun.
