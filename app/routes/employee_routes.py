from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_actor

employee_router = APIRouter(prefix="/employee", tags=["Employee"])

@employee_router.get("/profile")
def profile(user=Depends(get_current_actor)):
    if user["type"] != "employee":
        return {"error": "Only employee allowed"}
    return {"msg": "Employee profile", "user": user}