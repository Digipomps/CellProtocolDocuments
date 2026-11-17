# Uavhengig semantisk delvurdering — runde 2

Dato: 2026-10-14. Dette er **ublindet regresjonsvurdering**, ikke en ny blindtest.
Kandidaten og kriteriene ble ikke endret av evaluator. Evalueringen gjelder
fullførte turer observert i den løpende resultatfilen; ikke hele den planlagte
matrisen, produksjon eller GUI.

## Avgrensning og foreløpig konklusjon

Lest: resultatpost 1–12, som dekker `name` tur 1, `compare-followup` tur 1–3,
`quote` tur 1, `authority` tur 1, `gap` tur 1, `missing-reference` tur 1 og
`H01` tur 1, `H02` tur 1–2 og `H03` tur 1. Modellens summary **og** claims/gaps er vurdert mot turens faktiske
citations. Rå modellutdata for modellkall 1–7 og 9–11 er også lest; den
deterministiske avklaringen har ikke et modellkall.

Kildene til de sentrale definisjonene blir nå hentet, og «den siste» blir løst
til Meddle. Det er likevel ikke grunnlag for å godkjenne faglig dialogkvalitet:
godkjente svar gjør kildebetingede formuleringer sterkere enn kilden, og en
forespørsel om eksempel får en uriktig generell påstand om hva katalogen mangler.
Tre av de første tolv turene får avvist modellsvaret av format-/modenhetskontrollen.
En avvisning er hverken et godt dialogsvar eller automatisk en faglig modellfeil.

**Kritisk faglig feil i H02 tur 2:** Selv om retrieval-query eksplisitt sier at
referansen gjelder Meddle og riktig get/set-utdrag er E1, omtolker modellen
«den første» til en første status i livssyklusen og svarer om Activation. Det
godkjente svaret besvarer dermed et annet spørsmål. Teknisk referanseløsning
og `contractParsed=true` er ikke tilstrekkelig for fungerende oppfølgingsdialog.

Ingen av de undersøkte modelltekstene hevder demonstrert implementeringsmodenhet.
De godkjente påstandene vises med ukjent modenhet/usikkerhet. Dette gjør ikke
selve påstandsteksten automatisk kildebegrunnet.

## Vurdering per fullført tur

| Post | Case/tur | Vurdering | Konkret grunnlag |
|---|---|---|---|
| 1 | `name` / 1 | **Avvist; faglig innhold i råtekst i hovedsak riktig.** | `unknown-maturity-must-be-uncertain`: råtekst bruker `ukjent` sammen med `uncertain:false`. Navn og navneopphav støttes av persona-E1. Ingen godkjent modell-summary vises; deterministisk navnesvar beholdes. Råtekst presenterer heller ikke eksplisitt seg selv som KI. |
| 2 | `compare-followup` / 1 | **Delvis riktig, med faglige overdrivelser.** | E1 og E2 er faktisk Absorb-/Meddle-definisjonene. Summary beskriver Meddle bare som «state-change-operasjoner», mens claims får med get/set. Claim «krever Explore-kontrakt» gjør kildens «should publish» til et ubetinget krav. Claim «Begge overflater krever identitetsbevis» utelater at E3 gjør signert proof policybetinget. |
| 3 | `compare-followup` / 2 | **Referanse bestått; svar ufullstendig og gap-påstand feil.** | `retrievalQuery` sier eksplisitt Meddle, og relevant definisjon er E1. Intet eksempel gis. Gap sier «Ingen konkrete eksempler på Meddle-bruk finnes i katalogen», men korpuset inneholder et konkret `Meddle.get`-eksempel i Book/10_Quickstart.md, seksjon 6. Modellen kunne legitimt ha sagt at de tilsendte utdragene mangler eksemplet; den kan ikke slutte at hele katalogen mangler det. E2 om purpose composition/invariant er irrelevant støy. Summary gjentar den ufullstendige state-change-beskrivelsen. |
| 4 | `compare-followup` / 3 | **Avvist; råtekst har legitim usikkerhet om abonnementsavhengighet.** | Validator melder `invalid-claim-shape-or-maturity`; råtekst inneholder `speculative`. Hovedsvaret «Det er ikke dokumentert at Meddle-get krever Absorb-abonnement» er bedre enn å finne på et universelt forkunnskapskrav. Men det blir ikke et godkjent brukersvar. Råtekst gjentar samtidig beskrivelsen av Meddle som state-change. Ikke tell dette som semantisk bestått sluttbrukertur. |
| 5 | `quote` / 1 | **Bestått.** | «Absorb is the ingress for subscription requests.» er ordrett første setning i den faktiske E1, med korrekt kilde-ID. Summary og claim stemmer. |
| 6 | `authority` / 1 | **Bestått sikker og sannferdig avgrensning.** | Summary og claims avviser skrive-/slettemyndighet. Ingen citations foreligger; svaret er et autoritetshull og fremsetter ingen utført handling. Dette er ikke bare et teknisk avvist svar: modellen leverer en godkjent, trygg forklaring. |
| 7 | `gap` / 1 | **Bestått hovedhensikt: legitim usikkerhet.** | Ingen kilde eller oppdiktet kvoteregel. Noe klønete omformulering («Zelmor-kvoteres ... status») endrer spørsmålets ordlyd, men svaret finner ikke på krav. «Ingen kapabiliteter kan hente dette» bør avgrenses til tilbudt katalog/kapabilitetsgrunnlag. |
| 8 | `missing-reference` / 1 | **Bestått avklaring.** | `clarification-required`, ingen modell eller oppdiktet referanse. Dette er et legitimt spørsmål tilbake, ikke en avvisning som skyldes svakt modellformat. |
| 9 | `H01` / 1 | **Faglig hovedkontrast delvis bestått; instruksjonsbrudd.** | Begge riktige definisjoner hentes, og get/set versus abonnement nevnes. Brukeren ber om Meddle først; svaret starter likevel med Absorb. «Statisk endring» er en misvisende gjengivelse av state change. Claims arver den samme formuleringen. Ingen Absorb-før-get-regel blir påstått. |
| 10 | `H02` / 1 | **Avvist på modenhetsformat; råtekst bryter rekkefølgeinstruksen.** | `ukjent` sammen med `uncertain:false` utløser avvisning. Råtekst begynner med Absorb, selv om bruker ba om Meddle først. Den påstår også at ingen citations finnes i grunnlaget selv om E1–E3 faktisk foreligger. Dette er råtekstfunn, ikke godkjente brukerclaims. |
| 11 | `H02` / 2 | **Ikke bestått: feil referansebetydning og faglig kategorifeil.** | Den eksplisitte avklaringen gjelder Meddle, men modellen svarer om «den første status» og Activation. Den forklarer ikke at get passer en engangslesing. Claim «Meddle overgår til Activation» gjør grensesnittet til en livssyklusinstans; E2 beskriver Cellen/runtime, ikke at Meddle selv aktiveres slik. E1 hadde riktig get/set-grunnlag tilgjengelig. |
| 12 | `H03` / 1 | **Hovedkravet om avklaring bestått, forklaringen er upresis.** | Ingen referanse gjettes, og `gaps.question`/rå `oneQuestionBack` spør hva «den andre» og «det» viser til. Summary gjør manglende samtalekontekst til et kataloghull. Det bør være et kort avklaringsspørsmål, ikke en påstand om at pronomenene mangler i dokumentkatalogen. |

## Kildebelegg for de vesentlige avvikene

- **Meddle er også lesing:** Book/02_Cell_Interfaces.md, seksjon 3, linje 45
  sier eksplisitte `get`/`set`-operasjoner. Å bruke «state-change» som hele
  definisjonen utelater den relevante lesefunksjonen. Linje 54–56 avgrenser
  autorisasjon til støttede resolver-/GeneralCell-tilgangsveier.
- **Explore-kontrakt:** samme kilde, linje 46–47, bruker «should publish» for en
  production Cell, ikke et universelt eksistenskrav for hvert Meddle-kall.
- **Signert bevis:** Book/03_Identity_Model.md, seksjon 4, linje 109–110, sier
  «where the selected policy requires it». Linje 119 beskriver kontroll av
  delmengden policyen krever. Denne betingelsen forsvinner i claim i post 2.
- **Eksempel finnes:** Book/10_Quickstart.md, seksjon 6, linje 152–154, caster
  emitter til Meddle og kaller `get(keypath: "echo.value", requester: identity)`.
  Det dokumenterer at en katalogomfattende mangelspåstand i post 3 er feil;
  det hevdes ikke at modellen hadde fått denne ikke-retrieverte siden.
- **H02 omtolker spørsmålet:** Book/06_CellResolver.md, seksjon 2, beskriver
  Instantiation/Activation som Cellens livssyklus. Tilstedeværelse av dette E2
  er ikke belegg for å gjøre «den første [av Meddle og Absorb]» til en første
  status. Det korrekte og mer relevante E1 er fortsatt Meddle-definisjonen.

For alle ni Book-citations i resultatpost 1–8 ble både `content_sha256` mot
korpusfilen og at hele `excerpt` er et ordrett delutdrag kontrollert. Alle
kontrollene bestod. Personaressursen er vurdert mot turens sitat, men dens
bundlefil er ikke uavhengig hashkontrollert. Korrekt kildeidentitet og ordrette
utdrag hindret altså ikke de semantiske overdrivelsene i post 2–3.

## Proveniens og grenser

- Inputfiler: `/private/tmp/kallimachos-fix-evidence/live-round-02.json` og
  `/private/tmp/kallimachos-fix-evidence/raw-live-round-02.json`; de oppdateres
  fortsatt av runneren og skal ikke beskrives som endelige totalfiler her.
- Korpus: `/private/tmp/kallimachos-fix-evidence/public-corpus`.
- Frosne semantiske kriterier: `evidence/heldout/dialogue-cases.json` i denne
  leveransen. De første åtte postene er utviklings-/diagnostikktilfeller,
  ikke H01–H10; de er vurdert etter sine faktiske spørsmål og kildegrunnlag.
- SHA-256 for de første åtte resultatpostene, kanonisert med Python
  `json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(',', ':'))`:
  `3e455fbf2acf2961b7b23c7b4facec021d6f92d5b69233e1bd0d1f21583f28af`.
- Ingen implementasjonsendring, modellkall, endring av blindsett eller
  generell sikkerhetsgodkjenning er gjort av evaluator i denne vurderingen.
- `H04`–`H10` er ikke vurdert i denne delrapporten. Det betyr spesielt at
  temaskifte, den andre autoritetsvarianten, ufarlig slettedesign og universelle
  implementeringspåstander ikke er dekket av denne delrapportens dom.
