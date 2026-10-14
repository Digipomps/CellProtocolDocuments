// HOPP! Beveg figuren med piltastene, hopp med mellomrom og samle mynter.

const FART = 200;        // hvor fort figuren går
const HOPPEKRAFT = 420;  // hvor høyt figuren hopper
const TYNGDEKRAFT = 800; // hvor fort figuren faller
const ANTALL_MYNTER = 3; // hvor mange mynter som finnes

let figur;
let plattformer;
let mynter;
let piltaster;
let mellomrom;
let myntTekst;
let samlet = 0;

function lagTekstur(scene, navn, farge, bredde, hoyde, rund) {
  const tegning = scene.add.graphics();
  tegning.fillStyle(farge, 1);
  if (rund) {
    tegning.fillCircle(bredde / 2, hoyde / 2, bredde / 2);
  } else {
    tegning.fillRect(0, 0, bredde, hoyde);
  }
  tegning.generateTexture(navn, bredde, hoyde);
  tegning.destroy();
}

function lag() {
  lagTekstur(this, 'figur', 0xfca311, 28, 40, false);
  lagTekstur(this, 'plattform', 0x8ecae6, 100, 20, false);
  lagTekstur(this, 'mynt', 0xffd60a, 20, 20, true);

  // Plattformene: [x, y, bredde]
  plattformer = this.physics.add.staticGroup();
  const plattformListe = [
    [320, 350, 640],
    [120, 270, 160],
    [330, 200, 140],
    [530, 130, 160],
  ];
  for (const [x, y, bredde] of plattformListe) {
    const p = plattformer.create(x, y, 'plattform');
    p.setDisplaySize(bredde, 20);
    p.refreshBody();
  }

  figur = this.physics.add.sprite(60, 280, 'figur');
  figur.setCollideWorldBounds(true);
  this.physics.add.collider(figur, plattformer);

  // Myntene ligger over plattformene
  mynter = this.physics.add.staticGroup();
  const myntPlasser = [[120, 235], [330, 165], [560, 95]];
  for (let i = 0; i < ANTALL_MYNTER; i++) {
    const [x, y] = myntPlasser[i];
    mynter.create(x, y, 'mynt');
  }
  this.physics.add.overlap(figur, mynter, taMynt, null, this);

  myntTekst = this.add.text(16, 16, 'Mynter: 0 / ' + ANTALL_MYNTER, {
    fontSize: '22px',
    color: '#ffffff',
  });

  piltaster = this.input.keyboard.createCursorKeys();
  mellomrom = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
}

function taMynt(figur, mynt) {
  mynt.destroy();
  samlet = samlet + 1;
  myntTekst.setText('Mynter: ' + samlet + ' / ' + ANTALL_MYNTER);
  if (samlet === ANTALL_MYNTER) {
    this.add.text(320, 180, 'Du fant alle myntene!', {
      fontSize: '32px',
      color: '#ffd60a',
    }).setOrigin(0.5);
  }
}

function oppdater() {
  if (piltaster.left.isDown) {
    figur.setVelocityX(-FART);
  } else if (piltaster.right.isDown) {
    figur.setVelocityX(FART);
  } else {
    figur.setVelocityX(0);
  }

  const staarPaaNoe = figur.body.blocked.down || figur.body.touching.down;
  if (Phaser.Input.Keyboard.JustDown(mellomrom) && staarPaaNoe) {
    figur.setVelocityY(-HOPPEKRAFT);
  }
}

new Phaser.Game({
  type: Phaser.AUTO,
  width: 640,
  height: 360,
  backgroundColor: '#14213d',
  parent: document.body,
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: TYNGDEKRAFT } },
  },
  scene: { create: lag, update: oppdater },
});
