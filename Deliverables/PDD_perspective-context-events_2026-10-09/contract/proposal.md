# G2-kontraktgrunnlag — implementert kandidat

Godkjent G2-grunnlag er bevart nedenfor. Endelig wire/surface/avgrensning er
avstemt i context-v1.json og CellProtocol/Docs/Perspective_Context_Events.md.
Felttyper og grenser er nå implementert og testet; se TESTRESULT.md.

## Kildeevent

Topic context.observation.changed, FlowElement med object-content:

```json
{"schemaVersion":1,"revision":12,"observedAt":"2026-10-09T05:00:00Z","validUntil":"2026-10-09T07:00:00Z","transition":"entered","labels":["morning"],"configurationRevision":3}
```

FlowElement.id er hendelsesidentitet. sourceID kommer fra Perspective sin konfigurerte abonnementsbinding; eventets egne felter gir ikke kildeautoritet. Labels beskriver hele gjeldende sett hos kilden. Tom liste er kjent fravær; manglende/utløpt snapshot er ukjent. Transition: snapshot, entered, left, configurationChanged. Presise felttyper, størrelsesgrenser og feilkvitteringer låses i W1 med fixtures. Revisjonen er varig og strengt stigende for endringer; snapshot-get returnerer siste event uendret, også transition. Dermed har snapshot og Flow med samme revisjon identisk innhold. Etter restart tillates fersk autorisert snapshot-get å bekrefte samme revisjon igjen; gjentatt Flow gjør ikke dette alene.

## Perspective-surface

Forslag: get perspective.context og perspective.context.configuration; set perspective.context.configure, perspective.context.sources.attach og perspective.context.sources.detach. Regel-evaluering kjøres på godkjente kildeeventer og utløp, ikke gjennom et offentlig uautorisert event-injeksjonspunkt. Regler navngir GoalDefinition med deklarerte kilder, mål-label, formålsreferanser, vekter, regelprioritet og filter-labels. Vinnende aktiv regel kan øke/senke vekt eller sette 0 (deaktivering); grunnvekten gjenopprettes når ingen regel gjelder. Høyeste prioritet vinner, med stabil regel-id som deterministisk likhetsregel. Ved regelendring evalueres allerede gyldig state på nytt.

Event perspective.context.changed viser effektiv kontekst, formålsbidrag, årsak og revisjon. Intern observasjon kan endres uten at effektivt aktivt formålssett endres; forskjellen må være eksplisitt i state/eventkontrakten. Ingen formålsmatch oppretter rettigheter.

## Filter-surface

Forslag: get filter.state og filter.configuration; set filter.configure. Eier angir Perspective-kilde, innholdskilder, grunnfilter og regler per kontekst-label. Tidligere leverte elementer fjernes ikke retrospektivt; filtervalget gjelder ny levering. Kontroll-eventer sendes ikke til innholdslisten. Snapshot/Flow samordnes ved oppstart. Ugyldig kontroll-data erstatter ikke siste gyldige policy; utløpt/manglende state bruker eksplisitt grunnfilter.

Samtidige aktive filterregler kombineres som snitt av tillatte elementer, alltid innenfor grunnfilteret. Ingen aktiv regel kan utvide grunnfilteret. Kontroll-/beslutningsstrømmen er separat fra innholdsfiltreringen, slik at kildeeventer ikke filtrerer bort sin egen mulighet til å endre policy.
