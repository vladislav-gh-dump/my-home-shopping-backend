from datetime import datetime 
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class S_ConfigBase(BaseModel):
  class Config: 
    alias_generator = to_camel
    populate_by_name = True
    from_attributes = True


# Schemas of product 

class S_ProductBase(BaseModel):
  name: str = Field(min_length=1, max_length=30)
  product_category_id: Optional[int] = None

class S_ProductCreate(S_ProductBase):
  pass

class S_ProductUpdate(S_ProductBase):
  pass

class S_Product(S_ProductBase, S_ConfigBase):
  id: int
  created_at: datetime
  updated_at: datetime


# Schemas of product category

class S_ProductCategoryBase(BaseModel):
  name: str = Field(min_length=1, max_length=30)

class S_ProductCategoryCreate(S_ProductCategoryBase):
  pass

class S_ProductCategoryUpdate(S_ProductCategoryBase):
  pass

class S_ProductCategory(S_ProductCategoryBase, S_ConfigBase):
  id: int
  created_at: datetime
  updated_at: datetime
  products: List[S_Product] = []
