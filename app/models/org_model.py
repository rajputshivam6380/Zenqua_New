from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Org(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    mnc_id = Column(Integer, ForeignKey("mnc.id"))   # ✅ MUST

    mnc = relationship("Mnc", back_populates="organizations")
    users = relationship("User", back_populates="org", cascade="all, delete")
    tasks = relationship("Task", back_populates="organization", cascade="all, delete") 
    admin = relationship("Admin", back_populates="organization", uselist=False)