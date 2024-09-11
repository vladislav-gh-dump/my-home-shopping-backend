from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from sql_app.db import NewSession
from sql_app.models import ProductModel
from sql_app.schemas import (
    ProductSchema, 
    ProductCreateSchema, 
    ProductUpdateSchema, 
    ReadAllSchema
)


class ProductRepo:

	@staticmethod
	async def read_all(query_params: ReadAllSchema) -> List[ProductSchema]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ProductModel)
					.limit(query_params.limit)
					.offset(query_params.skip)
				)
				return result.scalars().all()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return []

	@staticmethod
	async def read_one(product_id: int) -> Optional[ProductSchema]:
		try:
			async with NewSession() as session:
				result = await session.execute(
					select(ProductModel)
					.where(ProductModel.id == product_id)
				)
				return result.scalar_one_or_none()
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return None

	@staticmethod
	async def create(body: ProductCreateSchema) -> Optional[int]:
		try:
			async with NewSession() as session:
				data = body.model_dump()
				new_product = ProductModel(**data)
				session.add(new_product)
				await session.flush()
				await session.commit()
				return new_product.id
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return None

	@staticmethod
	async def update(product_id: int, body: ProductUpdateSchema) -> Optional[int]:
		try:
			async with NewSession() as session:
				data = body.model_dump()
				result = await session.execute(
					update(ProductModel)
					.where(ProductModel.id == product_id)
					.values(**data)
				)
				await session.commit()
				return result.rowcount
		except SQLAlchemyError as e:
			print(f"Database error occurred: {e}")
			return None
