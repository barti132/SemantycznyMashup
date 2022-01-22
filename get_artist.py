import json
from random import randint

import SPARQLWrapper

import spotify


# pobiera dane z wikidata i spotify i łączy je w json
def get_data_about_artist(country_code):
    name = ""
    spotify_id = ""
    description = ""
    img = ""
    genre = set()
    country = set()
    website = set()

    while True:
        artist = choose_artist(country_code)
        wd_results = get_data_from_wikidata(artist)

        has_web = 'website' in wd_results["results"]

        for result in wd_results["results"]["bindings"]:
            name = result["name"]["value"]
            spotify_id = result["spotify"]["value"]
            description = result["description"]["value"]
            # img.add(result["img"]["value"])
            genre.add(result["genreName"]["value"])
            country.add(result["countryName"]["value"])
            if has_web:
                website.add(result["website"]["value"])

        if spotify_id != "":
            audio = spotify.get_data_about_id(spotify_id)
            if audio is not None:
                break

    image = spotify.get_artist_spotify_image(spotify_id)

    json_out = {
        "name": name,
        "description": description,
        "spotify": spotify_id,
        "image": image,
        "genre": list(genre),
        "country": list(country),
        "website": list(website),
        "audio": audio
    }
    return json.dumps(json_out, ensure_ascii=False).encode('utf8')


# wybiera 10 "losowych" twórców i losuje jednego
def choose_artist(country):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    print(country)
    query = """
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        SELECT DISTINCT ?name WHERE{
            {
                ?entity wdt:P106 wd:Q639669;
                    rdfs:label ?name;
                    wdt:P1902 ?spotify;
                    wdt:P27 ?country.
                ?country wdt:P297 \"""" + country + """\".
            }
            UNION
            {
                ?entity wdt:P106 wd:Q177220;
                    rdfs:label ?name;
                    wdt:P1902 ?spotify;
                    wdt:P27 ?country.
                ?country wdt:P297 \"""" + country + """\".
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

    if len(artists) == 0:
        return ""
    return artists[randint(0, len(artists) - 1)]


# pobiera dane o twórcy z wikidata
def get_data_from_wikidata(artist):
    wikidata = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
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
    return wd_results
