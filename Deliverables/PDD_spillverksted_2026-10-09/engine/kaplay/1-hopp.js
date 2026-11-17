// Hoppespill: hopp mellom plattformer og samle 3 mynter!
const FART = 200;          // hvor fort figuren går
const HOPPKRAFT = 520;     // hvor høyt figuren hopper
const TYNGDEKRAFT = 1200;  // hvor sterkt figuren faller ned
const ANTALL_MYNTER = 3;   // hvor mange mynter som finnes

kaplay({ width: 640, height: 360, letterbox: true, global: true, background: [20, 33, 61] });

setGravity(TYNGDEKRAFT);

// Plattformer: [x, y, bredde]
const plattformer = [
  [0, 340, 640],
  [80, 260, 140],
  [280, 200, 120],
  [460, 140, 140],
];

for (const p of plattformer) {
  add([
    rect(p[2], 20),
    pos(p[0], p[1]),
    area(),
    body({ isStatic: true }),
    color(90, 200, 120),
    "plattform",
  ]);
}

// Myntene ligger over plattformene
const myntPlasser = [
  [150, 230],
  [340, 170],
  [530, 110],
];

for (const m of myntPlasser) {
  add([
    circle(10),
    pos(m[0], m[1]),
    anchor("center"),
    area(),
    color(255, 215, 0),
    "mynt",
  ]);
}

// Figuren
const figur = add([
  rect(28, 36),
  pos(40, 280),
  area(),
  body(),
  color(240, 100, 120),
  "figur",
]);

let mynter = 0;
const teller = add([text("Mynter: 0 / " + ANTALL_MYNTER, { size: 20 }), pos(12, 12), fixed()]);

onKeyDown("left", () => {
  figur.move(-FART, 0);
});

onKeyDown("right", () => {
  figur.move(FART, 0);
});

onKeyPress("space", () => {
  if (figur.isGrounded()) {
    figur.jump(HOPPKRAFT);
  }
});

figur.onCollide("mynt", (mynt) => {
  destroy(mynt);
  mynter = mynter + 1;
  teller.text = "Mynter: " + mynter + " / " + ANTALL_MYNTER;
  if (mynter >= ANTALL_MYNTER) {
    add([text("Du fant alle myntene!", { size: 28 }), pos(width() / 2, height() / 2), anchor("center")]);
  }
});

// Faller figuren ut av skjermen, starter den på nytt
figur.onUpdate(() => {
  if (figur.pos.y > height() + 100) {
    figur.pos = vec2(40, 280);
  }
});
