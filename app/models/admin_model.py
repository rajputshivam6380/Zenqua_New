from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    role = Column(String(50))  # super_admin / mnc_admin / org_admin

    mnc_id = Column(Integer, ForeignKey("mnc.id"), nullable=True, unique=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True, unique=True)

    mnc = relationship("Mnc", back_populates="admin")
    organization = relationship("Org", back_populates="admin")