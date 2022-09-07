import json
import sqlite3
import flask
from flask import Flask

app = Flask(__name__)


def get_title(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()  # Выполняем запрос с помощью курсора

        return result


def get_by_title(title):
    sql = f"""SELECT title, country, release_year, listed_in as genre, description from netflix
    WHERE title = '{title}'
    order by date_added desc
    limit 1
    """

    result = get_title(sql)

    for item in result:
        return dict(item)


def step_5(name1="Rose McIver", name2="Ben Lamb"):
    sql = f"""select * from netflix
              where `cast` like '%{name1}%' and `cast` like '%{name2}%'"""
    result = get_title(sql)

    tmp = []
    names_dict = {}
    for item in result:
        names = set(dict(item).get("cast").split(", ") - set([name1, name2]))
        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1
    for key, value in names_dict.items():

        if value > 2:
            tmp.append(key)

    return tmp


def step_6(typ, year, genre):
    sql = f"""
            select * from netflix
            where type = '{typ}' and
            release_year = '{year}' and
            listed_in like '%{genre}%'
    """
    result = get_title(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))
    return json.dumps(tmp, ensure_ascii=False, indent=4)
