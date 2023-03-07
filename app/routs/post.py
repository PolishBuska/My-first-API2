from fastapi import status,HTTPException,Response,Depends,APIRouter,UploadFile,File
from .. import models,schemas,JWT_SERVICE
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)



@router.get('/',response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip:int = 0,search:Optional[str] = "" ):

    #posts = db.query(models.Post).filter(
        #models.Post.title.contains(search)).limit(
        #limit).offset(skip).all()
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    results =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)).limit(
        limit).offset(skip).all()

    return results

@router.post("/",status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
async def create_posts(post:schemas.CreatePost,
                       db: Session = Depends(get_db),
                 current_user: int = Depends(JWT_SERVICE.get_current_user),
                       file: UploadFile = File(...)):
    #file_location_db = {"url": f"app/static/images/{file.filename}"}
   # file_location_db = schemas.PictureOut(**file_location_db)

    #file_location = f"app/static/images/{file.filename}"
    #picture = models.Picture(owner_id=current_user.id, **file_location_db.dict())
    #db.add(picture)
    #db.commit()
    #db.refresh(picture)
    #with open(file_location, "wb+") as file_object:
       # file_object.write(file.file.read())
   # print(current_user)

    new_post = models.Post(owner_id =current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get('/{id}',response_model=schemas.PostOut)
async def get_post(id: int,
             response: Response,
             db: Session = Depends(get_db),
             current_user: int = Depends(JWT_SERVICE.get_current_user)):
    #cursor.execute("""SELECT * from posts WHERE id = %s """, str((id)))
    #tpost = cursor.fetchone()
    #tpost = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post id: {id} is not found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(JWT_SERVICE.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id =%s returning *""", str((id)))
    #delp = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='not authorized to perform requested action')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post,status_code=status.HTTP_200_OK)
async def update_posts(id: int,
                 uppost: schemas.CreatePost,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(JWT_SERVICE.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s returning *""",
                   #(post.title,post.content,post.published,str(id)))
    #uppost = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='not authorized to perform requested action')
    post_query.update(uppost .dict(),
                      synchronize_session=False)
    db.commit()
    return  post_query.first()