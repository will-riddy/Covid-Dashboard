##
Requirements Python >= 3.8
## Required Packages
flask
ukcovid-19
datetime
pytest
## Running the program
Run the `__init__.py` file in the server directory
## Config and api_key files
Please replace the api key with an api key from https://newsapi.org
The search terms for the news api must have a space inbetween each term
## Project Tree
```
│   api_key.json
│   config.json
│   LICENSE
│   README.md
│
└───server
    │   sys.log
    │   website.py
    │   __init__.py
    │
    ├───api
    │   │   covid_data_handler.py
    │   │   covid_news_handling.py
    │   │   __init__.py
    │   │
    │   ├───tests
    │   │       test_covid_data_handler.py
    │   │       test_covid_news_handling.py
    │   │       __init__.py
    │   │
    │   └───__pycache__
    │           covid_data_handler.cpython-39.pyc
    │           covid_news_handling.cpython-39.pyc
    │           __init__.cpython-39.pyc
    │
    ├───static
    │   └───images
    │           mike.jpg
    │
    └───templates
            index.html
```