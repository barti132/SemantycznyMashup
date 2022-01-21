import json
from random import randint

import SPARQLWrapper

import spotify


def get_data_about_band(country_id):
    name = ""
    spotify_id = ""
    description = ""
    img = set()
    genre = set()
    country = set()
    website = set()
    while True:
        band = choose_band(country_id)
        wd_results = get_data_from_wikidata(band)

        has_web = 'website' in wd_results["results"]

        for result in wd_results["results"]["bindings"]:
            name = result["name"]["value"]
            spotify_id = result["spotify"]["value"]
            description = result["description"]["value"]
            img.add(result["img"]["value"])
            genre.add(result["genreName"]["value"])
            country.add(result["countryName"]["value"])
            if has_web:
                website.add(result["website"]["value"])
        if spotify_id != "":
            audio = spotify.get_data_about_id(spotify_id)
            if audio is not None:
                break

    json_out = {
        "name": name,
        "description": description,
        "spotify": spotify_id,
        "image": list(img),
        "genre": list(genre),
        "country": list(country),
        "website": list(website),
        "audio": audio
    }
    return json.dumps(json_out, ensure_ascii=False).encode('utf8')


def choose_band(country):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>

    SELECT DISTINCT ?name ?spotify ?image ?followers WHERE{
      {
        ?entity wdt:P31 wd:Q215380 ;
           rdfs:label ?name ;
           wdt:P495 ?country ;
           wdt:P1902 ?spotify ;
           wdt:P8687 ?followers ;
           wdt:P18 ?image .
        ?country wdt:P297 \"""" + country + """\" .
      }
      UNION
      {
        ?entity wdt:P31 wd:Q215380 ;
           rdfs:label ?name ;
           wdt:P495 ?country ;
           wdt:P1902 ?spotify ;
           wdt:P18 ?image .
        ?country wdt:P297 \"""" + country + """\" .
      }
      FILTER (lang(?name) = 'en')
    }
    ORDER BY DESC(?followers)
    LIMIT 10
    """

    wikidata.setQuery(query)
    wikidata.setReturnFormat(SPARQLWrapper.JSON)
    wd_results = wikidata.query().convert()

    bands = []
    for result in wd_results["results"]["bindings"]:
        bands.append(result["name"]["value"])

    if len(bands) == 0:
        return ""
    band = bands[randint(0, len(bands) - 1)]
    return band


def get_data_from_wikidata(band):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX schema: <http://schema.org/>
    SELECT DISTINCT ?name ?spotify ?img ?genreName ?countryName ?website ?description
    WHERE {
      {
        ?entity wdt:P31 wd:Q215380;
          rdfs:label \"""" + band + """\"@en;
          rdfs:label ?name;
          wdt:P495 ?country;
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
        ?entity wdt:P31 wd:Q215380;
          rdfs:label \"""" + band + """\"@en;
          rdfs:label ?name;
          wdt:P495 ?country;
          wdt:P1902 ?spotify;
          wdt:P136 ?genre;
          wdt:P18 ?img;
          schema:description ?description .
        ?genre rdfs:label ?genreName.
        ?country rdfs:label ?countryName.
        OPTIONAL { ?entity wdt:P856 ?website }
      }
      FILTER (lang(?genreName) = 'en')
      FILTER (lang(?countryName) = 'en')
      FILTER (lang(?description) = 'en')
    }
    LIMIT 1
    """

    wikidata.setQuery(query)
    wikidata.setReturnFormat(SPARQLWrapper.JSON)
    wd_results = wikidata.query().convert()
    return wd_results
