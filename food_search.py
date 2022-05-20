
import requests

from dataclasses import dataclass
from dotenv import load_dotenv
import os
load_dotenv()

@dataclass
class Recipe:
    name:str
    picture:str
    present_ingredients:list[str]
    missing_ingredients:list[str]
    carbs:float 
    proteins:float
    calories:float


def get_recipe_from_API(include_ingredients:list,exclude_ingredients:list=None):
    if exclude_ingredients is None:
        exclude_ingredients=[]
        exclude_ingredients.append('plums')
    
    include_ingredients_str=",".join(include_ingredients)
    exclude_ingredients_str=",".join(exclude_ingredients)

    payload = {"includeIngredients": f"{include_ingredients_str}",
    "excludeIngredients":f"{exclude_ingredients_str}",
    "fillIngredients":True,"addRecipeNutrition":True,
    "number":2,"sort":"min-missing-ingredients"}

    headers = {"x-api-key": os.getenv('APIKEY')}

    resp = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=payload, headers=headers)

    return resp.json()




def filter_data(recipies:list):
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

        rec=Recipe(name,picture,present_ingredients,missing_ingredients,carbs,proteins,calories)
      
        list_of_object.append(rec)

    return list_of_object

recipies=get_recipe_from_API(['tomato,cheese'],['eggs'])
meals=filter_data(recipies)


from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('test.html')
output_from_parsed_template = template.render(items=meals)
print(output_from_parsed_template)

# to save the results
with open("my_new_file.html", "w") as fh:
    fh.write(output_from_parsed_template)





