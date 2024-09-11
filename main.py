from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sql_app.models import create_tables, delete_tables

from routers import (
  product_router,
  product_category_router
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(product_category_router)
