# Codex-handoff: Ny forside for digipomps.org — «uroen først, alternativet under bygging»

Dato: 2026-08-03. Skrevet av Claude etter gjennomgang med Kjetil.
Repo: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Website`

## 1. Objective

Bygg en ny versjon av forsiden (og støttende endringer i `kilder/` + én ny artikkel) som:

1. **Starter med uroen folk faktisk kjenner** når de må bruke de store tech-tjenestene — i veldig enkelt språk, uten fagord.
2. **Ikke bruker ordet «agent» i åpningen.** Ordet introduseres først i kontrollsløyfe-seksjonen eller senere, og da forklart («tjenester som handler for deg»).
3. Posisjonerer HAVEN som **alternativet under bygging**: et åpent økosystem, ikke ett produkt — med ærlig modenhetsstatus beholdt.
4. Introduserer **mulighets-/produktivitetsargumentet** som en begrunnet hypotese: et økosystem med tydelige avtaler kan bli mer produktivt enn dagens plattformøkonomi, fordi dagens økosystem sløser enorme mengder menneskelig tid og tillit.
5. Fletter inn — **subtilt** — at tydelige formål, avgrenset myndighet og kvitteringer er en samarbeidsgrammatikk som er god for *begge* sider: mennesker og de stadig mer kapable verktøyene som arbeider for dem. Harmoni, ikke frykt. Se §6.

Målet på suksess (fra tidligere analyse): en fremmed leser skal etter forsidens to første seksjoner kunne svare på «hva er galt i dag, for hvem, og hva bygger HAVEN i stedet» — uten å klikke videre.

## 2. Current state (les før du endrer noe)

- **Produksjon** `https://digipomps.org` kjører release `20260801T095935Z` (16 artikler, «Mennesket først»-hero). Skal IKKE endres i denne oppgaven.
- **Review-host** `https://new.haven.digipomps.org` kjører `20260803T162639Z` — arbeidskopien i dette repoet (17 artikler, «digital uavhengighet»-hero, femtrinns kontrollsløyfe, «mennesket først – ikke mennesket alene»). **Bygg videre på arbeidskopien, ikke på produksjonsvarianten.**
- `DEPLOYMENT_STATUS.md` har sjekksummer og verifikasjonshistorikk. Oppdater den ved deploy til review.
- **App-entry-blokken i `index.html` (mellom `HAVEN_APP_ENTRY_START`/`HAVEN_APP_ENTRY_END`) er `blocked` og fail-closed.** Ikke rør kontrakten. Release-guarden `python3 Website/tools/verify_app_entry.py` + `python3 -m unittest Website/tests/test_verify_app_entry.py` må fortsatt passere. Hero-en kan omskrives tekstlig, men skal fortsatt ha nøyaktig to ordinære lenker i blokken.
- Ingen analytics, ingen tredjeparts-assets, ingen JS-avhengighet for kjernereisen. Behold dette.
- Claim-kanon: `/Users/kjetil/Build/Digipomps/HAVEN/DiMyDocuments/ValueRedistribution/01_TERMINOLOGY_AND_CLAIMS_CANON.md` og modenhetsmatrisen i `05_ASSURANCE_MATURITY_MATRIX.md`. **Offentlig tekst kan aldri hevde høyere modenhet enn matrisen.**

## 3. Claim-sikkerhet for den nye vinklingen (avklart, følg dette)

Kjetils ønskede budskap, klassifisert og omskrevet til trygg form:

| Ønsket budskap | Klassifisering | Trygg formulering (bruk denne retningen) |
|---|---|---|
| «HAVEN er svaret på usikkerheten mange føler ved big tech-tjenester» | Overclaim som deklarativ («er svaret») | «HAVEN bygges for dem som kjenner denne uroen» / «et svar under bygging». Uroen dokumenteres med eksterne kilder (§4); HAVENs bidrag beskrives som designmål + det som faktisk er testet. |
| «HAVEN er alternativet» | Overclaim (det finnes ikke et brukbart produkt ennå) | «HAVEN bygges som et alternativ: et åpent økosystem der …». «Alternativ» er OK som *retning og identitet*, ikke som tilgjengelighetspåstand. |
| «Økosystemet har potensiale til å bli mer produktivt enn dagens corporate-styrte internett» | Aspirasjonell; krever begrunnelse + hypotese-merking | Formuler som begrunnet hypotese: dagens økosystem har målbare kostnader (samtykketeater, siloer, innlåsing — kilder i §4); et økosystem med forståelige avtaler *kan* frigjøre samarbeid som i dag er for risikabelt. Merk «Retning/hypotese» som på demokratiseksjonen. |

Tonekrav: **ikke navngi selskaper, ikke polemikk.** Beskriv strukturer («dagens plattformøkonomi», «tjenester der du er produktet»), ikke fiender. Stiftelsen er politisk uavhengig og siden skal tåle å leses av folk som jobber i de samme selskapene. Forbudte claims fra kanon gjelder fortsatt (ingen «løser ulikhet», ingen «global reputation» som feature, osv.).

## 4. Research: reelle bekymringer, med kilder (legg de brukte inn i `kilder/`)

Dette er dokumentasjonen som gjør at forsiden kan åpne med uro uten å overdrive. Eksterne kilder støtter *problemforståelsen* — ikke at HAVEN virker (eksisterende regel på kilder-siden).

**Kontrolltap og avmakt (norsk — bruk denne først):**
- Datatilsynets Personvernundersøkelse 2024: To av tre nordmenn opplever liten kontroll og avmakt over flyten av egne personopplysninger på nett; bare 29 % opplever kontroll; halvparten opplever ubehag ved tanken på hvor mye som ligger der ute.
  - https://www.datatilsynet.no/regelverk-og-verktoy/rapporter-og-utredninger/personvernundersokelser/personvernundersokelsen-2024/
  - PDF: https://www.datatilsynet.no/contentassets/8621a6059d314f478ef93da07f935cad/personvernundersokelsen-2024.pdf
- Samme undersøkelse — **nedkjølingseffekten** (dette er produktivitetsargumentets faktagrunnlag på individnivå): over halvparten har latt være å bruke en tjeneste pga. usikkerhet om databruk; 74 % har latt være å laste ned en app av samme grunn. Uro er ikke bare en følelse — den stopper faktisk bruk og verdiskaping.
- Nordmenn har høy tillit til offentlige institusjoner og svært lav tillit til selskapene bak sosiale medier, søk og meldingstjenester (samme kilde). Dette begrunner hvorfor et *stiftelsesforvaltet* alternativ er relevant.

**Internasjonal bekreftelse:**
- Pew Research (2023): 73 % av amerikanere føler liten eller ingen kontroll over data selskaper samler om dem. https://www.pewresearch.org/internet/2023/10/18/views-of-data-privacy-risks-personal-data-and-digital-privacy-laws/
- Pew (2025): 51 % er mer bekymret enn begeistret for økt AI i hverdagen; flertallet ønsker mer kontroll over hvordan AI brukes i livene deres. https://www.pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts-view-artificial-intelligence/ og https://www.pewresearch.org/science/2025/09/17/how-americans-view-ai-and-its-impact-on-people-and-society/

**Samtykketeaterets kostnad (produktivitetsargumentets faktagrunnlag på systemnivå):**
- Carnegie Mellon-estimat: å faktisk lese alle personvernerklæringer man møter ville koste ~76 arbeidsdager per person per år. (Referert bl.a. i https://uxmag.com/articles/consent-fatigue-are-we-designing-people-into-compliance)
- Brukere ser på et cookie-banner i ~4–7 sekunder før de klikker (MIT-studie 2022, samme oversikt); «informert samtykke» er i praksis en fiksjon i dagens modell.
- Europeere bruker samlet ~575 millioner timer i året på cookie-bannere. https://www.legiscope.com/blog/hidden-productivity-drain-cookie-banners.html
- ~72 % av undersøkte cookie-bannere inneholder minst ett dark pattern som dytter mot aksept (samme forskningsoversikt).

**Avhengighet/suverenitet (bakteppe, bruk varsomt):**
- EU er avhengig av ikke-europeiske leverandører for over 80 % av digitale produkter, tjenester og infrastruktur (digital suverenitet-rapporter, f.eks. https://www.france24.com/en/europe/20260124-europe-s-digital-reliance-on-us-big-tech-does-the-eu-have-a-plan og https://www.idc.com/resource-center/blog/digital-sovereignty-in-europe-in-2025-whats-plan-b/). Verifiser tallet mot primærkilde (Europakommisjonen) før publisering; ellers utelat prosenten og behold det kvalitative poenget.

Krav: hver statistikk som brukes på forsiden skal (a) ha kilde på `kilder/`-siden med lenke, (b) være datert, (c) formuleres nøkternt («to av tre nordmenn oppgir …», ikke «alle vet at …»).

## 5. Ny fortellingsbue for forsiden (seksjon for seksjon)

Behold det som virker i review-varianten (modenhetsgrense, kontrollsløyfe, «ikke mennesket alene», tre veier inn, status, organisasjon, åpen arbeidsregel). Endringen er **rekkefølge og inngang**. Foreslått bue:

### 5.1 Hero — uroen, gjenkjennelig og enkel
Krav: ingen fagord, ikke ordet «agent», ikke «protokoll», ikke «Cells», ikke «myndighet» i første avsnitt. Setninger under ~15 ord. Utkast (Codex kan forbedre språket, ikke claim-nivået):

> **Hva sa du egentlig ja til?**
>
> Mange av oss kjenner en uro når vi bruker de store digitale tjenestene.
> Hva vet de om meg? Hvor havner det jeg deler? Og hva godtok jeg i farten?
>
> Den uroen er ikke innbilt. To av tre nordmenn opplever at de har liten kontroll over egne opplysninger på nett.*
>
> HAVEN bygges som et alternativ: et åpent økosystem der en tjeneste må si hva den skal gjøre, bare får det den trenger — og viser etterpå hva som faktisk skjedde.
>
> [Forstå HAVEN] [Se et tidlig testbevis]
>
> *Datatilsynets personvernundersøkelse 2024 → kilder

Modenhetsgrensen (datert boks) beholdes rett under, som i dag. App-entry-kontrakten: de to lenkene over er blokkens to ordinære lenker.

### 5.2 «Kjenner du deg igjen?» — problemseksjon (NY)
Tre–fire korte kort som gjør uroen konkret, hver med nøktern statistikk + kildelenke:
1. **Du må si ja for å delta.** Å lese alt du godtar ville kostet ~76 arbeidsdager i året. Så ingen gjør det — og det vet designerne.
2. **Du gir mer enn oppgaven trenger.** Én app, én knapp, alt eller ingenting. Etterpå er det vanskelig å se hvem som fikk hva.
3. **Uroen stopper deg.** 74 % har droppet en app fordi de var usikre på hva som skjedde med opplysningene. Usikkerhet koster deltakelse — for deg og for samfunnet.
Avslutt seksjonen med broen: «Dette er ikke en naturlov. Det er en designbeslutning. HAVEN undersøker en annen.»

### 5.3 «Hva HAVEN bygger» — alternativet (omarbeidet fra dagens hero-stoff)
Enkel forklaring av økosystem-ideen: ikke én app, ikke én plattform, men mange små deler som samarbeider etter felles regler: si formålet, be om minst mulig, gi kvittering, la deg trekke tilbake. Her kan «tjenester — også de som handler for deg» introduseres; ordet «agent» først her eller i 5.4. Lenk «HAVEN på ett minutt».

### 5.4 Kontrollsløyfen (beholdes som i review-varianten)
Femtrinnssløyfen fungerer. Én justering: trinn-tekstene kan forenkles språklig (kortere setninger), og «agent» forklares første gang den brukes.

### 5.5 «Hva blir mulig?» — muligheter og produktivitet (NY, merket Retning/hypotese)
Dette er den nye ambisjonsseksjonen. Struktur:
- **Premiss (dokumentert):** dagens modell sløser tid (samtykketeater), stopper bruk (nedkjølingseffekt) og låser verdier inne i siloer.
- **Hypotese (merket):** når en avtale er forståelig og avgrenset, blir det trygt å si ja oftere. Da kan folk dele, samarbeide og bygge videre på hverandres arbeid uten å gi fra seg alt. *Vi undersøker om* et slikt økosystem kan bli mer produktivt enn dagens — det må måles i avgrensede piloter, ikke hevdes.
- Tre konkrete mulighetsbilder (korte, «tenk deg»-form): dele én opplysning til ett formål uten å miste den; la noen hjelpe deg uten å gi dem alt; bidra til et fellesprosjekt og kunne vise nøyaktig hva du bidro med. Lenk eksisterende artikler `produktivitet-uten-personscore` og `bidrag-og-verdi`.
- Samme visuelle hypotese-merking som demokratiseksjonen har i dag. Ingen påstander om ulikhet, penger eller ferdige fordelingsmekanismer (kanon).

### 5.6 Resten av buen beholdes
«Ikke mennesket alene» (kan strammes), tre veier inn, demokrati-hypotesen, utgangspunktet («Alle mennesker er like mye verdt» — behold, men den skal ikke lenger bære åpningen alene), tillit uten poengsum, artikler, status, organisasjon, åpen arbeidsregel, kontakt-CTA.

## 6. Det subtile harmoni-elementet (mennesker og maskiner)

Kjetil ønsker en håndsutrekning: hvordan mennesker og stadig mer kapable maskiner kan leve godt sammen. **Subtilitet er et krav** — ingen «AI-rettigheter», ingen sci-fi, ingen store ord. Virkemiddelet er å vise at HAVENs grammatikk er *gjensidig*:

1. **Én setning i seksjon 5.3 eller 5.4**, omtrent: «Tydelige avtaler er gode for begge sider av et samarbeid. Et verktøy som vet nøyaktig hva det har fått lov til, kan arbeide friere innenfor grensen — og fortjene mer tillit neste gang.» (Merk: dette er en designpåstand om forutsigbarhet, ikke en effektpåstand — trygg.)
2. **Én ny kort artikkel** (samme mal som de andre, kategori «Retning»): arbeidstittel `artikler/verktoy-som-samarbeider/` — «Verktøy som samarbeider». Tema: frykt oppstår der ingen vet hva den andre kan finne på; forutsigbarhet er tillitens råstoff begge veier. En tjeneste (eller en KI) med synlig formål og avgrenset myndighet er ikke lenket — den har fått en forståelig rolle, slik gode kolleger har. HAVEN undersøker om den samme grammatikken som beskytter mennesker også gjør samarbeid med maskiner roligere og mer fruktbart. Avslutt med standard «Grensen»-boks: dette er en designretning, ikke en dokumentert effekt.
3. **Ikke mer enn dette.** Ingen hero-plass, ingen egen forside-seksjon.

## 7. Constraints og non-goals

- Norsk først; behold eksisterende engelske metadata-praksis.
- Ikke rør: app-entry-guard-kontrakten, personvern-/rettelses-/om-sidene (utover ev. kildelenker), robots/sitemap-mønsteret, no-analytics, logo.
- Ingen nye rammeverk/avhengigheter; fortsatt statisk HTML/CSS + eksisterende `site.js`-omfang.
- Tilgjengelighet skal bestå: JS av/på, tastaturfokus, 200 % tekst, 390 px uten horisontal scroll.
- Alle daterte statuspåstander oppdateres til faktisk dato ved endring; endringer i offentlige påstander føres i `rettelser/`.
- **Deploy kun til review-hosten** (`/var/www/haven-public-review`-flyten). Produksjon byttes ikke uten Kjetils eksplisitte godkjenning av review-varianten.
- Ordet «agent» skal ikke forekomme før seksjon 5.3/5.4 i forsidens DOM-rekkefølge.

## 8. Verifikasjon som forventes før du melder ferdig

1. `python3 Website/tools/verify_app_entry.py` og `python3 -m unittest Website/tests/test_verify_app_entry.py` — grønt.
2. `node Website/tests/app_entry_browser_smoke.js http://127.0.0.1:4173` mot lokal preview — grønt.
3. Tekst-reliabilitetsverktøyet i repoet (se README «Content and claim maintenance») etter substansielle tekstendringer.
4. Manuell claim-sjekk mot §3-tabellen og kanon-dokumentet: grep forsiden for «er svaret», «løser», «garanterer», «alternativet er klart»-formuleringer.
5. Kildesjekk: hver statistikk på forsiden har en rad på `kilder/` med lenke og dato. 80 %-EU-tallet enten primærkildebelagt eller fjernet.
6. Lesbarhetssjekk av hero + problemseksjon: ingen fagord, «agent» fraværende, setningslengde-målet holdt.
7. Oppdater `DEPLOYMENT_STATUS.md` med ny review-release og sjekksummer ved deploy.

## 9. Åpne spørsmål til Kjetil (ikke blokkér — velg default og noter valget)

1. Skal statistikken stå i selve hero-en (utkastet i 5.1) eller først i problemseksjonen? Default: i hero, som én setning med fotnote-lenke.
2. Navn på den nye artikkelen i §6 («Verktøy som samarbeider» er arbeidstittel). Default: behold arbeidstittelen.
3. Skal «Kjenner du deg igjen?»-seksjonen ha illustrasjon i samme kollasj-stil som eksisterende assets? Default: gjenbruk stil, generer ett nytt bilde kun hvis det ikke forsinker.
4. Beholdes «digital uavhengighet»-begrepet som hero-tittelnivå, eller erstattes det helt av uro-inngangen? Default: uro-inngangen vinner hero-en; «digital uavhengighet» lever videre som prinsippartikkel og i 5.3.
