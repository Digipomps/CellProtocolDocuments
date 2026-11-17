== les-haven-deploy: 2026-10-06T11:55:51Z ==
haven-deploy i CellScaffold-mappen på Macen: sha256 05e52252387a5e87b10d9948d27235d65d034da074c8d954e6285cb071e2c7eb
-- den installerte haven-deploy
   sist endret 2026-09-01T20:27:03Z, 675 linjer, sha256 339a03a4507b86da683d0e0bd38df2c0e8851708167236d31d59d6cd4c1ce400
   linjer som nevner --env-only: 12
   linjer som nevner SET_ENV_FILE: 15
   linjer som nevner db_size: 1
-- loggen fra utsettingen som laget containeren som kjører (journalen for haven-deploy@staging-<revisjonen>)
   antall linjer i alt: 50
   2026-10-05T13:09:54Z PREFLIGHT_GREEN prev=<verdi> image=<verdi>
   2026-10-05T13:09:54Z arver 94 env-variabler (fjernet: CELL_SCAFFOLD_STAGING_MANIFEST_BYPASS; satt: VAPOR_ENV ARENDALSUKA_REMOTE_CONFIGURATION_ACCESS HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_PARTICIPANT_ID MVP_ADMIN_OPERATOR_USER_IDS MVP_ADMIN_SECURITY_USER_IDS HAVEN_CREDENTIAL_MASTER_KEY HAVEN_ARENDALSUKA_PUBLISHER_BOOTSTRAP_USERNAME; fil: /etc/haven/staging-correspondence-invites.env)
   2026-10-05T13:09:54Z arver 7 mounts
   2026-10-05T13:09:54Z arver kommando: serve --env production --hostname 0.0.0.0 --port 8081
   2026-10-05T13:10:06Z DEPLOYING gammel runtime parkert som cellscaffold-app-1-rollback-20261005T130952Z-staging-e5c34345
   2026-10-05T13:10:17Z READY_OK (foerste-start) etter 15s
   2026-10-05T13:10:17Z kontrollert restart
   2026-10-05T13:10:28Z READY_OK (restart) etter 15s
   2026-10-05T13:10:28Z COMMITTED_VERIFIED
-- navnene på variablene haven-deploy satte (fra «satt:» i siste «arver»-linje)
   VAPOR_ENV ARENDALSUKA_REMOTE_CONFIGURATION_ACCESS HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 HAVEN_ASSISTANT_CORRE
-- har containeren en invitasjonsliste i miljøet nå? (bare lengden på verdien)
   ja, 4115 tegn
Ingenting er kjørt på verten utover lesing, og ingenting er endret.
