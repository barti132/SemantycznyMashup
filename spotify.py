from random import randint

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# cid & secret here
cid = ''
secret = ''

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Dla wybranego twórcy ściaga top tracks i wybiera jednego z nich zwraca wynik jako json
def get_data_about_id(artist_id):
    result = sp.artist_top_tracks(artist_id, country='PL')

    name = []
    audio = []
    cover_art = []

    for track in result["tracks"][:10]:
        if track["preview_url"] is not None:
            name.append(track["name"])
            audio.append(track["preview_url"])
            cover_art.append(track["album"]["images"][0]['url'])

    if len(cover_art) == 0:
        return None
    i = randint(0, len(name) - 1)
    audio_track = {
        "name": name[i],
        "preview": audio[i],
        "image": cover_art[i]
    }

    return audio_track
