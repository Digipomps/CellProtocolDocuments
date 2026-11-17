// LABYRINT! Finn veien til det grønne målet med piltastene.

const RUTE = 40; // hvor stor hver rute er (i piksler)

// Kartet: # = vegg, S = start, M = mål, mellomrom = gang
const KART = [
  '################',
  '#S   #         #',
  '# ## # ####### #',
  '#  #   #     # #',
  '## ##### ### # #',
  '#      #   #   #',
  '# #### ### #####',
  '#    #       #M#',
  '################',
];

let spillerRad;
let spillerKolonne;
let spiller;
let piltaster;
let ferdig = false;

function lag() {
  const tegning = this.add.graphics();

  for (let rad = 0; rad < KART.length; rad++) {
    for (let kolonne = 0; kolonne < KART[rad].length; kolonne++) {
      const tegn = KART[rad][kolonne];
      const x = kolonne * RUTE;
      const y = rad * RUTE;
      if (tegn === '#') {
        tegning.fillStyle(0x8ecae6, 1);
        tegning.fillRect(x, y, RUTE, RUTE);
      } else if (tegn === 'M') {
        tegning.fillStyle(0x2a9d8f, 1);
        tegning.fillRect(x, y, RUTE, RUTE);
      } else if (tegn === 'S') {
        spillerRad = rad;
        spillerKolonne = kolonne;
      }
    }
  }

  spiller = this.add.circle(0, 0, RUTE / 2 - 6, 0xfca311);
  flyttSpillerTilRute();

  piltaster = this.input.keyboard.createCursorKeys();
}

function flyttSpillerTilRute() {
  spiller.x = spillerKolonne * RUTE + RUTE / 2;
  spiller.y = spillerRad * RUTE + RUTE / 2;
}

function provFlytt(scene, radEndring, kolonneEndring) {
  const nyRad = spillerRad + radEndring;
  const nyKolonne = spillerKolonne + kolonneEndring;
  const tegn = KART[nyRad][nyKolonne];
  if (tegn === '#') {
    return; // vegg! vi kan ikke gå hit
  }
  spillerRad = nyRad;
  spillerKolonne = nyKolonne;
  flyttSpillerTilRute();

  if (tegn === 'M') {
    ferdig = true;
    scene.add.text(320, 180, 'Du klarte det!', {
      fontSize: '48px',
      color: '#ffffff',
      backgroundColor: '#000000',
    }).setOrigin(0.5);
  }
}

function oppdater() {
  if (ferdig) {
    return;
  }
  const trykket = Phaser.Input.Keyboard.JustDown;
  if (trykket(piltaster.left)) provFlytt(this, 0, -1);
  if (trykket(piltaster.right)) provFlytt(this, 0, 1);
  if (trykket(piltaster.up)) provFlytt(this, -1, 0);
  if (trykket(piltaster.down)) provFlytt(this, 1, 0);
}

new Phaser.Game({
  type: Phaser.AUTO,
  width: 640,
  height: 360,
  backgroundColor: '#14213d',
  parent: document.body,
  scene: { create: lag, update: oppdater },
});
