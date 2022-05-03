#!usr/bin/env python3

from fastapi import FastAPI ,Response , status, HTTPException , Depends
from fastapi.params import Body
from typing import Optional , List
from pydantic import BaseModel 
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models , schemas , utils
from .database import engine ,SessionLocal , get_db
from sqlalchemy.orm import Session 
from .routes import post, user , auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




    
while True:
    try:
        conn = psycopg2.connect(host = 'localhost' , database = 'fastapi' , user='postgres' , password = 'ngai' , cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successfully")
        break
    except Exception as error:
        print("connecting to database field")
        print("error : "  , error )
        time.sleep(2)
    
    
    
def find_post(id):
    for p in my_post:
        if p['id'] ==id:
            return p
my_post = []
def find_index_post(id):
    for i , p in enumerate(my_post):
        if p['id'] == id:
            return i
        

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def index():
    return {"hello world"}

