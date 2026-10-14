# Lokal Gemma-dialogmåling, 2026-10-13

## Formål og avgrensning

Kjetils bestilling: «Finn eller gjenopprett riktig testoppsett og kjør en første lokal dialogtest med Gemma, så vi ser hva som mangler før finjustering.»

Dette oppsettet måler norsk forklaring, samtalehistorikk, kildebruk og usikkerhet med
den allerede installerte Gemma 4 E4B QAT-modellen. Det er en ny, avgrenset måleharness,
bygget på den kjente MLX/VLM-runtimen. Det er ikke gjenfunnet originalkode fra august.
Ingen trening eller produktendring er utført som del av målingen.

Rapporten `CellScaffold/Documentation/Kallimachos_Local_Gemma_Dialogue_Test_Report_2026-08-11.md`
(HAVEN-relativ sti) opplyser at den gamle implementasjonen var ubundet. Et søk i
lokal Git-historikk for det oppgitte testnavnet ga ingen treff, og søk i bevarte
CellScaffold-arbeidstrær, `_worktrees` og `_to_delete` fant ikke Swift-testen.
Dette beviser ikke at ingen annen sikkerhetskopi finnes.

Den gamle demooppskriften krever en bestemt Cell-kjede og offentlig evidensport.
Denne målingen kaller bare modellen med kontrollerte kilder. Den verifiserer ikke
CommonsLibrarian, AIGateway, produktets RAG, GUI, tilgangskontroll eller sletting.
Oppfølging gjennom dagens produktkjede er et eget, fortsatt utestet steg.

## Forhåndsdefinerte mål

- Forklare Cell og grensesnittene faglig korrekt på naturlig norsk.
- Bruke historikken til å tolke oppfølgingsspørsmål, med kontroll uten historikk.
- Bevare ordrett sitat og bare referere til leverte kilde-ID-er.
- Erkjenne kildemangel og avvise oppdiktede funksjoner/handlingsbekreftelser.
- Skille designmål fra universelle implementeringsgarantier.
- Måle total svartid, tokenbruk og eventuell avkorting.

Kriteriene står i `run_dialogue.py` før kjøring. Automatiske kontroller dekker
bare transport, kilde-ID-er, sitattekst og avkorting. Faglig kvalitet og naturlighet
må bedømmes manuelt. Ingen samlet prosent er en generell modellrangering.

## Kilder og reproduksjon

`evidence/corpus.json` inneholder to Book-kapitler lest med `git show` fra
`c8029847502fe007833d1ebd371bcb5adc01c3ae`, med SHA-256 per fil. Ucommittede
Book-endringer er ikke blandet inn. Kildene er forhåndsvalgt; dette gir modellen
relevant grunnlag, men måler ikke hvor godt en RAG finner det.

`evidence/environment.json` angir runtimeversjoner, modellfiler og SHA-256.
`evidence/run-01.jsonl` inneholder tillatte resultatfelter og syntetiske spørsmål,
ikke fulle HTTP-kropper, requester-ID-er eller privat dokumentasjon.

Gjenbruk de lokale aliasene for eksisterende modell og Python-miljø:
`/private/tmp/haven-gemma4-e4b` og `/private/tmp/haven-gemma-venv`.
Ikke overskriv aliaser som peker til et annet oppsett. Start den installerte
`kallimachos-local-gemma-setup/scripts/kallimachos-gemma-server.sh run` i en egen
terminal med `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`, og kontroller `health`.
Dette bruker bare serverens livssyklus; det er ikke bestått Cell-preflight.

Fra denne mappen:

```sh
python3 run_dialogue.py --output evidence/run-02.jsonl
```

Resultatfiler overskrives ikke. Serveren bindes til `127.0.0.1:8087`, klienten
ignorerer proxyinnstillinger, og ingen ekstern modell, nedlasting eller verktøy
inngår. Samtalehistorikken settes eksplisitt av klienten. Serveren stoppes med
livssyklusskriptets eierskapskontrollerte `stop` etter målingen.

Bruk bare syntetiske spørsmål og de frosne offentlige kildene i denne harness-en.
Rapportene her er kuraterte måleartefakter; de er ikke produktets samtalehistorikk
og omfattes ikke av produktets relasjonssletting.
