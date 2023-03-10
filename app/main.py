from fastapi import FastAPI,status,HTTPException
from .routs import post, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .pics_routs import post_pics
import os

origins = ["*"]

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Box social media"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(post_pics.router)


@app.get("/",status_code=status.HTTP_200_OK)
def root():
    return {"Message":"Hello World"}

app.mount("/static", StaticFiles(directory="app/static"),name="static")

