from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user, verify_driver_shipment

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)

@router.post("")
def create_shipments(shipment: ShipmentCreate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO shipments (
                    trip_id,
                    container_id,
                    sender_customer_id,
                    receiver_customer_id,
                    shipment_status,
                    received_date,
                    shipped_date,
                    delivered_date,
                    notes,
                    created_at,
                    updated_at
                )
                VALUES (
                    :trip_id,
                    :container_id,
                    :sender_customer_id,
                    :receiver_customer_id,
                    :shipment_status,
                    :received_date,
                    :shipped_date,
                    :delivered_date,
                    :notes,
                    NOW(),
                    NOW()
                )
                RETURNING shipment_id
            """),
            {
                   "trip_id" :shipment.trip_id,
                    "container_id" :shipment.container_id,
                    "sender_customer_id" :shipment.sender_customer_id,
                    "receiver_customer_id":shipment.receiver_customer_id,
                    "shipment_status":shipment.shipment_status,
                    "received_date":shipment.received_date,
                    "shipped_date":shipment.shipped_date,
                   "delivered_date":shipment.delivered_date,
                    "notes":shipment.notes
            }
        )
        shipment_id = result.scalar()

    return {
        "message": "shipment created successfully",
        "shipment_id": shipment_id
    }
    


@router.get("")
def get_shipments(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM shipments
        """))
        rows = result.fetchall()

        return [
            {     "shipment_id":row.shipment_id,
                  "trip_id" :row.trip_id,
                    "container_id" :row.container_id,
                    "sender_customer_id" :row.sender_customer_id,
                    "receiver_customer_id":row.receiver_customer_id,
                    "shipment_status":row.shipment_status,
                    "received_date":row.received_date,
                    "shipped_date":row.shipped_date,
                   "delivered_date":row.delivered_date,
                    "notes":row.notes
            }
            for row in rows
        ]
        


@router.get("/{shipment_id}")
def get_shipment(shipment_id:int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        if current_user["role"] != "admin":
            verify_driver_shipment(conn, shipment_id, int(current_user["sub"]))
        result = conn.execute(text("""
            SELECT *
            FROM shipments
            WHERE shipment_id = :shipment_id
        """),
        {"shipment_id"  :shipment_id})
        row = result.fetchone()
        if row is None :
                raise HTTPException(
                    status_code = 404,
                    detail = "Shipment not found"
                    )

        return {
            "shipment_id": row.shipment_id,
            "trip_id": row.trip_id,
            "container_id": row.container_id,
            "sender_customer_id": row.sender_customer_id,
            "receiver_customer_id": row.receiver_customer_id,
            "shipment_status": row.shipment_status,
            "received_date": row.received_date,
            "shipped_date": row.shipped_date,
            "delivered_date": row.delivered_date,
            "notes": row.notes
        }



@router.put("/{shipment_id}")
def update_shipments(shipment_id: int, shipment: ShipmentUpdate, current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE shipments
                SET 
                   trip_id = :trip_id,
                    container_id = :container_id,
                    sender_customer_id = :sender_customer_id,
                    receiver_customer_id = :receiver_customer_id,
                    shipment_status = :shipment_status,
                    received_date = :received_date,
                    shipped_date = :shipped_date,
                   delivered_date = :delivered_date,
                   notes=:notes,
                  updated_at = NOW()
                WHERE shipment_id = :shipment_id
            """),
            {
                    
                    "trip_id" :shipment.trip_id,
                    "container_id" :shipment.container_id,
                    "sender_customer_id" :shipment.sender_customer_id,
                    "receiver_customer_id":shipment.receiver_customer_id,
                    "shipment_status":shipment.shipment_status,
                    "received_date":shipment.received_date,
                    "shipped_date":shipment.shipped_date,
                   "delivered_date":shipment.delivered_date,
                    "notes":shipment.notes,
                    "shipment_id":shipment_id,
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found"
            )

        return {"message": "Shipment updated successfully"}
        


@router.delete("/{shipment_id}")
def delete_shipments(shipment_id: int,current_user=Depends(require_admin)):
    with engine.begin()  as conn:
        result = conn.execute(
            text("""
                UPDATE shipments
                SET
                    shipment_status = 'CANCELLED',
                    updated_at = NOW()
                WHERE shipment_id = :shipment_id
            """),
            {"shipment_id": shipment_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found"
            )

        return {"message": "Shipment deleted successfully"}
        

@router.get("/track/{shipment_id}")
def track_shipment(
    shipment_id: int,
    current_user=Depends(get_current_user)
):
    with engine.connect() as conn:
        if current_user["role"] != "admin":
            verify_driver_shipment(conn, shipment_id, int(current_user["sub"]))

        result = conn.execute(
            text("""
                SELECT
                    s.shipment_id,
                    s.shipment_status,
                    s.shipped_date,
                    s.delivered_date,

                    sender.customer_name AS sender_name,
                    receiver.customer_name AS receiver_name,

                    tr.trip_id,
                    tr.start_location,
                    tr.end_location,

                    d.full_name,
                    t.license_plate

                FROM shipments s

                JOIN customers sender
                    ON s.sender_customer_id = sender.customer_id

                JOIN customers receiver
                    ON s.receiver_customer_id = receiver.customer_id

                JOIN trips tr
                    ON s.trip_id = tr.trip_id

                JOIN trucks t
                    ON tr.truck_id = t.truck_id

                JOIN trip_assignments ta
                    ON tr.trip_id = ta.trip_id

                JOIN drivers d
                    ON ta.driver_id = d.driver_id

                WHERE s.shipment_id = :shipment_id
            """),
            {
                "shipment_id": shipment_id
            }
        )

        shipment = result.fetchone()

        if shipment is None:
            raise HTTPException(
                status_code=404,
                detail="Shipment not found"
            )

        return {
            "shipment_id": shipment.shipment_id,
            "shipment_status": shipment.shipment_status,

            "sender": shipment.sender_name,
            "receiver": shipment.receiver_name,

            "trip_id": shipment.trip_id,

            "driver_name": shipment.full_name,
            "truck_plate": shipment.license_plate,

            "start_location": shipment.start_location,
            "end_location": shipment.end_location,

            "shipped_date": shipment.shipped_date,
            "delivered_date": shipment.delivered_date
        }