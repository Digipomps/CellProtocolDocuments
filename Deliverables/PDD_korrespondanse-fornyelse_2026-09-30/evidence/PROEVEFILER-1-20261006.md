== les-proevefiler: 2026-10-06T18:29:58Z ==
-- umask i en økt hos ops uten terminal: 0002. I et skall startet derfra (sh -c): 0002
-- det prøvestartene la igjen i /home/ops (rettighet, eier, byte, sist endret, navn)
   600  ops  0  2026-10-06 17:06:48Z  /home/ops/haven-deploy-proevestart-20261006-170648.kjoer.brukt
   600  ops  90  2026-10-06 17:06:53Z  /home/ops/haven-deploy-proevestart-20261006-170648.log
   600  ops  0  2026-10-06 18:27:42Z  /home/ops/haven-deploy-proevestart-20261006-182742.kjoer.brukt
   600  ops  90  2026-10-06 18:27:48Z  /home/ops/haven-deploy-proevestart-20261006-182742.log
   i alt 4 filer
-- loggene fra prøvestartene (høyst fire linjer av hver)
   haven-deploy-proevestart-20261006-170648.log:
      FEIL: commit maa vaere 40-hex, eller 'current' sammen med --env-only
      HAVEN_DEPLOY_SLUTT=2
   haven-deploy-proevestart-20261006-182742.log:
      FEIL: commit maa vaere 40-hex, eller 'current' sammen med --env-only
      HAVEN_DEPLOY_SLUTT=2
-- låsen til haven-deploy (rettighet, eier, navn)
   1777  root  /run/lock
   711  root  /run/lock/haven
   644  root  /run/lock/haven/haven-deploy.lock
   644  root  /run/lock/haven/haven-deploy.holder
Ingenting er kjørt på verten utover lesing, og ingenting er endret.
