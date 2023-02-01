import spotipy
from spotipy.oauth2 import SpotifyOAuth
from login import clientid, clientsecret

scope = "user-read-currently-playing"

def get_current_track():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=clientid, client_secret=clientsecret, scope=scope, redirect_uri="http://localhost:8888/callback"))
        json_resp = sp.currently_playing()
        track_id = json_resp['item']['id']
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]
        images = [image for image in json_resp['item']
                ['album']['images'][-1]['url']]

        artist_names = ', '.join([artist['name'] for artist in artists])
        image_url = ''.join(image for image in images)
        current_track_info = {
            "id": track_id,
            "track_name": track_name,
            "artists": artist_names,
            "imageurl": image_url
        }

        return current_track_info

    except Exception as e:
        print('song fetch failed:   ', e)

print(get_current_track())