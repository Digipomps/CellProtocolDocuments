# Overdragelse av vedleggskopi — status 29.09.2026

**Ikke implementert.** Overdragelse er uttrykkelig autorisert og inngår i
kopimodus i denne runden. Det er ingen gjenværende avklaring om oppgavens
omfang. Arbeidet stoppet ved røde baseline-tester etter instruksen «Rødt: stopp».

## Mål

Et eget skritt skal overdra en fullt hentet vedleggskopi til mottakeren,
fjerne avsenders vedleggskopi og gjøre mottakerfilen uavhengig av meldingens
retensjon. Eiervalg eller uttrykkelig valgt policy og etterprøvbar historikk
skal styre dette. Skrittet skal bare finnes i `copy`.

## Påstander og belegg

- Forrige jobb leverte ingen vedleggskode. Dette er kontrollert mot rapporten
  fra dokumentcommit `6ff6ecc` og rene kodegrener ved oppstart.
- Denne runden fikk CellProtocol-bygget grønt, `exit=0`, på uendret `81601a6`.
- Full `swift test` ga `exit=1`: 1297 tester rapportert, 9 hoppet over, 3 feil
  i `AppleIdentityVaultKeyStorageTests` (`EPERM` og `-25291`).
- Ingen vedleggs- eller overdragelseskode er skrevet; målet er ikke oppnådd.
- 22 eksisterende strømkryptotester besto. De beviser ikke overdragelse.

Kommandoer, individuelle baseline-feil og rålogger finnes i
[Vedlegg, implementasjonsforsøk 2](VEDLEGG_IMPL_2_2026-09-29.md).

## Skrittets navn og tekst — krav til neste implementasjon

Ingen nytt verktøy eller Cell-keypath er registrert. Foreslått eierhandling
videreføres som **«Overdra vedleggskopien til mottakeren»**; et mulig separat
MCP-navn er `correspondence_transfer_attachment_ownership`. Dette navnet er
**ikke implementert**. Handlingen må ha en beskrivelse av at den ikke gir
installasjons-, kjøre- eller videresendingsrettigheter.

Teksten eieren skal få se sammen med aktuell fil og mottaker:

> Mottakeren har hentet hele vedlegget. Når du overdrar kopien, blir filen
> mottakerens, og vedleggskopien hos deg slettes. Du kan ikke lenger trekke
> filen tilbake. Den slettes ikke hos mottakeren når meldingen utløper.
> Vil du overdra vedleggskopien til mottakeren?

Valg: **«Overdra kopien»** / **«Behold som vedlegg»**.

Dette er leveransetekst, ikke en kjørende dialog. Uten en tidligere uttrykkelig
valgt policy skal overdragelse kreve det informerte valget i den konkrete
sendingen. En policy skal ikke skjule konsekvensen ved opprettelse, og skal ikke
omgå kravet om at mottakeren har fullført og verifisert strømmen.

## Testresultater, enkeltvis

| Test | Resultat |
| --- | --- |
| Sletting/overdragelse avvises før mottakeren har hentet | Ikke implementert / ikke kjørt |
| Overdratt vedlegg overlever meldingens utløp | Ikke implementert / ikke kjørt |
| Ikke-overdratt vedlegg dør med meldingen | Ikke implementert / ikke kjørt |
| Skrittet tilbys ikke i `reference` og `fetchOnDemand` | Ikke implementert / ikke kjørt |
| Eier uten policy får konsekvensen forelagt før handling | Ikke implementert / ikke kjørt |
| En uttrykkelig valgt policy kan sette standardsvaret | Ikke implementert / ikke kjørt |
| Hvilke vedlegg som er overdratt, og når, kan leses etterpå | Ikke implementert / ikke kjørt |

Ingen eierskapsovergang, sletting eller faktisk filhenting er utført.

## Hva som ble videreført

Samme eksisterende gren i alle tre repoer:
`codex/correspondence-attachments-20260929`. HavenAgentD står på `ba14895`,
CellProtocol på `81601a6`; ingen kodecommit. Rapport og belegg committes i
`_worktrees/documents-attachments`, videreført fra `6ff6ecc`. CellProtocol måtte
få en ny arbeidsmappe på samme gren fordi den gamle mappen manglet Git-metadata;
den gamle mappen er bevart.

Videreført: eierbeslutningen, `FORMAALSSPEC.md`, overdragelsesprompten i
`_losen-queue/done/`, den eksisterende strømkryptoen, konvoluttklienten og
forrige rapports kildefunn. Den gamle overdragelsesrapportens spørsmål om
omfang er løst av denne bestillingen. Den rapporten er bevart som
[historisk status](VEDLEGG_IMPL_2_2026-09-29_evidence/overdragelse-forrige-status.md).

Alt implementasjonsarbeid og alle nye tester gjenstår. Ingen push eller merge.
