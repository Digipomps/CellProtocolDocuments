// KLIKK! Klikk på figurene før de forsvinner. Du har 30 sekunder.

const SPILLETID = 30;       // hvor mange sekunder spillet varer
const NY_FIGUR_HVER = 700;  // millisekunder mellom hver nye figur
const FIGUR_LEVETID = 1200; // millisekunder før en figur forsvinner
const FARGER = [0xe63946, 0xfca311, 0x2a9d8f, 0x8ecae6, 0xffd60a];

let poeng = 0;
let tidIgjen = SPILLETID;
let poengTekst;
let tidTekst;
let figurTimer;
let ferdig = false;

function lag() {
  poengTekst = this.add.text(16, 16, 'Poeng: 0', { fontSize: '22px', color: '#ffffff' });
  tidTekst = this.add.text(624, 16, 'Tid: ' + tidIgjen, { fontSize: '22px', color: '#ffffff' })
    .setOrigin(1, 0);

  figurTimer = this.time.addEvent({
    delay: NY_FIGUR_HVER,
    loop: true,
    callback: () => lagFigur(this),
  });

  // Nedtelling: én gang i sekundet
  this.time.addEvent({
    delay: 1000,
    repeat: SPILLETID - 1,
    callback: () => {
      tidIgjen = tidIgjen - 1;
      tidTekst.setText('Tid: ' + tidIgjen);
      if (tidIgjen <= 0) {
        slutt(this);
      }
    },
  });
}

function lagFigur(scene) {
  const x = Phaser.Math.Between(40, 600);
  const y = Phaser.Math.Between(70, 320);
  const farge = Phaser.Utils.Array.GetRandom(FARGER);

  let figur;
  if (Math.random() < 0.5) {
    figur = scene.add.circle(x, y, 26, farge);
  } else {
    figur = scene.add.rectangle(x, y, 50, 50, farge);
  }
  figur.setInteractive({ useHandCursor: true });

  figur.on('pointerdown', () => {
    if (ferdig) return;
    poeng = poeng + 1;
    poengTekst.setText('Poeng: ' + poeng);
    figur.destroy();
  });

  // Figuren forsvinner av seg selv etter en stund
  scene.time.delayedCall(FIGUR_LEVETID, () => {
    if (figur.active) figur.destroy();
  });
}

function slutt(scene) {
  ferdig = true;
  figurTimer.remove();
  scene.add.text(320, 180, 'Tiden er ute!\nDu fikk ' + poeng + ' poeng', {
    fontSize: '40px',
    color: '#ffffff',
    align: 'center',
  }).setOrigin(0.5);
}

new Phaser.Game({
  type: Phaser.AUTO,
  width: 640,
  height: 360,
  backgroundColor: '#14213d',
  parent: document.body,
  scene: { create: lag },
});
