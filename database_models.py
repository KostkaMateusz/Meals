from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

engine = create_engine("sqlite:///./sql_app.db", echo=True, future=True)


class PresentIngredientsDB(Base):
    __tablename__ = "present_ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    meal_id = Column(Integer, ForeignKey("meals.id"))


class MissingIngredientsDB(Base):
    __tablename__ = "missing_ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    meal_id = Column(Integer, ForeignKey("meals.id"))


class MealDB(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True)
    hash = Column(String)
    name = Column(String)
    picture = Column(String)
    carbs = Column(Float)
    proteins = Column(Float)
    calories = Column(Float)
    ingridients = relationship("PresentIngredientsDB")
    missing_Ingredients = relationship("MissingIngredientsDB")


Base.metadata.create_all(engine)

Session = sessionmaker(engine)
