STATUS: LEVERT — lest

# Admin i produksjon — lest, ikke endret

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-admin-prod-probe.sh` 2026-09-23T07:29:22Z. Bevis: `evidence/admin-tilgang/`.

## Brukere i produksjon

```text
db: 
  (ops kan ikke lese databasen)
```

## Hva wrapperen vil gjoere

Kall: `haven-admin-access <miljo> --plan <uuid1> <uuid2>`. Plan-modus skal ikke endre noe.
Vi kjoerer den med UUID-ene som allerede staar i prod-listen, slik at planen viser formen
paa endringen — erstatter den listene, eller legger den til? — uten aa foreslaa nye personer.

```text
REFUSED: two distinct UUIDs required
```

### Hjelpetekst

```text
usage: haven-admin-access [-h] (--plan | --apply PLAN_TOKEN)
                          {staging,production} first_uuid second_uuid

HD-0029: add two existing, environment-local users to operator + security.
Root installation is required. CLI accepts no path, key name, shell or
command. Does not deploy. --plan is read-only; --apply atomically updates
config pointer.

positional arguments:
  {staging,production}
  first_uuid
  second_uuid

options:
  -h, --help            show this help message and exit
  --plan
  --apply PLAN_TOKEN
```
