from database_models import PresentIngredients, Meals, MissingIngredients, Session
from data_model import Recipe


def convert_to_Recipe(meals: list[Meals]) -> list[Recipe]:
    list_of_meals = []
    for meal in meals:
        prezent = [ing.name for ing in meal.ingridients]
        missing = [ing.name for ing in meal.missing_Ingredients]
        recipe = Recipe(meal.name, meal.picture, prezent, missing, meal.carbs, meal.proteins, meal.calories)
        list_of_meals.append(recipe)
    return list_of_meals


def check_database(include):
    with Session() as session:
        hash = sorted(include)
        hash = ",".join(hash)

        meals = session.query(Meals).filter(Meals.hash == hash).all()

        if meals:
            return convert_to_Recipe(meals)
        else:
            return None


def save_meals_in_db(include, meals: list[Recipe]) -> None:
    with Session() as session:
        hash = sorted(include)
        hash = ",".join(hash)

        for meal in meals:
            present_ingredients_list = [PresentIngredients(name=name) for name in meal.present_ingredients]
            missing_ingredients_list = [MissingIngredients(name=name) for name in meal.missing_ingredients]

            session.add_all(present_ingredients_list)
            session.add_all(missing_ingredients_list)

            meal = Meals(hash=hash, name=meal.name, picture=meal.picture, carbs=meal.carbs, proteins=meal.proteins, calories=meal.calories)

            meal.ingridients = present_ingredients_list
            meal.missing_Ingredients = missing_ingredients_list

            session.add(meal)

        session.commit()
