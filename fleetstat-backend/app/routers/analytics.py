from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, require_driver


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
        
@router.get("/dashboard")
def get_dashboard(
    current_user = Depends(require_admin)
):
    with engine.connect() as conn:
        total_trucks = conn.execute(text("""SELECT COUNT(*) FROM trucks WHERE is_active = TRUE""")).scalar()
        active_trucks = conn.execute(text("""SELECT COUNT(*) FROM trucks WHERE UPPER(status) = 'ACTIVE' AND is_active = TRUE""")).scalar()
        total_drivers = conn.execute(text("""SELECT COUNT(*) FROM drivers WHERE is_active = TRUE""")).scalar()
        active_trips = conn.execute(text("""SELECT COUNT(*) FROM trips WHERE UPPER(trip_status) = 'IN_PROGRESS'""")).scalar()
        completed_trips = conn.execute(text("""SELECT COUNT(*) FROM trips WHERE UPPER(trip_status) = 'COMPLETED'""")).scalar()
        total_shipments = conn.execute(text("""SELECT COUNT(*) FROM shipments""")).scalar()
        pending_shipments = conn.execute(text("""SELECT COUNT(*) FROM shipments WHERE UPPER(shipment_status) = 'PENDING'""")).scalar()
        total_revenue = conn.execute(text("""SELECT COALESCE(SUM(amount), 0) FROM payments WHERE UPPER(payment_status) = 'SUCCESS'""")).scalar()
        fuel_cost = conn.execute(text("""SELECT COALESCE(SUM(fuel_cost), 0) FROM fuel_logs""")).scalar()
        
        return {
            "total_trucks": total_trucks,
            "active_trucks": active_trucks,
            "total_drivers": total_drivers,
            "active_trips": active_trips,
            "completed_trips": completed_trips,
            "total_shipments": total_shipments,
            "pending_shipments": pending_shipments,
            "total_revenue": float(total_revenue),
            "fuel_cost": float(fuel_cost)
        }
        
@router.get("/dashboard/charts")
def get_dashboard_charts(current_user = Depends(require_admin)):
    with engine.connect() as conn:
        monthly_revenue = conn.execute(text("""
                                            SELECT 
                                                DATE_TRUNC('month', payment_date) AS month,
                                                SUM(amount) AS revenue
                                            FROM payments
                                            WHERE payment_status = 'SUCCESS'
                                            GROUP BY month
                                            ORDER BY month
                                        """)).fetchall()
        Shipment_status = conn.execute(text("""
                                            SELECT 
                                                shipment_status,
                                                COUNT(*) AS count
                                            FROM shipments
                                            GROUP BY shipment_status
                                        """)).fetchall()
        trip_status = conn.execute(text("""
                                            SELECT 
                                                trip_status,
                                                COUNT(*) AS count
                                            FROM trips
                                            GROUP BY trip_status
                                        """)).fetchall()
        monthly_fuel_cost = conn.execute(text("""SELECT 
                                                 DATE_TRUNC('month', filled_at) AS month,
                                                    SUM(fuel_cost) AS total_fuel_cost
                                            FROM fuel_logs
                                            GROUP BY month
                                            ORDER BY month
                                        """)).fetchall()
        return {
            "monthly_revenue": [
                {"month": row.month.strftime("%B %Y"), "revenue": float(row.revenue)}
                for row in monthly_revenue
            ],
            "shipment_status_distribution": [
                {"status": row.shipment_status, "count": row.count}
                for row in Shipment_status
            ],
            "trip_status_distribution": [
                {"status": row.trip_status, "count": row.count}
                for row in trip_status
            ],
            "monthly_fuel_cost": [
                {"month": row.month.strftime("%B %Y"), "fuel_cost": float(row.total_fuel_cost)}
                for row in monthly_fuel_cost
            ]
        }

@router.get("/my-trips")
def get_my_trips(current_user = Depends(require_driver)):
    with engine.connect() as conn:
        user_id = int(current_user["sub"])
        
        total_trips = conn.execute(
            text("""
                SELECT COUNT(tr.trip_id)
                FROM drivers d
                JOIN trip_assignments ta ON d.driver_id = ta.driver_id
                JOIN trips tr ON ta.trip_id = tr.trip_id
                WHERE d.user_id = :user_id
            """),
            {"user_id": user_id}
        ).scalar()
        
        completed_trips = conn.execute(
            text("""
                SELECT COUNT(tr.trip_id)
                FROM drivers d
                JOIN trip_assignments ta ON d.driver_id = ta.driver_id
                JOIN trips tr ON ta.trip_id = tr.trip_id
                WHERE d.user_id = :user_id AND UPPER(tr.trip_status) = 'COMPLETED'
            """),
            {"user_id": user_id}
        ).scalar()
        
        active_trips = conn.execute(
            text("""
                SELECT COUNT(tr.trip_id)
                FROM drivers d
                JOIN trip_assignments ta ON d.driver_id = ta.driver_id
                JOIN trips tr ON ta.trip_id = tr.trip_id
                WHERE d.user_id = :user_id AND UPPER(tr.trip_status) = 'IN_PROGRESS'
            """),
            {"user_id": user_id}
        ).scalar()
        
        fuel_logs = conn.execute(
            text("""
                SELECT COUNT(fl.fuel_log_id)
                FROM drivers d
                JOIN trip_assignments ta ON d.driver_id = ta.driver_id
                JOIN fuel_logs fl ON ta.trip_id = fl.trip_id
                WHERE d.user_id = :user_id
            """),
            {"user_id": user_id}
        ).scalar()
        
        damage_reports = conn.execute(
            text("""
                SELECT COUNT(dr.damage_id)
                FROM drivers d
                JOIN trip_assignments ta ON d.driver_id = ta.driver_id
                JOIN shipments s ON ta.trip_id = s.trip_id
                JOIN damage_reports dr ON s.shipment_id = dr.shipment_id
                WHERE d.user_id = :user_id
            """),
            {"user_id": user_id}
        ).scalar()
        
        return {
            "total_trips": total_trips,
            "completed_trips": completed_trips,
            "active_trips": active_trips,
            "fuel_logs": fuel_logs,
            "damage_reports": damage_reports
        }


@router.get("/damage-summary")
def get_damage_summary(current_user = Depends(require_admin)):
    with engine.connect() as conn:
        pending = conn.execute(text("""SELECT COUNT(*) FROM damage_reports WHERE UPPER(status) = 'PENDING'""")).scalar()
        under_review = conn.execute(text("""SELECT COUNT(*) FROM damage_reports WHERE UPPER(status) = 'UNDER_REVIEW'""")).scalar()
        resolved = conn.execute(text("""SELECT COUNT(*) FROM damage_reports WHERE UPPER(status) = 'RESOLVED'""")).scalar()
        avg_damage = conn.execute(text("""SELECT COALESCE(AVG(damage_percentage), 0) FROM damage_reports""")).scalar()
        
        return {
            "pending": pending,
            "under_review": under_review,
            "resolved": resolved,
            "average_damage_percentage": float(avg_damage)
        }