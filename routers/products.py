from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from sql_app.queries.product_repo import ProductRepo
from sql_app.schemas import S_Product, S_ProductCreate, S_ProductUpdate


products_router = APIRouter(
  prefix="/products",
  tags=["Товары"]
)


@products_router.get("")
async def get_products(skip: int = 0, limit: int = 20) -> List[S_Product]:
  result = await ProductRepo.read_all(skip, limit)
  return result
  
  
@products_router.get("/{product_id}")
async def get_product_by_id(product_id: int) -> S_Product:
  result = await ProductRepo.read_one(product_id)
  return result


@products_router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(product: S_ProductCreate = Depends()) -> int:
  result = await ProductRepo.create(product)
  if result is None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create product")
  return result


@products_router.put("/{product_id}")
async def update_product(product_id: int, product: S_ProductUpdate = Depends()):
  result = await ProductRepo.update(product_id, product)
  return result