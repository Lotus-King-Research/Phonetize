from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import bophono
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['https://localhost:8080',
           'http://localhost:8080',
           'chrome-extension://ckndbdjoogkmkledkdfclanamfodcbpe',
           'chrome-extension://hmjfaebolfifcpopioomhbpnpjgdcelb']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/phonetize")
async def phonetize_endpoint_get(string: str):
    return phonetize(string)

@app.post("/phonetize")
async def phonetize_endpoint_post(string: str):
    return phonetize(string)

def phonetize(string):
    options = {'aspirateLowTones': False}
    phon = bophono.UnicodeToApi(schema="LKT", options=options)
    phonetic = phon.get_api(string)
    return {"phonetic": phonetic}
