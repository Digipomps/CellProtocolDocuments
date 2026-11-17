== les-haven-deploy-2: 2026-10-06T11:59:01Z ==
-- hodet i den installerte haven-deploy (linje 1–34)
     1	#!/usr/bin/env bash
     2	# Fullstendig deploy for CellScaffold, ett miljoe om gangen — én operasjon, ingen mennesker.
     3	#
     4	# Kjører hele sekvensen og ender i nøyaktig én av to tilstander:
     5	#
     6	#   committed_verified  — prod kjører den nye revisjonen, verifisert
     7	#   rolled_back         — prod kjører den gamle revisjonen igjen, verifisert
     8	#
     9	# Den tredje tilstanden — «halvveis, ring Kjetil» — er det denne finnes for å
    10	# fjerne. Derfor gjenoppretter rollback BÅDE containeren og manifestet: etter
    11	# seremonien kan ikke den gamle containeren starte på det nye manifestet, så en
    12	# container-rollback alene ville etterlatt prod nede.
    13	#
    14	#   haven-deploy <miljoe> <40-hex commit> [--preflight | --verify | --wait <sek>]
    15	#                                         [--env-only]
    16	#
    17	# Med --env-only kan commit skrives som 'current'; da leses revisjonen fra
    18	# containeren som kjoerer, saa ingen runbook trenger aa pinne en sha.
    19	#
    20	# --env-only deployer SAMME revisjon paa nytt for aa faa ny env i kraft, uten
    21	# aa foere manifestet videre. Bruk den naar env maa endres - for eksempel nye
    22	# korrespondanse-invitasjoner - og revisjonen skal staa. Alt annet er likt:
    23	# env, mounts og kommandolinje arves fra kjoerende container, helsesjekk og
    24	# rollback gjelder. Det finnes derfor ingen grunn til aa skrive et eget
    25	# recreate-skript ved siden av dette; en haandrullet dublett arver ingen av
    26	# vaktene her, og har allerede kostet nedetid to ganger.
    27	#
    28	# --preflight leser og rapporterer. Den rører verken manifest, vault eller
    29	# container.
    30	#
    31	# Env settes fra to felt i miljoekonfigen. SET_ENV er kommaseparerte
    32	# KEY=VALUE for verdier miljoeet MAA ha. SET_ENV_FILE peker paa en fil med
    33	# én KEY=VALUE per linje, for generert materiale som ikke skal baeres for
    34	# haand - invitasjonsblobben er 2-4 kB base64, og aa lime den inn i konfigen
-- linjene om SET_ENV_FILE, med to linjer rundt
30-#
31-# Env settes fra to felt i miljoekonfigen. SET_ENV er kommaseparerte
32:# KEY=VALUE for verdier miljoeet MAA ha. SET_ENV_FILE peker paa en fil med
33-# én KEY=VALUE per linje, for generert materiale som ikke skal baeres for
34-# haand - invitasjonsblobben er 2-4 kB base64, og aa lime den inn i konfigen
--
103-STRIP_ENV="$(cfg STRIP_ENV)"
104-SET_ENV="$(cfg SET_ENV)"
105:SET_ENV_FILE="$(cfg SET_ENV_FILE)"
106-for k in OLD_NAME IMAGE_REPOSITORY HEALTH_URL PROVISION_CONFIG EVIDENCE_ROOT_BASE; do
107-  [[ -n "${!k}" ]] || { echo "FEIL: ${CONFIG} mangler felt for ${k}"; exit 2; }
--
463-# En arvet verdi som er feil skal erstattes, ikke suppleres.
464-# >>> set-env-merge (dekket av scripts/tests/test_haven_deploy_set_env.py)
465:# SET_ENV_FILE finnes fordi den genererte verdien ikke skal baeres for haand.
466-# Invitasjonsblobben er 2-4 kB base64 som generatoren allerede skriver til fil;
467-# aa lime den inn i denne konfigen mellom to vinduer er samme feilklasse som en
--
479-    # Fail-closed: to kilder som setter samme noekkel er en uavklart hensikt,
480-    # ikke en presedensregel aa gjette paa.
481:    [[ "${existing}" == "${key}" ]] && die "${key} settes baade i SET_ENV og SET_ENV_FILE"
482-  done
483-  SET_ENV_KEYS+=("${key}")
--
489-done
490-
491:if [[ -n "${SET_ENV_FILE}" ]]; then
492:  [[ -f "${SET_ENV_FILE}" ]] || die "SET_ENV_FILE finnes ikke: ${SET_ENV_FILE}"
493-  # Fila styrer miljoevariabler i en privilegert deploy og baerer hemmeligheter.
494-  # Er den skrivbar for andre enn eier, er den en angrepsflate, ikke en kilde.
--
502-    stat -c "$1" "$3" 2>/dev/null || stat -f "$2" "$3"
503-  }
504:  file_perm="$(stat_field '%a' '%Lp' "${SET_ENV_FILE}")"
505:  file_owner="$(stat_field '%u' '%u' "${SET_ENV_FILE}")"
506-  [[ "${file_owner}" == "${EUID}" ]] \
507:    || die "SET_ENV_FILE maa eies av den som kjoerer deployen: ${SET_ENV_FILE} (uid ${file_owner}, forventet ${EUID})"
508:  [[ "${file_perm}" =~ ^[0-7][0-7][0-7]$ ]] || die "SET_ENV_FILE har uleselig modus: ${SET_ENV_FILE} (${file_perm})"
509-  [[ $(( 8#${file_perm} & 8#022 )) -eq 0 ]] \
510:    || die "SET_ENV_FILE gir skriverett til gruppe eller andre: ${SET_ENV_FILE} (${file_perm})"
511-  set_env_file_count=0
512-  while IFS= read -r line || [[ -n "${line}" ]]; do
--
514-    line="${line%"${line##*[![:space:]]}"}"
515-    [[ -z "${line}" || "${line}" == \#* ]] && continue
516:    add_set_env_pair "${line}" "SET_ENV_FILE"
517-    set_env_file_count=$((set_env_file_count + 1))
518:  done < "${SET_ENV_FILE}"
519:  [[ "${set_env_file_count}" -gt 0 ]] || die "SET_ENV_FILE er tom: ${SET_ENV_FILE}"
520-fi
521-
--
532-  grep -Fxq "${pair}" "${ENV_FILE}" || die "${key} kom ikke med i arvet env"
533-done
534:log "arver $(wc -l < "${ENV_FILE}") env-variabler (fjernet: ${STRIP_ENV:-<ingen>}; satt: ${SET_ENV_KEYS[*]:-<ingen>}${SET_ENV_FILE:+; fil: ${SET_ENV_FILE}})"
535-# <<< set-env-merge
536-
-- linjene om env-only
15:#                                         [--env-only]
17:# Med --env-only kan commit skrives som 'current'; da leses revisjonen fra
20:# --env-only deployer SAMME revisjon paa nytt for aa faa ny env i kraft, uten
36:# hver deploy, saa en ny generering trer i kraft med --env-only alene. Setter
55:[[ "${COMMIT}" =~ ^[0-9a-f]{40}$ || "${COMMIT}" == "current" ]] || { echo "FEIL: commit maa vaere 40-hex, eller 'current' sammen med --env-only"; exit 2; }
56:[[ "${MODE}" == "run" || "${MODE}" == "--preflight" || "${MODE}" == "--verify" || "${MODE}" == "--wait" || "${MODE}" == "--env-only" ]] || { echo "FEIL: ukjent modus ${MODE}"; exit 2; }
116:  [[ "${MODE}" == "--env-only" ]] || { echo "FEIL: 'current' er bare gyldig sammen med --env-only"; exit 2; }
120:  echo "$(date -u +%FT%TZ) ENV_ONLY utledet revisjon ${COMMIT} fra ${OLD_NAME}"
238:if [[ "${MODE}" == "--env-only" ]]; then
245:    || die "--env-only krever at ${ENVIRONMENT} allerede kjoerer ${COMMIT} (kjoerer ${PREV_COMMIT})"
247:    || die "--env-only krever manifest signert for ${COMMIT} (signert for ${MANIFEST_REVISION})"
248:  log "ENV_ONLY samme revisjon ${COMMIT}; manifestet foeres ikke videre"
469:# hver deploy, saa en ny generering trer i kraft med --env-only alene.
576:if [[ "${MODE}" != "--env-only" ]]; then
597:log "ENV_ONLY seremonien hoppes over; manifestet staar urort paa ${COMMIT}"
-- linjene som tolker argumentene (MODE)
48:  MODE="${3:-run}"
52:  MODE="${3:-run}"
66:  MODE="run"
-- det ops har lov til med sudo uten passord (sudo -n -l)
User ops may run the following commands on ubuntu-16gb-hel1-1:
    (root) NOPASSWD: /usr/local/sbin/haven-admin-access
    (root) NOPASSWD: /usr/local/sbin/haven-deploy
    (root) NOPASSWD: /usr/local/sbin/haven-deploy-doctor
    (root) NOPASSWD: /usr/local/sbin/haven-ghcr-prefetch
    (root) NOPASSWD: /usr/local/sbin/haven-ghcr-prefetch-production
    (root) NOPASSWD: /usr/local/sbin/haven-manifest-provision
    (root) NOPASSWD: /usr/bin/systemctl start haven-deploy@*
    (root) NOPASSWD: /usr/bin/systemctl status haven-deploy@*
    (root) NOPASSWD: /usr/bin/systemctl is-active haven-deploy@*
    (root) NOPASSWD: /usr/bin/journalctl -u haven-deploy@*
-- kan ops se fila? (bare om den kan leses, ikke innholdet)
   nei (det er ventet: /etc/haven er lukket for ops)
Ingenting er kjørt på verten utover lesing, og ingenting er endret.
