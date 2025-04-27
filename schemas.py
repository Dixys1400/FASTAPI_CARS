from pydantic import BaseModel
from typing import Optional


class CarBase(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    price: float
    horsepower: int
    description: Optional[str] = None



class CarCreate(CarBase):
    pass

class CarOut(CarBase):
    id: int

    class Config:
        from_attributes = True