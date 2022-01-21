"""
Semantyczny Mashup
Api zwracające dane z wikidata i spotify o twórcach lub zespołach.
Endpointy:
/artist/<country>
zwraca losowego artyste z danego kraju, wraz z przykładowym utworem

/band/<country>
zwraca losowy zespół z danego kraju, wraz z przykładowym utworem

pip install sparqlwrapper Flask flask-cors spotipy
"""

from random import seed

from flask import Flask
from flask_cors import CORS

import get_artist

app = Flask(__name__)
CORS(app)


# endpoint zwraca nam losowego twórce dla podanego kraju
@app.route('/artist/<country>')
def get_random_artist(country):
    return get_artist.get_data_about_artist(country)


# endpoint zwraca nam losowy zespół dla podanego kraju
@app.route('/band/<country>')
def get_random_band(country):
    pass


if __name__ == '__main__':
    seed(1)
    app.run()
