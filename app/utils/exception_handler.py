from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


def handle_db_error(db,error):
    db.rollback()
    raise HTTPException(status_code=500,detail=f"Database Error: (str(error))")