import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api import api_router
from api.services import update_weathers
from core.db_settings import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    asyncio.create_task(update_weathers())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('script:app', reload=True)
