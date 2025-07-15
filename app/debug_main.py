from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/{full_path:path}")
def read_root(full_path: str):
    return HTMLResponse("<h1>Hello from FastAPI on Netlify!</h1><p>Path: /{}</p>".format(full_path))
