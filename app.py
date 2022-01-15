"""
Semantyczny Mashup

pip install sparqlwrapper rdflib owlready2 Flask flask-cors
"""

from random import seed

from flask import Flask
from flask_cors import CORS

import get_artist

app = Flask(__name__)
CORS(app)


# endpoint zwraca nam losowego twórce dla podanego kraju
# TODO: przrobić nazwe kraju na kod iso
@app.route('/artist/<country>')
def get_random_artist(country):
    return get_artist.get_data_about_artist(country)


if __name__ == '__main__':
    seed(1)
    app.run()
