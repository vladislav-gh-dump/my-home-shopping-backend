from contextlib import asynccontextmanager
from fastapi import FastAPI

from sql_app.queries.structure_db import create_tables, delete_tables

from routers import (
  products_router,
  product_categories_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   
   yield
   
   # for dev
   await delete_tables()
   print("База очищена")


app = FastAPI(lifespan=lifespan)
app.include_router(products_router)
app.include_router(product_categories_router)
