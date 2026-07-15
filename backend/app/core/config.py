import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

BACKEND_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
ENV_FILE_PATH = os.path.join(BACKEND_DIR,".env")

if os.path.exists(ENV_FILE_PATH):
    load_dotenv(ENV_FILE_PATH)
    
class Settings(BaseSettings):
    PROJECT_NAME: str = "FLEETSTAT API"
    API_V1_STR: str = "api/v1"
    
    # Database configurations
    DATABASE_URL: str | None = None
    
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_SERVER: str | None = None
    POSTGRES_DB: str | None = None
    
    SECRET_KEY: str = "temporary-secret-key-for-development-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    def get_database_url(self) -> str:
        url = self.DATABASE_URL
        if not url:
            if all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_SERVER, self.POSTGRES_DB]):
                url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}?sslmode=require"
            else:
                raise ValueError("Either DATABASE_URL or POSTGRES_* settings must be configured.")
        
        # Replace postgres:// with postgresql:// if needed for SQLAlchemy
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url
        
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")

settings = Settings() # type : ignore