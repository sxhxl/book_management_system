import asyncio
from app.schemas.base import Base, engine

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

if __name__ == "__main__":
    asyncio.run(init())
