from fastapi import FastAPI
from .routs import post, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/hello")
def root():
    return {"Message":"Goood"}

