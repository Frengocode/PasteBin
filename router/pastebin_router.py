from fastapi import  Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from databse.models import Paste, User
from databse.schemas import PasteCreate, PasteRead,SharePasteRead, PasteUpdateSchema
from databse.database import get_db
from authentication.oauth import get_current_user
from typing import List

router = APIRouter(
    tags=['PasteBin']
)



@router.post("/pastes/", response_model=PasteRead)
async def create_new_paste(paste: PasteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_paste = Paste(
        title=paste.title,
        content=paste.content,
        owner_id=current_user.id
        
    )
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    return db_paste


@router.get("/pastes/{id}", response_model=PasteRead)
async def read_paste(id: int, db: Session = Depends(get_db)):
    db_paste = db.query(Paste).filter(Paste.id == id).first()
    if not db_paste :
        raise HTTPException(status_code=404, detail="Paste not found")
    return db_paste


@router.post("/share/{paste_id}/{recipient_id}")
async def share_paste(paste_id: int, recipient_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_paste = db.query(Paste).filter(Paste.id == paste_id).first()
    if db_paste is None:
        raise HTTPException(status_code=404, detail=f"Paste with id {paste_id} not found")
    
    db_paste.shared_with = recipient_id
    db_paste.shared_by = current_user.id
    db.commit()
    return {"message": "Paste shared successfully"}



@router.get("/shared_pastes/", response_model=List[SharePasteRead])
async def get_shared_pastes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    shared_pastes = db.query(Paste).filter(Paste.shared_with == current_user.id).all()
    
    if not shared_pastes:
        raise HTTPException(status_code=404, detail="No shared pastes found")
    
    share_pastes_read = []
    for paste in shared_pastes:
        share_paste_read = SharePasteRead(
            id=paste.id,
            title=paste.title,
            content=paste.content,
            created_at=paste.created_at,
            owner_id=paste.owner_id,
            shared_by=paste.shared_by   
        )
        share_pastes_read.append(share_paste_read)
    
    return share_pastes_read


@router.delete('/{id}')
async def delete(id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete = db.query(Paste).filter(Paste.id == id).first()

    if delete:
        if delete.owner_id == current_user.id:
            db.delete(delete)
            db.commit()
        
        raise HTTPException(detail='Author error', status_code=402)
    

    return 'Delete Succsesfully'


@router.put('/{id}', response_model=PasteRead)
def update(request: PasteUpdateSchema, id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    update_model = db.query(Paste).filter(Paste.id == id).first()

    if update_model:
        if update_model.owner_id == current_user.id:

            update_model.title = request.title
            update_model.content = request.content
            db.commit()

            return update_model
                    
    
@router.get('/', response_model=List[PasteRead])
async def get_pastes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    all_pastest = db.query(Paste).all()
    return all_pastest