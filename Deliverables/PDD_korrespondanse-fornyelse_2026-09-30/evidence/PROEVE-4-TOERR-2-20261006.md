== bytt-invitasjoner: toerr, 2026-10-06T11:32:48Z ==
2026-10-06T11:32:48Z ok  tjenerfila har sjekksummen 57661ade26101eb1892f9e8fabdffe409508f5a34a2856e95b77566507bf6e0b
    sim-torrkjoring-a      gyldig i 164 timer til, tilgang til 2026-11-05T07:13:10.810Z
    sim-torrkjoring-b      gyldig i 164 timer til, tilgang til 2026-11-05T07:13:10.810Z
    vegar-local-agent      gyldig i 164 timer til, tilgang til 2026-11-05T07:13:10.810Z
    victoria-lille-robot   gyldig i 164 timer til, tilgang til 2026-11-05T07:13:10.810Z
2026-10-06T11:32:48Z ok  cellscaffold-app-1 kjører e5c3434510884275cae4a732935ab4b55cf7fad9
2026-10-06T11:32:49Z ok  /health/build oppgir samme revisjon, og miljøet staging
2026-10-06T11:32:50Z ok  /home/ops/cutover-invites-20260908.sh finnes på verten
2026-10-06T11:32:50Z ok  korrespondansevariablene i cellscaffold-app-1 (bare navnene): HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_DEVICE_ID HAVEN_ASSISTANT_CORRESPONDENCE_APPROVER_PARTICIPANT_ID HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64 
2026-10-06T11:32:51Z claimer på verten: ingen
-- bytteskriptet på verten: linjene som gjelder INVITES_FILE, og det det logger om utfallet
   133:if [[ -n "${INVITES_FILE:-}" ]]; then
   134:  [[ -r "${INVITES_FILE}" ]] || { log "FEIL: INVITES_FILE ikke lesbar: ${INVITES_FILE}"; false; }
   135:  grep -c '^HAVEN_ASSISTANT_CORRESPONDENCE_INVITES_BASE64=..*$' "${INVITES_FILE}" | grep -qx 1 \
   136:    || { log "FEIL: INVITES_FILE maa inneholde noeyaktig en ikke-tom INVITES_BASE64-linje"; false; }
   137:  [[ "$(wc -l < "${INVITES_FILE}")" -eq 1 ]] || { log "FEIL: INVITES_FILE maa vaere en enkelt linje"; false; }
   142:  cat "${INVITES_FILE}" >> "${ENV_FILE}.new"
   147:  log "INVITES_BASE64 erstattet fra ${INVITES_FILE} (ovrige ${ENV_BEFORE_LINES} miljolinjer uendret)"
   149:  log "INVITES_FILE ikke satt - arver invitasjonslisten uendret"
   224:log "COMMITTED_VERIFIED"
   sha256 av bytteskriptet: 7c227bf111f87516c0f20d90b68a0818b0d23140a0b4a3f05fc5ed40c239383e
-- tørrkjøring: dette ville utfoer gjort
   1. stoppe hvis en annen oppgave har claim på verten (nå: ingen)
   2. hd coord claim --task HD-0006 --host 89.167.90.101 --containers cellscaffold-app-1
   3. kopiere tjenerfila til verten som /home/ops/invites-20261006-fornyelse.env (rettighet 600)
   4. starte INVITES_FILE=/home/ops/invites-20261006-fornyelse.env /home/ops/cutover-invites-20260908.sh e5c3434510884275cae4a732935ab4b55cf7fad9 e5c3434510884275cae4a732935ab4b55cf7fad9
   5. vente på COMMITTED_VERIFIED i loggen (høyst 400 sekunder), eller på at byttet slutter uten
   6. kontrollere at revisjonen fortsatt er e5c3434510884275cae4a732935ab4b55cf7fad9, og at variabelnavnene er de samme som over
   7. hd coord release --task HD-0006
Ingenting er endret.
