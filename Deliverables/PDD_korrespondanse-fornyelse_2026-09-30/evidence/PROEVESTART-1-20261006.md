== bytt-invitasjoner: proevestart, 2026-10-06T17:06:43Z ==
2026-10-06T17:06:43Z ok  tjenerfila har sjekksummen 57661ade26101eb1892f9e8fabdffe409508f5a34a2856e95b77566507bf6e0b
    sim-torrkjoring-a      gyldig i 158 timer til, tilgang til 2026-11-05T07:13:10.810Z
    sim-torrkjoring-b      gyldig i 158 timer til, tilgang til 2026-11-05T07:13:10.810Z
    vegar-local-agent      gyldig i 158 timer til, tilgang til 2026-11-05T07:13:10.810Z
    victoria-lille-robot   gyldig i 158 timer til, tilgang til 2026-11-05T07:13:10.810Z
2026-10-06T17:06:44Z ok  cellscaffold-app-1 kjører e5c3434510884275cae4a732935ab4b55cf7fad9
2026-10-06T17:06:44Z ok  /health/build oppgir samme revisjon, og miljøet staging
2026-10-06T17:06:45Z ok  korrespondansevariablene i cellscaffold-app-1 (bare navnene): HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_DEVICE_ID HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_PARTICIPANT_ID HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 
2026-10-06T17:06:46Z ok  haven-deploy på verten er utgaven som er lest, og ops kan kjøre den med sudo
2026-10-06T17:06:46Z ok  verten har verktøyene skriptet bruker der
2026-10-06T17:06:47Z ok  logind lar prosessene til ops leve etter utlogging (KillUserProcesses er av)
2026-10-06T17:06:47Z ok  låsen til haven-deploy er fri: ingen utsetting går på verten nå
2026-10-06T17:06:48Z ok  lista som kjører i cellscaffold-app-1, har 5 invitasjoner: 5 er utløpt, 0 gjelder fortsatt
2026-10-06T17:06:48Z ok  den nye lista tar ikke bort noen invitasjon som fortsatt gjelder, ut over det som er godtatt
2026-10-06T17:06:59Z ok  prøvestart: skallet levde i 5 sekunder etter at forbindelsen var lukket, sudo kjørte så haven-deploy derfra uten terminal, og sluttmerket kom i loggen (kode 2, som ventet for en revisjon som ikke finnes)
-- proevestart: root-innlogging er ikke brukt, claimene er ikke lest, og verken fila under /etc/haven eller containeren er rørt.
   Hos ops ligger loggen fra prøven og startmerket igjen: /home/ops/haven-deploy-proevestart-20261006-170648.log
