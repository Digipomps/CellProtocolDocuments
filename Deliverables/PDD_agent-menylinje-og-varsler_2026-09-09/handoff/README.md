# Handoff — rekkefølge og kommandoer

Alt her kjøres på macOS. Stier er relative til repoet.

## Før du rører noe

```
cd <HavenAgentD>
./Scripts/preflight_before_landing.sh
```

Fire spørsmål: er lokal main == origin/main, er arbeidstreet rent, er noen
avhengighet koblet lokalt med `swift package edit`, og ligger hver pin på
avhengighetens egen main. Alle må være grønne før du måler en baseline eller
lander noe. Bakgrunnen står i `Docs/Bygg_og_landing.md`.

## Bygge og kjøre menylinjen

```
swift build --product haven-agent-menu
./Packaging/menu-app/make_app.sh debug
open ".build/debug/HAVEN Agent.app"
```

Appen leser vert, port og token fra
`~/Library/Application Support/HAVENAgent/config.json`. Den finner aldri på sitt
eget token.

Peke den mot en annen agent (demo, feilsøking):

```
HAVEN_MENU_BRIDGE_PORT=43119 HAVEN_MENU_BRIDGE_TOKEN=… \
  ".build/debug/HAVEN Agent.app/Contents/MacOS/HAVEN Agent"
```

## Se hele kjeden uten å røre den agenten som kjører

```
./Packaging/menu-app/demo.sh
```

Starter en engangsagent på en ledig port med tom rot, og en egen app pekt dit.
Stopper bare det den selv startet.

## Sjekke innboksen for hånd

```
TOKEN=$(python3 -c "import json;print(json.load(open('$HOME/Library/Application Support/HAVENAgent/config.json'))['localControlBridge']['accessToken'])")
curl -s "http://127.0.0.1:43110/status/summary?token=$TOKEN"
curl -s "http://127.0.0.1:43110/challenges?token=$TOKEN"
```

`sources` skal alltid ha én rad per kjent kilde. En tom `challenges`-liste
betyr bare «ingenting venter» hvis alle kildene står som `read`.

## Kjøre testene

```
swift test
```

Merk: `swift test` avslutter med 1 selv når alt er grønt, fordi en tom
XCTest-pakke ikke kan lastes («have arm64, need x86_64»). Det gjelder også på
ren main. Les resultatet fra linjen `Test run with N tests … passed/failed`,
ikke fra exitkoden.

## Landing

Gjennom PR, aldri direkte på main. CI kjører pin-sjekken, lockfile-sjekken og
`./Scripts/test_haven_agentd.sh`. Det er CI som avgjør, ikke et lokalt bygg.

## Deploy

```
.build/menylinje-baseline/deploy.sh
```

Kloner main fra GitHub, bygger release, tar sikkerhetskopi av den kjørende
agentbinæren, bytter den, og **ruller automatisk tilbake** hvis `/health` eller
`/challenges` ikke svarer. Installerer så appen i `~/Applications` og en
LaunchAgent som starter den ved innlogging. Tilbakerullingskommandoen skrives
ut til slutt.
