from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from sql_app.repos.product_category import ProductCategoryRepo
from sql_app.schemas import (
    ProductCategorySchema, 
    ProductCategoryCreateSchema, 
    ProductCategoryUpdateSchema,
    ProductSchema, 
    ReadAllSchema
)


router = APIRouter(
	prefix="/product-categories",
	tags=["Категории товаров"]
)


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ProductCategorySchema])
async def get_product_categories(query_params: ReadAllSchema = Depends()):
	return await ProductCategoryRepo.read_all(query_params)


@router.get("/{product_category_id}", status_code=status.HTTP_200_OK, response_model=ProductCategorySchema)
async def get_product_category(product_category_id: int):
	result = await ProductCategoryRepo.read_one(product_category_id)
	if result is not None:
		return result
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested product category was not found")


@router.get("/{product_category_id}/products", status_code=status.HTTP_200_OK, response_model=List[ProductSchema])
async def get_products(product_category_id: int):
	return await ProductCategoryRepo.read_products(product_category_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product_category(body: ProductCategoryCreateSchema):
	result = await ProductCategoryRepo.create(body)
	if result is not None:
		return {
			"status": "ok",
			"message": "Product category was successfully created"
		}
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create product category")


@router.put("/{product_category_id}", status_code=status.HTTP_200_OK)
async def update_product_category(product_category_id: int, body: ProductCategoryUpdateSchema):
	result = await ProductCategoryRepo.update(product_category_id, body)
	if result is not None:
		return {
			"status": "ok",
			"message": "Product category was successfully updated"
		}
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update product category")
