== bytt-invitasjoner: toerr, 2026-10-06T19:42:21Z ==
2026-10-06T19:42:21Z ok  tjenerfila har sjekksummen 57661ade26101eb1892f9e8fabdffe409508f5a34a2856e95b77566507bf6e0b
    sim-torrkjoring-a      gyldig i 156 timer til, tilgang til 2026-11-05T07:13:10.810Z
    sim-torrkjoring-b      gyldig i 156 timer til, tilgang til 2026-11-05T07:13:10.810Z
    vegar-local-agent      gyldig i 156 timer til, tilgang til 2026-11-05T07:13:10.810Z
    victoria-lille-robot   gyldig i 156 timer til, tilgang til 2026-11-05T07:13:10.810Z
2026-10-06T19:42:22Z ok  cellscaffold-app-1 kjører e5c3434510884275cae4a732935ab4b55cf7fad9
2026-10-06T19:42:23Z ok  /health/build oppgir samme revisjon, og miljøet staging
2026-10-06T19:42:23Z ok  korrespondansevariablene i cellscaffold-app-1 (bare navnene): HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_DEVICE_ID HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_PARTICIPANT_ID HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 
2026-10-06T19:42:25Z ok  haven-deploy på verten er utgaven som er lest, og ops kan kjøre den med sudo
2026-10-06T19:42:25Z ok  verten har verktøyene skriptet bruker der
2026-10-06T19:42:26Z ok  logind lar prosessene til ops leve etter utlogging (KillUserProcesses er av)
2026-10-06T19:42:26Z ok  låsen til haven-deploy er fri: ingen utsetting går på verten nå
2026-10-06T19:42:27Z ok  lista som kjører i cellscaffold-app-1, har 5 invitasjoner: 5 er utløpt, 0 gjelder fortsatt
2026-10-06T19:42:27Z ok  den nye lista tar ikke bort noen invitasjon som fortsatt gjelder, ut over det som er godtatt
2026-10-06T19:42:28Z ok  /etc/haven/deploy-staging.conf peker på /etc/haven/staging-correspondence-invites.env (eies av root, rettighet 600, sist endret 2026-09-23T09:39:13Z)
2026-10-06T19:42:28Z     variablene i fila (bare navnene, 6 linjer): HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_PARTICIPANT_ID MVP_ADMIN_OPERATOR_USER_IDS MVP_ADMIN_SECURITY_USER_IDS HAVEN_CREDENTIAL_MASTER_KEY HAVEN_ARENDALSUKA_PUBLISHER_BOOTSTRAP_USERNAME 
2026-10-06T19:42:28Z     HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 står på linje 1. Kopier av fila fra tidligere bytter ved siden av den: 0
2026-10-06T19:42:28Z     lista i fila og lista i containeren er den samme nå
2026-10-06T19:42:29Z claimer på verten: ingen
-- tørrkjøring: dette ville utfoer gjort
   1. stoppe hvis en annen oppgave har claim på verten (nå: ingen), eller hvis noe over er merket HINDER
   2. hd coord claim --task HD-0006 --host 89.167.90.101 --containers cellscaffold-app-1
   3. prøvestart: starte haven-deploy med en revisjon som ikke finnes, og se at den avviser den og at sluttmerket kommer
   4. kopiere tjenerfila til verten som /home/ops/invites-20261006-fornyelse.env (rettighet 600)
   5. som root: kopiere /etc/haven/staging-correspondence-invites.env til /etc/haven/staging-correspondence-invites.env.foer-20261006-<klokkeslett>, og bytte linja HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 der den står
   6. som ops: sudo -n /usr/local/sbin/haven-deploy staging current --env-only (nedetid ca. 35 sekunder 05.10)
   7. vente til haven-deploy melder at den er ferdig (høyst 25 minutter)
   8. kontrollere at revisjonen er e5c3434510884275cae4a732935ab4b55cf7fad9, at miljøet er staging, at variabelnavnene er de samme, og at lista i containeren har sjekksummen til tjenerfila
   9. hd coord release --task HD-0006
   Gjør ikke haven-deploy byttet, legges linja tilbake fra kopien etter at containeren er kontrollert som den gamle.
Ingenting er endret.
