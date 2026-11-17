# Fabel: etterkontroll av utsettingen 30.09, tillegget til koordineringsfila, svaret til Vegar og valget om rekkefølge

Etterkontroll 02.10.2026 av en uavhengig Claude-tråd («Fabel»). Teksten under er Fabels svar, uendret.

---

# Fabels etterkontroll 02.10

**1. Rettelsene.** Tre «må»-punkter er rettet, A1 er delvis rettet, og «bør»-punktene er rettet med én nyanse.
- K4/K7: rettet — diffene er skilt [belagt: E7:3-12], d83d9f6b er PR 277s hode [belagt: E7:30], K4 omformulert [belagt: KT:12; E7:14-15].
- A0: rettet som fil [belagt: A0:5-9]; innholdet i pkt. 4.
- Vegar-brevet: rettet — løftet borte [belagt: V2:16], setup-forbud [belagt: V2:15], `identity` verifisert [belagt: E7:26-27], grenanklagen borte [belagt: V2:20].
- A1: delvis — én rad pluss avsnitt, ikke hel fil [belagt: RAD:1; E7:36-37], men hvem som skriver det inn, og hvordan [ikke belagt]; hendelse på HD-0141 mangler [ikke belagt; kanalen: E6:75-86].
- Bør: HD-0006, ett claimvindu, målte steg [belagt: KT:16]; K3-flater [belagt: KT:8]; K6/K8-absoluttene er ikke gjentatt; køtråden får K2, HD-0108-klassen, løperen og skriptet som mangler [belagt: KT:5, 9, 18, 20]. Nyanse: «minst to» omstarter — bevisene gir tre [belagt: E2:30; E2:35-37; E3:35].

**2. KOORDINERING-tillegget.** Nøkternt skrevet, men fire påstander er sterkere enn bevisene, og køen og HD-0141s eier mangler noe.
- Sterkere: «CI grønn» — merge-sjekken er grønn, image-bygget pågår, hodet er d83d9f6b [belagt: E7:30; KT:14]. «Victoria er ute» — målt er bare `recipient_not_allowed` [belagt: E7:23], som også kommer uten noen tilgang; 08.09-settets tilganger går ut 08.10 [belagt: E3:33, E3:36]. Skillet avgjør om hennes enhets-ID trengs: kravet gjelder bare når en tilgang finnes [belagt: E1:12-14]. «Én commit» [ikke belagt]. «Tabellen øverst» har ingen staging-SHA [belagt: E5:224]; feilen står i ryddelisten og STAGING-2026.9.3.md [belagt: E5:281; E4:69; E6:88].
- Mangler for køen: en uttrykkelig bønn om å holde 2026.9.4 unna staging til Kjetils svar står — køens plan utløses av nøyaktig HD-0141-frigivelsen [belagt: E6:81; E5:222-224]; at `sha-415ea3d2`, rullbakcontaineren og 30.09-bevisene må inn i behold-listen [belagt: E4:68-73; E2:25, 33]; at jobbloggene (bevisene) ligger under `.tmp-clang-module-cache` og må flyttes før Mac-rydding [belagt: E4:141]; at HD-0006 eies av Kjetil, står HANDOFF_REQUIRED og foreskriver `--env-only`, ikke cutover-skriptet [belagt: E6:65-70; E3:35].
- Mangler for HD-0141s eier: deployen kjørte manifest-provisjonering mot `/etc/haven/…/runtime-identity-manifest.v2.json`, som er «ikke frigitt» [belagt: E2:18, 27; E4:77]; KT:8 nevner bare sikkerhetskopien.
- Kan misforstås: «leveres hit» — køen krever skript under `HAVEN-Deploy/_handoff/`, promptfil og `.job` via mv [belagt: E5:38-39, 140-145, 235].

**3. Vegar-brevet.** Det lover ikke mer enn det kan holde og stemmer med E7, men mangler kanalen for etter 08.10 og har tre småfeil.
- Riktig: `identity` og feltene [belagt: E7:26-27; V2:11]; principal/enhet/nøkkel [belagt: E1:12-14; E3:39]; setup-forbudet [belagt: E3:28-30]; «noen minutter» (14 min) [belagt: E2:38; E3:39]; PDD-valget [belagt: E7:32-33].
- Mangler: etter 08.10 feiler sending til Vegar med `recipient_not_allowed` [belagt: E1:32-34; BRIEF:9], så «jeg sier fra når invitasjonen er på plass» kan ikke leveres i brevets egen kanal. Avtal e-post eller annet nå.
- Småfeil: «legger bort beviset» — `setup` overskriver profilen med `accessCredential = nil` [belagt: E3:28]; «bygger mot 2026.9.3» er ny og [ikke belagt]; `identity` er målt bare på Kjetils installasjon [belagt: E7:26] — gi reservevei. «Write-a-skill … 29.09» fortsatt [ikke belagt].
- «Kan bli etter 08.10»: med dagens staging er det bare etter [belagt: E7:9-10]; før krever A eller D.

**4. A0.** B er riktig, C har en umulig «nå», A er forsvarlig men skjuler at den opphever Kjetils egen bestilling og køens plan; et fjerde valg finnes.
- A setter til side ordren «Be Codex utføre» (tag 2026.9.4, image, staging når HD-0141 slipper) [belagt: E6:81], reservasjonen [belagt: E5:224] og 2026.9.5-vilkårene som forutsetter 2026.9.4 i staging og prodsvar [belagt: E4:122-127]. 2026.9.4 verifiseres aldri som egen SHA; prodspørsmålet flytter [belagt: E5:225]. Releaseorden eies av køtråden [belagt: E5:210] — spør den. Sjudagersvinduet har bare enhetstester [belagt: E3:41-42]; 415ea3d2 er live-testet [belagt: E3:39]. «2,5 timer» [ikke belagt]. Victoria-kolonnen forutsetter en enhets-ID-vei som ikke finnes [ikke belagt]. Portene HD-0141, 40 GiB og HD-0150 gjelder også A [belagt: E5:222, 224].
- B: riktig; «tidligst 2026.9.5» betyr vilkår (a)–(e) [belagt: E4:122-127] — åpen ventetid, si det.
- C: «nå» krever claim mens HD-0141 står [belagt: E5:234, 226]; invitasjonen må leve forbi 08.10 (08.09-settet varte sju dager) [belagt: E3:33; styrbarhet ikke belagt]; Victoria senere = ny cutover [belagt: E3:34].
- D: 2026.9.4 først som bestilt, så en liten utgivelse med bare PR 277 oppå, til staging straks 2026.9.4 er `COMMITTED_VERIFIED`, invitasjonene i samme vindu. Pris: to image-bygg, to vinduer, fravik fra «staging skal ikke skifte mens prodspørsmålet er åpent» [belagt: E4:123]. Gevinst: 2026.9.4 verifiseres, ordren står, Vegar kan nå vinduet før 08.10 om portene åpner. Uansett valg kan PR 277 merges nå uten å røre 2026.9.4 [belagt: E5:233; E4:120].
- A0 sier ikke hva Kjetil selv gjør per valg.

**Må fortsatt rettes**
1. KT: hold-bønn for 2026.9.4; behold-listen; `/etc/haven`-manifestet; hendelse på HD-0141.
2. KT/A0: «Victoria er ute» → «`recipient_not_allowed`; utløpt eller aldri aktiv er uavklart» — avklar før enhets-ID kreves.
3. KT/A0: «CI grønn» → merge-sjekk grønn, hode d83d9f6b, image pågår.
4. V2: kanal utenom korrespondansen; «overskriver»; stryk «mot 2026.9.3»; reservevei for `identity`.
5. A0: skriv A-kostnaden (ordren til Codex, køens plan); rett C «nå»; legg inn D; hva Kjetil gjør per valg.
6. A1: fastslå at tillegget appendes på Mac-en eller av køtråden, med md5-sjekk.

**Kan stå**
- KT:3, 5, 7, 12, 18 og RAD (legg til klokkeslett); KT:16 og 20 med tilleggene i pkt. 2.
- V2: `identity`-linja, setup-forbudet, «principal, profil, maskin og nøkkel», bcd45de-avsnittet.
- A0: faktalinja, B-raden; anbefalingen A når kostnaden står.
- E7-målingene for K4, K7 og K9.

(Forkortelser: KT = KOORDINERING-tillegg-20261002.md, V2 = VEGAR-svar-utkast-v2.md, A0 = A0-rekkefolge-valg.md, RAD = RAD-koordinert-20261002.txt; alle i scratchpad/pdd-korr/handoff/. E1–E7 og BRIEF i scratchpad/panel-korr/. Ingen filer er endret, opprettet eller slettet; ingen nettverk eller maskintilgang brukt.)
