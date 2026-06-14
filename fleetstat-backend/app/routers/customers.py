from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("")
def create_customer(customer: CustomerCreate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO customers (
                    customer_type,
                    customer_name,
                    gst_number,
                    email,
                    phone_number,
                    address,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (
                    :customer_type,
                    :customer_name,
                    :gst_number,
                    :email,
                    :phone_number,
                    :address,
                    TRUE,
                    NOW(),
                    NOW()
                )
                RETURNING customer_id
            """),
            {
                "customer_type": customer.customer_type,
                "customer_name": customer.customer_name,
                "gst_number": customer.gst_number,
                "email": customer.email,
                "phone_number": customer.phone_number,
                "address": customer.address
            }
        )
        customer_id = result.scalar()

    return {
        "message": "Customer created successfully",
        "customer_id": customer_id
    }




@router.get("")
def get_customers(current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM customers
            WHERE is_active = TRUE
        """))
        rows = result.fetchall()

        return [
            {
                "customer_id": row.customer_id,
                "customer_type": row.customer_type,
                "customer_name": row.customer_name,
                "gst_number": row.gst_number,
                "email": row.email,
                "phone_number": row.phone_number,
                "address": row.address
            }
            for row in rows
        ]




@router.get("/{customer_id}")
def get_customer(customer_id: int, current_user=Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM customers
                WHERE customer_id = :customer_id 
                AND is_active = TRUE
            """),
            {"customer_id": customer_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return {
            "customer_id": row.customer_id,
            "customer_type": row.customer_type,
            "customer_name": row.customer_name,
            "gst_number": row.gst_number,
            "email": row.email,
            "phone_number": row.phone_number,
            "address": row.address
        }




@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE customers
                SET 
                    customer_type = :customer_type,
                    customer_name = :customer_name,
                    gst_number = :gst_number,
                    email = :email,
                    phone_number = :phone_number,
                    address = :address,
                    updated_at = NOW()
                WHERE customer_id = :customer_id 
                AND is_active = TRUE
            """),
            {
                "customer_type": customer.customer_type,
                "customer_name": customer.customer_name,
                "gst_number": customer.gst_number,
                "email": customer.email,
                "phone_number": customer.phone_number,
                "address": customer.address,
                "customer_id": customer_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return {"message": "Customer updated successfully"}




@router.delete("/{customer_id}")
def delete_customer(customer_id: int,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE customers
                SET
                    is_active = FALSE,
                    updated_at = NOW()
                WHERE customer_id = :customer_id
            """),
            {"customer_id": customer_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return {"message": "Customer deleted successfully"}
    


