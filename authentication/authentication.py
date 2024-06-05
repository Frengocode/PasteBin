from fastapi import APIRouter, Depends, HTTPException
from databse import  database, models
from sqlalchemy.orm import Session
from .hash import Hash
from .token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from databse import schemas, models, database
from .hash import Hash
from .oauth import get_current_user
from typing import List

router = APIRouter(
    tags=['Authentication'],
)


@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db) ):
    user = db.query(models.User).filter(models.User.username == request.username ).first()
    if not user:
        raise HTTPException(detail={'error': 'Invalid Creadion'}, status_code=402)

    if not Hash.verify(user.password, request.password):
        raise HTTPException(detail=f'In Correct', status_code=402)

    access_token = create_access_token(
        data={"sub": user.username}
        )
    return {"access_token":access_token, "token_type":"bearer"}





@router.post('/', response_model=schemas.UserSchema)
async def sign_up(request: schemas.UserSchema, db: Session = Depends(database.get_db)):
    exist_user = db.query(models.User).filter(models.User.username ==  request.username).first()

    if exist_user:
        raise HTTPException(detail=f' {request.username} Al Ready Exist', status_code=402)
    
    hashed_password = Hash.bcrypt(request.password)

    new_user = models.User(
        username = request.username,
        password = hashed_password,
        email = request.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get('/{id}', response_model=schemas.UserReadSchema)
async def user_detail(id:int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    detail = db.query(models.User).filter(models.User.id == id).first()
    if detail:
        return detail
    raise HTTPException(detail='Not found', status_code=404)




@router.get('/', response_model=List[schemas.UserReadSchema])
async def get_all_users(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users
