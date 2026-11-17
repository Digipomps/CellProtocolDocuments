STATUS: LEVERT — kartlagt, ingen endringer gjort

# Leveranse — kart over DiMyMint foer pin-bytte

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-lev-mint-kart.sh` 2026-09-22T07:48:44Z. Bevis: `evidence/leveranse-mint/`.

Arbeidskopien staar paa `micropayments-production-hardening`; endringer: 1 sporede filer.

| ref | sha |
| --- | --- |
| `origin/main` | `930efa50c7c4e89c29c68a978144e35a4622f1ab` |
| `origin/micropayments-production-hardening` | `cce8f1e8402f0354851f1f97e2ee78d492cd8268` |
| `origin/codex/prod-dependency-pins-20260917` | `ffdb0da85fc45be16926bfa5d335b247205f1b79` |
| CellScaffold-pinnen | `ffdb0da85fc45be16926bfa5d335b247205f1b79` |

## Hvor ligger pinnen `ffdb0da8`

Commit: ffdb0da 2026-09-18 Kjetil Hustveit — Align exact dependency gate and checkout with tested issuer revision

Grener som inneholder den (remote):
```text
    origin/HEAD -> origin/main
    origin/codex/prod-dependency-pins-20260917
    origin/main
```
**Pinnen er i `origin/main`.**

## DiMyMicropayments-avhengigheten per ref

### `origin/main`

```swift
  17-    dependencies: [
  18-        .package(
  19:            url: "git@github.com:DiMy-io/DiMyMicropayments.git",
  20-            revision: "cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0"
  21-        ),
  22-        .package(url: "https://github.com/apple/swift-crypto.git", "3.0.0" ..< "5.0.0"),
```
Treff paa den gamle pinnen `cd44d59f`: 1. Paa den nye `836ba8e6`: 0.

### `ffdb0da85fc45be16926bfa5d335b247205f1b79`

```swift
  17-    dependencies: [
  18-        .package(
  19:            url: "git@github.com:DiMy-io/DiMyMicropayments.git",
  20-            revision: "cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0"
  21-        ),
  22-        .package(url: "https://github.com/apple/swift-crypto.git", "3.0.0" ..< "5.0.0"),
```
Treff paa den gamle pinnen `cd44d59f`: 1. Paa den nye `836ba8e6`: 0.

### `origin/micropayments-production-hardening`

```swift
  75-        return .package(path: localPath)
  76-    }
  77:    return .package(url: "git@github.com:DiMy-io/DiMyMicropayments.git", branch: "main")
  78-}()
  79-
  80-let package = Package(
```
Treff paa den gamle pinnen `cd44d59f`: 0. Paa den nye `836ba8e6`: 0.

## Tidligere pin-runder i DiMyMint

```text
  2026-09-18 origin
  2026-09-18 origin/main
  2026-09-18 origin/codex/prod-dependency-pins-20260917
  2026-09-10 origin/codex/chronicle-consumer-chain-20260910
  2026-09-10 origin/codex/crypto4-security-compat-20260910
  2026-09-01 origin/claude/dimymicropayments-pin-1b31aec-20260901
  2026-08-17 origin/codex/dimymicropayments-652da7-pin-20260817
  2026-08-16 origin/codex/dimymicropayments-5e0c-pin-20260816
  2026-08-11 origin/codex/identityunique-micropayments-pin-20260811
  2026-08-05 origin/codex/archive-20260809/branches/codex/micropayments-policy-pin-20260805
  2026-08-01 origin/codex/apns-v3-dependency-pins-20260720
  2026-07-20 origin/codex/stripe-entitlement-provider-hardening-20260719
```
