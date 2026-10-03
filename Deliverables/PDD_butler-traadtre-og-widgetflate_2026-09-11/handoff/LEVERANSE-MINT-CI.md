STATUS: LEVERT — CI-loggen lest

# Leveranse — CI-feilen paa DiMyMint-pin-PR-en

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-lev-mint-ci.sh` 2026-09-22T08:00:03Z. Bevis: `evidence/leveranse-mint/`.

Kjoering: `35701988704` — source-contract (fail, 19s).

Stripe entitlement provider source gate / Stripe entitlement provider source gate — failure (pull_request paa pdd/dimymicropayments-skjelettrunden)

Logg for den feilende jobben: 13 linjer (hele i `evidence/leveranse-mint/ci-log.txt`).

## Siste 60 linjer

```text
source-contract	Run exact-source gate with disposable PostgreSQL	﻿2026-09-22T07:55:02.4086290Z ##[group]Run python3 scripts/verify-stripe-disposable-postgres.py
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:02.4086770Z ^[[36;1mpython3 scripts/verify-stripe-disposable-postgres.py^[[0m
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:02.4122580Z shell: /bin/bash -e {0}
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:02.4122800Z env:
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:02.4123080Z   DIMYMINT_EXPECTED_SOURCE_SHA: 2aedab6d023e13c6e3fb7ac1e85a1827c3ffb001
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:02.4123440Z ##[endgroup]
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.1968310Z waiting for server to start.... done
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.1968740Z server started
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.3382650Z Package.swift must pin DiMyMicropayments at cd44d59f584cccf618ff5a33d9a7c5d2c082e6a0
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.5345100Z waiting for server to shut down.... done
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.5346000Z server stopped
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.5720460Z {"source": "2aedab6d023e13c6e3fb7ac1e85a1827c3ffb001", "root": "/var/folders/nj/vtw8zd2j31d1gdrtntc5y4600000gn/T/dimymint-postgres-axmutdrb", "port": 49174, "gateExit": 72, "stopped": true, "socketDirectory": "/tmp/mint-pg-fznlo77a"}
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.5776590Z ##[error]Process completed with exit code 72.
```

## Linjer med error/failed

```text
source-contract	Run exact-source gate with disposable PostgreSQL	2026-09-22T07:55:03.5776590Z ##[error]Process completed with exit code 72.
```

## Arbeidsflytfilen

```text
  swift-ci.yml
```
