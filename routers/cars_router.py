from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from database import get_db
from models import Car

from typing import Optional, List
from fastapi import Query
from schemas import CarOut



router = APIRouter()



@router.get("/random", response_model=CarOut)
def get_random_car(db: Session = Depends(get_db)):
    car = db.query(Car).order_by(func.random()).first()
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return car




@router.get("/filter", response_model=List[CarOut])
def filter_cars_by_price(
        max_price: Optional[float] = Query(None, description="Максимальная цена"),
        min_price: Optional[float] = Query(None, description="Минимальная цена"),
        db: Session = Depends(get_db)
):
    query = db.query(Car)

    if max_price is not None:
        query = query.filter(Car.price <= max_price)
    if min_price is not None:
        query = query.filter(Car.price >= min_price)

    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="Машины не найдены")
    return results


@router.get("/by_year", response_model=List[CarOut])
async def get_cars_by_year(
    year: int = Query(..., description="Год выпуска"),
    db: Session = Depends(get_db)
):
    cars = db.query(Car).filter(Car.year == year).all()
    if not cars:
        raise HTTPException(status_code=404, detail="Машины с таким годом выпуска не найдены")
    return cars



@router.post("/cars{car_id}/like", response_model=List[CarOut])
def like_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")

    car.likes += 1
    db.commit()
    db.refresh(car)

    return {"message": "Вы лайкнули машину", "likes": car.likes}

