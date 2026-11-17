# k18 — én billett per vedleggsoverføring

Arbeidsrapport 2026-10-13. Kandidaten er implementert lokalt; sluttstatus og PR/CI fylles etter verifikasjon. Ingen merge, tag, deploy, installerbygg eller vertsendring.

## Mandat og grunnlag

Kjetils bestilling gir mandat til implementering, egne tester, uavhengig kontroll og to kladd-PR-er. CP origin/main ble hentet og kontrollert: `34cecefcb78e4e3775c116a50b0d96a32c1e2f9c`, squash av #67. Ny CP-gren `codex/k18-attachment-tickets` fra denne revisjonen. Klientgrenen med samme navn bygger på #36 etter k17s repinn: `8ae4c276ecedb26c784a19274756906f7415435b`. Dette beholder den allerede testede retry-koden og unngår å rekonstruere #36 på eldre main. Klientens kladd stables mot #36-grenen; #32/#36 er fortsatt landingsforutsetninger.

Arbeidstrær under HAVEN-roten: `_worktrees/k18/CellProtocol` og `_worktrees/k18/HavenAgentD`, begge låst mot prune. Primærutsjekkenes urelaterte endringer er ikke brukt eller endret.

## Kort design

- Opt-in `requestTransferTicket: true` på prepare for opplasting og metadata/transfer-start for nedlasting. Metadata-start krever fetch-grant. Vanlig `authorizeAttachment` med nøkkelbevis utføres én gang; den påfølgende kontraktkontrollen bruker den autoritative, allerede verifiserte kontraktslisten.
- 32 kryptografisk tilfeldige byte som ugjennomsiktig base64. Bare serverens minne inneholder registeret. Binding til requester UUID + signeringsnøkkel, celle, avsender, melding, Agreement, vedleggs-ID, nøyaktig upload/fetch-handling og fanget autentisert kanalgenerasjon.
- 120 s inaktivitet, forlenget først etter en vellykket bit, med 600 s absolutt grense. Både veggklokke og monoton klokke håndhever fristen. Dette tåler kortvarige pauser uten å gi en ubegrenset billett. Kanalens kortere levetid gjelder fortsatt.
- Åtte samtidige billetter per requester UUID/nøkkel i hver CorrespondenceCell og 1024 totalt i cellen. Utløpte poster ryddes før utstedelse/bruk. Ingen påstand om global kvote på tvers av alle relasjonsceller.
- Hver bit kontrollerer gjeldende medlemskap, nøkkel, grant og tidsgrenser uten ny signatur. En synkron sperre før medlemsmutasjon ugyldiggjør billettene før auditor endres. Lagringseffekten skjer innenfor medlems-/kanalsperren; svar kontrolleres igjen etter actor-hoppet. Hendelser publiseres etter at låsene er sluppet.
- Revoke, medlems-/kontraktsendring, siste bit, utløp og prosessrestart gjør billetten ubrukelig. Generasjonsteller og opptelling av samtidige revoke-operasjoner sperrer konkurrerende utstedelse. Mislykket utstedelse etter prepare tilbakekaller den opprettede lagringsposten.
- Kun fire eksakte SET-innganger tolker billettfeltene. En oppgitt ugyldig billett feiler uten overgang til vanlig bevis. Klient uten billett beholder gammel flyt; ny klient godtar gammel vert som mangler det valgfrie svarfeltet.
- Klienten lagrer ikke billetter varig og fjerner dem før publisering, kvittering og revoke. Forbindelsesbytte fornyer ikke billetten; avbrutt overføring må startes på nytt.

## Sikkerhet og avgrensning

Signeringspolicyen 12/60 s, #67s typede backpressure, lagringskvoter, diskreserve, bytegrenser og chunk-validering er uendret. Ingen generell proof-cache eller utvidet resolver-grant er innført. Lokal Resolver.set har fremdeles sin egen preflight; ytelseskravet må måles på broens direkte target.set-rute som produksjonsklienten bruker.

In-process-kall har ingen fysisk kanal og bruker en avgrenset bearer-billett med matchende identitetsdescriptor etter ordinær autorisert utstedelse. Fjernbruk via Bridge krever den fangede autentiserte kanalen. Billettene er hemmeligheter, ikke selvbærende autorisasjonsdokumenter, og inngår ikke i events, vedleggsenvelopen eller vedvarende cacheposter.

Uavhengig agent gjorde kildekontroll, uten å bygge eller endre produksjonskode. Den fant og fikk rettet feil knyttet til kanalfangst, callback under kanallås, opprydding etter avvist billett og medlemsmutasjonens actor-gap. Sluttkontrollen fant ingen gjenværende blokkerende kildefunn. Dette er avgrenset kildekontroll, ikke sikkerhetssertifisering. Rapport: `HAVEN-Deploy/_handoff/KORR-UT/k18/INDEPENDENT-REVIEW.md`.

## Tester og målinger

Alle identiteter og filer er syntetiske. Swift 6.4 / Xcode 27 på lokal macOS. Bounded-runner med to jobber, ordinær diskvakt, report-only GC og oppgaveegen administrert cacherot; ingen delt cacheopprydding. Første SwiftPM-forsøk stoppet fordi nestet sandbox ikke kunne startes. `--disable-sandbox` slo bare av SwiftPMs indre sandbox; kjøresandkassen ble beholdt.

Rød: `testTransferTicketIssuedAtPrepare` på uendret CP main feilet på manglende transferTicket, som forventet. Bevis: `red-cp-r2.log`.

Grønn fokusert: opprinnelige fem billettester bestod. Deretter utvidet til ni: opplasting/nedlasting, feil vedlegg/melding/Agreement/handling/UUID/nøkkel, kapasitetsgrense, utløp og absolutt maks, revoke, medlemsfjerning, siste bit, annen eller tilbakekalt kanal, varig lagring og gammel klient. Den niende holder en allerede kontrollert bit over autoritativ medlemsfjerning før medlemskopien oppdateres; avslag er målt.

Brokommando-testen med 1 100 037 byte, localProtection aktiv: siste kjøring målte eier→medlem opplasting 0,098601 s / nedlasting 0,072301 s; medlem→eier 0,095237 s / 0,072907 s. Nøyaktig ett bevis per prepare/metadata-start + bitsekvens. Handshake, publisering, meldingslesing og receipt er ikke med i disse tallene; separat klienttest teller hele sendAttachment/fetchAttachment over socket.

Full lokal CP-kjøring er forsøkt uten å hoppe over feilede tester. Første kjøring: 1682 tester, 12 hoppet over, tre feil i eksisterende AppleIdentityVaultKeyStorageTests. Feilene er Keychain EPERM / -25291 fra kjøresandkassen, ikke billettasserts. Derfor er den ikke en grønn fullport. Endelig CP-kjøring (`full-cp-final.log`): 1683 tester, 12 hoppet over, samme tre Keychain-feil; 233,094 s for XCTest-suiten. Alle ni billettester bestod. Klientresultat gjenstår her.

## Kildeanker, PR og CI

CP-kandidat: `098c9222ddb79e7c49c81850a8ccf1bcd44a02b8`, [kladd-PR #69](https://github.com/Digipomps/CellProtocol/pull/69), base main. PR-en oppgir eksplisitt at lokal fullport ikke er grønn. Bestillingen om kladd og CI er fulgt med miljøfeilen synlig; dette er ikke godkjenning for merge.

Kildeanker (relative til CellProtocol):
- `Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift:400`: medlemsmutasjonssperre; `:450`: smal SET-inngang; `:1337`: start/legacy-ruting; `:1457`: per-bit medlemskontroll; `:1480`: utstedelse; `:1504`: bitbruk.
- `Sources/CellBase/Cells/Correspondence/CorrespondenceTransferAuthorization.swift:1`: synkron lagrings-/kanalsperre.
- `Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:1476`, `:1567`, `:1596`, `:2173`, `:2191`: produksjonsmutasjoner som ugyldiggjør billetter.
- `Sources/CellBase/Cells/Bridging/BridgeBase.swift:1383`, `Sources/CellBase/Cells/Bridging/BridgeChannelSession.swift:449`, `Sources/CellBase/Identity/BridgeIdentityVault.swift:33`: eksplisitt kanalfangst.
- `Tests/CellBaseTests/CorrespondenceRelationshipTests.swift:833`: bit som venter mens autoritativ medlemsfjerning pågår.

Klientens commit, sluttmålinger og CI-status fylles ved sluttkontroll.

## Læring

`L-2026-10-13-overforingsbilletter-ma-bindes-til-kommandoens` er fanget og anvendt i `CellScaffold/.claude/skills/cellprotocol-identity-capability-security/SKILL.md`. Synk til hjemmemappens kopier er forsøkt og blokkert av skrivegrensen (EPERM); ikke omgått. Bevis: `learning-sync.log`.

Alle loggnavn ovenfor er relative til `HAVEN-Deploy/_handoff/KORR-UT/k18/`.

ARBEIDSSTATUS: VERIFIKASJON PÅGÅR
