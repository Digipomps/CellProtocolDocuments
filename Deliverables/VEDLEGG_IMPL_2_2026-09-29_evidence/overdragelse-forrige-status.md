# Overdragelse av vedleggskopi — manglende grunnimplementasjon

Rapportnavnet følger bestillingen. Kildekontrollen ble utført 2026-09-28.

**Status: ikke implementert.** Jobben `vedlegg-impl-20260929` leverte en
stopprapport, ikke en vedleggsimplementasjon. Dette er kontrollert mot både
rapporten og de eksisterende arbeidsmappene på den bestilte grenen.
Overdragelsen kan derfor ikke legges til som en utvidelse av den leveransen.

## Mål

Utvid den eksisterende vedleggsflyten med et eget, observerbart skritt som
overdrar en hentet kopi til mottakeren og fjerner avsenders vedleggskopi.
Skrittet skal bare tilbys i `copy`, kreve fullført mottakerhenting, frigjøre
mottakerens fil fra meldingens retensjon og tilbakekall, og kreve et informert
eiervalg per sending eller en policy eieren uttrykkelig har valgt på forhånd.

Beslutningen er
[«Avklart 29.09»](/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_vedlegg-korrespondanse_2026-09-28/BESLUTNINGER_KJETIL_2026-09-28.md).
Bestillingen opphever det tidligere forbudet mot sletting av avsenders
vedleggskopi. Det forbudet er **ikke** stoppgrunnen her.

## Påstander og belegg

| Påstand | Belegg | Begrensning |
| --- | --- | --- |
| Forrige jobb stoppet før implementasjon. | [Forrige rapport](VEDLEGG_IMPL_2026-09-29.md), status og avsnittet «Bygg og stoppgrunn». Dokumentcommit `6ff6ecc`. | Rapporten er en stopprapport; den er ikke belegg for en fungerende vedleggsflyt. |
| Det finnes ingen senere endringer i de to aktuelle kodearbeidsmappene. | Ren `git status --short`; CellProtocol HEAD `81601a6f835252aba7e99d43786fb5d67227c245`, HavenAgentD HEAD `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98`. Begge samsvarer med utgangspunktene i forrige rapport. | Kontrollert lokalt; ingen remote-oppdatering eller påstand om andre grener. |
| Den eksisterende korrespondansecellen har ingen vedleggsflyt å utvide. | `Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift`: meldingslageret er `storedEnvelopesByMessageID`; autoriserte operasjoner omfatter `inbox`, `readMessage`, `sendMessage`, `ackMessage` og `audience.inviteIdentities`. Ingen treff på `attachment`, `Attachment` eller `fetchOnDemand` i korrespondansekilden eller dens tester. | Gjelder den bestilte CellProtocol-grenen. |
| MCP-klienten har ikke fått vedleggsverktøy. | `Sources/HavenCorrespondenceMCP/CorrespondenceMCPService.swift`: de fire operasjonsverktøyene er fortsatt `correspondence_list_inbox`, `correspondence_read_message`, `correspondence_send_message` og `correspondence_ack_message`. | Profil-/kontraktressursene er ikke vedleggsverktøy. |
| En gjenbrukbar kryptografisk strømbyggekloss finnes. | `Sources/CellBase/Crypto/AttachmentStreamV1.swift` og `Tests/CellBaseTests/AttachmentStreamV1Tests.swift` finnes i CellProtocol-grenen. | Dette beviser ikke integrert mottakerhenting, lagring, retensjon eller overdragelse. Testene er ikke kjørt i denne runden. |
| Denne runden endrer ingen kode eller eierskap. | Bare denne rapporten er opprettet i dokumentarbeidsmappen og kopiert til bestilt rapportsti. | Ingen funksjon er levert, og ingen av akseptansetestenes utfall er kjent. |

## Skrittets navn og tekst — forslag, ikke implementert API

Navn i eierflaten: **«Overdra vedleggskopien til mottakeren»**.
Foreslått navn for den separate handlingen: `transferCopyOwnership`.
Dette er ikke et `delete`-flagg på sending. Navnet er ikke registrert som
Cell-keypath eller MCP-verktøy i denne runden.

Teksten eieren skal få se ved valget:

> Mottakeren har hentet hele vedlegget. Når du overdrar kopien, blir filen
> mottakerens, og vedleggskopien hos deg slettes. Du kan ikke lenger trekke
> filen tilbake. Den slettes ikke hos mottakeren når meldingen utløper.
> Vil du overdra vedleggskopien til mottakeren?

Handlingsvalg: **«Overdra kopien»** / **«Behold som vedlegg»**.
Den aktuelle filen og mottakeren må identifiseres ved teksten. Tekstens første
setning kan først brukes når autentisert, fullført mottakerhenting faktisk
er bekreftet; en meldingskvittering alene er ikke slikt belegg.

Foreslått tekst ved eksplisitt valg av automatisk policy:

> Overdra framtidige vedleggskopier automatisk etter at mottakeren har hentet
> hele filen. Da slettes vedleggskopien hos deg, og filen blir mottakerens.
> Du kan ikke trekke den tilbake, og den slettes ikke hos mottakeren når
> meldingen utløper. Dette gjelder bare kopimodus.

Ingen policy skal være valgt som standard. Uten en policy eieren har satt,
skal overdragelse kreve at konsekvensen legges fram og at eieren velger
«Overdra kopien». Et informert policyvalg kan besvare spørsmålet for senere
sendinger, men kan ikke oppheve kravet om fullført mottakerhenting.

En implementasjon må bevare en lesbar overdragelsespost med vedleggs-ID,
meldings-ID, avtale-ID, avsender, mottaker, tidspunkt og beslutningsgrunnlag
(eiervalg eller valgt policy). Posten må kunne leses etter meldingsutløp.
Ingen slik post, lagring eller leseoperasjon er implementert her.

## Testresultater enkeltvis

| Bestilt test | Resultat i denne runden | Manglende forutsetning |
| --- | --- | --- |
| Sletting hos avsender avvises før mottaker har hentet. | Ikke implementert; ikke kjørt. | Vedleggslager, bekreftet henting og separat overdragelseshandling. |
| Et overdratt vedlegg overlever meldingens utløp. | Ikke implementert; ikke kjørt. | Mottakerlagring og implementert overgang i eierskap/retensjon. |
| Et ikke-overdratt vedlegg dør med meldingen. | Ikke implementert; ikke kjørt. | Grunnimplementasjon av vedleggsretensjon. Eksisterende meldingsutløp beviser ikke dette. |
| Skrittet tilbys ikke i `reference` og `fetchOnDemand`. | Ikke implementert; ikke kjørt. | Implementert modusvalg og handlingsflate. |
| En eier uten policy får overdragelsen forelagt før den skjer. | Ikke implementert; ikke kjørt. | Eierflate, beslutningsflyt og policyhåndtering. Tekstforslaget ovenfor er ikke en funksjonstest. |
| Overdragelsen kan leses av i ettertid. | Ikke implementert; ikke kjørt. | Varig overdragelsespost og autorisert leseoperasjon. |

Ingen nye tester er skrevet. Eksisterende tester er ikke kjørt på nytt.

## Bygg

Ingen bygg- eller testkommando er startet i denne runden. Et nytt bygg ville
ikke etablere den manglende grunnimplementasjonen.

**Historisk resultat fra forrige jobb:** `swift build --disable-sandbox`
ga `exit=1` ved pakkemanifestet, før kildekodekompilering. Sandkassen nektet
skriving til `/Users/kjetil/.cache/clang/ModuleCache`. Se
[råloggen fra forrige jobb](VEDLEGG_IMPL_2026-09-29_evidence/cellprotocol-baseline-build.log).
Det var ikke `exit=64`, ikke en kjørt funksjonstest, og er ikke et nytt
byggresultat fra denne runden. Feilen er ikke utbedret eller prøvd på nytt her.

## Hva som ble videreført fra forrige jobb

De samme arbeidsmappene og grenene er brukt; ingenting er startet på nytt:

| Repository | Arbeidsmappe under HAVEN | Gren | HEAD ved kontroll |
| --- | --- | --- | --- |
| CellProtocol | `_worktrees/cellprotocol-attachments` | `codex/correspondence-attachments-20260929` | `81601a6` |
| HavenAgentD | `_worktrees/havenagentd-attachments` | `codex/correspondence-attachments-20260929` | `ba14895` |
| CellProtocolDocuments | `_worktrees/documents-attachments` | `codex/correspondence-attachments-20260929` | `6ff6ecc` |

Videreført underlag: forrige rapport, bygglogg, kodeutgangspunkter og den
eksisterende `AttachmentStreamV1`. Ingen ny vedleggskode fra forrige jobb
fantes å bygge videre på. Brukerens eksisterende endringer i andre
arbeidsmapper er urørt. Ingen commit, push eller merge er utført i denne runden.

Rapporten ligger på dokumentgrenens arbeidsmappe og som identisk kopi på
`CellProtocolDocuments/Deliverables/VEDLEGG_OVERDRAGELSE_2026-09-29.md`.

## Nødvendig avklaring før implementasjon

Oppgi eventuell annen commit/arbeidsmappe som inneholder den leverte
vedleggsflyten, eller avklar at også den manglende grunnimplementasjonen fra
`vedlegg-impl-20260929` skal fullføres i denne jobben. Spørsmålet er stilt til
eieren. Det gjelder manglende kode og oppgavens omfang, ikke den allerede
avklarte tillatelsen til overdragelse i kopimodus.

Instruksen «bygg videre på det den jobben leverte; ikke start på nytt» er
grunnen til at det ikke er bygget en ny, frittstående vedleggsimplementasjon
her. Målet er fortsatt uoppnådd.
