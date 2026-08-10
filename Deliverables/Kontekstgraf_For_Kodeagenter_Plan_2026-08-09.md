# Kontekstgraf for kodeagenter — plan

**Dato:** 2026-08-09
**Status:** Omfang og kontekstkontrakt besluttet 2026-08-09 (§8, §8b). Ikke påbegynt.
**Avhengighet:** submodulen `Binding/CellProtocolDocuments` bør fjernes før Fase 1 (§10).
**Utløst av:** Spørsmål om graflagring kan holde midlertidig kontekst slik at kodeagenter slipper å sende hele transkriptet til modellen hver tur.

---

## 1. Formål og målekriterium

**Formål:** En kodeagent skal kunne løse en oppgave i HAVEN-repoene med et kontekstvindu som inneholder *det oppgaven trenger*, hentet deterministisk fra en graf, i stedet for et akkumulert transkript av alt den har sett underveis.

**Goal (målbart, terminalt):** På et fast sett reelle oppgaver skal agenten med grafflaten bruke færre tokens til ferdig løsning enn baseline, **uten** lavere løsningsrate og **uten** flere turer.

Dette er ett mål med tre ledd, og alle tre må måles samtidig. Måler du bare tokens, optimaliserer du deg til en agent som er billig og ubrukelig. Måler du bare løsningsrate, har du ingen grunn til å bygge dette i det hele tatt.

**Ikke-mål:**
- Erstatte prompt-caching. Grafen konkurrerer ikke med caching, den samspiller dårlig med den (se §6.2).
- Bygge en generell kodesøkemotor. Seleksjon for et kontekstvindu er en annen oppgave enn søk for et menneske.
- Semantisk/embedding-basert gjenfinning i første omgang. Strukturkanter først; likhet er en fallback vi legger til hvis strukturen viser seg utilstrekkelig.

---

## 2. Utgangspunkt: hva som allerede finnes

### 2.1 Lagring og API — riktig form

`GraphStoreCell` (3228 linjer) har allerede handlingsflaten en kontekstserver trenger:

| Handling | Hva den gir oss |
|---|---|
| `graph.node.upsert` / `graph.edge.upsert` | Skriveflate med `id`, `kind`, `label`, fritt `properties`-objekt |
| `graph.node.list` | Filtrering på `ids`, `kind`, `text`; paginering, tak 1000 |
| `graph.edge.list` | Filtrering på endepunkt, retning, relasjon |
| `graph.neighbors` | Avgrenset traversering, `depth` 1–6, `direction`, `relationship`, `limit` |
| `graph.subgraph` | Nabolagsuttrekk, `depth` default 2, `limit` opp til 2000 |
| `graph.path.exists` | Kobling mellom to noder |
| `graph.state` | Lesetilgang til hele tilstanden |

Hele flaten er allerede grant-styrt (`GraphStoreCell.swift:216`–`236`), altså identitetsavgrenset per handling. Det betyr at en agent kan få `r---` på henting og ingen skrivetilgang til strukturgrafen, uten nytt policyarbeid.

`EntityGraphStorageAdapter` (`EntityGraphStorageAdapter.swift:33`) gir i tillegg noder, kanter, **proofs**, **sources** og en append-only **hendelseslogg** over SQLite. Provenienslaget er allerede der — vi trenger det for å svare på «hvorfor lå denne noden i vinduet».

**Konsekvens for planen:** ingen protokollendring i CellProtocol-kjernen. `properties` er et fritt objekt, så digest og payload-referanse (§4.2) får plass uten skjemaendring.

### 2.2 Skala — feil størrelsesorden

Dette er det avgjørende funnet.

`listNodes` (`GraphStoreCell.swift:1219`) holder hele grafen i minne (`nodesByID`), og gjør per kall:
- lineær kopiering av alle noder til en array,
- substring-match mot `"\(label)\n\(String(describing: properties))"` for tekstfilter,
- full sortering av alle treff,
- deretter paginering.

`SQLiteEntityGraphStorage` har indekser på `kind_domain`, `edges_from`, `edges_to` og `events_kind_time` — men ingen fulltekstindeks, og filtreringen skjer uansett i Swift-minnet, ikke i SQL.

Det holder fint for en prosjektgraf med hundrevis av noder. Indeksmålet her er en annen størrelsesorden:

| Repo | Filer | Linjer | Merknad |
|---|---|---|---|
| CellScaffold | 779 | 433 238 | `Sources` + `Tests` |
| CellProtocol | 473 | 143 847 | `Sources` + `Tests` |
| Binding | 203 | 138 134 | blandet: Xcode-mål (`Binding` 55, `BindingTests` 19, `BindingUITests` 2, `Cells` 8) + SPM-pakken `HavenAgentD` (`Sources` 83, `Tests` 33) |
| **Sum** | **1455** | **715 219** | |

Anslagsvis 25 000–50 000 symbolnoder og et par hundre tusen kanter. Lineær skanning med `String(describing:)` per node per kall er ikke levedyktig der, og det finnes ingen rangering — `node.list` sorterer på `updatedAt`, som er meningsløst som relevansmål.

**Beslutning:** vi bygger *ikke* på `GraphStoreCell`s nåværende lagring. Vi gjenbruker handlingsformen og `EntityGraphStorageAdapter`-protokollen, men med en ny backend som pusher filtrering ned i SQL og legger til FTS5. Se Fase 1.

### 2.3 Presedens for flaten

- `CellProtocolDocuments/Tools/HavenDocsMCP/haven_docs_mcp.py` — read-only MCP-flate over HAVEN-innhold. Mal for §5.
- `Binding/HavenAgentD/Sources/HavenAgentDMCP` — MCP-server i Swift, med dokumentert overflate i `HavenAgentDMCPServerSurface.md`.
- `CellScaffold/scripts/setup_haven_gui_exchange_mcp.py` — installasjonsmønster.

---

## 3. Arkitektur

Fem lag. Lag 1–2 er deterministiske og krever ingen modell. Lag 4–5 er der intelligensen sitter, og der risikoen sitter.

```
[5] Arbeidssett-politikk    velger hva som materialiseres i vinduet, med tokenbudsjett
[4] Sesjonslag (episodisk)  observasjoner, hypoteser, beslutninger — det «midlertidige»
[3] Hentflate (MCP)         budsjetterte, selvrapporterende svar til agenten
[2] Digestlag               ≤1 linje per node i vinduet, payload utenfor
[1] Strukturindeks          fil/symbol/test/commit + defines/references/covers/changed-with
```

**Invariant gjennom alle lag:** ingenting forsvinner, ting *dereferereres*. En node som kastes ut av vinduet etterlater seg ID + digest + kant. Agenten kan alltid hente kroppen tilbake deterministisk. Det er hele forskjellen mot tapsbehandlet compaction slik Codex og Claude Code gjør det i dag.

---

## 4. Faser

Hver fase har en gate. Gaten er ikke «koden kompilerer», den er et tall eller en observerbar egenskap. Fase N+1 startes ikke før gate N er passert.

### Fase 0 — Målestokk

**Uten dette er resten ufalsifiserbart.** Bygges først, ikke sist.

Innhold:
- 12–20 reelle oppgaver hentet fra git-historikken i CellScaffold/CellProtocol: en feilende test, en kontraktsendring som treffer flere renderere, en ny celle etter mønster, en regresjon med stack trace, et parity-avvik mellom Binding og CellScaffold. Hver oppgave har en verifiserbar ferdigtilstand (test grønn, diff-ekvivalens mot faktisk commit).
- Kjøreharnisk som kjører en agent mot en oppgave i en ren worktree og logger: totale input-tokens, output-tokens, antall turer, verktøykall, og om ferdigtilstanden ble nådd.
- Baseline: dagens Codex og dagens Claude Code, tre kjøringer per oppgave per agent.

Plassering: `CellProtocolDocuments/Tools/ContextBench/`.

**Gate 0:** baseline-tallene reproduserer innenfor ±15 % over tre kjøringer. Hvis variansen er større enn den forventede gevinsten, er benken ikke god nok til å avgjøre noe, og den må strammes før Fase 1.

### Fase 1 — Strukturindeks

Deterministisk uttrekk. Ingen modell involvert.

Noder: `file`, `symbol`, `test`, `commit`, `doc`, `cell`, `configuration`.
Kanter: `defines`, `references`, `imports`, `covers`, `changed-with`, `documents`.

Kilder:
- Swift: SourceKit-LSP (`textDocument/documentSymbol`, `references`) — allerede tilgjengelig i toolchainen.
- Python: `ast`-modulen for PyCellProtocol og Tools.
- JSON/CellConfiguration: eksisterende skjemakunnskap fra `cellconfiguration-skeleton-authoring`.
- `changed-with`: `git log --name-only`, co-endring over siste ~2000 commits, terskel på støtte.

Lagring: ny `CodeGraphStorage` som implementerer `EntityGraphStorageAdapter`, men med
- filtrering og paginering i SQL, ikke i minnet,
- FTS5-indeks over `label` + utvalgte `properties`-felter,
- indeks på `(kind, updatedAt)` og `(relationship, fromNodeID)`.

Ny celle `CodeGraphIndexCell` i `CellScaffold/Sources/App/Cells/CodeGraph/`, native etter regelen om native HAVEN-celler. Den eier skriving; ingen ekstern prosess skriver direkte til basen.

Cellen indekserer tre repoer, men bor i ett. Derfor:
- Indekserte røtter er **konfigurasjon**, ikke hardkodet — cellen har ingen kunnskap om at den tilfeldigvis ligger i CellScaffold.
- Basen legges **utenfor** de indekserte repoene (`~/Library/Application Support/HAVEN/codegraph.sqlite`, konfigurerbar). En indeks som ligger i et repo den indekserer, indekserer sine egne skrivinger.
- Ingen statisk delt instans. Lagringsstien injiseres ved konstruksjon. Dette er ikke pedanteri: CellScaffold-suiten har allerede lekkasje av global tilstand mellom suiter, og en SQLite-singleton er nøyaktig formen som gjør det verre.

Merk: `GraphStoreCell` normaliserer nodetyper med en hardkodet `switch` (`GraphStoreCell.swift:2941`). Den nye cellen skal *ikke* arve det mønsteret — nodetyper konfigureres, ikke kompileres inn.

#### 4.1.1 Kryssrepo: identitet, duplikater og versjonsdrift

Dette er der beslutningen om alle tre repoene koster, og der den betaler.

**Node-IDer må være repo- og versjonskvalifiserte.** Formen er `{repo}:{path}#{symbol}@{blobHash}`. Uten `repo` kolliderer `CellScaffold:Sources/.../GraphStoreCell.swift` med sitt eget speil i et annet repo; uten `blobHash` kan ikke Fase 2 avgjøre om en digest er foreldet.

**Duplikatfellen.** CellProtocol finnes fysisk på seks steder i treet:

```
HAVEN/CellProtocol                              1632ed6   ← arbeidskopi
HAVEN/CellScaffold/.build/checkouts/CellProtocol      1632ed6
HAVEN/Binding/HavenAgentD/.build/checkouts/CellProtocol   0ef84bc
HAVEN/DiMyMint/.build/checkouts/CellProtocol          edf8335
HAVEN/DiMyMicropayments/.build/checkouts/CellProtocol
HAVEN/DiMyMicropayments/exports/.../CellProtocol
```

I tillegg er `CellProtocolDocuments` submodul i Binding på `e138166`, mens toppnivået står på `771b625`.

Dette er ikke en opprydningssak — SPM-checkouts *skal* stå på pinnet versjon. Men det betyr at «samme symbol» ikke finnes. Binding kompilerer mot en annen CellProtocol enn CellScaffold gjør.

**Regel:** `.build/checkouts` indekseres **aldri** som førsteklasses kilde. Kun de tre arbeidskopiene er kilde. Hver konsumentpakke får i stedet en `dependency-pin`-node (`repo` + `commit` + `resolvedAt`) og en `compilesAgainst`-kant til den.

**Kapabiliteten dette gir oss** — og som alene forsvarer kryssrepo-omfanget: når en agent henter en CellProtocol-signatur mens den jobber i Binding, kan `graph_expand` svare *«Binding kompilerer mot CellProtocol 0ef84bc; du leser 1632ed6; denne signaturen er endret mellom dem»*. Det er en feilklasse som i dag koster reelle feilsøkingstimer, og som ingen agent fanger opp i dag.

**Kryssrepo-kanter** utledes deterministisk, ikke ved likhet:
- `co-implements` — to symboler i ulike repoer som begge `references` samme CellProtocol-type. Dette er paritetskanten mellom Binding-SwiftUI-rendereren og CellScaffold-web-rendereren for samme `SkeletonElement`-case.
- `compilesAgainst` — konsumentpakke → `dependency-pin`.
- `mirrors` — submodulsti → toppnivåsti for samme repo, med begge commits. *Utgår hvis `Binding/CellProtocolDocuments` fjernes først (§10) — den er eneste kjente tilfelle.*

**Gate 1:**
- Fullindeksering av alle tre arbeidskopiene under 20 minutter.
- Inkrementell oppdatering ved én filendring under 2 sekunder.
- ≥95 % av symbolreferanser i et stikkprøvesett på 200 oppslag resolverer til riktig definisjonsnode.
- `node.list` med tekstfilter over full indeks svarer under 100 ms.
- **Null noder fra `.build/checkouts` eller `exports/`** i indeksen.
- Minst 20 `co-implements`-kanter mellom Binding og CellScaffold, stikkprøvekontrollert mot kjente paritetspar fra `binding-skeleton-parity-testing`.

### Fase 2 — Digestlag

Hver node får i `properties`:
- `digest`: ≤120 tegn, én linje.
- `ref`: `{path, startLine, endLine, contentHash}` — *ikke* innholdet.
- `cost`: estimert tokenkostnad ved full utfolding.

Digestene lages deterministisk der det går: signaturlinje for symboler, testnavn + antall assertions, første overskrift + antall seksjoner for dokumenter. Modellgenererte digester kun der deterministiske er verdiløse (prosadokumenter), og da med `digestSource: "model"` slik at de kan revurderes.

`contentHash` er invalideringsmekanismen: endres filen, merkes digesten `stale` og payload-ref ugyldig til reindeksering.

**Gate 2:** et arbeidssett på 200 noder — digester og ingen payloads — måler under 4000 tokens. Hvis vi ikke klarer det, er digestene for lange og hele premisset faller.

### Fase 3 — Hentflate

MCP-server `havengraph`, read-only mot strukturgrafen, modellert på `haven_docs_mcp.py`.

Verktøy:

| Verktøy | Inn | Ut |
|---|---|---|
| `graph_seed` | fritekst / stack trace / diff | rangerte kandidat-node-IDer + digester |
| `graph_neighborhood` | `center`, `depth`, `budget_tokens` | digester innenfor budsjett |
| `graph_expand` | `nodeID[]` | full payload for utvalgte noder |
| `graph_path` | `from`, `to` | korteste kantsti, med relasjonsnavn |
| `graph_impact` | `nodeID` | hva som brekker hvis denne endres (`references` + `covers` + `changed-with`) |

To designkrav som avgjør om dette funker:

1. **Hvert svar er tokenbudsjettert.** Kalleren oppgir budsjett; serveren fyller det og stopper.
2. **Hvert svar rapporterer hva det utelot.** `"elided": {"nodes": 47, "atDepth": 3, "reason": "budget"}`. Agenten skal kunne se at den ikke har hele bildet, og be om mer. Dette er motgiften mot den tause seleksjonsfeilen (§6.3).

**Gate 3:** en agent løser minst 3 av benkoppgavene med *kun* grafverktøy — ingen `cat`, `grep`, `find`. Feiler dette, mangler hentflaten en primitiv, og den skal identifiseres før vi går videre.

### Fase 4 — Sesjonslag (det midlertidige) — *i første leveranse*

Her ligger den faktiske «midlertidige kontekstlagringen» fra det opprinnelige spørsmålet.

Per agentøkt en episodisk subgraf:
- Noder: `observation` (verktøykall + resultat), `hypothesis`, `decision`, `edit`, `goal`.
- Kanter: `touched` (episodisk → struktur), `supports` / `contradicts` (episodisk → hypotese), `supersedes` (nyere observasjon utdaterer eldre).
- Hendelsesloggen i `EntityGraphStorageAdapter.appendEvent` brukes som den er.

`supersedes` er poenget: når agenten leser samme fil for tredje gang, skal de to første observasjonene være dereferert, ikke gjentatt. Det er den største enkeltposten i «søppelet» Codex sender.

Retensjon: sesjonssubgrafer får TTL og eksplisitt `graph_session_close` som enten forkaster eller promoterer utvalgte noder til varig prosjektgraf (en `decision` med begrunnelse er verdt å beholde; 400 `observation`-noder er ikke).

**Gate 4:** replay av en lagret sesjon rekonstruerer identisk arbeidssett per tur. Determinisme her er en forutsetning for å kunne feilsøke seleksjon i det hele tatt, og den passer contract-testing-kulturen i repoet.

### Fase 5 — Arbeidssett-politikk

Selve seleksjonsfunksjonen. Vinduet bygges hver tur som:

```
STABILT PREFIKS   systemprompt + grafskjema + verktøydefinisjoner + pinnede noder (mål, oppgave, kontrakter)
                  — endres aldri innenfor en økt, cachebart
VOLATILT SUFFIKS  arbeidssett fra traversering rundt gjeldende fokus
                  + digester for periferien
                  + siste N turer ordrett
```

Båndbudsjetter, foreslåtte startverdier: pinnet 15 %, utfoldede payloads 45 %, digester 25 %, ordrett historikk 15 %.

Hentplanleggeren — «hva er fokusnoden nå, hvilke relasjoner er relevante for denne oppgavetypen» — kjøres av en liten modell, i samme form som formålsdekomponeringen (pre-parse → shortlist → constrained valg). Den skal aldri generere fri tekst inn i vinduet, bare velge node-IDer og relasjonsnavn fra en lukket mengde.

**Gate 5:** på benken fra Fase 0, målt mot baseline: færre fakturerbare input-tokens til ferdig, løsningsrate ikke lavere, antall turer ikke høyere. Alle tre. Dette er hovedgaten for hele prosjektet.

**Ablasjonskrav.** Siden sesjonslaget er med fra start, måler Gate 5 to mekanismer samtidig — presis henting (Fase 3) og historikk-dereferering (Fase 4). Det må derfor kjøres tre armer på benken:

| Arm | Fase 3 | Fase 4 | Svarer på |
|---|---|---|---|
| A | ✓ | — | Er presis henting alene nok? |
| B | — | ✓ | Er historikk-dereferering alene nok? |
| C | ✓ | ✓ | Er de additive eller overlappende? |

Uten dette vet du ved gevinst ikke hvilken halvdel som tjente den, og ved tap ikke hvilken du skal kutte. Arm B er billig å kjøre når A og C først finnes, og er den som avgjør om strukturindeksen i Fase 1 var verdt 20 minutters indekseringstid i det hele tatt.

### Fase 6 — Integrasjon

- Claude Code: MCP-server + en skill som instruerer grafbruk fremfor `cat`/`grep`, og en hook som reindekserer ved filendring.
- Codex: samme MCP-server; `AGENTS.md`-instruks i hvert repo.
- HAVEN Co-Pilot Chat: samme celle, direkte over CellProtocol uten MCP-hopp.
- Invalidering: filvakt som marker noder `stale` ved endring. Hendelsesdrevet, ikke polling.

**Gate 6:** en uke reell bruk uten at en agent tar en feilbeslutning som kan spores til en foreldet digest.

---

## 5. Hva som ikke bygges, og hvorfor

| Utelatt | Begrunnelse |
|---|---|
| Embeddings / vektorsøk | Strukturkanter er en sterkere seleksjonsfunksjon for kode. Legges til som `graph_seed`-fallback først hvis Gate 3 feiler på gjenfinning, ikke før. |
| Egen grafdatabase (Neo4j o.l.) | SQLite + FTS5 holder i denne størrelsesordenen, og `EntityGraphStorageAdapter` finnes allerede. Ny driftsavhengighet uten påvist behov. |
| Modellgenererte sammendrag i strukturlaget | Ikke-deterministisk, dyrt å reindeksere, umulig å verifisere. Kun der deterministisk uttrekk er verdiløst. |
| Automatisk skriving til strukturgrafen fra agenten | Agenten får `r---` på struktur, skrivetilgang kun til sin egen sesjonssubgraf. En agent som kan forgifte indeksen sin er verre enn ingen indeks. |

---

## 6. Risikoer

### 6.1 Skalaen i eksisterende lagring
Behandlet i §2.2. Håndteres ved ny backend i Fase 1, ikke ved å strekke `GraphStoreCell`.

### 6.2 Caching arbeider mot oss
Codex' repetisjon er dyr i oppmerksomhet, men billig i kroner så lenge prefikset er stabilt. Graf-drevet omskriving av historikken invaliderer cachen, og regningen kan gå opp mens tokentellingen går ned.

Håndteres av prefiks/suffiks-delingen i Fase 5, og ved at Fase 0-benken måler **fakturerbar** kostnad med cache-treff, ikke rå tokentelling. Hvis vi bare teller tokens, kan vi «vinne» og likevel betale mer.

### 6.3 Taus seleksjonsfeil
Manglende kontekst ser ut som en dum modell, ikke som en trunkeringsfeil. Håndteres av `elided`-rapportering (Fase 3) og av at `graph_neighborhood` alltid oppgir hva som lå like utenfor budsjettet. Benken skal inneholde minst tre oppgaver der riktig svar krever en node som *ikke* ligger i det åpenbare nabolaget — ellers måler vi ikke dette i det hele tatt.

### 6.4 Foreldet indeks
En foreldet digest er verre enn ingen kontekst, fordi agenten stoler på den. `contentHash` + `stale`-flagg i Fase 2, filvakt i Fase 6. Regelen er: heller nekte å svare enn å levere en digest som ikke matcher hash.

### 6.5 Kompleksitetsbudsjett
Dette er femseks nye komponenter, og med sesjonslaget inne fra start er ingen av dem strøket. Rekkefølgen er likevel valgt slik at Gate 3 er et gyldig stoppunkt: da har du et presist hentverktøy over alle tre repoene, som har verdi uavhengig av om Fase 4–5 fullføres. Sesjonslaget er med i leveransen, men ikke på den kritiske stien fram til første brukbare resultat.

### 6.6 Versjonsdrift mellom repoene
Behandlet i §4.1.1. Den underliggende risikoen er at indeksen presenterer én sannhet der det finnes tre. Håndteres av `dependency-pin`-noder og advarsel ved `graph_expand`. Restrisiko: hvis pinnene endres uten reindeksering, advarer vi *feil vei*, som er verre enn ikke å advare. `Package.resolved` må derfor inn i filvakten i Fase 6 på linje med kildefiler.

### 6.7 Testisolasjon i CellScaffold
Suiten er ikke grønn i dag på grunn av lekkasje av global tilstand mellom suiter. En ny celle med persistent SQLite-tilstand kan gjøre dette målbart verre og bli feilaktig utpekt som årsak — eller skjule seg bak eksisterende rekkefølgeavhengige feil. Håndteres ved injisert lagringssti, ingen statiske instanser, og at `CodeGraphIndexCell`-testene kjøres som egen suite med egen midlertidig base. Målepunkt: antall rekkefølgeavhengige feil i CellScaffold-suiten skal ikke øke etter Fase 1.

---

## 7. Rekkefølge og avhengigheter

```
Fase 0 (benk) ──> Fase 1 (indeks) ──┬─> Fase 2 (digest) ──> Fase 3 (MCP) ──┬─> Fase 5 (politikk) ──> Fase 6
                                    │                                       │      ↑ ablasjon A/B/C
                                    └─> Fase 4 (sesjon) ────────────────────┘
```

Fase 4 kjøres parallelt med Fase 2–3 så snart Fase 1 er i mål. Sesjonslaget avhenger av at strukturnoder har stabile IDer, ikke av at de har digester — og med den ID-formen §4.1.1 slår fast, er den avhengigheten oppfylt ved Gate 1.

Kritisk sti til første brukbare resultat: **0 → 1 → 2 → 3**. Gate 3 er et gyldig stoppunkt. Fase 4 er i leveransen, men forsinker ikke det stoppunktet, og arm A i ablasjonen kan måles før Fase 4 er ferdig.

---

## 8. Beslutninger

Avgjort av Kjetil 2026-08-09:

| Valg | Beslutning | Konsekvens i planen |
|---|---|---|
| Indeksomfang | **Alle tre repoene** — CellScaffold, CellProtocol, Binding | §4.1.1 i sin helhet: repo+versjonskvalifiserte IDer, `dependency-pin`-noder, `co-implements`-kanter, utvidet Gate 1 (20 min, null checkout-noder, ≥20 paritetskanter) |
| Plassering | **`CellScaffold/Sources/App/Cells/CodeGraph/`** | Indekserte røtter og lagringssti er konfigurasjon; base utenfor indekserte repoer; injisert sti pga. §6.7 |
| Sesjonslag | **Med i første leveranse** | Fase 4 parallelt med 2–3; ablasjonskrav A/B/C i Gate 5; Gate 3 forblir gyldig stoppunkt |

Kryssrepo-omfanget viste seg å være mer enn en volumøkning: det avdekket at CellProtocol eksisterer i tre ulike versjoner samtidig på maskinen (§4.1.1). Drift-advarselen som følger av `dependency-pin`-noder er sannsynligvis den enkeltkapabiliteten med høyest verdi i hele planen, og den finnes ikke uten dette omfanget.

**Avledede valg tatt underveis** (endres fritt, ingen blokkering):
- `DiMyMint` og `DiMyMicropayments` indekseres ikke som kilde, men får `dependency-pin`-noder. Kostnaden er én commit-oppslag per repo, og de får drift-advarsler gratis.
- Reindeksering eies av **HavenAgentD**, ikke av en hook i den enkelte agenten. Hendelsesdrevet filvakt finnes allerede der, det er én vakt uansett hvor mange agenter som kjører, og det følger preferansen for hendelsesdrevet venting fremfor polling.

## 8b. Repo-kontekst er påkrevd

**Besluttet 2026-08-09: hvert oppslag krever repo-kontekst. Uten den feiler flaten eksplisitt — den gjetter aldri.**

Det finnes ingen «sann» CellProtocol-versjon i dette treet (§4.1.1), så et svar uten repo-kontekst er ikke et upresist svar, det er et udefinert spørsmål. Flaten skal si det.

**Kontrakt:**
- Alle `graph_*`-verktøy tar `context: {repo, commit?}` som **påkrevd** felt. Utelates det, er svaret en feil — ikke et default.
- Tvetydig oppslag feiler med **enumerering**, ikke med et valg:
  ```json
  { "error": "ambiguous_symbol",
    "symbol": "CellResolver.validateAccess",
    "candidates": [
      {"repo": "CellProtocol", "commit": "1632ed6", "role": "arbeidskopi"},
      {"repo": "Binding/HavenAgentD", "compilesAgainst": "0ef84bc", "signatureDiffers": true}
    ],
    "hint": "angi context.repo" }
  ```
- `signatureDiffers` beregnes fra `blobHash` i node-IDen. Er den `true`, er valget av repo-kontekst ikke en formalitet, og feilmeldingen sier det.

**Prisen** er flere rundturer, og den betales av sesjonslaget: `graph_session_open` setter `defaultContext` én gang, og senere kall arver den. Kravet forsvinner ikke — det oppfylles fra sesjonstilstand i stedet for per kall. Dette er en direkte gevinst av at Fase 4 er med i første leveranse; uten sesjonslaget hadde beslutningen kostet merkbart i ergonomi.

**Prinsippet dette følger:** en flate som gjetter, gjetter riktig i de tilfellene du tester og feil i de du ikke tester. Eksplisitt feil er den eneste varianten som er lik i begge. Dette er samme resonnement som `elided`-rapporteringen i §6.3 — vi gjør seleksjonsfeil hørbare i stedet for tause.

**Tillegg til Gate 3:** et tvetydig kryssrepo-oppslag skal returnere enumerert feil, ikke ett repos svar. Testes eksplisitt, ikke antas.

---

## 9. Første konkrete steg

Fase 0, oppgavesettet. Uten benken er alt annet meningsytring. Konkret:

1. Velg 16 commits siste seks måneder der endringen er ikke-triviell og har tilhørende test. Fordeling nå som omfanget er alle tre repoene: 7 CellScaffold, 4 CellProtocol, 3 Binding, **2 kryssrepo** (en paritetsendring som treffer både Binding-renderer og CellScaffold-renderer, og en CellProtocol-signaturendring som brekker en konsument).
   De to kryssrepo-oppgavene er ikke pynt. De er de eneste som kan vise om §4.1.1 tjener noe, og de skal være blant de tre som krever en node utenfor det åpenbare nabolaget (§6.3).
2. Skriv `ContextBench/tasks/*.yml` med oppgavetekst, ren utgangspunkt-commit per repo, og verifikasjonskommando.
3. Skriv `ContextBench/run.py`: worktree, kjør agent, logg fakturerbare tokens (med cache-treff), turer, verktøykall, utfall.
4. Kjør baseline — Codex og Claude Code, tre kjøringer per oppgave. Publiser tallene her i dokumentet.

Merk mot pågående git-opprydning: benken trenger rene worktrees per oppgave. Hvis opprydningstråden endrer branch-tilstand eller submodulpinner i mellomtiden, må utgangspunkt-commitene i steg 2 velges *etter* at den er ferdig, ellers peker de på tilstand som ikke lenger finnes.

---

## 10. Submodulen `Binding/CellProtocolDocuments` — funn og anbefaling

Undersøkt 2026-08-09 på forespørsel. **Anbefaling: fjern den.** Ingen byggavhengighet, men den leverer i dag foreldet dokumentasjon til agenter som tror den er kanonisk.

### 10.1 Hva som faktisk refererer til den

| Referanse | Type | Bryter ved fjerning? |
|---|---|---|
| `Binding.xcodeproj/project.pbxproj:39,160` | `PBXFileReference`, `lastKnownFileType = folder`, i en gruppe | Nei — mappereferanse for navigasjon. Ikke compile source, ikke resource phase. |
| `Binding.xcworkspace/contents.xcworkspacedata:8` | `location = "group:CellProtocolDocuments"` | Nei — workspace-gruppe. |
| `Binding/ChatWorkbenchParityCells.swift:7456` | `"group": .string("CellProtocolDocuments")` | Nei — **etikett i en datastruktur, ikke en filsti**. Falsk positiv. |
| Build-faser med `shellScript` | ingen treff i prosjektfilen | Nei |
| ~20 stier i `Documentation/`, `Prompts/`, `README.md` | prosalenker, dels `../CellProtocolDocuments/...`, dels `CellProtocolDocuments/...` | **Ja** — dette er hele kostnaden |

Verifisert: ingen Swift-kode leser en sti under submodulen, og `Scripts/` refererer den ikke i det hele tatt.

De som faktisk biter er agent-inngangene: `Prompts/SystemPrompt-Codex.md:6` og `Prompts/SystemPrompts.md:6` peker på `../CellProtocolDocuments/Prompts/CoreContext.md`. Fjernes submodulen uten å rette disse, mister Codex sin kjernekontekst når den jobber i Binding.

### 10.2 Grunnen til at den bør bort uansett

Submodulen er pinnet til `e138166` (2026-03-04, «Adjust formatting in Purpose and Interests chapter»). Den commiten er **ikke** forfar til `origin/main` — den ligger på en divergerende linje med 21 commits som ikke finnes i main.

Konsekvensen er at enhver agent eller person som følger `../CellProtocolDocuments/Book/...` fra Binding, i fem måneder har lest dokumentasjon fra en sidegren, ikke fra kanonisk kilde — mens `HAVEN/CellProtocolDocuments` ved siden av har den gjeldende. Det er samme feilklasse som versjonsdriften i §4.1.1, bare på dokumenter i stedet for kode, og den rammer nettopp de dokumentene som er ment å være kanoniske.

### 10.3 Ingenting går tapt

De 21 commitene er bevart flere steder:
- `archive/main` — `e138166` er forfar, 11 commits foran.
- `codex/cellprotocol-documents-wip-2026-05-03` og `main-local-history-20260704`, begge arkivert i dag av opprydningstråden under `origin/codex/archive-20260809/branches/...`.

Submodulens arbeidstre er rent (ingen ukommitterte endringer). Opprydningstråden har dessuten allerede laget `origin/codex/archive-20260809/binding-cellprotocoldocuments-stash-0-docs` (stash fra 2026-06-12, «Binding origin sync CellProtocolDocuments dirty docs») — altså er nøyaktig denne submodulen allerede på dens bord.

### 10.4 Utførelse

Ikke i denne planen, og ikke av denne tråden: å fjerne en submodul er en git-operasjon i et repo som opprydningstråden restrukturerer akkurat nå. Rekkefølge:

1. Opprydningstråden fullfører og fjerner submodulen (`git rm`, `.gitmodules`, `.git/modules/`, pbxproj-linje 39 + 160, workspace-linje 8).
2. De ~20 prosalenkene rettes. **Ikke** til en symlink mot `../CellProtocolDocuments`: `HavenAgentD/Package.swift` henter CellProtocol via git-URL, så Binding kan klones frittstående i dag, og en symlink ut av repoet ville brutt det.
3. `Prompts/SystemPrompt-Codex.md` og `SystemPrompts.md` får eksplisitt sti til søsken-utsjekk med feilmelding hvis den mangler — samme prinsipp som §8b: feil eksplisitt fremfor å lese noe foreldet.

**Effekt på planen:** `mirrors`-kanten i §4.1.1 var innført nettopp for denne submodulen. Fjernes den før Fase 1, utgår kanttypen, og dokumentnoder får én kanonisk kilde. Det er en forenkling av indeksen, ikke bare en opprydning.
