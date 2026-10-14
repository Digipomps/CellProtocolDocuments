# Ordlistetrådene, runde 2 (7. oktober 2026 kl. 11:05–11:28 UTC)

Stier er relative til denne mappen der ikke annet står.

Første måling på setninger fra seks nye skribenter ga 176 av 281 (`../rapport/MAALING-1-20261007.md`). Det som manglet mest, var talemål skrevet ned, svensk, engelske vendinger og chat-språk. Fem uavhengige tråder fikk derfor foreslå ord en gang til, med regler som ba om nettopp det. De fikk se emnene, stikkordklassene og menyen. De fikk ikke se en eneste setning fra korpuset.

| Fil | Innhold |
|---|---|
| `inn/REGLER-LEKS-2.md` | Reglene trådene fikk |
| `inn/OPPGAVE-EMNER-A.md`, `inn/OPPGAVE-EMNER-B.md`, `inn/OPPGAVE-STIKK-1.md`, `inn/OPPGAVE-STIKK-2.md`, `inn/OPPGAVE-STIKK-3.md` | Oppgaven hver tråd fikk |
| `inn/emner-A.json`, `inn/emner-B.json` | Emnene og allergenene med ordformene grafen hadde i versjon `.2`. Én tråd per fil. Laget med `../prototype/lag_leksinn.py` |
| `inn/stikk.json` | Stikkordklassene og ordlistene med forklaring og uttrykkene de hadde. Tre tråder fikk samme fil, hver for seg |
| `ut/emner-A.json`, `ut/emner-B.json`, `ut/stikk-1.json`, `ut/stikk-2.json`, `ut/stikk-3.json` | Det trådene leverte, uendret |
| `haand/avvist.json`, `haand/haandplukket.json`, `haand/utelatt.json`, `haand/LES-MEG.md` | Det som er avgjort for hånd, også det fra runde 1 |
| `tillegg-leks-2.json` | Det som ble tatt inn i datafilen, laget av `../prototype/flett_leks2.py` |
| `tillegg-leks-2-logg.json` | Hvert forslag med hva som skjedde med det, og hvorfor |
| `tillegg-egne-3.json` | Losens egne tillegg, gjort etter lesing av treningsradene i korpus 2 |

## Hva som ble tatt inn, og hvordan

- **Emner og allergener** (én tråd per fil): det tråden kalte sikkert, minus det som alt sto, det regelen alt traff, ord som også er stikkord, og ord som er et annet ord i grafen. Ord på fire tegn eller færre treffer bare nøyaktig.
- **Stikkord og ordlister** (tre tråder, samme innfil): det minst to tråder kalte sikkert; det én kalte sikkert og en annen var usikker på; og det én kalte sikkert når uttrykket har minst to ord eller minst seks tegn.
- **For hånd:** 36 forslag er avvist i denne runden fordi uttrykket like ofte betyr noe annet, eller ville slukt et emneord («til dessert» som høflighetsord tar ordet «dessert»). 48 er utelatt fordi de ikke er samme ting som emnet. Listene står i `haand/`.
- **Kontroll mot treningsradene:** nektelsene «shouldn t», «wouldn t» og «couldn t» gjorde en treningsrad feil og ble avvist. «først» som høflighetsord gjorde en treningsrad feil og ble avvist. Ingen treningsrad ble dårligere av resten.

Tallene, slik `../prototype/flett_leks2.py` skriver dem: 1115 forslag vurdert. Tatt med: 309 ordformer for emner, 23 ord for allergener, 270 stikkord, 16 nektelser og 212 ord i ordlistene. Resten: 60 sto alt, 102 traff alt, 48 utelatt for hånd, 36 avvist for hånd, 37 foreslått av bare én tråd og korte, 12 for korte til annet enn nøyaktig treff.

Datafilen `husgraf-20261007.3` bygges av disse tilleggene og seks navngitte rettelser i grunnlaget. Se `../../graf/ENDRINGSLOGG.md`.

## Slik gjøres det om igjen

Fra `../prototype/`, på en maskin som har HAVEN-roten (ellers med `HAVEN_ROOT` satt):

```
GRUNN=3 python3 lag_data.py /tmp/grunn3.json husgraf-proeve ../ordlister/tillegg-leks.json
python3 flett_leks2.py /tmp/grunn3.json /tmp/tillegg-leks-2.json
GRUNN=3 python3 lag_data.py /tmp/palazzo_husgraf.json husgraf-20261007.3 ../ordlister/tillegg-leks.json ../ordlister2/tillegg-leks-2.json ../ordlister2/tillegg-egne-3.json
python3 sammenlign2.py ../../graf/palazzo_husgraf-20261007.2.json /tmp/palazzo_husgraf.json
```

Den andre linjen skal gi en fil lik `tillegg-leks-2.json` (md5 `d88c4564d4dae1e838d069a641c95388`), og den tredje en fil lik `../../graf/palazzo_husgraf-20261007.3.json` (md5 `116d851f7e6db0cd4e671039b6a3483c`). Begge er prøvd slik 7. oktober 2026.

## Det som svekker runden

- **Tre av de fem trådene holdt ikke tidsgrensen på 8 minutter** (8 min 32 s, 10 min 5 s og 11 min 24 s). Grensen holdes ikke av verktøyet.
- **Reglene hadde tre eksempelfraser hentet fra treningsrader i korpus 2:** «har løst på», «I'm in the mood for» og «could go for». Det er treningsrader, så ingen avholdt rad er brukt. Men for de tre frasene var trådene ikke uavhengige av setningene.
- **Losens egne tillegg** (`tillegg-egne-3.json`) er gjort med treningsradene foran seg. De retter rader Losen har lest, og sier lite om rader ingen har lest.
- **Tallet etterpå er ikke et nytt usett tall.** De 84 uleste radene i korpus 2 er fra de samme seks skribentene som de 197 leste: 56 av 84 mot 54 før. Et nytt usett tall krever nye skribenter.
- Ingen av filene var kjørt gjennom en JSON-leser av tråden selv. Alle fem lot seg lese.
- Forslagene er ikke lest av en uavhengig tråd etterpå. Kontrollen er den over, og målingen.
