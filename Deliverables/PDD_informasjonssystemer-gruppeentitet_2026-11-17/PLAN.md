# PLAN — Informasjonssystemer som gruppeentitet

G1 godkjent 2026-11-18 · G1-GUI godkjent 2026-11-18 · **G2: godkjent 2026-11-18**

Én arbeidspakke per bladformål i FORMAALSSPEC §1, i rekkefølgen de avhenger av hverandre. Swift (CellBase,
CellScaffold, Binding) er referansen og bygges først i hver pakke. Python og Go porteres fra Swift-genererte
fixtures i `CellProtocol/fixtures/interop/v1`, slik interop-arbeidet i oktober gjorde.

Utførere: **Claude** (skyen, Swift via Docker `swift:6.1-noble` for CellBase/ScaffoldKit-rigger, Python, Go),
**Mac** (Claude via Remote Control i en /tmp-klon: Binding/CellApple-bygg og tester, CellProtocol-tag),
**Kjetil** (merge, tag-godkjenning, HAVEN-Deploy-forespørsel, invitasjon til Petter).
Ingenting merges, tagges eller deployes av Claude. Staging går via HAVEN-Deploy-toget med en FORESPOERSEL.

## Arbeidspakker

| WP | purposeRef (`…gruppeentitet.*`) | Repo / PR | Hva | Test(er) som skal bli grønne | Utfører |
|---|---|---|---|---|---|
| WP0 | — (baseline) | alle | Kjør eksisterende tester før endring: `GovernancePolicyEvaluatorTests` (17), interop-fixturene i Py/Go, CellScaffold Linux-CI på main, Binding `-only-testing:BindingTests` på Mac. Tall føres i TESTRESULT.md#baseline som «forventet ≈ N (kilde, dato)» | — | TESTRESULT.md#baseline | Claude + Mac |
| WP1 | genesis | CellProtocol | `OrganizationGenesisSeal` (signert av grunnleggerne, peker på policy v1), policykjede (`previousPolicyHash`, monoton versjon, endring bare via `amendmentRuleID`). `IdentityLinkRegistry.sameEntityLink` og EntityAnchor feiler lukket fra person til organisasjonsanker. Fixtures `org-genesis/*` | test.ge.genesis, test.ge.no-same-entity | Claude |
| WP2 | ownership-agreement, owners | CellProtocol | Maler som data: `rolesOneGovernanceAll` (start), `allTwo`, `oneAlone`, `twoOfThree`. Regelnavn `roller` (actionClass `role.issue`, `role.revoke`) og `styring` (`policy.amend`). Bytte av mal = ny policyversjon. Fixtures med forventet godtatt/avvist per mal | test.ge.ownership-templates, test.ge.owners-rules | Claude |
| WP3 | owner-onboarding | CellProtocol | v1 med Kjetil alene → v2 med Kjetil + Petter (testidentitet i fixtures). Rolle utstedt under v1 verifiseres etter v2 | test.ge.policy-chain | Claude |
| WP4 | vault | CellProtocol | `OrganizationKeyCustodian`-protokoll og `OrganizationVaultCell` i CellBase: forslag inn, godkjenninger inn, signatur ut, nonce via `CellSecuritySigningChallengeReplayStore`, journal i `EntityAuthorityJournal`, sammendrag laget av hvelvet fra payloaden. CellVapor-custodian med programvarenøkkel (`keyIsExportable = true`, vist som «testnøkkel»). CellApple-custodian utsettes (ingen bruk her) | test.ge.vault-negative, test.ge.journal, test.cell.auth-negative, test.cell.contract-fixtures | Claude (Linux), Mac (CellApple-bygg) |
| WP5 | roles | CellProtocol | `InformasjonssystemerRoleCredential` (generelt navn i koden: `OrganizationRoleCredential` med `type` som også bærer gruppas typenavn): `credentialSubject.id`, `role`, `cohort`, `validUntil`, `policyHash`, `credentialStatus`. Utstedes som `role.issue` gjennom hvelvet. Fixture `org-role-vc/*` | test.ge.role-vc-fixture | Claude |
| WP6 | revoke, status-offline | CellProtocol | Statusliste signert av gruppa, speilet til noden ved hver endring. Vilkåret sjekker lokalt; speil eldre enn 10 min eller borte → `role_status_unknown`, lukket | test.ge.revoke-next-access, test.ge.status-offline | Claude |
| WP7 | condition, trust-anchor | CellProtocol | `ProvedClaimCondition` med `requiredCredentialType` + `subjectClaimPath: "role"` mot rolle-VC-en; utsteder må stå i `TrustedIssuerCell` for formålet. Negative: fremmed, feil rolle, tilbaketrukket, utløpt, ikke godkjent utsteder | test.ge.condition-interop (Swift-delen), test.ge.issuer-not-trusted | Claude |
| WP8 | genesis … condition (port) | PyCellProtocol | Port av WP1–WP7: policy, evaluator, maler, genesis, rolle-VC-verifisering, statusliste, `ProvedClaimCondition` + TrustedIssuer. Bare fra fixtures; ingen Py-spesifikk snarvei | samme tester, Py-kolonnen | Claude |
| WP9 | genesis … condition (port) | GoCellProtocol | Som WP8 for Go | samme tester, Go-kolonnen | Claude |
| WP10 | condition | PyCellProtocol `interop/matrix` | Matrisen 3 språk × 5 tilfeller (+ utsteder ikke godkjent, + status ukjent) | test.ge.condition-interop, test.ge.issuer-not-trusted, test.ge.status-offline | Claude |
| WP11 | owns-cells, vault | CellScaffold | Hvelvcellen og gruppecellen registreres på scaffolden med gruppas identitet som eier. Scaffold-eier kan stoppe, ikke signere eller gi roller. Ny testsuite føres i `ci/test-filter.txt` | test.ge.owns-cells, test.cell.auth-negative | Claude |
| WP12 | owner-surface, approve (web) | CellScaffold | Gruppeflaten og «Gi rolle» etter de godkjente bildene (`skeleton/gruppe.v1.json`, `gi-rolle.v1.json`); keypaths `group.*` mot cellene fra WP11; passkey-godkjenning på web gir samme bundle-format. «trukket» i rødt (avvik i images/README.md) | test.ge.approve-web, test.skeleton.no-unreachable-elements, test.skeleton.purpose-actions-reachable, test.gui.load-time | Claude |
| WP13 | member-view | CellScaffold | «Mine roller» etter `skeleton/min-rolle.v1.json`; tekst fra VC-en, ikke lokal etikett | test.gui.parity (web) | Claude |
| WP14 | approve (Binding), owner-surface, member-view | Binding | Godkjenning med Face ID via `Identity.sign(data:)`; flatene i Binding fra samme skjelett | test.ge.approve-binding, test.gui.parity (Binding) | Claude lager patch/PR; Mac bygger og tester |
| WP15 | not-uio | CellScaffold | Profil-JSON uten `legalIdentifier`, evidens = lenke til gruppas side, visningsnavn «Informasjonssystemer (Ifi, UiO)», `entity:ifi-informasjonssystemer` | test.ge.profile-honest | Claude |
| WP16 | consumers | CellProtocolDocuments | Lenker i CPD #44, #45 og Mistral-spesifikasjonen til vilkåret (de to første er alt gjort av trådene) | test.ge.consumers-linked | Claude |
| WP17 | — (release) | CellProtocol, CellScaffold, Binding | CellProtocol-tag på Mac etter at Binding er bygd mot kandidaten; flytt pins i CellScaffold og Binding; FORESPOERSEL til HAVEN-Deploy | test.build, test.regression | Kjetil (merge/tag), Mac, Claude (forespørsel) |
| WP18 | root | staging | Etter deploy: Kjetil oppretter gruppa (v1), gir en testkonto studentrollen, testkontoen kommer inn i en celle med vilkåret, fremmed nektes; web og Binding | test.ge.e2e, test.gui.parity | Kjetil + Claude |
| WP19 | owner-onboarding (ekte) | staging | Når Petter har konto: Kjetil foreslår og godkjenner v2. Claude kontakter ikke Petter | test.ge.policy-chain på staging | Kjetil |
| WP20 | — | CellProtocol Docs, Book 07 | `Organization_Entities_and_Group_Signing_NO.md` sier hva som er bygd; Book 07: Informasjonssystemer er organisasjonsentitet, ikke scaffold-administrator | test.docs-updated | Claude |

## Pakkeartefakter

- `contract/`: kontrakt for `OrganizationVaultCell` og gruppecellen med fixtures (WP4, WP11) — `pkg.std.cell-contract`.
- `dataflow.md` (WP4): eier → forslag → hvelv → rolle-VC → student → celle med vilkår → statusspeil.
- TESTRESULT.md og ACCEPT.md bygges fra bevisfilene, og en uavhengig tråd kontrollerer dem før G3.

<a id="dataflow"></a>
## Dataflyt (kort)

| Kant | Fra → til | Keypath / event | Kontrakt |
|---|---|---|---|
| 1 | Eier → gruppecelle | `group.proposal.create` | WP11 |
| 2 | Eier → gruppecelle | `group.proposal.approve` (signert godkjenning) | WP4 |
| 3 | Gruppecelle → hvelv | `vault.sign` med `ApprovalBundle` | WP4 |
| 4 | Hvelv → mottaker | rolle-VC (`role.issue`) | WP5 |
| 5 | Gruppecelle → node | statusliste (`role.status.publish`) | WP6 |
| 6 | Student → celle | Agreement med `ProvedClaimCondition` | WP7 |

## Risiko og rekkefølge

- WP1–WP7 er ren CellBase og blokkerer alt annet. WP8–WP10 kan gå parallelt med WP11–WP13 når fixturene finnes.
- CellApple bygges ikke i Linux-CI. Hver CellProtocol-endring bygges i Binding på Mac før tag (2026.9.12 ble trukket av den grunn).
- Full CellScaffold-app bygger ikke i skyriggen; draft-PR-ens Linux-CI er byggesjekken, og den er ikke grønn før den er grønn.
- Petter er ingen forutsetning før WP19.
