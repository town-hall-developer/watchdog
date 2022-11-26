from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parser import parse
from pydantic import BaseModel
# from app.recommend.routes import recommend_router

app = FastAPI()
# app.include_router(recommend_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

class BasicRequest(BaseModel):
    query: str

@app.post("/parse")
def health_check(request: BasicRequest):
    return parse(request.query)