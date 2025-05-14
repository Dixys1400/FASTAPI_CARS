from sqlalchemy import Column, Integer, String, Float
from database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String)
    year = Column(Integer)
    price = Column(Float)
    horsepower = Column(Integer)
    description = Column(String, nullable=True)
    likes = Column(Integer, default=0)





