from sqlalchemy.orm import Session
from databse.models import Paste
from  typing import List
from fastapi import HTTPException


def get_paste(db: Session, paste_id: str):
    return db.query(Paste).filter(Paste.unique_id == paste_id).first()


def get_shared_pastes_for_user(db: Session, user_id: int) -> List[Paste]:
    return db.query(Paste).filter(Paste.shared_with == user_id).all()


def share_paste(db: Session, paste_id: int, recipient_id: int) -> Paste:
    db_paste = db.query(Paste).filter(Paste.id == paste_id).first()
    if db_paste is None:
        raise HTTPException(status_code=404, detail=f"Paste with id {paste_id} not found")
    
    if db_paste.shared_with is None:
        db_paste.shared_with = recipient_id
    else:
        db_paste.shared_with.append(recipient_id)
    
    db.commit()
    db.refresh(db_paste)
    
    return db_paste