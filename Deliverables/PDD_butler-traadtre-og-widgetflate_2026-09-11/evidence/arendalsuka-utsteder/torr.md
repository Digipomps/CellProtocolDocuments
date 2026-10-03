Root-adkomst: `root@ubuntu-16gb-hel1-1` (exit 0).

Skriptet ligger paa verten som `/root/ROOT-arendalsuka-utsteder.sh` (md5 lokalt: 5b2118bfbb347f124965687863da8f84).

## Toerrkjoringen

`ROOT-arendalsuka-utsteder.sh --torrkjor` → exit 1

```text
09:38:10Z arbeidskatalog: /root/arendalsuka-utsteder-20260923T093810Z  (torrkjoring=1)
09:38:10Z haven-deploy har --env-only (verifisert i kilden, ikke i hjelpeteksten)
09:38:10Z == staging (cellscaffold-app-1)
09:38:10Z   32 brukere i staging
09:38:10Z   Ingen --brukernavn oppgitt. Kandidater med kjetil eller vegar i navnet:
    kjetil2
    vegar
    vegar-cellconfiguration-upload-8010
09:38:10Z   Hele listen: /root/arendalsuka-utsteder-20260923T093810Z/brukernavn-staging.txt
09:38:10Z   Kjoer paa nytt med --brukernavn <navn>. Skriptet gjetter ikke.
09:38:10Z STOPP: staging feilet - prod ikke roert
09:38:10Z logg: /root/arendalsuka-utsteder-20260923T093810Z/kjoring.log
```

Ingenting er endret. Neste steg er samme skript med `--brukernavn <navn>` per miljoe.
