import os
import requests
from dotenv import load_dotenv
from dataclasses import dataclass
from utils import make_meal_propositions,create_html, add_translation,create_file_name

load_dotenv()

@dataclass
class Recipe:
    __slots__ = ['name', 'picture', 'present_ingredients','missing_ingredients','carbs','proteins','calories']
    name:str
    picture:str
    present_ingredients:list[str]
    missing_ingredients:list[str]
    carbs:float 
    proteins:float
    calories:float


def get_recipe_from_API(include_ingredients:list,exclude_ingredients:list):

    
    include_ingredients_str=",".join(include_ingredients)
    exclude_ingredients_str=",".join(exclude_ingredients)

    payload = {"includeIngredients": f"{include_ingredients_str}",
    "excludeIngredients":f"{exclude_ingredients_str}",
    "fillIngredients":True,"addRecipeNutrition":True,
    "number":2,"sort":"min-missing-ingredients"}

    headers = {"x-api-key": os.getenv('APIKEY')}

    resp = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=payload, headers=headers)

    return resp.json()


def make_meals(recipies:list)->list[Recipe]:
    list_of_object=[]
    
    for recipie_info in recipies['results']:

        name=recipie_info["title"]
        picture=recipie_info["image"]
        present_ingredients=[ingridients['name']  for ingridients in recipie_info["usedIngredients"]]
        missing_ingredients=[missed_ingridients['name']  for missed_ingridients in recipie_info["missedIngredients"]]
        
        nutrients={nutriotion['name']:nutriotion['amount'] for  nutriotion in recipie_info["nutrition"]["nutrients"]  if  nutriotion['name'] in ['Carbohydrates', 'Protein', 'Calories']}
        
        carbs=nutrients['Carbohydrates']
        proteins=nutrients['Protein']
        calories=nutrients['Calories']

        recipe=Recipe(name,picture,present_ingredients,missing_ingredients,carbs,proteins,calories)
        
        list_of_object.append(recipe)

    return list_of_object

from database_models import PresentIngredients,Meals,MissingIngredients,Session

def check_database(include):
    
    with Session() as session:
        # hash=sorted(include)
        hash=include
    
        hash=",".join(hash)
        ingredients=session.query(PresentIngredients).filter(PresentIngredients.name==hash).first()
     
        if ingredients==None:
            return None
        else:
            meals=session.query(Meals).filter(Meals.ingridients==ingredients).all()
            return meals
        

def convert_to_Recipe(include,meals:list[Meals])->list[Recipe]:
    for meal in meals:
        recipe=Recipe(name=meal.name,picture=meal.picture,present_ingredients=include,missing_ingredients=,carbs=meal.carbs,proteins=meal.proteins,calories=meal.calories)


def find_food(include:list,exclude:list=None):

    if exclude is None:
        exclude=[]
        exclude.append('plums')

    

        # if ghj is None:
        #     #call Api
        # else:



    # recipies=get_recipe_from_API(include,exclude)
    # meals=make_meals(recipies)

    # translated_meals=add_translation(meals)
    # sugestion=make_meal_propositions(translated_meals)

    # file_name=create_file_name(include)
    
    # create_html(translated_meals,sugestion,file_name)


find_food(['jaja','boczek','salceson'],['eggs'])



