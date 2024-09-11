from datetime import datetime
from typing import List, Optional
from .db import engine
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
  DeclarativeBase, 
  Mapped, mapped_column,
  relationship
)


class BaseModel(DeclarativeBase):
  pass


async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(BaseModel.metadata.create_all)


async def delete_tables():
  async with engine.begin() as conn:
    await conn.run_sync(BaseModel.metadata.drop_all)


# models

class ProductCategoryModel(BaseModel):
  __tablename__ = "product_category"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=func.now())
  updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
  
  products: Mapped[List["ProductModel"]] = relationship(back_populates="product_category")
                                     

class ProductModel(BaseModel):
  __tablename__ = "product"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=func.now())
  updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
  
  product_category_id: Mapped[Optional[int]]         = mapped_column(ForeignKey("product_category.id"))
  product_category:    Mapped["ProductCategoryModel"] = relationship(back_populates="products") 
