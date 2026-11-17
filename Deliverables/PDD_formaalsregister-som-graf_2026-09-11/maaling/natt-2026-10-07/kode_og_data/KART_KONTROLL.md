# Kontroll av etikett_kart_butler_v2.json (Astra, før første kjøring)

Dato: 2026-10-07. Grunnlag: generator-definisjonene (etiketter-generator-v2.md), alle 264 meldinger i korpus-v2.jsonl (33 etiketter × 8), register_liste.txt (89 noder) + NEW_NODES i register_v1.py.

Målestokk: en liste er **for vid** hvis den godtar et formål som en nøytral leser ikke ville sagt «betyr» det meldingene ber om, eller en gren eller fellesnode som matcheren kan treffe som reserve. Den er **for smal** hvis den mangler et registerformål som beskriver meldingene minst like godt som det som står der.

## Tabell

| etikett | dom | foreslått liste | begrunnelse med eksempelmelding |
|---|---|---|---|
| H.invite | FOR VID | `contact.introduction` | «add jonas to this chat», «Please invite Espen Haugli to HAVEN». Det handler om å få noen inn i en tråd eller i HAVEN. `contact.introduction` («connect people through a purpose-bound contact request») er den nærmeste noden. `contact.communication` er fellesnoden for all kontakt («initiate, continue, or refuse contact»), og den passer bedre på H.video, som står som HULL. Kartet godtar altså noden der den passer dårligst og avviser den der den passer best. Fjern den her. (Streng lesning: begge er omtrentlige, og «inviter medlem» er egentlig et hull.) |
| H.poll | OK (merknad) | `digital-work.collect-structured-input`, `questionnaire.campaign.complete` | «can u make a qucik pol for the board, quiz nite thursday or friday?» `collect-structured-input` passer godt. `campaign.complete` (med samtykke, utsending og analyse) er tyngre enn en hurtigavstemning, men kan forsvares. Er den godtatt, er `questionnaire.admin.authoring` like forsvarlig. Velg én linje: godta hele questionnaire-familien eller bare `collect-structured-input`. Grenen `digital-work` er riktignok ikke godtatt, og det er bra. |
| H.idea | OK | HULL | «idea: silent disco at samfundet», «not a task, just something to think more about later». Ingen node for idélager. `work-items` er uttrykkelig avvist i flere av meldingene. |
| H.workitem | OK | `project-work.work-items` | «Tokn-refresh feiler … Kan du lagge en bug på det?» Beskrivelsen «Track tasks, bugs…» passer. |
| H.project | FOR SMAL | `project-work.overview-and-sharing`, `project-work.project-portfolio`, `digital-work.coordinate` | «need one place with all the tasks, people and deadlines for the whole thing». Dette er nesten ordrett `digital-work.coordinate` («Plan, coordinate, share and track work across people»). Kartet godtar `coordinate` for H.meeting, der den passer dårligere, men ikke her. |
| H.todo | OK | `project-work.work-items` | «Add to my list: order balls». Beste node i registeret. NB: samme svar er riktig for H.workitem, så matcheren må ikke skille de to. Det gjør treffraten for begge litt lettere. |
| H.reminder | OK | HULL | «Remind me Sunday at 8 …». Ingen node har tid eller påminnelse. |
| H.meeting | FOR VID | `event.meeting.draft-request` | «Jeg trenger en møte med Ingrid og Tobias neste uke … Kan du booke det». `draft-request` er eneste møtenode og kan godtas. `digital-work.coordinate` er en bred fellesnode («work across people») som treffer alt med flere deltakere. Den gir gratispoeng og bør ut. |
| H.video | OK (merknad) | HULL | «Start video call with Marit.» Videomøte finnes ikke. Se H.invite: hvis `contact.communication` beholdes noe sted, er det her den hører hjemme, ikke under invite. |
| H.agent | OK | HULL | «close all the finder windows on my mac». Ingen node. `grounding` er en abstrakt gren og skal ikke godtas. |
| H.onboarding | BØR VÆRE HULL | HULL (eventuelt egen rapport) | `human-agency` er en gren nær roten («understand, choose, delegate, review, and reverse digital actions»), ikke et formål for å komme i gang. Med søskentilbakefall (`sibling_backoff`) kan matcheren svare med en forelder, og da får den kreditt for et vagt svar. Halvparten av meldingene handler om API-nøkkel og språkmodell («i got an api key from my prof, where do i paste it»), og det er samme hull som S.aigateway. Merknaden i kartet sier selv at etiketten er arvet fra nattkorpuset, ikke at den er riktig. |
| H.advisory | OK | `analysis.decision-support` | «want a proper pros/cons breakdown». Passer nøyaktig. `advisory-panel` er facet-only og kan ikke treffes uansett. |
| H.capability | FOR SMAL | `capability.request-new-functionality`, `capability.request-human-review` | «send det videre til dem som utvikler dette», «please tell the developers we need that». `request-human-review` («Queue capability gaps for human review») beskriver nettopp det å sende videre til mennesker. En rimelig leser godtar den. |
| S.agenda | OK | `event.agenda.recommendation`, `event.participation` | «What's on at Arendalsuka today?» Begge passer. |
| S.docs | FOR VID | `librarian.explain-haven`, `librarian.catalog` | «wheres the documentaion for cellprotocol», «What actually happens when a cell emits an event and nobody's subscribed?» Meldingene gjelder teknisk virkemåte, ikke regler eller samtykke. `knowledge.explain-policy` («Explain rules, policy, or consent boundaries») passer i beste fall på én av 8 (tilgangsstyring). Fjern den. NB: `explain-haven` er også godtatt under M.meta, så ett og samme svar gir poeng i to etiketter. |
| S.map | OK | HULL | «samfundet on a map pls». Ingen node. |
| S.agreement | OK | HULL | «both parties must sign». Ingen avtalenode. |
| S.profilepage | OK | HULL | «Edit my profile page, please.» Ingen node. |
| S.publish | BØR VÆRE LISTE (feil HULL) | `content.review-before-publish` | «can i publish our fall semester recap so anyone can read it?» Noden lyder «Prepare publication of notes, summaries, or public content with review, consent, and explicit confirmation». Den treffer nesten ordrett, og en melding ber til og med om gjennomlesing først («fix the obvious typos first»). Som HULL blir et riktig svar talt som forslag på et hull, altså urettferdig mot matcheren. |
| S.music | OK (merknad) | HULL | «I want to upload the club song we recorded». Musikkopplasting finnes ikke. Svarer matcheren `content.review-before-publish` (gjøre innhold offentlig), bør det rapporteres som et delvis riktig hull-forslag og ikke telles som en feil. |
| S.mermaid | OK | HULL | «Kan du tegne et sekvensdiagarm». Ingen diagramnode. |
| S.entity | BØR VÆRE HULL | HULL | «I need to manage my relations — remove my old employer and add Lysverk». `skeleton.owner-entity-access` er en GUI-invariant («every production skeleton leaves the owner a visible route back to their own entity»), ikke håndtering av relasjoner. Kartet ser ut til å være laget på ordet «entity». Det finnes ingen node for relasjoner til personer og organisasjoner. |
| S.admin | OK | `scaffold.operations` | «can i see which services are runing and whats down?» Beskrivelsen «connected, observable, recoverable» passer. |
| S.aigateway | OK (merknad) | HULL | «Switch to a cheaper AI model». Hull. Men 3 av 8 meldinger er rene spørsmål om sted og jurisdiksjon («servers inside the EU», «datasenter i Norge», «not through an american company»). Der er `self-determination.data.locality` et rimelig svar. Rapporter slike treff for seg i stedet for å telle dem som feil. |
| S.meetplace | OK | HULL | «what's a good middle point between Majorstuen and Nydalen?» |
| S.commerce | OK | HULL | «anywhere near here in arendal that sells one?» |
| S.networking | OK | `event.privacy-preserving-networking`, `contact.introduction` | «Is there a way to see who is present and interested in the same topics?» Begge passer. `event.participation` kan diskuteres, men er ikke nødvendig. |
| S.vote | OK (merknad) | HULL | «Hvor kan jeg stemme i saken om åpne data i kommunen?» Ingen node for avstemning blant innbyggere. `questionnaire.respondent.form` (svare som respondent) ligger nær. Rapporter treff der som delvis riktige hull-forslag. Vær obs på at H.poll-formålene ikke må lekke inn her som «riktig». |
| S.cellconfig | BØR VÆRE HULL / UTENFOR R4 | ingen liste. Skal ut av nevneren for topp-1 og rapporteres for seg | «I want to build a new surface myself …» Alle capability-noder som betyr dette er facet-only: `construct-cellconfiguration`, `delivery` og `reuse-visible-configuration`. R4 utelukker dem som primærsvar, så de 8 meldingene gir garantert bom. Står listen, blir det 8 kunstige bom i topp-1. `request-new-functionality` passer ikke, fordi brukeren vil bygge selv og ikke bestille. |
| M.meta | FOR SMAL + delvis FOR VID | `conversation.introduce-self`, `knowledge.explain-policy`, `self-determination.data.recipients`, `access.audit.privacy` (+ `librarian.explain-haven` **bare** ved kjøring mot det frosne R4-registeret) | Etiketten dekker to ting. 4 av 8 er «hvem er du» («e du en ekte person eller en bot?»), og der er `introduce-self` riktig. Like mange er «hvem kan lese det jeg skriver» («does anyone on the HAVEN side read these chats?»), og det er personvern. Der er `explain-policy` («consent boundaries in plain language»), `data.recipients` og `access.audit.privacy` riktige, men ingen av dem står i listen. `explain-haven` har i v1 fått fjernet AI-figuren og aliaset «hvem er du». Mot v1-registeret er den derfor feil. Godta den bare i kjøringen mot det frosne registeret, og merk det. |
| C.clarify | OK (presisering) | NEG | «Gjør som sist». Riktig. Testriggen må definere at `prompt.unknown` og spørsmål tilbake regnes som riktig avholdenhet, og at et forslag om et formål er feil. |
| N.none | OK (presisering) | NEG | «lol ok thanks», «Thank you, that was helpful.» Dette vil sannsynligvis trekke matcheren mot `conversation.accept` og `conversation.open`. De er `neverSurface`, men de er fortsatt formål. Avgjør før kjøringen om et `conversation.*`-svar på NEG skal telles som et formålsforslag. Jeg anbefaler at `conversation.accept` på «takk» telles som feil, men holdes adskilt fra feil forslag om en flate. |
| G.gap | OK | NEG | «can u oder me a taxi to værnes». Riktig at ingenting skal foreslås. `prompt.unknown` = riktig. |

## Generelle funn

1. **Gratispoeng fra fellesnoder:** `digital-work.coordinate` (H.meeting), `contact.communication` (H.invite) og grenen `human-agency` (H.onboarding) er brede noder som en svak matcher treffer som reserve. Alle tre bør fjernes der de står. Den eneste fellesnoden som bør godtas, er `coordinate` under H.project, der den betyr det meldingene ber om.
2. **Etiketter som ikke kan treffes:** S.cellconfig (bare facet-only). H.onboarding i praksis også, siden den eneste godtatte noden er en gren. Begge må ut av nevneren for topp-1, ellers måles egenskaper ved registeret og ikke ved matcheren.
3. **Feil HULL som straffer matcheren:** S.publish har en nesten perfekt node (`content.review-before-publish`). S.entity har motsatt problem: en node som er godtatt uten å bety det.
4. **Blandede etiketter:** M.meta er halvt identitet og halvt personvern. Listen dekker bare den første halvdelen. Det samme gjelder S.aigateway, der 3 av 8 handler om sted og jurisdiksjon. Kartet virker per etikett, men slike etiketter trenger fasit per melding eller en egen kategori for delvis riktige svar.
5. **Overlapp som gir dobbel kreditt:** `librarian.explain-haven` er godtatt under både S.docs og M.meta, og `work-items` under både H.todo og H.workitem. Det er ikke galt i seg selv, men en matcher som ofte svarer med de to nodene får høyere treffrate uten å kunne skille etikettene. Rapporter en forvekslingsmatrise per formål, ikke bare treff per etikett.
6. **Meldinger med flere ønsker:** Flere meldinger har et annet ønske i tillegg til hovedetiketten. Eksempler: «… pros and cons, and also put on my list to call their chairman» (H.advisory + todo), «… legg gjerne inn på lista mi …» (H.meeting), «… remind me tomorrow …» (S.cellconfig). Et svar på bi-ønsket telles som feil. Rapporter topp-k eller merk disse meldingene.
7. **Register i to versjoner:** register_liste.txt har den gamle teksten for `explain-haven` («and explain the AI figure itself»), mens register_v1.py endrer den. Kartet må knyttes til registerversjonen det brukes mot, særlig for M.meta.
8. **Avvik mellom generator og sølvfasit:** 3 av 264 (S.meetplace→C.clarify, S.map→G.gap, H.idea→H.capability). Lite, men bestem på forhånd hvilken etikett som gjelder.

## Samlet dom

Kartet er i hovedsak forsvarlig. 20 av 33 etiketter kan brukes som de står, noen med merknader til riggen. Men det har **to systematiske skjevheter** som må rettes før første kjøring:

- **For rundt i retning gratispoeng:** H.invite, H.meeting, S.docs og H.onboarding (gren) godtar brede noder eller noder som ikke betyr det meldingene ber om.
- **Urettferdig mot matcheren:** S.publish (feil HULL), H.capability, H.project og M.meta (mangler noder som åpenbart passer) og S.cellconfig (kan ikke treffes).

S.entity er rett og slett feilkartlagt på grunn av likt ordvalg.

Endres disse, blir tallet fra R4 et mål på matcheren og ikke på kartet. Uten endringene kan skjevhetene i noen grad oppheve hverandre, men topp-1 per etikett blir da ikke til å stole på.

**Endringer:** 10 etiketter (H.invite, H.meeting, H.project, H.onboarding, H.capability, S.docs, S.publish, S.entity, S.cellconfig, M.meta). I tillegg kommer presiseringer i riggen for C.clarify og N.none og rapportering av delvis riktige hull-forslag for S.music, S.aigateway og S.vote. Selve kartet trenger ingen endring for disse.
