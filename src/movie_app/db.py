# Sqlite3 database to store list of movies

import sqlite3
import json
from tmdb import search_movie, get_user_list
from models import Movie

def build_letterboxd_db(datafile, database):
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
        except Exception as e:
            print(f'Failed to save {row['Name']} {e}')
    conn.commit()
    conn.close()

def build_tmdb_db(account_id, database):
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
    tmdb_movies = get_user_list(account_id)

    for movie in tmdb_movies:
        save_movie(conn, movie)
    
    print("All Done")

def save_movie(conn: sqlite3.Connection, movie: Movie) -> None:
    conn.execute(
        """
            INSERT OR REPLACE INTO movies(tmdb_id, title, data) VALUES (?,?,?)
        """,
        (movie.id, movie.title, movie.model_dump_json())
    )
    conn.commit()



def get_movies(conn: sqlite3.Connection):
    return("test")

build_tmdb_db(24112422, "test2.db")

