import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Truck, Activity, Users, Settings,
  LogOut, Bell, Search, TrendingUp, BarChart3,
  Clock, Shield, CheckCircle2, AlertTriangle,
  Fuel, Wrench, MapPin, ChevronRight, Menu, X,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Spinner } from '../components/ui';

/* ── Sidebar nav items ── */
const NAV = [
  { id: 'overview',  label: 'Overview',   icon: LayoutDashboard },
  { id: 'fleet',     label: 'Fleet',      icon: Truck           },
  { id: 'analytics', label: 'Analytics',  icon: Activity        },
  { id: 'users',     label: 'Team',       icon: Users           },
  { id: 'settings',  label: 'Settings',   icon: Settings        },
];

/* ── Stat cards data ── */
const STATS = [
  { label: 'Active Vehicles',   value: '284',    delta: '+12', unit: '%',    icon: Truck,      color: 'from-blue-500   to-blue-600',   glow: 'rgba(59,130,246,0.3)'   },
  { label: 'Trips Today',       value: '1,847',  delta: '+8.4',unit: '%',   icon: TrendingUp,  color: 'from-violet-500 to-violet-600', glow: 'rgba(139,92,246,0.3)'   },
  { label: 'Avg Speed',         value: '68',     delta: '+3.2',unit: 'km/h',icon: Activity,    color: 'from-emerald-500 to-teal-600',  glow: 'rgba(16,185,129,0.3)'   },
  { label: 'Fleet Uptime',      value: '99.7',   delta: '+0.2',unit: '%',   icon: BarChart3,   color: 'from-amber-500  to-orange-500', glow: 'rgba(245,158,11,0.3)'   },
];

/* ── Activity feed ── */
const ACTIVITY = [
  { title: 'Vehicle TN-01-AB-2345 departed', sub: 'Chennai → Bangalore',  color: '#3b82f6', time: '2m ago',  icon: MapPin       },
  { title: 'Low fuel: KA-09-XY-7890',        sub: 'Below 15% threshold',   color: '#f59e0b', time: '8m ago',  icon: Fuel         },
  { title: 'Delivery confirmed #1029',        sub: 'Mumbai warehouse',      color: '#22c55e', time: '14m ago', icon: CheckCircle2 },
  { title: 'Route deviated: DL-7C-3456',     sub: 'Recalculating…',        color: '#8b5cf6', time: '31m ago', icon: MapPin       },
  { title: 'Maintenance due: HR-26-AZ-0011', sub: 'Schedule service now',   color: '#ef4444', time: '1h ago',  icon: Wrench       },
];

/* ── Fleet health ── */
const HEALTH = [
  { label: 'Engine',    pct: 94, color: 'bg-emerald-500', glow: 'rgba(34,197,94,0.5)'   },
  { label: 'Fuel',      pct: 71, color: 'bg-blue-500',    glow: 'rgba(59,130,246,0.5)'  },
  { label: 'Tyres',     pct: 88, color: 'bg-violet-500',  glow: 'rgba(139,92,246,0.5)'  },
  { label: 'Brakes',    pct: 79, color: 'bg-amber-500',   glow: 'rgba(245,158,11,0.5)'  },
  { label: 'Electrics', pct: 96, color: 'bg-emerald-500', glow: 'rgba(34,197,94,0.5)'   },
];

/* ─────────────────────────────────────────── */

function StatCard({ stat, index }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.06 * index, duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -6, transition: { duration: 0.3 } }}
      className="metric-card"
      style={{ '--glow': stat.glow }}
    >
      <div className="flex items-start justify-between mb-4">
        <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center shadow-lg`}
             style={{ boxShadow: `0 0 20px ${stat.glow}` }}>
          <stat.icon size={18} className="text-white" />
        </div>
        <span className="text-emerald-400 text-xs font-bold bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
          {stat.delta}{stat.unit !== '%' ? '' : '%'}
        </span>
      </div>
      <p className="text-slate-400 text-xs font-medium mb-1 tracking-wide">{stat.label}</p>
      <p className="font-display text-2xl font-bold text-slate-50">
        {stat.value}
        {stat.unit !== '%' && <span className="text-sm font-medium text-slate-400 ml-1">{stat.unit}</span>}
      </p>
    </motion.div>
  );
}

function UserProfileCard({ user }) {
  const created = user?.created_at
    ? new Date(user.created_at).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })
    : '—';

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.35, duration: 0.45 }}
      whileHover={{ y: -4 }}
      className="metric-card"
    >
      <div className="flex items-center gap-3 mb-4">
        <div
          className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center text-xl font-bold text-white shadow-ag-md"
          style={{ boxShadow: '0 0 20px rgba(99,102,241,0.4)' }}
        >
          {user?.username?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || 'U'}
        </div>
        <div>
          <p className="font-display font-bold text-slate-50">{user?.username || '—'}</p>
          <p className="text-slate-400 text-xs">{user?.email || '—'}</p>
        </div>
      </div>

      <div className="space-y-2.5">
        <div className="flex items-center justify-between py-2 border-b border-slate-800">
          <span className="text-slate-500 text-xs font-medium flex items-center gap-1.5">
            <Shield size={11} /> Role
          </span>
          <span className="text-xs font-semibold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-full border border-blue-500/20 capitalize">
            {user?.role || 'user'}
          </span>
        </div>

        <div className="flex items-center justify-between py-2 border-b border-slate-800">
          <span className="text-slate-500 text-xs font-medium flex items-center gap-1.5">
            <CheckCircle2 size={11} /> Status
          </span>
          {user?.is_active !== false ? (
            <span className="status-active">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Active
            </span>
          ) : (
            <span className="status-inactive">
              <span className="w-1.5 h-1.5 rounded-full bg-red-400" />
              Inactive
            </span>
          )}
        </div>

        <div className="flex items-center justify-between py-2">
          <span className="text-slate-500 text-xs font-medium flex items-center gap-1.5">
            <Clock size={11} /> Joined
          </span>
          <span className="text-slate-300 text-xs font-medium">{created}</span>
        </div>
      </div>
    </motion.div>
  );
}

function HealthBar({ item, index }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-slate-400 text-xs font-medium w-16 flex-shrink-0">{item.label}</span>
      <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${item.color}`}
          initial={{ width: 0 }}
          animate={{ width: `${item.pct}%` }}
          transition={{ delay: 0.5 + index * 0.08, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          style={{ boxShadow: `0 0 8px ${item.glow}` }}
        />
      </div>
      <span className="text-slate-300 text-xs font-bold w-9 text-right">{item.pct}%</span>
    </div>
  );
}

/* ─── Main Dashboard ─────────────────────── */
export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate  = useNavigate();
  const [active, setActive]     = useState('overview');
  const [sidebarOpen, setSidebar] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);
    await new Promise(r => setTimeout(r, 800));
    logout();
    navigate('/');
  };

  return (
    <AnimatePresence>
      {!loggingOut && (
        <motion.div
          key="dashboard-shell"
          className="flex h-screen bg-slate-950 overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{
            opacity: 0, scale: 0.95, filter: 'blur(10px)',
            transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] },
          }}
        >
          {/* Background orbs */}
          <div className="fixed inset-0 pointer-events-none overflow-hidden">
            <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full opacity-10 animate-drift-1"
                 style={{ background: 'radial-gradient(circle, #3b82f6 0%, transparent 70%)', filter: 'blur(80px)' }} />
            <div className="absolute bottom-[-10%] right-[-5%] w-[400px] h-[400px] rounded-full opacity-10 animate-drift-2"
                 style={{ background: 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)', filter: 'blur(80px)' }} />
          </div>

          {/* ── Sidebar ──────────────────────────────── */}
          <motion.aside
            className="relative z-20 flex flex-col bg-slate-900/80 border-r border-slate-800/60 backdrop-blur-2xl"
            style={{ width: 240, flexShrink: 0 }}
            initial={{ x: -240, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* Logo */}
            <div className="flex items-center gap-3 p-5 pb-6">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center shadow-ag-sm">
                <svg viewBox="0 0 24 24" className="w-4 h-4 fill-white">
                  <path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zm-1.5 1.5 1.96 2.5H17V9.5h1.5zM6 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm11 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/>
                </svg>
              </div>
              <div>
                <p className="font-display font-bold text-sm gradient-text">FleetStat</p>
                <p className="text-[9px] tracking-[0.15em] uppercase text-slate-600">Platform V2</p>
              </div>
            </div>

            {/* Nav */}
            <nav className="flex-1 px-3 space-y-0.5">
              {NAV.map((item, i) => (
                <motion.button
                  key={item.id}
                  className={`
                    relative w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl
                    text-sm font-medium transition-all duration-200 group
                    ${active === item.id
                      ? 'text-white'
                      : 'text-slate-500 hover:text-slate-300 hover:bg-slate-800/50'
                    }
                  `}
                  onClick={() => setActive(item.id)}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0,   opacity: 1 }}
                  transition={{ delay: 0.08 * i, duration: 0.4 }}
                  whileHover={{ x: active !== item.id ? 2 : 0 }}
                >
                  {active === item.id && (
                    <motion.div
                      layoutId="nav-active"
                      className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-600/90 to-violet-600/90"
                      style={{ boxShadow: '0 0 20px rgba(99,102,241,0.3)' }}
                      transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                    />
                  )}
                  <item.icon size={16} className="relative z-10 flex-shrink-0" />
                  <span className="relative z-10">{item.label}</span>
                  {active === item.id && (
                    <ChevronRight size={13} className="relative z-10 ml-auto opacity-70" />
                  )}
                </motion.button>
              ))}
            </nav>

            {/* User + Logout */}
            <div className="p-3 border-t border-slate-800/60 space-y-2">
              {/* User card */}
              <div className="flex items-center gap-2.5 px-3 py-2.5 bg-slate-800/50 rounded-xl border border-slate-700/40">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
                  {user?.username?.[0]?.toUpperCase() || 'U'}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-slate-200 text-xs font-semibold truncate">{user?.username || 'User'}</p>
                  <p className="text-slate-500 text-[10px] capitalize">{user?.role || 'user'}</p>
                </div>
              </div>

              {/* Logout */}
              <motion.button
                className="w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-slate-500 text-sm font-medium border border-transparent hover:text-red-400 hover:bg-red-500/8 hover:border-red-500/20 transition-all duration-200"
                onClick={handleLogout}
                disabled={loggingOut}
                whileHover={{ x: 2 }}
                whileTap={{ scale: 0.97 }}
              >
                {loggingOut ? <Spinner size={15} /> : <LogOut size={15} />}
                <span>Sign out</span>
              </motion.button>
            </div>
          </motion.aside>

          {/* ── Main ──────────────────────────────────── */}
          <div className="flex-1 flex flex-col overflow-hidden">

            {/* Topbar */}
            <motion.header
              className="flex items-center justify-between px-6 py-4 bg-slate-900/60 border-b border-slate-800/60 backdrop-blur-xl"
              initial={{ y: -50, opacity: 0 }}
              animate={{ y: 0,  opacity: 1 }}
              transition={{ duration: 0.45, delay: 0.1 }}
            >
              <div>
                <h2 className="font-display text-xl font-bold text-slate-50 tracking-tight">
                  {NAV.find(n => n.id === active)?.label || 'Dashboard'}
                </h2>
                <p className="text-slate-500 text-xs flex items-center gap-1.5 mt-0.5">
                  <Clock size={11} />
                  {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                </p>
              </div>

              <div className="flex items-center gap-3">
                {/* Search */}
                <div className="flex items-center gap-2 bg-slate-800/60 border border-slate-700/50 rounded-xl px-3 py-2 text-slate-500 hover:border-slate-600/60 transition-colors">
                  <Search size={14} />
                  <input
                    placeholder="Search fleet…"
                    className="bg-transparent border-none outline-none text-sm text-slate-300 placeholder:text-slate-600 w-36"
                  />
                </div>

                {/* Notifications */}
                <motion.button
                  className="relative p-2.5 bg-slate-800/60 border border-slate-700/50 rounded-xl text-slate-400 hover:text-slate-200 hover:border-slate-600/60 transition-all"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Bell size={16} />
                  <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-slate-900" />
                </motion.button>
              </div>
            </motion.header>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6">
              <AnimatePresence mode="wait">
                <motion.div
                  key={active}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{    opacity: 0, y: -8 }}
                  transition={{ duration: 0.28 }}
                  className="space-y-5"
                >
                  {/* Greeting banner */}
                  <motion.div
                    initial={{ opacity: 0, scale: 0.98 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.1 }}
                    className="glass-card rounded-2xl px-6 py-5 flex items-center justify-between"
                    style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.1) 0%, rgba(139,92,246,0.08) 100%)' }}
                  >
                    <div>
                      <h3 className="font-display text-lg font-bold text-slate-50">
                        Good {getGreeting()}, {user?.username || 'Fleet Manager'}! 👋
                      </h3>
                      <p className="text-slate-400 text-sm mt-0.5">
                        Your fleet is performing well. All systems operational.
                      </p>
                    </div>
                    <div className="flex items-center gap-2 bg-emerald-500/15 border border-emerald-500/25 px-3 py-1.5 rounded-full hidden sm:flex">
                      <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                      <span className="text-emerald-400 text-xs font-semibold">All systems go</span>
                    </div>
                  </motion.div>

                  {/* Stats grid */}
                  <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    {STATS.map((s, i) => <StatCard key={s.label} stat={s} index={i} />)}
                  </div>

                  {/* Bottom row */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

                    {/* Activity feed */}
                    <motion.div
                      className="lg:col-span-2 metric-card"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.35 }}
                    >
                      <div className="flex items-center justify-between mb-4">
                        <h4 className="font-display font-bold text-slate-200 text-sm">Recent Activity</h4>
                        <div className="flex items-center gap-1.5 text-emerald-400 text-xs font-semibold">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                          Live
                        </div>
                      </div>
                      <div className="space-y-0">
                        {ACTIVITY.map((a, i) => (
                          <motion.div
                            key={i}
                            className="flex items-center gap-3 py-3 border-b border-slate-800/60 last:border-0 group cursor-default"
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.4 + 0.06 * i }}
                            whileHover={{ x: 3 }}
                          >
                            <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                                 style={{ background: a.color + '20', border: `1px solid ${a.color}35` }}>
                              <a.icon size={14} style={{ color: a.color }} />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-slate-200 text-xs font-semibold truncate">{a.title}</p>
                              <p className="text-slate-500 text-[11px] truncate">{a.sub}</p>
                            </div>
                            <span className="text-slate-600 text-[10px] font-medium whitespace-nowrap">{a.time}</span>
                          </motion.div>
                        ))}
                      </div>
                    </motion.div>

                    {/* Right column: User profile + Health */}
                    <div className="space-y-4">
                      <UserProfileCard user={user} />

                      <motion.div
                        className="metric-card"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.42 }}
                      >
                        <h4 className="font-display font-bold text-slate-200 text-sm mb-4">Fleet Health</h4>
                        <div className="space-y-3">
                          {HEALTH.map((h, i) => <HealthBar key={h.label} item={h} index={i} />)}
                        </div>
                      </motion.div>
                    </div>
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>
          </div>
        </motion.div>
      )}

      {/* Logout transition overlay */}
      {loggingOut && (
        <motion.div
          key="logout-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 z-50 bg-slate-950 flex items-center justify-center"
        >
          <motion.div
            className="flex flex-col items-center gap-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <motion.div
              className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center"
              animate={{ rotate: [0, 0, 180, 180, 360], scale: [1, 1.1, 1.1, 1, 1] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
              style={{ boxShadow: '0 0 30px rgba(99,102,241,0.5)' }}
            >
              <svg viewBox="0 0 24 24" className="w-6 h-6 fill-white">
                <path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4z"/>
              </svg>
            </motion.div>
            <p className="text-slate-500 text-sm font-medium">Signing out…</p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

const getGreeting = () => {
  const h = new Date().getHours();
  return h < 12 ? 'morning' : h < 17 ? 'afternoon' : 'evening';
};
