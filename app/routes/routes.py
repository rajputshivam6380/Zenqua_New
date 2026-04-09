from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse,UserUpdate,LoginSchema,UserPatch
from app.services import user_service
from app.auth.jwt_handler import create_access_token
from app.auth.hashing import hash_password, verify_password
from app.models.user_model import User
from app.auth.dependencies import get_current_actor, require_role


router = APIRouter(prefix="/users")


@router.get("/my-scope-users")
def get_users(
    db: Session = Depends(get_db),
    user=Depends(get_current_actor)
):
    return user_service.get_users_by_role_scope(db, user)



@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # return user_service.create_user_service(db,user)
    return user_service.create_user_service(
    db,
    user.name,
    user.email,
    user.password,
    # user.role,
    user.mnc_id,
    user.organization_id
)

@router.get("/all_users")
def get_all_users(
    db: Session = Depends(get_db),
    user=Depends(require_role(["super_admin","mnc_admin","org_admin"]))
):
    return user_service.get_users_by_role_scope(db)





@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_actor)
):
    return user_service.get_user_by_id_service(db, user_id, current_user)



@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user_service(db, user_id, user.name, user.email)


# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user_service(db, user_id)



@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(user_id: int, user: UserPatch, db: Session = Depends(get_db)):
    return user_service.patch_user_service(db, user_id, user)
