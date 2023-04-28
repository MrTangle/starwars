import csv
import requests
from flask import Flask
from starwars.api import get_people, ordered_top_ten_by_films, filter_people, order_people_by_height, csv_to_httpbin

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


@app.route("/")
def index():
    return get_people()


@app.route("/people")
def get_starwars():
    people = get_people()
    top10_people = ordered_top_ten_by_films(people)
    filter_list = filter_people(top10_people)
    final_list = order_people_by_height(filter_list)
    response = csv_to_httpbin(final_list)
    return response