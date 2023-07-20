from pydantic import BaseModel, Field

class ProductInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    price: int = Field(..., gt=0)

class Product(ProductInput):
    id: int
    title: str
    price: int

    class Config:
        orm_mode = True