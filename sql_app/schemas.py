import datetime
from typing import List
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
  name: str = Field(min_length=1, max_length=30)
  product_category_id: int | None = None
  
class ProductCreate(ProductBase):
  pass
  
class ProductUpdate(ProductBase):
  pass

class Product(ProductBase):
  id: int
  created_at: datetime
  updated_at: datetime
  
  class Config:
    orm_mode = True


class ProductCategoryBase(BaseModel):
  name: str = Field(min_length=1, max_length=30)
  
class ProductCategoryCreate(ProductCategoryBase):
  pass
  
class ProductCategoryUpdate(ProductCategoryBase):
  pass

class ProductCategory(ProductCategoryBase):
  id: int
  created_at: datetime
  updated_at: datetime
  products: List[Product] = []
  
  class Config:
    orm_mode = True
