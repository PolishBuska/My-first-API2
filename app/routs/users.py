from fastapi import status,HTTPException,Response,FastAPI,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #HASH the password - user.password

    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user


@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} does not exist')
    return user