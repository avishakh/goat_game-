const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const backgroundMusic = document.getElementById('backgroundMusic');
const laserSound = document.getElementById('laserSound');
const explosionSound = document.getElementById('explosionSound');
const hilaSound = document.getElementById('hilaSound');
const massSound = document.getElementById('massSound');
const restartButton = document.getElementById('restartButton');

let playerImg = new Image();
playerImg.src = 'player.gif';

let enemyImg = new Image();
enemyImg.src = 'invaders.gif';

let player = { x: 270, y: 520, width: 50, height: 50, speed: 5 };
let bullet = { x: 0, y: 0, width: 5, height: 20, speed: 7, active: false };
let enemies = [];
let enemySpeed = 2;
let score = 0;
let gameRunning = true;

function spawnEnemies() {
    enemies = [];
    for (let i = 0; i < 5; i++) {
        let x = Math.random() * (canvas.width - 50);
        let y = Math.random() * 100;
        enemies.push({ x: x, y: y, width: 40, height: 40 });
    }
}

function drawPlayer() {
    ctx.drawImage(playerImg, player.x, player.y, player.width, player.height);
}

function drawEnemies() {
    enemies.forEach(enemy => {
        ctx.drawImage(enemyImg, enemy.x, enemy.y, enemy.width, enemy.height);
    });
}

function drawBullet() {
    if (bullet.active) {
        ctx.fillStyle = 'yellow';
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    }
}

function drawScore() {
    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}`, 10, 30);
}

function moveBullet() {
    if (bullet.active) {
        bullet.y -= bullet.speed;
        if (bullet.y < 0) bullet.active = false;
    }
}

function moveEnemies() {
    enemies.forEach(enemy => {
        enemy.x += enemySpeed;
        if (enemy.x <= 0 || enemy.x + enemy.width >= canvas.width) {
            enemySpeed *= -1;
            enemies.forEach(e => e.y += 40);
        }
    });
}

function checkCollision(a, b) {
    return a.x < b.x + b.width && a.x + a.width > b.x &&
           a.y < b.y + b.height && a.y + a.height > b.y;
}

function checkBulletCollision() {
    enemies.forEach((enemy, index) => {
        if (bullet.active && checkCollision(bullet, enemy)) {
            explosionSound.play();
            enemies.splice(index, 1);
            bullet.active = false;
            score += 10;
            if (score % 100 === 0) enemySpeed += 1;
        }
    });
}

function checkPlayerCollision() {
    enemies.forEach(enemy => {
        if (checkCollision(player, enemy)) {
            gameOver();
        }
    });
}

function gameOver() {
    gameRunning = false;
    backgroundMusic.pause();
    hilaSound.play();
    setTimeout(() => {
        massSound.play();
        setTimeout(() => {
            restartButton.style.display = 'block';
        }, 1500);
    }, 1500);
}

function restartGame() {
    score = 0;
    enemySpeed = 2;
    bullet.active = false;
    player.x = 270;
    backgroundMusic.currentTime = 0;
    backgroundMusic.play();
    spawnEnemies();
    restartButton.style.display = 'none';
    gameRunning = true;
}

function gameLoop() {
    if (!gameRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawPlayer();
    drawEnemies();
    drawBullet();
    drawScore();

    moveBullet();
    moveEnemies();
    checkBulletCollision();
    checkPlayerCollision();

    if (enemies.length === 0) {
        spawnEnemies();
    }

    requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', e => {
    if (e.key === 'a' || e.key === 'ArrowLeft') {
        player.x -= player.speed;
        if (player.x < 0) player.x = 0;
    } else if (e.key === 'd' || e.key === 'ArrowRight') {
        player.x += player.speed;
        if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
    } else if (e.key === ' ' && !bullet.active) {
        laserSound.play();
        bullet.x = player.x + player.width / 2 - bullet.width / 2;
        bullet.y = player.y;
        bullet.active = true;
    }
});

// Start the Game
backgroundMusic.play();
spawnEnemies();
gameLoop();
