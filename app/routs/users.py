from fastapi import status,HTTPException,Response,FastAPI,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.exc import IntegrityError
from typing import Optional

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #HASH the password - user.password
    try:
        if len(user.password) <= 4:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="password's lenght should be more then 5")
        user.password = utils.hash(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail="already registered")



@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} does not exist')
    return user