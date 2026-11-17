# Lokal Kallimachos-/RAG-test

Les `RESULTAT.md` for funn og avgrensning. Dette er en måling av eksisterende
Advisor-kode med virkelig CommonsLibrarian og AIGateway, ikke en endring av
produktet eller en gjenoppretting av den tapte Gemma-matrisen fra august.

## Inndata og runner

- `evidence/prebuilt-provenance.json`: identifisert kildearbeidstre, binærhash og
  begrensningen ved å bruke en eksisterende testpakke uten ny kompilering.
- `evidence/resources.json`: hash av testpakkens ressurser og kapabilitetsindeks.
- `evidence/public-corpus.json`: 37 offentlige Book-filer, Git-revisjon, filhash og
  sist endret-dato. Snapshotet inneholder ingen Deliverables-filer.
- `evidence/canary-fixtures.json`: full tekst og hash for tre syntetiske korpus.
- `evidence/local-model.json`: den faktiske produktmodellens identitet og hash.
- `run_prebuilt.py`: isolert kjøring av navngitte XCTest-metoder; avviser feil
  binærhash og overskriving av tidligere resultater. Ingen kompilering.
- `extract_evidence.py`: henter bare tillatte resultatfelt fra midlertidige logger.
  Gjenkjennelige XCTest-diagnostikklinjer fjernes hvis stderr ble flettet inn i
  stdout; selve modellsvaret omskrives ikke.

Midlertidig testområde: `/private/tmp/kallimachos-chain-20261013/`. Rålogger
beholdes bare der; varige observasjoner finnes i `evidence/observations.json`.
Midlertidige filer og modellalias er ikke garantert å overleve opprydding/omstart.

For gjentakelse må den eksakte testbinæren og ressursene gjenfinnes eller bygges
fra kilde med repoets godkjente, kapasitetskontrollerte wrapper. En ny binær er en
ny kjøring med ny proveniens, og skal ikke gis gammel hash. Kopier kun en stabil
testpakke; ikke endre eller rydd en annen oppgaves aktive byggcache.

Lag det offentlige snapshotet med `git show <revision>:<path>` for hver fil i
`public-corpus.json` og kontroller SHA-256. Legg den registrerte `provenance`
som `.commons-corpus-provenance.json` i snapshotroten. Canary A/B/C bruker den
registrerte teksten som `Book/01_Canary.md`, med eksplisitt syntetisk proveniens.

Kjørekonfigurasjonen for hvert utført løp ligger som `liveConfiguration` i dets
evidence-JSON. Modellserveren må identifisere seg som `Qwen3-8B-Q4_K_M.gguf` på
loopback 8083, med det faktiske modellinnholdet — ikke et alias for Qwen3.5.

Eksempel med allerede kontrollert testpakke og arbeidstre, fra Documents-roten:

```bash
python3 Deliverables/Kallimachos_RAG_Chain_2026-10-13/run_prebuilt.py \
  --name ny-showcase \
  --selector AppTests.KallimachosAdvisorCellTests/testShowcaseAgainstRealCorpus \
  --source-repo /private/tmp/kontrollert-cellscaffold-arbeidstre \
  --env-json /private/tmp/kallimachos-chain-20261013/showcase-env.json
```

`KALLIMACHOS_ADVISOR_LIVE_TIER=local` er eksplisitt. Ingen ekstern modellnøkkel
arves av runneren. Testens resolver kobler de tre ekte Cell-instansene sammen;
quota er en eksplisitt noop-testadapter. Dette er ikke bevis for produksjonsresolver,
fakturering, Porthole, nettverk mellom maskiner eller en bestemt release.
