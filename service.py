from sqlalchemy.orm import Session

import models
import dtos

def get_products(db: Session, min_price: int = 0, max_price: int = 1000, skip: int = 0, limit: int = 100):
    return db.query(models.Product).filter(models.Product.price >= min_price, models.Product.price <= max_price).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: dtos.ProductInput):
    db_product = models.Product(title=product.title, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: dtos.ProductInput):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db_product.title = product.title
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product