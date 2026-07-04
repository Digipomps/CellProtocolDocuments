# Audit og ettervurdering

Analysert rapport: `Deliverables/Norwegian_Innovation_Policy_Measurable_Purpose_2026-06-23.md`  
Audit-output:

- `Tools/TextReliability/results/norwegian_innovation_policy_measurable_purpose_2026-06-23.analysis.json`
- `Tools/TextReliability/results/norwegian_innovation_policy_measurable_purpose_2026-06-23.report.md`

## Verktøy og datakilder

Den lokale `Tools/TextReliability/text_reliability.py`-flyten ble brukt som claim-ledger, Markdown-tabellparser, claim-klyngebygger, argumentgrafgenerator, kilde-audit-ledger og produktivitetsmodell. Verktøyet henter ikke eksterne kilder selv. Det markerer derfor eksterne URL-ankre som `needs_external_source_audit` og kildeløse claim som `source_missing`.

Det ble også forsøkt å finne en intern InnoRAG-/rådgiverflate. Lokal repo-kontekst viste en RAGGateway-konfigurasjon for `innovasjon` på `https://innorag.haven.digipomps.org`, men direkte query mot gatewayen returnerte `Invalid gateway secret`. Rapporten bygger derfor ikke på utilgjengelig InnoRAG-innhold. Den bygger på offisielle eksterne kilder og lokal tidligere policyanalyse som kontekst.

## Auditresultat

| Felt | Resultat | Vurdering |
| --- | ---: | --- |
| Claim-ledger | 122 claims | Akseptabelt for audit, men inkluderer også tabellrader og normative formuleringer. |
| Markdown-seksjoner | 13 | Strukturen er lesbar og egnet for videre review. |
| Markdown-tabeller | 6 | Tabellparseren fanger målarkitektur, indikatorer, modell og kildeclaim. |
| Claim-klynger | 11 | Klyngene følger seksjonsstrukturen og er nyttige for manuell adjudisering. |
| Argumentgraf | 11 noder, 10 kanter | God som oversiktskart; kantene er strukturelle, ikke dyp logisk inferens. |
| Kilde-audit-status | 39 `needs_external_source_audit`, 83 `source_missing` | Viktige kildeclaims er auditbare; mange normative/strategiske formuleringer er bevisst ikke kildecitert. |
| Produktivitetsmodell | Generert | 0,3 / 0,5 / 1,0 prosentpoeng gir ca. 134,5 / 226,2 / 462,7 mrd. kroner etter 10 år på 4 423 mrd. kroner. |
| Tester | 8/8 OK | Verktøyets testpakke passerte etter rapportkjøring. |

## Manuell kildeaudit

| Påstand | Status | Kildegrunnlag | Kommentar |
| --- | --- | --- | --- |
| Perspektivmeldingen peker på arbeidskraft, omstilling, fordeling og smartere oppgaveløsning. | Støttet | Regjeringen, Meld. St. 31 (2023-2024). | Sentral kilde for makroproblemet og velferdsmodellens bærekraft. |
| Langtidsplanen peker på konkurransekraft, innovasjonsevne, bærekraft, beredskap og kunnskap i bruk. | Støttet | Regjeringen, Meld. St. 5 (2022-2023). | Sentral kilde for kunnskap, absorpsjon og samfunnsoppdrag. |
| Næringslivets FoU skal mot 2 prosent av BNP innen 2030. | Støttet | Regjeringens FoU-strategi for næringslivet. | Offisielt mål, men fortsatt innsats-/kapasitetsmål. |
| Eksport utenom olje og gass skal øke 50 prosent innen 2030. | Støttet | Hele Norge eksporterer 2022-2024. | Offisielt mål; bør renses for valuta og pris i styringsmodell. |
| Digitalisering er et verktøy, ikke et mål i seg selv. | Støttet | Fremtidens digitale Norge. | Direkte relevant for å unngå virkemiddel som sluttmål. |
| Norge er sterk innovatør, men har svakere utslag på intellectual assets og salg fra nye produkter. | Støttet | European Innovation Scoreboard 2025, Norway profile. | God ekstern stresstest; ikke alene normativt beslutningsgrunnlag. |
| 0,3-0,5 prosentpoeng produktivitetsbidrag er egnet som referansepunkt. | Delvis støttet | Makrotall fra Nasjonalbudsjettet og Perspektivmeldingen; intervallet er analytisk. | Bør videreutvikles med SSB/FIN/OECD-baseline før formell beslutningsbruk. |

## Kvalitetsvurdering

Rapporten er egnet som faglig utgangspunkt. Den har en tydelig formålssetning, en målarkitektur som kan brukes på flere nivåer, en eksplisitt virkemiddeltest, et argumentkart og en kildeclaim-tabell. Den unngår den svakeste formen for innovasjonsretorikk: å behandle mer FoU, mer digitalisering, flere piloter eller flere bedrifter som mål i seg selv.

Den sterkeste delen er at formålet binder nasjonale interesser til målbare effekter: produktivitet, lønnsom eksport, offentlig tjenesteevne, beredskap og grønn omstilling. Den svakeste delen er den kvantitative produktivitetsmodellen. Den er riktig brukt som størrelsesorden, men den er ikke en empirisk kausalmodell.

## Forbedringer før tyngre bruk

1. Bygg et lite dataappendiks med SSB-serier for produktivitet, timeverk, Fastlands-BNP, offentlig ressursbruk og eksport utenom petroleum.
2. Del 0,3-0,5 prosentpoeng-målet i sektorbidrag: markedsrettet fastlandsøkonomi, offentlig sektor, energi/industri, helse, kommunal tjenesteyting og SMB-diffusjon.
3. Legg inn ansvarlig datakilde per indikator: SSB, Finansdepartementet, Innovasjon Norge, Forskningsrådet, Siva, Eksfin, DFØ, Digitaliseringsdirektoratet eller EU/EIS.
4. Gjør en egen kontradiksjonsrunde mot alternative formål: grønn omstilling, FoU-andel, eksport, gründerskap og regional utvikling.
5. Kjør en faktisk InnoRAG-fase når gateway-secret eller en autorisert rådgiverflate er tilgjengelig.
