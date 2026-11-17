# Bolk 3 og 5 — k8: fullport grønn, kladd-PR åpnet, CI blokkert av CP-main-port

STATUS: STOPPET ved eksisterende dependency-port i klient-CI. Ingen notarisert pakke levert.

## Levert og verifisert

- K7-rapport bevart byte-identisk som `handoff/BOLK-3-RAPPORT-k7.md`.
- Backup SHA-256: `ffe6cfcab8b01683257f603e720ee618c6ca60db20c605275ebaeaa8ecf1ff8c`.
- Uendret k7-kapasitetsvakt passerte: 60,7 GiB ledig; 50,7 GiB og 5 prosent etter 10 GiB reserve. Ingen rydding nødvendig eller utført.
- Fullport i eget klientarbeidstre mot CP `7ebb4f5f76cdcda39a2abc2e42c8743a62a703b0`, via eksisterende bounded-runner og cache-leie: exit 0.
- Åtte Python-helpertester grønne. Kompilerte testbundler: 14 + 7 + 31 + 25 + 60 + 187 + 46 + 5 = 375 tester grønne. Lokal ekstra korrespondanseprøve kjørt før fullbundle-løperen. Korrespondansebundlen inkluderer 100 autentiserte Vapor-brotilfeller med opprinnelige assertions.
- Daemon smoke exit 0. Ressursstaging-fixture grønn; manglende bundle og symlenker avvises. Diff-hygiene grønn.
- Commit `c09f95b6b6f66683ee81e9adae7bafbd067f6bc8`, med bestilt co-author, pushet på `codex/korr-klient-20261007`.
- Kladd-PR: https://github.com/Digipomps/HavenAgentD/pull/32
- Diagnostikk under `Evidence/k6/` holdt utenfor commit. Native admin-utkast ikke tatt inn.

## CI-stopp og Bolk 5

CI-run https://github.com/Digipomps/HavenAgentD/actions/runs/37877927205 på eksakt klientcommit avsluttet FAILURE. Steget «Assert every pinned dependency is on its own main» feilet: CellProtocol `7ebb4f5f76cd` ligger ikke på main. Sprout `7aea5b0f814e` passerer. Senere klienttest- og artefaktsteg ble ikke kjørt.

CP PR #63 er fortsatt åpen kladd på bestilt hode. GitHub compare mot main viste diverged: 17 foran, 1 bak. Denne jobben har ingen merge- eller CP-endringsfullmakt. Ingen assertion, CI-port eller pinne er svekket for å få grønt. Den lokale fullporten er grønn; klient-CI er ikke grønn.

Bolk 5 krever grønn klient-CI. Derfor er ren eksport for pakkebygg, universal2-kompilering, Developer ID-signering, notarisering og staple ikke utført. Ingen ny installer eller installer-SHA-256 hevdes. Bestilt dist-mål er `HavenAgentD/.build/korr-release-20261008/dist/`.

Videreføring krever at dependency-porten kan passere gjennom separat autorisert CP-landing, med pinneproveniens bevart. Deretter ny grønn klient-CI før ren eksport og pakkebygg. En squash-landing kan kreve separat avgjørelse om pinne: ikke anta at det gamle PR-hodet blir ancestor av main.

## Native og øvrige begrensninger

Native approval-signer og enhetstester er inkludert og grønne; dette er ikke levert native adminvindu. K3-utkastet mangler fortsatt produkt-/GUI-akseptanse, ekte LAContext, innmelding og fornyelse etter utløp. Samlet prøve mot faktisk vert og tre separate vaults, Intel-kjøring og ren mottaker-Mac er fortsatt ikke verifisert.

## Bevis

Under `HAVEN-Deploy/_handoff/KORR-UT/bolk3/`: `k8-full-private.log`, `k8-full-queue-output.md`, `k8-ci-private.log`, `k8-pr-ci.json` og `k8-pr-body.md`. Private logger er rå lokal evidens, ikke del av denne rapporten eller PR-commit.

Fullportskriptene ble funnet direkte under KORR-UT-handoff, ikke under bolk3 som k7-rapportens formulering kunne tolkes. Første direkte forsøk stoppet på inkompatibel Python i PATH; neste på sandbox-nektet ps. Kjøring gjennom eksisterende skriptkø med fungerende Python bestod. Første køinnlegging avvist fordi promptfil manglet; korrigert r2-jobb fullførte exit 0.

Ingen CP-endring, diskvaktendring, sletting, merge, deploy eller korrespondansesending. Ingen secrets, nøkler, IP-er eller brukerstier gjengitt i rapporten.
