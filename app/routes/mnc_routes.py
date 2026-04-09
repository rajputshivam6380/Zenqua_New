from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.mnc_schema import MncCreate,MncResponse,MncUpdate
from app.services import mnc_service



mnc_router=APIRouter(prefix="/mnc")

@mnc_router.post("/",response_model=MncResponse)
def create_org(mnc:MncCreate,db:Session=Depends(get_db)):
    return mnc_service.create_mnc_service(db,mnc.name,mnc.created_by)



@mnc_router.get("/",response_model=list[MncResponse])
def get_org(db:Session=Depends(get_db)):
    return mnc_service.get_all_mnc(db)


@mnc_router.get("/{mnc_id}",response_model=MncResponse)
def get_org(mnc_id:int,db:Session=Depends(get_db)):
    return mnc_service.get_mnc_by_id(db,mnc_id)


@mnc_router.put("/{mnc_id}",response_model=MncResponse)
def update_mnc(mnc_id:int,mnc:MncUpdate,db:Session=Depends(get_db)):
    return mnc_service.update_org(db,mnc_id,mnc.name,mnc.created_by)


@mnc_router.delete("/{mnc_id}")
def delete_mnc(mnc_id:int,db:Session=Depends(get_db)):
    return mnc_service.delete_org(db,mnc_id)