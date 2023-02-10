from fastapi import status,HTTPException,Response,FastAPI,Depends,APIRouter
from .. import models,schemas,JWT_SERVICE
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func
from fastapi.staticfiles import StaticFiles
import os

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



