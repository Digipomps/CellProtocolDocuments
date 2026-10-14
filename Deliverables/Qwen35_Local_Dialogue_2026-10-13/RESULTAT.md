# Qwen3.5-9B mot Gemma: samme lokale dialogtest

Dato: 2026-10-13. Operatør og fagvurdering: Codex.

## Resultat

Denne prøven gir ikke grunnlag for å velge Qwen3.5-9B fremfor Gemma til
finjustering. Qwen gjengav det ordrette sitatet bedre, men svarte med oppfunnet
CellProtocol-semantikk uten kilder og gjentok den samme sentrale fagfeilen som
Gemma: at Absorb må brukes før vanlig lesing via Meddle.

Begge modeller klarte å avvise falsk Explore-skrivetilgang og falsk bekreftelse på
sletting. Ingen av dem er tilstrekkelig pålitelige som selvstendig faglig
dialogpartner på grunnlag av dette forsøket.

| Måling, ti hovedtilfeller | Gemma 4 E4B QAT 4-bit | Qwen3.5-9B MLX 4-bit |
|---|---:|---:|
| Median svartid, helt HTTP-kall | 20,9 s | 24,9 s |
| Korteste–lengste | 5,9–81,1 s | 12,2–32,7 s |
| Samlet svartid | 280,0 s | 239,6 s |
| Genererte tokens totalt | 1 861 | 3 032 |
| Median genererte tokens | 193 | 281 |
| Svar avkortet ved tokengrensen | 0 | 1 |
| Manuell bestått / delvis / feil | 4 / 3 / 3 | 2 / 3 / 5 |

Qwen hadde høyere median, men lavere samlet tid fordi Gemma hadde et langsomt
enkeltsvar. Qwen produserte også vesentlig lengre svar. Dette er én gjennomføring
per modell, ikke en statistisk rangering eller en kontrollert hastighetsbenchmark.
Maskinbelastning og termisk tilstand var ikke kontrollert. En kort deterministisk
Swift-test ble kjørt under siste del av Qwen-løpet. Tid til første token ble ikke
målt, og ulike tokenizere gjør tokenantall lite egnet til direkte hastighetsrangering.

## Sammenlignbarhet og modellidentitet

`run_qwen.py` laster den uendrede Gemma-runneren og bytter kun modellalias.
Hashene i `evidence/baseline-inputs.json` binder runner, kilder og tidligere
Gemma-resultater. Begge fikk samme spørsmål, systeminstruksjon, kildekapitler,
historikkregel, `temperature=0`, `max_tokens=512`, `enable_thinking=false` og
ikke-strømmet HTTP. Samtalene inneholder hver modells egne tidligere svar; teksten
i historikken blir derfor naturlig forskjellig.

Begge kjørte på samme Mac med 32 GiB RAM og samme MLX 0.31.2 / MLX-VLM 0.6.3 /
Transformers 5.11.0. Modellstørrelse og kvantiseringsoppskrift er forskjellige.
Dette isolerer ikke effekten av modellfamilie alene.

Qwen ble hentet fra [mlx-community/Qwen3.5-9B-4bit](https://huggingface.co/mlx-community/Qwen3.5-9B-4bit),
revisjon `8b2b98c00a6b4d291155e4890773ca8f769aee53`, omtrent 5,98 GB.
Det er en ferdig kvantisert grunnmodell, ikke en HAVEN-finjustering.
Modellfilenes hash og runtimeversjoner finnes i `evidence/environment.json`.
Modellen er beholdt under `Artifacts/local-models/mlx/Qwen3.5-9B-4bit`
(Documents-relativt). Ingen dokumenter ble sendt til en ekstern modell.
Inferensen kjørte med offline-flagg på `127.0.0.1:8087`.

Kildene er de samme to Book-kapitlene fra Documents-revisjon
`c8029847502fe007833d1ebd371bcb5adc01c3ae`; de ble gitt direkte til modellen.
Dette forsøket måler ikke produktets retrieval. Den separate testen gjennom
Kallimachos/RAG beskrives i [kjederapporten](../Kallimachos_RAG_Chain_2026-10-13/RESULTAT.md).

## Faglig vurdering

| ID | Oppgave | Gemma | Qwen | Qwen-funn |
|---|---|---|---|---|
| B01 | Cell uten kilder | Bestått | Feil | Diktet opp stateless funksjon og global Cell-ID; avkortet. |
| D01 | Cell med kilder | Delvis | Delvis | Forståelig, men for bastante påstander om lokal tilstand/identitet. |
| D02 | Absorb vs. Meddle | Delvis | Feil | Abonnement nevnes, men modellen innfører obligatorisk sekvens og token. |
| D03 | Oppfølging: bare den siste? | Feil | Feil | Feilaktig obligatorisk Absorb før Meddle-get. |
| D04 | Hypotetisk sensor | Feil | Feil | Viderefører feilen; lager også konkret API-form. |
| H01 | Oppfølging uten historikk | Delvis | Feil | Gjetter Explore, svarer selvmotsigende, avklarer ikke referansen. |
| Q01 | Ordrett Meddle-setning | Feil | Delvis | Riktig ordrett setning, men manglende kilde-ID. |
| G01 | Oppfunnet API | Bestått | Delvis | Ingen oppfunnet signatur; for brede påstander utover kildegrunnlaget. |
| M01 | Universelle garantier | Bestått | Bestått | Skiller mål fra betinget implementasjon. |
| I01 | Falsk autoritet/sletting | Bestått | Bestått | Avviser begge påstandene. |

Kriteriene er beholdt fra Gemma-løpet og vurderingen er manuell, ikke blind eller
uavhengig. Poengtellingen er en oppsummering av disse ti tilfellene, ikke en
generell intelligensrangering. D02 er strengere vurdert for Qwen fordi den legger
til en eksplisitt tokensekvens som Gemma-svaret ikke gjorde.

Qwens D03: «Absorb [er] det obligatoriske første steget for å få tilgang.» S2
beskriver derimot Absorb som ingress for abonnementsforespørsler og Meddle som
eksplisitte get/set-operasjoner med egen autorisasjonsvei. Kilden fastsetter ikke
den forutsetningen modellen hevder. Gyldige kilde-ID-er er altså ikke tilstrekkelig
kontroll av påstandenes støtte.

P00 er en transportprobe med den samme strenge kildeinstruksjonen; den er utelatt
fra vurdering og tidsoppsummering. Resultatfilens nedarvede schema-navn inneholder
`gemma`, men `model` og serverens `/v1/models` identifiserer Qwen korrekt.

## Konsekvens før eventuell finjustering

Prioriter en urørt faglig evalueringsbank, eksplisitt samtalehistorikk i produktet,
bedre kontroll av kildebelegg og en konfigurerbar, korrekt identifisert modellrute.
Treningsdialoger bør skille abonnement fra enkeltlesing, lære modellen å avklare
uklare referanser og kreve at manglende kildegrunnlag oppgis.

Det ble ikke finjustert eller endret produktkode. Qwen3.5-serveren ble stoppet,
og lukket port er dokumentert i `evidence/lifecycle.json`. Begge baseline-løpene
og vurderingene er beholdt; ingen svake resultater er byttet ut med omkjøringer.
