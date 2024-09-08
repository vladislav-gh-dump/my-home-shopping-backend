import datetime
from typing import List
from pydantic import BaseModel, Field


class S_ProductBase(BaseModel):
  name: str = Field(min_length=1, max_length=30)
  product_category_id: int | None = None
  
class S_ProductCreate(S_ProductBase):
  pass
  
class S_ProductUpdate(S_ProductBase):
  pass

class S_Product(S_ProductBase):
  id: int
  created_at: datetime
  updated_at: datetime
  
  class Config:
    orm_mode = True


class S_ProductCategoryBase(BaseModel):
  name: str = Field(min_length=1, max_length=30)
  
class S_ProductCategoryCreate(S_ProductCategoryBase):
  pass
  
class S_ProductCategoryUpdate(S_ProductCategoryBase):
  pass

class S_ProductCategory(S_ProductCategoryBase):
  id: int
  created_at: datetime
  updated_at: datetime
  products: List[S_Product] = []
  
  class Config:
    orm_mode = True
