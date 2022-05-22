import os
import requests
from dotenv import load_dotenv
from database_models import Session
from model import make_list_of_meals
from database_functions import get_meals_from_DB, save_meals_in_db, get_custom_hash
from utils import make_meal_propositions, create_html, add_translation, create_file_name

load_dotenv()


def get_recipe_from_API(include_ingredients: list[str], exclude_ingredients: list[str]) -> list:
    """Call spooncular api with required ingredients and baned_ingredients"""

    include_ingredients_str = ",".join(include_ingredients)
    exclude_ingredients_str = ",".join(exclude_ingredients)

    payload = {
        "includeIngredients": include_ingredients_str,
        "excludeIngredients": exclude_ingredients_str,
        "fillIngredients": True,
        "addRecipeNutrition": True,
        "number": 5,
        "sort": "min-missing-ingredients",
    }

    # get secret API key from env variable
    headers = {"x-api-key": os.getenv("APIKEY")}

    resp = requests.get("https://api.spoonacular.com/recipes/complexSearch", params=payload, headers=headers)

    return resp.json()


def find_food(include: list[str], exclude: list[str] = None) -> None:

    if exclude is None:
        exclude = ["plums"]

    # create custom identifier for input parameters
    hash = get_custom_hash(include, exclude)

    with Session() as session:
        # get meals for the hash
        meals = get_meals_from_DB(hash, session)
        # if none found len(meals)=0
        if len(meals) == 0:
            # query API for data
            recipies = get_recipe_from_API(include, exclude)

            # filter data and create DataClass objects
            meals = make_list_of_meals(recipies)
            # save new meals in DB
            save_meals_in_db(hash, meals, session)

    # make sugestions based on nutrition
    sugestion = make_meal_propositions(meals)

    # insert translation to a object
    translated_meals = add_translation(meals)

    # create file name from input
    file_name = create_file_name(include)

    # render jinj2 template ans save it
    create_html(translated_meals, sugestion, file_name)


if __name__ == "__main__":
    find_food(["tomato", "cheese", "potato", "milk", "bread"], ["eggs"])
