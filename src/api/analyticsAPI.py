
# Importing
from fastapi import FastAPI
import sqlite3
import pandas as pd

app = FastAPI()

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(r"/app/sqlite-db.db")
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

@app.get("/players/")
def get_players():
    """Fetch all player stats"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT PERSON_ID, FIRST_NAME, LAST_NAME FROM playerstats", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/players/{player_id}")
def get_player_stats(player_id: int):
    """Fetch stats for a specific player"""
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM playerstats WHERE PERSON_ID = ?", conn, params=[player_id])
    conn.close()
    if df.empty:
        return {"error": "Player not found"}
    return df.to_dict(orient="records")

@app.get("/alldata")
def get_all_data():
    """Fetch all data"""
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT * FROM playerstats", conn)
    conn.close()
    if df.empty:
        return {"error": "Player not found"}
    return df.to_dict(orient="records")

