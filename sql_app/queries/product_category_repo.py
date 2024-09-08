from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from sql_app.db import NewSession
from sql_app.models import ORM_ProductCategory
from sql_app.schemas import S_ProductCategory, S_ProductCategoryCreate, S_ProductCategoryUpdate


class ProductCategoryRepo:
    
    @staticmethod
    async def read_all(skip: int = 0, limit: int = 20) -> List[S_ProductCategory]:
      try:
        async with NewSession() as session:
          result = await session.execute(
              select(ORM_ProductCategory)
              .limit(limit)
              .offset(skip)
          )
          return result.scalars().all()
      except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return []

    @staticmethod
    async def read_one(product_category_id: int) -> Optional[S_ProductCategory]:
      try:
        async with NewSession() as session:
          result = await session.execute(
              select(ORM_ProductCategory)
              .where(ORM_ProductCategory.id == product_category_id)
          )
          return result.scalar_one_or_none()
      except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return None

    @staticmethod
    async def create(product_category: S_ProductCategoryCreate) -> Optional[int]:
      try:
        async with NewSession() as session:
          data = product_category.model_dump()
          new_product_category = ORM_ProductCategory(**data)
          session.add(new_product_category)
          await session.flush()
          await session.commit()
          return new_product_category.id
      except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return None

    @staticmethod
    async def update(product_category_id: int, product_category: S_ProductCategoryUpdate) -> Optional[int]:
      try:
        async with NewSession() as session:
          data = product_category.model_dump()
          result = await session.execute(
              update(ORM_ProductCategory)
              .where(ORM_ProductCategory.id == product_category_id)
              .values(**data)
          )
          await session.commit()
          return result.rowcount 
      except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        return None
