const canvas = document.getElementById("stars");
const ctx = canvas.getContext("2d");

let flakes = [];

function resize() {
  const dpr = window.devicePixelRatio || 1;

  canvas.width = window.innerWidth * dpr;
  canvas.height = window.innerHeight * dpr;

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function createFlakes() {
  flakes = [];

  for (let i = 0; i < 70; i++) {
    flakes.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      size: Math.random() * 11 + 5,
      speed: Math.random() * 0.65 + 0.25,
      drift: Math.random() * 0.4 - 0.2,
      opacity: Math.random() * 0.45 + 0.3,
      angle: Math.random() * Math.PI
    });
  }
}

function animate() {
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

  for (const flake of flakes) {
    ctx.save();

    ctx.translate(flake.x, flake.y);
    ctx.rotate(flake.angle);

    ctx.font = `${flake.size}px Arial`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    ctx.fillStyle =
      `rgba(110, 86, 207, ${flake.opacity})`;

    ctx.shadowColor = "rgba(110, 86, 207, 0.25)";
    ctx.shadowBlur = 4;

    ctx.fillText("❄", 0, 0);

    ctx.restore();

    flake.y += flake.speed;
    flake.x += flake.drift;
    flake.angle += 0.003;

    if (flake.y > window.innerHeight + 20) {
      flake.y = -20;
      flake.x = Math.random() * window.innerWidth;
    }

    if (flake.x < -20) {
      flake.x = window.innerWidth + 20;
    }

    if (flake.x > window.innerWidth + 20) {
      flake.x = -20;
    }
  }

  requestAnimationFrame(animate);
}

window.addEventListener("resize", () => {
  resize();
  createFlakes();
});

resize();
createFlakes();
animate();
