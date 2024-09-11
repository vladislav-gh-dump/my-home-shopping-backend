from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from sql_app.repos.product import ProductRepo
from sql_app.schemas import (
    ProductSchema, 
    ProductCreateSchema, 
    ProductUpdateSchema, 
    ReadAllSchema
)


router = APIRouter(
  prefix="/products",
  tags=["Товары"]
)



@router.get("", status_code=status.HTTP_200_OK, response_model=List[ProductSchema])
async def get_products(query_params: ReadAllSchema = Depends()):
	return await ProductRepo.read_all(query_params)


@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def get_product(product_id: int):
	result = await ProductRepo.read_one(product_id)
	if result is not None:
		return result
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested product was not found")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductCreateSchema):
	result = await ProductRepo.create(body)
	if result is not None:
		return {
			"status": "ok",
			"message": "Product was successfully created"
		}
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create product")


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: int, body: ProductUpdateSchema):
	result = await ProductRepo.update(product_id, body)
	if result is not None:
		return {
			"status": "ok",
			"message": "Product was successfully updated"
		}
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update product")
