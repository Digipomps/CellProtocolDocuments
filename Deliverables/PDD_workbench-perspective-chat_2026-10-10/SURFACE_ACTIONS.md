# Hvor handlingene hører hjemme

2026-10-10. **Vurdering og forventningskontrakt, ikke implementerte knapper.** Kildeinventaret er avgrenset som SOURCE_AUDIT.md beskriver. Designet gjenbruker handlingene fra cellenes Explore-kontrakt; hvert valg må både være implementert og autorisert. En knapp som mangler utfører vises som utilgjengelig med presis grunn, ikke som vellykket køing.

| Flate / objekt | Naturlige handlinger | Forventet kilde til effekt / hendelse | Krav før utføring |
|---|---|---|---|
| Idé / Inbox | Utforsk, gjør til oppgave, knytt til formål, legg oppgaven i kø | WorkItem capture/addRelation og autorisert AgentD-submit | Vis idé, prosjekt, mål og akseptkriterier. Idé-TTL og relasjoner bevares. |
| Board / oppgavedetalj | Legg i kø, utfør avgrenset prompt, les relaterte repo-filer | Arbeidsordre → AgentJobs; AgentRun viser kildekvitteringer | Bind workItemID, executor, workspace, base-ref, filer, mandat, budsjett og stabil commandID. |
| Prosjektportefølje / arbeidsrom | Les repo, oppsummer status, opprett oppgave, start køet jobb | Autorisert repo-leser og WorkItem/AgentJobs | Bruk prosjektets verifiserte repo; ingen vilkårlig URL/path eller credential i modellprompt. |
| Cell Configuration Studio | Les cellekontrakt, generer forslag, forhåndsvis, lagre versjon, publiser | Studio + DraftVersion + eiercelle | Vis akkurat valgt configuration/instance; valider Skeleton og faktisk action-payload; lagring og publisering er separate. |
| Formålstrær | Finn/match, dekomponer, foreslå relasjon, opprett oppgave | Purpose/Goal/Perspective og WorkItem | Match gir relevans; det oppretter ikke rettigheter og godkjenner ikke modellens forslag. |
| Agreement Workbench | Forklar, foreslå vilkår/grants, prøv requester, be om tilgang | Agreement-løpet og faktiske ressurser | Gjenbruk PR #314 og underliggende preflight. Ingen signering uten at lovet tilgang er prøvd. |
| Git / PR-kort | Les diff/kilde, be om review, merge PR | Avgrenset Git-effektcelle og verifisert GitHub-kvittering | Eksakt repo, PR, head/base SHA, påkrevde checks og review. Endret head ugyldiggjør gammelt forslag. Ikke rå shell fra modellen. |
| AgentRuns / kø | Se løp og rapport, oppfølging/retry som ny attempt | AgentJobs som autoritativ utfører | Registration betyr passivt registrert. Køet/running/done kommer fra executor, ikke chattekst. Usikkert utfall leses tilbake før retry. |
| Admin Workbench / release | Legg verifisert kandidat i deploykø, utfør tillatt staging/prod-ordre | Canonical deploykø og Admin receipt | Eksakt artefakt/SHA, miljø, gjeldende mandat, claim, kapasitet, backup og funksjonsprøve. Koordiner med køeier. |
| Historikk / Chronicle | Søk tekst/formål, åpne kilde, lag oppfølging, del valgt utdrag | Privat eller prosjektavgrenset historikk med samme tilgang i indeks | Replay åpner ikke tidligere effekt på nytt. Skjulte treff, counts, snippets og embeddings må ikke lekke. |
| Butler / selvstendig chat / komponent | Samme tillatte handlinger ut fra valgt objekt | Samme domeneoperasjoner som over | Egen session- og mountidentitet; ingen tilgang via vertens eier i stedet for faktisk requester. |

«Utfør prompt» består av to forskjellige valg: send en samtaletur til valgt modell, eller start en konkret agentjobb. Modellen må ikke velge den dyrere/mer privilegerte betydningen i det stille. «Legg i kø» kvitterer først med en faktisk jobbreferanse når utføreren har tatt imot ordren.

Merge/deploy er ikke generisk angrebare. Undo for vanlige oppgaveendringer må sjekke forventet revisjon; den skal ikke overskrive en annen brukers senere arbeid. Planlegging, autorisasjon, utføring og kvittering er separate steg, men eksisterende gyldige mandater skal hindre overflødige bekreftelser.
