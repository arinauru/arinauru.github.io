const canvas = document.getElementById("stars");
const ctx = canvas.getContext("2d");

let stars = [];

function resize() {
  const dpr = window.devicePixelRatio || 1;

  canvas.width = window.innerWidth * dpr;
  canvas.height = window.innerHeight * dpr;

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function createStars() {
  stars = [];

  for (let i = 0; i < 90; i++) {
    stars.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      size: Math.random() * 1.8 + 0.5,
      speed: Math.random() * 0.45 + 0.15,
      opacity: Math.random() * 0.5 + 0.25
    });
  }
}

function animate() {
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

  stars.forEach(star => {
    ctx.beginPath();
    ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);

    ctx.fillStyle =
      `rgba(110, 86, 207, ${star.opacity})`;

    ctx.fill();

    star.y += star.speed;

    if (star.y > window.innerHeight + 5) {
      star.y = -5;
      star.x = Math.random() * window.innerWidth;
    }
  });

  requestAnimationFrame(animate);
}

window.addEventListener("resize", () => {
  resize();
  createStars();
});

resize();
createStars();
animate();
