// Fangespill: fang ballene med kurven før de treffer bakken!
const KURV_FART = 350;      // hvor fort kurven flytter seg
const BALL_FART = 160;      // hvor fort ballene faller
const NY_BALL_HVERT = 1.2;  // sekunder mellom hver nye ball
const START_LIV = 3;        // hvor mange liv du har

kaplay({ width: 640, height: 360, letterbox: true, global: true, background: [20, 33, 61] });

let poeng = 0;
let liv = START_LIV;
let ferdig = false;

const kurv = add([
  rect(90, 20),
  pos(width() / 2, height() - 20),
  anchor("center"),
  area(),
  color(200, 140, 60),
  "kurv",
]);

const poengTekst = add([text("Poeng: 0", { size: 20 }), pos(12, 12)]);
const livTekst = add([text("Liv: " + liv, { size: 20 }), pos(width() - 12, 12), anchor("topright")]);

onKeyDown("left", () => {
  if (!ferdig && kurv.pos.x > 45) kurv.move(-KURV_FART, 0);
});

onKeyDown("right", () => {
  if (!ferdig && kurv.pos.x < width() - 45) kurv.move(KURV_FART, 0);
});

// Lag en ny ball med jevne mellomrom
loop(NY_BALL_HVERT, () => {
  if (ferdig) return;
  add([
    circle(12),
    pos(rand(20, width() - 20), -20),
    anchor("center"),
    area(),
    move(DOWN, BALL_FART),
    color(rand(100, 255), rand(100, 255), rand(100, 255)),
    "ball",
  ]);
});

kurv.onCollide("ball", (ball) => {
  destroy(ball);
  poeng = poeng + 1;
  poengTekst.text = "Poeng: " + poeng;
});

// Sjekk om en ball har falt forbi kurven
onUpdate("ball", (ball) => {
  if (ball.pos.y > height() + 20) {
    destroy(ball);
    if (ferdig) return;
    liv = liv - 1;
    livTekst.text = "Liv: " + liv;
    if (liv <= 0) {
      ferdig = true;
      add([text("Game over", { size: 48 }), pos(width() / 2, height() / 2), anchor("center"), color(255, 80, 80)]);
    }
  }
});
