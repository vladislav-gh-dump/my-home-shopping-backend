from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


class CreateProduct(BaseModel):
  name: str = Field(min_length=4, max_length=30)
  product_category_id: int | None = None
  
class UpdateProduct(CreateProduct):
  pass
  
class CreateProductCategory(BaseModel):
  name: str = Field(min_length=4, max_length=30)


fake_db = {
  "product": [],
  "product_category": []
}

@app.get("/products")
async def read_products(skip: int = 0, limit: int = 100):
  return {
    "data": fake_db["product"][skip:skip+limit]
  }


@app.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product(qp: CreateProduct = Depends()):
  data = {
    "product_id": 0, # id
    "name": qp.name,
    "product_category_id": qp.product_category_id
  }
  fake_db["product"].append(data)
  return data

@app.put("/products/{product_id}")
async def update_product(product_id: int, qp: UpdateProduct = Depends()):
  data = None
  for product in fake_db["product"]:
    if product["product_id"] == product_id:
      product["name"] = qp.name
      product["product_category_id"] = qp.product_category_id    
      data = product
      break
  
  if data is None: 
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product not found"
      )
  
  return data



@app.get("/product_categories")
async def read_product_categories(skip: int = 0, limit: int = 100):
  return {
    "data": fake_db["product_category"][skip:skip+limit]
  }
  
@app.post("/product_categories", status_code=status.HTTP_201_CREATED)
async def create_product(qp: CreateProductCategory = Depends()):
  data = {
    "product_category_id": 0, # id
    "name": qp.name,
  }
  fake_db["product_category"].append(data)
  return data  
