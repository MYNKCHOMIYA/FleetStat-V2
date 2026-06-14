from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text

from app.database import engine
from app.auth import (
    verify_password,
    create_access_token
)

from app.dependencies import (
    get_current_user,
    verify_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM users
                WHERE username = :username
                AND is_active = TRUE
            """),
            {"username": form_data.username}
        )

        db_user = result.fetchone()

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        if not verify_password(
            form_data.password,
            db_user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        access_token = create_access_token(
            {
                "sub": str(db_user.user_id),
                "username": db_user.username,
                "role": db_user.role
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


@router.get("/me")
def me(
    current_user=Depends(get_current_user)
):
    return current_user


@router.get("/test-token")
def test_token(
    token: str,
    current_user=Depends(get_current_user)
):
    return verify_token(token)
