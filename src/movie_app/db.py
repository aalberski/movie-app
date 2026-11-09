# Sqlite3 database to store list of movies

import sqlite3
import json
import pandas as pd
from .tmdb import search_movie
from .models import Movie

# df = pd.read_csv('watched.csv')

# conn = sqlite3.connect('movie_ranker.db')

# conn.execute(
#     """
#     CREATE TABLE IF NOT EXISTS movies(
#         tmdb_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT NOT NULL,
#         data TEXT NOT NULL,
#         elo_rating REAL DEFAULT 1500
#     )
#     """
# )

def build_db(datafile, database):
    conn = sqlite3.connect(database)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS movies(
            tmdb_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            data TEXT NOT NULL,
            elo_rating REAL DEFAULT 1500
        )
        """
    )
    for index, row in datafile.iterrows():
        try:
            save_movie(conn, search_movie(row['Name'], row['Year']))
        except:
            print('Failed to save',  row['Name'])
    conn.commit()
    conn.close()

def save_movie(conn, movie: Movie) -> None:
    conn.execute(
        """
            INSERT OR REPLACE INTO movies(tmdb_id, title, data) VALUES (?,?,?)
        """,
        (movie.id, movie.title, movie.model_dump_json())
    )
    conn.commit()

# build_db(df.head(5))
# build_db(df)