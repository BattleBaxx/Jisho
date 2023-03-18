import uvicorn
from fastapi import FastAPI

from src.core.config import Config
from src.server.routers.search import search_router

config = Config.get_config()

app = FastAPI(title=config["APP_TITLE"])

app.include_router(
    search_router,
    prefix="/search/v1",
    tags=["Search API V1"]
)

if __name__ == "__main__":
    uvicorn.run(app, host=config["SERVER_HOST"], port=config["SERVER_PORT"])
