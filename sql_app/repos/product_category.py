from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from sql_app.db import NewSession
from sql_app.models import ProductCategoryModel, ProductModel
from sql_app.schemas import (
    ProductCategorySchema, 
    ProductCategoryCreateSchema, 
    ProductCategoryUpdateSchema,
    ProductSchema, 
    ReadAllSchema
)


class ProductCategoryRepo:
	
	@staticmethod
	async def read_all(query_params: ReadAllSchema) -> List[ProductCategorySchema]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ProductCategoryModel)
					.options(joinedload(ProductCategoryModel.products))
					.limit(query_params.limit)
					.offset(query_params.skip)
				)
				return result.unique().scalars().all()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return []

	@staticmethod
	async def read_one(product_category_id: int) -> Optional[ProductCategorySchema]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ProductCategoryModel)
					.options(joinedload(ProductCategoryModel.products))
					.where(ProductCategoryModel.id == product_category_id)
				)
				return result.unique().scalar_one_or_none()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return None

	@staticmethod
	async def read_products(product_category_id: int) -> List[ProductSchema]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ProductModel)
					.where(ProductModel.product_category_id == product_category_id)
				)
				return result.unique().scalars().all()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return []
	
	@staticmethod
	async def create(body: ProductCategoryCreateSchema) -> Optional[int]:
		try:
			async with NewSession() as session:
				data = body.model_dump()
				new_product_category = ProductCategoryModel(**data)
				session.add(new_product_category)
				await session.flush()
				await session.commit()
				return new_product_category.id
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			await session.rollback()
			return None

	@staticmethod
	async def update(product_category_id: int, body: ProductCategoryUpdateSchema) -> Optional[int]:
		try:
			async with NewSession() as session:
				data = body.model_dump()
				result = await session.execute(
					update(ProductCategoryModel)
					.where(ProductCategoryModel.id == product_category_id)
					.values(**data)
				)
				await session.commit()
				return result.rowcount
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			await session.rollback()
			return None
