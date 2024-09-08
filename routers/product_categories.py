from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from sql_app.queries.product_category_repo import ProductCategoryRepo
from sql_app.schemas import S_ProductCategory, S_ProductCategoryCreate, S_ProductCategoryUpdate


product_categories_router = APIRouter(
  prefix="/product-categories",
  tags=["Категории товаров"]
)


@product_categories_router.get("")
async def get_product_categories(skip: int = 0, limit: int = 20) -> List[S_ProductCategory]:
  result = await ProductCategoryRepo.read_all(skip, limit)
  return result
  
  
@product_categories_router.get("/{product_category_id}")
async def get_product_category_by_id(product_category_id: int) -> S_ProductCategory:
  result = await ProductCategoryRepo.read_one(product_category_id)
  return result


@product_categories_router.post("", status_code=status.HTTP_201_CREATED)
async def create_product_category(product_category: S_ProductCategoryCreate = Depends()) -> int:
  result = await ProductCategoryRepo.create(product_category)
  if result is None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create product category")
  return result


@product_categories_router.put("/{product_category_id}")
async def update_product_category(product_category_id: int, product_category: S_ProductCategoryUpdate = Depends()):
  result = await ProductCategoryRepo.update(product_category_id, product_category)
  return result
