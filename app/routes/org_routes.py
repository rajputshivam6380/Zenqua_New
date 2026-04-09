from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.org_schema import OrgCreate,OrgResponse,OrgUpdate
from app.services import org_service



org_router=APIRouter(prefix="/org")

@org_router.post("/",response_model=OrgResponse)
def create_org(org:OrgCreate,db:Session=Depends(get_db)):
    return org_service.create_org_service(db,org.name,org.mnc_id)



@org_router.get("/",response_model=list[OrgResponse])
def get_org(db:Session=Depends(get_db)):
    return org_service.get_all_organization(db)


@org_router.get("/{org_id}",response_model=OrgResponse)
def get_org(org_id:int,db:Session=Depends(get_db)):
    return org_service.get_org_by_id(db,org_id)


@org_router.put("/{org_id}",response_model=OrgResponse)
def update_org(org_id:int,org:OrgUpdate,db:Session=Depends(get_db)):
    return org_service.update_org(db,org_id,org.name,org.mnc_id)


@org_router.delete("/{org_id}")
def delete_org(org_id:int,db:Session=Depends(get_db)):
    return org_service.delete_org(db,org_id)