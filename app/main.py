#!usr/bin/env python3

from fastapi import FastAPI ,Response , status, HTTPException , Depends
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models 
from .database import engine ,SessionLocal , get_db
from sqlalchemy.orm import Session 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    
    title : str
    content : str
    published : bool = True
    
    
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
        
@app.get("/") 
def read_root():
    return {"hello" : "world"}

@app.get("/sqlalchemy")
def test(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data" : posts }

@app.get("/posts")
def get_post():
    cursor.execute("""
                   SELECT  * FROM posts
                   """) 
    posts = cursor.fetchall()
    print(posts)
    return { "data" : posts}


@app.post("/createposts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title , content ,published) VALUES (%s,%s ,%s) RETURNING * """,
                   (post.title , post.content , post.published))
    new_post= cursor.fetchone()
    conn.commit()
    return {"data" : new_post }

@app.get("/post/latest")
def get_latest_post():
    post= my_post[len(my_post)  -1]
    return {"detail" : post}

@app.get("/post/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """ , (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id : {id} was not found ")
  
    return {"post_detail" : post}


@app.delete("/post/{id}" , status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""" , (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    
    if delete_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with  id : {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def update_post(id : int ,  post  : Post):
    cursor.execute("""UPDATE 
                   posts 
                   SET 
                   title = %s, content = %s , published = %s 
                   WHERE id = %s
                   RETURNING *""", 
                   (post.title , post.content, post.published ,(str(id) , )))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if update_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with  id : {id} does not exist")
        

    
    return {"data" : updated_post}