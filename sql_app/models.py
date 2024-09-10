from datetime import datetime
from typing import List, Optional
from .db import engine
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
  DeclarativeBase, 
  Mapped, mapped_column,
  relationship
)


class ORM_Base(DeclarativeBase):
  pass


async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(ORM_Base.metadata.create_all)


async def delete_tables():
  async with engine.begin() as conn:
    await conn.run_sync(ORM_Base.metadata.drop_all)


# models

class ORM_ProductCategory(ORM_Base):
  __tablename__ = "product_category"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=func.now())
  updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
  
  products: Mapped[List["ORM_Product"]] = relationship(back_populates="product_category")
                                     

class ORM_Product(ORM_Base):
  __tablename__ = "product"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=func.now())
  updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
  
  product_category_id: Mapped[Optional[int]]         = mapped_column(ForeignKey("product_category.id"))
  product_category:    Mapped["ORM_ProductCategory"] = relationship(back_populates="products") 
