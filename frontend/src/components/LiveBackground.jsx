import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const ORBS = [
  { size: 600, x: '-10%', y: '-15%', color: 'var(--orb-1)', delay: 0,    duration: 22 },
  { size: 480, x: '75%',  y: '65%',  color: 'var(--orb-2)', delay: -8,   duration: 26 },
  { size: 340, x: '55%',  y: '-5%',  color: 'var(--orb-4)', delay: -4,   duration: 19 },
  { size: 260, x: '20%',  y: '70%',  color: 'var(--orb-3)', delay: -13,  duration: 30 },
];

const drift = (i) => ({
  animate: {
    x: [0, 30 + i * 10, -20 - i * 5, 0],
    y: [0, -40 - i * 8, 25 + i * 6,  0],
    scale: [1, 1.06, 0.96, 1],
  },
  transition: {
    duration: ORBS[i].duration,
    delay: ORBS[i].delay,
    repeat: Infinity,
    ease: 'easeInOut',
  },
});

/* Particle canvas for live wallpaper effect */
function ParticleCanvas() {
  const canvasRef = useRef(null);
  const animRef   = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx    = canvas.getContext('2d');
    let W, H, particles = [];

    const isDark = () => document.documentElement.getAttribute('data-theme') !== 'light';

    const resize = () => {
      W = canvas.width  = window.innerWidth;
      H = canvas.height = window.innerHeight;
    };

    class Particle {
      constructor() { this.reset(); }
      reset() {
        this.x     = Math.random() * W;
        this.y     = Math.random() * H;
        this.r     = Math.random() * 1.4 + 0.3;
        this.vx    = (Math.random() - 0.5) * 0.25;
        this.vy    = (Math.random() - 0.5) * 0.25;
        this.alpha = Math.random() * 0.5 + 0.1;
        this.pulse = Math.random() * Math.PI * 2;
      }
      update() {
        this.x    += this.vx;
        this.y    += this.vy;
        this.pulse += 0.01;
        this.alpha = 0.08 + Math.abs(Math.sin(this.pulse)) * 0.3;
        if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
      }
      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        const dark = isDark();
        ctx.fillStyle = dark
          ? `rgba(99,179,237,${this.alpha})`
          : `rgba(37,99,235,${this.alpha * 0.6})`;
        ctx.fill();
      }
    }

    const init = () => {
      resize();
      particles = Array.from({ length: 100 }, () => new Particle());
    };

    const drawLines = () => {
      const dark = isDark();
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx   = particles[i].x - particles[j].x;
          const dy   = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 100) {
            const a = (1 - dist / 100) * 0.06;
            ctx.beginPath();
            ctx.strokeStyle = dark
              ? `rgba(99,179,237,${a})`
              : `rgba(37,99,235,${a * 0.5})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
    };

    const loop = () => {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(p => { p.update(); p.draw(); });
      drawLines();
      animRef.current = requestAnimationFrame(loop);
    };

    init();
    loop();
    window.addEventListener('resize', resize);
    return () => {
      cancelAnimationFrame(animRef.current);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{ position: 'absolute', inset: 0, zIndex: 0, pointerEvents: 'none' }}
    />
  );
}

export default function LiveBackground() {
  return (
    <div className="bg-canvas">
      <ParticleCanvas />
      <div className="bg-gradient-overlay" />
      <div className="grid-overlay" />
      {ORBS.map((orb, i) => (
        <motion.div
          key={i}
          className="orb"
          style={{
            width:      orb.size,
            height:     orb.size,
            left:       orb.x,
            top:        orb.y,
            background: `radial-gradient(circle, ${orb.color}, transparent 68%)`,
            opacity:    0.35,
          }}
          {...drift(i)}
        />
      ))}
    </div>
  );
}
