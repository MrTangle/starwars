from starwars.api import get_people, filter_people

from flask import Flask

people = get_people()
nueva_lista = filter_people(people)

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


@app.route("/")
def index():
    return dict(welcome="welcome")


@app.route("/people")
def get_starwars():
    from starwars.api import filter_people
    nueva_lista = filter_people(people)
    return nueva_lista


@app.route("/ord-by-height")
def order_people():
    from starwars.api import order_people_by_height
    return order_people_by_height(nueva_lista)