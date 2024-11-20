
#!/usr/bin/env python3

import os
import mysql.connector
from mysql.connector import Error
=======
import mysql.connector
from mysql.connector import Error
#!/usr/bin/env python3

>>>>>>> 7b69b2d7b4088293a5480f18cec4aad1c05eac5b
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
<<<<<<< HEAD
from fastapi.middleware.cors import CORSMiddleware
=======
import os
from fastapi.middleware.cors import CORSMiddleware 
>>>>>>> 7b69b2d7b4088293a5480f18cec4aad1c05eac5b

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "ds2022"
DBPASS = os.getenv('DBPASS')
DB = "qxm6fm"

try:
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur = db.cursor()
    print("Database connection successful")
except Error as e:
    print(f"Error connecting to database: {e}")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
=======
    allow_origins= ['*'],
    allow_methods= ['*'],
    allow_headers= ['*'],
>>>>>>> 7b69b2d7b4088293a5480f18cec4aad1c05eac5b
)

@app.get("/")
def zone_apex():
    return {"Hello": "Stranger!"}

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except Error as e:
        print(f"MySQL Error: {e}")
        return {"Error": f"MySQL Error: {e}"}

@app.get('/songs')
def get_songs():
    query = """
        SELECT 
            songs.title, 
            songs.album, 
            songs.artist, 
            songs.year, 
            songs.file, 
            genres.genre 
        FROM 
            songs 
        JOIN 
            genres 
        ON 
            songs.genre = genres.genreid 
        ORDER BY 
            songs.id;
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
        print(f"MySQL Error: {e}")
        return {"Error": f"MySQL Error: {e}"}

