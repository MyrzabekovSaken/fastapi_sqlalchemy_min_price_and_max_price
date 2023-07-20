from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import service
import models
import dtos
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products", response_model=list[dtos.Product])
def get_products(min_price: int = 0, max_price: int = 1000, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_products(db, min_price, max_price, skip, limit)

@app.get("/products/{product_id}", response_model=dtos.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = service.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=dtos.Product, status_code=201)
def create_product(product: dtos.ProductInput, db: Session = Depends(get_db)):
    return service.create_product(db, product)

@app.put("/products/{product_id}", response_model=dtos.Product)
def update_product(product_id: int, product: dtos.ProductInput, db: Session = Depends(get_db)):
    return service.update_product(db, product_id, product)

@app.delete("/products/{product_id}", response_model=dtos.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return service.delete_product(db, product_id)