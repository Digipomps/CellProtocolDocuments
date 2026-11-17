== proev-fornyelse: setup, 2026-10-06T21:11:06Z ==
ok  forny-haven-tilgang.sh har sjekksummen som er ventet (e4ca57eddda23736378ffcdefcb052ebfbfb8dceda3d02eca7205e39990c7438)
ok  sim-a: klienten fra pakken 08.09 (den Vegar fikk)
ok  sim-b: klienten som er installert her fra pilotpakken
-- sim-a
   ok  invitasjonen er hentet fra staging: principal sim-torrkjoring-a, enhets-ID i fila: nei, 8 felt
   forny-haven-tilgang.sh ga kode 0 og skrev:
      Klient:      /Users/kjetil/Build/Digipomps/HAVEN/korrespondanse-privat-20261006/pakkebin/sep/haven-correspondence-mcp
      Invitasjon:  /Users/kjetil/Build/Digipomps/HAVEN/korrespondanse-privat-20261006/arbeid/nedlastet/haven-sim-a-invite.json
      Profil:      sim-a (sim-torrkjoring-a)
      Tilgang nå:  gjelder til 2026-10-08T13:03:23.640Z
      
      Forespørselen er sendt og venter på Kjetil (access-request-<tatt ut>).
      Si fra til ham nå. Forespørselen står i høyst 24 timer.
      Når han har godkjent, kjører du:
          bash "/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/HD-0006/forny-haven-tilgang.sh" aktiver sim-a
      En kopi av profilen slik den var, ligger i /Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence/sim-a/profile.json.foer-fornyelse-20261006T211106Z. La den ligge.
   ok  profilen venter på godkjenning, med samme enhet (84db9305b8b0), identitet og nøkkel som før
-- sim-b
   ok  invitasjonen er hentet fra staging: principal sim-torrkjoring-b, enhets-ID i fila: nei, 8 felt
   forny-haven-tilgang.sh ga kode 0 og skrev:
      Klient:      /Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence/bin/haven-correspondence-mcp
      Invitasjon:  /Users/kjetil/Build/Digipomps/HAVEN/korrespondanse-privat-20261006/arbeid/nedlastet/haven-sim-b-invite.json
      Profil:      sim-b (sim-torrkjoring-b)
      Tilgang nå:  gjelder til 2026-10-08T13:03:23.640Z
      
      Forespørselen er sendt og venter på Kjetil (access-request-<tatt ut>).
      Si fra til ham nå. Forespørselen står i høyst 24 timer.
      Når han har godkjent, kjører du:
          bash "/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/HD-0006/forny-haven-tilgang.sh" aktiver sim-b
      En kopi av profilen slik den var, ligger i /Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence/sim-b/profile.json.foer-fornyelse-20261006T211107Z. La den ligge.
   ok  profilen venter på godkjenning, med samme enhet (64c358cc0b63), identitet og nøkkel som før
2 av 2 forespørsler venter på Kjetil, som må godkjenne innen 24 timer: https://staging.haven.digipomps.org/admin/funding
Etter godkjenningen kjøres fasen aktiver.
