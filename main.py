import json

from flask import render_template, Flask
from utils import get_by_title, get_title

app = Flask(__name__)


@app.get("/movie/<title>")
def view_title(title):
    result = get_by_title(title)
    return app.response_class(response=json.dumps(result, ensure_ascii=False, indent=4), status=200,
                              mimetype="application/json")


@app.get("/movie/<int:year1>/to/<year2>")
def get_by_date(year1, year2):
    sql = f"""SELECT title, release_year from netflix
              WHERE release_year between {year1} and {year2}
              limit 100"""
    result = get_title(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))
    return app.response_class(response=json.dumps(tmp, ensure_ascii=False, indent=4), status=200,
                              mimetype="application/json")


@app.get("/rating/<rating>")
def get_by_rating(rating):
    my_dict = {
        "children": ("G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f"""select title, rating, discription from netflix
              where rating in {my_dict.get(rating, ("G", "NC-17"))}"""
    result = get_title(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))
    return app.response_class(response=json.dumps(tmp, ensure_ascii=False, indent=4), status=200,
                              mimetype="application/json")


@app.get("/genre/<genre>")
def get_by_genre(genre):
    sql = f"""select title, discription, listed_in from netflix
              where listed_in like '%{str(genre)[1:]}%'"""

    result = get_title(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))
    return app.response_class(response=json.dumps(tmp, ensure_ascii=False, indent=4), status=200,
                              mimetype="application/json")


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
