from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from sql_app.db import NewSession
from sql_app.models import (
    ORM_ProductCategory,
    ORM_Product
)
from sql_app.schemas import (
    S_ProductCategory, S_ProductCategoryCreate, S_ProductCategoryUpdate,
    S_Product, S_ProductCreate, S_ProductUpdate
)


class ProductCategory:
	
	@staticmethod
	async def read_all(skip: int = 0, limit: int = 20) -> List[S_ProductCategory]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ORM_ProductCategory)
					.options(joinedload(ORM_ProductCategory.products))
					.limit(limit)
					.offset(skip)
				)
				return result.unique().scalars().all()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return []

	@staticmethod
	async def read_one(product_category_id: int) -> Optional[S_ProductCategory]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ORM_ProductCategory)
					.options(joinedload(ORM_ProductCategory.products))
					.where(ORM_ProductCategory.id == product_category_id)
				)
				return result.unique().scalar_one_or_none()
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
			await session.rollback()
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
			await session.rollback()
			return None


class Product:

	@staticmethod
	async def read_all(skip: int = 0, limit: int = 20) -> List[S_Product]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ORM_Product)
					.limit(limit)
					.offset(skip)
				)
				return result.scalars().all()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return []

	@staticmethod
	async def read_one(product_id: int) -> Optional[S_Product]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ORM_Product)
					.where(ORM_Product.id == product_id)
				)
				return result.scalar_one_or_none()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return None

	@staticmethod
	async def create(product: S_ProductCreate) -> Optional[int]:
		try:
			async with NewSession() as session:
				data = product.model_dump()
				new_product = ORM_Product(**data)
				session.add(new_product)
				await session.flush()
				await session.commit()
				return new_product.id
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return None

	@staticmethod
	async def update(product_id: int, product: S_ProductUpdate) -> Optional[int]:
		try:
			async with NewSession() as session:
				data = product.model_dump()
				result = await session.execute(
					update(ORM_Product)
					.where(ORM_Product.id == product_id)
					.values(**data)
				)
				await session.commit()
				return result.rowcount
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return None
