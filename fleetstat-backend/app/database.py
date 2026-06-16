from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # Auto-reconnect on stale connections (prevents errors after DB restart)
    pool_size=10,              # Connection pool size
    max_overflow=20,           # Max additional connections when pool is full
    pool_recycle=300,          # Recycle connections every 5 minutes (prevents timeout disconnects)
)

# Log the database connection target on startup (without password)
print(f"[FleetStat DB] Connecting to postgresql://{DB_USER}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")
