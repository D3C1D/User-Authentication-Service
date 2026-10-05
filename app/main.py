from fastapi import FastAPI
from app.database.connection import engine
from app.database.connection import Base
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "User Authentication Service"}