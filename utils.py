import re
from jinja2 import Environment, FileSystemLoader
from pygoogletranslation import Translator
from model import MealDataClass
import threading


def make_meal_propositions(meals: list[MealDataClass]) -> dict:
    """Take object with min carbon and object with max protein from list of Recipe objects"""
    # minimal carbon porposition
    min_carbon = min(meals, key=lambda x: x.carbs)
    # max protein porposition
    max_proteins = max(meals, key=lambda x: x.proteins)

    return {"min_carbon": min_carbon.name, "max_proteins": max_proteins.name}


def create_html(meals_data: list[MealDataClass], sugestions: dict, file_name: str = "output_html") -> None:
    """Create a html file from templete if it does not exist or truncates the file if it exists"""

    # Load and render template with data
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("template.html")
    output_from_parsed_template = template.render(items=meals_data, sugestions=sugestions)

    # save the results
    with open(f"{file_name}.html", "w", encoding="utf-8") as fh:
        fh.write(output_from_parsed_template)


translator = Translator()


def translate(translated_words: list, index: int, word: str) -> str:
    """Translate word to polish language"""

    tr = translator.translate(word, src="en", dest="pl")

    translated_words[index] = tr.text
    return


def translation_menager(words: list[str]):
    # create spaces fo translated words
    translated_words = [""] * len(words)
    threads_list = []

    for index, word in enumerate(words):
        x = threading.Thread(target=translate, args=(translated_words, index, word))
        x.start()
        threads_list.append(x)

    # wait until all threads finish
    for thread in threads_list:
        thread.join()

    return translated_words


def add_translation(meals: list[MealDataClass]) -> list[MealDataClass]:
    """Add translation to a Recipe datacalass to missing_ingredients field"""
    for meal in meals:
        translated_missing_ingredients = ",".join(translation_menager(meal.missing_ingredients))
        meal.missing_ingredients.append(f"PL({translated_missing_ingredients})")

    return meals


def create_file_name(names: list[str]) -> str:
    """Normalize file name from list of strings with given regex [a-zA-Z0-9_-]+"""
    expresion = re.compile("[a-zA-Z0-9_-]+")
    checket_string = []
    for name in names:
        matches = expresion.findall(name)

        checket_string.append("".join(matches))

    file_name = "_".join(checket_string)
    file_name = file_name.strip()
    file_name = file_name.lower()

    return file_name
