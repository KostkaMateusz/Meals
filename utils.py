from jinja2 import Environment, FileSystemLoader
from pygoogletranslation import Translator

def make_meal_propositions(meals)->dict:
    # minimal carbon porposition
    min_carbon=min(meals,key=lambda x:x.carbs)
    # max protein porposition
    max_proteins=max(meals,key=lambda x:x.proteins)   

    return {'min_carbon':min_carbon.name,'max_proteins':max_proteins.name}


def create_html(data,sugestion,file_name:str="output_html")->None:
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')
    output_from_parsed_template = template.render(items=data, sugestion=sugestion)

    #save the results
    
    with open(f"{file_name}.html", "w",encoding="utf-8") as fh:
        fh.write(output_from_parsed_template)




translator = Translator()
def translate(words:list[str])->str:
    string_to_translate=",".join(words)
    tr=translator.translate(string_to_translate, dest='pl')
    return tr.text
    
def add_translation(meals):
    for meal in meals:
        translated_missing_ingredients=translate(meal.missing_ingredients)
        meal.missing_ingredients.append(f"pol({translated_missing_ingredients})")
    
    return meals