== les-fingeravtrykk: 2026-10-06T11:51:19Z ==
-- de to kjøringene 08.09 (linjene med tid, uten advarslene om mounts)
   /home/ops/cutover-invites-20260908.log
      2026-09-08T12:55:46Z PREFLIGHT_GREEN image=sha256:<skjult> <skjult>
      2026-09-08T12:55:47Z fingerprint_before: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
      2026-09-08T12:55:47Z INVITES_BASE64 erstattet fra /home/ops/corr-invites-20260908.env (ovrige 92 miljolinjer uendret)
      2026-09-08T12:55:47Z arver 7 mounts fra kjørende runtime
      2026-09-08T12:55:57Z DEPLOYING gammel runtime parkert som cellscaffold-app-1-rollback-20260908T125546Z-b8df547e
      2026-09-08T12:56:08Z READY_OK (foerste-start) etter 15s
      2026-09-08T12:56:08Z fingerprint_first: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
      2026-09-08T12:56:08Z kontrollert restart
      2026-09-08T12:56:19Z READY_OK (restart) etter 15s
      2026-09-08T12:56:20Z fingerprint_second: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
      2026-09-08T12:56:20Z COMMITTED_VERIFIED
   /home/ops/cutover-invites-20260908b.log
      2026-09-08T13:04:31Z PREFLIGHT_GREEN image=sha256:<skjult> <skjult>
      2026-09-08T13:04:32Z fingerprint_before: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
      2026-09-08T13:04:32Z INVITES_BASE64 erstattet fra /home/ops/corr-invites-20260908b.env (ovrige 92 miljolinjer uendret)
      2026-09-08T13:04:32Z arver 7 mounts fra kjørende runtime
      2026-09-08T13:04:33Z DEPLOYING gammel runtime parkert som cellscaffold-app-1-rollback-20260908T130431Z-b8df547e
      2026-09-08T13:04:43Z READY_OK (foerste-start) etter 15s
      2026-09-08T13:04:44Z fingerprint_first: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
      2026-09-08T13:04:44Z kontrollert restart
      2026-09-08T13:04:55Z READY_OK (restart) etter 15s
      2026-09-08T13:04:55Z fingerprint_second: ScaffoldOrchestrator/NamedEmitters.<skjult> <skjult>.<skjult> db.<skjult> <skjult> 
      2026-09-08T13:04:55Z COMMITTED_VERIFIED
-- dataroten: /mnt/disk1/app/CellsContainer.staging-f76de5a
-- første måling, 11:51:21Z (tider i UTC)
   db.sqlite: 495616 byte, endret 2026-10-06 07:16:41, sha256 6ca3f1aebcd6
   db.sqlite-wal: finnes ikke
   db.sqlite-shm: finnes ikke
   db.sqlite-journal: finnes ikke
   ScaffoldOrchestrator/NamedEmitters.json: 2374 byte, endret 2026-10-05 13:12:33, sha256 5980c54f2a77
   ScaffoldOrchestrator/IdentityNamedEmitters.json: 75949 byte, endret 2026-10-06 07:19:39, sha256 eb40ed8dfd14
   IdentityVaults: 65 filer, nyeste endret 2026-09-28 12:35:23, samlet sha256 1efaf57d6d70
-- andre måling, 11:51:46Z
   db.sqlite: 495616 byte, endret 2026-10-06 07:16:41, sha256 6ca3f1aebcd6
   db.sqlite-wal: finnes ikke
   db.sqlite-shm: finnes ikke
   db.sqlite-journal: finnes ikke
   ScaffoldOrchestrator/NamedEmitters.json: 2374 byte, endret 2026-10-05 13:12:33, sha256 5980c54f2a77
   ScaffoldOrchestrator/IdentityNamedEmitters.json: 75949 byte, endret 2026-10-06 07:19:39, sha256 eb40ed8dfd14
   IdentityVaults: 65 filer, nyeste endret 2026-09-28 12:35:23, samlet sha256 1efaf57d6d70
LIKT: ingenting av det fingeravtrykket dekker, endret seg på 25 sekunder.
containeren cellscaffold-app-1: running, startet 2026-10-05T13:10:18.000726989Z
cellscaffold-app-1 er ikke rørt, og ingenting er endret.
