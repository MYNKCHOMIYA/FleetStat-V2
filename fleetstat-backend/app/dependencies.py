from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import text
from app.database import engine
from app.auth import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        return None


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload


def require_admin(
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user
    
    
def require_driver(
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "driver":
        raise HTTPException(
            status_code=403,
            detail="Driver access required"
        )

    return current_user

def verify_driver_trip(conn, trip_id, user_id):
    ownership = conn.execute(
        text("""
            SELECT 1
            FROM trip_assignments ta
            JOIN drivers d
                ON ta.driver_id = d.driver_id
            WHERE ta.trip_id = :trip_id
            AND d.user_id = :user_id
        """),
        {
            "trip_id": trip_id,
            "user_id": user_id
        }
    ).fetchone()

    if ownership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this trip"
        )


def verify_driver_shipment(conn, shipment_id, user_id):
    ownership = conn.execute(
        text("""
            SELECT 1
            FROM shipments s
            JOIN trip_assignments ta ON s.trip_id = ta.trip_id
            JOIN drivers d ON ta.driver_id = d.driver_id
            WHERE s.shipment_id = :shipment_id
            AND d.user_id = :user_id
        """),
        {
            "shipment_id": shipment_id,
            "user_id": user_id
        }
    ).fetchone()

    if ownership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to the trip for this shipment"
        )


def verify_driver_fuel_log(conn, fuel_log_id, user_id):
    ownership = conn.execute(
        text("""
            SELECT 1
            FROM fuel_logs fl
            JOIN trip_assignments ta ON fl.trip_id = ta.trip_id
            JOIN drivers d ON ta.driver_id = d.driver_id
            WHERE fl.fuel_log_id = :fuel_log_id
            AND d.user_id = :user_id
        """),
        {
            "fuel_log_id": fuel_log_id,
            "user_id": user_id
        }
    ).fetchone()

    if ownership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to the trip for this fuel log"
        )
        
def verify_driver_damage_report(
    conn,
    damage_id,
    user_id
):
    ownership = conn.execute(
        text("""
            SELECT 1
            FROM damage_reports dr
            JOIN shipments s
                ON dr.shipment_id = s.shipment_id
            JOIN trip_assignments ta
                ON s.trip_id = ta.trip_id
            JOIN drivers d
                ON ta.driver_id = d.driver_id
            WHERE dr.damage_id = :damage_id
            AND d.user_id = :user_id
        """),
        {
            "damage_id": damage_id,
            "user_id": user_id
        }
    ).fetchone()

    if ownership is None:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this damage report"
        )
