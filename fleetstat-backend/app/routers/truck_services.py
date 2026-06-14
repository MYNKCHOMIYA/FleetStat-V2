from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/truck_services",
    tags=["Trucks Services"]
)

@router.post("")
def create_truck_service(service: TruckServiceCreate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO truck_services (
                    truck_id,
                    service_center,
                    service_date,
                    service_cost,
                    next_due_date,
                    description,
                    created_at
                )
                VALUES (
                    :truck_id,
                    :service_center,
                    :service_date,
                    :service_cost,
                    :next_due_date,
                    :description,
                    NOW()
                )
                RETURNING service_id
            """),
            {
                "truck_id": service.truck_id,
                "service_center": service.service_center,
                "service_date": service.service_date,
                "service_cost": service.service_cost,
                "next_due_date": service.next_due_date,
                "description": service.description
            }
        )
        service_id = result.scalar()

    return {
        "message": "Truck service record created successfully",
        "service_id": service_id
    }




@router.get("")
def get_truck_services(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM truck_services
        """))
        rows = result.fetchall()

        return [
            {
                "service_id": row.service_id,
                "truck_id": row.truck_id,
                "service_center": row.service_center,
                "service_date": row.service_date,
                "service_cost": row.service_cost,
                "next_due_date": row.next_due_date,
                "description": row.description,
                "created_at": row.created_at
            }
            for row in rows
        ]




@router.get("/{service_id}")
def get_truck_service(service_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM truck_services
                WHERE service_id = :service_id
            """),
            {"service_id": service_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Truck service record not found"
            )

        return {
            "service_id": row.service_id,
            "truck_id": row.truck_id,
            "service_center": row.service_center,
            "service_date": row.service_date,
            "service_cost": row.service_cost,
            "next_due_date": row.next_due_date,
            "description": row.description,
            "created_at": row.created_at
        }




@router.put("/{service_id}")
def update_truck_service(service_id: int, service: TruckServiceUpdate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE truck_services
                SET 
                    truck_id = :truck_id,
                    service_center = :service_center,
                    service_date = :service_date,
                    service_cost = :service_cost,
                    next_due_date = :next_due_date,
                    description = :description
                WHERE service_id = :service_id
            """),
            {
                "truck_id": service.truck_id,
                "service_center": service.service_center,
                "service_date": service.service_date,
                "service_cost": service.service_cost,
                "next_due_date": service.next_due_date,
                "description": service.description,
                "service_id": service_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Truck service record not found"
            )

        return {"message": "Truck service record updated successfully"}




@router.delete("/{service_id}")
def delete_truck_service(service_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                DELETE FROM truck_services
                WHERE service_id = :service_id
            """),
            {"service_id": service_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Truck service record not found"
            )

        return {"message": "Truck service record deleted successfully"}




