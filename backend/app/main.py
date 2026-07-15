from fastapi import FastAPI
from app.core.api.user import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Fleetstat V2 API"}

