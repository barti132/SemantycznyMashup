"""
Semantyczny Mashup

pip install sparqlwrapper rdflib owlready2 Flask flask-cors
"""

from random import seed

from flask import Flask
from flask_cors import CORS
import pycountry

import get_artist

app = Flask(__name__)
CORS(app)

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2


# endpoint zwraca nam losowego twórce dla podanego kraju
@app.route('/artist/<country>')
def get_random_artist(country):
    code = countries.get(country)
    return get_artist.get_data_about_artist(str(code))


# endpoint zwraca nam losowy zespół dla podanego kraju
@app.route('/band/<country>')
def get_random_band(country):
    pass


if __name__ == '__main__':
    seed(1)
    app.run()
