from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/paymnets",
    tags=["Payments"]
)
@router.post("")
def create_payment(payment: PaymentCreate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO payments (
                    shipment_id,
                    amount,
                    payment_method,
                    payment_status,
                    payment_date,
                    remarks
                )
                VALUES (
                    :shipment_id,
                    :amount,
                    :payment_method,
                    :payment_status,
                    NOW(),
                    :remarks
                )
                RETURNING payment_id
            """),
            {
                "shipment_id": payment.shipment_id,
                "amount": payment.amount,
                "payment_method": payment.payment_method,
                "payment_status": payment.payment_status,
                "remarks": payment.remarks
            }
        )
        payment_id = result.scalar()

    return {
        "message": "Payment created successfully",
        "payment_id": payment_id
    }




@router.get("")
def get_payments(current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM payments
        """))
        rows = result.fetchall()

        return [
            {
                "payment_id": row.payment_id,
                "shipment_id": row.shipment_id,
                "amount": row.amount,
                "payment_method": row.payment_method,
                "payment_status": row.payment_status,
                "payment_date": row.payment_date,
                "remarks": row.remarks
            }
            for row in rows
        ]




@router.get("/{payment_id}")
def get_payment(payment_id: int, current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM payments
                WHERE payment_id = :payment_id
            """),
            {"payment_id": payment_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return {
            "payment_id": row.payment_id,
            "shipment_id": row.shipment_id,
            "amount": row.amount,
            "payment_method": row.payment_method,
            "payment_status": row.payment_status,
            "payment_date": row.payment_date,
            "remarks": row.remarks
        }




@router.put("/{payment_id}")
def update_payment(payment_id: int, payment: PaymentUpdate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE payments
                SET 
                    shipment_id = :shipment_id,
                    amount = :amount,
                    payment_method = :payment_method,
                    payment_status = :payment_status,
                    remarks = :remarks
                WHERE payment_id = :payment_id
            """),
            {
                "shipment_id": payment.shipment_id,
                "amount": payment.amount,
                "payment_method": payment.payment_method,
                "payment_status": payment.payment_status,
                "remarks": payment.remarks,
                "payment_id": payment_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return {"message": "Payment updated successfully"}




@router.delete("/{payment_id}")
def delete_payment(payment_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE payments
                SET 
                    payment_status = 'REFUNDED'
                WHERE payment_id = :payment_id
            """),
            {"payment_id": payment_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return {"message": "Payment status updated to REFUNDED successfully"}




