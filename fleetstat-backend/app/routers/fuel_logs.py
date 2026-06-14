from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user, verify_driver_fuel_log

router = APIRouter(
    prefix="/fuel_logs",
    tags=["Fuel Logs"]
)

@router.post("")
def create_fuel_log(log: FuelLogCreate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO fuel_logs (
                    truck_id,
                    trip_id,
                    fuel_amount,
                    fuel_cost,
                    filled_at
                )
                VALUES (
                    :truck_id,
                    :trip_id,
                    :fuel_amount,
                    :fuel_cost,
                    NOW()
                )
                RETURNING fuel_log_id
            """),
            {
                "truck_id": log.truck_id,
                "trip_id": log.trip_id,
                "fuel_amount": log.fuel_amount,
                "fuel_cost": log.fuel_cost
            }
        )
        fuel_log_id = result.scalar()

    return {
        "message": "Fuel log created successfully",
        "fuel_log_id": fuel_log_id
    }




@router.get("")
def get_fuel_logs(current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM fuel_logs
        """))
        rows = result.fetchall()

        return [
            {
                "fuel_log_id": row.fuel_log_id,
                "truck_id": row.truck_id,
                "trip_id": row.trip_id,
                "fuel_amount": row.fuel_amount,
                "fuel_cost": row.fuel_cost,
                "filled_at": row.filled_at
            }
            for row in rows
        ]




@router.get("/{fuel_log_id}")
def get_fuel_log(fuel_log_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        if current_user["role"] != "admin":
            verify_driver_fuel_log(conn, fuel_log_id, int(current_user["sub"]))
        result = conn.execute(
            text("""
                SELECT * FROM fuel_logs
                WHERE fuel_log_id = :fuel_log_id
            """),
            {"fuel_log_id": fuel_log_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Fuel log not found"
            )

        return {
            "fuel_log_id": row.fuel_log_id,
            "truck_id": row.truck_id,
            "trip_id": row.trip_id,
            "fuel_amount": row.fuel_amount,
            "fuel_cost": row.fuel_cost,
            "filled_at": row.filled_at
        }




@router.put("/{fuel_log_id}")
def update_fuel_log(fuel_log_id: int, log: FuelLogUpdate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE fuel_logs
                SET 
                    truck_id = :truck_id,
                    trip_id = :trip_id,
                    fuel_amount = :fuel_amount,
                    fuel_cost = :fuel_cost
                WHERE fuel_log_id = :fuel_log_id
            """),
            {
                "truck_id": log.truck_id,
                "trip_id": log.trip_id,
                "fuel_amount": log.fuel_amount,
                "fuel_cost": log.fuel_cost,
                "fuel_log_id": fuel_log_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Fuel log not found"
            )

        return {"message": "Fuel log updated successfully"}




@router.delete("/{fuel_log_id}")
def delete_fuel_log(fuel_log_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                DELETE FROM fuel_logs
                WHERE fuel_log_id = :fuel_log_id
            """),
            {"fuel_log_id": fuel_log_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Fuel log not found"
            )

        return {"message": "Fuel log deleted successfully"}




