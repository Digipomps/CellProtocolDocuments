**1. Prod /health/build — rå JSON**

`curl -s https://haven.digipomps.org/health/build`

Hentet: 2026-09-25 09:37:17 UTC (11:37:17 Europe/Oslo). Exit-kode: 0. Hele svaret, uten avkorting.

```json
{"cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","dimymint_revision":"af41630bbc01cece2a26f3004fdf6f83724ca77e","environment":"production","dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","build_timestamp":"2026-09-25T01:50:25Z","status":"ok","app_revision":"e6277af1f90fea5ce81a896a5a6c904d75dd184e"}
```

**2. Prod /health/ready — rå JSON**

`curl -s https://haven.digipomps.org/health/ready`

Hentet: 2026-09-25 09:37:17 UTC (11:37:17 Europe/Oslo). Exit-kode: 0. Hele svaret, uten avkorting.

```json
{"acceptsNewTraffic":true,"runtimeAdvisories":["scaffold_administrator_threshold_below_two scaffold=scaffold:cellscaffold requiredSignatures=1 reason=utviklingsfase, styreleder alene setAt=2026-09-09T00:00:00Z"],"status":"ready","runtimeDiagnostics":[],"mode":"serving","updatedAt":1790311760.4852638}
```

**3. Staging /health/build — rå JSON**

`curl -s https://staging.haven.digipomps.org/health/build`

Hentet: 2026-09-25 09:37:17 UTC (11:37:17 Europe/Oslo). Exit-kode: 0. Hele svaret, uten avkorting.

```json
{"cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10","environment":"staging","status":"ok","dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","build_timestamp":"2026-09-24T13:35:13Z","dimymint_revision":"af41630bbc01cece2a26f3004fdf6f83724ca77e","app_revision":"4dd70c520dac2d8921229fed767533c05b1c574b","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved"}
```

**4. Staging /health/ready — rå JSON**

`curl -s https://staging.haven.digipomps.org/health/ready`

Hentet: 2026-09-25 09:37:17 UTC (11:37:17 Europe/Oslo). Exit-kode: 0. Hele svaret, uten avkorting.

```json
{"status":"ready","acceptsNewTraffic":true,"mode":"serving","updatedAt":1790312224.1584988,"runtimeAdvisories":["arendalsuka_published_read_access_not_provisioned","scaffold_administrator_threshold_below_two scaffold=scaffold:cellscaffold requiredSignatures=1 reason=utviklingsfase, styreleder alene setAt=2026-09-09T00:00:00Z"],"runtimeDiagnostics":[]}
```

**5. CellScaffold — rå Git-utdata**

Kommandoene ble kjørt 2026-09-25 etter helsesjekkene. Git-utdata under er ikke avkortet. Tom stdout er uttrykkelig angitt.

`git fetch origin main --quiet`

```text
(tom stdout/stderr)
```
Exit-kode: 0.

`git rev-parse --short origin/main`

```text
18c14c32
```
Exit-kode: 0.

`git log --oneline -1 origin/main`

```text
18c14c32 Merge pull request #263 from Digipomps/pdd/musikkstatistikk-fanen
```
Exit-kode: 0.

`git cat-file -e 'e6277af1f90fea5ce81a896a5a6c904d75dd184e^{commit}'`

```text
(tom stdout/stderr)
```
Exit-kode: 0.

`git rev-parse origin/main`

```text
18c14c32cb6e2957c1d13a20a4b2d97ece2f02b6
```
Exit-kode: 0.

`git merge-base --is-ancestor e6277af1f90fea5ce81a896a5a6c904d75dd184e origin/main`

```text
(tom stdout/stderr)
```
Exit-kode: 0.

Prod-revisjonen fantes lokalt (`git cat-file -e`: exit 0); ekstra `git fetch origin <app_revision>` var derfor ikke nødvendig.

**Uttrekk fra de fire JSON-svarene**

«Mangler» betyr at nøkkelen ikke finnes i det aktuelle svaret; felt er ikke overført fra et annet endepunkt.

| Svar | app_revision | environment | status | mode |
| --- | --- | --- | --- | --- |
| Prod /health/build | `e6277af1f90fea5ce81a896a5a6c904d75dd184e` | `production` | `ok` | Mangler |
| Prod /health/ready | Mangler | Mangler | `ready` | `serving` |
| Staging /health/build | `4dd70c520dac2d8921229fed767533c05b1c574b` | `staging` | `ok` | Mangler |
| Staging /health/ready | Mangler | Mangler | `ready` | `serving` |

Hele `runtimeAdvisories` for hvert svar:

- Prod /health/build: Mangler.
- Prod /health/ready: `["scaffold_administrator_threshold_below_two scaffold=scaffold:cellscaffold requiredSignatures=1 reason=utviklingsfase, styreleder alene setAt=2026-09-09T00:00:00Z"]`
- Staging /health/build: Mangler.
- Staging /health/ready: `["arendalsuka_published_read_access_not_provisioned","scaffold_administrator_threshold_below_two scaffold=scaffold:cellscaffold requiredSignatures=1 reason=utviklingsfase, styreleder alene setAt=2026-09-09T00:00:00Z"]`

**Kort konklusjon**

- Prod rapporterer fortsatt `scaffold_administrator_threshold_below_two` med `scaffold=scaffold:cellscaffold` og `requiredSignatures=1`. Terskelen er altså **1** ifølge det ferske readiness-svaret.
- Staging rapporterer samme scaffold-administratoradvarsel og samme terskel **1**. Staging rapporterer også `arendalsuka_published_read_access_not_provisioned`.
- Om administratoren fortsatt er **`entity:digipomps`**, er **ikke verifisert av disse svarene**: de oppgir scaffold-identifikatoren, men ingen administrator-entitet. `entity:digipomps` finnes ikke i noen av de fire JSON-svarene. Administratorens identitet kan derfor ikke fastslås fra dette datagrunnlaget alene.
- Er prod-revisjonen `e6277af1f90fea5ce81a896a5a6c904d75dd184e` en forfar av fersk `origin/main` (`18c14c32`)? **JA** — `git merge-base --is-ancestor` returnerte exit-kode 0.

Ingen tjeneste-, konfigurasjons- eller kodeendringer er gjort. Lokal `git fetch` og denne rapporten er de eneste bestilte skriveoperasjonene. Eksisterende endringer i arbeidsområdene er ikke rørt. Rapporten gir ingen vurdering av G3-akseptanse.

