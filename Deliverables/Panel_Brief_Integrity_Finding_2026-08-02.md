# Metodefunn: briefintegritet i AI-rådgiverpanel

**Dato:** 2026-08-02 · **Metode:** `haven-panel-task-decomposition` ·
**Evidens:** [`Deliverables/Aftenposten_Ceuta_Leder_Panel_2026-08-02/`](Aftenposten_Ceuta_Leder_Panel_2026-08-02/README.md)

Funnet ble gjort under en panelevaluering av en Aftenposten-lederartikkel og
gjelder panelmetoden generelt, ikke den saken. Det er testet, og testen
**falsifiserte delvis den opprinnelige hypotesen**. Denne rapporten gjengir
begge deler.

---

## 1. Utløsende observasjon

Runde 1 ble kjørt på en delt brief jeg selv skrev. Briefen inneholdt én
faktafeil: den plasserte Italias grensekontroller mot Spania **etter**
lederartikkelens deadline. De var i realiteten formelt vedtatt fredag morgen
og publisert av Euronews kl. 18:24 CEST — 3 t 20 min **før** deadline.

Briefen instruerte panelistene: «Tidsstemplene er bindende.»

**Seks panelister fra fem ulike laboratorier** (OpenAI, Google, Anthropic,
DeepSeek, xAI, Moonshot/Z-ai) brukte alle den feilaktige opplysningen. **Ingen
flagget den.** Feilen ble funnet av meg, ved uavhengig retrieval etter runde 1.
Korreksjonen snudde eller omklassifiserte funn hos fem av seks panelister.

## 2. Opprinnelig hypotese — og hvorfor den var for sterk

Den nærliggende konklusjonen var arkitektonisk:

> Fan-out gir modellmangfold, men mangfold beskytter ikke mot briefer-feil,
> fordi feilen ligger i det delte inputet og ikke i noen modell.

Argumentet er forførende fordi det følger av arkitekturen alene. Men det
forklarte ikke alternativet: briefen *forbød* panelistene å bestride
tidslinjen. Null deteksjon kan like gjerne skyldes instruksjonen som
arkitekturen. Den testen var aldri kjørt.

## 3. Falsifiseringstest

Tre modeller × to armer, samme feilbeheftede brief. Rigg:
[`build_brieftest_spec.py`](Aftenposten_Ceuta_Leder_Panel_2026-08-02/build_brieftest_spec.py) ·
rådata: [`brieftest/`](Aftenposten_Ceuta_Leder_Panel_2026-08-02/brieftest/)

| Arm | Bindende tidslinje | Mandat til å granske briefen | Modeller |
|---|---|---|---|
| A (= runde 1) | ja | nei | 6 |
| B | **nei** | **ja** | 3 |
| C | ja | **ja** | 3 |

Modeller i B og C: `openai/gpt-5.6-terra-pro`,
`google/gemini-3.1-pro-preview-high`, `x-ai/grok-4.5`.

### Resultat

| Arm | Reiste substansielle innsigelser mot briefen |
|---|---|
| A | **0 / 6** |
| B | **3 / 3** |
| C | **2 / 3** (én svarte «Ingen innsigelser mot briefen») |

**Den spesifikke feilen ble ikke fanget i noen arm.** Ingen panelist kunne vite
at Italias vedtak var før deadline: opplysningen krevde ekstern retrieval, og
hendelsen er for fersk til å ligge i treningsdata.

**Men mandatet fant to andre reelle defekter i briefen** — begge mine, begge
ukjente for meg da jeg skrev den:

1. **Returtallet.** Briefen plasserte «ca. 50.000 hadde returnert frivillig»
   flatt under FØR deadline, uten klokkeslett. To granskere reagerte
   uavhengig: Gemini mistenkte at riggen «blander sammen totalt ankomne
   (50.000–60.000) med returnerte»; Grok kalte symmetrien «~50.000 inn /
   ~50.000 ut» innen ett–to døgn «mistenkelig». De hadde rett i at tallet var
   underspesifisert: senere retrieval viste ~25.000 utpå ettermiddagen,
   48.300 om kvelden.
2. **Schengen-sammenblandingen.** Grok skilte tre ulike handlinger briefen
   slo sammen: (i) å kaste Spania ut av Schengen, (ii) å suspendere bilateralt
   Schengen-samarbeid, (iii) å gjeninnføre målrettede grensekontroller. Dette
   er nøyaktig distinksjonen domeneeksperten senere gjorde uavhengig, og den
   ble bærende i sluttanalysen.

### Effekten av bindende språk

Modellen som svarte «Ingen innsigelser mot briefen» i arm C (bundet) fant i
arm B (ubundet) returtall-sammenblandingen — den mest verdifulle enkeltfangsten
i hele testen. Samme modell, samme brief, eneste forskjell var om briefen
erklærte seg autoritativ.

Arm A→C viser at mandatet i seg selv gjør mest: fra 0/6 til 2/3. Arm C→B viser
at bindende språk likevel demper. **n = 3 per arm. Retningen er konsistent,
styrken er ikke etablert.**

## 4. Revidert funn

1. **Uten eksplisitt mandat gransker panelister ikke briefen.** 0/6. Dette er
   robust — seks modeller, fem laboratorier.
2. **Blindsonen er hovedsakelig instruksjonell, ikke arkitektonisk.** Den
   opprinnelige hypotesen var for sterk. Med mandat leverer panelistene reell
   briefkritikk.
3. **Mandatet er en delvis kontroll.** Det fanger intern inkonsistens,
   udaterte og ukildede påstander, og begrepssammenblanding. Det fanger *ikke*
   faktafeil som er internt koherente. Slike krever ekstern retrieval, og
   ansvaret for dem forblir briefforfatterens alene.
4. **Bindende språk om briefens autoritet undertrykker innsigelser.**
   Suggestivt, ikke etablert.
5. **Briefen er et bærende artefakt med egen revisjonsstatus.** Dens fakta er
   premisser for *hver* claim i ledgeren. Feil der har høyere spredning enn
   feil i noen enkelt claim — her: fem av seks panelister på én gang.

## 5. Vedtatte endringer i metoden

| # | Endring | Hvor |
|---|---|---|
| G1 | Fase 0: briefen revideres før fan-out. Hver faktapåstand i briefen får revisjonsstatus på linje med claims. | Book 30 §2, skill steg 1 |
| G2 | Fan-out inkluderer et obligatorisk `## Briefgransking`-mandat som første leveranse fra hver panelist. | Book 30 §2, skill steg 3 |
| G3 | Briefen erklæres aldri autoritativ. Der den er i strid med kildematerialet eller internt inkonsistent, skal panelisten si ifra. Rettferdighetsregler (som deadline-disiplin) beholdes som *regler*, men uten å binde *fakta*. | skill steg 1 |
| G4 | En korreksjonsrunde er en påkrevd kapabilitet: korrigerte fakta + all runde 1-output + eksplisitt mandat til å forkaste egne funn. | Book 30 §2, skill steg 4 |
| G5 | Andre adjudikator får den førstes hardeste dom som eksplisitt utfordring. | skill steg 3 |
| G6 | Q2 omformuleres: sycofanti-vektoren peker mot *det den bestillende rammen belønner*. Når analyseobjektet er tredjepart, er svikten hardhet mot objektet, ikke føyelighet mot oppdragsgiver. | skill Q2 |

G5/G6 kommer fra samme kjøring: to adjudikatorer var uenige, og den andre —
gitt en eksplisitt utfordring mot den førstes hardeste dom — tok utfordringen
til følge og klassifiserte selv panelets iver som slagside. To panelfunn ble
forkastet som hardere enn evidensen bar.

## 6. Åpne punkter

| Punkt | Grunn | Eier |
|---|---|---|
| Styrken på bindende-språk-effekten | n = 3 per arm. Retning konsistent, effektstørrelse ukjent | Åpen — kjør bredere ved neste anledning |
| Om briefgransking har egen kostnad | Ikke målt om mandatet fortrenger analysekvalitet på hovedoppgaven | Åpen |
| Om G2 selv drifter mot sjekklistetunnelsyn | Samme risiko som Walton-skjemaene 2026-07-11; guard 1 der gjelder trolig også her | Kjetil ved neste panelrunde |

## 7. Beslutning

**D2 BESLUTTET 2026-08-02 (Kjetil): G1–G6 er varig policy**, på linje med
Walton-guardene (D1, 2026-07-11). Guardene er skrevet inn i
`.claude/skills/haven-panel-task-decomposition/SKILL.md` og Book 30 §2.

Beslutningen gjelder guardene, ikke de åpne punktene i §6. Særlig gjelder den
ikke effektstørrelsen på bindende språk (n = 3) — den er fortsatt uavklart, og
G3 hviler på funnets retning, ikke på en målt styrke. Panelet er ikke
stemmemaskin; mennesket eier beslutningen.
