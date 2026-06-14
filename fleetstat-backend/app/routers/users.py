from fastapi import APIRouter, HTTPException ,Depends
from app.auth import hash_password
from sqlalchemy import text
from app.database import engine
from app.schemas import *
from app.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("")
def create_user(user: UserCreate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO users (
                    username,
                    email,
                    password_hash,
                    role,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (
                    :username,
                    :email,
                    :password_hash,
                    :role,
                    TRUE,
                    NOW(),
                    NOW()
                    )
                RETURNING user_id
            """),
            {
                "username": user.username,
                "email": user.email,
                "password_hash": hash_password(user.password),
                "role": user.role
            }
        )
        user_id = result.scalar()

    return {
        "message": "User created successfully",
        "user_id": user_id
    }
    


@router.get("")
def get_users(current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM users
            WHERE is_active = TRUE
        """))
        rows = result.fetchall()

        return [
            {
                "user_id": row.user_id,
                "username": row.username,
                "email": row.email,
                "role": row.role,
                "is_active": row.is_active
            }
            for row in rows
        ]
        


@router.get("/{user_id}")
def get_user(user_id: int, current_user=Depends(require_admin)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT *
                FROM users
                WHERE user_id = :user_id 
                AND is_active = TRUE
            """),
            {"user_id": user_id}
        )
        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "user_id": row.user_id,
            "username": row.username,
            "email": row.email,
            "role": row.role,
            "is_active": row.is_active
        }
        


@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate,current_user=Depends(require_admin)):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE users
                SET 
                   username = :username,
                    email = :email,
                    password_hash = :password_hash,
                    role = :role,
                    updated_at = NOW()
                 WHERE user_id = :user_id
            """),
            {
                    
                    "username" :user.username,
                    "email":user.email,
                    "password_hash":user.password_hash,
                    "role":user.role,
                    "user_id":user_id,
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {"message": "User updated successfully"}
    


@router.delete("/{user_id}")
def delete_user(user_id: int,current_user=Depends(require_admin)):
    with engine.begin()  as conn:
        result = conn.execute(
            text("""
                UPDATE users
                SET
                    is_active = FALSE,
                    updated_at = NOW()
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {"message": "User deleted successfully"}



