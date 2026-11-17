// FANG BALLENE! Flytt kurven med piltastene og fang ballene som faller.

const KURV_FART = 350;   // hvor fort kurven går
const BALL_FART = 150;   // hvor fort ballene faller
const NY_BALL_HVER = 1000; // millisekunder mellom hver nye ball
const LIV = 3;           // hvor mange liv du starter med

let kurv;
let baller;
let piltaster;
let poeng = 0;
let liv = LIV;
let tekst;
let ferdig = false;
let ballTimer;

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
  lagTekstur(this, 'kurv', 0xa0522d, 90, 24, false);
  lagTekstur(this, 'ball', 0xe63946, 24, 24, true);

  kurv = this.physics.add.sprite(320, 330, 'kurv');
  kurv.setCollideWorldBounds(true);
  kurv.body.setAllowGravity(false);
  kurv.setImmovable(true);

  baller = this.physics.add.group();
  this.physics.add.overlap(kurv, baller, fangBall);

  tekst = this.add.text(16, 16, '', { fontSize: '22px', color: '#ffffff' });
  visTekst();

  piltaster = this.input.keyboard.createCursorKeys();

  ballTimer = this.time.addEvent({
    delay: NY_BALL_HVER,
    loop: true,
    callback: () => {
      const x = Phaser.Math.Between(20, 620);
      const ball = baller.create(x, -20, 'ball');
      ball.body.setAllowGravity(false);
      ball.setVelocityY(BALL_FART);
    },
  });
}

function visTekst() {
  tekst.setText('Poeng: ' + poeng + '   Liv: ' + liv);
}

function fangBall(kurv, ball) {
  ball.destroy();
  poeng = poeng + 1;
  visTekst();
}

function oppdater() {
  if (ferdig) {
    return;
  }

  if (piltaster.left.isDown) {
    kurv.setVelocityX(-KURV_FART);
  } else if (piltaster.right.isDown) {
    kurv.setVelocityX(KURV_FART);
  } else {
    kurv.setVelocityX(0);
  }

  // Sjekk om noen baller har falt forbi kurven
  for (const ball of baller.getChildren().slice()) {
    if (ball.y > 380) {
      ball.destroy();
      liv = liv - 1;
      visTekst();
      if (liv <= 0) {
        ferdig = true;
        ballTimer.remove();
        this.physics.pause();
        this.add.text(320, 180, 'Game over', {
          fontSize: '48px',
          color: '#fca311',
        }).setOrigin(0.5);
        return;
      }
    }
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
