STATUS: LEVERT — prod har HAVEN_ARENDALSUKA_PUBLISHER_BOOTSTRAP_USERNAME=kjetil2

# Prod-utsteder — satt

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-utsteder-prod-sett.sh` 2026-09-23T10:10:21Z. Bevis: `evidence/arendalsuka-utsteder/`.

`ROOT-arendalsuka-utsteder.sh` md5 `ac7e58ccd7bee8821d035e133b3dd169` — samme fil som generalproeven 09:59:56Z kjoerte.

## Kjoeringen (`--kun production --brukernavn kjetil2`) → exit 0

```text
10:09:59Z arbeidskatalog: /root/arendalsuka-utsteder-20260923T100959Z  (torrkjoring=0)
10:09:59Z haven-deploy har --env-only (verifisert i kilden, ikke i hjelpeteksten)
10:09:59Z == production (cellscaffold-production-app-1)
10:09:59Z   3 brukere i production
10:09:59Z   brukernavn «kjetil2» finnes i production
10:09:59Z   /etc/haven/deploy-production.conf peker paa /etc/haven/deploy-production.secrets.env - legger noekkelen inn der, oppretter ingen ny fil
10:09:59Z   ville lagt til HAVEN_ARENDALSUKA_PUBLISHER_BOOTSTRAP_USERNAME=kjetil2 i /etc/haven/deploy-production.secrets.env
10:09:59Z   revisjon foer: 77a922bc
10:09:59Z   doctor: 0 feil
      },
      "completedAt": "2026-09-23T10:10:14Z"
    }
    2026-09-23T10:10:14Z COMMITTED_VERIFIED
    2026-09-23T10:10:14Z FERDIG — bevis i /mnt/HC_Volume_104775511/haven-production-evidence/deploy/20260923T100959Z-production-77a922bc
10:10:20Z   production OK: revisjon uendret 77a922bc, ready, HAVEN_ARENDALSUKA_PUBLISHER_BOOTSTRAP_USERNAME=kjetil2
10:10:20Z FERDIG.
10:10:20Z NESTE STEG, og det maa du gjoere selv i nettleseren:
10:10:20Z   Logg inn som «kjetil2» og kall POST /<slug>/api/configuration/access/issue
10:10:20Z   UTEN subjectUsername. Foerste kall lager Agreementet med rw-s paa
10:10:20Z   publisherAccess.issue og utsteder VC-en til deg. Deretter kaller du den
10:10:20Z   samme ruten med {"subjectUsername":"vegar"} for aa gi Vegar tilgang.
10:10:20Z   Env-variabelen kan fjernes etterpaa; Agreementet staar.
10:10:20Z Bevis og kopi av originalfilene: /root/arendalsuka-utsteder-20260923T100959Z
```

## Kontroll utenfra

```text
revisjon: 77a922bc301a0ea7586a6b3677a87c2b1e0f73f7
noekkel:  kjetil2
ready:    {"runtimeAdvisories":["scaffold_administrator_not_provisioned scaffold=scaffold:cellscaffold","scaffold_administrator_threshold_below_two scaffold=scaffold:cellscaffold requiredSignatures=1 reason=utviklingsfase, styreleder alene setAt=2026-09-09T00:00:00Z"],"updatedAt":1790158214.1014683,"status":"ready","mode":"serving","acceptsNewTraffic":true,"runtimeDiagnostics":[]}
build:    {"dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","status":"ok","environment":"production","build_timestamp":"2026-09-22T11:21:08Z","dimymint_revision":"af41630bbc01cece2a26f3004fdf6f83724ca77e","package_resolved_source":"\/app\/BuildMetadata\/Package.resolved","app_revision":"77a922bc301a0ea7586a6b3677a87c2b1e0f73f7","cellprotocol_revision":"473357cf4efee831cb3b55ae87bc921d4bb63c10"}```

Begge miljoeer har naa bootstrap-pekeren. Den gir ingen tilgang i seg selv:
foerste gang `kjetil2` kaller `POST /<slug>/api/configuration/access/issue` fra sin
egen innloggede sesjon, lager cellen ett Agreement med ett grant — `rw-s` paa
`publisherAccess.issue` — og utsteder VC-en. Deretter samme rute med
`{"subjectUsername":"Vegar"}` for Vegar. Da ligger autoriteten i CellProtocol og
env-variabelen kan fjernes.
