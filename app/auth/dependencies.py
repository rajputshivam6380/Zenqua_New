from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def get_current_actor(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return {
            "email": payload.get("sub"),
            "role": payload.get("role"),
            "type": payload.get("type"),  # admin / employee
            "mnc_id": payload.get("mnc_id"),
            "organization_id": payload.get("organization_id"),
            "id": payload.get("id")
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(roles: list):
    def checker(user=Depends(get_current_actor)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Access Denied")
        return user
    return checker