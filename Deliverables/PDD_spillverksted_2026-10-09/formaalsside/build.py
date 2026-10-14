import json, os
D = os.path.dirname(os.path.abspath(__file__))
t = json.load(open(os.path.join(D, "tree.json")))
t["analysis"] = {
  "summary": [
    "Ingen spillarbeid fantes fra før. «Sverres spillrom» fra 8. oktober er det eneste, og det er en Claude-side, ikke HAVEN.",
    "HAVEN har det meste av chathjelperen allerede: ruting, forslag med bekreftelse, eskaleringstak, AIGateway og formålsforankring. Det som mangler er at hjelpere kan registreres uten kode, og en kjede fra samtale til forhåndsvisning.",
    "Formål er bare løst koblet til verktøy og GUI-elementer i dag (fritekst og tre ulike vokabularer). Biblioteket må nøkles på purpose://-refs.",
    "Spillmotor: KAPLAY først, Phaser når spillene vokser, bak en adapter så valget kan endres.",
    "Ikke et eget scaffold nå. Brukerlaget spillkode isoleres med sandkasse, og en egen spillvert lages bare hvis målte kriterier slår til.",
    "Publisering krever Kjetils godkjenning per versjon. HAVEN har ingen barne- eller foresattmodell i dag."
  ],
  "loop": [
    ["Forstå", "Ønsket klassifiseres mot formålstreet; bare resten dekomponeres.", "modell for resten"],
    ["Avklar", "Spør bare om det som endrer hva som lages.", ""],
    ["Foreslå", "Plan med verktøy og GUI-elementer fra biblioteket, med forklaring.", "modell"],
    ["Vis", "Forhåndsvisning ved siden av samtalen.", ""],
    ["Bestem", "Brukeren godtar, endrer eller forkaster med et klikk.", ""],
    ["Utfør", "Målcellen sjekker tilgang og lagrer en versjon.", ""],
    ["Lær", "Avvik blir lærdommer og skill-endringer.", ""]
  ],
  "profile": "formålsgren, bibliotek, forhåndsvisningsadapter, tillatte handlinger, tone og alder, eskaleringstak og måletall (andel forslag godtatt uten endring, tid til første forhåndsvisning, avklaringsspørsmål per ønske).",
  "gaps": [
    ["Samtale med språkmodell", "AIGateway (ai.invoke), Butler Chat-ruting, eskaleringstak", "Hjelpere er hardkodet i chatmotoren"],
    ["Vise hvordan det blir", "Porthole-editoren lagrer skjelett uten rekompilering", "Ingen kjede fra chat til forhåndsvisning; ingen sandkasse for spill"],
    ["Formål til verktøy og GUI", "PurposeKnowledgeBase, PurposeDecomposition, ConfigurationCatalog", "Ingen typede koblinger; tre vokabularer; katalogen matcher på fritekst"],
    ["Bibliotek / RAG", "CommonsLibrarian, kapabilitetsindeksen, RAG-celler (ordsøk)", "Ingen oppføringer nøklet på formål; ingen vektorsøk"],
    ["Prosjektadministrasjon", "ProjectPortfolio, WorkItem, Developer Workbench", "Barnespråk og versjoner per spill"],
    ["Publisering", "/pub (Publication), personlig side, Butterpop", "Ingen vei for brukerlaget JS; ingen foresattgodkjenning"],
    ["Godkjenning", "Spesifisert i PDD_godkjenninger-i-arbeidsbenken", "Ikke bygget; denne siden er midlertidig"]
  ],
  "engineVerdict": "KAPLAY først, fordi koden er kort og lesbar for et barn og kjører i nettleseren uten byggesteg. Phaser er neste trinn for større spill. Valget bekreftes ved at hjelperen lager fem småspill i hver motor før planen (G2).",
  "engine": [
    ["Kriterium", "KAPLAY", "Phaser 4", "Godot", "Scratch", "MakeCode Arcade"],
    ["Kjører i nettleser uten byggesteg", "ja", "ja", "nei, eksport", "ja", "ja, fra makecode.com"],
    ["Lesbar for et barn", "best", "middels", "eget verktøy", "blokker", "blokker, JS, Python"],
    ["Modeller skriver riktig kode", "antatt god, ikke målt", "risiko: mest Phaser 3 i treningsdata", "middels", "—", "ikke målt"],
    ["Kan bygges inn i HAVEN", "ja (MIT)", "ja (MIT)", "tungt", "nei, AGPL siden 2024", "ikke sjekket"],
    ["Vokser med eleven", "mellomstore spill", "store spill", "fullverdig", "begrenset", "begrenset"]
  ],
  "scaffold": "Nei, ikke nå. Arbeidsbenken, hjelperen og biblioteket har samme risiko og deploytakt som resten av CellScaffold, og regelen i Scaffold_Product_Split_Plan er at et eget scaffold bare lages når det er annerledes. Det eneste som skiller seg ut er brukerlaget spillkode. Den isoleres med iframe uten allow-same-origin i forhåndsvisning og CSP sandbox på publiserte spill, som gir spillet et eget opphav uten tilgang til HAVEN-økten. En egen spillvert lages hvis spill trenger lagring per spiller, belaster resten av HAVEN, eller sandkassetesten ikke blir grønn.",
  "library": "Først en katalog nøklet på formål, bygget fra cellenes egne beskrivelser og kapabilitetsindeksen, slik at den ikke råtner. Oppslag går via formål, så ordsøk. Modellen får tekst fra biblioteket først etter oppslaget. Vektorsøk legges til bare hvis målinger på et uavhengig sett viser at ordsøk ikke holder.",
  "questions": [
    "Hvor gammel er Sverre, og leser han godt? Det avgjør om de første nivåene skal ha blokker i stedet for tekst.",
    "Hvilken enhet bruker han mest: iPad, PC eller Mac?",
    "Hvilken modell skal hjelperen bruke for ham: Claude via AIGateway, eller en lokal modell?",
    "Skal publiserte spill være åpne for alle, eller bare for dem som har lenken?"
  ],
  "next": [
    "Bilder av arbeidsbenken (samtale, forhåndsvisning, prosjekt, bibliotek) til G1-GUI.",
    "En klikkbar prototype Sverre kan prøve: chat med Claude, KAPLAY-spill i sandkasse og angre.",
    "Profilformat og kontrakt for arbeidsbenk-assistenten.",
    "Bibliotek v0 for spill med formål og lisens.",
    "Motorvalgsmåling: fem småspill i KAPLAY og Phaser."
  ],
  "docs": [
    "Formålsspesifikasjon: CellProtocolDocuments/Deliverables/PDD_spillverksted_2026-10-09/FORMAALSSPEC.md",
    "Mønsteret: CellScaffold Documentation/Arbeidsbenkassistent/README.md",
    "Spillverkstedet: CellScaffold Documentation/Spillverksted/README.md",
    "Grunnlag: Book 19 (chat-arbeidsbenk), Book 35 (PDD), Book 36 (formålssammensetning)"
  ]
}
data = json.dumps(t, ensure_ascii=False).replace("</", "<\\/")
html = open(os.path.join(D, "page.template.html")).read().replace("/*TREE*/", data)
open(os.path.join(D, "spillverksted-formaal.html"), "w").write(html)
# script for syntax check
s = html[html.rindex("<script>") + 8: html.rindex("</script>")]
open(os.path.join(D, "_check.js"), "w").write(s)
print(len(html))
