== les-beholder: 2026-10-06T11:48:09Z ==
tid på verten nå:      2026-10-06T11:48:10Z
containeren laget:     2026-10-05T13:10:06Z, startet 2026-10-05T13:10:18Z
revisjon (merkelapp):  e5c3434510884275cae4a732935ab4b55cf7fad9
bildet den kjører:     84466586cc65aff8315fd52d…
bildenavn ved start:   cellscaffold-staging-local:sha-<skjult>
-- det bytteskriptet skriver selv, slik det står i containeren nå
kommando:              ["serve","--env","production","--hostname","0.0.0.0","--port","8081"]
inngang (entrypoint):  ["/usr/local/bin/cellscaffold-entrypoint"]
porter:                {"8081/tcp":[{"HostIp":"127.0.0.1","HostPort":"8081"}]}
delt minne:            67108864
logg:                  {"Type":"json-file","Config":{"max-file":"3","max-size":"10m"}}
omstart:               {"Name":"unless-stopped","MaximumRetryCount":0}
-- det bytteskriptet ikke fører videre, hvis det er satt
nettverk:              {"modus":"bridge","nett":["bridge"]}
bruker, arbeidsmappe:  ["vapor:vapor","/app"]
grenser og rettigheter: {"minne":0,"cpu":0,"capAdd":null,"capDrop":null,"sikkerhet":null,"skrivebeskyttet":false,"init":null,"privilegert":false,"tmpfs":[],"ulimits":[],"ekstraverter":null,"dns":null,"pid":"","ipc":"private"}
helsesjekk i containeren: null
merkelapper (navn):    ["org.haven.cellprotocol-documents.revision","org.opencontainers.image.created","org.opencontainers.image.description","org.opencontainers.image.licenses","org.opencontainers.image.revision","org.opencontainers.image.source","org.opencontainers.image.title","o
miljøvariabler:        94 (bare antallet er lest)
-- mounts (type, mål, skrivbar, kilde)
   bind  /run/secrets/alertmanager-notification-relay-token  ro  /etc/haven/cellscaffold-runtime-secrets-f76de5a/admin-alert-relay-token
   bind  /etc/haven/cellscaffold-runtime-secrets/runtime-identity-manifest.v2.json  ro  /etc/haven/cellscaffold-runtime-identity-manifest-f76de5a/runtime-identity-manifest.v2.json
   bind  /run/cellscaffold-key-continuity  ro  /var/lib/haven/cellscaffold-key-continuity-f76de5a
   bind  /app/CellsContainer  rw  /mnt/disk1/app/CellsContainer.staging-f76de5a
   bind  /run/secrets/apns-auth-key.p8  ro  /etc/haven/cellscaffold-runtime-secrets-f76de5a/apns-auth-key.p8
   bind  /run/secrets/admin-bridge-client-credential.json  ro  /etc/haven/cellscaffold-runtime-secrets-f76de5a/admin-bridge-client-credential.json
   bind  /run/secrets/cell-vault-master-key  ro  /etc/haven/cellscaffold-runtime-secrets-f76de5a/cell-vault-master-key
-- bildet bytteskriptet vil bruke
finnes:                ja, under navnet cellscaffold-staging-local:sha-<revisjonen over>
bildets id:            84466586cc65aff8315fd52d…
samme bilde som kjører: JA
revisjon (merkelapp):  e5c3434510884275cae4a732935ab4b55cf7fad9
laget (merkelapp):     2026-09-30T08:13:00Z
bildets egen kommando: [["/usr/local/bin/cellscaffold-entrypoint"],["serve","--env","production","--hostname","0.0.0.0","--port","8080"]]
navn på bildet:        ["cellscaffold-production-candidate:sha-<skjult>","cellscaffold-staging-local:sha-<skjult>","ghcr.io/digipomps/cellscaffold-web:sha-<skjult>"]
-- containere med cellscaffold-app-1 i navnet (navn, tilstand)
cellscaffold-app-1  Up 23 hours
cellscaffold-app-1-rollback-20261005T130952Z-staging-e5c34345  Exited (0) 23 hours ago
cellscaffold-app-1-rollback-20260930T202428Z-415ea3d2  Exited (0) 5 days ago
cellscaffold-app-1-rollback-20260930T202347Z-staging-415ea3d2  Exited (0) 5 days ago
cellscaffold-app-1-rollback-20260928T031723Z-staging-feec2372  Exited (0) 8 days ago
cellscaffold-app-1-rollback-20260925T120348Z-staging-4dd70c52  Exited (0) 11 days ago
cellscaffold-app-1-rollback-20260925T120232Z-staging-18c14c32  Exited (0) 11 days ago
cellscaffold-app-1-rollback-20260925T045638Z-staging-4dd70c52  Exited (0) 11 days ago
cellscaffold-app-1-rollback-20260925T044817Z-staging-e6277af1  Exited (0) 11 days ago
cellscaffold-app-1-rollback-20260924T135808Z-staging-4dd70c52  Exited (0) 11 days ago
cellscaffold-app-1-rollback-20260924T115310Z-staging-6c70a592  Exited (0) 12 days ago
cellscaffold-app-1-rollback-20260924T073914Z-staging-60e5a64d  Exited (0) 12 days ago
cellscaffold-app-1-rollback-20260924T040140Z-staging-03fc0eff  Exited (0) 12 days ago
cellscaffold-app-1-rollback-20260923T162113Z-staging-f262a8eb  Exited (0) 12 days ago
cellscaffold-app-1-rollback-20260923T093913Z-staging-77a922bc  Exited (0) 13 days ago
cellscaffold-app-1-rollback-20260922T160255Z-staging-77a922bc  Exited (0) 13 days ago
cellscaffold-app-1-rollback-20260918T150253Z-staging-e3ae9fc0  Exited (0) 2 weeks ago
cellscaffold-app-1-rollback-20260918T083112Z-staging-87256f9a  Exited (0) 2 weeks ago
cellscaffold-app-1-rollback-20260915T201702Z-staging-b4a2779a  Exited (0) 2 weeks ago
cellscaffold-app-1-rollback-20260915T085456Z-staging-6c391437  Exited (0) 3 weeks ago
-- verktøy bytteskriptet bruker
   jq finnes
   curl finnes
   docker finnes
   getent finnes
   sha256sum finnes
vertsnavn:             ubuntu-16gb-hel1-1
-- loggen fra byttet 30.09 (/home/ops/cutover-invites-20260930.log), bare linjene med tid, lange tegnrekker strøket
2026-09-30T20:24:28Z PREFLIGHT_GREEN image=sha256:<skjult> <skjult>
2026-09-30T20:24:28Z fingerprint_before: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
2026-09-30T20:24:28Z INVITES_BASE64 erstattet fra /home/ops/invites-20260930-kjetil.env (ovrige 94 miljolinjer uendret)
2026-09-30T20:24:28Z ADVARSEL: kan ikke avgjøre om mount-kilde finnes (ingen lesetilgang): /etc/haven/cellscaffold-runtime-secrets-f76de5a/admin-bridge-client-credential.json
2026-09-30T20:24:28Z ADVARSEL: kan ikke avgjøre om mount-kilde finnes (ingen lesetilgang): /etc/haven/cellscaffold-runtime-secrets-f76de5a/cell-vault-master-key
2026-09-30T20:24:28Z ADVARSEL: kan ikke avgjøre om mount-kilde finnes (ingen lesetilgang): /etc/haven/cellscaffold-runtime-secrets-f76de5a/admin-alert-relay-token
2026-09-30T20:24:28Z ADVARSEL: kan ikke avgjøre om mount-kilde finnes (ingen lesetilgang): /etc/haven/cellscaffold-runtime-identity-manifest-f76de5a/runtime-identity-manifest.v2.json
2026-09-30T20:24:28Z ADVARSEL: kan ikke avgjøre om mount-kilde finnes (ingen lesetilgang): /var/lib/haven/cellscaffold-key-continuity-f76de5a
2026-09-30T20:24:28Z ADVARSEL: kan ikke avgjøre om mount-kilde finnes (ingen lesetilgang): /etc/haven/cellscaffold-runtime-secrets-f76de5a/apns-auth-key.p8
2026-09-30T20:24:28Z arver 7 mounts fra kjørende runtime
2026-09-30T20:24:29Z DEPLOYING gammel runtime parkert som cellscaffold-app-1-rollback-20260930T202428Z-415ea3d2
2026-09-30T20:24:39Z READY_OK (foerste-start) etter 15s
2026-09-30T20:24:40Z fingerprint_first: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
2026-09-30T20:24:40Z kontrollert restart
2026-09-30T20:24:50Z READY_OK (restart) etter 15s
2026-09-30T20:24:51Z fingerprint_second: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
2026-09-30T20:24:51Z COMMITTED_VERIFIED
Ingenting er kjørt på verten utover lesing, og ingenting er endret.
