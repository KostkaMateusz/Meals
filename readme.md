# Home Task

All tests was made on machine with python 3.10.4

---

### Main External Libraries:

- Requests
- SQLAlchemy
- Jinja2
- pygoogletranslation

---

### Setup

- download\
  `git clone https://github.com/KostkaMateusz/Meals.git .`

- create virtual enviroment\
  `python -m virtualenv venv`

- activate virtual enviroment\

  - On Windows\
    `.\venv\Scripts\activate`
  - On Linux\
    `source venv/bin/activate`

- run command\
  `pip3 install -r requirements.txt`

- create .env file in project root folder like:\
  `APIKEY=Your_ApiKey_to_spoonacular.com API`

- entry point of app is **find_food** function in a file **food_search.py**\
  `python .\food_search.py find_food `
