from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/trucks",
    tags=["Trucks"]
)

@router.post("")
def create_truck(truck: TruckCreate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO trucks (
                    license_plate,
                    manufacturer,
                    model,
                    purchase_date,
                    purchase_cost,
                    capacity_tons,
                    total_distance_travelled,
                    truck_condition,
                    status,
                    last_service_date,
                    description,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (
                    :license_plate,
                    :manufacturer,
                    :model,
                    :purchase_date,
                    :purchase_cost,
                    :capacity_tons,
                    :total_distance_travelled,
                    'GOOD',
                    'ACTIVE',
                    :last_service_date,
                    :description,
                    TRUE,
                    NOW(),
                    NOW()
                )
                RETURNING truck_id
            """),
            {
                "license_plate": truck.license_plate,
                "manufacturer": truck.manufacturer,
                "model": truck.model,
                "purchase_date": truck.purchase_date,
                "purchase_cost": truck.purchase_cost,
                "capacity_tons": truck.capacity_tons,
                "total_distance_travelled": truck.total_distance_travelled,
                "last_service_date": truck.last_service_date,
                "description": truck.description
            }
        )
        truck_id = result.scalar()

    return {
        "message": "Truck created successfully",
        "truck_id": truck_id
    }




@router.get("")
def get_trucks(current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM trucks
            WHERE is_active = TRUE
        """))
        rows = result.fetchall()

        return [
            {
                "truck_id": row.truck_id,
                "license_plate": row.license_plate,
                "status": row.status,
                "is_active": row.is_active,
                "capacity_tons": row.capacity_tons,
                "total_distance_travelled": row.total_distance_travelled,
                "truck_condition": row.truck_condition
            }
            for row in rows
        ]




@router.get("/{truck_id}")
def get_truck(truck_id: int,current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM trucks
                WHERE truck_id = :truck_id 
                AND is_active = TRUE
            """),
            {"truck_id": truck_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Truck not found"
            )

        return {
            "truck_id": row.truck_id,
            "license_plate": row.license_plate,
            "manufacturer": row.manufacturer,
            "model": row.model,
            "capacity_tons": row.capacity_tons,
            "status": row.status,
            "is_active": row.is_active
        }




@router.put("/{truck_id}")
def update_truck(truck_id: int, truck: TruckUpdate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE trucks
                SET 
                    license_plate = :license_plate,
                    manufacturer = :manufacturer,
                    model = :model,
                    purchase_date = :purchase_date,
                    purchase_cost = :purchase_cost,
                    capacity_tons = :capacity_tons,
                    total_distance_travelled = :total_distance_travelled,
                    last_service_date = :last_service_date,
                    description = :description,
                    updated_at = NOW()
                WHERE truck_id = :truck_id 
                AND is_active = TRUE
            """),
            {
                "license_plate": truck.license_plate,
                "manufacturer": truck.manufacturer,
                "model": truck.model,
                "purchase_date": truck.purchase_date,
                "purchase_cost": truck.purchase_cost,
                "capacity_tons": truck.capacity_tons,
                "total_distance_travelled": truck.total_distance_travelled,
                "last_service_date": truck.last_service_date,
                "description": truck.description,
                "truck_id": truck_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Truck not found"
            )

        return {"message": "Truck updated successfully"}




@router.delete("/{truck_id}")
def delete_truck(truck_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE trucks
                SET
                    is_active = FALSE,
                    status = 'OUT_OF_SERVICE',
                    updated_at = NOW()
                WHERE truck_id = :truck_id
            """),
            {"truck_id": truck_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Truck not found"
            )

        return {"message": "Truck deleted successfully"}



        


