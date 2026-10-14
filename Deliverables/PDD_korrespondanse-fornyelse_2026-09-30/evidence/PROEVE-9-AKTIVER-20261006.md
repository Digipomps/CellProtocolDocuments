== proev-fornyelse: aktiver, 2026-10-07T10:01:03Z ==
ok  forny-haven-tilgang.sh har sjekksummen som er ventet (e4ca57eddda23736378ffcdefcb052ebfbfb8dceda3d02eca7205e39990c7438)
ok  sim-a: klienten fra pakken 08.09 (den Vegar fikk)
ok  sim-b: klienten som er installert her fra pilotpakken
-- sim-a
   forny-haven-tilgang.sh aktiver sim-a ga kode 0 og skrev:
      Tilgangen er på plass, og tjeneren godtar den. Den gjelder til 2026-11-05T07:13:10.810Z.
      Start Claude eller Codex på nytt nå. Meldingsverktøyet leser tilgangen bare når det starter,
      så et som alt kjører, bruker den gamle.
   ok  profilen har et nytt tilgangsbevis, til 2026-11-05T07:13:10.810Z, med samme enhet (84db9305b8b0), identitet og nøkkel som før
-- sim-b
   forny-haven-tilgang.sh aktiver sim-b ga kode 0 og skrev:
      Tilgangen er på plass, og tjeneren godtar den. Den gjelder til 2026-11-05T07:13:10.810Z.
      Start Claude eller Codex på nytt nå. Meldingsverktøyet leser tilgangen bare når det starter,
      så et som alt kjører, bruker den gamle.
   ok  profilen har et nytt tilgangsbevis, til 2026-11-05T07:13:10.810Z, med samme enhet (64c358cc0b63), identitet og nøkkel som før
ok  begge har fått nytt tilgangsbevis, og tjeneren godtar dem
   sim-a -> sim-b: sendt (sent)
   sim-b: meldingen står i innboksen
   sim-b: lest, og innholdet er det som ble sendt
   sim-b: kvittert, og kvitteringen står i innboksen
   sim-b -> sim-a: sendt (sent)
   sim-a: meldingen står i innboksen
   sim-a: lest, og innholdet er det som ble sendt
   sim-a: kvittert, og kvitteringen står i innboksen
ok  en melding hver vei er sendt, listet, lest og kvittert
PRØVEN ER GRØNN: forny-haven-tilgang.sh fornyet tilgangen for begge prøveidentitetene mot staging,
tjeneren godtar de nye tilgangsbevisene, og meldinger går begge veier etterpå.
sim-a: klienten fra pakken 08.09 (den Vegar fikk). sim-b: klienten som er installert her fra pilotpakken.
Prøven sier ikke noe om hva tjeneren har lagret for Vegar og Victoria, eller om klientene på deres maskiner.
