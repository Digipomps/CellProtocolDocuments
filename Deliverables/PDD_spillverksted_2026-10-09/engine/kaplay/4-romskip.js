// Romskip: skyt asteroidene før de treffer skipet ditt!
const SKIP_FART = 300;        // hvor fort skipet flytter seg
const SKUDD_FART = 450;       // hvor fort skuddene flyr
const STEIN_FART = 120;       // hvor fort asteroidene faller
const NY_STEIN_HVERT = 0.9;   // sekunder mellom hver nye asteroide

kaplay({ width: 640, height: 360, letterbox: true, global: true, background: [20, 33, 61] });

let poeng = 0;
let ferdig = false;

const skip = add([
  polygon([vec2(0, -18), vec2(16, 14), vec2(-16, 14)]),
  pos(width() / 2, height() - 30),
  area(),
  color(120, 220, 255),
  "skip",
]);

const poengTekst = add([text("Poeng: 0", { size: 20 }), pos(12, 12)]);

onKeyDown("left", () => {
  if (!ferdig && skip.pos.x > 20) skip.move(-SKIP_FART, 0);
});

onKeyDown("right", () => {
  if (!ferdig && skip.pos.x < width() - 20) skip.move(SKIP_FART, 0);
});

onKeyPress("space", () => {
  if (ferdig) return;
  add([
    rect(4, 12),
    pos(skip.pos.x, skip.pos.y - 20),
    anchor("center"),
    area(),
    move(UP, SKUDD_FART),
    offscreen({ destroy: true }),
    color(255, 255, 120),
    "skudd",
  ]);
});

loop(NY_STEIN_HVERT, () => {
  if (ferdig) return;
  add([
    circle(rand(12, 24)),
    pos(rand(30, width() - 30), -30),
    anchor("center"),
    area(),
    move(DOWN, STEIN_FART),
    offscreen({ destroy: true, distance: 60 }),
    color(150, 120, 100),
    "stein",
  ]);
});

onCollide("skudd", "stein", (skudd, stein) => {
  destroy(skudd);
  destroy(stein);
  poeng = poeng + 1;
  poengTekst.text = "Poeng: " + poeng;
});

skip.onCollide("stein", () => {
  if (ferdig) return;
  ferdig = true;
  destroy(skip);
  add([text("Game over", { size: 48 }), pos(width() / 2, height() / 2 - 20), anchor("center"), color(255, 80, 80)]);
  add([text("Poeng: " + poeng, { size: 24 }), pos(width() / 2, height() / 2 + 30), anchor("center")]);
});
