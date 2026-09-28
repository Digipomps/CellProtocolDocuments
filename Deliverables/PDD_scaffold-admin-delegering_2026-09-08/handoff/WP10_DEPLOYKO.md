# WP10 — deploykø-post. Eier: Kjetil

Forberedt av Losen 2026-09-09. **Ikke kjørt.** Deploy-/image-steg planlegges aldri som
Codex-slice (`lesson.codex-sandbox-cannot-reach-docker`); dette er en HAVEN-Deploy-post.

## Forutsetninger som må være sanne først

| # | Forutsetning | Status |
|---|---|---|
| 1 | `pdd/scaffold-admin-delegering` er reviewet og landet i `CellScaffold` | **venter på git-administrator** |
| 2 | Full regresjon grønn mot baselinen på den landede commiten | grønn i worktreet 2026-09-09: 2150 tester, null nye feil |
| 3 | G3 godkjent av Kjetil mot `P/ACCEPT.md` | venter |
| 4 | CI har bygget webimaget fra nøyaktig den commiten, med `org.opencontainers.image.revision` lik hashen | venter |

## Selve posten

1. Bygg image fra godkjent commit. Registrer immutable digest.
2. Transaksjonell cutover på staging etter mønsteret i
   `/home/ops/cutover-invites-20260908.sh`: fingeravtrykk-vakt på dataroten, mounts arvet
   fra kjørende runtime, gammel container parkert som rollback, readiness- og
   revisjonsgate før commit. Den kjøringen tok 35 sekunder og har kvittering.
3. **Registrer administrator-entitetene.** Dette er det nye steget:
   - `entity:digipomps` som administrator for staging-scaffoldet
   - `entity:dimy` når Palazzo får sitt eget scaffold, og for Arendalsuka/konferanser når de flyttes
   - terskelpolicy settes eksplisitt til 1 med begrunnelse og dato, slik at
     `scaffold_administrator_threshold_below_two` står i `runtimeAdvisories` og unntaket er synlig
4. Verifiser mot kjørende tjeneste, ikke mot testene:
   - `administrator.state` svarer med organisasjonsentitet og **ingen personidentitet**
   - `runtimeAdvisories` inneholder terskeladvarselen
   - en identitet med `admin.operator` og uten mandat avvises på `mandate.issue`
5. Ingen prod før staging er verifisert. Prod har egen datarot
   (`/mnt/HC_Volume_104775511/haven-production/CellsContainer`) og egen seremoni.

## Rollback

Samme som cutover-skriptets: gammel container er parkert, ikke slettet. En feilet
registrering av administrator er en autorisasjonshandling som kan reverseres med
`administrator.transfer` tilbake, med begrunnelse — ikke ved å slette celle-state.

## Etterpå

**Planlagt nytteverdi, ikke levert:** Vegars publiseringstilgang kan først følges
opp når staging, organisasjonsregistrering og representantmyndighet er verifisert,
og den faktiske publiseringshandlingen er tilgjengelig og testet. På den målte
branchen er `publisherAccess.issue` ikke implementert; WP2s grønne målcelle-test
bruker `resetEditableCellConfiguration`. Deploy alene beviser derfor ikke at
publiseringstilgangen er gjenopprettet. Dette er fortsatt en egen oppgave; se
[hurtigfiksfunnene](VEGAR_HURTIGFIKS_FUNN.md) og [akseptansens avgrensning](../ACCEPT.md#status).

WP9-presisering 2026-09-09: dette dokumentet er den forberedte postteksten.
WP9 har ingen kvittering for registrering i HAVEN-Deploy og har ikke opprettet
eller utført en ekstern køpost, et image eller en deploy.
