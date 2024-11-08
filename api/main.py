from fastapi import FastAPI, Form, Request
from api.routes import recommend
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

template = Jinja2Templates(directory="api/templates")

app.mount("/static", StaticFiles(directory="api/static"), name="static")

app.include_router(recommend.router, prefix="/api")

@app.get("/")
async def root(request: Request):
    return template.TemplateResponse("index.html", {"request": request, "books": []})