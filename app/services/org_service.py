from sqlalchemy.orm import Session
from app.models.org_model import Org
from fastapi import HTTPException


# def create_org_service(db:Session,name:str,created_by:str):
#     org=Org(name=name,created_by=created_by)

def create_org_service(db:Session,name:str,mnc_id:int):
    org=Org(name=name,mnc_id=mnc_id)
    
    db.add(org)
    db.commit()
    db.refresh(org)
    
    return org



def get_all_organization(db:Session):
    return db.query(Org).all()


def get_org_by_id(db:Session,org_id:int):
    return db.query(Org).filter(Org.id==org_id).first()



# def update_org(db:Session,org_id:int,name:str,created_by:str):
#     org=db.query(Org).filter(Org.id==org_id).first()
    
    
def update_org(db:Session,org_id:int,name:str,mnc_id:int):
    org=db.query(Org).filter(Org.id==org_id).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    org.name=name
    org.mnc_id=mnc_id
    
    db.commit()
    db.refresh(org)
    
    return org


def delete_org(db:Session,org_id:int):
    org=db.query(Org).filter(Org.id==org_id).first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    db.delete(org)
    db.commit()
    
    return {"Message": "Organization deleted succesfully"}