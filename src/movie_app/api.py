import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, UploadFile, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .db import build_letterboxd_db
from .tmdb import get_request_token, create_session, get_account
# from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
FRONTEND = Path(__file__).parent / "frontend"
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

CALLBACK_URL = os.getenv("CALLBACK_URL")

@app.post('/uploadLetterBoxd')
async def upload_letterboxd_file(file: UploadFile):
    df = pd.read_csv(file.file)
    build_letterboxd_db(df.head(5), "test.db")
    return RedirectResponse("/", status_code=303)

@app.get('/getToken')
async def get_tmdb_token() -> str:
    token = get_request_token()
    return RedirectResponse(f"https://www.themoviedb.org/authenticate/{token}?redirect_to={CALLBACK_URL}")

@app.get('/tmdbCallback')
async def tmdb_callback(request_token: str, approved: bool = False):
    if not approved:
        return RedirectResponse("/?error=tmdbdenied", status_code=303)
    session_id = create_session(request_token)

    response = RedirectResponse("/", status_code=303)
    response.set_cookie("tmdb_session_id", session_id, httponly=True, samesite="lax")
    return response

@app.get('/syncTMDB')
async def sync_tmdb_account(request: Request):
    session_id = request.cookies.get("tmdb_session_id")
    print(session_id)
    get_account(session_id)
    return RedirectResponse("/", status_code=303)



app.mount("/", StaticFiles(directory=FRONTEND, html=True), name = "Frontend")