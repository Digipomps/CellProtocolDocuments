# Planlagt dataflyt — ikke implementert

~~~mermaid
flowchart LR
 A[Tilgjengelige prosjekter / Portfolio] -->|projectRef + viewID| W[ProjectWorkspace]
 P[ProjectPortfolio / WorkItem / Idea] -->|snapshot + Flow| W
 G[GraphStore] -->|relasjoner + synkstatus| W
 W -->|autorisert snapshot / cursor| U[Porthole og Binding]
 U -->|commandID + prosjekt + versjon| C[Workbench kommandoport]
 C -->|requester-grant + lokal policy| D[AgentD jobbkontroll]
 D -->|varig kvittering + hendelse| W
~~~

| Kant | Kontrakt | Autorisasjon og kvittering |
|---|---|---|
| Inngang → Workspace | projectContext | Eksakt portfolioUUID/projectID autoriseres; lokal viewID gir ingen tilgang |
| Kilder → projeksjon | sourceSnapshot/sourceEvent | Kilderevisjon/tilgang per kilde, separate cursors |
| Graf → projeksjon | relation | Typet retning, sourceRef og tillatte endepunkter/etiketter; completeness eksplisitt |
| Workspace → klient | projectionSnapshot/projectionEvent | Scope, cursor og freshness; gap gir avstemming, revokering fjerner data |
| GUI → port | command | Grant og versjon server-side; commandID binder identitet/payload |
| Port → AgentD | executionCommand | Prosjektbundet myndighet i tillegg til lokal executable/path/network-policy |
| AgentD → Workspace | commandReceipt/jobEvent | Lagret command er ikke start/stopp; terminal status kommer fra utfører |

Privat jobbinnhold/historikk lagres i eierpartition. Felles prosjektprojeksjon får bare eksplisitt tillatt metadata. Ingen automatisk deling av private tekster eller arbeidsstier. Hjelpechat W1/W7 integreres gjennom samme kontrakter. AgentRun er observasjon.

