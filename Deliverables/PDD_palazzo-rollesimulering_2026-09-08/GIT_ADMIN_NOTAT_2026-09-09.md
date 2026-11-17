# Git-administrasjon av Losen-leveransen, 9. september 2026

work_id: git-admin-losen-20260909-docs
status: VERIFIED
owner: Codex Git-admin (integrator)
repo: /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments
base_ref: be6839a (origin/main kontrollert 2026-09-09)
target_branch: codex/losen-deliverables-20260909

Kjetil ba om å lese og utføre
`/Users/kjetil/Build/Digipomps/HAVEN/_handoff-20260909/GIT_ADMIN_PROMPT.md`.
Denne leveransen versjoneres i tre separate commits på en isolert branch fra
`origin/main`. Det utelater de fire lokale commitene fra den andre oppgaven på
`codex/docs-cleanup-20260810`. Bare `Tools/RepoPaths/`, denne PDD-mappen og
`Deliverables/Repo_Path_Konvensjon_2026-09-09.md` inngår i diffen mot basen.
Dokumentbranchen er lokal; overleveringens uttrykkelige push-steg gjaldt
UniverseSimulation. Ingen merge til dokumentrepoets `main` er utført.

## Beslutning om Palazzo-kilden

PalazzoScaffold har ingen `.git`. De elleve kildefilene i
`PalazzoScaffold::Tests/Roles/` er bevart byte for byte i
[source-snapshot-2026-09-09/](source-snapshot-2026-09-09/verification.md), med
SHA-256-manifest og fersk fixturelogg. De operative filene blir liggende der
PLAN.md peker. Ingen referanse til den kjørbare leveransen trenger å flyttes.
Dette sikrer dagens kilde i Git uten å avgjøre repostrukturen for hele
scaffoldet. Senere endringer i den operative mappen blir ikke automatisk
versjonert av dette arkivet.

PDD-ens opprinnelige seks filer, inkludert `_selftest_raw.txt`, er bevart
uendret. FORMAALSSPEC har en foreldet innledende status om at G1 ikke er
godkjent; PLAN, STATUS og overleveringen registrerer godkjenning 9. september.
Dette notatet gjør motstriden synlig uten å omskrive historisk evidens.

## Verifikasjon og åpne feil

RepoPaths-kilden ble bevart uendret i commit `ae0ae4b`. Midlertidige fixtures og
konfigurasjoner ga **20/24 beståtte kontroller**. Det dokumenterte lokke-treet
ble korrekt avvist med 0/2, og gyldige oppsett med spredte/omdøpte mapper,
arbeidsmappebytte, stiutbrudd og symbolske lenker ble kontrollert. Fullt resultat
og originale filhasher ligger i
[git-admin-evidence/repo-paths-verification.json](git-admin-evidence/repo-paths-verification.json).
Fire kontroller avdekker to forhold som må rettes i en egen kodeendring:

- JSON-konfigurasjon med toppnivå `[]` eller repo-oppføring uten `path` gir
  ukontrollert AttributeError/KeyError, ikke navngitt `config_invalid`.
- Relativ `commonRoot: "repos"` aksepteres og gir ulik full sti fra ulike
  arbeidsmapper. Påstanden om uavhengighet av `cwd` gjelder derfor ikke alle
  konfigurasjoner verktøyet i dag aksepterer.

Palazzo-fixturen bestod skjemakontroll og **8/8 tester** i en midlertidig kopi.
Docker opptar standardportene 8101/8102 på denne maskinen, så siste kjøring
endret bare portbasen i minnet og brukte 18200–18207. Arkivkilden er uendret.
[Kontrollnotatet](source-snapshot-2026-09-09/verification.md) beskriver også
svakhetene i kalibrering, klassifisering og exit-koder. Et grønt fixtureløp er
ikke bevis for at alle faktiske Palazzo-formål er oppnådd. WP10 mot faktisk
server og WP11 om rekkevidde er fortsatt utestående.

Stikonvensjonen er fortsatt et forslag. Dokumentets 145 kildeankere og den
historiske verifikasjonen gjør ikke hele foreslåtte CLI-/skjema-/installasjons-
eller migreringsløpet implementert.

## Til Losen

Fortsett å bruke `PalazzoScaffold::Tests/Roles/` som operativ sti. Dagens kilde
har nå et datert Git-arkiv sammen med PDD-en. Planen trenger ingen flytting av
operativ sti; ved senere arbeid bør det avklares hvordan nye kildeendringer
skal versjoneres. Gjenværende feil og WP10/WP11 er synlige ovenfor.
