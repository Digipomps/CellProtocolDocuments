# Porthole-paritet — Sicilia GUI, 2026-09-07

**Status: BLOKKERT / ikke visuelt akseptert.** Alle tre pålagte `npm run skeleton:iterate -- --mode preview`-kjøringer er forsøkt fra urørt `CellScaffold`, med desktop 1440×1000 og mobil 390×844. Ingen nettleserside ble åpnet, og ingen verifikasjons-PNG ble produsert. Originalbildene er inspisert, men det finnes ingen faktisk gjengivelse å sammenligne dem med side om side.

## Original og verifikasjon

| G1-GUI-original | Porthole desktop + mobil | Hva er kontrollert / hva mangler |
|---|---|---|
| [Gjesteliste](../gjest-sicilia-liste-v1.png) | Ingen skjermbilder — nettleserstart blokkert | JSON-test: «Fra Sicilia», forklaring, rekkefølgen title/lead/region, kortklasse, single/item_id og åpningsaction. Visuell gjengivelse, reell navigasjon og responsivitet er ikke verifisert. |
| [Artikkel](../gjest-sicilia-artikkel-v1.png) | Ingen skjermbilder — nettleserstart blokkert | JSON- og celletest: region, tittel, body, opphav, Divider, reaksjonstekst, tre riktige knapper, kommentarfelt og personvernløftet. Reaksjoner/kommentar har verifisert lagringseffekt gjennom cellehandlerne, men ikke gjennom Porthole-klikk. |
| [Husets tagger](../hus-artikkel-tagger-v1.png) | Ingen skjermbilder — nettleserstart blokkert | JSON- og celletest: artikkeloverskrift, forklaring, felter, Godkjenn tagger/Uten signal/Publiser, redigering og godkjenning av en konkret artikkel. Visuell radoppdatering og native/web-fokus er ikke verifisert. |
| [Tom gjesteflate](../gjest-sicilia-tom-v1.png) | Ingen skjermbilder — samme miljøblokkering | Fabrikktest og eksport fra kjørt celle: Sicilia-seksjonen utelates når publisert artikkelliste er tom. Omkringliggende eksisterende gjesteseksjoner er beholdt; full bildelikhet er ikke hevdet. |

Ingen farge-, font- eller avstandsparitet er vurdert. `styleClasses` er metadata. Fravær av synlig debug-/action-tekst kan heller ikke attesteres uten gjengitt flate.

## Faktiske blokkeringer

1. Lokal Palazzo-kilde på `127.0.0.1:18083`: `bind(descriptor:ptr:bytes:): Operation not permitted) (errno: 1)`, exit 133. Brukte isolert `CELL_VAULT_DOCUMENT_ROOT` i `/private/tmp`, ikke brukerens vanlige cellelager. [Serverlogg](../../../../../PalazzoScaffold/docs/sicilia-gui-evidence/g5-source-server.log).
2. Chromium i alle tre preview-forsøk: `bootstrap_check_in ... MachPortRendezvousServer ... Permission denied (1100)`, exit 1 før sideåpning. [Liste](../../../../../PalazzoScaffold/docs/sicilia-gui-evidence/g5-list-preview.log), [artikkel](../../../../../PalazzoScaffold/docs/sicilia-gui-evidence/g5-article-preview.log), [hus](../../../../../PalazzoScaffold/docs/sicilia-gui-evidence/g5-house-preview.log).
3. `http://127.0.0.1:18080` var den planlagte lokale Porthole-adressen; en fungerende Porthole-instans der ble ikke etablert. Ingen staging-instans ble brukt. Ingen commit-runtime ble kjørt.

Tillatelsesprofilen tillater ikke eskalering. Dette er miljøblokkeringer før produktet ble nådd, ikke bevis for en rendererfeil.

## Datagrunnlag og kjørbare inndata

[inputs](../../../../../PalazzoScaffold/docs/sicilia-gui-evidence/inputs/) inneholder konfigurasjoner/skeletons eksportert fra kjørte Palazzo-celler i XCTVapor, faktiske Explore-operasjoner, tomtilstand, artikkelrader og taggrader. Eksporttesten bruker original `content/artikler_v1.json`, med åtte artikler og eksplisitt godkjente tagger før gjesteeksport. Dette er ikke en seedet, nåbar TCP-server.

Fixturen mangler ingress. `lead` bindes til modellens eksisterende `subtitle`/`ingress`, og blir derfor tomt for denne fixturen. Ingressene i listebildet kan ikke dokumenteres som gjengitt med dette uendrede datagrunnlaget. Artikkelrekkefølgen i fixturen er heller ikke de tre utvalgte kortene i bildet. Disse innholdsforskjellene er åpne akseptansepunkter for en ny, faktisk visuell kjøring, ikke stilavvik.

Husbildet viser én forkortet eksempelrad; cellens eksisterende `dishTitle`/`dishDescription` leverer full artikkeltittel og tekst. Feltnavnene er beholdt som GUI-handoffet tillater. En visuell sammenligning av faktisk valgt seed/rad gjenstår.

## Beviste formattilpasninger

- Referanseetiketten kommer foran cellens faktiske keypath: `guest.guest.state.house.articles`, `guest.guest.article.open`, `entity.entity.article.react`, `content.content.draft.tags.*`. Testene normaliserer bare dette eksplisitte prefikset mot JSON-eksemplene og tester faktisk dispatch.
- Artikkeltekst hentes fra `article.guest.articles.<SHA256(articleID)>.{region,title,body,originLabel}`. Artikkel-ID-en er bundet i konfigurasjonen; det finnes ingen delt sist-lest-tilstand. Alle fire felt er lest gjennom de faktiske keypathene i testen.
- TextArea mangler payload. `entity.entity.article.comment.<SHA256(articleID)>` binder artikkelen og mottar tekst/`{text}`. Den videresender til `entity.article.comment` med `{articleID,text}`; lagrer én ordrett interaction med reaction=comment.
- `$id` i husknappene er erstattet av eksisterende rad-`payload`, slik handoffet krever. Publiser-knappen har eksplisitt tomt objektpayload slik at den sender SET.

## Explore-kontroll

App-audit: 101 komplette operasjonsregistreringer, 0 feil, 0 advarsler. Den rå skeleton-validatoren er **ikke grønn**: liste 21 feil/6 advarsler; hus 3 feil/2 advarsler; artikkel 0 feil/4 advarsler. [Rårapporter](../../../../../PalazzoScaffold/docs/sicilia-gui-evidence/).

Manuell triage: validatoren tolker List-radfelter som remote root-GET og knapper med rad-payload som GET. Listefunnene omfatter også eksisterende gjesteseksjoner og den svakt beskrevne `serviceModes`-foreldrekontrakten. Den nye artikkellisten har nå egen eksakt list-kontrakt. Artikkelens fire dynamiske lesefelt matches via `guest`-foreldrekontrakten. Validatoren teller ikke TextArea.submitActionKeypath eller List.selectionActionKeypath; disse er verifisert separat gjennom celletestene. Verken råvalidatoren eller testene erstatter Porthole-paritet.
