# Ordlistetrådene (7. oktober 2026 kl. 09:42–09:57 UTC)

Stier er relative til denne mappen der ikke annet står.

Etter første måling leste dekomponeringen 87 av 100 treningsrader slik tolkene leste dem, men bare 68 av 100 holdout-rader. Ordlistene var skrevet av Losen med treningsradene foran seg, og manglet det radene ikke hadde. Fire uavhengige tråder fikk derfor foreslå ord ut fra det de vet om språk. De fikk se emnene, stikkordklassene og menyen. De fikk ikke se en eneste setning fra korpuset.

| Fil | Innhold |
|---|---|
| `inn/REGLER-LEKS.md` | Reglene trådene fikk |
| `inn/emner-A.json`, `inn/emner-B.json` | Emnene (43 og 43) med ordformene grafen hadde, og de 14 allergenene. Én tråd per fil |
| `inn/stikk.json` | Stikkordklassene med forklaring og uttrykkene de hadde. To tråder fikk samme fil, hver for seg |
| `ut/emner-A.json`, `ut/emner-B.json`, `ut/stikk-1.json`, `ut/stikk-2.json` | Det trådene leverte, uendret |
| `tillegg-leks.json` | Det som ble tatt inn i datafilen, laget av `../prototype/flett_leks.py` |
| `tillegg-leks-logg.json` | Hvert forslag med hva som skjedde med det, og hvorfor |

## Hva som ble tatt inn, og hvordan

- **Emner og allergener:** det tråden kalte sikkert, minus det som alt sto, det regelen alt traff, og ord som også er stikkord. Ord på fire tegn eller færre treffer bare nøyaktig. Noen er tatt ut for hånd fordi de ikke er samme ting (listen `UTELATT` i skriptet).
- **Stikkord:** det begge trådene foreslo, det den ene foreslo og den andre var usikker på, og en kort liste Losen plukket fra den enes forslag (`HAANDPLUKKET` i skriptet). Noen er avvist for hånd fordi de like ofte betyr noe annet (`AVVIST`).
- **Kontroll mot treningsradene:** to forslag ødela en treningsrad hver og ble tatt ut («tar jeg» som ønske, «eplejuice» som eplemost). Ingen treningsrad ble dårligere av resten.
- **Tre rettelser i det som sto fra før**, som trådene pekte på: «kveite» er også en fisk og er byttet med «kveitemjøl» og «kveitemel»; «skaldjur» er skalldyr og er tatt ut av emnet sjømat; «fried» er videre enn fritert og er tatt ut.

Tallene: 750 forslag vurdert, 606 tatt inn (371 ordformer for emner, 57 for allergener, 102 stikkord, 10 nektelser og 66 ord i ordlistene). `tillegg-leks-logg.json` har hvert forslag for seg. Det trådene la under `usikre`, er ikke tatt inn, bortsett fra stikkord den andre tråden kalte sikre.

## Det trådene ikke gjorde

- To av trådene holdt ikke tidsgrensen på 8 minutter (8 min 41 s og 14 min 28 s). Den hardeste grensen er altså ikke hard.
- Ingen av filene var kjørt gjennom en JSON-leser av tråden selv. Alle fire lot seg lese.
- Forslagene er ikke lest av en uavhengig tråd etterpå. Kontrollen er den over, og målingen.
