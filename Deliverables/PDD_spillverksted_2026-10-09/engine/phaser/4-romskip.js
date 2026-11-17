// ROMSKIP! Flytt skipet med piltastene og skyt asteroidene med mellomrom.

const SKIP_FART = 300;        // hvor fort skipet går
const SKUDD_FART = 450;       // hvor fort skuddene flyr
const ASTEROIDE_FART = 120;   // hvor fort asteroidene faller
const NY_ASTEROIDE_HVER = 900; // millisekunder mellom hver nye asteroide

let skip;
let skudd;
let asteroider;
let piltaster;
let mellomrom;
let poeng = 0;
let poengTekst;
let ferdig = false;
let asteroideTimer;

function lag() {
  // Tegn skipet som en trekant
  let tegning = this.add.graphics();
  tegning.fillStyle(0x8ecae6, 1);
  tegning.fillTriangle(16, 0, 32, 32, 0, 32);
  tegning.generateTexture('skip', 32, 32);
  tegning.destroy();

  tegning = this.add.graphics();
  tegning.fillStyle(0xffd60a, 1);
  tegning.fillRect(0, 0, 4, 12);
  tegning.generateTexture('skudd', 4, 12);
  tegning.destroy();

  tegning = this.add.graphics();
  tegning.fillStyle(0x9c6644, 1);
  tegning.fillCircle(18, 18, 18);
  tegning.generateTexture('asteroide', 36, 36);
  tegning.destroy();

  skip = this.physics.add.sprite(320, 330, 'skip');
  skip.setCollideWorldBounds(true);

  skudd = this.physics.add.group();
  asteroider = this.physics.add.group();

  this.physics.add.overlap(skudd, asteroider, treff);
  this.physics.add.overlap(skip, asteroider, krasj, null, this);

  poengTekst = this.add.text(16, 16, 'Poeng: 0', { fontSize: '22px', color: '#ffffff' });

  piltaster = this.input.keyboard.createCursorKeys();
  mellomrom = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

  asteroideTimer = this.time.addEvent({
    delay: NY_ASTEROIDE_HVER,
    loop: true,
    callback: () => {
      const x = Phaser.Math.Between(20, 620);
      const stein = asteroider.create(x, -20, 'asteroide');
      stein.setVelocityY(ASTEROIDE_FART);
    },
  });
}

function treff(ettSkudd, stein) {
  ettSkudd.destroy();
  stein.destroy();
  poeng = poeng + 1;
  poengTekst.setText('Poeng: ' + poeng);
}

function krasj() {
  ferdig = true;
  asteroideTimer.remove();
  this.physics.pause();
  skip.setTint(0xff0000);
  this.add.text(320, 180, 'Spillet er slutt!', {
    fontSize: '44px',
    color: '#fca311',
  }).setOrigin(0.5);
}

function oppdater() {
  if (ferdig) {
    return;
  }

  if (piltaster.left.isDown) {
    skip.setVelocityX(-SKIP_FART);
  } else if (piltaster.right.isDown) {
    skip.setVelocityX(SKIP_FART);
  } else {
    skip.setVelocityX(0);
  }

  if (Phaser.Input.Keyboard.JustDown(mellomrom)) {
    const nyttSkudd = skudd.create(skip.x, skip.y - 20, 'skudd');
    nyttSkudd.setVelocityY(-SKUDD_FART);
  }

  // Rydd bort ting som har forlatt skjermen
  for (const s of skudd.getChildren().slice()) {
    if (s.y < -20) s.destroy();
  }
  for (const stein of asteroider.getChildren().slice()) {
    if (stein.y > 400) stein.destroy();
  }
}

new Phaser.Game({
  type: Phaser.AUTO,
  width: 640,
  height: 360,
  backgroundColor: '#14213d',
  parent: document.body,
  physics: { default: 'arcade' },
  scene: { create: lag, update: oppdater },
});
