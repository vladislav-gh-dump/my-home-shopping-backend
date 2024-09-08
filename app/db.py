from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import TableModel


DB_URL = "sqlite+aiosqlite:///app.db"
engine = create_async_engine(DB_URL, echo=True)
NewSession = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(TableModel.metadata.create_all)


async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(TableModel.metadata.drop_all)
