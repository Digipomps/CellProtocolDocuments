# Oppgave: skriv naturlige chatmeldinger til HAVEN

HAVEN er en norsk plattform fra stiftelsen Digipomps der folk har sine egne data og får hjelp av assistenter i chat.
Det finnes fire chatflater:
- butler: Butler (personlig chat-assistent i HAVEN: prosjekter, oppgaver, kontakter, møter, spørreundersøkelser)
- kallimachos: Kallimachos (bibliotekaren i HAVEN: kunnskap, kilder, allmenningen, forklarer HAVEN)
- onboarding: Onboarding (første møte med HAVEN: personvern, egne data, regler, komme i gang)
- hjelp: Hjelpechat (når noe ikke virker eller man lurer på hvordan noe fungerer)

Vi måler om en assistent UTEN språkmodell forstår hva folk mener. Derfor trenger vi meldinger slik ekte folk faktisk
skriver dem — ikke slik en maskin eller en dokumentasjon ville formulert dem.

Du skal skrive som personaen under. Hold deg i rollen: ordvalg, lengde, dialekt/målform, skrivefeil, tegnsetting.

## Formålene

Hver linje er et formål med kode, hvilken flate meldingen skrives til, og en ENGELSK teknisk beskrivelse. Beskrivelsen
forteller deg hva brukeren vil. **Ikke oversett beskrivelsen og ikke gjenbruk ordene i den.** Tenk: hva ville personaen
din faktisk skrevet i chatten når hun/han ville dette? Bruk konkrete ting (navn, prosjekter, steder, datoer) slik folk gjør.
Er formålet internt eller teknisk, skriv det en vanlig bruker av flaten ville spurt om som leder dit.

G01 | flate: kallimachos, hjelp | Access, audit and privacy: Keep visibility grant-bound and mutations auditable. Keep visibility grant-bound and mutations auditable.
G02 | flate: kallimachos, hjelp | Eierstyrt kryptering og nøkkellagring for celledata: Preserve owner control and independent private cell instances with cell-scoped SQLCipher, recipient-encrypted SecretCredentialCell custody, separate IdentityVault/Keychain unlocking roots and verified recovery. The database process remains trusted; discovery never authorizes key use.
G03 | flate: butler | Decision-support analysis: Set up structured analysis for a problem when the user needs depth, evidence, disagreement and an actionable recommendation.
G04 | flate: butler, hjelp | Human review for capability gap: Queue capability gaps for human review, prioritization and approval instead of forcing the user through many low-value messages.
G05 | flate: butler, hjelp | Request new functionality: Capture a feature request with purpose, interests, missing capabilities and acceptance goals when existing cells/configurations cannot satisfy it.
G06 | flate: butler | Contact and communication: Help people initiate, continue, or refuse contact with explicit purpose and privacy boundaries.
G07 | flate: butler | Contact follow-up: Continue an existing contact or meeting thread with explicit recipient and message context.
G08 | flate: butler | Contact introduction: Introduce or connect people through a purpose-bound contact request.
G09 | flate: butler | Review content before publish: Prepare publication of notes, summaries, or public content with review, consent, and explicit confirmation.
G10 | flate: butler, kallimachos, onboarding, hjelp | Accept what is proposed: Agree to, confirm or go ahead with the proposal, claim or step that is active in the perspective.
G11 | flate: butler, kallimachos, onboarding, hjelp | Introduce yourself: The AI figure presents itself: its name, what it does, what role it has and what it can and cannot do.
G12 | flate: butler, kallimachos, onboarding, hjelp | Open a conversation or request: Greeting or opening that starts a request. The assistant answers and invites the request; nothing is proposed.
G13 | flate: butler, kallimachos, onboarding, hjelp | Reject what is proposed: Decline, refuse or do not accept the proposal, claim or step that is active in the perspective.
G14 | flate: butler | Collect structured input: Collect structured answers or evidence from people or systems. Collect structured answers or evidence from people or systems.
G15 | flate: butler | Coordinate work: Plan, coordinate, share, and track work across people, agents, or scaffolds. Plan, coordinate, share and track work across people, agents or scaffolds.
G16 | flate: butler | Export data to a file format: Export and download data the owner may access (for example a table or list) to a file format such as spreadsheet, CSV or JSON.
G17 | flate: onboarding | The environment must bear the project's purposes: HAVEN-general (not librarian-specific). A project declares which environment Goals it depends on. It may start only when none of those bearing Goals is missed; a missing or unknown certificate lets the project start with a declared assumption and status unknown, never silently. When a bearing Goal is missed, the next work item is to make the environment more robust — and strengthening work items are exempt from their own level's gate, otherwise nothing could ever be repaired. Every environment i
G18 | flate: onboarding | Earth bears everything: Terminal ancestor of the adequacy recursion. HAVEN cannot measure the planet; it can measure and bound its own draw on it (energy per query, hosting energy source, hardware lifecycle, data retention as storage) and refuse projects whose environment certificate at this level is missed. Aligned with the existing SDG pilot purposes in CellProtocol (SDGPilotPurposeCatalog).
G19 | flate: butler | Event agenda recommendation: Recommend or open an agenda item based on current time, interests, constraints, and available event context.
G20 | flate: butler | Event meeting draft request: Draft an event meeting request or introduction while requiring explicit user action before sending.
G21 | flate: butler | Event participation: Help a person participate in an event by understanding agenda, people, privacy, and next useful actions.
G22 | flate: butler | Privacy-preserving event networking: Help people meet others at an event while limiting profile visibility and private data exposure.
G23 | flate: butler | Event schedule change request: Propose a schedule change for an event item while requiring role checks and confirmation.
G24 | flate: kallimachos | Local model assisted decomposition: Use a local model as proposal engine while HAVEN keeps deterministic authority. Use a local model as proposal engine while HAVEN keeps deterministic authority.
G25 | flate: hjelp | Functional accessible GUI: Ensure controls are labeled, focusable, visually stable, aesthetic, and wired to real actions. Ensure controls are labeled, focusable, visually stable and wired to real actions.
G26 | flate: onboarding | Human agency and understanding: Help people understand, choose, delegate, review, and reverse digital actions.
G27 | flate: kallimachos, hjelp | Explain policy or rules: Explain rules, policy, or consent boundaries in plain language without inventing authority.
G28 | flate: kallimachos, hjelp | Argument analysis: Turn a text, proposal or disagreement into a claim ledger (haven.claim-definition.v0) with type, strength, quote anchors, support and counters, and — where the inference type is recognisable — a Walton scheme with critical questions. Arguments are analysed; persons are never ranked.
G29 | flate: kallimachos, hjelp | Examine own bias: Kallimachos can measure structural bias in itself — coverage skew, source concentration, demand-vs-answer skew, answer drift, invitation patterns in aggregate, adversarial probes — and report it with statuses. It cannot measure 'truth bias'; it says so.
G30 | flate: kallimachos | Publish how Kallimachos is built: Transparency is core business (vedtektene § 5: gjennomsiktighet i tekniske og organisatoriske løsninger). The recipe — code, root data, tests, evaluation results, this tree, the persona, the merge protocol — is published so that others can instantiate Kallimachos themselves and audit ours.
G31 | flate: kallimachos, hjelp | Commons catalogue with sources and freshness: F3: answer 'what exists in the commons about X' with verbatim excerpts, source and last_verified; admit gaps explicitly and count them as demand.
G32 | flate: kallimachos | Growth of the commons: F4: when a gap is found or the user holds relevant data or functionality, Kallimachos invites them to add it — as an invitation with visible value return, never as nagging. At most one invitation per conversation; refusals are remembered; contributions get a ContributionProof trail.
G33 | flate: kallimachos, hjelp | Explain HAVEN: Explain HAVEN's concepts, rules and maturity with the right status (principle / implemented / tested / internal prototype / research direction).
G34 | flate: kallimachos | HAVEN canon conformity (gatekeeper, level 3): Proposals and answers obey HAVEN's own rules: no global reputation score, no global person ID, no hidden behavioural profiling, purpose declared and never inferred, agreement before access with least necessary authority, claims with status, forbidden claims never made.
G35 | flate: kallimachos | Illuminate value: Make visible where value arises in HAVEN (data, work, curation, consent, attention, code), where it flows and accumulates (PSP, operator, commons, providers, users/groups), and how a person's own contribution can return value — without reducing anyone to a value score.
G36 | flate: kallimachos | Merge of Kallimachos instances after audit: When two Kallimachos instances meet, they merge — but only after five gates: provenance handshake, cross purpose-audit, data-credibility audit (anti-poisoning), overlap analysis with highest scrutiny on non-overlapping data, and normalisation. Merging is growth (coverage up, cost per query down) and must pass the positive-sum ledger.
G37 | flate: kallimachos | Positive-sum exchange: Kjetil's rule: a trade or transaction is something every party should come out of well; the ecosystem is not a zero-sum game. Applied as a condition on everything Kallimachos proposes.
G38 | flate: onboarding | Presence on call: Kallimachos acts only after explicit call or a purpose-routed offer from the owner's butler; handover is visible and reversible; no background scanning of user content.
G39 | flate: kallimachos, hjelp | Propose a research question: Suggest a problem statement or research question worth investigating, grounded in what the commons holds and where its gaps are.
G40 | flate: kallimachos | Purpose decomposition: Decompose a request, proposal or disagreement into 1-3 known purpose:// nodes with haven.goal-definition.v1 Goals, facets and a verifier; unknown intent resolves to purpose://prompt.unknown with candidate intake. Refs are never invented.
G41 | flate: kallimachos | Regulatory design conformity (gatekeeper, level 1): Every proposal from Kallimachos is checked against the regulatory nodes that apply now, via explicit edges with a stated verifiability level. Results are reported as 'design criteria derived from', never as 'compliance with'.
G42 | flate: onboarding | Requester control over own history: F2: the asker can see, export and delete own query history per relation; every answer is auditable; a standing readable agreement replaces per-question consent.
G43 | flate: kallimachos | Root data available and verifiable to every fragment: Kallimachos lives across several scaffolds. The set of artifacts that define who Kallimachos is (purpose tree + norm hierarchy, persona, statutes with retrieval attestation, claims canon, corpus manifest, regulatory overlay, system instruction, test contracts) is content-addressed, listed in a signed root manifest, replicated to every fragment, and verified before a fragment serves.
G44 | flate: kallimachos | Sustain and grow the librarian (lowest level): F5: operating cost, coverage and created value per period are visible in an operating ledger; when capacity or coverage is too low, Kallimachos submits an evidence-based expansion proposal with purpose + Goal + cost. Kallimachos never spends funds itself.
G45 | flate: kallimachos | Ecosystem value-flow design: Analyse and propose constructions of the ecosystem in which a share of created value flows to maintenance, development and operation of the commons' resources (HAVEN commons allocation in ValuePoolPolicy), as simulable policy variants with a party ledger — humans decide.
G46 | flate: kallimachos | Ward statute conformity (gatekeeper, level 2): Kallimachos never proposes anything outside Stiftelsen Digipomps' registered purpose, anything that threatens its independent and politically neutral standing, or anything that makes payment a condition for non-commercial registered users' basic services.
G47 | flate: butler | Personal semantic context state: Represent owner-defined labels such as Home, Work, or lunch time without exposing raw location/time unless explicitly granted.
G48 | flate: kallimachos | Owner-controlled preferences: Keep reusable preference facts explicit, scoped, inspectable, and deletable. Keep reusable preference facts explicit, scoped and deletable.
G49 | flate: butler | Current status and outstanding work: Show where a project stands now and what remains outstanding. Show where a project stands now and what remains outstanding.
G50 | flate: butler | Project work overview and sharing: Manage projects, tasks, sharing, and current outstanding work. Manage projects, tasks, sharing and current outstanding work.
G51 | flate: butler | Project portfolio: Track project status, health, priorities, milestones, releases, and capacity. Track project status, health, priorities, milestones, releases and capacity.
G52 | flate: butler | Share selected project intent: Prepare, deliver, and open a selected project/work snapshot for a recipient. Prepare, deliver and open a selected project/work snapshot for a recipient.
G53 | flate: butler | Work items: Track tasks, bugs, decisions, comments, subtasks, relations, and blockers. Track tasks, bugs, decisions, comments, subtasks, relations and blockers.
G54 | flate: kallimachos | Capture and place new purposes: Detect new purpose candidates, find their nearest ancestor, and queue review when automatic placement is uncertain or consent is required.
G55 | flate: kallimachos, hjelp | Questionnaire access audit: Keep questionnaire responses consent-gated and transport payloads minimal. Keep questionnaire responses consent-gated and transport payloads minimal.
G56 | flate: butler | Questionnaire admin authoring: Configure title, context, consent, questions, pages, and lifecycle. Configure title, context, consent, questions, pages and lifecycle.
G57 | flate: butler | Complete questionnaire campaign: Create, deliver, answer, inspect, and analyze a questionnaire campaign. Create, deliver, answer, inspect and analyze a questionnaire campaign.
G58 | flate: butler | Questionnaire delivery and consent: Select recipients, send access-proof links, and preserve consent boundaries. Select recipients, send access-proof links and preserve consent boundaries.
G59 | flate: butler | Respondent questionnaire form: Expose consent, questions, draft save, submit, and withdrawal paths for a respondent. Expose consent, questions, draft save, submit and withdrawal paths.
G60 | flate: butler | Analyze questionnaire responses: Inspect counts and export response data transparently. Inspect counts and export response data transparently.
G61 | flate: butler | Collect questionnaire responses: Store draft and submitted answers with consent state and receipt IDs. Store draft/submitted answers with consent state and receipt IDs.
G62 | flate: onboarding | Scaffold operations: Purposes for scaffolds to keep themselves connected, observable, recoverable, and aligned with HAVEN.
G63 | flate: onboarding | Data self-determination: The owner decides the purpose, extent, place, manner, recipients and duration of any use of their own and derived data, and can verify that the decision was honoured.
G64 | flate: onboarding | Duration, withdrawal and deletion: How long use may last, and the right to change one's mind with downstream effect. New dimension: absent from the sketch.
G65 | flate: onboarding | Control that can actually be exercised: Control that demands expertise, time or money distributes power unevenly. Raises the sketch's ease-of-use wish to a criterion.
G66 | flate: onboarding | Place and jurisdiction of data use: The owner decides where data is stored and processed, and how many copies exist.
G67 | flate: onboarding | Manner of processing and derived data: Whether data may be linked, profiled, used for model training or otherwise derived from, and who controls the derived result.
G68 | flate: onboarding | Recipients and delegation: Named recipients, onward delegation the owner can see, and default deny for everyone else. New dimension: the sketch had no recipient axis.
G69 | flate: onboarding | Extent of data made available: The owner decides which fields, and at what precision, are made available, including the degree of identifiability.
G70 | flate: onboarding | Purpose binding for data use: Data is used only for a declared purpose the owner accepted; a new purpose requires a new acceptance.
G71 | flate: onboarding | Verifiability instead of trust: The owner can check that the rules were followed without having to trust the operator. Replaces the sketch's trust-in-organisation requirement.
G72 | flate: hjelp | Owner entity access affordance: Ensure every production skeleton leaves the owner a visible route back to their own entity, Co-Pilot, or equivalent recovery interface.
G73 | flate: kallimachos, hjelp | Current methodology sources: Use source evidence with checked dates and stale-source policy. Use source evidence with checked dates and stale-source policy.
G74 | flate: hjelp | Hallucination evaluation gate: Periodically test that chat, purpose decomposition, model-assisted proposals, and source-backed answers do not invent facts, refs, capabilities, or unsupported certainty.
G75 | flate: hjelp | Project work acceptance tests: Protect project/work decomposition and cell behavior. Protect project/work decomposition and cell behavior.
G76 | flate: hjelp | Purpose decomposition acceptance: Protect deterministic prompt decomposition and model-proposal boundaries. Protect deterministic prompt decomposition and model-proposal boundaries.
G77 | flate: hjelp | Questionnaire acceptance tests: Protect questionnaire decomposition and campaign behavior. Protect questionnaire decomposition and campaign behavior.

## Hva du leverer

For HVERT formål: nøyaktig TO meldinger.
1. `kort`: 1–4 ord, slik man skriver kjapt.
2. `naturlig`: en vanlig melding, gjerne indirekte eller med kontekst rundt (ikke start alle med «kan du»).

Varier oppbygningen. Ingen to meldinger skal begynne med samme tre ord. Ikke nevn formålskoden eller ordet «formål».
For samtaleformålene (åpne, godta, avvise, presenter deg) skal meldingene være slik man faktisk hilser, sier ja/nei
til noe assistenten nettopp foreslo, eller spør hvem assistenten er.

Skriv resultatet som JSON med Write-verktøyet til filen som står i oppdraget ditt:
`[{"code": "G01", "flate": "<en av flatene oppgitt for koden>", "stil": "kort"|"naturlig", "tekst": "..."}, ...]`
Totalt 2 × antall formål objekter. Kontroller at filen er gyldig JSON (les den tilbake med Read). Svar til slutt bare
med antall meldinger du skrev. Ikke bruk andre verktøy enn Write/Read, og ikke kall mcp__hearthbot__-verktøy.
