import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import Spotify_Api_Settings

client_id = Spotify_Api_Settings.client_id
client_secret = Spotify_Api_Settings.client_secret

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_spotify(query):
    results = sp.search(q=query, limit=1, type='track')
    if results['tracks']['items']:
        top_result = results['tracks']['items'][0]
        song_name = top_result['name']
        artist_name = top_result['artists'][0]['name']
        album_name = top_result['album']['name']

        return {
            'song_name': song_name,
            'artist_name': artist_name,
            'album_name': album_name,
        }
    else:
        return "No results found."
