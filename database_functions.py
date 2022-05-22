from database_models import PresentIngredientsDB, MealDB, MissingIngredientsDB
from data_model import MealDataClass
from sqlalchemy.orm import Session


def get_custom_hash(include: list[str], exclude: list[str]) -> str:
    """Create custom hash for input"""
    hash1 = "".join(sorted(include))
    hash2 = "".join(sorted(exclude))

    hash = hash1 + "-" + hash2
    hash = hash.lower()

    return hash


def convert_MealDB_to_MealDataClass(meals: list[MealDB]) -> list[MealDataClass]:
    """Convetr list of MealDB to list of MealDataClass"""
    list_of_meals = []
    for meal in meals:
        # meal.indgridients is list[PresentIngredientsDB]
        # meal.missing_Ingredients is list[MissingIngredientsDB]
        # get only name atribute from PresentIngredientsDB and MissingIngredientsDB objects
        prezent = [ing.name for ing in meal.ingridients]
        missing = [ing.name for ing in meal.missing_Ingredients]

        recipe = MealDataClass(meal.name, meal.picture, prezent, missing, meal.carbs, meal.proteins, meal.calories)

        list_of_meals.append(recipe)

    return list_of_meals


def get_meals_from_DB(hash: str, session: Session) -> list[MealDataClass]:
    """check database for meals with given hash and if finded convert database information to MealDataClass"""

    meals = session.query(MealDB).filter(MealDB.hash == hash).all()

    return convert_MealDB_to_MealDataClass(meals)


def save_meals_in_db(hash: str, meals: list[MealDataClass], session: Session) -> None:
    """Saves data from MealDataClass to a right table in DataBase"""
    for meal in meals:

        present_ingredients_list = [PresentIngredientsDB(name=name) for name in meal.present_ingredients]
        missing_ingredients_list = [MissingIngredientsDB(name=name) for name in meal.missing_ingredients]

        session.add_all(present_ingredients_list)
        session.add_all(missing_ingredients_list)

        meal = MealDB(hash=hash, name=meal.name, picture=meal.picture, carbs=meal.carbs, proteins=meal.proteins, calories=meal.calories)

        meal.ingridients = present_ingredients_list
        meal.missing_Ingredients = missing_ingredients_list

        session.add(meal)

    session.commit()
