# Beslutning 08.10.2026 00:35Z: innmelding gjennom cellen og vedleggsrot ved oppstart

Skrevet av korrespondanse-tråden. Gjelder p2, k1 og s2. Grunnlag: FORMAALSSPEC C1–C3 (mottakeren gir agenten lenken og sender Kjetil koden; Kjetil får ett kort per forespørsel under «Trenger deg»), `handoff/BOLK-3-INTEGRASJON.md` (innmeldingskontrakten mangler) og s2s spørsmål i `_losen-queue/KOORDINERING.md` 00:22Z (vedleggsroten kan ikke bindes ved ubetjent oppstart).

## 1. Vedleggsroten ved oppstart (CellProtocol, p2)

Verten binder sin betrodde lagerrot gjennom et lokalt Swift-API som ikke finnes på wire, for eksempel `configureTrustedHostAttachmentStorage(root:)`. Det krever ikke at et medlem har bevist nøkkelen sin, og det starter opprydding av utløpte vedlegg med en gang. Det gir ingen medlemsrett og ingen nøkkel. `configureAttachmentStorage(root:requester:)` blir som den er. Test: kald omstart fra lagret tilstand uten at noe medlem kobler til, og et utløpt vedlegg forsvinner.

## 2. Innmelding gjennom relasjonscellen (CellProtocol, p2; klient k1; vert s2)

Verten videresender bare. Den slipper ikke inn noen og har ingen privat nøkkel.

| Operasjon | Hvem | Nyttelast | Svar |
|---|---|---|---|
| `join.request` (SET) | den inviterte, ikke medlem | eiersignert invitasjon (celle-UUID, invitasjons-ID, utløp høyst 7 døgn, engangs), den invitertes offentlige signerings- og X25519-nøkkel, nøkkelbevis (signatur over celle, invitasjon, nøkler, tidspunkt) | `requestID`, `status: pending` |
| `join.pending` (GET) | eieren, med nøkkelbevis | — | ventende forespørsler: `requestID`, invitasjons-ID, offentlige nøkler, mottatt-tid. Ingen navn. |
| `join.decide` (SET) | eieren, med nøkkelbevis | `requestID`, `approve` med ferskt eiersignert cellebundet `Contract`, eller `deny` | `status` |
| `join.result` (GET) | den inviterte, med nøkkelbevis for samme nøkkel som i forespørselen | `requestID` | `pending`, `approved` med `Contract`, `denied` eller `expired` |

Deretter `agreement.accept` som i dag. Flow på `haven.correspondence`: `join.requested` bare til eieren, `join.decided` bare til den som spurte. Invitasjonen kan brukes én gang; nummer to gir `invitation.used`. Utløpt invitasjon gir `invitation.expired`. Verten lagrer bare offentlige nøkler. Kortnavnet Kjetil gir lenken, lagres bare på Macen hans.

Koden på seks sifre: én offentlig hjelpefunksjon i CellProtocol, `CorrespondenceJoinCode.code(cellUUID:invitationID:signingPublicKey:agreementPublicKey:)`, = SHA-256 over de fire i fast rekkefølge, de første 4 byte som stort-endian heltall modulo 1 000 000, med ledende nuller. Begge klientene bruker den. En forespørsel med en annen nøkkel gir en annen kode.

Lenken inneholder vertsadressen, celle-UUID, publisher-navnet og den signerte invitasjonen. Den gir ikke medlemskap alene.

## 3. Hvem gjør hva

- **p2** (CellProtocol, PR #63): punkt 1 og 2 med tester og en formålsprøve med tre adskilte nøkkellagre, fullport, push, CI.
- **k1** (HavenAgentD): bygger klientsiden mot tabellen over (lenke, forespørsel, kode, kort under «Trenger deg», godkjenning med Touch ID, henting av avtalen). Pinner det PR #63-hodet p2 skyver.
- **s2** (CellScaffold): vertslaget videresender de fire operasjonene for ikke-medlemmer også (cellen avgjør), og binder vedleggsroten med API-et i punkt 1 ved oppstart.

## 4. Eierens nøkkelgrense i første pakke (tillegg 01:40Z, til k1)

Svar på `handoff/BOLK-3-NOKKELGRENSE.md`. Ingen ny provisioningprofil finnes, og bare Kjetil kan lage en. Første pakke venter ikke på den:

- Agentens MCP får bare de typede meldings- og vedleggsoperasjonene. Ingen rå signering, nøkkelbevis, vilkårlig keypath, `join.*`-administrasjon, `agreement.*` eller tilbakekall gjennom MCP. Prøve 2 og 3 i nøkkelgrensen skal være grønne.
- Lenke, godkjenning, fornyelse og tilbakekall gjøres bare i adminvinduet til HAVEN Agent. Dokumentet fryses, så kreves fersk `LAContext` (`deviceOwnerAuthentication`, Touch ID eller passord), så signeres nøyaktig det fryste dokumentet. Avbrutt eller feilet autentisering gir ingen signatur. Prøve 4, 5 og 6 skal være grønne.
- Nøkkelen ligger der den ligger i dag. Skriv i rapporten, under «Ikke vist», at en prosess som kjører som Kjetil kan lese den, og at dette lukkes med en egen nøkkelgruppe når profilen finnes. Ikke bruk en profil for en annen app.
- Spør ikke Kjetil om profilen i jobben; korrespondanse-tråden tar det med ham.

## §5 Kildemoduser i første pakke (lagt til 2026-10-08 18:25Z, korrespondanse-tråden)

Grunnlag: den G2-godkjente formålsspesifikasjonen (`FORMAALSSPEC.md`, S1 i §6 og A18 i §0) sier at første pakke sender vedlegg **bare som kopi**. «Referanse» og «hent ved behov» er uttrykkelig utenfor første pakke. CP på PR #63-hodet `36959ae` håndhever dette (`attachments.probe` kaster unavailable; `attachments.prepare` krever `sourceID == nil`).

Beslutning: HavenAgentD-testen `sourceModesAreObservedAndNeverOfferTransfer` skal ikke slettes eller hoppes over. Den skrives om til å prøve den godkjente kontrakten: at en registrert sourceID og en kildeprobe gir et **eksplisitt, typet avslag** gjennom MCP (ikke stille suksess, ikke krasj), og at kopi fortsatt virker etterpå. Testen skal vise til S1 i en kommentar. Dette svekker ingen påstand om det som leveres; det endrer en forventning som var skrevet mot et omfang Kjetil ikke godkjente for første pakke.

De andre funnene fra k5 er ikke dekket av denne beslutningen og skal løses som rettinger: snapshot-fixturen rebinder den betrodde vedleggsroten etter §1; Resolver-verdien i `legacyAgreementCannotUseAttachmentActions` klassifiseres og må være et avslag; `.closed` i broprøven feilsøkes til årsak.
