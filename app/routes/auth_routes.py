from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin_model import Admin
from app.models.user_model import User
from app.schemas.user_schema import LoginSchema
from app.schemas.admin_schema import AdminCreate
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token

auth_router = APIRouter()

# ✅ ADMIN REGISTER
@auth_router.post("/admin/register")
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):

    if admin.role == "mnc_admin":
        existing = db.query(Admin).filter(Admin.mnc_id == admin.mnc_id).first()
        if existing:
            raise HTTPException(400, "MNC already has admin")

    if admin.role == "org_admin":
        existing = db.query(Admin).filter(Admin.organization_id == admin.organization_id).first()
        if existing:
            raise HTTPException(400, "ORG already has admin")

    new_admin = Admin(
        name=admin.name,
        email=admin.email,
        password=hash_password(admin.password),
        role=admin.role,
        mnc_id=admin.mnc_id,
        organization_id=admin.organization_id
    )

    db.add(new_admin)
    db.commit()

    return {"msg": "Admin created successfully"}


# ✅ ADMIN LOGIN
@auth_router.post("/admin/login")
def admin_login(data: LoginSchema, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.email == data.email).first()

    if not admin:
        raise HTTPException(401, "Admin not found")

    if not verify_password(data.password, admin.password):
        raise HTTPException(401, "Wrong password")

    token = create_access_token({
        "sub": admin.email,
        "role": admin.role,
        "type": "admin",
        "mnc_id": admin.mnc_id,
        "organization_id": admin.organization_id,
        "id": admin.id
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": admin.role
        }

# ✅ EMPLOYEE LOGIN
@auth_router.post("/employee/login")
def employee_login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(401, "User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(401, "Wrong password")

    token = create_access_token({
        "sub": user.email,
        "role": "employee",
        "type": "employee",
        "mnc_id": user.mnc_id,
        "organization_id": user.organization_id,
        "id": user.id
    })

    return {"access_token": token}