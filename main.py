import logging
import contextlib

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database import init_models, preload_db, context_get_session
from app.routers import api_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    
    
    async with context_get_session() as db_session:
        await preload_db(db_session=db_session)
    
    yield


logger = logging.getLogger("uvicorn")
app = FastAPI(redoc_url=None, lifespan=lifespan)

app.include_router(api_router)


@app.get("/", include_in_schema=False)
async def redirect_response():
    return RedirectResponse("/docs")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
