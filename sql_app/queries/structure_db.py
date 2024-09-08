from sql_app.db import engine
from sql_app.models import ORM_Base


async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(ORM_Base.metadata.create_all)


async def delete_tables():
  async with engine.begin() as conn:
    await conn.run_sync(ORM_Base.metadata.drop_all)
