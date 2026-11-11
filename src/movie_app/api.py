import pandas as pd
from pathlib import Path
from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from .db import build_letterboxd_db
# from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
FRONTEND = Path(__file__).parent / "frontend"
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# @app.post('/upload')
# async def upload_file(file: UploadFile):
#     contents = await file.read()
#     print(f"Received {file.filename}: {len(contents)} bytes")
#     return RedirectResponse("/", status_code=303)

@app.post('/uploadLetterBoxd')
async def upload_letterboxd_file(file: UploadFile):
    df = pd.read_csv(file.file)
    build_letterboxd_db(df.head(5), "test.db")
    return RedirectResponse("/", status_code=303)

@app.post('/syncTMDB')
async def sync_tmdb_account():
    return 1

@app.get('/movies')
def get_movies():



app.mount("/", StaticFiles(directory=FRONTEND, html=True), name = "Frontend")