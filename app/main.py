#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os
import mysql
import mysql.connector
from mysql.connector import Error
from fastapi.middleware.cors import CORSMiddleware

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "ds2022"
DBPASS = os.getenv('DBPASS')
DB = "qxm6fm"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ['*'],
    allow_methods= ['*'],
    allow_headers= ['*'],
)
@app.get("/")
def zone_apex():
    return {"Hello": "Stranger!"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
            return(json_data)
    except Error as e:
        print("MySQL Error: ", str(e))
        return {"Error": "MySQL Error: " + str(e)}

@api.get('/songs')
def get_songs():
    query = """
    SELECT 
        songs.title AS title,
        songs.album AS album,
        songs.artist AS artist,
        songs.year AS year,
        CONCAT('http://qxm6fm-dp1-spotify.s3-website-us-east-1.amazonaws.com', songs.file) AS file,
        CONCAT('http://qxm6fm-dp1-spotify.s3-website-us-east-1.amazonaws.com', songs.image) AS image,
        genres.genre AS genre
    FROM 
        songs
    JOIN 
        genres ON songs.genre = genres.genreid
    ORDER BY 
        songs.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
