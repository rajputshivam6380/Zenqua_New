from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_actor

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/dashboard")
def dashboard(user=Depends(get_current_actor)):
    if user["type"] != "admin":
        return {"error": "Only admin allowed"}
    return {"msg": "Welcome Admin"}