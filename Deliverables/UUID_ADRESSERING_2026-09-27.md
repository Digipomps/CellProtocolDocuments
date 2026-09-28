# UUID-adressering — kildekontroll og publisering

Utført 2026-09-28. Filnavnets dato 2026-09-27 er beholdt som bestilt.
Omfang: dokumentasjon og skills; ingen Swift-endringer.

## Kildegrunnlag og faktiske linjenumre

Kilde: `CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift`.
Alle tre oppgitte steder ble lest før redigering, og persisteringsveien ble
fulgt frem til autoritetssjekken.

- Lokalt CellProtocol-arbeidstre: HEAD `561d34a7ea785c087bd6036921f60debe6bace4a`,
  gren `pdd/tillitspakke-agentflaate`, med eksisterende ukommitterte endringer.
  SHA-256 for den leste lokale resolver-filen: `cfaa964c8a7e4963204ad7c38db99721e88f4c00e3cb64243fb64e211317c148`.
- Publisert CellProtocol `origin/main`, hentet fra origin og kontrollert separat:
  `9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366`.
  [Fast kildeversjon](https://github.com/Digipomps/CellProtocol/blob/9c60001ac53abc35ba7ad6e2c0efa2a79ab2a366/Sources/CellBase/Cells/CellResolver/CellResolver.swift).
  SHA-256: `6394a9024629e14ebc52691d149ce3e410e3aeb2833825042db5bf6ccb9ceae7`.
  Boktekstens kildehenvisning bruker denne publiserte versjonen.

| Kontrollpunkt | Lokalt arbeidstre | Publisert main |
|---|---|---|
| Dispatch: `ws`, `wss`, `cell`; andre skjemaer avvises | 1333–1348 | 1325–1340 |
| Vert velger lokal eller fjern rute; `localhost` er lokal | 1390–1406 | 1382–1398 |
| `URL.path`, fjern én innledende skråstrek, send til `emitCellWithReference` | **1408–1412** | **1400–1404** |
| UUID: minne først, deretter `loadCellFromPersistance(uuid:requester:)` | **1777–1813** | **1769–1805** |
| `identityUnique` i minnet: `validatesIdentityUniqueDirectReferenceAccess`, ellers `ownerAuthorityUnavailable` | **1780–1787** | **1772–1779** |
| Ikke UUID: `auditor.loadNamedResolve(reference)` | 1815 | 1807 |
| Persisteringsdelegasjon til requester-bevisst `loadTypedEmitCell` | 1992–1994 | 1984–1986 |
| Persistert `identityUnique` og samme direkte UUID-autoritetssjekk | 2716–2748 | 2712–2744 |
| Direkte UUID-autoritet: bevist eier eller verifisert kontrakt i `GeneralCell` | 2820–2834 | 2816–2830 |
| Port videreføres til WebSocket-forbindelsen | 1715 | 1707 |

**De tre oppgitte linjeintervallene stemmer i det lokale arbeidstreet.** De er
forskjøvet i publisert `main`, som tabellen viser. Navneoppslaget står på 1815
lokalt, rett etter oppgavens intervall 1777–1813. Setningen i kapittel 37 står
på linje **68** i publisert grunnlag, mot **54** i det lokale arbeidstreet.

UUID-oppslag velger en konkret instans også når en annen identitet eier den.
For `identityUnique` må autoritetssjekken fortsatt lykkes, både i minnet og fra
persistens. Funksjonen aksepterer bevist eier eller, for `GeneralCell`, en
verifisert aktiv signert autorisasjonskontrakt. GET/SET-autorisasjon for aktuelle
nøkkelstier er fortsatt separat. Adressering er ikke autorisasjon.

## Adresseformer funnet

| Form | Betydning |
|---|---|
| `cell:///<navn>` | Lokalt navneoppslag gjennom `loadNamedResolve`, etter registrert scope. |
| `cell:///<uuid>` | Konkret celleinstans, minne før persistens, under autoritetskontroll. |
| `cell://<vert>/<referanse>` | Registrert fjernrute; verten er en rutevert. |
| `ws://...`, `wss://...` | Egen `emitCellAtWSEndpoint`-vei og WebSocket-policy. |
| `cell://localhost/<referanse>` | Eksplisitt lokal variant i vertstesten. |
| `cell:/<referanse>` | Hostløs lokal variant; samme stiuttrekk. |
| `cell://<vert>:<port>/<referanse>` | Fjernvarianten med eksplisitt port, videreført av koden. |

De fire etterspurte kategoriene finnes. De tre siste radene er ekstra varianter
av de lokale/fjerne formene. Hostløs enkelt-skråstrek og port ble også kontrollert
med Foundation `NSURL.URLWithString` gjennom JXA: `cell:/Example` gir skjema
`cell`, ingen vert og sti `/Example`; `cell://example.org:8443/Example` gir vert
`example.org`, port 8443 og sti `/Example`. Dette var en parserkontroll, ikke en
kjøring av resolveren. `cell:Example` ga ingen sti og er ikke dokumentert som
oppslagsform. Ingen eier-UUID i verten eller andre nye adressekontrakter er innført.

## Hva som ble skrevet

- `Book/06_CellResolver.md:32`: ny §1.1 med adresseformene, konkret UUID-eksempel,
  minne/persistens-rekkefølge, instans eid av annen identitet, autoritetssjekk,
  egen GET/SET-autorisasjon og kildeversjon med linjenumre.
- `Book/37_EntityData.md:68`: eksisterende tilgangssetning beholdt; lagt til
  UUID-adressering og kryssreferanse til kapittel 6.
- `.claude/skills/cellconfiguration-skeleton-authoring/SKILL.md:105`:
  kort endpoint-veiledning etter dataplanen, med henvisning til kapittel 6.
- `.claude/skills/cellconfiguration-skeleton-authoring/references/examples.md:25`:
  forklaring rett etter det minimale `CellConfiguration`-eksemplet.
- `.claude/skills/public-presence-cell-authoring/SKILL.md:72`:
  kort forklaring før gjenbrukskartets navngitte endpoints, også med skillet
  mot publisering. Eksisterende ugyldig YAML-description ble gjort til en
  foldet streng (`>-`), med uendret beskrivelsestekst, slik at skillen validerer.
- Denne rapporten: `Deliverables/UUID_ADRESSERING_2026-09-27.md`.

Kapittelinventar og katalogmetadata er uendret; `Book/book_catalog.json` trengte
ingen endring. Andre tråders bok-, skill- og kodeendringer ble ikke kopiert inn.

## Rene arbeidstrær, SHA-er og commit-stier

Egne isolerte kloner med lokal gren `main`, ren indeks og rent arbeidstre ved
start, basert på fersk `origin/main`:

- `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/uuid-adressering-20260928/CellProtocolDocuments`
- `/Users/kjetil/Build/Digipomps/HAVEN/_worktrees/uuid-adressering-20260928/CellScaffold`

| Repo | Origin/main før | Publisert innholdscommit etter |
|---|---|---|
| CellProtocolDocuments | `c83dab6e1ee3c481c99758b09e03cf610a7011b5` | `ffc603fb04d0c851e741843828827c13a07cced1` |
| CellScaffold | `feec23725321320ab00f0e7f7bf728b775869ec7` | `a0a2fde9543f0c9df0a63972fac33ab9803cf4cf` |

CellProtocolDocuments-innholdscommiten bruker nøyaktig bestilt commit-melding:

```text
docs(book): a cell is addressable by its uuid

cellAtEndpoint takes the path of a cell:// endpoint as a reference; a uuid
resolves to the instance in memory or in persistence, including one owned by
another identity. identityUnique cells pass an owner-authority check on the
way. Addressing is not authorization: the chapter says both.
```

CellScaffold: `docs(skills): explain uuid cell addressing`.

Eksplisitt tillatt liste, kontrollert mot `git diff --cached --name-only` før
hver innholdscommit og mot `git diff-tree` etterpå:

```text
CellProtocolDocuments / ffc603fb04d0c851e741843828827c13a07cced1
Book/06_CellResolver.md
Book/37_EntityData.md

CellScaffold / a0a2fde9543f0c9df0a63972fac33ab9803cf4cf
.claude/skills/cellconfiguration-skeleton-authoring/SKILL.md
.claude/skills/cellconfiguration-skeleton-authoring/references/examples.md
.claude/skills/public-presence-cell-authoring/SKILL.md
```

Rapporten følger som en egen commit etter den verifiserte dokumentasjonscommiten,
med bare denne eksplisitte stien:

```text
Deliverables/UUID_ADRESSERING_2026-09-27.md
```

Tabellens etter-SHA gjelder innholdscommitene. Rapportcommitens egen SHA kan ikke
skrives inn i filen den hasher; den identifiseres med
`git log -1 --format=%H -- Deliverables/UUID_ADRESSERING_2026-09-27.md` og oppgis
sammen med endelig `origin/main`-kontroll i leveringssvaret.

## Publisering og verifikasjon

Begge innholdscommiter ble pushet med `git push origin main`; første forsøk
lyktes i begge repoer. Ingen rebase eller nytt pushforsøk var nødvendig.
Etterpå ga `git ls-remote origin refs/heads/main` nøyaktig SHA-ene i tabellen.
Origin ble hentet på nytt, og `git show <remote-SHA>:<sti>` ble sammenlignet
byte for byte med hver kontrollert arbeidsfil. **Alle fem var byte-like.**

SHA-256 for de kontrollerte og publiserte innholdsfilene:

| Fil | SHA-256 |
|---|---|
| `CellProtocolDocuments/Book/06_CellResolver.md` | `1a2c3268d5132c7003d2acf57c902c2bb2acacd0d09b145a658bc38066b091b6` |
| `CellProtocolDocuments/Book/37_EntityData.md` | `ea19be5d2a580289acb290551ce198e14de0a9f7d48a79020595e59aaf8226ca` |
| `CellScaffold/.claude/skills/cellconfiguration-skeleton-authoring/SKILL.md` | `b0daa63c4a5d698151a4b61e8f7d20262e54f7a4e383ff53c3728366153afe98` |
| `CellScaffold/.claude/skills/cellconfiguration-skeleton-authoring/references/examples.md` | `2c2eeb3d1ddd1ca44bda43918df73e1c8b2ea8351c525a8227cca94771d4bc1c` |
| `CellScaffold/.claude/skills/public-presence-cell-authoring/SKILL.md` | `ee87978b64d4fa9d3fdd50d82f74f35fe4618eedcb8bcc7991c3513527a3bc61` |

Utførte kontroller:

- `git diff --check` og `git diff --cached --check`: bestått.
- Docs MCP: alle 7 eksisterende tester bestått; den nye §1.1 kan hentes via
  `read_section` med anker `11-endpoint-address-forms-and-uuid-lookup`.
- Alle fem nye kryssreferanser: målfil og seksjonsanker finnes, inkludert
  relative lenker fra begge skill-katalogene til søskenrepoet.
- Alle tre eksisterende JSON-eksempler i `references/examples.md`: gyldig JSON.
- Skill Creator `quick_validate.py`: begge skills bestått. PyYAML manglet i
  system-Python og ble installert i en midlertidig venv; ingen repoavhengighet
  ble endret. Den eksisterende YAML-feilen i public-presence ble først
  reprodusert mot grunnlagscommiten, deretter rettet i den samme berørte filen.
- Pålagt `ci/check-value-literals.sh`: seks selvtester og baselinekontroll
  bestått med `HAVEN_PYTHON=/usr/bin/python3`. Automatisk Python-valg feilet
  først med `Bad CPU type in executable` for `/usr/local/bin/python3.12`/`python3`.
- Før rapportskriving var begge publiseringsarbeidstrær rene. De fem aktuelle
  filene i de opprinnelige arbeidstrærne og den lokale resolver-filen hadde
  uendrede SHA-256-verdier sammenlignet med registreringen før commit.

## Avgrensning og gjenstående arbeid

Alle etterspurte innholdsendringer er publisert og byte-kontrollert.
Rapportens egen commit/push og siste bytekontroll skjer etter at denne filen er
skrevet; resultat og SHA rapporteres i leveringssvaret. Ingen Swift-filer,
submodulpekere eller andre tråders endringer inngår. Ingen runtime-bygg eller
ende-til-ende-kjøring av celleoppslag er utført: grunnlaget her er lest kildekode,
parserkontroll og dokumentasjonsvalidering. Det er ikke en ny funksjonsleveranse.
