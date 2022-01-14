"""
Semantyczny Mashup

pip install sparqlwrapper rdflib owlready2 Flask
"""

from flask import Flask
import SPARQLWrapper

app = Flask(__name__)


@app.route('/artist/<country>')
def get_random_artist(country):
    get_data_from_wikidata(country)
    return country


def get_data_from_wikidata(country):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")

    query = """
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>

    SELECT DISTINCT ?name ?spotify 
    WHERE{
        ?entity wdt:P106 wd:Q855091 ;
            wdt:P27 ?country ;
            wdt:P1559 ?name ;
            wdt:P1902 ?spotify .
        ?country wdt:P1448 "Canada"@en .
    }
    ORDER BY RAND()
    LIMIT 1
    """

    wikidata.setQuery(query)
    wikidata.setReturnFormat(SPARQLWrapper.JSON)
    wd_results = wikidata.query().convert()
    print(wd_results)


if __name__ == '__main__':
    app.run()
