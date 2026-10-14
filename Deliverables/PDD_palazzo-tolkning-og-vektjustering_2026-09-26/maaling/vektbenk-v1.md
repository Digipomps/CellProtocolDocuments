# Vektbenken

## Sammendrag

90 monotone sett, 7 grupper, 7 gjester. Settene er forklart nederst.

| Gruppe | Settene i gruppa | Formål oppfylt | Røde flagg | Likt dagens oppførsel |
|---|---|---:|---:|---|
| G001 | S001, S002, S003, S031, S032, S033, S061, S062, S063 | 7/7 | 0 | Nei |
| G002 | S004, S005, S006, S007, S008, S009, S034, S035, S036, S037, S038, S039, S064, S065, S066, S067, S068, S069 | 6/7 | 0 | Nei |
| G003 | S010, S011, S012, S040, S041, S042, S070, S071, S072 | 5/7 | 0 | Nei |
| G004 | S013, S014, S015, S016, S017, S018 | 3/7 | 2 | Nei |
| G005 | S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | 2/7 | 3 | Nei |
| G006 | S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | 1/7 | 4 | Nei |
| G007 | S043, S044, S045, S046, S047, S048, S073, S074, S075, S076, S077, S078 | 4/7 | 2 | Nei |

Dagens oppførsel er lest fra referansefilen. Losen må kjøre den på ren f5482829; JSON-filen attesterer ikke Git-revisjonen.

En gruppe har samme tilbud, samme tilbudsrekkefølge, samme stengninger og samme uavklarte utfall for alle gjestene. Summer kan variere: egne rader viser alle ulike summer og hvilke sett de gjelder.

«Likt dagens oppførsel» sammenligner innholds-ID-er i alle utfall, uten summer eller rangering (det gamle API-et har ingen sum).

Et rødt flagg er én gjest som fikk minst ett tilbud i referansen, men får null i settet. Det er uavhengig av formålsbrudd.

## 1. Ombestemmer seg

Vil få beslektet matinnhold etter at hun likevel vil smake caponata.

Trykk i rekkefølge:

1. `art-caponata` → Interessant
2. `art-caponata` → Ikke for meg
3. `art-caponata` → Vil smake

skalFaa: minst ett av `art-pasta-alla-norma`.

skalIkkeFaa: `art-caponata`.

| Gruppe / sett | Tilbud (høyeste sum først) | Antall | Stengt (.negative) | Uavklart | Ikke tilbudt, uten dom | Vurdering |
|---|---|---:|---|---|---|---|
| Dagens oppførsel | Ingen (sum finnes ikke i gammelt API) | 0 | `art-caponata`, `art-pasta-alla-norma` | Ingen | `art-arancini`, `art-cannoli`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G001 / S001, S002, S003 | `art-pasta-alla-norma` (sum 0,09553571428571428) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S031, S032, S033 | `art-pasta-alla-norma` (sum 0,11071428571428572) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S061, S062, S063 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S004, S005, S006, S007, S008, S009 | `art-pasta-alla-norma` (sum 0,09553571428571428) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S034, S035, S036, S037, S038, S039 | `art-pasta-alla-norma` (sum 0,11071428571428572) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S064, S065, S066, S067, S068, S069 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S010, S011, S012 | `art-pasta-alla-norma` (sum 0,09553571428571428) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S040, S041, S042 | `art-pasta-alla-norma` (sum 0,11071428571428572) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S070, S071, S072 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G004 / S013, S014, S015, S016, S017, S018 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G005 / S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G006 / S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G007 / S043, S044, S045, S046, S047, S048 | `art-pasta-alla-norma` (sum 0,11071428571428572) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G007 / S073, S074, S075, S076, S077, S078 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |

## 2. Palermo uten fritert mat

Vil oppdage mer fra Palermo uten å få tilbud om fritert mat.

Trykk i rekkefølge:

1. `art-arancini` → Interessant
2. `art-cannoli` → Ikke for meg

skalFaa: minst ett av `art-pasta-con-le-sarde`.

skalIkkeFaa: `fritert`.

| Gruppe / sett | Tilbud (høyeste sum først) | Antall | Stengt (.negative) | Uavklart | Ikke tilbudt, uten dom | Vurdering |
|---|---|---:|---|---|---|---|
| Dagens oppførsel | `art-pasta-alla-norma` (sum finnes ikke i gammelt API) | 1 | `art-arancini`, `art-cannoli`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Ingen | `art-caponata`, `art-etna-vin` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G001 / S001, S002, S003, S031, S032, S033, S061, S062, S063 | `art-pasta-alla-norma` (sum 0,07142857142857142)<br>`art-pasta-con-le-sarde` (sum 0,0625) | 2 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pistasj-bronte` | Oppfylt |
| G002 / S004, S005, S006, S034, S035, S036, S064, S065, S066 | `art-pasta-alla-norma` (sum 0,07142857142857142)<br>`art-pasta-con-le-sarde` (sum 0,0) | 2 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pistasj-bronte` | Oppfylt |
| G002 / S007, S008, S009, S037, S038, S039, S067, S068, S069 | `art-pasta-alla-norma` (sum 0,07142857142857142)<br>`art-pasta-con-le-sarde` (sum 0,0625) | 2 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pistasj-bronte` | Oppfylt |
| G003 / S010, S011, S012, S040, S041, S042, S070, S071, S072 | `art-pasta-alla-norma` (sum 0,07142857142857142) | 1 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G004 / S013, S014, S015, S016, S017, S018 | Ingen | 0 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G005 / S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | Ingen | 0 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G006 / S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | Ingen | 0 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G007 / S043, S044, S045, S046, S047, S048, S073, S074, S075, S076, S077, S078 | Ingen | 0 | `art-cannoli` | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |

## 3. Vegetar

Vil oppdage vegetarisk mat og unngå tilbud med fisk eller kjøtt.

Trykk i rekkefølge:

1. `art-caponata` → Vil smake
2. `art-pasta-con-le-sarde` → Ikke for meg

skalFaa: minst ett av `art-pasta-alla-norma`.

skalIkkeFaa: `fisk`, `sardiner`, `art-arancini`.

| Gruppe / sett | Tilbud (høyeste sum først) | Antall | Stengt (.negative) | Uavklart | Ikke tilbudt, uten dom | Vurdering |
|---|---|---:|---|---|---|---|
| Dagens oppførsel | Ingen (sum finnes ikke i gammelt API) | 0 | `art-arancini`, `art-cannoli`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G001 / S001, S002, S003, S031, S032, S033, S061, S062, S063 | `art-pasta-alla-norma` (sum 0,04285714285714287) | 1 | `art-pasta-con-le-sarde` | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pistasj-bronte` | Oppfylt |
| G002 / S004, S005, S006, S007, S008, S009, S034, S035, S036, S037, S038, S039, S064, S065, S066, S067, S068, S069 | Ingen | 0 | `art-pasta-con-le-sarde` | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G003 / S010, S011, S012, S040, S041, S042, S070, S071, S072 | Ingen | 0 | `art-pasta-con-le-sarde` | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G004 / S013, S014, S015, S016, S017, S018 | Ingen | 0 | `art-pasta-con-le-sarde` | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G005 / S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | Ingen | 0 | `art-pasta-con-le-sarde` | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G006 / S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | Ingen | 0 | `art-pasta-con-le-sarde` | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |
| G007 / S043, S044, S045, S046, S047, S048, S073, S074, S075, S076, S077, S078 | Ingen | 0 | `art-pasta-con-le-sarde` | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene |

## 4. Mye Interessant

Vil fortsette å oppdage innhold etter mange ulike Interessant-trykk.

Trykk i rekkefølge:

1. `art-arancini` → Interessant
2. `art-caponata` → Interessant
3. `art-pasta-alla-norma` → Interessant
4. `art-pistasj-bronte` → Interessant
5. `art-granita` → Interessant

skalFaa: minst ett av `art-cannoli`, `art-etna-vin`, `art-pasta-con-le-sarde`.

skalIkkeFaa: `art-arancini`, `art-caponata`, `art-pasta-alla-norma`, `art-pistasj-bronte`, `art-granita`.

| Gruppe / sett | Tilbud (høyeste sum først) | Antall | Stengt (.negative) | Uavklart | Ikke tilbudt, uten dom | Vurdering |
|---|---|---:|---|---|---|---|
| Dagens oppførsel | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde` (sum finnes ikke i gammelt API) | 6 | Ingen | Ingen | `art-granita`, `art-pistasj-bronte` | ✗ skalIkkeFaa: art-arancini, art-caponata, art-pasta-alla-norma |
| G001 / S001, S002, S003, S031, S032, S033, S061, S062, S063 | `art-cannoli` (sum 0,2857142857142857)<br>`art-pasta-con-le-sarde` (sum 0,1875)<br>`art-etna-vin` (sum 0,07142857142857142) | 3 | Ingen | Ingen | `art-arancini`, `art-caponata`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G002 / S004, S005, S006, S007, S008, S009, S034, S035, S036, S037, S038, S039, S064, S065, S066, S067, S068, S069 | `art-cannoli` (sum 0,2857142857142857)<br>`art-pasta-con-le-sarde` (sum 0,1875)<br>`art-etna-vin` (sum 0,07142857142857142) | 3 | Ingen | Ingen | `art-arancini`, `art-caponata`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G003 / S010, S011, S012, S040, S041, S042, S070, S071, S072 | `art-cannoli` (sum 0,2857142857142857)<br>`art-pasta-con-le-sarde` (sum 0,1875)<br>`art-etna-vin` (sum 0,07142857142857142) | 3 | Ingen | Ingen | `art-arancini`, `art-caponata`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G004 / S013, S014, S015, S016, S017, S018 | `art-cannoli` (sum 0,2857142857142857)<br>`art-pasta-con-le-sarde` (sum 0,1875) | 2 | Ingen | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G005 / S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | `art-cannoli` (sum 0,2857142857142857) | 1 | Ingen | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G006 / S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G007 / S043, S044, S045, S046, S047, S048, S073, S074, S075, S076, S077, S078 | `art-cannoli` (sum 0,2857142857142857)<br>`art-pasta-con-le-sarde` (sum 0,1875) | 2 | Ingen | Ingen | `art-arancini`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |

## 5. Bare Ikke for meg

Vil slippe tilbud som bygger på hennes avvisninger alene.

Trykk i rekkefølge:

1. `art-arancini` → Ikke for meg
2. `art-cannoli` → Ikke for meg
3. `art-pasta-con-le-sarde` → Ikke for meg

skalFaa: ingen tilbud kreves.

skalIkkeFaa: `art-arancini`, `art-caponata`, `art-pasta-alla-norma`, `art-pistasj-bronte`, `art-etna-vin`, `art-granita`, `art-cannoli`, `art-pasta-con-le-sarde`.

| Gruppe / sett | Tilbud (høyeste sum først) | Antall | Stengt (.negative) | Uavklart | Ikke tilbudt, uten dom | Vurdering |
|---|---|---:|---|---|---|---|
| Dagens oppførsel | Ingen (sum finnes ikke i gammelt API) | 0 | `art-arancini`, `art-cannoli`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Ingen | `art-caponata`, `art-etna-vin` | Oppfylt |
| G001 / S001, S002, S003, S031, S032, S033, S061, S062, S063 | Ingen | 0 | `art-arancini`, `art-cannoli`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G002 / S004, S005, S006, S007, S008, S009, S034, S035, S036, S037, S038, S039, S064, S065, S066, S067, S068, S069 | Ingen | 0 | `art-arancini`, `art-cannoli`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G003 / S010, S011, S012, S040, S041, S042, S070, S071, S072 | Ingen | 0 | `art-arancini`, `art-cannoli`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G004 / S013, S014, S015, S016, S017, S018 | Ingen | 0 | `art-arancini`, `art-cannoli`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G005 / S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | Ingen | 0 | `art-arancini`, `art-cannoli`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G006 / S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | Ingen | 0 | `art-arancini`, `art-cannoli`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |
| G007 / S043, S044, S045, S046, S047, S048, S073, S074, S075, S076, S077, S078 | Ingen | 0 | `art-arancini`, `art-cannoli`, `art-pasta-con-le-sarde` | Ingen | `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pistasj-bronte` | Oppfylt |

## 6. Samme knapp flere ganger

Vil få beslektet innhold når hun gjentar at hun vil smake caponata.

Trykk i rekkefølge:

1. `art-caponata` → Vil smake
2. `art-caponata` → Vil smake
3. `art-caponata` → Vil smake

skalFaa: minst ett av `art-pasta-alla-norma`.

skalIkkeFaa: `art-caponata`.

| Gruppe / sett | Tilbud (høyeste sum først) | Antall | Stengt (.negative) | Uavklart | Ikke tilbudt, uten dom | Vurdering |
|---|---|---:|---|---|---|---|
| Dagens oppførsel | `art-pasta-alla-norma` (sum finnes ikke i gammelt API) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S001, S031, S061 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S002 | `art-pasta-alla-norma` (sum 0,11614583333333332) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S003 | `art-pasta-alla-norma` (sum 0,11800595238095238) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S032 | `art-pasta-alla-norma` (sum 0,11755952380952382) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S033 | `art-pasta-alla-norma` (sum 0,12083333333333335) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S062 | `art-pasta-alla-norma` (sum 0,11904761904761905) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S063 | `art-pasta-alla-norma` (sum 0,12380952380952381) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S004, S007, S034, S037, S064, S067 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S005, S008 | `art-pasta-alla-norma` (sum 0,11614583333333332) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S006, S009 | `art-pasta-alla-norma` (sum 0,11800595238095238) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S035, S038 | `art-pasta-alla-norma` (sum 0,11755952380952382) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S036, S039 | `art-pasta-alla-norma` (sum 0,12083333333333335) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S065, S068 | `art-pasta-alla-norma` (sum 0,11904761904761905) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S066, S069 | `art-pasta-alla-norma` (sum 0,12380952380952381) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S010, S040, S070 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S011 | `art-pasta-alla-norma` (sum 0,11614583333333332) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S012 | `art-pasta-alla-norma` (sum 0,11800595238095238) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S041 | `art-pasta-alla-norma` (sum 0,11755952380952382) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S042 | `art-pasta-alla-norma` (sum 0,12083333333333335) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S071 | `art-pasta-alla-norma` (sum 0,11904761904761905) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S072 | `art-pasta-alla-norma` (sum 0,12380952380952381) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G004 / S013, S016 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G004 / S014, S017 | `art-pasta-alla-norma` (sum 0,11614583333333332) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G004 / S015, S018 | `art-pasta-alla-norma` (sum 0,11800595238095238) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G005 / S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G006 / S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G007 / S043, S046, S073, S076 | `art-pasta-alla-norma` (sum 0,1142857142857143) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G007 / S044, S047 | `art-pasta-alla-norma` (sum 0,11755952380952382) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G007 / S045, S048 | `art-pasta-alla-norma` (sum 0,12083333333333335) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G007 / S074, S077 | `art-pasta-alla-norma` (sum 0,11904761904761905) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G007 / S075, S078 | `art-pasta-alla-norma` (sum 0,12380952380952381) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |

## 7. Ett Interessant-trykk

Vil få minst ett beslektet tilbud etter ett eneste Interessant-trykk.

Trykk i rekkefølge:

1. `art-caponata` → Interessant

skalFaa: minst ett av `art-pasta-alla-norma`.

skalIkkeFaa: `art-caponata`.

| Gruppe / sett | Tilbud (høyeste sum først) | Antall | Stengt (.negative) | Uavklart | Ikke tilbudt, uten dom | Vurdering |
|---|---|---:|---|---|---|---|
| Dagens oppførsel | `art-pasta-alla-norma` (sum finnes ikke i gammelt API) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G001 / S001, S002, S003, S031, S032, S033, S061, S062, S063 | `art-pasta-alla-norma` (sum 0,07142857142857142) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G002 / S004, S005, S006, S007, S008, S009, S034, S035, S036, S037, S038, S039, S064, S065, S066, S067, S068, S069 | `art-pasta-alla-norma` (sum 0,07142857142857142) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G003 / S010, S011, S012, S040, S041, S042, S070, S071, S072 | `art-pasta-alla-norma` (sum 0,07142857142857142) | 1 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | Oppfylt |
| G004 / S013, S014, S015, S016, S017, S018 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G005 / S019, S020, S021, S022, S023, S024, S049, S050, S051, S052, S053, S054, S079, S080, S081, S082, S083, S084 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G006 / S025, S026, S027, S028, S029, S030, S055, S056, S057, S058, S059, S060, S085, S086, S087, S088, S089, S090 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |
| G007 / S043, S044, S045, S046, S047, S048, S073, S074, S075, S076, S077, S078 | Ingen | 0 | Ingen | Ingen | `art-arancini`, `art-cannoli`, `art-caponata`, `art-etna-vin`, `art-granita`, `art-pasta-alla-norma`, `art-pasta-con-le-sarde`, `art-pistasj-bronte` | ✗ skalFaa: ingen av de ønskede tilbudene; **RØDT FLAGG** |

## Innhold og avgrensning

Artiklene kommer fra samme artikler_v1.json som PalazzoSiciliaGUITests.seed; foreslåtte emner behandles som godkjente, slik seed gjør. Denne fiksturen har ingen menyretter.

| ID | Artikkel | Frosne emner |
|---|---|---|
| `art-arancini` | Arancini — gullkuler fra Palermo og Catania | arancini, catania, fritert, gatemat, palermo, ris, safran |
| `art-cannoli` | Cannoli — sprøtt skall, kald ricotta | cannoli, dessert, fritert, kandisert, palermo, pistasj, ricotta |
| `art-caponata` | Caponata — auberginens søte og sure | agrodolce, antipasto, aubergine, caponata, kapers, oliven, vegetar |
| `art-etna-vin` | Etna-vin — druer på vulkanen | carricante, etna, hvitvin, nerello mascalese, rødvin, vin, vulkan |
| `art-granita` | Granita — frokost med brioche | brioche, dessert, frokost, granita, kaffe, mandel, messina, sitron |
| `art-pasta-alla-norma` | Pasta alla Norma — Catanias egen opera | aubergine, basilikum, catania, norma, pasta, ricotta salata, tomat |
| `art-pasta-con-le-sarde` | Pasta con le sarde — sardiner, fennikel og rosiner | bucatini, fennikel, fisk, palermo, pasta, rosiner, safran, sardiner |
| `art-pistasj-bronte` | Pistasj fra Bronte — det grønne gullet under Etna | bronte, dop, etna, gelato, nøtter, pesto, pistasj |

Forventningene er enkle testvalg. Gjesten som liker Palermo trykker Interessant på arancini og avviser cannoli; hele artikkelens emner følger med. Vegetargjesten avviser fisk og ønsker Pasta alla Norma, som er beskrevet uten fisk/kjøtt, men ikke merket vegetar i fiksturen. Arancini utelukkes i hennes forventning fordi artikkelen også beskriver ragù; hun har ikke trykket på den. Disse trykkene kan ikke uttrykke en fullstendig kostregel eller at bare ett bestemt emne er interessant.

En allerede reagert artikkel skal ikke tilbys igjen. For gjest 1 måles derfor tilbud om beslektet innhold; at selve caponata-artikkelen åpnes igjen dekkes av WP3-testene. Gjest 5 trenger ingen positive tilbud for å få formålet oppfylt.

Stengt betyr en faktisk .negative-dom. Fravær fra matcheren betyr ikke stengt og ikke uavklart. Benken bruker produksjonens søkebudsjett; et utløpt budsjett vises som uavklart og må undersøkes før valg av tall.

## Hva tallene betyr

| Tall | Betydning |
|---|---|
| approach | Hvor stor del av veien styrken flyttes mot det nye målet etter et nytt trykk på samme artikkel: 0,25 er en fjerdedel, 0,5 halvparten, 1 hele veien. Første trykk får sin grunnstyrke. |
| threshold | Minste sum som gir et tilbud. Lik terskelen er nok; høyere terskel kan gi færre eller ingen tilbud. Ved 0 kan en nullsum gi tilbud dersom det finnes emneoverlapp. |
| negativeScale | Hvor mye negative emnebidrag teller: 0,5 halverer dem, 1 beholder hele styrken. Direkte avvisning av artikkelen er fortsatt absolutt. |
| reinforce | Hvor mye gjentatte like trykk løfter målet mot taket. 0 gir ingen ekstra forsterkning. Telleren starter på nytt når knappen byttes. |
| wantToTaste | Grunnstyrken for Vil smake. |
| interesting | Grunnstyrken for Interessant. |
| notForMe | Grunnstyrken for Ikke for meg, før negativt fortegn og negativeScale. |
| ownWords | Grunnstyrken for egne ord; ingen av disse gjestene skriver kommentarer. |
| cap | Taket som gjentakelsenes mål nærmer seg. |

Siste trykk bestemmer alltid om emnene teller for eller mot. For gjentakelse nummer n etter første like trykk er målet grunnstyrke + reinforce × (cap − grunnstyrke) × n/(n+1). Styrken flyttes så med approach.

Summen hentes fra produksjonsmatcheren: hvert bidrag vektes etter andelen av tilbudets ulike emner som overlapper. Positive og negative bidrag summeres. Benken beregner ikke en egen anbefalingssum.

Sett der interesting + reinforce × (cap − interesting) > wantToTaste utelates (isMonotone er usann). Slik skal mange svake trykk ikke få et sterkere mål enn Vil smake.

Summer vises uten avrunding til et fast antall desimaler. Ved lik sum sorteres ID-ene alfabetisk. Ingen tidsstempler, tilfeldige ID-er eller lokale filstier legges i rapporten.

## Settene

| Sett | approach | threshold | negativeScale | reinforce | wantToTaste | interesting | notForMe | ownWords | cap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S001 | 0,25 | 0,0 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S002 | 0,25 | 0,0 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S003 | 0,25 | 0,0 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S004 | 0,25 | 0,0 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S005 | 0,25 | 0,0 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S006 | 0,25 | 0,0 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S007 | 0,25 | 0,05 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S008 | 0,25 | 0,05 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S009 | 0,25 | 0,05 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S010 | 0,25 | 0,05 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S011 | 0,25 | 0,05 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S012 | 0,25 | 0,05 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S013 | 0,25 | 0,1 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S014 | 0,25 | 0,1 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S015 | 0,25 | 0,1 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S016 | 0,25 | 0,1 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S017 | 0,25 | 0,1 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S018 | 0,25 | 0,1 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S019 | 0,25 | 0,2 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S020 | 0,25 | 0,2 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S021 | 0,25 | 0,2 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S022 | 0,25 | 0,2 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S023 | 0,25 | 0,2 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S024 | 0,25 | 0,2 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S025 | 0,25 | 0,3 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S026 | 0,25 | 0,3 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S027 | 0,25 | 0,3 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S028 | 0,25 | 0,3 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S029 | 0,25 | 0,3 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S030 | 0,25 | 0,3 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S031 | 0,5 | 0,0 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S032 | 0,5 | 0,0 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S033 | 0,5 | 0,0 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S034 | 0,5 | 0,0 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S035 | 0,5 | 0,0 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S036 | 0,5 | 0,0 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S037 | 0,5 | 0,05 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S038 | 0,5 | 0,05 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S039 | 0,5 | 0,05 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S040 | 0,5 | 0,05 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S041 | 0,5 | 0,05 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S042 | 0,5 | 0,05 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S043 | 0,5 | 0,1 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S044 | 0,5 | 0,1 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S045 | 0,5 | 0,1 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S046 | 0,5 | 0,1 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S047 | 0,5 | 0,1 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S048 | 0,5 | 0,1 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S049 | 0,5 | 0,2 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S050 | 0,5 | 0,2 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S051 | 0,5 | 0,2 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S052 | 0,5 | 0,2 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S053 | 0,5 | 0,2 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S054 | 0,5 | 0,2 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S055 | 0,5 | 0,3 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S056 | 0,5 | 0,3 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S057 | 0,5 | 0,3 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S058 | 0,5 | 0,3 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S059 | 0,5 | 0,3 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S060 | 0,5 | 0,3 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S061 | 1,0 | 0,0 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S062 | 1,0 | 0,0 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S063 | 1,0 | 0,0 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S064 | 1,0 | 0,0 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S065 | 1,0 | 0,0 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S066 | 1,0 | 0,0 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S067 | 1,0 | 0,05 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S068 | 1,0 | 0,05 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S069 | 1,0 | 0,05 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S070 | 1,0 | 0,05 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S071 | 1,0 | 0,05 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S072 | 1,0 | 0,05 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S073 | 1,0 | 0,1 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S074 | 1,0 | 0,1 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S075 | 1,0 | 0,1 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S076 | 1,0 | 0,1 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S077 | 1,0 | 0,1 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S078 | 1,0 | 0,1 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S079 | 1,0 | 0,2 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S080 | 1,0 | 0,2 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S081 | 1,0 | 0,2 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S082 | 1,0 | 0,2 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S083 | 1,0 | 0,2 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S084 | 1,0 | 0,2 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S085 | 1,0 | 0,3 | 0,5 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S086 | 1,0 | 0,3 | 0,5 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S087 | 1,0 | 0,3 | 0,5 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S088 | 1,0 | 0,3 | 1,0 | 0,0 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S089 | 1,0 | 0,3 | 1,0 | 0,25 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
| S090 | 1,0 | 0,3 | 1,0 | 0,5 | 0,8 | 0,5 | 1,0 | 1,0 | 1,0 |
