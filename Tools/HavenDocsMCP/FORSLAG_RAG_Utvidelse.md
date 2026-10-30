# Forslag: utvide dokumentasjons-RAG-en (ikke vedtatt)

Status: **forslag fra 2026-10-30, utarbeidet via Vegar til Kjetils team.** Ingenting her er vedtatt eller i bruk.
Dette dokumentet ligger bevisst utenfor `book_catalog.json`, så det ikke blir indeksert som kanonisk.
Prototypen i denne grenen er kjørt mot lokale kloner og en testfixture. Den er ikke vurdert av eierne av repoene.

Forslaget **utvider** kontrakten i `Book/15_Documentation_Discovery_and_RAG.md`. Det erstatter den ikke, og endrer ingen eksisterende URI, tool eller sitering.

## 1. Målt tilstand (verifisert 2026-10-30)

| Funn | Tall / observasjon |
|---|---|
| MCP-en registrert i en Claude-klient hos Vegar | **Nei.** `~/.claude.json` (global og prosjekter) og Claude Desktop-konfigen har bare `haven-correspondence`. Ingen `.mcp.json` i repoet. |
| Indeksert i dag | 59 dokumenter (56 i katalogen + `README-CellProtocol.md`, `DEVELOPERS.md`, `Gap_Analysis.md`), 60 ressurser. 49 er `Book/*.md`, 5 er `Manuals/`, 2 er `Deliverables/`. README sier «Book» og er dermed utdatert. |
| `status` | 27 `active`, 29 `draft`. Ingen `legacy`. |
| `owner`, `last_verified` | **0 av 56** har dem, selv om Book 15 krever dem. Ingen Markdown-fil har frontmatter. |
| Ikke i katalogen | `Book/33_Correspondence_First_Class.md` og `Book/34_Audio_Analysis_Cell.md`. De kan ikke finnes via MCP-en. |
| Tester | 7 av 7 grønne før endring. |
| Treff har alder? | Nei. Siteringen har sti, overskrift, linjer og dokumentstatus. Ingen commit, dato eller ferskhet. |

## 2. (a) `implementation_status`

Verdier: `implemented` · `decided` · `proposal` · `mixed` · `unknown`.
`unknown` er standard. Et dokument regnes aldri som `implemented` fordi det mangler etikett.

Ved siden av følger `status_basis`: `code-verified` · `doc-self-declared` · `unverified`.
Uten den ville «implemented» se likt ut enten noen har lest koden eller bare gjentatt det dokumentet selv sier.

**Hvor etiketten står** (første treff vinner):
1. Seksjonsmarkør `<!-- haven:implementation_status=decided -->` rett under en overskrift. Arves av undernivåer. Trengs fordi Book 37 blander kildebekreftet struktur (§1–6) og besluttet-men-ikke-implementert (§7).
2. Frontmatter i dokumentet: `implementation_status`, `status_basis`, `owner`, `last_verified`.
3. Katalogfeltene i `book_catalog.json` (Book-dokumenter).
4. `status_overrides` i `sources.json` for repoer vi ikke kan redigere (CellProtocol er read-only for oss). Hver oppføring har `evidence` og `set_by`.

**Hvem setter den:**
- Forfatteren av endringen setter `decided` eller `proposal`, i samme commit som teksten.
- `implemented` settes bare av den som har lest koden (eller kjørt testen) og skriver `status_basis: code-verified` med commit-hash i `evidence`. En AI-agent kan foreslå `implemented`, men ikke sette `code-verified`.
- Kode committes før dokumentasjonen som sier `implemented` (regelen fra skillet `cellprotocol-docs-and-rag-maintenance`).
- Når koden lander, flytter eieren `decided` → `implemented` i samme PR som koden, eller i en oppfølger som er lenket fra den.

**Kontroll:** `--lint-status` leter etter motsigelser (etikett `implemented`, tekst «ikke implementert») og lister `unknown`-dokumenter hvor teksten sier «ikke implementert». Det er regex og gir en arbeidsliste, ikke en dom.

## 3. (b) `CellProtocol/Docs/<emne>/` og CellScaffold som egne kildetyper

Konfigureres i `Tools/HavenDocsMCP/sources.json` (av som standard, på med `--with-sources`):

- `cp-docs`: `CellProtocol/Docs/**/*.md` og `*.schema.json`.
- `cellscaffold`: `AGENTS.md`, `Documentation/**/*.md`, `.claude/skills/*/SKILL.md`.
- Rot: `root` eller miljøvariabelen (`HAVEN_CELLPROTOCOL_ROOT`, `HAVEN_CELLSCAFFOLD_ROOT`). Ellers søsken til hovedklonen, også når MCP-en kjøres fra en worktree.

**Stabile id-er:** `doc_id = <kilde>/<sti>`, URI `haven-docs://<kilde>/<sti>[#anker]`.
Id-en følger stien, ikke commiten, så et svar kan siteres og slås opp igjen. Omdøpte filer får ny id. Forslag til oppfølging: `aliases` fra `git log --follow`.

**Siteringen får** `source`, `implementation_status`, og per treff `provenance`: `commit` (40 tegn), `committed_at`, `age_days`, `dirty` (filen er lokalt endret), `tracked`.

**Filtre:** `source` og `implementation_status` på `haven_docs_list` og `haven_docs_search`.
Eksempel fra kjøring: `implementation_status=decided` gir bare `V2-BESLUTTET-FORM.md` og Book 37 §7.

**Utelatt fra indeksen:**
- Globale mønstre: `**/haven-correspondence/**`, `**/correspondence-ledger*`, `**/*.eml` og lignende.
- Frontmatter `index: false`, eller `haven:index=false` i toppen av filen.
- `Documentation/ClaudeSkills/desktop-src/**` (kopier av skills), `Documentation/Operations/correspondence-*/**`.

Stibasert utelukking er grovt. `--lint-status` lister 5 indekserte filer hvis sti ligner korrespondanse: skillet `haven-assistant-correspondence`, `cp-docs/Docs/CorrespondenceAttachments.md`, og tre i `CellScaffold/Documentation/Operations/` (TLS/Nginx-status, `Korrespondanse_Invitasjoner_Runbook.md`, `Vegar_Victoria_Correspondence_Handoff_2026-07-31.md`). Den siste ser ut som en overlevering om en korrespondanse, ikke bare en funksjonsbeskrivelse, og bør sannsynligvis ut. Filnavn alene fanger ikke melding som ligger i filer uten slike navn; det er ikke undersøkt. **Eierne må avgjøre** hva som skal ut. På sikt er en tillatelsesliste per katalog tryggere enn en sperreliste.

## 4. (c) Ferskhet i selve svaret

Hvert søk og hver lesing får `freshness` per kilde, og en linje som siste rad i tekstsvaret, for eksempel:

> Ferskhet: CellScaffold: skill/correspondence-ledger-reference@924949d er 293 commits bak origin/main; ref sist hentet 2026-10-27 ⚠ klonen står på gren skill/…, ikke main; svaret gjenspeiler grenen.

Innhold: gren, HEAD, commit-dato, `behind`/`ahead` mot `origin/main`, når `FETCH_HEAD` sist ble skrevet, og advarsler:
- klonen står på en annen gren enn `main`,
- `origin/main`-refen er eldre enn 24 timer (tallet kan være for lavt),
- uten treff vises ferskheten likevel, så et tomt svar ikke ser autoritativt ut.

`--check-remote` (eller `HAVEN_DOCS_CHECK_REMOTE=1`) kjører `git ls-remote` (nettverk, 8 s tidsavbrudd) og sier fra når `origin/main` har commits klonen ikke har hentet. Uten det er tallet bare så riktig som siste `git fetch`.
Prototypen kjører aldri `fetch`, `pull` eller noe annet som endrer klonen.

## 5. Det prototypen viste mot de faktiske klonene (2026-10-30)

- `EntityData.v2.schema.json` ligger i `cp-docs` og er første treff på filnavnet, merket `[decided]` med commit `a40ceeb` (2026-09-25). Før måtte det letes etter manuelt.
- Book 37 viser `[mixed]` på kapittelnivå og `[decided]` på §7. Det er de to eneste Book-etikettene prototypen setter, begge hentet fra kapitlets egen tekst.
- `lint`: 605 dokumenter `unknown`, 3 `decided`, 1 `mixed`, 1 `implemented`. 121 `unknown`-seksjoner sier «ikke implementert» i teksten. Det er størrelsen på etikettjobben.
- Ferskhet: `CellScaffold` står på `skill/correspondence-ledger-reference`, 293 commits bak `origin/main`. `CellProtocol` stod på `arendalsuka-navigationbar-icon-support`, `origin/main`-refen var fra 2026-10-26 og fjernrepoet hadde commits klonen ikke hadde (`--check-remote` fanget det).
- `bcd45de` (`SkeletonElement.NavigationBar`-ikoner) ligger **bare** på feature-grenen `arendalsuka-navigationbar-icon-support`, ikke på `origin/main`. Et svar fra grenen vil derfor sitere kode som ikke er på main. Ferskhetslinjen viser grenen; den viser ennå ikke «commiten er ikke på main». Det er en åpenbar neste utvidelse.

## 6. Kjente begrensninger

- Fortsatt leksikalsk søk. Ingen vektorer.
- JSON-skjema er én seksjon. Treff er riktige, men snippeten er grov.
- `implemented` er ikke automatisk verifisert mot koden; prototypen har ingen kode-til-dokument-sjekk.
- Regex-linten gir både falske positive og falske negative (f.eks. `EntityData.review.schema.json`, merket `implemented`, har en beskrivelse som nevner «ikke implementert»; bør sjekkes av eier).
- Ytelse: 610 dokumenter parses én gang per prosess og cacher på filens mtime. Første søk tar rundt et sekund.
- Ikke dekket: CellScaffolds egne skills som *kilde til sannhet* (de indekseres bare som tekst), `Documentation/` i andre repoer (Binding, DiMyDocuments), og CellProtocolDocuments sin egen `Website/` og `Prompts/`.

## 7. Spørsmål til eierne

1. Er `CellProtocol/Docs` og `CellScaffold/Documentation` riktige kilder, og hvem eier hver?
2. Hvem skal få sette `code-verified`?
3. Skal `Manuals/` og `Deliverables/` fortsatt ligge i Book-katalogen, og skal Book 33 og 34 inn?
4. Sperreliste eller tillatelsesliste for korrespondanse-lignende filer?
5. Skal `last_verified` kreves for `active`, og skal et `active`-dokument uten det skjules fra standardsøket?

## 8. Hva som er endret i prototypen

- Ny: `haven_docs_sources.py`, `sources.json`, `tests/test_sources_prototype.py`, dette dokumentet.
- Endret: `haven_docs_mcp.py` (tilleggsfelt med standardverdier, nye flagg `--with-sources`, `--check-remote`, `--lint-status`, `--source-report`, seksjonsmarkør, proveniens og ferskhet i svar), `Book/book_catalog.json` (to felter på Book 37), `Book/37_EntityData.md` (én markørlinje i §7).
- Uendret: URI-er, tool-navn og svarformat for Book uten `--with-sources`. De 7 eksisterende testene går uendret.
- Ikke gjort: ingen push, ingen endring i `CellProtocol` eller `CellScaffold`.
