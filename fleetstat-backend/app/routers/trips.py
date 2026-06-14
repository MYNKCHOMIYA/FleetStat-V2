from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin,require_driver, get_current_user, verify_driver_trip 

router = APIRouter(
    prefix="/trips",
    tags=["Trips "]
)

@router.post("")
def create_trips(trip: TripCreate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO trips (
                    truck_id,
                    start_location,
                    end_location,
                    trip_distance,
                    fuel_used,
                    start_time,
                    end_time,
                    trip_status,
                    created_at,
                    updated_at
                )
                VALUES (
                    :truck_id,
                    :start_location,
                    :end_location,
                    :trip_distance,
                    :fuel_used,
                    :start_time,
                    :end_time,
                    :trip_status,
                    NOW(),
                    NOW()
                )
                RETURNING trip_id
            """),
            {
                 "truck_id":trip.truck_id,
                   "start_location" :trip.start_location,
                   "end_location" :trip.end_location,
                   "trip_distance" :trip.trip_distance,
                    "fuel_used":trip.fuel_used,
                  "start_time" :trip.start_time,
                  "end_time"  :trip.end_time,
                    "trip_status":trip.trip_status,
            }
        )
        trip_id = result.scalar()

    return {
        "message": "Trip created successfully",
        "trip_id": trip_id
    }
    
@router.post("/{trip_id}/start")
def start_trip(
    trip_id: int,
    current_user=Depends(require_driver)
):
    with engine.begin() as conn:
        verify_driver_trip(
            conn,
            trip_id,
            int(current_user["sub"])
        )
            
        result = conn.execute(
            text("""
                UPDATE trips
                SET trip_status = 'IN_PROGRESS',
                actual_start_time = NOW()
                WHERE trip_id = :trip_id
                AND trip_status = 'PLANNED'
            """),
            {"trip_id": trip_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=400,
                detail="Trip cannot be started"
            )

        return {
            "message": "Trip started successfully"
        }

@router.post("/{trip_id}/end")
def end_trip(
    trip_id: int,
    current_user=Depends(require_driver)
):
    with engine.begin() as conn:
        verify_driver_trip(
            conn,
            trip_id,
            int(current_user["sub"])
        )
        result = conn.execute(
            text("""
                UPDATE trips
                SET trip_status = 'COMPLETED',
                    actual_end_time = NOW()
                WHERE trip_id = :trip_id
                AND trip_status = 'IN_PROGRESS'
            """),
            {"trip_id": trip_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=400,
                detail="Trip cannot be completed"
            )

        return {
            "message": "Trip completed successfully"
        }

@router.get("")
def get_trips(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM trips
        """))
        rows = result.fetchall()

        return [
            {
                "trip_id": row.trip_id,
                "start_location": row.start_location,
                "end_location": row.end_location,
                "trip_distance": row.trip_distance,
                "fuel_used": row.fuel_used,
                "start_time": row.start_time,
                "end_time": row.end_time,
                "trip_status":row.trip_status
            }
            for row in rows
        ]
        
        



@router.get("/{trip_id}")
def get_trip(trip_id:int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        if current_user["role"] != "admin":
            verify_driver_trip(conn, trip_id, int(current_user["sub"]))
        result = conn.execute(text("""
            SELECT *
            FROM trips
            WHERE trip_id = :trip_id
        """),
        {"trip_id"  :trip_id})
        row = result.fetchone()
        if row is None :
                raise HTTPException(
                    status_code = 404,
                    detail = "Trip not found"
                    )

        return {
                 "trip_id": row.trip_id,
                 "start_location": row.start_location,
                 "end_location": row.end_location,
                 "trip_distance": row.trip_distance,
                 "fuel_used": row.fuel_used,
                 "start_time": row.start_time,
                 "end_time": row.end_time,
                 "trip_status": row.trip_status
                }
            
        
        


@router.put("/{trip_id}")
def update_trip(trip_id: int, trip: TripUpdate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE trips
                SET 
                   truck_id = :truck_id,
                    start_location = :start_location,
                    end_location = :end_location,
                    trip_distance = :trip_distance,
                    fuel_used = :fuel_used,
                    start_time = :start_time,
                    end_time = :end_time,
                    trip_status = :trip_status,
                    updated_at = NOW()
                WHERE trip_id = :trip_id
            """),
            {
                    "truck_id" :trip.truck_id,
                    "start_location"  :trip.start_location,
                    "end_location"  :trip.end_location,
                    "trip_distance"  :trip.trip_distance,
                    "fuel_used" :trip.fuel_used,
                    "start_time"  :trip.start_time,
                    "end_time" :trip.end_time,
                    "trip_status"  :trip.trip_status,
                    "trip_id": trip_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )

        return {"message": "Trip updated successfully"}
        
        


@router.delete("/{trip_id}")
def delete_trip(trip_id: int,current_user=Depends(require_admin)):
    with engine.begin()  as conn:
        result = conn.execute(
            text("""
                UPDATE trips
                SET
                    trip_status = 'CANCELLED',
                    updated_at = NOW()
                WHERE trip_id = :trip_id
            """),
            {"trip_id": trip_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )

        return {"message": "Trip deleted successfully"}
        

@router.get("/{trip_id}/duration")
def trip_duration(trip_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        if current_user["role"] != "admin":
            verify_driver_trip(conn, trip_id, int(current_user["sub"]))
        result = conn.execute(
            text("""
                SELECT 
                    trip_id,
                    actual_start_time,
                    actual_end_time
                FROM trips
                WHERE trip_id = :trip_id
            """),
            {"trip_id": trip_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )
        if (
            row.actual_start_time is None or
            row.actual_end_time is None
        ):
            raise HTTPException(
                status_code=400,
                detail="Trip has not been completed yet"
            )
            
        duration = row.actual_end_time - row.actual_start_time

        return {
            "trip_id": row.trip_id,
            "actual_start_time": row.actual_start_time,
            "actual_end_time": row.actual_end_time,
            "duration": str(duration)
        }
        
@router.post("/{trip_id}/fuel-log")
def add_fuel_log(
    trip_id:int,
    fuel_log : TripFuelLogCreate,
    current_user=Depends(require_driver)
    
):
    with engine.begin() as conn:
        verify_driver_trip(
            conn,
            trip_id,
            int(current_user["sub"])
        )
        result = conn.execute(
            text("""
                SELECT 
                    trip_status,
                    truck_id
                FROM trips
                WHERE trip_id = :trip_id
                """),
            {"trip_id": trip_id}
        )
        row = result.fetchone()
        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )
        if row.trip_status != 'IN_PROGRESS':
            raise HTTPException(
                status_code=400,
                detail="Fuel logs can only be added for trips that are in progress"
            )
        result = conn.execute(
            text("""
                INSERT INTO fuel_logs (
                    trip_id,
                    truck_id,
                    fuel_amount,
                    fuel_cost,
                    filled_at
                )
                VALUES (
                    :trip_id,
                    :truck_id,
                    :fuel_amount,
                    :fuel_cost,
                    NOW()
                )
                RETURNING fuel_log_id
            """),
            {
                "trip_id": trip_id,
                "truck_id": row.truck_id,
                "fuel_amount": fuel_log.fuel_amount,
                "fuel_cost": fuel_log.fuel_cost
            }
        )
        return {
            "message": "Fuel log added successfully",
            "fuel_log_id": result.scalar()
        }