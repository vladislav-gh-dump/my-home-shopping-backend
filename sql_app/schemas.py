from datetime import datetime 
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


# common schemas

class ConfigSchema(BaseModel):
	class Config: 
		alias_generator = to_camel
		populate_by_name = True
		from_attributes = True

class IdSchema(BaseModel):
    id: int


class ReadAllSchema(BaseModel):
	skip: int = Field(ge=0, default=0)
	limit: int = Field(ge=0, default=20)


class NameSchema(BaseModel):
	name: str = Field(min_length=1, max_length=30)


class AtDatetimeSchema(BaseModel):
	created_at: datetime
	updated_at: datetime


# Schemas for products 

class ProductBaseSchema(NameSchema, BaseModel):
	product_category_id: Optional[int] = None

class ProductCreateSchema(ProductBaseSchema): ...

class ProductUpdateSchema(ProductBaseSchema): ...

class ProductSchema(IdSchema, AtDatetimeSchema, ProductBaseSchema, ConfigSchema): ...


# Schemas for product categories

class ProductCategoryBaseSchema(NameSchema, BaseModel): ...

class ProductCategoryCreateSchema(ProductCategoryBaseSchema): ...

class ProductCategoryUpdateSchema(ProductCategoryBaseSchema): ...

class ProductCategorySchema(IdSchema, AtDatetimeSchema, ProductCategoryBaseSchema, ConfigSchema):
  	products: List[ProductSchema] = []
