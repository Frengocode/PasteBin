from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    pastes_owned = relationship("Paste", foreign_keys="[Paste.owner_id]", back_populates="owner")
    pastes_shared_with = relationship("Paste", foreign_keys="[Paste.shared_with]", back_populates="shared_with_user")
    pastes_shared_by = relationship("Paste", foreign_keys="[Paste.shared_by]", back_populates="shared_by_user")

class Paste(Base):
    __tablename__ = "pastes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text, nullable=False)
    unique_id = Column(String, unique=True, index=True, default=lambda: str (uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    shared_with = Column(Integer, ForeignKey("users.id"), nullable=True)
    shared_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", foreign_keys=[owner_id], back_populates="pastes_owned")
    shared_with_user = relationship("User", foreign_keys=[shared_with])
    shared_by_user = relationship("User", foreign_keys=[shared_by])

