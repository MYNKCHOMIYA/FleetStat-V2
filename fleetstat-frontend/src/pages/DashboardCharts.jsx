import { useEffect, useState } from "react";
import api from "../services/api";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function DashboardCharts() {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    api.get("/analytics/dashboard/charts")
      .then((res) => setChartData(res.data))
      .catch((err) => console.log(err));
  }, []);

  if (!chartData) {
    return <p>Loading charts...</p>;
  }

  return (
    <div
      style={{
        marginTop: "40px",
        background: "#111827",
        padding: "20px",
        borderRadius: "15px"
      }}
    >
      <h2>Revenue Trend</h2>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={chartData.monthly_revenue}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="month" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#f59e0b"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DashboardCharts;