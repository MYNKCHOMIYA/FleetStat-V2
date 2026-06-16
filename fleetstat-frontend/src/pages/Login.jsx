import { useState, useEffect, useRef } from "react";
import api from "../services/api";

// ─── Fleet data rows (mirrors your actual DB entities) ───────────────────────
// Trucks, Drivers, Trips, Shipments, Containers, Fuel, Revenue, Damage Reports
const FLEET_ROWS = [
  {
    items: [
      { text: "MH 12 AB 3456", type: "truck" },
      { text: "TRIP-2847  Active", type: "trip" },
      { text: "Rajesh Kumar", type: "driver" },
      { text: "SHP-0451  In Transit", type: "shipment" },
      { text: "₹2,84,500", type: "revenue" },
      { text: "432 L  Diesel", type: "fuel" },
      { text: "CNT-2341  Loaded", type: "container" },
      { text: "KA 05 MN 7654", type: "truck" },
      { text: "On Route", type: "status" },
      { text: "TRIP-3018  Running", type: "trip" },
    ],
    dir: "left",
    duration: 42,
  },
  {
    items: [
      { text: "DL 01 KA 9870", type: "truck" },
      { text: "Mohammed Ali", type: "driver" },
      { text: "TRIP-1923  Done", type: "trip" },
      { text: "₹1,12,800", type: "revenue" },
      { text: "890 km", type: "fuel" },
      { text: "SHP-0782  Delivered", type: "shipment" },
      { text: "Suresh Patel", type: "driver" },
      { text: "CNT-1892  Unloaded", type: "container" },
      { text: "UP 32 CD 4521", type: "truck" },
      { text: "Service OK", type: "status" },
    ],
    dir: "right",
    duration: 34,
  },
  {
    items: [
      { text: "TRIP-3012  Running", type: "trip" },
      { text: "Vikram Singh", type: "driver" },
      { text: "SHP-0613  Loading", type: "shipment" },
      { text: "CNT-3041  Transit", type: "container" },
      { text: "₹4,56,200", type: "revenue" },
      { text: "620 L  Diesel", type: "fuel" },
      { text: "GJ 15 EF 8832", type: "truck" },
      { text: "Maintenance Due", type: "damage" },
      { text: "TRIP-2910  Active", type: "trip" },
      { text: "₹98,400", type: "revenue" },
    ],
    dir: "left",
    duration: 48,
  },
  {
    items: [
      { text: "Anil Sharma", type: "driver" },
      { text: "TRIP-2199  Done", type: "trip" },
      { text: "SHP-0334  Pending", type: "shipment" },
      { text: "₹87,450", type: "revenue" },
      { text: "Damage Report #14", type: "damage" },
      { text: "CNT-2891  Empty", type: "container" },
      { text: "TN 09 GH 2210", type: "truck" },
      { text: "1,240 km Route", type: "fuel" },
      { text: "Pradeep Nair", type: "driver" },
    ],
    dir: "right",
    duration: 38,
  },
  {
    items: [
      { text: "TRIP-3341  Active", type: "trip" },
      { text: "SHP-0967  In Transit", type: "shipment" },
      { text: "₹3,21,750", type: "revenue" },
      { text: "CNT-4012  Full", type: "container" },
      { text: "810 km Route", type: "fuel" },
      { text: "RJ 14 IJ 6643", type: "truck" },
      { text: "Fuel: 510 L", type: "fuel" },
      { text: "Manoj Tiwari", type: "driver" },
      { text: "TRIP-2556  Done", type: "trip" },
    ],
    dir: "left",
    duration: 45,
  },
  {
    items: [
      { text: "SHP-0218  Delivered", type: "shipment" },
      { text: "₹1,95,300", type: "revenue" },
      { text: "380 L  Diesel", type: "fuel" },
      { text: "CNT-1234  Unloaded", type: "container" },
      { text: "HR 26 KL 3389", type: "truck" },
      { text: "Damage Report #08", type: "damage" },
      { text: "TRIP-2003  Done", type: "trip" },
      { text: "Santosh Yadav", type: "driver" },
      { text: "₹2,40,000", type: "revenue" },
    ],
    dir: "right",
    duration: 30,
  },
];

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [focusedField, setFocusedField] = useState(null);
    const [errorMsg, setErrorMsg] = useState("");
    const [errorShake, setErrorShake] = useState(false);
    const [loginSuccess, setLoginSuccess] = useState(false);
    const cardRef = useRef(null);

    const handleLogin = async (e) => {
        e.preventDefault();
        

        if(!username.trim() && !password.trim()){
            setErrorMsg("Username and password cannot be empty");
            setErrorShake(true);
            setTimeout(() => setErrorShake(false), 650);
            return;
        }

        if(!username.trim()){
            setErrorMsg("Username cannot be empty");
            setErrorShake(true);
            setTimeout(() => setErrorShake(false), 650);
            return;
        }

        if(!password){
            setErrorMsg("Password cannot be empty");
            setErrorShake(true);
            setTimeout(() => setErrorShake(false), 650);
            return;
        }

        setErrorMsg("");
        setIsLoading(true);


        try {
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            const response = await api.post("/api/v1/auth/login", formData);
            localStorage.setItem("token", response.data.access_token);

            setLoginSuccess(true);
            setTimeout(() => { window.location.reload(); }, 800);
        } catch (error) {
            const msg = error.response?.data?.detail || "Invalid username or password";
            setErrorMsg(msg);
            setErrorShake(true);
            setTimeout(() => setErrorShake(false), 650);
        } finally {
            setIsLoading(false);
        }
    };

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
        if (errorMsg) setErrorMsg("");
    };
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        if (errorMsg) setErrorMsg("");
    };

    useEffect(() => {
        if (localStorage.getItem("token")) window.location.reload();
    }, []);

    return (
        <div className="login-root">

            {/* ── LEFT: Fleet animation canvas ─────────────────────── */}
            <div className="fleet-canvas" aria-hidden="true">
                {/* Brand tag top-left */}
                <div className="fleet-brand">
                    <svg width="22" height="22" viewBox="0 0 38 38" fill="none">
                        <circle cx="19" cy="19" r="18" stroke="rgba(255,160,30,0.6)" strokeWidth="1.5" />
                        <path d="M8 22h6l2-8h6l2 6h6" stroke="#ff9a1a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <circle cx="13" cy="26" r="2.5" fill="#ff9a1a" />
                        <circle cx="25" cy="26" r="2.5" fill="#ff9a1a" />
                    </svg>
                    <span>FleetStat</span>
                </div>

                {/* Marquee rows */}
                <div className="fleet-rows-wrapper">
                    {FLEET_ROWS.map((row, ri) => (
                        <div key={ri} className="fleet-row">
                            <div
                                className={`fleet-row-track${row.dir === "right" ? " dir-right" : ""}`}
                                style={{ "--dur": `${row.duration}s` }}
                            >
                                {/* duplicated for seamless infinite loop */}
                                {[...row.items, ...row.items].map((tag, ti) => (
                                    <span key={ti} className={`fleet-tag tag-${tag.type}`}>
                                        {tag.text}
                                    </span>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Central headline overlay */}
                <div className="fleet-headline">
                    <p className="fleet-hl-sub">Powering India's logistics</p>
                    <h2 className="fleet-hl-main">Manage. Track.<br />Deliver.</h2>
                </div>
            </div>

            {/* ── BLEND gradient ───────────────────────────────────── */}
            <div className="fleet-blend" aria-hidden="true" />

            {/* ── RIGHT: Login panel ───────────────────────────────── */}
            <div className="login-panel">
                <div
                    ref={cardRef}
                    className={`glass-card login-card${errorShake ? " error-shake" : ""}${loginSuccess ? " success-pulse" : ""}`}
                >
                    <div className="card-glow" />

                    {/* Header */}
                    <div className="login-header">
                        <div className="logo-icon">
                            <svg width="38" height="38" viewBox="0 0 38 38" fill="none">
                                <circle cx="19" cy="19" r="18" stroke="rgba(255,160,30,0.7)" strokeWidth="1.5" />
                                <path d="M8 22h6l2-8h6l2 6h6" stroke="#ff9a1a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                <circle cx="13" cy="26" r="2.5" fill="#ff9a1a" />
                                <circle cx="25" cy="26" r="2.5" fill="#ff9a1a" />
                            </svg>
                        </div>
                        <h1 className="login-title">FleetStat Login</h1>
                        <p className="login-subtitle">Fleet Management System</p>
                    </div>

                    <form onSubmit={handleLogin} className="login-form" autoComplete="off">

                        {/* Username */}
                        <div style={{ display: "flex", gap: "30px", flexWrap: "wrap" }}
                            className={`input-group${errorMsg ? " input-group--error" : ""}`}>
                            <label className={`floating-label${focusedField === "username" || username ? " active" : ""}`}>
                                Username
                            </label>
                            <span className="input-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                                    <circle cx="12" cy="7" r="4" />
                                </svg>
                            </span>
                            <input
                                id="login-username"
                                placeholder="Username"
                                value={username}
                                className={`input-styled${focusedField === "username" ? " input-focused" : ""}${errorMsg ? " input-error" : ""}`}
                                onChange={handleUsernameChange}
                                onFocus={() => setFocusedField("username")}
                                onBlur={() => setFocusedField(null)}
                            />
                            <div className="input-underline" />
                        </div>

                        {/* Password */}
                        <div style={{ display: "flex", gap: "30px", flexWrap: "wrap" }}
                            className={`input-group${errorMsg ? " input-group--error" : ""}`}>
                            <label className={`floating-label${focusedField === "password" || password ? " active" : ""}`}>
                                Password
                            </label>
                            <span className="input-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                                </svg>
                            </span>
                            <input
                                id="login-password"
                                type={showPassword ? "text" : "password"}
                                placeholder="Password"
                                value={password}
                                className={`input-styled${focusedField === "password" ? " input-focused" : ""}${errorMsg ? " input-error" : ""}`}
                                onChange={handlePasswordChange}
                                onFocus={() => setFocusedField("password")}
                                onBlur={() => setFocusedField(null)}
                            />
                            <button type="button" className="eye-toggle"
                                onClick={() => setShowPassword(v => !v)}
                                aria-label={showPassword ? "Hide password" : "Show password"}>
                                {showPassword ? (
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                                        <line x1="1" y1="1" x2="23" y2="23" />
                                    </svg>
                                ) : (
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                                        <circle cx="12" cy="12" r="3" />
                                    </svg>
                                )}
                            </button>
                            <div className="input-underline" />
                        </div>
                        {/*Password input group */}
                        <div className="forgot-password">
                            <a href="#"
                                onClick={(e) => {
                                    e.preventDefault();
                                    setErrorMsg("Password reset feature coming soon");
                                    setErrorShake(true);
                                    setTimeout(() => setErrorShake(false), 650);
                                }}>Forgot Password?</a>
                        </div>

                        {/* Inline error */}
                        {errorMsg && (
                            <div className="error-banner" role="alert">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                    <circle cx="12" cy="12" r="10" />
                                    <line x1="12" y1="8" x2="12" y2="12" />
                                    <line x1="12" y1="16" x2="12.01" y2="16" />
                                </svg>
                                {errorMsg}
                            </div>
                        )}

                        {/* Button */}
                        <button id="login-submit" type="submit"
                            className={`login-btn${isLoading ? " loading" : ""}${loginSuccess ? " success" : ""}`}
                            disabled={isLoading || loginSuccess }>
                            {loginSuccess ? (
                                <span className="btn-content">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                        <polyline points="20 6 9 17 4 12" />
                                    </svg>
                                    &nbsp;Authenticated
                                </span>
                            ) : isLoading ? (
                                <span className="btn-content">
                                    <span className="spinner" />
                                    &nbsp;Signing In...
                                </span>
                            ) : (
                                <span className="btn-content">
                                    Login
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="btn-arrow">
                                        <line x1="5" y1="12" x2="19" y2="12" />
                                        <polyline points="12 5 19 12 12 19" />
                                    </svg>
                                </span>
                            )}
                        </button>
                    </form>

                    {/* Ticker footer */}
                    <div className="login-footer">
                        <div className="ticker-track">
                            {[
                                "WELCOME to FleetStat",
                                "Driver Profiles",
                                "Trip Management",
                                "Fuel Analytics",
                                "Shipment Management",
                                "Truck Management",
                                "Role Based Access",
                                "Fuel , Damage Logs",
                                "50 + APIS Integrations",
                                "14+ Tables of Data " ,
                                "Multi table Relations",
                                "WELCOME to FleetStat",
                                "Driver Profiles",
                                "Trip Management",
                                "Fuel Analytics",
                                "Shipment Management",
                                "Truck Management",
                                "Role Based Access",
                                "Fuel , Damage Logs",
                                "50 + APIS Integrations",
                                "14+ Tables of Data " ,
                                "Multi table Relations",
                                 
                            ].map((text, i) => (
                                <span key={i} className="ticker-item">
                                    <span className="ticker-dot" />
                                    {text}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;
