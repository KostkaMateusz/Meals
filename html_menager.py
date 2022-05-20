from jinja2 import Environment, FileSystemLoader

def create_html(data,sugestion,file_name:str="output_html"):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')
    output_from_parsed_template = template.render(items=data, sugestion=sugestion)

    #save the results
    with open(f"{file_name}.html", "w") as fh:
        fh.write(output_from_parsed_template)

