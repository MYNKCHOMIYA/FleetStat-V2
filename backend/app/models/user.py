from sqlalchemy import String,func,Boolean,DateTime
from sqlalchemy.orm import Mapped, mapped_column ,relationship
from app.models.base import Base
from datetime import datetime
import uuid

class user(Base):
    __tablename = "users"
    
    user_id : Mapped[str] = mapped_column(
        String, primary_key=True,default=lambda:str(uuid.uuid4)
    )
    
    username:Mapped[str] =mapped_column(String,nullable=False)
    
    email:Mapped[str] =mapped_column(String,unique =True, index = True , nullable = False
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean,default=True
    )
    
    hashed_password: Mapped[str] = mapped_column(String,nullable = False
    )
    
    role: Mapped[str] = mapped_column(String,default="user"
    )
    
    created_at :Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now()
    )
    
    updated_at :Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now()
    )
    
    