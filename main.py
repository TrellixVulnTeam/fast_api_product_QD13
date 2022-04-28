#!usr/bin/env python3

from fastapi import FastAPI
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel 
from random import randrange

app = FastAPI()


class Post(BaseModel):
    content : str
    name : str
    published : bool = True
    rating : Optional[int] = None
    
my_post =  [{"title" : "title of post 1" , "content" : "content of post 1" , "id" : 1 },
            {"title" : "title of post 2" , "content" : "content of post 2" , "id" : 2 }
            ]
def find_post(id):
    for p in my_post:
        if p['id'] ==id:
            return p

@app.get("/") 
def read_root():
    return {"hello" : "world"}

@app.get("/post")
def get_post(post : Post):
    return { "data" : f"all {post.content}" }


@app.post("/createposts")
def create_post(post: Post):
    
    post_dict = post.dict()
    post_dict['id'] = randrange(0 , 100000)
    print(post)
    my_post.append(post_dict)
    return {"data" : post_dict}


@app.get("/post/{id}")
def get_post(id : int):
    post = find_post(id) 
    print(id)   
    return {"post_detail" : post}