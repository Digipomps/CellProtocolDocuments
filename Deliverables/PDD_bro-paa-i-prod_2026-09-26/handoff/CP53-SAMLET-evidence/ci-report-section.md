**CI grønn på slutt-head `1e3e7f10b378591870c16d4e2bb6a3928496946d`. Alle fem kjøringer er ferdige og godkjent. Siste jobb ble ferdig 07:29:08 UTC, innen samlet overvåkingsfrist 06:39–07:39 UTC. Midlertidige GitHub-/TLS-forbindelsesfeil ble håndtert ved gjenopptatt native `gh run watch`; ingen CI-jobb er startet om for å skjule feil. PR er fortsatt OPEN, `mergedAt = null`.

| Kjøring | Resultat |
|---|---|
| [CellProtocol Swift Linux](https://github.com/Digipomps/CellProtocol/actions/runs/36535224178) | grønn, `36535224178` |
| [CellProtocol macOS regression](https://github.com/Digipomps/CellProtocol/actions/runs/36535224125) | grønn, `36535224125` |
| [Notify PyCellProtocol](https://github.com/Digipomps/CellProtocol/actions/runs/36535221618) | grønn, `36535221618` |
| [Runtime capacity benchmark (macOS)](https://github.com/Digipomps/CellProtocol/actions/runs/36535224305) | grønn, `36535224305` |
| [Vapor identity vault Swift Linux](https://github.com/Digipomps/CellProtocol/actions/runs/36535224133) | grønn, `36535224133` |

macOS fulltest, siste linje: `Executed 1511 tests, with 5 tests skipped and 0 failures (0 unexpected) in 65.106 (65.427) seconds`. Alle tre lokale Keychain-feiltester består i CI. CI bruker én samlet XCTest-runner; main bidrar med fem ekstra Vault-tester sammenlignet med lokal head.

Utvidet TSAN er kjørt i tre friske prosesser:

- Pass 1/3: `Executed 137 tests, with 0 failures (0 unexpected) in 45.576 (45.684) seconds`.
- Pass 2/3: `Executed 137 tests, with 0 failures (0 unexpected) in 43.331 (43.410) seconds`.
- Pass 3/3: `Executed 137 tests, with 0 failures (0 unexpected) in 41.569 (41.647) seconds`.

Linux device-ingress-gaten: siste `Executed 150 tests, with 0 failures (0 unexpected) in 7.118 (7.118) seconds`; egen vault-gate: `Executed 25 tests, with 0 failures (0 unexpected) in 0.522 (0.522) seconds`. Native MC-prøver er eksplisitt kjørt lokalt, ikke hevdet kjørt i GitHub CI.

**Checkout-proveniens:** macOS-/Linux-/vault-regresjonene tester GitHubs midlertidige PR-merge `d5c00c79bb3083fc28ea1bf469c71289e443e039`, med head `1e3e7f1` som forelder. Sammenligningen mot head viser kun main-endringene i `VaultCell.swift`, nye `VaultIdeaRetention.swift`/tester/dokument og Linux-testkopiering; alle bro-, Scanner-, publisher-, EphemeralIdentityVault- og TSAN-filer er identiske med lokal head. Kapasitetsjobben sjekket ut eksakt `1e3e7f1`. Dette er GitHubs testmerge, ikke en merge av PR-en. Rådata: `delivered-ci-merge-comparison.json`, `delivered-ci-final-pr.json`, `delivered-ci-final-runs.json` og `delivered-ci-{macos,linux,vault,capacity}-logs.zip`.

Tidligere røde kjøringer er bevart: `e02cd61` avslørte vault-racen; `a4a2c01` avslørte eldre Swift-kompilators behov for eksplisitt `self.frames` i reléfiks­turen. Begge er rettet og inngår i den grønne sluttkjøringen. Nye pushes erstattet automatisk eldre pågående CI; ingen skip/exclusion ble lagt til.
