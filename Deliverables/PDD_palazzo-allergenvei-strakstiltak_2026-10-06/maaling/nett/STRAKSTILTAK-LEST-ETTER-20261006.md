# HD-0077 strakstiltaket: lest foer utsetting — 2026-10-06T14:53:01Z
utgaven som staar i dag: c5058f49640fc71a2b684713e7406add9e81b183

=== 1 claimene (hd coord status)
    claimer i alt: 0
    claimer paa verten 89.167.90.101: 0

=== 2 status for HD-0077
    status: COMMITTED_VERIFIED   forsoek: 23

=== 3 verten (ops, kun lesing)
## Verten 2026-10-06T14:53:02Z som ops
container:      ghcr.io/dimy-io/palazzoscaffold:sha-c5058f49640fc71a2b684713e7406add9e81b183 · Up 2 hours (healthy)
startet:        2026-10-06T13:19:12.002206162Z
omstarter:      0
PALAZZO_IMAGE:  ghcr.io/dimy-io/palazzoscaffold:sha-c5058f49640fc71a2b684713e7406add9e81b183

## imaget for utgaven som staar i dag
lokalt paa verten: ja (revisjon c5058f49640fc71a2b684713e7406add9e81b183)

## lokale image av palazzoscaffold
  ghcr.io/dimy-io/palazzoscaffold:sha-c5058f49640fc71a2b684713e7406add9e81b183 · 2 hours ago · 555MB
  ghcr.io/dimy-io/palazzoscaffold:sha-a3fc5042e15bbb6d2b896c116d980cad0b21bf2e · 43 hours ago · 554MB
  ghcr.io/dimy-io/palazzoscaffold:sha-771f991e7f010ca822679fb903c3c43038a6bccd · 2 days ago · 554MB

## aapne innstillinger i /opt/palazzo/.env (ingen hemmelighet)
  PALAZZO_HOST_PORT=8086
  LOG_LEVEL=info
  PALAZZO_BRIDGEHEAD_ENABLED=false
  PALAZZO_DEMO_SURFACES_ENABLED=true
  PALAZZO_CONCIERGE_MODEL_ENABLED=true
  PALAZZO_CONCIERGE_MODEL=claude-haiku-4-5-20251001

## ledig disk
  /: 48.9 GiB ledig av 149.9 GiB

## conciergens formuleringslinjer siden containeren startet
antall linjer: 183
foerste:       2026-10-06T13:19:19.814093046Z
siste:         2026-10-06T14:53:01.685052991Z

## antall per utfall
      125 utfall=allergi-henvisning:ordliste
       16 utfall=ikke-sendt:ikke-aapent-spoersmaal
       12 utfall=ikke-sendt:ikke-besvart
        7 utfall=modell
        6 utfall=ikke-sendt:kontakt
        4 utfall=ikke-sendt:holdes-ordrett
        4 utfall=ikke-sendt:flere-kolon
        3 utfall=ikke-sendt:handling
        3 utfall=allergi-henvisning:merking
        2 utfall=ikke-sendt:spoersmaal
        1 utfall=ikke-sendt:forbehold:ingen

## antall per handling
      180 handling=ask
        2 handling=beverages
        1 handling=menu

## antall per time (UTC)
      114 2026-10-06T13
       69 2026-10-06T14

## linjer som ikke har formen «concierge-formulering handling=<ord> utfall=<kode>» (skal vaere 0)
0
<!-- LES-FOER-BYTTE FERDIG gammelt_image_lokalt=ja -->

=== 4 GHCR: imaget for utgaven som staar i dag (root, --check)
    GHCR_CHECK_OK image=ghcr.io/dimy-io/palazzoscaffold:sha-c5058f49640fc71a2b684713e7406add9e81b183

<!-- LEST FOER UTSETTING claims_paa_verten=0 gammelt_image_lokalt=ja ghcr_gammelt=ok -->
