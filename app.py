"""
Semantyczny Mashup

pip install sparqlwrapper rdflib owlready2 Flask
"""
from random import seed, randint
from flask import Flask
import SPARQLWrapper
import json

app = Flask(__name__)

# endpoint zwraca nam losowego twórce dla podanego kraju
@app.route('/artist/<country>')
def get_random_artist(country):
    return get_data_from_wikidata(country)

# wybiera 10 "losowych" twórców i losuje jednego
def choose_artist(country):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        SELECT DISTINCT ?name WHERE{
            {
                ?entity wdt:P106 wd:Q639669;
                    rdfs:label ?name ;
                    wdt:P1902 ?spotify ;
                    wdt:P27 ?country .
                ?country rdfs:label \"""" + country + """\"@en .
            }
            UNION
            {
                ?entity wdt:P106 wd:Q177220;
                    rdfs:label ?name ;
                    wdt:P1902 ?spotify ;
                    wdt:P27 ?country .
                ?country rdfs:label \"""" + country + """\"@en .
            }
            FILTER (lang(?name) = 'en')
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

    print(artists)

    return artists[randint(0, len(artists)) - 1]


# pobranie danych z wikidata o twórcy
def get_data_from_wikidata(country):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")

    artist = choose_artist(country)
    print(artist)

    query = """
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX schema: <http://schema.org/>

    SELECT DISTINCT ?name ?spotify ?img ?genreName ?countryName ?website ?description
    WHERE {
    {
        ?entity wdt:P106 wd:Q639669;
            rdfs:label \"""" + artist + """\"@en;
            wdt:P1559 ?name;
            wdt:P27 ?country;
            wdt:P1902 ?spotify;
            wdt:P136 ?genre;
            wdt:P18 ?img;
            schema:description ?description .
        ?genre rdfs:label ?genreName.
        ?country rdfs:label ?countryName.
        OPTIONAL { ?entity wdt:P856 ?website }
    }
    UNION
    {
        ?entity wdt:P106 wd:Q177220;
            rdfs:label \"""" + artist + """\"@en;
            wdt:P1559 ?name;
            wdt:P27 ?country;
            wdt:P1902 ?spotify;
            wdt:P136 ?genre;
            wdt:P18 ?img;
            schema:description ?description.
        ?genre rdfs:label ?genreName.
        ?country rdfs:label ?countryName.
        OPTIONAL { ?entity wdt:P856 ?website }
    }
    FILTER (lang(?genreName) = 'en')
    FILTER (lang(?countryName) = 'en')
    FILTER (lang(?description) = 'en')
    }
    """

    wikidata.setQuery(query)
    wikidata.setReturnFormat(SPARQLWrapper.JSON)
    wd_results = wikidata.query().convert()

    name = ""
    spotify = ""
    description = ""
    img = set()
    genre = set()
    country = set()
    website = set()

    has_web = 'website' in wd_results["results"]

    for result in wd_results["results"]["bindings"]:
        name = result["name"]["value"]
        spotify = result["spotify"]["value"]
        description = result["description"]["value"]
        img.add(result["img"]["value"])
        genre.add(result["genreName"]["value"])
        country.add(result["countryName"]["value"])
        if has_web:
            website.add(result["website"]["value"])

    json_out = {
        "name": name,
        "description": description,
        "spotify": spotify,
        "image": list(img),
        "genre": list(genre),
        "country": list(country),
        "website": list(website)
    }
    return json.dumps(json_out, ensure_ascii=False).encode('utf8')


if __name__ == '__main__':
    seed(1)
    app.run()
