from .db import engine, NewSession
from .models import TableModel, Product, ProductCategory


async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(TableModel.metadata.create_all)


async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(TableModel.metadata.drop_all)