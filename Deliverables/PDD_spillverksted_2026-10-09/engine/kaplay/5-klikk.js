// Klikkespill: klikk på figurene før de forsvinner!
const SPILLETID = 30;        // hvor mange sekunder spillet varer
const NY_FIGUR_HVERT = 0.7;  // sekunder mellom hver nye figur
const FIGUR_LEVETID = 1.2;   // hvor lenge en figur blir synlig
const FIGUR_STORRELSE = 26;  // hvor stor en figur er

kaplay({ width: 640, height: 360, letterbox: true, global: true, background: [20, 33, 61] });

let poeng = 0;
let tidIgjen = SPILLETID;
let ferdig = false;

const poengTekst = add([text("Poeng: 0", { size: 20 }), pos(12, 12), z(10)]);
const tidTekst = add([text("Tid: " + SPILLETID, { size: 20 }), pos(width() - 12, 12), anchor("topright"), z(10)]);

function lagFigur() {
  const x = rand(40, width() - 40);
  const y = rand(60, height() - 40);
  const farge = color(rand(80, 255), rand(80, 255), rand(80, 255));
  let form;
  if (randi(0, 2) === 0) {
    form = circle(FIGUR_STORRELSE);
  } else {
    form = rect(FIGUR_STORRELSE * 2, FIGUR_STORRELSE * 2);
  }
  const figur = add([form, pos(x, y), anchor("center"), area(), farge, "figur"]);

  figur.onClick(() => {
    if (ferdig) return;
    poeng = poeng + 1;
    poengTekst.text = "Poeng: " + poeng;
    destroy(figur);
  });

  // Figuren forsvinner av seg selv etter en stund
  wait(FIGUR_LEVETID, () => {
    destroy(figur);
  });
}

loop(NY_FIGUR_HVERT, () => {
  if (!ferdig) lagFigur();
});

onUpdate(() => {
  if (ferdig) return;
  tidIgjen = tidIgjen - dt();
  tidTekst.text = "Tid: " + Math.ceil(tidIgjen);
  if (tidIgjen <= 0) {
    ferdig = true;
    tidTekst.text = "Tid: 0";
    destroyAll("figur");
    add([text("Tiden er ute!", { size: 40 }), pos(width() / 2, height() / 2 - 25), anchor("center")]);
    add([text("Du fikk " + poeng + " poeng", { size: 28 }), pos(width() / 2, height() / 2 + 25), anchor("center"), color(255, 215, 0)]);
  }
});
