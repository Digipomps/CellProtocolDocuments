# Celle-autentisitet — vurdering

Dato: 2026-09-04 (vurderingen utført 2026-08-28 mot dokumentene slik de forelå da)
Status: kildeforankret vurderingsnotat. Ingen implementasjon følger av dette
dokumentet alene. Videre arbeid går gjennom PDD-mappen
`Deliverables/PDD_bridge-fase2-handshake_2026-09-04/` (bridge fase 2).

Bestilling (Kjetil, 2026-08-28, ordrett):

> Vurder om det kan være nyttig om celler i seg selv kan bevise sin
> autensitet. Jeg tenker det kan være nyttig å vite helt sikkert at den
> cellen som bruker set/get eller andre ting er den man forventer. Med samme
> mekanisme som Identity bruker men knyttet til celle. Slik at man ikke kan
> lure inn en feil celle i en eller annen sammenheng. Kanskje også for å få
> bedre sikkerhet over bridge?

Påstandsdisiplinen fra
[Bridge_Kapabiliteter_Som_Formaal_2026-08-09.md](Bridge_Kapabiliteter_Som_Formaal_2026-08-09.md)
gjelder i hele notatet: hver bærende påstand merkes **dokumentert** (kilde
finnes), **brukt** (et lag benytter det i dag), **krav** (ønsket, mangler
implementasjon) eller **antatt**.

## 1. Formål

Mottakeren av et get/set (eller en flow) skal kunne avgjøre, uavhengig av
transport og konfigurasjon, at avsenderen er nøyaktig den cellen den
forventer — og avsenderen skal kunne avgjøre det samme om mottakeren, særlig
over bro. Målbart: en byttet celle (feil navn, feil instans, feil vert, feil
konfigurasjon) gir et typed avslag uten sideeffekt.

## 2. Dagens tilstand

- **Dokumentert:** Requesteren i get/set er en Identity, ikke en celle:
  `cellAtEndpoint(endpoint:requester:)` og `get(keypath:requester:)` tar
  identiteten fra vaulten (`Book/10_Quickstart.md` §6). Mottakercellen vet
  hvilken *eier* som kaller, ikke hvilken *celle* som kaller på eierens vegne.
- **Dokumentert:** Mottakercellen identifiseres ved navn — `cell:///Navn` med
  `cellScope: .identityUnique` (`Book/10_Quickstart.md` §5) — og over bro ved
  `cell://vert/Navn` → `wss://vert/bridgehead/Navn`
  (`Book/06_CellResolver.md` §8). TLS beviser verten, ikke cellen.
- **Dokumentert:** FlowElement har ingen produsentsignatur
  (`Book/05_Flows_Lifecycle.md` §1 og §7). **Krav:** `Book/08_Bridging_Transport.md`
  §1 beskriver envelopes med «producer identity» og «signature» — det er
  arkitekturmål, ikke implementert kontrakt.
- **Dokumentert:** Bridgeheaden får identitetsdomene
  `bridgehead:<bridgeReference>:<requester.uuid>`, og kanalbesittelse er ikke
  en kapabilitet (`Bridge_Kapabiliteter_Som_Formaal_2026-08-09.md`, F3).
- **Dokumentert, gjenbrukbart:** Identity-modellen med domenebinding og
  `grantsAuthority: false` (`Book/03_Identity_Model.md` §2.1);
  scaffold-identitet med enrollment-flyt — signert forespørsel →
  eiergodkjenning → aktiveringsutfordring → aktiv lenke, med testede avslag
  for forfalsket scaffold-signatur (`Book/32_Cross_Scaffold_Entity_Enrollment.md`
  §4 og §8); eierkontroll-challenge bundet til bro-endepunkt
  (`Book/06_CellResolver.md` §9.1); A4-beslutningen der celle-endepunkt og
  keypath inngår i policyens config-digest, versjonert 1.1.0
  (`Purpose_Bound_External_Action_Contract_2026-08-03/A4_AUTHORITY_ISOLATION_DECISION.md`).

## 3. Funnet som styrer designet

Audit-en fra 13.07 fant nøyaktig fellen som må unngås. I device-ingressen var
«a signature alone is insufficient because the current Contact-style envelope
verifies against the identity embedded by the caller», og reviewer-en advarte
at «Contact's self-contained signature verification is a cryptographic
primitive, not a registered-key authority proof»
(`HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md`, ca. linje 1137 og 1484).

En celle som signerer med en nøkkel den selv presenterer, beviser bare at den
har nøkkelen. Om det er *riktig* celle avgjøres av hvem som har gått god for
at nøkkel K er celle X — og av hva X betyr (type, konfigurasjon, instans,
scaffold). Uten den bindingen er mekanismen T10 i trusselmodellen
(`Purpose_Bound_External_Action_Contract_2026-08-03/THREAT_MODEL.md`):
trust theater. «Samme mekanisme som Identity» er riktig tanke, men
Identity-mekanismen alene løser ikke oppgaven — det er derfor domenebindingen
allerede er merket `grantsAuthority: false`.

## 4. Trusler mekanismen faktisk treffer

**Feil kaller-celle (T5, confused deputy).** I dag kan mottaker ikke skille
«eier via Butler» fra «eier via en annen celle» når begge bruker eierens
identitet. Et skille mellom prinsipal (hvem sin autoritet) og aktør (hvilken
celle) gir minste privilegium per celle; Contract-subjekt kan være en celle.
A4 løste dette ett sted med en egen celletype med nøyaktig ett Grant;
celleidentitet generaliserer mønsteret. Avgrensning (**dokumentert**,
`Book/06_CellResolver.md` §7): i samme prosess stopper det ikke ondsinnet
kode. Det stopper *forvekslede* celler — og det er den realistiske trusselen
nå: navnematch (`resolveCellConfiguration` matcher på uuid eller eksakt navn;
«Butler Chat» er et klientalias, jf. Samlet_Oversikt 2026-08-24), dekodede
persisterte celler og stale mappings har allerede kostet en hel
reparasjonsbølge (audit D2, ca. linje 1253).

**Feil mottaker-celle over bro.** Sterkeste nytten. En byttet celle på verten
— operatørfeil, feil deploy, kompromittert scaffold — er usynlig for klienten
når bare TLS beviser verten. Pinnet celle-fingerprint i
Agreement/CellConfiguration, pluss at bridgeheaden signerer
handshake-transkriptet (kanalbundet, med nonce) med cellens nøkkel, gir
known_hosts på cellenivå. Det er også det som gjør `Book/08` §6 sant: at
transporten ikke kan legge til eller fjerne autoritet forutsetter at
autentisiteten ligger i semantikken, ikke i TLS.

**Proveniens i flows.** Signerte produsent-envelopes gjør `Book/08` §1 sant og
er forutsetningen for multi-hop-regelen «ingen hop kan re-signere» (noe må
være signert først) og for offline bundles. Kallimachos-fusjonen trenger det:
når instanser møtes og fusjonerer etter audit, må hvert datainnslag kunne
spores til en bestemt instans for at «unngå forgiftning» skal være mer enn en
intensjon.

## 5. Kostnad

- **Nøkler:** én per celleinstans, og i praksis én per domene om korrelasjon
  skal unngås (`Book/03` §2 advarer mot gjenbruk). Vaulten vokser; rotasjon,
  revokasjon og backup må håndteres. Viktigst: WO-E —
  runtime-identity-manifest-backup-transaksjonen — låser 2026.08.1 allerede;
  per-celle nøkler gjør den transaksjonen større. Persisterte celler må
  re-hydrere nøkkel med samme UUID+fingerprint-disiplin som eierhydrering
  (audit D2), som tok en hel bølge å få riktig.
- **Ytelse og plassering:** signering på hvert lokale get/set er kostnad uten
  nytte i samme prosess. Aktør-identitet lokalt trenger ingen kryptografi —
  resolveren vet hvilken celle den ga ut ved resolve. Signatur hører hjemme
  der en tillitsgrense krysses: bro, persistens, flows som forlater
  scaffoldet.
- **Planen:** sju porter står åpne (Samlet_Oversikt 2026-08-24); dette må ri
  på en eksisterende port, ikke bli en åttende.

## 6. Anbefaling, trinnvis og målt mot formålet

**Nå, uten å bygge:** bestem at handshake-scope i bridge fase 2 skal ha plass
til celle-nivå bevis begge veier — fra klient requester-identitet pluss
aktør-celle, fra vert celle-proof over transkript med nonce. Feltene er
billige å legge inn nå og dyre å ettermontere. Dette er den ene beslutningen
som haster, fordi porten allerede er åpen.

**Steg 1 (billigst, ingen nøkler):** pinning av type og config-digest i
`cellReferences` — `cell:///Navn` pluss forventet type og digest — slik at
resolveren avviser feil celle lokalt. Dekker forvekslingstrusselen (T7) og
utvider A4-mønsteret.

**Steg 2 (bro):** pin scaffold-identiteten per vertsrute i
`RemoteCellHostRoute` — én nøkkel per scaffold; `Book/32` gir scaffoldet
identitet allerede. Celle-nivå nøkkel bare der celler på samme vert er
innbyrdes mistroiske: flerbrukerscaffold (Palazzo) og distribuert
Kallimachos.

**Steg 3:** prinsipal/aktør-skille i requester-konteksten og Contract-subjekt
som celle. Modelleres som Identity med ny `bindingKind: cell_instance`
(celle-UUID, typenavn, config-digest, scaffold-fingerprint,
`grantsAuthority: false`) — ikke en parallell type, slik at vault, challenge
og enrollment gjenbrukes.

**Steg 4:** signerte produsent-envelopes på flows som forlater scaffoldet —
der, og bare der.

**Forutsetning for 2–4 i prod:** WO-E må håndtere de nye nøklene. Ellers
flytter release-blokkeringen én etasje opp.

## 7. Hva mekanismen ikke gir

Kodeintegritet (et kompromittert scaffold signerer gjerne), E2EE
(`Fabel_E2EE_Assessment_2026-07-21.md` skiller lagene), eller beskyttelse mot
fiendtlig kode i samme prosess. Dette skal ikke loves i produktspråk;
`haven-claim-review` gjelder for alle offentlige formuleringer.

## 8. Kilder

- `Book/03_Identity_Model.md` (§2, §2.1, §3)
- `Book/05_Flows_Lifecycle.md` (§1, §7)
- `Book/06_CellResolver.md` (§7, §8, §9.1)
- `Book/08_Bridging_Transport.md` (§1, §5, §6)
- `Book/10_Quickstart.md` (§5, §6)
- `Book/32_Cross_Scaffold_Entity_Enrollment.md` (§1, §4, §7, §8)
- `Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13.md` (ca. linje
  1109–1137, 1253–1259, 1452–1456, 1484–1485)
- `Deliverables/Bridge_Kapabiliteter_Som_Formaal_2026-08-09.md` (F3, F4, regelen om påstander)
- `Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/THREAT_MODEL.md` (T5, T7, T10)
- `Deliverables/Purpose_Bound_External_Action_Contract_2026-08-03/A4_AUTHORITY_ISOLATION_DECISION.md`
- `Deliverables/Fabel_E2EE_Assessment_2026-07-21.md` (§4.2, §5)
