"""
Semantyczny Mashup

pip install sparqlwrapper rdflib owlready2 Flask
"""
from random import seed, randint

from flask import Flask
import SPARQLWrapper

app = Flask(__name__)


@app.route('/artist/<country>')
def get_random_artist(country):
    get_data_from_wikidata(country)
    return country


def choose_artist(country):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        SELECT DISTINCT ?name
        WHERE{
            {
                ?entity wdt:P106 wd:Q639669;
                    wdt:P1559 ?name ;
                    wdt:P1902 ?spotify ;
                    wdt:P27 ?country .
                ?country rdfs:label \"""" + country + """\"@en .
            }
            UNION{
                ?entity wdt:P106 wd:Q177220;
                    wdt:P1559 ?name ;
                    wdt:P1902 ?spotify ;
                    wdt:P27 ?country .
                ?country rdfs:label \"""" + country + """\"@en .
            }
        }
        ORDER BY RAND()
        LIMIT 10
        """

    wikidata.setQuery(query)
    wikidata.setReturnFormat(SPARQLWrapper.JSON)
    wd_results = wikidata.query().convert()

    artists = []

    for result in wd_results["results"]["bindings"]:
        artists.append(result["name"]["value"])

    return artists[randint(0, len(artists)) - 1]


def get_data_from_wikidata(country):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")

    artist = choose_artist(country)

    query = """
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>

    SELECT DISTINCT ?name ?spotify ?img
    WHERE{
      {
        ?entity wdt:P106 wd:Q639669;
            wdt:P27 ?country ;
            wdt:P1559 ?name ;
            wdt:P1902 ?spotify ;
            wdt:P18 ?img .
        ?country rdfs:label \"""" + country + """\"@en .
        }
    }
    LIMIT 10
    """

    wikidata.setQuery(query)
    wikidata.setReturnFormat(SPARQLWrapper.JSON)
    wd_results = wikidata.query().convert()

    #for result in wd_results["results"]["bindings"]:
    #    print(f'{result["name"]["value"]}' + " " + f'{result["spotify"]["value"]}' + " " + f'{result["img"]["value"]}')



if __name__ == '__main__':
    seed(1)
    app.run()
