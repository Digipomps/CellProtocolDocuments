STATUS: KJØRER — http://localhost:9192 (Butler-arbeidsflaten)

# Lokal testvert for Butler-arbeidsflaten

Skrevet av `HAVEN-Deploy/_handoff/WP-R/start-testvert.sh` 2026-09-22T06:09:53Z.

Ingen testvert kjørte.
Testverten kjører på **http://localhost:9192** (pid 55836), bundet til 127.0.0.1 — ingen andre maskiner ser den.

Passkey: `RP_ID=localhost`, `RP_ORIGIN=http://localhost:9192` (uten dem bruker koden 9089, og nettleseren avviser passkey-en).

1. Åpne http://localhost:9192/login og lag en bruker (passkey eller passord; dette er en egen lokal testbase).
2. Åpne Butler-arbeidsflaten: <http://localhost:9192/browserhead/webo?configurationName=Co-Pilot%20Chat&configurationEndpoint=cell:///PersonalChatHub>

Dette er grenen `pdd/skjelett-elementer-web` @ `81b47bada14068cb9b98b015a1e7940412e302d8` mot CellProtocol `1b92d01a030bac424e5172c875753a1dcfe41752` — det samme T-P1 kjører mot. Staging og prod har ikke arbeidsflaten; grenene er ikke pushet.

Stopp verten med jobben `start-testvert.sh` og argumentet `stopp` (linje 6 i jobbfila), eller `kill 55836` i et terminalvindu.

Mens verten kjører bør ingen byggjobber kjøre i samme worktree.
