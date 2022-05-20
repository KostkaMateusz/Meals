from sqlalchemy import create_engine,Column ,ForeignKey ,Integer, String, Float,Table
from sqlalchemy.orm import declarative_base, relationship,Session


Base = declarative_base()

engine = create_engine("sqlite:///./sql_app.db", echo=True, future=True)

Base.metadata.create_all(engine)


association_table = Table('association', Base.metadata,
    Column('meal_id', ForeignKey('meals.id'), primary_key=True),
    Column('present_ingredients_id', ForeignKey('present_ingredients.id'), primary_key=True)
)

class Meals(Base):
    __tablename__ = 'meals'

    name=Column(String)
    picture=Column(String)
    carbs=Column(Float) 
    proteins=Column(Float) 
    calories=Column(Float)

    id = Column(Integer, primary_key=True)
    ingridients = relationship("PresentIngredients",secondary=association_table,back_populates='meals')


class PresentIngredients(Base):
    __tablename__ = 'present_ingredients'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    meals = relationship("Meals", secondary=association_table, back_populates='ingridients')

class MissingIngredients(Base):
    __tablename__ = 'missing_ingredients'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    meals = relationship("Meals", secondary=association_table, back_populates='ingridients')


# with Session(engine) as session:
    
#     meal=Meals(name="jajecznica",
#     picture="www.google.com",
#     carbs=21.34,
#     proteins=69, 
#     calories=26)
    
#     mea2=Meals(name="jajecznica z boczkiem",
#     picture="www.prypry.com",
#     carbs=50.60,
#     proteins=70.80, 
#     calories=25.25)
    
#     pres_ing=PresentIngredients(name="pomidory")

#     meal.ingridients=[pres_ing]
#     pres_ing.meals=[meal]

#     session.add(meal)
#     session.add(pres_ing)

#     session.commit()