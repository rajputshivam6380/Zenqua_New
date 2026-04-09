from sqlalchemy import Column, Integer, String,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    role = Column(String(100))  # admin / manager / employee
    
    mnc_id = Column(Integer, ForeignKey("mnc.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    mnc = relationship("Mnc", back_populates="users")
    org = relationship("Org", back_populates="users")
    tasks = relationship("Task", back_populates="employee")