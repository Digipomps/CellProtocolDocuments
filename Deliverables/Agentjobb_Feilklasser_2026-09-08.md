# Feillogg — Losen, 3.–5. september 2026

**Formål:** dokumentere hva som dokumenterbart ikke virket, slik at samme feil
ikke gjentas. Skrevet av Losen om Losen.

**Status:** de mekaniske feilene (klasse B og C) er lukket i kode. Klasse A er
en disiplin og har ingen mekanisk sperre; den er derfor listet med sitt eget
mottiltak og må håndheves av den som leser.

---

## Klasse A — påstander om koden som ikke holdt

Alvorligste klasse, fordi den ikke feiler synlig. En jobb som avvises stopper.
En feil påstand går videre inn i design og dokumentasjon.

### A1. «Append-only er allerede håndhevbar i koden»

**Sagt:** 4. sept., etter å ha funnet hash-kjeden i `EntityAuthorityCommit`
(`previousHash`/`entryHash`/`revision`, verifisert kjedegang, replikalager som
avviser feil `previousHash`). Konkluderte med at «forvalteren kan ikke omskrive
historikken» var en egenskap ved koden.

**Faktisk:** kjeden er ekte, men **commit er valgfri**. `Object.set` erstatter
verdier, flere aktive skrivestier lagrer snapshot direkte utenom journalen, og
aktiv lagring mangler ekstern anti-rollback og innkoblet quorum. Garantien
gjelder kun commit-deltakende historikk.

**Rotårsak:** jeg fant en mekanisme og antok at den var obligatorisk. Jeg leste
verifiseringskoden, ikke kallstedene.

**Mottiltak:** en mekanisme er ikke en garanti før man har vist at det ikke
finnes vei utenom. Finn kallstedene, ikke bare implementasjonen.

### A2. «Nøkkelen ligger hos entiteten»

**Sagt:** i kapittel 33 §4A, som en egenskap ved vault-modellen.

**Faktisk:** Apple-implementasjonen eksponerer `privateKeyData(for:role:)` og
forsøker rå eksport av signeringsnøkkelen. Ikke-ekstraherbarhet og
bruksmyndighet er dessuten to forskjellige kontroller som må dokumenteres hver
for seg — et skille jeg ikke hadde gjort.

**Rotårsak:** jeg leste protokollen (`IdentityVaultProtocol`) og ikke
implementasjonen.

**Mottiltak:** for sikkerhetspåstander teller implementasjonen, ikke
grensesnittet. Den svakeste implementasjonen setter garantien.

### A3. Oppløsningsmålingen på BOK 1

**Sagt:** en spektraltest viste detaljer opp mot 200 dpi, altså at fila var
trykkbar i A4.

**Faktisk:** testen målte den ferdig rendrede siden, der vektortekst i
snakkebobler er knivskarp oppå et bløtt bilde. Et tekstfritt utsnitt i 1:1 ved
300 dpi var tydelig grøtet. Median effektiv oppløsning var 63 dpi, ikke 200.

**Rotårsak:** jeg målte noe i nærheten av påstanden og rapporterte det som
påstanden.

**Mottiltak:** når en måling og en direkte observasjon er uenige, vinner
observasjonen. Se på saken selv før du stoler på metrikken.

**Merk:** A3 ble oppdaget av meg selv, A1 og A2 av Codex. Det er et argument
for at gjennomgang av påstander skal gjøres av en annen part enn den som
fremmet dem.

---

## Klasse B — sandkassen strammet uten at leveransen fikk plass

Tre tilfeller på to dager, samme form.

| Dato | Jobb | Feil | Kostnad |
|---|---|---|---|
| 3. sept. | `losen-entitet-design` | `read-only`, men skulle skrive rapport | 16 min analyse, ikke lagret |
| 4. sept. | `losen-entitet-design-2` | cwd `CellProtocol`, leveranse til søskenkatalogen `CellProtocolDocuments` | 22 min, fil havnet feil sted |
| 3. sept. | `audio-s1s2` | (ingen feil — nevnt som kontroll: cwd og leveranse i samme tre) | — |

**Rotårsak:** jeg satte sandkassen ut fra hva jobben ikke skulle få lov til, og
sjekket aldri at det den *skulle* levere fikk plass innenfor.

**Mottiltak — implementert i `_losen-queue/runner.sh`:**

- Jobbfilen har fått en valgfri linje 3: erklært leveransesti.
- Runneren avviser før kjøring hvis leveransesti er erklært og sandkassen er
  `read-only`, eller hvis stien ligger utenfor `cwd`. Avvisningen logges med
  navngitt grunn.
- Etter kjøring sjekker runneren at fila faktisk ble skrevet, og skriver en
  advarsel i både logg og svarfil hvis ikke.
- Tom linje 1 betyr nå HAVEN-rot. Standarden er bred cwd; innsnevring krever
  en grunn.

---

## Klasse C — plattformantakelse

### C1. `flock` i runneren

**Sagt:** runneren ble skrevet og syntakssjekket med `bash -n`, som passerte.

**Faktisk:** `flock` er en Linux-kommando og finnes ikke på macOS. Runneren
avsluttet stille hvert minutt i en halvtime uten å kjøre noe. Feilen sto i
`logs/launchd.err`, ikke i noe jeg hadde sjekket.

**Rotårsak:** jeg redigerer fra en Linux-VM og leverer til en macOS-vert. Det
er en stående felle, ikke et engangsuhell.

**Mottiltak:** `bash -n` fanger syntaks, ikke manglende kommandoer. For skript
som skal kjøre på Mac: unngå plattformspesifikke verktøy (`flock`, GNU-flagg
til `sed`/`date`), og sjekk `launchd.err` som første feilsøkingssteg.

---

## Det som virket, og bør beholdes

- **Jobbkøen.** Etter `flock`-fiksen har den kjørt jobber fra flere tråder uten
  tilsyn. Den fjernet 60-sekunders-taket som blokkerte alt Codex-arbeid.
- **Å be Codex korrigere mitt eget arbeid eksplisitt.** Instruksen «avsnittet er
  skrevet av meg og skal rettes, ikke forsvares» ga tolv konkrete korreksjoner.
  Uten den formuleringen ville han sannsynligvis vært mildere.
- **Å skrive forbehold inn i leveransen.** Kapittel 34s tier-system og
  kravet om at et felt bare kan vises sammen med sitt opphav, er samme
  disiplin som manglet i A1 og A2 — anvendt på utdata, men ikke på mine egne
  påstander om koden. Det er hullet.

---

## Åpent

Ingen mekanisk sperre finnes for klasse A. Det nærmeste er at
påstandsgjennomgang gjøres av en annen part, slik Codex gjorde her. Vurder om
`haven-claim-review` bør utvides til også å gjelde interne påstander om
kodebasen, ikke bare offentlige påstander om produktet.
