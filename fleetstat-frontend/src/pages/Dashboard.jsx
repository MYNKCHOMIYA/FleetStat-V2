/**
 * Dashboard.jsx
 * =============
 * Main analytics workspace for FleetStat.
 *
 * Structure (top → bottom):
 *   imports → constants → helpers → CountUpValue component → Dashboard component
 *     Dashboard internals:
 *       state & effects → derived values → render (sidebar + header + KPI + grid)
 *
 * To add a new page: replace the onClick handlers inside .sidebar-nav buttons
 * with react-router-dom <Link> or useNavigate() calls.
 */

import { useEffect, useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import api from "../services/api";
import "../styles/dashboard.css";


/* ================================================================
   CONSTANTS
   ================================================================ */

/**
 * Sidebar navigation items.
 * badge: "Live"  — currently wired up
 * badge: "Soon"  — placeholder; replace onClick with a router link later
 */
const navItems = [
  { label: "Overview",  badge: "Live" },
  { label: "Drivers",   badge: "Soon" },
  { label: "Trucks",    badge: "Soon" },
  { label: "Fuel Logs", badge: "Soon" },
  { label: "Damage",    badge: "Soon" },
  { label: "Analytics", badge: "Soon" },
];

/**
 * Chart colour palette — shared by area, pie, and bar charts.
 * To change a colour, edit the hex value at the matching index.
 *   [0] gold  [1] teal  [2] green  [3] red  [4] purple
 */
const chartColors = ["#ff9a1a", "#16c8c8", "#22c55e", "#ef4444", "#8b5cf6"];

/**
 * Compact layout breakpoint.
 * Auto-collapse is useful on mobile/tablet or short screens, but annoying on a
 * full desktop layout. This query controls where scroll/touch should hide the
 * sidebar automatically.
 */
const COMPACT_VIEWPORT_QUERY = "(max-width: 1180px), (max-height: 760px)";


/* ================================================================
   FORMATTERS
   Small pure functions that convert raw numbers to display strings.
   ================================================================ */

/**
 * Formats a number as Indian Rupee currency (no decimal places).
 * Used on KPI cards, chart tooltips, and table rows.
 */
const formatCurrency = (value = 0) =>
  new Intl.NumberFormat("en-IN", {
    style:                "currency",
    currency:             "INR",
    maximumFractionDigits: 0,
  }).format(value);

/**
 * Formats a count using the Indian numbering system (lakhs/crores).
 * Used on KPI cards, summary table, and the utilization meter.
 */
const formatNumber = (value = 0) =>
  new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 }).format(value);

/**
 * Returns the integer percentage of part relative to total.
 * Returns 0 when total is 0 to prevent divide-by-zero crashes.
 */
const getPercent = (part = 0, total = 0) =>
  total > 0 ? Math.round((part / total) * 100) : 0;


/* ================================================================
   COUNT-UP VALUE COMPONENT
   Animates a number from 0 → target value using requestAnimationFrame.
   Uses a cubic ease-out curve so numbers decelerate smoothly.
   Props:
     value     — target number to animate to
     formatter — function that formats the raw number (default: formatNumber)
     duration  — animation length in ms (default: 900)
   ================================================================ */
function CountUpValue({ value = 0, formatter = formatNumber, duration = 900 }) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let frameId;
    const startTime = performance.now();
    const target    = Number(value) || 0;

    const animate = (currentTime) => {
      const progress = Math.min((currentTime - startTime) / duration, 1);

      // Cubic ease-out: fast start, smooth deceleration at the end.
      const easedProgress = 1 - Math.pow(1 - progress, 3);

      setDisplayValue(target * easedProgress);

      // Continue until progress reaches 1 (animation complete).
      if (progress < 1) {
        frameId = requestAnimationFrame(animate);
      }
    };

    frameId = requestAnimationFrame(animate);

    // Cleanup: cancel any pending frame if value changes mid-animation.
    return () => cancelAnimationFrame(frameId);
  }, [value, duration]);

  return <>{formatter(displayValue)}</>;
}


/* ================================================================
   DASHBOARD COMPONENT
   ================================================================ */
function Dashboard() {

  /* ── STATE ──────────────────────────────────────────────────── */

  // Backend API data
  const [stats,  setStats]  = useState(null); // KPI card data from /analytics/dashboard
  const [charts, setCharts] = useState(null); // Chart data from /analytics/dashboard/charts

  // Sidebar visibility flags
  const [isSidebarOpen,      setSidebarOpen]      = useState(false); // Mobile: drawer open/close
  const [isSidebarCollapsed, setSidebarCollapsed] = useState(false); // Desktop: rail collapse
  const [isCompactViewport,  setCompactViewport]  = useState(false); // Mobile/tablet/short-screen behaviour

  // UI interaction state
  const [activeNav,     setActiveNav]     = useState("Overview"); // Highlighted nav item
  const [range,         setRange]         = useState("All");      // Chart time-range filter
  const [focusedMetric, setFocusedMetric] = useState("Revenue");  // Highlighted KPI card / chart tab
  const [error,         setError]         = useState("");         // API error message


  /* ── DATA FETCH ─────────────────────────────────────────────── */

  useEffect(() => {
    // Load both endpoints simultaneously; set data only when both resolve.
    Promise.all([
      api.get("/analytics/dashboard"),
      api.get("/analytics/dashboard/charts"),
    ])
      .then(([statsRes, chartRes]) => {
        setStats(statsRes.data);
        setCharts(chartRes.data);
      })
      .catch(() => setError("Dashboard data could not be loaded."));
  }, []);


  /* ── VIEWPORT MODE EFFECT ───────────────────────────────────── */

  useEffect(() => {
    /**
     * Keeps React aware of whether the UI is in compact mode.
     * When returning to full desktop, force the sidebar open again because
     * full view should stay expanded unless the user manually collapses it.
     */
    const compactMedia = window.matchMedia(COMPACT_VIEWPORT_QUERY);

    const syncViewportMode = () => {
      const isCompact = compactMedia.matches;

      setCompactViewport(isCompact);

      if (!isCompact) {
        setSidebarOpen(false);
        setSidebarCollapsed(false);
      }
    };

    syncViewportMode();

    if (compactMedia.addEventListener) {
      compactMedia.addEventListener("change", syncViewportMode);
      return () => compactMedia.removeEventListener("change", syncViewportMode);
    }

    // Older browser fallback for matchMedia.
    compactMedia.addListener(syncViewportMode);
    return () => compactMedia.removeListener(syncViewportMode);
  }, []);


  /* ── COMPACT SCROLL-TO-COLLAPSE EFFECT ──────────────────────── */

  useEffect(() => {
    // Full desktop should not auto-collapse on scroll.
    if (!isCompactViewport) return undefined;

    let frameId;

    /**
     * Collapses the sidebar when compact/mobile users scroll or wheel.
     * requestAnimationFrame batches rapid scroll events into one update,
     * preventing excessive state re-renders during fast scrolling.
     */
    const collapseSidebar = (event) => {
      if (event?.target?.closest?.(".dashboard-sidebar")) return;

      cancelAnimationFrame(frameId);
      frameId = requestAnimationFrame(() => {
        setSidebarCollapsed(true);
        setSidebarOpen(false);
      });
    };

    // passive: true tells the browser these listeners won't call preventDefault(),
    // which allows the browser to optimise scroll performance.
    window.addEventListener("scroll",    collapseSidebar, { passive: true });
    window.addEventListener("wheel",     collapseSidebar, { passive: true });
    window.addEventListener("touchmove", collapseSidebar, { passive: true });

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener("scroll",    collapseSidebar);
      window.removeEventListener("wheel",     collapseSidebar);
      window.removeEventListener("touchmove", collapseSidebar);
    };
  }, [isCompactViewport]);


  /* ── DERIVED DATA ───────────────────────────────────────────── */

  /**
   * Merges the two separate backend arrays (monthly_revenue and
   * monthly_fuel_cost) into a single array keyed by month string.
   * Also computes profit = revenue − fuel_cost for each month.
   * shortMonth is truncated for the X-axis label.
   */
  const monthlyData = useMemo(() => {
    const revenue = charts?.monthly_revenue   || [];
    const fuel    = charts?.monthly_fuel_cost || [];
    const byMonth = new Map();

    // Seed the map with revenue rows.
    revenue.forEach((item) => {
      byMonth.set(item.month, {
        month:     item.month,
        revenue:   item.revenue  || 0,
        fuel_cost: 0,
      });
    });

    // Merge fuel cost into the matching month, creating a new row if missing.
    fuel.forEach((item) => {
      const current = byMonth.get(item.month) || {
        month:     item.month,
        revenue:   0,
        fuel_cost: 0,
      };
      byMonth.set(item.month, { ...current, fuel_cost: item.fuel_cost || 0 });
    });

    // Convert Map → Array and attach profit + shortMonth.
    return Array.from(byMonth.values()).map((item) => ({
      ...item,
      profit:     item.revenue - item.fuel_cost,
      shortMonth: item.month.split(" ")[0], // e.g. "June 2024" → "June"
    }));
  }, [charts]);

  /**
   * Slices monthlyData according to the selected range button.
   * No new API call is made — the full dataset is trimmed client-side.
   */
  const visibleMonthlyData = useMemo(() => {
    if (range === "3M")  return monthlyData.slice(-3);
    if (range === "6M")  return monthlyData.slice(-6);
    if (range === "9M")  return monthlyData.slice(-9);
    if (range === "12M") return monthlyData.slice(-12);
    return monthlyData; // "All" — no slice
  }, [monthlyData, range]);

  // Distribution arrays used by pie and bar charts.
  const shipmentStatus = charts?.shipment_status_distribution || [];
  const tripStatus     = charts?.trip_status_distribution     || [];

  // Aggregate counts used on cards and the summary panel.
  const totalTrips    = (stats?.active_trips    || 0) + (stats?.completed_trips || 0);
  const totalShipments = stats?.total_shipments || 0;

  // Percentage values for progress bars and the utilization ring.
  const activeTruckPercent     = getPercent(stats?.active_trucks,    stats?.total_trucks);
  const pendingShipmentPercent = getPercent(stats?.pending_shipments, totalShipments);
  const profitMargin           = getPercent(stats?.total_profit,      stats?.total_revenue);

  /**
   * KPI card configuration array.
   * Each entry maps to one .metric-card in the .kpi-grid.
   *   label     — displayed label text
   *   value     — raw number passed to CountUpValue
   *   formatter — currency or number formatter
   *   suffix    — optional text appended after the count (e.g. " / 10")
   *   meta      — sub-label below the count
   *   tone      — CSS tone class suffix: gold | green | blue | red
   *   progress  — 0–100 integer for the progress bar fill
   */
  const kpis = [
    {
      label:     "Total Revenue",
      value:     stats?.total_revenue,
      formatter: formatCurrency,
      meta:      `${profitMargin}% margin`,
      tone:      "gold",
      progress:  Math.min(Math.max(profitMargin, 0), 100),
    },
    {
      label:     "Total Profit",
      value:     stats?.total_profit,
      formatter: formatCurrency,
      meta:      `${formatCurrency(stats?.fuel_cost)} fuel cost`,
      tone:      "green",
      progress:  Math.min(Math.max(profitMargin, 0), 100),
    },
    {
      label:     "Active Trucks",
      value:     stats?.active_trucks,
      formatter: formatNumber,
      suffix:    ` / ${formatNumber(stats?.total_trucks)}`,
      meta:      `${activeTruckPercent}% fleet ready`,
      tone:      "blue",
      progress:  activeTruckPercent,
    },
    {
      label:     "Pending Shipments",
      value:     stats?.pending_shipments,
      formatter: formatNumber,
      meta:      `${pendingShipmentPercent}% need action`,
      tone:      "red",
      progress:  pendingShipmentPercent,
    },
  ];

  /**
   * Operational summary table rows.
   * Each entry maps to one clickable button in the .data-table.
   *   label  — row heading
   *   value  — count shown on the right
   *   status — sub-label below the heading
   */
  const operationalRows = [
    { label: "Drivers",          value: stats?.total_drivers,   status: "Available roster"    },
    { label: "Trips in progress", value: stats?.active_trips,    status: "Currently moving"   },
    { label: "Completed trips",  value: stats?.completed_trips, status: "Closed routes"       },
    { label: "Total shipments",  value: stats?.total_shipments, status: "All shipment records" },
  ];

  /**
   * Logs out the current user by clearing the auth token from
   * localStorage and reloading the page, which will redirect to login.
   */
  const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
  };

  /**
   * Manual collapse button.
   * Works on full desktop too, because the user explicitly asked for it.
   */
  const toggleSidebarCollapse = () => {
    setSidebarCollapsed((prev) => !prev);
  };

  /**
   * Mobile persistent menu button.
   * Opening the drawer clears the collapsed rail state so mobile always shows
   * the full labels inside the drawer.
   */
  const toggleMobileSidebar = () => {
    setSidebarOpen((prev) => {
      const nextOpen = !prev;

      if (nextOpen) {
        setSidebarCollapsed(false);
      }

      return nextOpen;
    });
  };

  /**
   * Tap/click outside the sidebar in compact mode.
   * On mobile web/Android, touching the dashboard content closes the drawer.
   * On full desktop this does nothing, so the sidebar stays stable.
   */
  const closeCompactSidebarFromContent = (event) => {
    if (!isCompactViewport) return;
    if (event.target.closest(".menu-toggle")) return;

    setSidebarOpen(false);
    setSidebarCollapsed(true);
  };


  /* ── EARLY RETURNS ──────────────────────────────────────────── */

  // API error state — shown when either analytics endpoint fails.
  if (error) {
    return (
      <main className="dashboard-shell">
        <section className="dashboard-state">
          <span className="state-icon">!</span>
          <h1>FleetStat Dashboard</h1>
          <p>{error}</p>
          <button className="primary-action" onClick={() => window.location.reload()}>
            Retry
          </button>
        </section>
      </main>
    );
  }

  // Loading state — shown until both API responses have resolved.
  if (!stats || !charts) {
    return (
      <main className="dashboard-shell">
        <section className="dashboard-state">
          <span className="loading-ring" />
          <h1>FleetStat Dashboard</h1>
          <p>Loading fleet analytics…</p>
        </section>
      </main>
    );
  }


  /* ── MAIN RENDER ────────────────────────────────────────────── */

  return (
    /*
     * .sidebar-collapsed adds --sidebar-width: 88px to the shell grid,
     * triggering the CSS transition that smoothly narrows the sidebar column.
     */
    <main className={`dashboard-shell${isSidebarCollapsed ? " sidebar-collapsed" : ""}`}>


      {/* ============================================================
          SIDEBAR
          Desktop: sticky rail that collapses to icon-only.
          Mobile : fixed off-screen drawer that slides in on .is-open.
          ============================================================ */}
      <aside
        className={[
          "dashboard-sidebar",
          isSidebarOpen      ? "is-open"      : "",
          isSidebarCollapsed ? "is-collapsed" : "",
        ].join(" ").trim()}
      >
        <div className="sidebar-inner">

          {/* ── Collapse toggle button ─────────────────────────── */}
          <button
            className="sidebar-collapse-btn"
            type="button"
            onClick={toggleSidebarCollapse}
            aria-label={isSidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            title={isSidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {/* CSS-only chevron — direction flips via CSS transform. */}
            <span className="collapse-icon" aria-hidden="true" />
          </button>

          {/* ── Brand logo + name ──────────────────────────────── */}
          <div className="sidebar-brand">
            {/* Circular amber badge — always visible even when collapsed. */}
            <span className="brand-mark">FS</span>

            {/* Text slides out as sidebar collapses (opacity + max-width). */}
            <div className="sidebar-copy">
              <strong>FleetStat</strong>
              <small>Control center</small>
            </div>
          </div>

          {/* ── Navigation items ───────────────────────────────── */}
          {/*
           * Replace onClick with react-router-dom navigation when pages exist.
           * The title prop shows the label as a tooltip in collapsed mode.
           */}
          <nav className="sidebar-nav" aria-label="Dashboard sections">
            {navItems.map((item) => (
              <button
                key={item.label}
                className={activeNav === item.label ? "active" : ""}
                onClick={() => {
                  setActiveNav(item.label);
                  setSidebarOpen(false); // close drawer on mobile after tap
                }}
                title={isSidebarCollapsed ? item.label : undefined}
              >
                {/* First letter of the label as the icon glyph. */}
                <span className="nav-icon" aria-hidden="true">
                  {item.label.slice(0, 1)}
                </span>

                {/* Full label — hidden in collapsed mode via CSS. */}
                <span className="nav-label">{item.label}</span>

                {/* Status badge — hidden in collapsed mode via CSS. */}
                <small>{item.badge}</small>
              </button>
            ))}
          </nav>

          {/* ── Future modules info panel ──────────────────────── */}
          {/* This panel collapses to height 0 when the rail is narrow. */}
          <div className="sidebar-panel">
            <span>Next modules</span>
            <p>
              Driver, truck, fuel logs, damage summary, and deeper analytics
              can connect here later.
            </p>
          </div>

          {/* ── Logout button (sidebar footer) ─────────────────── */}
          {/* margin-top: auto in CSS pushes this to the bottom. */}
          <button 
            className="logout-btn sidebar-logout"
            onClick={logout}
            title="Logout"
          >
            <span className="logout-icon" aria-hidden="true">L</span>
            <span className="logout-label">Logout</span>
          </button>

        </div>
      </aside>


      {/* ============================================================
          MAIN CONTENT AREA
          Compact mode:
            - wheel/touch movement collapses the drawer/rail
            - tapping dashboard content closes the mobile drawer
          Full desktop mode:
            - these handlers do nothing, keeping the sidebar visible
          ============================================================ */}
      <section
        className="dashboard-content"
        onPointerDown={closeCompactSidebarFromContent}
        onWheel={closeCompactSidebarFromContent}
        onTouchMove={closeCompactSidebarFromContent}
      >

        {/* ==========================================================
            HEADER
            [hamburger] [title block] [range tabs]
            ========================================================== */}
        <header className="dashboard-header">

          {/* Mobile-only hamburger — toggles the drawer. */}
          <button
            className="menu-toggle"
            type="button"
            onClick={toggleMobileSidebar}
            aria-label="Open navigation menu"
          >
            <span />
            <span />
            <span />
          </button>

          {/* Title block: eyebrow label + main heading + description. */}
          <div className="dashboard-title">
            <h1>FleetStat Dashboard</h1>
            <p>Revenue, operations, shipment movement, and fleet readiness in one workspace.</p>
          </div>

          {/* Right-side controls: time-range segmented tabs. */}
          <div className="header-actions">
            {/*
             * Range buttons trim the chart data client-side.
             * No new API call is made when switching range.
             */}
            <div className="range-tabs" aria-label="Chart time range">
              {["3M", "6M", "9M", "12M", "All"].map((label) => (
                <button
                  key={label}
                  className={range === label ? "active" : ""}
                  onClick={() => setRange(label)}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

        </header>


        {/* ==========================================================
            KPI CARDS GRID
            Four interactive metric cards — clicking one sets
            focusedMetric which also drives the chart tab highlight.
            ========================================================== */}
        <section className="kpi-grid" aria-label="Key fleet metrics">
          {kpis.map((card) => (
            <article
              key={card.label}
              className={[
                "metric-card",
                `tone-${card.tone}`,
                focusedMetric === card.label ? "selected" : "",
              ].join(" ").trim()}
              onClick={() => setFocusedMetric(card.label)}
              tabIndex={0}
              onKeyDown={(e) => { if (e.key === "Enter") setFocusedMetric(card.label); }}
            >
              <div>
                {/* Card label (e.g. "TOTAL REVENUE"). */}
                <span>{card.label}</span>

                {/* Animated count + optional suffix (e.g. " / 10"). */}
                <strong>
                  <CountUpValue value={card.value} formatter={card.formatter} />
                  {card.suffix || ""}
                </strong>

                {/* Sub-label below the count (e.g. "93% margin"). */}
                <small>{card.meta}</small>
              </div>

              {/* Progress bar at the bottom of the card. */}
              <div className="metric-progress" aria-hidden="true">
                {/* width is set as an inline style; CSS transitions animate it. */}
                <span style={{ width: `${card.progress}%` }} />
              </div>
            </article>
          ))}
        </section>


        {/* ==========================================================
            ANALYTICS GRID
            Left column  : revenue area chart
            Right column : utilization meter / shipment pie / trip bar /
                           summary table / quick-actions
            ========================================================== */}
        <section className="dashboard-grid">


          {/* ── Revenue vs Fuel Area Chart ─────────────────────── */}
          <article className="analytics-panel revenue-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Financial trend</span>
                <h2>Revenue vs fuel cost</h2>
              </div>

              {/* Metric-focus tabs: clicking one changes focusedMetric. */}
              <div className="metric-switch">
                {["Revenue", "Fuel", "Profit"].map((label) => (
                  <button
                    key={label}
                    className={focusedMetric === label ? "active" : ""}
                    onClick={() => setFocusedMetric(label)}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            {/* chart-wrap.tall gives the area chart extra vertical space. */}
            <div className="chart-wrap tall">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={visibleMonthlyData}>
                  <defs>
                    {/* Revenue fill gradient — from semi-transparent amber to clear. */}
                    <linearGradient id="revenueFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#ff9a1a" stopOpacity={0.36} />
                      <stop offset="95%" stopColor="#ff9a1a" stopOpacity={0.02} />
                    </linearGradient>
                    {/* Fuel fill gradient — from semi-transparent teal to clear. */}
                    <linearGradient id="fuelFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#16c8c8" stopOpacity={0.28} />
                      <stop offset="95%" stopColor="#16c8c8" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>

                  {/* Horizontal grid lines only (vertical=false). */}
                  <CartesianGrid stroke="rgba(255,255,255,0.07)" vertical={false} />

                  {/* X-axis: month abbreviations. */}
                  <XAxis dataKey="shortMonth" tickLine={false} axisLine={false} />

                  {/* Y-axis: compact thousands labels (e.g. "320k"). */}
                  <YAxis
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(v) => `${Math.round(v / 1000)}k`}
                  />

                  {/* Tooltip: dark glass popup with amber border. */}
                  <Tooltip
                    formatter={(v) => formatCurrency(v)}
                    contentStyle={{
                      background:   "#08101f",
                      border:       "1px solid rgba(255,154,26,0.26)",
                      borderRadius: 8,
                    }}
                  />

                  {/* Revenue area (amber). */}
                  <Area
                    type="monotone"
                    dataKey="revenue"
                    stroke="#ff9a1a"
                    fill="url(#revenueFill)"
                    strokeWidth={3}
                  />

                  {/* Fuel cost area (teal). */}
                  <Area
                    type="monotone"
                    dataKey="fuel_cost"
                    stroke="#16c8c8"
                    fill="url(#fuelFill)"
                    strokeWidth={2}
                  />

                  {/* Profit line (green) — no fill, just the stroke. */}
                  <Line
                    type="monotone"
                    dataKey="profit"
                    stroke="#22c55e"
                    strokeWidth={2}
                    dot={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </article>


          {/* ── Truck Utilization Meter ────────────────────────── */}
          <article className="analytics-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Fleet readiness</span>
                <h2>Truck utilization</h2>
              </div>
            </div>

            <div className="utilization-meter">
              {/*
               * --value is the conic-gradient stop angle.
               * activeTruckPercent × 3.6 converts percent → degrees (0–360).
               */}
              <div
                className="meter-ring"
                style={{ "--value": `${activeTruckPercent * 3.6}deg` }}
              >
                <strong>
                  <CountUpValue value={activeTruckPercent} />%
                </strong>
                <span>active</span>
              </div>

              {/* Three stat rows beside the ring. */}
              <div className="meter-details">
                <p>
                  <strong>{formatNumber(stats.active_trucks)}</strong> active trucks
                </p>
                <p>
                  <strong>{formatNumber(stats.total_trucks - stats.active_trucks)}</strong>{" "}
                  inactive or unavailable
                </p>
                <p>
                  <strong>{formatNumber(stats.total_drivers)}</strong> drivers in roster
                </p>
              </div>
            </div>
          </article>


          {/* ── Shipment Status Pie Chart ──────────────────────── */}
          <article className="analytics-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Shipment mix</span>
                <h2>Status distribution</h2>
              </div>
            </div>

            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={shipmentStatus}
                    dataKey="count"
                    nameKey="status"
                    innerRadius="58%"
                    outerRadius="82%"
                    paddingAngle={4}
                  >
                    {/* Each slice gets the next colour from the palette. */}
                    {shipmentStatus.map((entry, index) => (
                      <Cell
                        key={entry.status}
                        fill={chartColors[index % chartColors.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background:   "#08101f",
                      border:       "1px solid rgba(255,154,26,0.26)",
                      borderRadius: 8,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Colour-coded legend pills below the chart. */}
            <div className="legend-list">
              {shipmentStatus.map((item, index) => (
                <span key={item.status}>
                  <i style={{ background: chartColors[index % chartColors.length] }} />
                  {item.status}: {item.count}
                </span>
              ))}
            </div>
          </article>


          {/* ── Trip Status Bar Chart ──────────────────────────── */}
          <article className="analytics-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Trip pipeline</span>
                <h2>Trips by status</h2>
              </div>
            </div>

            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={tripStatus}>
                  <CartesianGrid stroke="rgba(255,255,255,0.07)" vertical={false} />
                  <XAxis dataKey="status" tickLine={false} axisLine={false} />
                  <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                  <Tooltip
                    contentStyle={{
                      background:   "#08101f",
                      border:       "1px solid rgba(255,154,26,0.26)",
                      borderRadius: 8,
                    }}
                  />
                  {/* Rounded top corners on bars (radius: [top-l, top-r, btm-r, btm-l]). */}
                  <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                    {tripStatus.map((entry, index) => (
                      <Cell
                        key={entry.status}
                        fill={chartColors[index % chartColors.length]}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </article>


          {/* ── Operational Summary Table ──────────────────────── */}
          {/*
           * Each row is a <button> so it can navigate to a detail page later.
           * Clicking a row also updates focusedMetric for visual feedback.
           */}
          <article className="analytics-panel table-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Operational summary</span>
                <h2>Today at a glance</h2>
              </div>
              {/* Pill showing total trip count. */}
              <span className="panel-pill">{formatNumber(totalTrips)} trips</span>
            </div>

            <div className="data-table">
              {operationalRows.map((row) => (
                <button
                  key={row.label}
                  onClick={() => setFocusedMetric(row.label)}
                >
                  <span>{row.label}</span>
                  <strong>
                    <CountUpValue value={row.value} />
                  </strong>
                  <small>{row.status}</small>
                </button>
              ))}
            </div>
          </article>


          {/* ── Quick Actions Panel ────────────────────────────── */}
          {/*
           * Placeholder buttons — wire up to router.push() or modals
           * once the individual pages exist.
           */}
          <article className="analytics-panel action-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Quick actions</span>
                <h2>Ready for pages</h2>
              </div>
            </div>

            <div className="quick-actions">
              {[
                "Add driver",
                "Register truck",
                "Fuel entry",
                "Damage report",
                "Shipment log",
                "Full analytics",
              ].map((label) => (
                <button key={label} onClick={() => setActiveNav(label)}>
                  {label}
                </button>
              ))}
            </div>
          </article>


        </section>{/* end .dashboard-grid */}
      </section>{/* end .dashboard-content */}
    </main>
  );
}

export default Dashboard;
