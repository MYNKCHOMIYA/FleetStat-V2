import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

/* ─── Orb data ─────────────────────────────────────────── */
const ORBS = [
  {
    size: 700, top: '-18%', left: '-12%',
    color: 'radial-gradient(circle, rgba(59,130,246,0.45) 0%, transparent 68%)',
    animation: 'animate-drift-1', opacity: 0.45, blur: 100,
  },
  {
    size: 550, bottom: '-15%', right: '-10%',
    color: 'radial-gradient(circle, rgba(139,92,246,0.40) 0%, transparent 68%)',
    animation: 'animate-drift-2', opacity: 0.4, blur: 110,
  },
  {
    size: 380, top: '40%', left: '55%',
    color: 'radial-gradient(circle, rgba(99,102,241,0.35) 0%, transparent 68%)',
    animation: 'animate-drift-3', opacity: 0.35, blur: 90,
  },
  {
    size: 300, top: '10%', right: '20%',
    color: 'radial-gradient(circle, rgba(20,184,166,0.25) 0%, transparent 68%)',
    animation: 'animate-drift-4', opacity: 0.3, blur: 80,
  },
];

/* ─── Particle canvas ──────────────────────────────────── */
function ParticleCanvas() {
  const ref = useRef(null);
  const raf = useRef(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H, pts = [];

    const resize = () => {
      W = canvas.width  = window.innerWidth;
      H = canvas.height = window.innerHeight;
    };

    class Pt {
      constructor() { this.reset(true); }
      reset(init = false) {
        this.x  = Math.random() * (W || window.innerWidth);
        this.y  = init ? Math.random() * (H || window.innerHeight) : -4;
        this.vx = (Math.random() - 0.5) * 0.3;
        this.vy = Math.random() * 0.2 + 0.05;
        this.r  = Math.random() * 1.2 + 0.3;
        this.a  = Math.random() * 0.45 + 0.08;
        this.pulse = Math.random() * Math.PI * 2;
      }
      tick() {
        this.x += this.vx; this.y += this.vy;
        this.pulse += 0.012;
        if (this.y > H + 4) this.reset();
      }
      draw() {
        const a = this.a * (0.5 + 0.5 * Math.sin(this.pulse));
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(148,163,184,${a})`;
        ctx.fill();
      }
    }

    const drawLines = () => {
      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
          const d  = Math.sqrt(dx*dx + dy*dy);
          if (d < 90) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(99,102,241,${(1 - d/90) * 0.07})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(pts[i].x, pts[i].y);
            ctx.lineTo(pts[j].x, pts[j].y);
            ctx.stroke();
          }
        }
      }
    };

    const loop = () => {
      ctx.clearRect(0, 0, W, H);
      pts.forEach(p => { p.tick(); p.draw(); });
      drawLines();
      raf.current = requestAnimationFrame(loop);
    };

    resize();
    pts = Array.from({ length: 90 }, () => new Pt());
    loop();
    window.addEventListener('resize', resize);
    return () => {
      cancelAnimationFrame(raf.current);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={ref}
      className="absolute inset-0 w-full h-full pointer-events-none opacity-60"
    />
  );
}

/* ─── Floating animated orb ────────────────────────────── */
function Orb({ size, color, opacity, blur, animation, ...pos }) {
  return (
    <div
      className={`absolute rounded-full pointer-events-none ${animation}`}
      style={{
        width:      size,
        height:     size,
        background: color,
        opacity,
        filter:     `blur(${blur}px)`,
        ...pos,
      }}
    />
  );
}

/* ─── Star field ────────────────────────────────────────── */
function Stars() {
  const stars = Array.from({ length: 60 }, (_, i) => ({
    id: i,
    x:  Math.random() * 100,
    y:  Math.random() * 100,
    r:  Math.random() * 1.5 + 0.3,
    a:  Math.random() * 0.4 + 0.1,
    delay: Math.random() * 4,
  }));

  return (
    <svg className="absolute inset-0 w-full h-full pointer-events-none" xmlns="http://www.w3.org/2000/svg">
      {stars.map(s => (
        <motion.circle
          key={s.id}
          cx={`${s.x}%`}
          cy={`${s.y}%`}
          r={s.r}
          fill="white"
          initial={{ opacity: 0 }}
          animate={{ opacity: [s.a * 0.4, s.a, s.a * 0.4] }}
          transition={{ duration: 3 + Math.random() * 2, delay: s.delay, repeat: Infinity, ease: 'easeInOut' }}
        />
      ))}
    </svg>
  );
}

/* ─── Grid overlay ──────────────────────────────────────── */
function GridOverlay() {
  return (
    <div
      className="absolute inset-0 pointer-events-none opacity-20"
      style={{
        backgroundImage: `
          linear-gradient(rgba(99,102,241,0.08) 1px, transparent 1px),
          linear-gradient(90deg, rgba(99,102,241,0.08) 1px, transparent 1px)
        `,
        backgroundSize: '50px 50px',
        maskImage: 'radial-gradient(ellipse 100% 100% at 50% 50%, black 20%, transparent 80%)',
      }}
    />
  );
}

/* ─── AuthLayout ────────────────────────────────────────── */
export default function AuthLayout({ children }) {
  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-slate-950 flex items-center justify-center p-4 sm:p-6 lg:p-8">

      {/* Deep space base gradient */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse 100% 80% at 50% 0%, rgba(15,23,42,1) 0%, rgba(2,6,23,1) 100%)',
        }}
      />

      {/* Stars */}
      <Stars />

      {/* Grid */}
      <GridOverlay />

      {/* Particle canvas */}
      <ParticleCanvas />

      {/* Orbs */}
      {ORBS.map((o, i) => <Orb key={i} {...o} />)}

      {/* Subtle scanline effect */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.02]"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,1) 2px, rgba(255,255,255,1) 4px)',
        }}
      />

      {/* Content */}
      <div className="relative z-10 w-full">
        {children}
      </div>
    </div>
  );
}
