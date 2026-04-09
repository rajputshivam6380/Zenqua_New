from sqlalchemy import Column,Integer,String,ForeignKey,Enum
from app.enum_fdr.status_enum import Status
from sqlalchemy.orm import relationship
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(400))
    description = Column(String(300))
    status = Column(Enum(Status))
    assigned_by=Column(String(100))
    assigned_to=Column(String(100))

    employee_id = Column(Integer, ForeignKey("users.id"))
    mnc_id = Column(Integer, ForeignKey("mnc.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    employee = relationship("User", back_populates="tasks")
    mnc = relationship("Mnc", back_populates="tasks")
    organization = relationship("Org", back_populates="tasks")