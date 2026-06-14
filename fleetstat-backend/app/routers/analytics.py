from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/driver_performance")
def get_driver_performance(current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                d.full_name,
                COUNT(tr.trip_id) AS total_trips,
                SUM(tr.trip_distance) AS total_distance,
                SUM(tr.fuel_used) AS total_fuel,
                AVG(tr.trip_distance / NULLIF(tr.fuel_used, 0)) AS avg_mileage
            FROM trip_assignments ts
            JOIN drivers d ON ts.driver_id = d.driver_id
            JOIN trips tr ON ts.trip_id = tr.trip_id
            GROUP BY d.full_name
            ORDER BY avg_mileage DESC;
        """))
        rows = result.fetchall()

        return [
            {
                "driver_name": row.full_name,
                "total_distance": row.total_distance,
                "total_trips": row.total_trips,
                "mileage": row.avg_mileage,
            }
            for row in rows
        ]


@router.get("/revenue")
def get_revenue(current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM revenue_summary
        """))
        rows = result.fetchall()

        return [
            {
                "month": row.month.strftime("%B %Y"),
                "revenue": row.revenue
            }
            for row in rows
        ]


@router.get("/trip_profit/{trip_id}")
def get_trip_profit(trip_id: int,current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 
                    d.full_name,
                    tr.trip_distance,
                    tr.trip_id,
                    t.license_plate,
                    SUM(p.amount) AS revenue,
                    f.fuel_cost,
                    (SUM(p.amount) - f.fuel_cost) AS profit
                FROM trip_assignments ts
                JOIN drivers d ON ts.driver_id = d.driver_id
                JOIN trips tr ON ts.trip_id = tr.trip_id
                JOIN trucks t ON t.truck_id = tr.truck_id
                JOIN fuel_logs f ON tr.trip_id = f.trip_id
                JOIN shipments sh ON tr.trip_id = sh.trip_id
                JOIN payments p ON sh.shipment_id = p.shipment_id
                WHERE tr.trip_id = :trip_id
                GROUP BY 
                    d.full_name,
                    tr.trip_id,
                    tr.trip_distance,
                    t.license_plate,
                    f.fuel_cost
            """),
            {"trip_id": trip_id}
        )
        rows = result.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )

        return [
            {
                "driver_name": row.full_name,
                "trip_id": row.trip_id,
                "distance": row.trip_distance,
                "license_plate": row.license_plate,
                "amount": row.revenue,
                "fuel_cost": row.fuel_cost,
                "profit": row.profit
            }
            for row in rows
        ]
