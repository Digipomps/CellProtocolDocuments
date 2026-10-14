STATUS: LEVERT — lest

# Kjenner haven-deploy paa verten `--env-only`?

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-envonly-sjekk.sh` 2026-09-23T09:36:05Z. Bevis: `evidence/arendalsuka-utsteder/`.

## Hjelpeteksten (det vakten leser)

```text
/usr/local/sbin/haven-deploy: line 51: 2: commit kreves (40-hex)
```

Nevner hjelpeteksten flagget? **0
ukjent** treff.

## Finnes flagget i selve skriptet?

```text
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
```

## Kvittering fra kjoeringen 07:34Z

```text
20260922T212341Z-production-77a922bc
20260922T212423Z-production-77a922bc
20260923T073431Z-production-77a922bc
```
