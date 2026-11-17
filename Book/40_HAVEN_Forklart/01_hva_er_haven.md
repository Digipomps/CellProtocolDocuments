# Hva er HAVEN?

Status: batch 1 · godkjent av Kjetil 2026-10-16 · kildegrunnlag: snapshot 2026-10-07, ankre kontrollert ordrett 2026-10-15 · godkjenner: Kjetil (per batch)

## Hva er HAVEN, kort fortalt?

**[kan sies] HF-01-01.** HAVEN er et forslag til en åpen protokoll der hver digital tjeneste skal oppgi et tydelig formål, be om minst mulig data, gi en kvittering for det den gjorde og kunne trekkes tilbake for framtidige handlinger. Det finnes ingen globale poengsummer på personer.

*Begrensning:* Dette er designreglene. At en bestemt tjeneste faktisk følger dem, må vises for den tjenesten.

Kilder:
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 16: «declare an explicit purpose; request minimal data; issue a receipt for what it did; remain revocable for future actions (revocation does not undo completed actions). There are no global personal scores»

## Hva prøver HAVEN å finne ut?

**[kan sies] HF-01-02.** Arbeidet er formulert som et spørsmål, ikke et løfte: Vi undersøker om CellProtocol kan gi et etterprøvbart og personvernvennlig grunnlag for å gi mer verdi tilbake til enkeltpersoner og fellesskap. Verdifordeling er en forsknings- og pilotretning, ikke en ferdig økonomisk mekanisme.

*Begrensning:* Om dette lykkes, er ikke vist (se «Hvor modent er HAVEN?»).

Kilder:
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 12: «We are investigating whether CellProtocol can provide an auditable, privacy-preserving foundation for returning more value to individuals and commons.»
- `DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` linje 37: «Value redistribution er en forsknings- og pilotretning, ikke en ferdig økonomisk mekanisme.»

## Hva er CellProtocol?

**[kan sies] HF-01-03.** CellProtocol er den tekniske kjernen i HAVEN: en liten modell der små, adskilte enheter (celler) har eksplisitt tilstand, sender hendelser, styrer tilgang eksplisitt og skal kunne etterprøves.

*Begrensning:* Determinisme, avspilling, etterprøvbarhet og personvern er mål og betingede egenskaper, ikke garantier for hver celle i dag (HF-01-04).

Kilder:
- `Book/01_CellProtocol_Core.md` linje 19: «CellProtocol is a minimal, privacy-first model intended to make deterministic»

## Er alt i HAVEN etterprøvbart og privat?

**[kan sies] HF-01-04.** Nei, ikke automatisk. Book sier selv at determinisme, avspilling, etterprøvbarhet og personvern er mål og betingede egenskaper. En del av systemet kan bare påberope seg dem når den aktuelle veien er bygget og testet.

Kilder:
- `Book/01_CellProtocol_Core.md` linje 10: «and transport-independent semantics are goals and conditional properties,»

## Har HAVEN en felles ID for hver person?

**[med forbehold] HF-01-05.** Nei. Identitet i HAVEN er avgrenset til ett domene, og det finnes ingen global identifikator og ingen automatisk kobling på tvers av domener.

*Forbehold:* Dette er en designregel. Hvis en tjeneste gjenbruker samme nøkkel, ID eller sporbare metadata på tvers av domener, kan de likevel kobles. Typesystemet kan ikke hindre det.

Kilder:
- `Book/03_Identity_Model.md` linje 12: «- There is no global identifier and no automatic cross-domain linkage.»
- `Book/03_Identity_Model.md` linje 52: «Reusing a UUID, signing key, or correlatable metadata across domains can still»

## Er HAVEN et digitalt fellesgode (DPG) eller offentlig infrastruktur?

**[kan sies] HF-01-06.** Nei. HAVEN er ikke registrert som digitalt fellesgode og er ikke en implementasjon av offentlig digital infrastruktur. Det er et spesifisert og delvis prototypet protokollforslag.

Kilder:
- `Kallimachos/Verdifordeling/Sachs_2026-09-07/TILLITSPAKKE_v1.md` linje 18: «not a DPI implementation and not a registered DPG. It is a specified and partially prototyped protocol proposal»

## Gjør HAVEN ting lettere enn alternativene?

**[ikke ennå] HF-01-07.** Det kan vi ikke si ennå. En uavhengig opponentvurdering fant at «HAVEN gjør det lettere» ikke er etablert som faktum for noen av forskningsspørsmålene som ble vurdert.

*Skal ikke sies:* «HAVEN gjør det lettere.» · «HAVEN er bedre enn alternativene.»

Kilder:
- `Kallimachos/Claude outputs/B3_OPPONENT.md` linje 123: ««HAVEN gjør det lettere» **ikke etablert som faktum for noe dossier**»
