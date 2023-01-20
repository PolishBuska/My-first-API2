from fastapi import status,HTTPException,Response,FastAPI,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schemas,database,models
from .. import JWT_SERVICE

router = APIRouter(
    prefix="/vote",
    tags = ['Vote']

)

@router.post('/',status_code=status.HTTP_201_CREATED)
async def voting(vote: schemas.Vote,db: Session = Depends(database.get_db),
           current_user: int = Depends(JWT_SERVICE.get_current_user)):
    vote_query = (db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    ))
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {vote.post_id} does not exist')
    found_vote = vote_query.first()
    if (vote.dir ==1):
        if found_vote:
            raise  HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail=f' user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message':'good'}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"good":"baad"}

