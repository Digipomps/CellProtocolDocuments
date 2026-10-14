STATUS: STOPPET — staging svarer ikke med 4db0b1d6d619863d7f56f74129755ec826670a43 — prod ikke rørt

# Metodikken i HAVEN — steg B2: staging og prod

Skrevet av `HAVEN-Deploy/_handoff/METODIKK/wp-metodikk-b2-ut.sh` 2026-09-25T01:23:56Z.

Før utrulling: staging `4dd70c520dac2d8921229fed767533c05b1c574b`, prod `6c70a59211e6be93ec33f5ba46a033bd103cb9ac`.

Staging kjører `4dd70c520dac2d8921229fed767533c05b1c574b` fra en annen tråd. Lånes for denne utrullingen og legges tilbake etterpå.

Image: `ghcr.io/digipomps/cellscaffold-web:sha-4db0b1d6d619863d7f56f74129755ec826670a43`

## staging

`sudo -n haven-ghcr-prefetch 4db0b1d6d619863d7f56f74129755ec826670a43` → exit 65
```text
FEIL: for lite diskplass for imagepull: 27 GiB / 13% ledig; krever minst 40 GiB og 4%
```

**STOPPET:** staging svarer ikke med 4db0b1d6d619863d7f56f74129755ec826670a43 — prod ikke rørt
