from fastapi import FastAPI
from src.routers import router
from src.database import engine, Base

app = FastAPI()

app.include_router(router, prefix="/api", tags=["TodoLists"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "Приложение успешно работает"}