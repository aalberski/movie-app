import json
import requests
from dotenv import load_dotenv
import os
from rich import print
from .models import Movie

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")
api_token = os.getenv("TMDB_ACCESS_TOKEN")

def get_request_token() -> str:
    response = requests.get("https://api.themoviedb.org/3/authentication/token/new", params = {"api_key": api_key})
    return response.json()["request_token"]

def create_session(request_token: str) -> str | None:
    try:
        response = requests.get("https://api.themoviedb.org/3/authentication/session/new",
        params = {"api_key": api_key, "request_token": request_token})
        print(response.json())
        if(response.json()['success'] == False):
            raise Error(response.json()['status_message'])
        return response.json()['session_id']
    except:
        print("error")
        return None

def search_movie(title, year) -> Movie | None:
    try:
        response = requests.get("https://api.themoviedb.org/3/search/movie", params = {"api_key": api_key, "query": title, "year": year}).json()['results']

        filtered_response = [r for r in response if r['title'] == title and r['release_date'].startswith(str(year))]
        movie_response = filtered_response[0]
        return Movie(id = movie_response['id'], title = movie_response['title'], backdrop_path = movie_response['backdrop_path'], poster_path = movie_response['poster_path'], vote_average = movie_response['vote_average'])
    except:
        return None

def get_account(session_id) -> str | None:
    response = requests.get("https://api.themoviedb.org/3/account/", 
    headers = {"accept" : "application/json", "Authorization" : f"Bearer {api_token}"},
    params = {"api_key": api_key, "session_id": session_id})
    print(response.json())
    return response

def get_user_list(account_id: int, session_id: str) -> list[Movie] | None:
    user_movie_list = []
    movies_response = []
    page = 1
    while True:
        response = requests.get(f"https://api.themoviedb.org/3/account/{account_id}/rated/movies", 
        headers = {"accept" : "application/json", "Authorization" : f"Bearer {api_token}"},
        params = {"page": page, "session_id": session_id})
        user_movie_list.extend(response.json()['results'])
        if page >= response.json()['total_pages']:
            break
        page += 1
    for raw_movie in user_movie_list:
        clean_movie = Movie(id = raw_movie['id'], title = raw_movie['title'], backdrop_path = raw_movie['backdrop_path'], poster_path = raw_movie['poster_path'], vote_average = raw_movie['vote_average'])
        movies_response.append(clean_movie)
    return movies_response