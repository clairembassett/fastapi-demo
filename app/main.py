#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json
import os
import mysql.connector
from mysql.connector import Error

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "ds2022"
DBPASS = os.getenv('DBPASS')
DB = "qxm6fm"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

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
        return {"Error": "MySQL Error: " + str(e)}

@app.get('/songs')
def get_songs(): 
    query = """
	SELECT
		songs.title AS title,
		albums.name AS album,
		artists.name AS artist,
		songs.year AS year,
		CONCAT('https://s3.amazonaws.com/yourbucket/', songs.file) AS file,
		CONCAT('https://s3.amazonaws.com/yourbucket/', songs.image) AS image,
		genres.name AS genre
	FROM songs
	JOIN albums on songs.albumid = albums.albumid
	JOIN artists ON albums.artistid = artists.artistid
	JOIN genres ON songs.genre = genres.genreid
	ORDER BY songs.title;
"""
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
