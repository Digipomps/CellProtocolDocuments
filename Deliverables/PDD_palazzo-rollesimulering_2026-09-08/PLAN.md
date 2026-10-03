# PLAN — palazzo rollesimulering

G1 godkjent av Kjetil 2026-09-09. Arbeidspakker 1:1 mot bladformål i
FORMAALSSPEC.md §1 og §2b.

Alt ligger i **repoet PalazzoScaffold**, under `Tests/Roles/` (ren
stdlib-python, ingen avhengigheter, ingen import av App-modulen).

Stier i dette dokumentet er relative til repoet de ligger i. Hvor repoene ligger
på en gitt maskin er en device-innstilling, ikke noe dokumentet skal anta — se
`CellProtocolDocuments/Deliverables/Repo_Path_Konvensjon_2026-09-09.md` når den
er levert.

| WP | Bladformål | Utfører | Test | Status |
|---|---|---|---|---|
| WP1 | roles-have-purposes | Losen | test.roles.schema | **levert** — 5 roller, 26 formål |
| WP2 | simulated-actor-uses-production-path | Losen | test.roles.production-path | **levert** — `run_roles.py` går bare over HTTP med principal-header og bearer-token |
| WP3 | actor-is-calibrated | Losen | test.roles.calibration | **levert** — kalibreringsblokk kjøres først, exit 2 |
| WP4 | null-principal-run | Losen | test.roles.null-principal | **levert** — `--null-principal`, exit 3, med reviderbare unntak |
| WP5 | no-unevaluated-success | Losen | test.roles.no-unevaluated-success | **levert** — 200 uten lesbar tilstand blir UKLASSIFISERT |
| WP6 | every-stop-is-classified | Losen | test.roles.unclassified-fails | **levert** — exit 4; `stop_is` er den menneskelige forhåndsavgjørelsen |
| WP7 | cross-role-privacy | Losen | test.roles.cross-privacy | **delvis** — dømmingen er bevist mot fixturen (exit 5); Palazzos faktiske oppførsel er ukjent til WP10 |
| WP8 | agent-role | Losen | test.roles.agent | **levert, med generator** — `Tests/Roles/roles_from_trust_package.py` utleder agentens formål fra en tillitspakke: en grant med `r` i permission gir «forvent tilgang», uten `r` gir «forvent avslag». Begge retninger kommer fra pakken selv, så kjøringen blir etterprøvingen av at pakken ble overholdt. `roles/agent.json` er fortsatt håndskrevet og merket som det — det finnes ingen pakke for en flåte som kjører mot Palazzo ennå |
| WP9 | report-for-humans | Losen | test.roles.report | **levert** — RAPPORT med kalibreringsblokk først |
| WP10 | root · første ekte kjøring, **før Sicilia G7** | Kjetil | test.roles.report | **venter på Kjetil** — krever kjørende server med token og isolert vault |
| WP11 | reachable-in-app | Losen + Kjetil | test.roles.reachable | **ikke startet** — krever SkeletonReachabilityAudit fra Swift-siden; egen slice |

## Hvorfor WP10 ikke kan gjøres herfra

Cowork-VM-en har ingen `swiftc` og skal ikke starte servere i Kjetils mapper.
`lesson.codex-workspace-write-cannot-build-cellscaffold` (2026-09-09) sier
dessuten at lange bygg og testkjøringer ikke legges som køjobb. Serveren startes
av Kjetil, eller som detached skript med `danger-full-access` og logg i en
montert mappe — samme mønster som produserte den notariserte HavenAgentD-pakken.

## Kommandoen WP10 er

```bash
cd "$(python3 ~/.haven/haven_path.py path PalazzoScaffold::Tests/Roles)"
python3 run_roles.py \
  --base-url http://127.0.0.1:8080 --token "$PALAZZO_GATEWAY_TOKEN" \
  --env guest_id=… other_guest_id=… staff_id=… agent_id=… \
        guest_cell=… consenting_guest_cell=… article_id=… agreement_id=… \
  --null-principal "guest:$(uuidgen)" \
  --out "$(python3 ~/.haven/haven_path.py path \
      CellProtocolDocuments::Deliverables/PDD_palazzo-rollesimulering_2026-09-08)/RAPPORT_$(date +%F).md"
```

Verdiene til `--env` må peke på ekte celler: én gjest som **har** gitt samtykke
til de fem briefKeypaths (`consenting_guest_cell`) og én som **ikke** har det
(`guest_cell`). Uten det paret finnes det ingen kalibrering, og kjøringen skal
nekte å bli lest.

## Forventet utfall av første kjøring

Ikke grønt. Bridgehead publiserer ikke gjest-/innholdscellen før Sicilia G7, så
`gjest.read-articles` og `gjest.article-configuration` skal stoppe — de er
allerede merket `stop_is: feil` med begrunnelse. Finner kjøringen dem ikke, er
det metoden som er for svak, ikke systemet som er friskt.
