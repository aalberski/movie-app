import sqlite3
import json
import pandas as pd
from tmdb import search_movie

df = pd.read_csv('watched.csv')

def build_db(datafile, database):
    conn = sqlite3.connect(database)
    
    # Create movies table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elo_rating REAL DEFAULT 1500,
            comparisons_count INTEGER DEFAULT 0,
            adult BOOLEAN,
            backdrop_path TEXT,
            genre_ids TEXT,
            tmdb_id INTEGER UNIQUE,
            title TEXT NOT NULL,
            original_language TEXT,
            original_title TEXT,
            overview TEXT,
            popularity REAL,
            poster_path TEXT,
            release_date TEXT,
            softcore BOOLEAN,
            video BOOLEAN,
            vote_average REAL,
            vote_count INTEGER
        )
        """
    )

    # Create comparisons table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS comparisons(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_a_id INTEGER NOT NULL,
            movie_b_id INTEGER NOT NULL,
            winner_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    for index, row in datafile.iterrows():
        try:
            movie_response = search_movie(row['Name'], row['Year'])
            # print(movie_response['title'])
            conn.execute(
                """
                    INSERT INTO movies(adult, backdrop_path, genre_ids, tmdb_id, title, original_language, original_title, overview, popularity, poster_path, release_date, softcore, video, vote_average, vote_count)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (movie_response['adult'], movie_response['backdrop_path'], json.dumps(movie_response['genre_ids']), movie_response['id'], movie_response['title'], movie_response['original_language'], movie_response['original_title'], movie_response['overview'], movie_response['popularity'], movie_response['poster_path'], movie_response['release_date'], movie_response['softcore'], movie_response['video'], movie_response['vote_average'], movie_response['vote_count'])
            )
        except:
            print('Failed to find ',  row['Name'])

    conn.commit()
    conn.close()

build_db(df.head(50), 'movie_ranker.db')