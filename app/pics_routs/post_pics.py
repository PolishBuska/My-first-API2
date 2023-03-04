import http

from fastapi import status,HTTPException,Response,FastAPI,Depends,APIRouter,UploadFile,File
from .. import models,schemas,JWT_SERVICE
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func
from fastapi.staticfiles import StaticFiles
import os
import shutil

router = APIRouter(
    prefix='/jpgs',
    tags=['pics']
)


@router.get('/images',status_code=status.HTTP_200_OK)
def images():
    out = []
    for filename in os.listdir('app/static/images'):
        out.append({"name":filename.split('.')[0],
                    "path":"/static/images/" + filename})
    return out

@router.post('/',response_model=schemas.Picture_out_response)
async def create_file(file: UploadFile = File(...),
                      current_user: int = Depends(JWT_SERVICE.get_current_user),
                      db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="not authorized to perform requested action'")
    file_location_db = {"url":f"app/static/images/{file.filename}"}
    file_location_db = schemas.PictureOut(**file_location_db)

    file_location = f"app/static/images/{file.filename}"
    picture = models.Picture(owner_id =current_user.id, **file_location_db.dict())
    db.add(picture)
    db.commit()
    db.refresh(picture)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    user = db.query(models.User).where(models.User.id == current_user.id).first()
    return {"url":file_location,"owner":user}




