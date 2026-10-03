# Vedlegg i korrespondansen — implementasjonsforsøk 2

Dato: 2026-09-29. **Ikke implementert. Stoppet ved røde tester på uendret kode,
etter grønt bygg.** Eierens instruks «Rødt: stopp» er fulgt. Ingen Swift-kode,
avtale, verktøy eller vedleggsrettighet er endret. Overdragelse er del av det
autoriserte oppdraget; det er ikke en åpen avklaring eller grunnen til stoppen.

## Mål

Bygge avtalebundne vedlegg gjennom eksisterende `AttachmentStreamV1` og
korrespondansekonvolutten: automatisk valg av `reference`, `fetchOnDemand` eller
`copy`, avsenderlagring, metadata uten hash, meldingsstyrt retensjon og signert
melding-/avtalebinding. Kopimodus skal i tillegg ha en uttrykkelig overdragelse
etter verifisert mottakerhenting, med informert eiervalg eller valgt policy.

Målene er **ikke oppnådd**. Leveranse av installerpakken og budsjettet er heller
ikke prøvd. Det er ikke brukt operative korrespondanseprofiler eller lest,
sendt eller kvittert for virkelige meldinger.

## Påstander og belegg

| Påstand | Målt belegg | Begrensning |
| --- | --- | --- |
| Nett og skrivbar modulcache fungerte i denne kjøringen. | SwiftPM hentet avhengigheter og CellProtocol-bygget fullførte med `exit=0`. | Gjelder dette bygget, ikke alle nødvendige tester eller HavenAgentD. |
| Uendret grunnlag har røde tester i denne prosessen. | `AppleIdentityVaultKeyStorageTests` feilet med `EPERM` og `-25291`. | Feilene oppsto før vedleggsimplementasjon; ingen påstand om at nye vedleggstester feiler. |
| Den eksisterende strømkryptoen besto sine tester. | 22 av 22 `AttachmentStreamV1Tests` besto i samme testkjøring. | Beviser ikke integrert henting, retensjon, binding til melding/avtale eller overdragelse. |
| Kodegrenene er uendret. | Ren status i de to anvendte kode-worktreene. | Dokumenter, rålogger og læringsfangst er endret separat. |
| Ingen kode er pushet eller slått sammen til main. | Kun lokal dokumentcommit på oppdragsgrenen. | Dette er en stopprapport, ikke en funksjonsleveranse. |

## Bygg, tester og faktisk stoppgrunn

Utgangspunkt: CellProtocol `81601a6f835252aba7e99d43786fb5d67227c245`, samme
lokale `origin/main` og gren som forrige forsøk. Remote ble ikke oppdatert.
Swift: `Apple Swift version 6.4 (swiftlang-6.4.0.34.1 clang-2100.3.34.1)`.

Kjørt fra `_worktrees/cellprotocol-attachments-impl2`:

```sh
Scripts/haven-swiftpm.sh \
  --cache-root /private/tmp/haven-attachments-impl2-swiftpm \
  --cache-key correspondence-attachments-impl2 --wait-seconds 55 \
  -- build --disable-sandbox

Scripts/haven-swiftpm.sh \
  --cache-root /private/tmp/haven-attachments-impl2-swiftpm \
  --cache-key correspondence-attachments-impl2 --wait-seconds 55 \
  -- test --disable-sandbox
```

Wrapperen setter både `CLANG_MODULE_CACHE_PATH` og
`SWIFTPM_MODULECACHE_OVERRIDE` til sin skrivbare cache. Hver kommando ble startet
én gang. **Ingen `exit=64` oppsto**, så ingen vent/omprøving for cachevakten var
nødvendig. Ingen omprøving, testutfiltrering eller svekkelse av nøkkellagringen
ble gjort etter rødt.

- Build: **exit 0**, fullført. [Rålogg](VEDLEGG_IMPL_2_2026-09-29_evidence/cellprotocol-baseline-build.log).
- Test: **exit 1**, fullført: 1297 tester rapportert, 9 hoppet over og 3 feil. [Rålogg](VEDLEGG_IMPL_2_2026-09-29_evidence/cellprotocol-baseline-test.log).
- HavenAgentD build/test: ikke startet etter stopp.

De tre faktiske feilene:

| Eksisterende test | Resultat |
| --- | --- |
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns` | Feil: `NSOSStatusErrorDomain Code=100001`, `failed to generate CDSA key`, `EPERM: Operation not permitted`. |
| `AppleIdentityVaultKeyStorageTests.testLegacyEmbeddedPrivateKeyStillSigns` | Samme feil ved opprettelse av privat nøkkel. |
| `AppleIdentityVaultKeyStorageTests.testScopedSecretDataStaysStableInUnsignedTestHost` | Feil: `unhandledError(status: -25291)`. |

Koden i disse testene bruker Apples nøkkellagring. Andre tester i samme klasse
hopper eksplisitt over utilgjengelig nøkkellagring; de tre ovenfor feiler.
Observasjonen er at denne prosessen mangler nødvendig tilgang til
sikkerhetstjenestene. At en annen testvert vil bestå er **ikke verifisert**.
`--disable-sandbox` opphever ikke den omsluttende prosessens begrensninger.

## Verktøyflaten slik den er

Ingen nye verktøy er levert. `CorrespondenceMCPService` har fortsatt bare
`correspondence_list_inbox`, `correspondence_read_message`,
`correspondence_send_message` og `correspondence_ack_message`.
`send_message` har intet vedleggsargument. Det finnes verken metadata-/henteverktøy
for vedlegg eller et overdragelsesverktøy. Forslagene fra forrige rapport er
fortsatt forslag, ikke implementerte API-er.

Kildefunn for neste forsøk:

- `CorrespondenceEnvelopeClient` bruker den delte signerte og krypterte
  konvolutten. `CorrespondenceClient.validate` binder medlemsnøkler til den
  signerte avtalen og krever nøyaktig fire eksisterende meldingsrettigheter.
- `CorrespondenceCell.sendMessage` lager endelig `messageID` først etter mottak
  av den krypterte konvolutten. ID-en må være kjent før vedleggsbindingen signeres.
- Strømforsegleren er inkrementell. `AttachmentStreamV1.open` bufferer hele
  klarteksten og returnerer først etter autentisert slutt. Den er ikke et ferdig
  minnebegrenset mottakerlager for vilkårlig store vedlegg.
- Den eksisterende korrespondansecellen er relasjonsavgrenset. Å kalle dens
  felles lager «avsenders celle» etablerer ikke avsenderlagring.

## Modusvalgets regel — krav, ikke bygget

1. Begge parter når referansen og mottaker kan få avtalebundet lesetilgang:
   `reference`, uten flytting av byte.
2. Mottaker når ikke referansen, men filen bor hos avsender og lagres der:
   `fetchOnDemand`; strømmen starter ved mottakers henting.
3. Kilden er utenfor cellens rekkevidde, eller avsender bærer ikke kildelagringen:
   `copy`.

Nåbarhet og lagringsansvar skal avgjøre, og valgt modus med begrunnelse skal
rapporteres. Avsender skal ikke få et fritt modusfelt. Kopimodus må ha det
separate overdragelsesskrittet beskrevet i den tilhørende rapporten.

## Testresultater for bestillingen, enkeltvis

| Krav | Resultat |
| --- | --- |
| `reference` velges i riktig situasjon, uten byteflytting | Ikke implementert / ikke kjørt |
| `fetchOnDemand` velges når bare avsender når kilden | Ikke implementert / ikke kjørt |
| `copy` velges ved utilgjengelig kilde eller manglende lagringsbæring | Ikke implementert / ikke kjørt |
| Mottaker henter samme byte som avsender | Ikke implementert / ikke kjørt; kryptografisk rundtur alene besto |
| Strøm fra melding A avvises i melding B | Ikke implementert / ikke kjørt |
| Strøm avvises med annen avtale | Ikke implementert / ikke kjørt |
| Ikke-overdratt vedlegg forsvinner med meldingen | Ikke implementert / ikke kjørt |
| Avbrutt overføring gir feil, ingen fullført halvfil | Ikke implementert / ikke kjørt; eksisterende manglende-slutt-kryptotest besto |
| Metadata uten henting og uten hash | Ikke implementert / ikke kjørt |
| Full disk midt i overføring | Ikke implementert / ikke kjørt |
| Overdragelse/sletting avvises før verifisert henting | Ikke implementert / ikke kjørt |
| Overdratt fil overlever meldingens utløp | Ikke implementert / ikke kjørt |
| Overdragelse tilbys ikke i `reference`/`fetchOnDemand` | Ikke implementert / ikke kjørt |
| Eier uten policy ser konsekvensen før overdragelse | Ikke implementert / ikke kjørt |
| Uttrykkelig valgt policy kan sette standardsvaret | Ikke implementert / ikke kjørt |
| Overdragelse med vedleggsidentitet og tidspunkt kan leses etterpå | Ikke implementert / ikke kjørt |

## Full disk og avbrudd

Ingen filoverføring er implementert eller startet. **Det foreligger derfor
ingen måling av full disk eller avbrudd i en vedleggsoverføring.** Keychain-feilen
ovenfor er ikke en diskfullfeil.

Den eksisterende kryptotesten for fjernet sluttchunk besto og bekrefter at den
bufferende åpneren kaster feil. Det beviser ikke opprydding i midlertidige filer,
atomisk publisering, kortskrivingshåndtering eller crash recovery. Slike
lagringstester og en faktisk feilkontrakt gjenstår. En delvis strøm må ikke
publiseres som komplett, og ryddefeil må ikke skjules.

## Sprik i underlaget og hvilket krav som gjelder

Beslutningsfilen med «Avklart 29.09» og den siste bestillingen har prioritet.

| `FORMAALSSPEC.md` / tidligere tekst | Gjeldende eierbeslutning |
| --- | --- |
| G1-forslag uten implementasjonsautorisasjon | Dette oppdraget autoriserer implementasjon og lokal commit på egen gren. |
| Én fast leveringskopi anbefales | Alle tre moduser skal støttes, valgt av nåbarhet. |
| Relasjonsvert foreslås som lager | Avsenders celle lagrer; mottaker henter. |
| Generelt bevaringsvalg hos mottaker foreslås | Vanlige vedlegg dør med meldingen; uttrykkelig overdragelse i `copy` er unntaket. |
| 100 MiB/fil og 1 GiB/relasjon foreslås | Ingen total størrelsesgrense i protokollen; faktiske ressursfeil må rapporteres. |
| Hash foreslås i metadata før nedlasting | Kun navn, type og størrelse før henting; ingen hash. |
| Tidligere bestilling forbød sletting hos avsender | Opphevet. Overdragelse skal bygges i `copy`, først etter verifisert henting. |

Sletting skal ikke være et flagg på sending. Eierens klare konsekvenstekst,
policyvalget, varig mottakerfil og etterprøvbar historikk inngår i oppdraget.

## Grener, videreføring og gjenstående arbeid

Alle oppdragsgrenene heter `codex/correspondence-attachments-20260929`.

| Repository | Arbeidsmappe under HAVEN | Kodegrunnlag / arbeid |
| --- | --- | --- |
| CellProtocol | `_worktrees/cellprotocol-attachments-impl2` | `81601a6f835252aba7e99d43786fb5d67227c245`; ingen kodecommit |
| HavenAgentD | `_worktrees/havenagentd-attachments` | `ba1489554bdf8b27f10ef0fdc8fa727689fa0c98`; ingen kodecommit |
| CellProtocolDocuments | `_worktrees/documents-attachments` | Videreført fra `6ff6ecc`; disse rapportene og råloggene committes her |

CellProtocols gamle `_worktrees/cellprotocol-attachments` hadde en `.git`-peker
til manglende worktree-metadata. `git worktree repair` ga `exit=1` og kunne ikke
lokalisere repositoryet. En ny arbeidsmappe ble opprettet fra **samme eksisterende
gren**, uten å slette eller endre den gamle mappen. Dette starter ikke en ny
implementasjon eller kaster tidligere arbeid.

Rapporter og belegg kopieres også til den bestilte
`CellProtocolDocuments/Deliverables/`-stien. Eksisterende endringer i vanlige
arbeidsmapper er bevart. Ingen push, merge, utrulling eller operative sendinger.

Gjenstår: hele vedleggs- og overdragelsesimplementasjonen, signert avtaleutvidelse,
kildeløsning/nåbarhet, strøm-/lagringsintegrasjon, MCP-verktøy, samtlige nye
akseptansetester, HavenAgentD build/test og de virkelige mottakerleveransene.
Neste kjøring trenger en testvert som kan kjøre de aktuelle nøkkellagringstestene,
eller en uttrykkelig eierbeslutning om hvordan denne kjente miljøfeilen skal
håndteres. Ingen av delene er antatt eller gjennomført her.

## Læringsfangst

`L-2026-09-29-i-skrivebegrenset-macos-sandkasse-kan` er fanget og anvendt i
`CellScaffold/.claude/skills/cellprotocol-contract-testing/SKILL.md`. Den forklarer
skillet mellom skrivbar modulcache og tilgang til macOS-nøkkellagring. Tidligere
endringer i ferdigheten er bevart.

Synkronisering ble forsøkt én gang: ZIP ble bygget, men kopiering til
brukerens ferdighetsmappe ble nektet med `Operation not permitted`, `exit=1`.
Læringen er derfor **anvendt, ikke distribuert**; den er ikke markert som synket.
Ingen alternativ prosess ble brukt for å omgå skrivetilgangen.
