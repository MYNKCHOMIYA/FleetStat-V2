import api from "../services/api";
import { useEffect, useState } from "react";

function Dashboard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    api.get("/analytics/dashboard")
      .then((res) => setUser(res.data))
      .catch((err) => {
  	console.log(err);});
  }, []);

  return (
    <div>	
    		<button
		  onClick={() => {
		    localStorage.removeItem("token");
		    window.location.reload();
		  }}
		>
		  Logout
		</button>
		<h1>FleetStat Admin Dashboard</h1>
		{user ? (
		     
		<div style={{ display: "flex", gap: "30px", flexWrap: "wrap", padding : "20px"  }}>
			
			<div style={{ border: "1px solid gray", padding: "20px", minWidth: "150px" }}>
				<h3>Trucks </h3>
				<p style={{ fontSize: "32px", fontWeight: "bold" }}>
					{user.total_trucks}
				</p>
			</div>
			
			<div style={{ border: "1px solid gray", padding: "20px", minWidth: "150px"}}>
				<h3>Driver </h3>
				<p style={{ fontSize: "32px", fontWeight: "bold" }}>
				{user.total_drivers}
				</p>
			</div>
			
			<div style={{ border: "1px solid gray", padding: "20px", minWidth: "150px"}}>
				<h3>Active Trips </h3>
				<p style={{ fontSize: "32px", fontWeight: "bold" }}>
				{user.active_trips}
				</p>
			</div>
			
			<div style={{ border: "1px solid gray", padding: "20px", minWidth: "150px" }}>
				<h3>Shipments </h3>
				<p style={{ fontSize: "32px", fontWeight: "bold" }}>
				{user.total_shipments}
				</p>
			</div>
			
			<div style={{ border: "1px solid gray", padding: "20px", minWidth: "150px" }}>
				<h3>Revenue </h3>
				<p style={{ fontSize: "32px", fontWeight: "bold" }}>
				{user.total_revenue.toLocaleString("en-IN")}
				</p>
			</div>
			
			<div style={{ border: "1px solid gray", padding: "20px", minWidth:  "150px" }}>
				<h3>Fuel Cost </h3>
				<p style={{ fontSize: "32px", fontWeight: "bold" }}>
				{user.fuel_cost.toLocaleString("en-IN")}
				</p>
		    </div>
		
	    </div>
    ) : (
      
    <p>Loading...</p>
    )}
      
    </div>
  );
}

export default Dashboard;
