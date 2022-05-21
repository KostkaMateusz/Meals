from sqlalchemy import create_engine,Column ,ForeignKey ,Integer, String, Float,Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

engine = create_engine("sqlite:///./sql_app.db", echo=True, future=True)


class PresentIngredients(Base):
    __tablename__ = 'present_ingredients'

    id = Column(Integer, primary_key=True)
    name=Column(String)
    
    meal_id =  Column(Integer, ForeignKey('meals.id'))

class MissingIngredients(Base):
    __tablename__ = 'missing_ingredients'

    id = Column(Integer, primary_key=True)
    name=Column(String)
    
    meal_id = Column(Integer, ForeignKey('meals.id'))
    

class Meals(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    hash = Column(String)
    
    name=Column(String)
    picture=Column(String)
    carbs=Column(Float) 
    proteins=Column(Float) 
    calories=Column(Float)

    ingridients = relationship("PresentIngredients")
    
    missing_Ingredients = relationship("MissingIngredients")

    
    

Base.metadata.create_all(engine)

   
Session = sessionmaker(engine)


def test():
    
    with Session() as session:    
        entry_data=['jaja','boczek','salceson']
        hash=sorted(entry_data)
        hash=",".join(hash)

        prezent_list=[]
        for item in entry_data:
            prezent=PresentIngredients(name=item)
            prezent_list.append(prezent)
        
        missing1=MissingIngredients(name='kupa')
        missing2=MissingIngredients(name='dupa')
        
        meal=Meals(hash=hash,name="jajecznica",
        picture="www.google.com",
        carbs=21.34,
        proteins=69, 
        calories=26)

        meal.ingridients=prezent_list

        meal.missing_Ingredients=[missing1]

        meal2=Meals(hash=hash,name="jajecznica z boczkiem",
        picture="www.prypry.com",
        carbs=50.60,
        proteins=70.80, 
        calories=25.25)
        meal2.ingridients=prezent_list
        meal2.missing_Ingredients=[missing2]    
        
        session.add_all(prezent_list)
        session.add(missing1)
        session.add(missing2)
        session.add(meal)
        session.add(meal2)
        session.commit()
    


# test()