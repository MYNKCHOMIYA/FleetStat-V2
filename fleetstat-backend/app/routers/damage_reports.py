from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user, verify_driver_shipment

router = APIRouter(
    prefix="/damage_reports",
    tags=["Damage Reports"]
)

@router.post("")
def create_damage_report(report: DamageReportCreate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        if current_user["role"] != "admin":
            verify_driver_shipment(
                conn,
                report.shipment_id,
                int(current_user["sub"])
            )
        result = conn.execute(
            text("""
                INSERT INTO damage_reports (
                    shipment_id,
                    damage_percentage,
                    description,
                    status,
                    reported_at
                )
                VALUES (
                    :shipment_id,
                    :damage_percentage,
                    :description,
                    'PENDING',
                    NOW()
                )
                RETURNING damage_id
            """),
            {
                "shipment_id": report.shipment_id,
                "damage_percentage": report.damage_percentage,
                "description": report.description
            }
        )
        damage_id = result.scalar()

    return {
        "message": "Damage report created successfully",
        "damage_id": damage_id,
        "status": "PENDING"
    }




@router.get("")
def get_damage_reports(current_user=Depends(get_current_user)):
    
    with engine.connect() as conn:
        if current_user["role"] == "admin":
            result = conn.execute(text("""
                SELECT * FROM damage_reports
            """))
        else:
            result = conn.execute(
                text("""
                    SELECT dr.* 
                    FROM damage_reports dr
                    JOIN shipments s ON dr.shipment_id = s.shipment_id
                    JOIN trip_assignments ta ON s.trip_id = ta.trip_id
                    JOIN drivers d ON ta.driver_id = d.driver_id
                    WHERE d.user_id = :user_id
                """),
                {"user_id": int(current_user["sub"])}
            )
        rows = result.fetchall()

        return [
            {
                "damage_id": row.damage_id,
                "shipment_id": row.shipment_id,
                "damage_percentage": row.damage_percentage,
                "description": row.description,
                "status":row.status,
                "reported_at": row.reported_at
            }
            for row in rows
        ]




@router.get("/{damage_id}")
def get_damage_report(damage_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM damage_reports
                WHERE damage_id = :damage_id
            """),
            {"damage_id": damage_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Damage report not found"
            )

        if current_user["role"] != "admin":
            verify_driver_shipment(conn, row.shipment_id, int(current_user["sub"]))

        return {
            "damage_id": row.damage_id,
            "shipment_id": row.shipment_id,
            "damage_percentage": row.damage_percentage,
            "description": row.description,
            "status":row.status,
            "reported_at": row.reported_at
        }




@router.put("/{damage_id}")
def update_damage_report(damage_id: int, report: DamageReportUpdate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        if current_user["role"] != "admin":
            verify_driver_shipment(
                conn,
                report.shipment_id,
                int(current_user["sub"])
            )
        result = conn.execute(
            text("""
                UPDATE damage_reports
                SET 
                    shipment_id = :shipment_id,
                    damage_percentage = :damage_percentage,
                    description = :description
                WHERE damage_id = :damage_id
            """),
            {
                "shipment_id": report.shipment_id,
                "damage_percentage": report.damage_percentage,
                "description": report.description,
                "damage_id": damage_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Damage report not found"
            )

        return {"message": "Damage report updated successfully"}




@router.delete("/{damage_id}")
def delete_damage_report(damage_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                DELETE FROM damage_reports
                WHERE damage_id = :damage_id
            """),
            {"damage_id": damage_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Damage report not found"
            )

        return {"message": "Damage report deleted successfully"}
        
        
    
@router.patch("/{damage_id}/status")
def update_damage_status(
    damage_id: int,
    data: DamageStatusUpdate,
    current_user=Depends(require_admin)
):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE damage_reports
                SET status = :status
                WHERE damage_id = :damage_id
            """),
            {
                "status": data.status,
                "damage_id": damage_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Damage report not found"
            )

        return {
            "message": "Damage status updated successfully"
        }




