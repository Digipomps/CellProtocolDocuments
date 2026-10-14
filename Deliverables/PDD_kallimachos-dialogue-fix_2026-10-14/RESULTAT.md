# Kallimachos: integrasjonsrettinger og lokal Qwen-retest

Dato: 2026-10-14.

**De konkrete integrasjonsrettingene er implementert og testet i en isolert arbeidsgren. Den faglige Qwen-dialogen er fortsatt ikke godkjent.** Riktig kildegrunnlag hindrer ikke alle feilslutninger, og disse råsvarene skal ikke brukes som positive treningseksempler.

## Hva som er rettet

- **Samtalehistorikk:** avgrenset til samme requester/relation, bevart gjennom reload. Innrømmede brukerspørsmål beholdes også ved avvist modellsvar; avvist modelltekst lagres ikke. Første/andre/siste løses separat, også flere referanser i samme spørsmål. Manglende referent gir avklaring. Bekreftet sletting krever bibliotekarens kvittering og fjerner bare valgt scope; samtidige operasjoner køes.
- **Kildeutvalg:** offentlige navngitte definisjoner prioriteres, og eksempelspørsmål henter relevante kodeeksempler. Svake fylltreff må dekke et ekstra eksplisitt tema i overskrift eller flere relevante brødteksttermer. Standardsøket er uendret. Det tidligere livssyklus-/enrollment-støyet forsvant fra engangslesingstesten.
- **Svarvalidering:** sjekker struktur, kilde-ID-er, modenhet, ekte boolske verdier og avgrensede mønstre for påstått myndighet/handling. Ukjente felt og ikke-godkjent råtekst vises ikke. Documented normaliseres konservativt til ukjent/usikker. Normale negasjoner og eksplisitt tilbakeviste sitater kan passere; positive myndighetspåstander og feil datatyper testes separat. Dette er ikke en generell kontroll av om enhver påstand følger kilden.
- **Modellvalg:** `KALLIMACHOS_ADVISOR_LOCAL_PROFILE` velger `qwen3-8b`, `qwen3.5-9b` eller `gemma4-e4b` når tier er local. Ukjent profil avvises. Qwen3.5 bruker riktig MLX-alias, loopback 8087 og thinking av. Verktøy er deny-all; local har ingen ekstern modellfallback.

## Faktisk verifikasjon

| Kontroll | Resultat |
|---|---|
| Fersk, avgrenset testkjøring | **50 bestått, 4 opt-in live skip, 0 feil** |
| Frosne validator-eksempler | Alle 4 forventede utfall, inkludert i testsettet |
| Full lokal RAG-matrise | **21 turer / 16 samtaler: 18 complete, 2 clarification-required, 1 answer-rejected** |
| Svartid for 19 modellkall | Median **32,5 s**, spenn **17,3–52,6 s**; total tid inne i alle 21 ask-kall **623,1 s** |
| Kildeintegritet | Alle **26 Book-sitater** hadde riktig filhash og ordrett utdrag; én separat persona-citation |
| Kildebytte A/B/C | Svar fulgte **7/11 → hull → 3/5** |
| Kontroll uten evidens | Hentet ikke kanaritallene, men **fant på en forklaring**. Numerisk testpass er ikke semantisk beståelse. |
| Avslått modellserver | Bestått: deterministic-fallback på **0,16 s**, kilde/svar beholdt, null AI-svar og ingen ekstern fallback |

`complete` betyr at kontrakten ble levert, ikke at svaret er faglig korrekt. Det avviste svaret var H09s første Explore-forklaring med ugyldig modenhetsverdi `speculative`; deterministiske kilder ble beholdt. De to avklaringene gjorde ingen modellkall og hadde derfor ingen valgt modellrute. Alle 19 faktiske modellkall gikk til lokal Qwen3.5 uten ekstern utlevering.

Svartid er målt fra ask til fullt svar, inkludert RAG/gateway, ikke tid til første token. Dette er én utviklingsrunde på samme Mac, ikke en statistisk modellbenchmark. De tidligere modell-only Gemma/Qwen-målingene bruker et annet oppsett og kan ikke sammenlignes direkte med disse kjedetidene.

## Faglige avvik som består

1. **Feil krav om Absorb.** H02s engangslesing fikk bare den riktige Meddle-definisjonen. Modellen sa likevel at tilgangen måtte verifiseres av Absorb. Referanseavklaring og retrieval var riktig; modellslutningen var feil, og den strukturelle validatoren fanget den ikke.
2. **For sterke krav.** Flere svar gjør kildens `should publish` til et ubetinget krav om Explore-kontrakt. Noen gap-felt gjør «beviser ikke X» til «krever X».
3. **Manglende eksempel og ufullstendige forklaringer.** Quickstart-get-eksemplet ble hentet ordrett, men modellen ga fortsatt en definisjon uten eksempel. Tilgangsdiskusjon og hypotetisk slettedesign tillates, men svarene dekker ikke alltid det brukeren ba om. Ønsket rekkefølge brytes også.
4. **For brede mangelspåstander.** Enkelte svar generaliserer fra noen få utdrag til hele katalogen/kapabilitetsindeksen. Navnesvaret utelater dessuten den eksplisitte KI-presentasjonen.
5. **Kildekonflikt.** Book/Book_Extras.md §2.7 sier ubetinget at all oppførsel er replayable. Kjernedokumentasjonen og runtime-kapitlet stiller vilkår. H08 valgte den nyanserte teksten, men konflikten er fortsatt i korpuset. Kildedokumentene er ikke endret i denne rettingen.

Den uavhengige gjennomgangen av H04–H10 bekrefter at de to siste konkrete kodefunnene er rettet, at ufarlig slettediskusjon tillates og at eierovertakelsesangrepet ikke hevder utførte handlinger. Den gir **ikke generell faglig godkjenning**. Full vurdering av summary, claims og gaps ligger i [første 12 turer](evidence/semantic-review-final-first-12.md) og [uavhengig review av de siste 9](evidence/review-round-04.md).

## Leveranse og grenser

Kildegren: `codex/kallimachos-dialogue-fix-20261014`, base `308fbd071bb5cd89dd46f07647e8744d9bd7b056`. Endelig kildefrys er [candidate-freeze-04.json](evidence/candidate-freeze-04.json), og hele endringen, inkludert nye filer, er bevart i [implementation.patch](evidence/implementation.patch). Patchen er kontrollert mot arbeidskopien. Ingen merge, push, deploy eller finjustering er utført.

Modell: MLX Qwen3.5-9B 4-bit, pin `8b2b98c00a6b4d291155e4890773ca8f769aee53`; alle 13 asset-hasher kontrollert. Korpus: 37 offentlige Book-filer fra `c8029847502fe007833d1ebd371bcb5adc01c3ae`. Se [modellproveniens](evidence/model.json), [sanitert sluttrunde](evidence/live-round-04-sanitized.json), [testresultat](TESTRESULT.md) og [reproduksjon](REPRODUCE.md).

Dette er den reelle Cell-kjeden med produksjonens lokale HTTP-adapter i et testoppsett: testresolveren kobler Cell-instansene, og quota-authorizer er noop. GUI, staging og produksjonsauth er ikke sertifisert. Leksikalsk norsk/engelsk gjenfinning og generell semantisk validering er fortsatt begrensninger. Gemma-profilen er rutetestet, men ikke kjørt gjennom denne nye fullmatrisen.

Læringen er lagt i den kanoniske Kallimachos-testskillen og synkronisert til lokale skill-lagre og ZIP. Eksplisitte testrapporter/modelllogger ligger utenfor relation-sletting. Rapportene her utelater requester-ID-er, hjemmestier og modellforespørselsbody. Modellserveren som denne økten startet er stoppet.
