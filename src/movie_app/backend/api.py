from fastapi import FastAPI

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get('/')
def root():
    return {'Movie App'}

@app.post('/upload')
def upload_file(file: f):
    return f