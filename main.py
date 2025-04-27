from tkinter.font import names

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base
from typing import List, Optional

from models import Car, Base
from schemas import CarOut

from routers import cars_router



app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(cars_router.router, prefix="/cars", tags=["Cars"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/cars", response_model=schemas.CarOut)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car









@app.get("/cars/search", response_model=List[CarOut])
def search_cars_by_brand(
        brand: str = Query(..., description="Название машины"),
        db: Session = Depends(get_db)
):
    cars = db.query(Car).filter(Car.brand.ilike(f"%{brand}%")).all()
    if not cars:
        raise HTTPException(status_code=404, detail="Машины не найдена")
    return cars








@app.get("/cars", response_model=list[schemas.CarOut])
def list_cars(db: Session = Depends(get_db)):
    return db.query(models.Car).all()


@app.get("/cars/{car_id}", response_model=schemas.CarOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return car







@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    db.delete(car)
    db.commit()
    return {"message": "Машина удалена"}


