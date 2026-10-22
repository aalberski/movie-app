import json
import requests
from dotenv import load_dotenv
import os
from rich import print
from models import Movie

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

def search_movie(title, year) -> Movie | None:
    try:
        response = requests.get("https://api.themoviedb.org/3/search/movie", params = {"api_key": api_key, "query": title, "year": year}).json()['results']
        filtered_response = [r for r in response if r['title'] == title and r['release_date'].startswith(str(year))]
        movie_response = filtered_response[0]
        return Movie(id = movie_response['id'], title = movie_response['title'], backdrop_path = movie_response['backdrop_path'], poster_path = movie_response['poster_path'], vote_average = movie_response['vote_average'])
    except:
        return None

def similar_movie(id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}/recommendations", params = {"api_key": api_key}, timeout=10)
    return response.json()['results']