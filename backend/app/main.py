from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/{settings.API_V1_STR}/openapi.json",
    docs_url=f"/{settings.API_V1_STR}/docs",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",  # Good to include both variations
]

# Allow frontend requests (local file or dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"/{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Fleetstat V2 API"}
