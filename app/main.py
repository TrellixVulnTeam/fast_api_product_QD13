#!usr/bin/env python3

from fastapi import FastAPI ,Response , status, HTTPException , Depends
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models , schemas
from .database import engine ,SessionLocal , get_db
from sqlalchemy.orm import Session 

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
        
@app.get("/") 
def read_root():
    return {"hello" : "world"}


@app.get("/posts")
def get_post(db : Session = Depends(get_db)):
    # cursor.execute("""
    #                SELECT  * FROM posts
    #                """) 
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return  posts


@app.post("/createposts", status_code = status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate , db : Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title , content ,published) VALUES (%s,%s ,%s) RETURNING * """,
    #                (post.title , post.content , post.published))
    # new_post= cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post 

@app.get("/post/latest")
def get_latest_post():
    post= my_post[len(my_post)  -1]
    return  post

@app.get("/post/{id}")
def get_post(id : int , db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """ , (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id : {id} was not found ")
  
    return  post


@app.delete("/post/{id}" , status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db : Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""" , (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with  id : {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def update_post(id : int ,  updated_post  : schemas.PostCreate , db : Session = Depends(get_db)) :
    # cursor.execute("""UPDATE 
    #                posts 
    #                SET 
    #                title = %s, content = %s , published = %s 
    #                WHERE id = %s
    #                RETURNING *""", 
    #                (post.title , post.content, post.published ,(str(id) , )))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.PostCreate).filter(models.Post.id == id)  
    post = post_query.first()
    
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with  id : {id} does not exist")
        
    post_query.update(updated_post.dict() , synchronize_session = False)
    
    db.commit()

    return  post_query.first()