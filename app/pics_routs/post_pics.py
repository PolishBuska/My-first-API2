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


@router.get('/images')
def images():
    out = []
    for filename in os.listdir('app/static/images'):
        out.append({"name":filename.split('.')[0],
                    "path":"/static/images/" + filename})
    return out

@router.post('/')
async def create_file(file: UploadFile = File(...)):
    file_location = f"app/static/images/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}




