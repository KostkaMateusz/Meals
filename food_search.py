import os
import requests
from data_model import Recipe
from dotenv import load_dotenv
from utils import make_meal_propositions, create_html, add_translation, create_file_name
from database_functions import check_database, save_meals_in_db

load_dotenv()


def get_recipe_from_API(include_ingredients: list, exclude_ingredients: list) -> list:
    """Call spooncular api with required ingredients and baned_ingredients"""

    include_ingredients_str = ",".join(include_ingredients)
    exclude_ingredients_str = ",".join(exclude_ingredients)

    payload = {
        "includeIngredients": f"{include_ingredients_str}",
        "excludeIngredients": f"{exclude_ingredients_str}",
        "fillIngredients": True,
        "addRecipeNutrition": True,
        "number": 5,
        "sort": "min-missing-ingredients",
    }

    headers = {"x-api-key": os.getenv("APIKEY")}

    resp = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=payload, headers=headers)

    return resp.json()


def make_meals(recipies: list) -> list[Recipe]:
    """Filtr response from spoonacular and create dataclass Recipe from needed information"""
    list_of_object = []

    for recipie_info in recipies["results"]:

        name = recipie_info["title"]
        picture = recipie_info["image"]
        present_ingredients = [ingridients["name"] for ingridients in recipie_info["usedIngredients"]]
        missing_ingredients = [missed_ingridients["name"] for missed_ingridients in recipie_info["missedIngredients"]]

        nutrients = {nutriotion["name"]: nutriotion["amount"] for nutriotion in recipie_info["nutrition"]["nutrients"] if nutriotion["name"] in ["Carbohydrates", "Protein", "Calories"]}

        carbs = nutrients["Carbohydrates"]
        proteins = nutrients["Protein"]
        calories = nutrients["Calories"]

        recipe = Recipe(name, picture, present_ingredients, missing_ingredients, carbs, proteins, calories)

        list_of_object.append(recipe)

    return list_of_object


def find_food(include: list, exclude: list = None):

    if exclude is None:
        exclude = []
        exclude.append("plums")

    meals = check_database(include)

    if meals is None:

        recipies = get_recipe_from_API(include, exclude)
        meals = make_meals(recipies)
        save_meals_in_db(include, meals)

    translated_meals = add_translation(meals)
    sugestion = make_meal_propositions(translated_meals)

    file_name = create_file_name(include)

    create_html(translated_meals, sugestion, file_name)


find_food(["cheese", "potato"], ["eggs"])
