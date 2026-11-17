# Målt: PNG-filer levert til Macen har én blokk mer enn fila de ble laget fra (07.10.2026)

Målt av korrespondanse-tråden 07.10.2026 mellom kl. 15:38Z og 15:50Z. Lest mot måleutskriftene av en uavhengig leser (Claude Opus) 07.10.2026 kl. 15:52–15:57Z. Den fant én ting i dette notatet som måtte rettes (tellingen av de 18 filene); den er rettet, og rettelsen er ikke lest på nytt.

Dette er ikke nytt. Det samme står i `Book/haven_lessons_register_v0.json` (`lesson.md5-differs-for-images-written-from-the-cloud`, 02.10.2026) og i skillen `haven-purpose-driven-dev`, under «Verification and landing tools». Lærdommen står i §4 i `FORMAALSSPEC.md` i denne mappen, skrevet dit av `lookup`. Tråden slo den ikke opp da md5 avvek for en figur 07.10, og målte på nytt. Målingen legger til to ting: kopien i trådens utdatamappe har ikke alltid blokken, og hva blokken inneholder.

## Fire bilder, lest tre steder

Hver fil er lest blokk for blokk med samme skript på tre steder: fila slik den ble rendret (trådens arbeidsmappe i skyen), kopien i trådens utdatamappe i skyen (`/mnt/user-data/outputs/`), og fila i denne mappen på Macen. Fila fra Macen er hentet tilbake til skyen og lest der; md5 var den samme som da den ble lest på Macen kl. 15:38Z.

| Fil | Rendret: byte, md5 | Utdatamappen: byte, md5 | På Macen: byte, md5 | Skrevet til Macen (filtid) |
|---|---|---|---|---|
| `figur/leddene-v3.png` | 221 525, `3c85797ce89710f9449cbcbd77fefe05` | 227 295, `e02f574987c22ded7834112581561cde` | 227 295, `e02f574987c22ded7834112581561cde` | 13:31:11Z |
| `figur/leddene-v4.png` | 299 730, `c3ca08f2fb36cfb97297345965781cd3` | 299 730, `c3ca08f2fb36cfb97297345965781cd3` | 305 500, `a803adbf83612320c4a31cb580dd9fc2` | 15:32:19Z |
| `images/godkjenning-paa-macen-v1.png` | 428 325, `bfb1de5f13d2b71edb54e3c5f09797c1` | 434 095, `8fd23cbe5cd71eb4207754ad0395a7f8` | 434 095, `8fd23cbe5cd71eb4207754ad0395a7f8` | 13:31:09Z |
| `images/mottaker-oppsett-v1.png` | 278 365, `a8dabd6e5c933855fa6b71486b54d3c0` | 284 135, `9e6ca9ea30fca72c4bfe654c23c68902` | 284 135, `9e6ca9ea30fca72c4bfe654c23c68902` | 13:31:10Z |

| Fil | Blokker, rendret | Blokker, på Macen | `IDAT` satt sammen, md5 | Pakket ut: byte, md5 |
|---|---|---|---|---|
| `figur/leddene-v3.png` | IHDR x1 (13), IDAT x55 (220820), IEND x1 (0) | IHDR x1 (13), caBX x1 (5758), IDAT x55 (220820), IEND x1 (0) | `5f01993dd1deb8047972f233f00cf649` | 4 728 845, `d12f64cd8d97d2dc7a20137a89f75ab3` |
| `figur/leddene-v4.png` | IHDR x1 (13), IDAT x74 (298797), IEND x1 (0) | IHDR x1 (13), caBX x1 (5758), IDAT x74 (298797), IEND x1 (0) | `1138df2f2569f25fdef51d4469b41f05` | 5 469 255, `2b70b939cc9bf834b20dbc237dea20d1` |
| `images/godkjenning-paa-macen-v1.png` | IHDR x1 (13), IDAT x106 (427008), IEND x1 (0) | IHDR x1 (13), caBX x1 (5758), IDAT x106 (427008), IEND x1 (0) | `687714eaef788e353ae968fbb48ef50b` | 8 696 325, `8f6191d3b33f4faf2ca63ed0ec39ae2d` |
| `images/mottaker-oppsett-v1.png` | IHDR x1 (13), IDAT x69 (277492), IEND x1 (0) | IHDR x1 (13), caBX x1 (5758), IDAT x69 (277492), IEND x1 (0) | `b870521b26a7074d2b2ff3599ddf82fe` | 5 196 840, `0e456730e6e9131ff61a9906a4a9bf56` |

Det målingen viser:

- Fila på Macen er 5 770 byte større enn den rendrede, for alle fire: én blokk med navnet `caBX` og 5 758 byte innhold, lagt rett etter `IHDR`, pluss 12 byte for blokkens lengde, navn og sjekksum.
- Bildedataene er de samme. `IDAT`-blokkene satt sammen har samme md5 på alle tre stedene for alle fire filene, og de pakker ut til samme data.
- For tre av de fire har kopien i utdatamappen samme md5 som fila på Macen, altså med blokken. For den fjerde, `figur/leddene-v4.png`, hadde kopien i utdatamappen ingen `caBX`-blokk kl. 15:40Z (samme md5 som den rendrede fila), og heller ikke kl. 15:50Z. Fila på Macen var skrevet kl. 15:32Z, med blokken.
- Kl. 15:50Z hadde 17 av de 18 PNG-filene som lå i utdatamappen, en `caBX`-blokk. Den ene uten var `figur/leddene-v4.png`. Lista fra den lesningen viser blokktypene uten `IDAT` for hver fil; skriptet som laget den, er ikke lagret. Samme telling kl. 15:40Z ga også 17 med og 1 uten, men den utskriften er ikke lagret som fil.
- Kopien av `figur/leddene-v4.png` i utdatamappen har filtid 15:31:57Z, altså før fila ble skrevet til Macen. De tre andre kopiene har filtid 13:24:49Z.
- Blokken er forskjellig i de fire filene (fire ulike md5).

## Hva blokken inneholder

Lesbare strenger i blokken (utskrift med id-er skjult): `c2pa.claim.v2`, `c2pa.actions.v2`, `c2pa.ingredient.v3`, `c2pa.hash.data`, `c2pa.signature`, handlingen `com.anthropic.claude.provided` med en beskrivelse som begynner «Claude provided this file at the request of a user», `claim_generator_info` med navnet «Anthropic Files» og versjon 1.0.0, og navnene «Anthropic Content Credentials Root CA» og «Anthropic Claude Content Signing». Hver blokk har to id-er (`urn:c2pa:…` og `xmp:iid:…`); de er ikke gjengitt her. Ingen e-postadresse står blant de lesbare strengene. Det binære innholdet er ikke tolket.

## Tekstfiler

Ni tekstfiler skrevet til denne mappen samme dag hadde samme md5 i skyen og på Macen (målt kl. 15:41Z):

- `PLAN.md` `a6cb2d4cbbb2e7c30bd0e74ea42c6618`
- `dataflow.md` `0370c8106669d8dc8fde7272c515b1a7`
- `contract/README.md` `84cd33a8e267d08ad6707aa373fb62d8`
- `contract/relasjonscelle-avtale.json` `692dc8bc040a5dc6a96bfbd2509bc59c`
- `handoff/README.md` `8b37ec1a9020a6f3355f7756ecd7e449`
- `handoff/BOLK-1-OPPDRAG.md` `121ba9dbcf4717dafe40f5a9f0ee3574`
- `handoff/BOLK-1-KOEPROMPT.md` `c3e437c5c7346bd06b0c0fca2629955b`
- `figur/leddene-v4.html` `c76b8e619b980153aaa04b89a9af3081`
- `STATUS.md` `a56b06ed22e2415ca391080281a16ce7`

## Ikke målt

- Hvilket steg som legger blokken til, og når. Tre kopier i utdatamappen hadde den, én hadde den ikke.
- Hvordan hver av de fire filene ble sendt (med sti fra utdatamappen, eller etter at fila var vist i samtalen). Det er ikke bevart.
- Om andre bildeformater enn PNG får et tilsvarende merke.

## Følge

- Avvikende md5 for en PNG som er levert til Macen, betyr ikke at bildet er endret. Sammenlign `IDAT`-dataene eller pikslene.
- md5 for et levert bilde tas fra den leverte fila, ikke fra arbeidsmappen og ikke fra utdatamappen.

Skriptet som leste blokkene, ligger ved siden av denne fila: `panel/png_blokker.py` (bare standardbiblioteket; `python3 png_blokker.py <fil.png> …`). Det skriver størrelse, md5, blokkene i rekkefølge og md5 av `IDAT`-dataene, så to kopier kan holdes mot hverandre. Utskriftene og skriptet som leste strengene i blokken, ligger i trådens arbeidsmappe i skyen og er ikke lagret her.
