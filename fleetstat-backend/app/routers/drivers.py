from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text

from app.database import engine
from app.schemas import DriverCreate, DriverUpdate
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

@router.post("/", dependencies=[Depends(require_admin)])
def create_driver(driver: DriverCreate):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO drivers (
                    full_name,
                    user_id,
                    date_of_birth,
                    address,
                    license_number,
                    email,
                    phone_number,
                    prior_experience_years,
                    joining_date,
                    employment_status,
                    availability_status,
                    created_at,
                    updated_at,
                    is_active
                )
                VALUES (
                    :full_name,
                    :user_id,
                    :date_of_birth,
                    :address,
                    :license_number,
                    :email,
                    :phone_number,
                    :prior_experience_years,
                    :joining_date,
                    'active',
                    'idle',
                    NOW(),
                    NOW(),
                    TRUE
                )
                RETURNING driver_id
            """),
            {
                "full_name": driver.full_name,
                "date_of_birth": driver.date_of_birth,
                "address": driver.address,
                "license_number": driver.license_number,
                "email": driver.email,
                "phone_number": driver.phone_number,
                "prior_experience_years": driver.prior_experience_years,
                "joining_date": driver.joining_date,
                "user_id": driver.user_id
            }
        )
        driver_id = result.scalar()

    return {
        "message": "Driver created successfully",
        "driver_id": driver_id
    }


@router.get("/")
def get_drivers(current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM drivers
            WHERE is_active = TRUE
        """))
        rows = result.fetchall()

        return [
            {
                "driver_id": row.driver_id,
                "full_name": row.full_name,
                "license_number": row.license_number,
                "experience": row.prior_experience_years,
            }
            for row in rows
        ]


@router.get("/{driver_id}")
def get_driver(driver_id: int, current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM drivers
                WHERE driver_id = :driver_id 
                AND is_active = TRUE
            """),
            {"driver_id": driver_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Driver not found"
            )

        return {
            "driver_id": row.driver_id,
            "full_name": row.full_name,
            "user_id": row.user_id,
            "email": row.email,
            "phone_number": row.phone_number
        }


@router.put("/{driver_id}", dependencies=[Depends(require_admin)])
def update_driver(driver_id: int, driver: DriverUpdate):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE drivers
                SET 
                    address = :address,
                    phone_number = :phone_number,
                    email = :email,
                    updated_at = NOW()
                WHERE driver_id = :driver_id 
                AND is_active = TRUE
            """),
            {
                "address": driver.address,
                "phone_number": driver.phone_number,
                "email": driver.email,
                "driver_id": driver_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Driver not found"
            )

        return {"message": "Driver updated successfully"}


@router.delete("/{driver_id}", dependencies=[Depends(require_admin)])
def delete_driver(driver_id: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE drivers
                SET
                    is_active = FALSE,
                    employment_status = 'inactive',
                    updated_at = NOW()
                WHERE driver_id = :driver_id
            """),
            {"driver_id": driver_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Driver not found"
            )

        return {"message": "Driver deleted successfully"}
