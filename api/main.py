from fastapi import FastAPI
from api.routes import recommend

app = FastAPI()
app.include_router(recommend.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to my Book Recommendation System API."}