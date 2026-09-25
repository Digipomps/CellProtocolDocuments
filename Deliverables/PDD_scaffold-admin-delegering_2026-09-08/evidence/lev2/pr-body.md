To ting Kjetil ga ordet for 2026-09-23.

**1. Scaffold-administrator i prod.** Provisjoneringen av representanter for `entity:digipomps` var «bare staging» i både Swift-grensen og operatørskriptet. Staging ble provisjonert i dag (Kjetil og Vegar, `committed_verified`). Nå kan den kjøres i nøyaktig to grenser, hver bundet til sin RP og sin godkjenning (staging: G3 2026-09-11, prod: 2026-09-23). En forespørsel skrevet for det ene miljøet, eller med det andre miljøets godkjenning, avvises før registeret røres.

`scripts/provision-scaffold-administrator-production.sh` er prod-utgaven av staging-skriptet. Prod har databasen (`/app/Database`) og identitetsvaultene (`/app/IdentityVaults`) utenfor `/app/CellsContainer`, så backup og rollback dekker **alle** skrivbare binds, ikke bare CellsContainer.

**2. «Koble til modell» sier hvorfor.** Butler svarte «GuidedOnboardingCell is not available in this Porthole runtime» for tre ulike årsaker, fordi `scopedCellSet` svelger både oppslaget og `set` med `try?`. Prods logg sa ingenting. Nå skilles uregistrert celle, nektet tilgang og avvist steg, hver med egen kode, og årsaken logges.

**Testet mot funksjon og formål:** fokuserte tester grønne (nye: to representanter under én registrering; prod bare innenfor egen grense og godkjenning; tre årsaker gir tre koder; produksjonsveien bruker dem), og det lokale CI-filteret uten nye feil eller avbrudd.

**Ikke med:** rollebevis-patchen for top-up-godkjenning. Den bryter `AdminEntryRemoteBridgeLoopbackTests` og leveres for seg.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011CHU13qBKbb5szsQQo53rW
