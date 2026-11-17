// Labyrint: finn veien gjennom labyrinten til det grønne målet!
const RUTE = 32;     // hvor stor hver rute er (i piksler)
const FART = 140;    // hvor fort spilleren går

kaplay({ width: 640, height: 360, letterbox: true, global: true, background: [20, 33, 61] });

// Kartet: # = vegg, S = start, M = mål, mellomrom = gang
const kart = [
  "####################",
  "#S     #           #",
  "# #### # ######### #",
  "# #    #         # #",
  "# # ######## ### # #",
  "# #        #   # # #",
  "# ######## ### # # #",
  "#        #     #  M#",
  "# ###### ######### #",
  "#      #           #",
  "####################",
];

const bane = addLevel(kart, {
  tileWidth: RUTE,
  tileHeight: RUTE,
  pos: vec2(0, 4),
  tiles: {
    "#": () => [rect(RUTE, RUTE), color(70, 90, 160), area(), body({ isStatic: true }), "vegg"],
    "M": () => [rect(RUTE, RUTE), color(80, 220, 120), area(), "maal"],
    "S": () => [rect(RUTE, RUTE), opacity(0), "start"],
  },
});

// Spilleren starter på S-ruten
const start = bane.get("start")[0];
const spiller = add([
  rect(RUTE - 10, RUTE - 10),
  pos(start.pos.add(bane.pos).add(5, 5)),
  area(),
  body(),
  color(255, 200, 60),
  "spiller",
]);

let ferdig = false;

onKeyDown("left", () => { if (!ferdig) spiller.move(-FART, 0); });
onKeyDown("right", () => { if (!ferdig) spiller.move(FART, 0); });
onKeyDown("up", () => { if (!ferdig) spiller.move(0, -FART); });
onKeyDown("down", () => { if (!ferdig) spiller.move(0, FART); });

spiller.onCollide("maal", () => {
  if (ferdig) return;
  ferdig = true;
  add([rect(360, 70), pos(width() / 2, height() / 2), anchor("center"), color(0, 0, 0), opacity(0.7)]);
  add([text("Du klarte det!", { size: 36 }), pos(width() / 2, height() / 2), anchor("center")]);
});
