from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PasteUpdateSchema(BaseModel):
    title: str
    content: str


class UserReadSchema(BaseModel):
    id: int
    email: str
    username: str



class UserSchema(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True


class PasteCreate(BaseModel):
    title: str
    content: str


class TokenData(BaseModel):
    username: Optional[str] = None

class PasteRead(BaseModel):
    id: int
    title: str
    content: str
    unique_id: str
    created_at: datetime
    owner_id: int
    shared_with: Optional[int] = None
    shared_by: Optional[int] = None

    class Config:
        orm_mode = True

class SharePasteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    shared_by: Optional[int] = None

    class Config:
        orm_mode = True