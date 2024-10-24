from math import ceil
from auth import *
from config import *
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up API to read User Information
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

# Get Username
username = sp.me()['id']

# Go through liked tracks and add information to lists
years, months, track_ids = [], [], []
offset = 0
results = sp.current_user_saved_tracks(result_limit,offset)
while results['items'] != []:
    for idx, item in enumerate(results['items']):
        dt_object = datetime.datetime.strptime(item['added_at'],dt_format)
        if dt_object.year >= oldest_year:
            years.append(dt_object.year)
            months.append(dt_object.strftime('%B %Y'))  # Get month and year as a string
            track_ids.append(item['track']['id'])
            print("To be added to playlist \"{}\": {} - {}".format(dt_object.strftime('%B %Y'), item['track']['artists'][0]['name'], item['track']['name']))
    offset += result_limit
    results = sp.current_user_saved_tracks(result_limit, offset)

# Set up API to create playlists
scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

# Go through liked tracks found and add them to the appropriate playlist
existing_playlists = {}
for i in range(len(years)):
    playlist_name = months[i]  # Use the month and year as the playlist name
    if playlist_name not in existing_playlists.keys():
        this_playlist = sp.user_playlist_create(user=username, name=playlist_name + " Picks", public=True, collaborative=False, description='Automatically generated playlist of liked songs using python from ' + playlist_name + '.')
        existing_playlists[playlist_name] = this_playlist['id']
    sp.user_playlist_add_tracks(user=username, playlist_id=existing_playlists[playlist_name], tracks=[track_ids[i]])

print("Added {} tracks to {} playlists.".format(len(track_ids), len(existing_playlists)))


