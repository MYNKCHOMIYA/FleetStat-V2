from fastapi import APIRouter

router = APIRouter()

@router.get("/user")
def user():
    return {"message" : "user is incoming "}
