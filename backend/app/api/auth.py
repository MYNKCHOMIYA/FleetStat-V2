from datetime import timedelta
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.api.deps import SessionDep, get_current_active_user, get_current_admin
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, session: SessionDep) -> Any:
    user = session.execute(
        select(User).where(User.email == user_in.email)
    ).scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=400,
            detail=" the use with this email id is already exists",
        )

    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        username=user_in.username,
    )
    session.add(db_user)
    session.commit()
    return db_user

@router.post("/login", response_model=Token)
def login_access_token(
    session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = session.execute(
        select(User).where(User.email == form_data.username)
    ).scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=" incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.user_id, expire_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
    
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)) -> Any:
    return current_user

@router.get("/users", response_model=List[dict])
def read_all_users(
    session: SessionDep,
    current_admin: User = Depends(get_current_admin),
):
    users = session.scalars(select(User)).all()
    return [{"id": u.user_id, "email": u.email, "role": u.role} for u in users]