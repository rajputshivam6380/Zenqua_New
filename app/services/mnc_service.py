from sqlalchemy.orm import Session
from app.models.mnc_model import Mnc
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exception_handler import handle_db_error


def create_mnc_service(db:Session,name:str,created_by:str):
    try:
        mnc=Mnc(name=name,created_by=created_by)
    
    
        db.add(mnc)
        db.commit()
        db.refresh(mnc)
        
        return mnc
    except SQLAlchemyError as e:
        handle_db_error(db,e)



def get_all_mnc(db:Session):
    return db.query(Mnc).all()


def get_mnc_by_id(db:Session,mnc_id:int):
    return db.query(Mnc).filter(Mnc.id==mnc_id).first()



def update_org(db:Session,mnc_id:int,name:str,created_by:str):
    mnc=db.query(Mnc).filter(Mnc.id==mnc_id).first()
    
    if not mnc:
        raise HTTPException(status_code=404, detail="MNC not found")

    mnc.name=name
    mnc.created_by=created_by
    
    db.commit()
    db.refresh(mnc)
    
    return mnc


def delete_org(db:Session,mnc_id:int):
    mnc=db.query(Mnc).filter(Mnc.id==mnc_id).first()
    
    if not mnc:
        raise HTTPException(status_code=404, detail="Mnc not found")
    
    db.delete(mnc)
    db.commit()
    
    return {"Message": "Mnc deleted succesfully"}