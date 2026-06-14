from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from jose import jwt, JWTError
from app.database import engine
from app.auth import (
    SECRET_KEY,
    create_access_token,
    verify_password,
    create_refresh_token,
    ALGORITHM
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
        refresh_token = create_refresh_token(
            {
                "sub": str(db_user.user_id)
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@router.post("/refresh")
def refresh_token(
    refresh_token: str
):
    try:

        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        with engine.connect() as conn:

            user = conn.execute(
                text("""
                    SELECT *
                    FROM users
                    WHERE user_id = :user_id
                    AND is_active = TRUE
                """),
                {
                    "user_id": user_id
                }
            ).fetchone()

            if user is None:
                raise HTTPException(
                    status_code=401,
                    detail="User not found"
                )

            new_access_token = create_access_token(
                {
                    "sub": str(user.user_id),
                    "username": user.username,
                    "role": user.role
                }
            )

            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )


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
