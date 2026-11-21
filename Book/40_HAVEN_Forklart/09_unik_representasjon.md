# Unik representasjon i HAVEN: hva finnes, og hva er åpent

Status: batch 2 · utkast, ikke godkjent · ankre kontrollert ordrett 2026-11-20 · godkjenner: Kjetil (per batch)

Dette kapittelet er for deg som skal forske på *unik representasjon*: å vise at en entitet (en person, en organisasjon) er representert bare én gang i en gruppe, for eksempel når gruppen stemmer. Kapittelet forteller hva HAVEN har å bygge på i dag, og hva som ikke finnes ennå.

Merkene betyr det samme som i resten av «HAVEN forklart»: **[kan sies]**, **[med forbehold]** og **[ikke ennå]**.

## Hva er en identitet i HAVEN?

**[kan sies] HF-09-01.** En identitet er en digital, operativ representasjon som brukes i beskyttede handlinger. Den har en UUID og en offentlig signeringsnøkkel. Det finnes ingen global identifikator og ingen automatisk kobling mellom domener.

*Begrensning:* Dette er modellen i spesifikasjonen. Hvor sterkt den holder, avhenger av hvilket hvelv, bevis og hvilken policy en tjeneste bruker.

Kilder:
- `Book/03_Identity_Model.md` linje 34: «Public signing key and optional key-agreement key»
- `Book/03_Identity_Model.md` linje 12: «There is no global identifier and no automatic cross-domain linkage.»

## Kan én person ha flere identiteter?

**[kan sies] HF-09-02.** Ja. Én entitet kan ha mange identiteter i ulike domener. Det er et bevisst valg for personvern: aktiviteten din i ett domene skal ikke uten videre kunne kobles til et annet.

Kilder:
- `Book/03_Identity_Model.md` linje 39: «An Entity may have many Identities across»

## Hvordan knyttes to identiteter til samme entitet?

**[kan sies] HF-09-03.** Bare gjennom en signert seremoni (IdentityLink). Å legge til en ny nøkkel eller slå sammen to identiteter som ikke er koblet, krever den seremonien. Ingen kobling skjer av seg selv.

*Begrensning:* Seremonien kobler identiteter til én entitet. Den beviser ikke at entiteten bare har *én* slik koblet gruppe identiteter.

Kilder:
- `Book/32_Cross_Scaffold_Entity_Enrollment.md` linje 51: «unlinked identities still requires the signed IdentityLink ceremony»

## Hva gir tilgang?

**[kan sies] HF-09-04.** Tilgang gis bare eksplisitt, gjennom avtaler (Agreement), kontrakter og grants, eller et annet verifisert eierbevis. Ingenting gis implisitt.

Kilder:
- `Book/04_Agreements_Contracts.md` linje 11: «Nothing in HAVEN is implicit: all authority must be granted through a»

## Hvordan telles stemmer i dag?

**[med forbehold] HF-09-05.** Avstemningene i HAVEN (live-interaksjon og konferanser) teller én stemme per identitetsnøkkel. Stemmen lagres per kombinasjon av identitetens UUID og nøkkelens fingeravtrykk.

*Forbehold:* Det er én stemme per **identitet**, ikke per **person**. En person med flere identiteter kan stemme flere ganger. Dette er svakheten unik representasjon handler om.

Kilder:
- `CellScaffold/Sources/App/Cells/LiveInteraction/LiveInteractionCell.swift` linje 1711: «"\(requester.uuid)|\(fingerprint(requester))"» (proveniens, ikke offentlig Book-kilde)

## Finnes det bevis for at en entitet bare er med én gang?

**[ikke ennå] HF-09-06.** Nei. HAVEN har i dag ingen kode for motstand mot falske identiteter (sybil), engangsmerker (nullifiers) eller anonyme medlemsbevis. Det er kjernen i oppgaven, og den må bygges.

*Skal ikke sies:* «HAVEN garanterer én person, én stemme.» · «HAVEN har anonym og etterprøvbar stemmegivning.»

Kilder:
- `CellProtocol/Sources/CellApple/EntityRadar/ScannerAdmission.swift` linje 7: «a Sybil can exhaust the global cap» (koden kjenner problemet, men løser det ikke)

## Hvor du kan begynne

- `Book/03_Identity_Model.md`: identitet, domener og nøkler.
- `Book/04_Agreements_Contracts.md`: avtaler og grants, grunnlaget for samtykke og tilgang.
- `Book/32_Cross_Scaffold_Entity_Enrollment.md`: hvordan en entitet meldes inn på tvers av noder, og IdentityLink.
- `Book/37_EntityData.md`: hva en entitet eier, og hvordan data deles.
- `Book/31_Developer_Identity_Pack.md` og `Book/36_Agent_Trust_Package.md`: konkrete eksempler på identitets- og tillitspakker.
- Kode i det offentlige CellProtocol-repoet: `Sources/CellBase/Identity`, `Sources/CellBase/VerifiableCredentials`, `Sources/CellBase/Agreement`.
