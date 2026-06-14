from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/shipment_items",
    tags=["Shipment Items"]
)

@router.post("")
def create_shipment_item(item: ShipmentItemCreate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO shipment_items (
                    shipment_id,
                    item_name,
                    quantity,
                    weight_kg,
                    declared_value,
                    temperature_required
                )
                VALUES (
                    :shipment_id,
                    :item_name,
                    :quantity,
                    :weight_kg,
                    :declared_value,
                    :temperature_required
                )
                RETURNING item_id
            """),
            {
                "shipment_id": item.shipment_id,
                "item_name": item.item_name,
                "quantity": item.quantity,
                "weight_kg": item.weight_kg,
                "declared_value": item.declared_value,
                "temperature_required": item.temperature_required
            }
        )
        item_id = result.scalar()

    return {
        "message": "Shipment item created successfully",
        "item_id": item_id
    }




@router.get("")
def get_shipment_items(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM shipment_items
        """))
        rows = result.fetchall()

        return [
            {
                "item_id": row.item_id,
                "shipment_id": row.shipment_id,
                "item_name": row.item_name,
                "quantity": row.quantity,
                "weight_kg": row.weight_kg,
                "declared_value": row.declared_value,
                "temperature_required": row.temperature_required
            }
            for row in rows
        ]




@router.get("/{item_id}")
def get_shipment_item(item_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM shipment_items
                WHERE item_id = :item_id
            """),
            {"item_id": item_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment item not found"
            )

        return {
            "item_id": row.item_id,
            "shipment_id": row.shipment_id,
            "item_name": row.item_name,
            "quantity": row.quantity,
            "weight_kg": row.weight_kg,
            "declared_value": row.declared_value,
            "temperature_required": row.temperature_required
        }




@router.put("/{item_id}")
def update_shipment_item(item_id: int, item: ShipmentItemUpdate, current_user=Depends(get_current_user)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE shipment_items
                SET 
                    shipment_id = :shipment_id,
                    item_name = :item_name,
                    quantity = :quantity,
                    weight_kg = :weight_kg,
                    declared_value = :declared_value,
                    temperature_required = :temperature_required
                WHERE item_id = :item_id
            """),
            {
                "shipment_id": item.shipment_id,
                "item_name": item.item_name,
                "quantity": item.quantity,
                "weight_kg": item.weight_kg,
                "declared_value": item.declared_value,
                "temperature_required": item.temperature_required,
                "item_id": item_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Shipment item not found"
            )

        return {"message": "Shipment item updated successfully"}




@router.delete("/{item_id}")
def delete_shipment_item(item_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                DELETE FROM shipment_items
                WHERE item_id = :item_id
            """),
            {"item_id": item_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Shipment item not found"
            )

        return {"message": "Shipment item deleted successfully"}




