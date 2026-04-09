from sqlalchemy import Column,String,Integer,Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Mnc(Base):
    __tablename__ = "mnc"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    created_by = Column(String(100))

    organizations = relationship("Org", back_populates="mnc", cascade="all, delete")
    users = relationship("User", back_populates="mnc", cascade="all, delete")
    tasks = relationship("Task", back_populates="mnc")
    admin = relationship("Admin", back_populates="mnc", uselist=False)