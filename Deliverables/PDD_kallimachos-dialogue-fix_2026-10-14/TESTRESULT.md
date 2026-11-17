# Testresultat — lokal Kallimachos-kandidat

Dato: 2026-10-14. Kandidatgren `codex/kallimachos-dialogue-fix-20261014`, base `308fbd071bb5cd89dd46f07647e8744d9bd7b056`. Ikke merget eller deployet.

## Ferdig verifikasjon

| Lag | Resultat | Bevis |
|---|---|---|
| Ren baseline, fersk bounded build | 27 bestått, 3 live skip, 0 feil | evidence/baseline.json |
| Endelig fokusert testsett | 50 bestått, 4 live skip, 0 feil; 54 oppdaget | candidate-tests-08, oppsummering i evidence/test-runs.json |
| Frosne validator-eksempler | 4/4 forventede utfall; inkludert i én av de 50 testene | evidence/validator-round-04.json |
| Literalguard | Seks selvtester og skann bestått; ingen nye brudd | evidence/test-runs.json |
| Diff/patch | git diff --check og git apply --reverse --check bestått | evidence/implementation.patch |

De fire live-skipene er opt-in-metoder, ikke fire mislykkede tester. Live-runder rapporteres separat; overlappende kjøringer summeres ikke til unik dekning.

Dekket: samme requester/relation, reload via faktisk Codable-serialisering, gammel state uten nye felt, scopes/relation-bytte, bekreftet/ubekreftet sletting og SHA-256-kvittering, kølagt sletting under pågående modellkall, avvist modelltekst utelatt fra historikk, spørsmålet bevart ved avvisning, referanseorden, manglende referent, flere referenter, kildeopptak/rangering/ordrette utdrag, valide/ugyldige profiler, faktiske HTTP-body-bytes for thinking-off/tools-off, inn-/utleveringsporter, struktur/kilde-ID/modenhet/myndighet og sanitert visning.

## Mellomliggende funn og rettinger

- Første kandidat feilet to nye tester: rå definisjonsterm ble sammenlignet med stemmet søketerm; samme feil slo ut i oppfølging. Felles tokennormalisering rettet dette, uendrede tester bestod.
- Første live-runde hadde 13 avvisninger; diagnostikk viste at Qwen brukte evidensstatusen documented som modenhetsverdi. Konservativ normalisering nedgraderer til ukjent/usikker, ikke implementert/testet.
- Andre runde avdekket ukjent med uncertain:false, tapt referanse etter avvist svar, manglende eksempelkilde og falsk avvisning av «ingen dokumentasjon på at …». Dette er rettet med avgrensede regler og positive motkontroller.
- Uavhengig review av kandidat 03 fant kollaps av flere referanser til ett navn og at documented-normalisering skjulte feil datatype. Begge er rettet i kandidat 04.
- Et nytt kontrolltilfelle for standardsøk blandet treffopptak og topp-tre-rangering. Kontrollsøket bruker nå limit:20 for å sjekke opptak; produksjonsrangeringen ble ikke endret for å gjøre testen grønn.
- Buildforsøk 05 ble stoppet før kompilering av gammel 10 %-overstyring. Gjeldende dokumenterte Mac-policy er minst 40 GiB og 5 % etter 10 GiB reserve. Standardporten passerte; ingen sletting eller ad-hoc cache ble brukt.

## Modell og korpus

Qwen3.5-9B, MLX affine 4-bit/group64, pin `8b2b98c00a6b4d291155e4890773ca8f769aee53`. Alle 13 modellasset-hasher kontrollert mot tidligere måling. MLX 0.31.2, mlx-vlm 0.6.3, transformers 5.11.0. Modellalias `/private/tmp/haven-qwen35-9b`, provider `local-qwen35`, loopback 8087. Ingen ekstern modellfallback. Max 1600 output tokens, deterministic mode, thinking av, tools deny-all.

37 offentlige Book-filer fra `c8029847502fe007833d1ebd371bcb5adc01c3ae`, eksakte filhash­er fra forrige kjedemåling. Ingen private Deliverables som modellgrunnlag. Modellen ble startet fra allerede installerte assets i offline-modus.

## Tolkning og avgrensning

Alle runder bruker faktiske CommonsLibrarian-, Advisor- og AIGateway-instanser og produksjonens HTTP-adapter. En testresolver kobler Cell-instansene, og quota-authorizer er noop i testen. Dette er ikke GUI-, deploy-, nettverksresolver- eller produksjonsauth-akseptanse.

Live-runneren verifiserer lokal modellidentitet, ingen ekstern utlevering, tools deny-all, manglende modellmyndighet og eksakte offentlige citations. Den beviser ikke at hvert utsagn følger kildens mening. Gyldig JSON og riktige kilde-ID-er kan fortsatt inneholde feil slutninger. Usikkerhetsmerking er heller ikke bevis for påstanden.

Kriteriene ble frosset før første kandidatvurdering. Runde 2 og senere er ublindede regresjoner. Det finnes ingen påstand om generell modellrangering, statistisk signifikant hastighetsforskjell eller effekt av finjustering.

## Sluttrunder

Endelig matrise: 21 turer i 16 samtaler, 18 complete, 2 clarification-required, 1 answer-rejected. Runtime-/kildeassertions bestod, men faglig dialogkvalitet er ikke godkjent. 19 modellkall hadde median 32,488 s (17,266–52,591 s); sum ask-tid 623,121 s. Se evidence/live-round-04-summary.json og sanitert fullresultat.

Canary-testens ene XCTest bestod på 129,509 s. A/B/C fulgte 7/11, hull og 3/5. D uten evidens gjentok ikke tallene, men fant på en forklaring om statsborgerskap; semantisk avståelse feilet. Dette er ingen juridisk opplysning. Se evidence/canary-final.json.

Egen modellserver ble stoppet og loopback-port 8087 bekreftet lukket. Offline-testens ene XCTest bestod; ask tok 0,161 s, status deterministic-fallback, én Meddle-citation bevart, null AI-svar, ingen ekstern fallback. Se evidence/offline-final-sanitized.json og evidence/server-stop-final.json.

Alle 26 Book-citation-forekomster i sluttrunden hadde riktig content SHA-256 og ordrett excerpt. Persona-citation ble kontrollert mot tillatt bundle-sti, men bundlehash er ikke uavhengig kontrollert i sluttgjennomgangen. Uavhengig review dekket de siste ni turene; hovedagentens review dekket de første tolv. Ingen semantisk total-passrate hevdes.
