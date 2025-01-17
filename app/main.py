from fastapi import FastAPI
from .database import engine
from . import models
from .Routers import Posts, Users,Auth,Votes
from fastapi.middleware.cors import CORSMiddleware

 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Posts.router)
app.include_router(Users.router)
app.include_router(Auth.router)
app.include_router(Votes.router)



