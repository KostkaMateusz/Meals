from sqlalchemy import Column ,ForeignKey ,Integer, String, Float,Table
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


association_table = Table('association', Base.metadata,
    Column('left_id', ForeignKey('meals.id'), primary_key=True),
    Column('right_id', ForeignKey('present_ingredients.id'), primary_key=True)
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



from sqlalchemy import create_engine
engine = create_engine("sqlite:///./sql_app.db", echo=True, future=True)

Base.metadata.create_all(engine)


from sqlalchemy.orm import Session


with Session(engine) as session:
    
    meal=Meals(name="jajecznica",
    picture="www.google.com",
    carbs=21.34,
    proteins=69, 
    calories=26)
    

    pres_ing=PresentIngredients(name="pomidory")

    meal.ingridients=[pres_ing]
    pres_ing.meals=[meal]

    session.add(meal)
    session.add(pres_ing)

    session.commit()