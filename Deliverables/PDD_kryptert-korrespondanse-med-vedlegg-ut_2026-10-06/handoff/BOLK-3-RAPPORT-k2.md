# Bolk 3 og 5 — k2 stoppet ved protokollgrensen

Klientens lille broport er rettet og grønn på den dokumenterte, direkte autentiserte Native-ruten. De gjennomgåtte vault-cache- og shutdown-patchene er tatt inn. CP er pinnet til PR #63-hodet 3d6be30a108c72aeb3ce632a8b08f49ca3d9586c. Den samlede leveransen er ikke ferdig eller grønn. Ingen commit, push, ny PR, merge, deploy, sending eller installer er gjort. K1-rapporten er bevart som separat kopi.

| Krav | Test | Utfall | Bevis |
|---|---|---|---|
| A5: autentisert bro og push etter initial state | Opprinnelig c150 med samtlige asserter beholdt; serverfixture følger Native-topologien; ny publisher-ruteprøve | 2 bestått, 0 feil; konvolutten åpnes direkte uten polling. Ikke full produktakseptanse | b-k2-native-adapter-20261008 |
| Bufret kanal bundet til opprinnelig vault | Detached og fremmed vault mot etablert kanal | Begge avvist; ingen lånt privat kapabilitet | Samme broport |
| Shutdown, sen factory og cache-retirement | Opprinnelige negative lifetime-assert­er | Bestod; lukket kanal og nye operasjoner avvises, sen factory pensjoneres, feilet factory kan prøves på nytt | Samme broport |
| Sammenligning med native fixture | Samme klient-proof-vault over direkte autentisert gate | Push bestod uten forsinkelse. Multipleksdiagnose rød; separat SET-svarforsinkelse gjorde diagnosekopien grønn. Ingen slik forsinkelse i produktet | b-k2-bridge-diagnose-20261008; b-k2-response-race-r2-20261008; b-k2-direct-native-r3-20261008 |
| A1: samme klient for eier og invitert | Lokal eierprøve og faktisk to-profil socketprøve | Lokal prøve grønn; socketprøven nådde tekst og 1 100 037 byte begge veier | c-k2-native-baseline-full-r3-20261008 |
| A7: Flow, historikk og gjenkobling | Socketprøve og lokale recovery-prøver | Push og overføring nådd; gjenkobling stoppet på lokal vedleggscache-lås. Automatisk gjenkobling ikke levert | Samme fullport |
| C2/D3: native signering og fersk autentisering | Eksisterende signerprøver fra k1; menu-core-bundle i k2-baseline | Bundle 60/0, inkludert signerprøvene. Ekte Touch ID/passord og integrert kort ikke prøvd | Samme fullport; k1s native red/grønn |
| C1/C2: lenke, forespørsel, kode og kort under Trenger deg | Bevarte native utkast | Ikke integrert eller vist som samlet flyt. Ingen nye GUI-bevis | K1-overleveringen |
| C3: eierstyrt fornyelse etter utløp og tilbakekall | P4-kontrakt lest; klientens socketprøve stoppet før fornyelse | Protokollens leverte bevis erstatter ikke klientbevis. Klientens requestID-/fornyelsesflyt ikke levert | P4-overleveringen; socketprøven |
| D4: ingen verdier i diagnostikk | Lokale personvernprøver | Avgrensede prøver grønne; komplett produkt-/GUI-loggport ikke vist | K2-baseline |
| Alle eksisterende tester | Full baseline: fem bundler 310/0; correspondence-bundle 45 tester med 10 issues | Rød. Midlertidig signed-fixture-oppsett endret legacy-premissen og ble tatt ut igjen. Senere original hosted-fixture med public-key-lookup: 9/10 grønne, én reell CP-kompatibilitetsfeil | c-k2-native-baseline-full-r3-20261008; b-k2-legacy-hosted-20261008 |
| CP-grense: separat signert eieravtale | Eksisterende S54ResolverDeniesExternalInvitationAndAcceptsSeparateOwnerAgreement | Gyldig separat eieravtale blir avvist: faktisk denied, forventet unchanged. Avgjørelsen ligger i CP inviteIdentities | b-k2-legacy-hosted-20261008 |
| Lokal full formålsprøve mot PR #286 | Join, tre vaults, begge retninger, Flow, utløp/fornyelse/revoke | Ikke kjørt som samlet produktprøve mot den faktiske verten. Lokale socketfixtures teller ikke som PR286-vertakseptanse | Ingen slikt bevis |
| Commit, kladd-PR og CI | Tillatt når fullport grønn | Ikke utført; grønn port mangler | Ingen ny PR eller CI |
| Bolk 5: ren eksport, universal2, notarisation og staple | Bare etter alle grønne porter | Ikke bygget | Ingen pakke, SHA-256, spctl-, lipo- eller manifestbevis |

## Stoppgrunn og nødvendig oppstrøms avklaring

Den gjenværende hosted-testen beholder hele forventningen: ordinær ekstern invitasjon avvises, mens en særskilt signert eieravtale skal gi den eksisterende, idempotente eieroperasjonen. På p4 avviser inviteIdentities alle requestere med annen UUID enn selve celleeieren, også den særskilt autoriserte eierdelegaten. Dette kan ikke rettes i HavenAgentD: prøven går direkte gjennom CellProtocol-resolveren til CellProtocol-cellen.

For å bevare den eksisterende kontrakten må CP gjøre denne operasjonen i samsvar med den verifiserte, eksakte eieravtalen uten å gi ordinære medlemmer invitasjonsrett. Alternativet er en uttrykkelig beslutning om at den tidligere kontrakten skal endres og testen oppdateres. K2 har ikke gjort noen av delene, ikke svekket den røde assert­en og ikke endret CP eller CellScaffold. Oppdragets grense utløser stopp her.

En mulig konflikt mellom kortvarige operasjonsbevis og aktive feed-bevis er kildebasert diagnose, ikke endelig instrumentert rotårsak. Den lille Native-porten er faktisk grønn. De senere signeringsmeldingene ved nedkobling må ikke omtales som bevis for at aktiv Flow feilet: socketprøven leverte data, og den faktiske exceptionen var vedleggscache-låsen.

## PR #28 og #30

#28: behold k1s anbefaling om bare CI-fasevakten og den direkte Swift Testing-kjøreren i denne kandidaten, og skill ut/rebase provenance-funksjonen. Helperne er tatt inn; ingen merge eller lukking. Historisk grønn CI på inventarert 5cf3531 er ikke en ny k2-CI-kontroll.

#30: behold anbefalingen om rebase på verifiserte fasehelpere og ny full CI før merge. Tidligere inventarert 653fb87 stoppet på ytre tidsgrense; ingen ny rotårsak eller grønn CI hevdes. Ikke lukk på dette beviset. Ingen endring eller merge.

## Ikke vist

Integrert admin- og mottakerflate, ekte LAContext-godkjenning i produktflyten, agentregistrering/discovery, automatisk gjenkobling, full join/result/accept og eierstyrt fornyelse etter utløp, samlet tilbakekall, vedleggenes komplette metadata-/modus-/restore-port, daemon smoke, GUI-akseptanse, full grønn port, PR/CI og universal installasjon.

Første pakkes beslutning om dagens nøkkellagring står ved lag: en prosess som kjører som samme bruker kan ha nøkkeltilgang. Appens ferske LAContext er ikke separat Keychain-håndhevet nøkkelgruppe. Ingen produksjons-debug-bypass er lagt til.

Pakke og checksum finnes ikke. spctl, lipo, Developer ID-signering, notarisation, staple og manifest etter staple er ikke kjørt. Minimum macOS 13 er bare dagens manifestkrav; Intel, Tahoe og eldre systemer er ikke installasjonstestet.

STATUS: STOPPET — fullport krever avklaring eller retting i CellProtocol for eksisterende separat eieravtale; CP-endringer er utenfor jobben.
