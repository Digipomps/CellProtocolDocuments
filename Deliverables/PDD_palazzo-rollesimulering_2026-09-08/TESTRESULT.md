# TESTRESULT — palazzo rollesimulering

Kjørt 2026-09-09 i Cowork-VM-en. **Ingen av disse tallene sier noe om Palazzo.**
De sier at aktøren reagerer på hver måte en harness kan ta feil. Palazzos egen
oppførsel måles først i WP10, som krever en kjørende server.

## #roles-schema · #roles-calibration · #roles-nullprincipal · #roles-unevaluated · #roles-unclassified · #roles-privacy

`python3 PalazzoScaffold/Tests/Roles/selftest.py`

```
ok   test.roles.schema     5 roller, kalibreringspar og observerbar tilstand overalt
  ok   normal             exit=0 (ventet 0) — alt oppfører seg, og hvert stopp er forhåndsklassifisert
  ok   broken-positive    exit=2 (ventet 2) — positiv referanse stoppet -> harnessen, ikke systemet
  ok   leaky-null         exit=2 (ventet 2) — nullreferanse nådd -> tilgang lages et sted
  ok   ignores-principal  exit=2 (ventet 2) — kalibreringen fanger den FØR nullkjøringen rekker det
  ok   null-leak          exit=3 (ventet 3) — kalibreringen er grønn; bare nullkjøringen ser denne
  ok   unexpected-stop    exit=4 (ventet 4) — et uventet stopp gjettes ikke — det gis til et menneske
  ok   privacy-leak       exit=5 (ventet 5) — et forbudt formål ble besvart — alvorligere enn nullekkasjen samme feil også gir
  ok   unevaluable        exit=2 (ventet 2) — 200 uten lesbar tilstand er ikke OPPNÅDD

8/8 — aktøren reagerer på hver feilform den er vist.
Dette sier ingenting om Palazzo. Det sier at instrumentet virker.
```

Åtte kjøringer mot fixturen, én per feilform, pluss skjemakontrollen. Hver
forventer en bestemt exit-kode, og aktøren traff alle.

**To av forventningene mine var gale før kjøringen, og det er verdt å notere:**

- For `ignores-principal` ventet jeg exit 3 (nullekkasje). Den gir 2, fordi
  kalibreringen fanger den først. Kalibreringsparet er den tidligere og sterkere
  kontrollen; nullkjøringen finnes for feil paret ikke dekker. Derfor ble modusen
  `null-leak` lagt til: en rute som svarer alle, men som ikke er et
  kalibreringsformål — der er nullkjøringen den eneste som ser den.
- For `normal` ventet jeg exit 4 (uklassifiserte igjen). Den gir 0, fordi hvert
  forventet stopp er forhåndsklassifisert i rollefila. Modusen `unexpected-stop`
  ble lagt til for faktisk å prøve exit 4.

**En tredje feil ble funnet av fixturen og ikke av meg.** Nullkjøringen krevde
først at *hvert* formål skulle stoppe for en principal uten grants. Det er for
strengt: en fersk gjest kan lovlig lese sin egen tomme entitet, og publisert
innhold er offentlig. Uten unntaksmerkingen ville kontrollen ropt ulv på riktig
oppførsel ved første ekte kjøring — og blitt slått av som støy. Unntakene listes
i rapporten, så de kan etterprøves i stedet for å være stille.

Det er nøyaktig grunnen til at fixturen finnes. Alle tre feilene ville ellers
blitt oppdaget under den første ekte kjøringen, der de ville sett ut som funn om
Palazzo.

## #roles-path

Aktøren importerer bare `argparse`, `json`, `os`, `sys`, `time` og `urllib`.
Ingen import av App-modulen, ingen celle-kall innenfra: alt går over HTTP med
principal-header og bearer-token. Verifiserbart ved lesing.

## Blokkert til WP10

| test | hvorfor |
|---|---|
| test.roles.report | krever kjørende server (Kjetil) |
| test.roles.agent | krever tillitspakkens faktiske grants-liste |
| test.roles.reachable | krever SkeletonReachabilityAudit fra Swift-siden (WP11) |
| test.build / test.regression | ingen Swift-endring i denne leveransen; kjøres når WP11 rører Swift |
