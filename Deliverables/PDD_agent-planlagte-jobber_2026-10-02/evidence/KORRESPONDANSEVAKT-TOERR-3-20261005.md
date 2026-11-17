== omslag: korrespondansevakten, toerr, 2026-10-05T15:02:51Z ==
ok  de3611ee7c89b8b59d2bcaccf893868bb8a5e2c9f442891dd4342612e9696824  Scripts/install-scheduled-tasks.sh
ok  b9efd187f5d6a00260c2ae16273da70ffe95a966bee4d6ccafe53b1a176403e5  Scripts/scheduled/installer.py
ok  316186c959a0822a908220bd7dfba5ea983d89432b197666036f65f59e3fcff3  Scripts/scheduled/korrespondanse_vakt.py
== Korrespondansevakten: tørrkjøring, ingenting endres ==
tid: 2026-10-05T15:02:51Z
1. Python og selvtest
   /usr/bin/python3 er 3.9.6
   SELVTEST OK 128 kontroller
2. Sjekksummer og korrespondanseklienten
   program   316186c959a0822a908220bd7dfba5ea983d89432b197666036f65f59e3fcff3  Scripts/scheduled/korrespondanse_vakt.py
   klient    9b7a86df422bbbbf2a342635c2d7c22234dfba7ac8b8bb2bf1405c74ccfa696c  /Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence/bin/haven-correspondence-mcp
   klienten tar --root: ja
   klienten svarte for kjetil-vegar-d: 4 verktøy (correspondence.list_inbox, correspondence.read_message, correspondence.send_message, correspondence.ack_message)
   innboksverktøyet heter correspondence.list_inbox, og krever ingen argumenter
   ingen innboks ble lest
3. Kandidat
   config.json nå: 8361c1cd56daa84d1e13ec00a419bff365f29e12c175becea004ee07667373e8
   lagt til i kandidaten: 2 faste programmer og 2 hendelser, firstFireAt 2026-10-05T15:03:07Z
4. Validering med agenten som er installert
   haven-agentd validate-config: ok
   haven-agentd schedule-list: ok, 3 hendelser (<id>: scheduled, korrespondanse-sjekk: scheduled, korrespondanse-frist: scheduled)
   haven-agentd-scheduler validate-config: ok
   haven-agentd-scheduler schedule-list: ok, 3 hendelser (<id>: scheduled, korrespondanse-sjekk: scheduled, korrespondanse-frist: scheduled)
   hver hendelse peker på et fast program i policyen: ok
   den ekte tilstandsfila er urørt: ok
5. Forskjellen i config.json (tokener er byttet med <skjult>)
   --- config.json nå
   +++ config.json etter
   @@ -81,4 +81,54 @@
            "executablePath": "/Users/kjetil/Library/Application Support/HAVENAgent/bin/losen-probe.sh",
            "id": "losen-probe",
   +        "requiresUserSession": false
   +      },
   +      {
   +        "arguments": [
   +          "/Users/kjetil/Library/Application Support/HAVENAgent/bin/korrespondanse_vakt.py",
   +          "sjekk",
   +          "--profil",
   +          "kjetil-vegar-d",
   +          "--profil",
   +          "kjetil-d",
   +          "--navn",
   +          "vegar-local-agent=Vegar",
   +          "--navn",
   +          "victoria-lille-robot=Victoria",
   +          "--navn",
   +          "pilot-simulation-d=pilotsimuleringen",
   +          "--klient",
   +          "/Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence/bin/haven-correspondence-mcp",
   +          "--klientrot",
   +          "/Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence",
   +          "--markorer",
   +          "/Users/kjetil/Library/Application Support/HAVENAgent/Inbox/CorrespondenceWaiting",
   +          "--tilstand",
   +          "/Users/kjetil/Library/Application Support/HAVENAgent/State/ScheduledTasks"
   +        ],
   +        "description": "Lister innboksen for to korrespondanseprofiler og skriver én markør per avsender med ulest post. Leser ikke innhold, kvitterer ikke og sender ingenting.",
   +        "executablePath": "/usr/bin/python3",
   +        "id": "korrespondanse-sjekk",
   +        "requiresUserSession": true
   +      },
   +      {
   +        "arguments": [
   +          "/Users/kjetil/Library/Application Support/HAVENAgent/bin/korrespondanse_vakt.py",
   +          "frist",
   +          "--profil",
   +          "kjetil-vegar-d",
   +          "--profil",
   +          "kjetil-d",
   +          "--klientrot",
   +          "/Users/kjetil/Library/Application Support/HAVEN/AssistantCorrespondence",
   +          "--dager",
   +          "7",
   +          "--markorer",
   +          "/Users/kjetil/Library/Application Support/HAVENAgent/Inbox/CorrespondenceWaiting",
   +          "--tilstand",
   +          "/Users/kjetil/Library/Application Support/HAVENAgent/State/ScheduledTasks"
   +        ],
   +        "description": "Leser når tilgangsbeviset i to korrespondanseprofiler går ut, og skriver en markør når det er under åtte døgn igjen. Bruker ikke nettet.",
   +        "executablePath": "/usr/bin/python3",
   +        "id": "korrespondanse-frist",
            "requiresUserSession": false
          }
   @@ -323,4 +373,26 @@
          "id": "<skjult>",
          "repeatMode": "once"
   +    },
   +    {
   +      "action": {
   +        "arguments": {},
   +        "id": "korrespondanse-sjekk",
   +        "kind": "localTask"
   +      },
   +      "firstFireAt": "2026-10-05T15:03:07Z",
   +      "id": "korrespondanse-sjekk",
   +      "intervalSeconds": 1800,
   +      "repeatMode": "untilStopped"
   +    },
   +    {
   +      "action": {
   +        "arguments": {},
   +        "id": "korrespondanse-frist",
   +        "kind": "localTask"
   +      },
   +      "firstFireAt": "2026-10-05T15:03:07Z",
   +      "id": "korrespondanse-frist",
   +      "intervalSeconds": 86400,
   +      "repeatMode": "untilStopped"
        }
      ],
6. Stopper her. Ingenting er endret.
   For å legge inn: «utfoer», med HAVEN_FORVENTET_CONFIG_SHA256=8361c1cd56daa84d1e13ec00a419bff365f29e12c175becea004ee07667373e8
   og programmet med sjekksum 316186c959a0822a908220bd7dfba5ea983d89432b197666036f65f59e3fcff3
