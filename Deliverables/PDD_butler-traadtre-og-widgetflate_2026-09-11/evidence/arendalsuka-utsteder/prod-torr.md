Rettet `ROOT-arendalsuka-utsteder.sh` (md5 `ac7e58ccd7bee8821d035e133b3dd169`) lagt paa verten. Rettelsen staar i koden med begrunnelse.

## Toerrkjoeringen (`--torrkjor --kun production --brukernavn kjetil2`) → exit 0

```text
09:59:56Z arbeidskatalog: /root/arendalsuka-utsteder-20260923T095956Z  (torrkjoring=1)
09:59:56Z haven-deploy har --env-only (verifisert i kilden, ikke i hjelpeteksten)
09:59:56Z == production (cellscaffold-production-app-1)
09:59:56Z   3 brukere i production
09:59:56Z   brukernavn «kjetil2» finnes i production
09:59:56Z   /etc/haven/deploy-production.conf peker paa /etc/haven/deploy-production.secrets.env - legger noekkelen inn der, oppretter ingen ny fil
09:59:56Z   ville lagt til HAVEN_ARENDALSUKA_PUBLISHER_BOOTSTRAP_USERNAME=kjetil2 i /etc/haven/deploy-production.secrets.env
09:59:56Z   revisjon foer: 77a922bc
09:59:56Z   [torr] ville kjoert: haven-deploy production current --env-only
09:59:56Z FERDIG.
09:59:56Z NESTE STEG, og det maa du gjoere selv i nettleseren:
09:59:56Z   Logg inn som «kjetil2» og kall POST /<slug>/api/configuration/access/issue
09:59:56Z   UTEN subjectUsername. Foerste kall lager Agreementet med rw-s paa
09:59:56Z   publisherAccess.issue og utsteder VC-en til deg. Deretter kaller du den
09:59:56Z   samme ruten med {"subjectUsername":"vegar"} for aa gi Vegar tilgang.
09:59:56Z   Env-variabelen kan fjernes etterpaa; Agreementet staar.
09:59:56Z Bevis og kopi av originalfilene: /root/arendalsuka-utsteder-20260923T095956Z
```

## Brukertabellen i prod

```text
fil: /root/arendalsuka-utsteder-20260923T095956Z/brukernavn-production.txt
antall brukere: 3
treff paa kjetil|vegar|digipomps:
1:kjetil2
3:Vegar
```

Den rettede `db_for()` leser prods database. Neste steg er noeyaktig samme kall
uten `--torrkjor`.
