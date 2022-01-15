"""
Semantyczny Mashup

pip install sparqlwrapper rdflib owlready2 Flask
"""

from random import seed

from flask import Flask

import get_artist

app = Flask(__name__)


# endpoint zwraca nam losowego twórce dla podanego kraju
@app.route('/artist/<country>')
def get_random_artist(country):
    return get_artist.get_data_about_artist(country)


if __name__ == '__main__':
    seed(1)
    app.run()
