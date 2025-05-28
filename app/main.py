# app/main.py

from fastapi import FastAPI
from app.routes import users, external_api

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(external_api.router, prefix="/external", tags=["External APIs"])

@app.get("/")
def root():
    return {"message": "FastAPI API call demo is working!"}
