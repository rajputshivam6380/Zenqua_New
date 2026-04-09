from sqlalchemy.orm import Session
from app.models.user_model import User
from fastapi import HTTPException
from app.auth.hashing import hash_password
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exception_handler import handle_db_error






def create_user_service(db, name, email, password, mnc_id=None, organization_id=None):
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=name,
        email=email,
        password = hash_password(password),
        # role=role,
        mnc_id=mnc_id,
        organization_id=organization_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_all_users_service(db: Session):
    return db.query(User).all()


def get_user_by_id_service(db, user_id, current_user):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ EMPLOYEE → only self
    if current_user["role"] == "employee":
        if user.id != current_user["id"]:
            raise HTTPException(
                status_code=403,
                detail="You can only view your own profile"
            )

    # ✅ ORG ADMIN
    elif current_user["role"] == "org_admin":
        if user.organization_id != current_user["organization_id"]:
            raise HTTPException(
                status_code=403,
                detail="Access denied to other organizations"
            )

    # ✅ MNC ADMIN
    elif current_user["role"] == "mnc_admin":
        if user.mnc_id != current_user["mnc_id"]:
            raise HTTPException(
                status_code=403,
                detail="Access denied to other MNCs"
            )

    return user





def update_user_service(db, user_id, name, email, current_user):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if current_user["role"]=="employee":
            if user.id!=current_user["id"]:
                raise HTTPException(403,"You cant update others profile")
        elif current_user["role"]=="org_admin":
            if user.organization_id != current_user["organization_id"]:
                raise HTTPException(403, "Not your organization")

        elif current_user["role"] == "mnc_admin":
             if user.mnc_id != current_user["mnc_id"]:
                raise HTTPException(403, "Not your MNC")
        user.name = name
        user.email = email

        db.commit()
        db.refresh(user)

        return user

    except SQLAlchemyError as e:
        handle_db_error(db, e)


def delete_user_service(db, user_id, current_user):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    if current_user["role"] == "employee":
        raise HTTPException(403, "Employees cannot delete users")

    if current_user["role"] == "org_admin":
        if user.organization_id != current_user["organization_id"]:
            raise HTTPException(403, "Not your organization")

    if current_user["role"] == "mnc_admin":
        if user.mnc_id != current_user["mnc_id"]:
            raise HTTPException(403, "Not your MNC")

    db.delete(user)
    db.commit()

    return {"msg": "Deleted successfully"}


# Patch
def patch_user_service(db, user_id, user_data):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.dict(exclude_unset=True)

    if "role" in update_data and update_data["role"] == "admin":
        existing_admin = db.query(User).filter(User.role == "admin").first()

        if existing_admin and existing_admin.id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Admin role already assigned to another user"
            )

    for key, value in update_data.items():

        if key == "password":
            value = hash_password(value)

        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user





def get_users_by_role_scope(db, current_user):

    if current_user["role"] == "mnc_admin":
        return db.query(User).filter(
            User.mnc_id == current_user["mnc_id"]
        ).all()

    elif current_user["role"] == "org_admin":
        return db.query(User).filter(
            User.organization_id == current_user["organization_id"]
        ).all()

    elif current_user["role"] == "employee":
        # ✅ ONLY HIMSELF
        return db.query(User).filter(
            User.id == current_user["id"]
        ).all()

    else:
        raise HTTPException(status_code=403, detail="Unauthorized access")