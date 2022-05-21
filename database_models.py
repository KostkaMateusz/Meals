from sqlalchemy import create_engine,Column ,ForeignKey ,Integer, String, Float,Table
from sqlalchemy.orm import declarative_base, relationship,Session


Base = declarative_base()

engine = create_engine("sqlite:///./sql_app.db", echo=True, future=True)


class PresentIngredients(Base):
    __tablename__ = 'present_ingredients'
    
    name=Column(String,primary_key=True)
    
    meal = relationship("Meals", back_populates="ingridients")

class Meals(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    present_ingred = Column(String, ForeignKey('present_ingredients.name'))


    name=Column(String)
    picture=Column(String)
    carbs=Column(Float) 
    proteins=Column(Float) 
    calories=Column(Float)

    ingridients = relationship("PresentIngredients", back_populates="meal")
    
    missing_Ingredients = relationship("MissingIngredients")

    
class MissingIngredients(Base):
    __tablename__ = 'missing_ingredients'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    
    parent_id = Column(Integer, ForeignKey('meals.id'))
    


   

Base.metadata.create_all(engine)

with Session(engine) as session:
    
    ing=['jaja','boczek','salceson']
    ing=",".join(ing)
    pres=PresentIngredients(name=ing)
    missing1=MissingIngredients(name='dupawolowa')
    missing2=MissingIngredients(name='duparozowa')
    
    meal=Meals(name="jajecznica",
    picture="www.google.com",
    carbs=21.34,
    proteins=69, 
    calories=26)
    meal.ingridients=pres

    meal.missing_Ingredients=missing1

    meal2=Meals(name="jajecznica z boczkiem",
    picture="www.prypry.com",
    carbs=50.60,
    proteins=70.80, 
    calories=25.25)
    meal2.ingridients=pres
    meal2.missing_Ingredients=missing2    
    
    session.add(pres)
    session.add(meal)
    session.add(meal2)
    session.commit()
    




    