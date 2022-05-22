from database_models import PresentIngredientsDB, MealDB, MissingIngredientsDB, Session
from data_model import MealDataClass


def get_custom_hash(include: list[str], exclude: list[str]) -> str:
    """Create custom hash for input"""
    hash1 = "".join(sorted(include))

    hash2 = "".join(sorted(exclude))

    hash = hash1 + "-" + hash2

    hash = hash.lower()

    return hash


def convert_MealDB_to_MealDataClass(meals: list[MealDB]) -> list[MealDataClass]:
    list_of_meals = []
    for meal in meals:
        prezent = [ing.name for ing in meal.ingridients]
        missing = [ing.name for ing in meal.missing_Ingredients]
        recipe = MealDataClass(meal.name, meal.picture, prezent, missing, meal.carbs, meal.proteins, meal.calories)
        list_of_meals.append(recipe)
    return list_of_meals


def check_database(include: list[str], exclude: list[str]):
    with Session() as session:
        hash = get_custom_hash(include, exclude)

        meals = session.query(MealDB).filter(MealDB.hash == hash).all()

        return convert_MealDB_to_MealDataClass(meals)


def save_meals_in_db(include: list[str], exclude: list[str], meals: list[MealDataClass]) -> None:
    with Session() as session:
        hash = get_custom_hash(include, exclude)

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
