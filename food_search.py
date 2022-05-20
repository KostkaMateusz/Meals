from urllib import response
import requests

from dataclasses import dataclass

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

    headers = {"x-api-key": "2c66451ac84b4553a55639e96711eb74"}

    response = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=payload, headers=headers)

    print(response.url)

    return response.json()






