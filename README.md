### Simple Flask API Sacaar Battles

This project presents a simple REST API with Python and Flask with Sqlite3 database to manage battles: see rating of active characters or killed ones, randomly choose characters to fight, kill character.

#### How to use

1. Clone this project
2. run ```pip install pipenv```
3. run ```pipenv install```
4. run ```python app.py```

#### API request examples:
To access the data, open the browser and access the API as the examples below.

Get rating of characters:

``` http://127.0.0.1:5000/characters```

Get list of killed characters:

```http://127.0.0.1:5000/killed```

Randomly pair characters:

```http://127.0.0.1:5000/battle```

Kill character:

```http://127.0.0.1:5000/kill/<character id>```
