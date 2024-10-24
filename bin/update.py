#pip3 install spotipy
from auth import *
from config import *
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Set up API to read User Information
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Get Username
username = sp.me()['id']

# Set up API to create playlists
playlist_scope = "playlist-modify-public"
sp_playlist = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=playlist_scope))

# Get the current month and year
current_month = datetime.datetime.now().month
current_year = datetime.datetime.now().year

# Get previous month and year
previous_month = current_month - 1
previous_year = current_year

# Check if the previous month is January to handle year difference
if previous_month == 0:  # January
    previous_month = 12  # Set previous month to December
    previous_year -= 1    # Decrement the year

# Use previous month and year for further operations
previous = (previous_month, previous_year)


# Check for a playlist for the current month and year
playlist_name = datetime.datetime.now().strftime('%B %Y') + " Picks"
playlists = sp_playlist.user_playlists(user=username)

playlist_id = None
for playlist in playlists['items']:
    if playlist['name'] == playlist_name:
        playlist_id = playlist['id']
        break

# Get the track IDs already in the existing playlist
existing_track_ids = set()
if playlist_id:
    offset = 0
    while True:
        playlist_items = sp_playlist.playlist_items(playlist_id, limit=result_limit, offset=offset)
        tracks = playlist_items.get('items', [])
        for track in tracks:
            existing_track_ids.add(track['track']['id'])
        if not tracks:
            break
        offset += result_limit

# Go through liked tracks and add newly liked songs to the current month's playlist
offset = 0
results = sp.current_user_saved_tracks(limit=result_limit, offset=offset)
while results['items']:
    for item in results['items']:
        dt_object = datetime.datetime.strptime(item['added_at'], dt_format)
        track_id = item['track']['id']

        if dt_object.year == current_year and dt_object.month == current_month:
            if playlist_id:
                if track_id not in existing_track_ids:
                    # Add the track to the current month's playlist
                    sp_playlist.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=[track_id])
                    print("Added to playlist \"{}\": {} - {}".format(playlist_name, item['track']['artists'][0]['name'], item['track']['name']))
                    existing_track_ids.add(track_id)
                else:
                    print("Skipping duplicate track: {} - {}".format(item['track']['artists'][0]['name'], item['track']['name']))
            else:
                # Create the playlist for the current month if it doesn't exist
                this_playlist = sp_playlist.user_playlist_create(user=username, name=playlist_name, public=True, collaborative=False, description='Automatically generated playlist of liked songs using Python from ' + playlist_name)
                playlist_id = this_playlist['id']
                sp_playlist.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=[track_id])
                print("Created and added to playlist \"{}\": {} - {}".format(playlist_name, item['track']['artists'][0]['name'], item['track']['name']))
                existing_track_ids.add(track_id)

    offset += result_limit
    results = sp.current_user_saved_tracks(limit=result_limit, offset=offset)

# Check for a playlist for the previous month and year
previous_playlist_name = datetime.datetime.now().replace(month=previous[0], year=previous[1]).strftime('%B %Y') + " Picks"
playlists = sp_playlist.user_playlists(user=username)

previous_playlist_id = None
for playlist in playlists['items']:
    if playlist['name'] == previous_playlist_name:
        previous_playlist_id = playlist['id']
        break


# Get the track IDs already in the existing playlist for last month
existing_track_ids = set()
if previous_playlist_id:
    offset = 0
    while True:
        playlist_items = sp_playlist.playlist_items(previous_playlist_id, limit=result_limit, offset=offset)
        tracks = playlist_items.get('items', [])
        for track in tracks:
            existing_track_ids.add(track['track']['id'])
        if not tracks:
            break
        offset += result_limit

# Go through liked tracks and add newly liked songs to the current month's playlist
offset = 0
results = sp.current_user_saved_tracks(limit=result_limit, offset=offset)
while results['items']:
    for item in results['items']:
        dt_object = datetime.datetime.strptime(item['added_at'], dt_format)
        track_id = item['track']['id']
        # Check if the track was added in the previous month
        if dt_object.year == previous[1] and dt_object.month == previous[0]:
            if previous_playlist_id:
                if track_id not in existing_track_ids:
                    # Add the track to the previous month's playlist
                    sp_playlist.user_playlist_add_tracks(user=username, playlist_id=previous_playlist_id, tracks=[track_id])
                    print("Added to playlist \"{}\": {} - {}".format(previous_playlist_name, item['track']['artists'][0]['name'], item['track']['name']))
                    existing_track_ids.add(track_id)
                else:
                    print("Skipping duplicate track: {} - {}".format(item['track']['artists'][0]['name'], item['track']['name']))
            else:
                # Create the playlist for the previous month if it doesn't exist
                this_playlist = sp_playlist.user_playlist_create(user=username, name=previous_playlist_name, public=True, collaborative=False, description='Automatically generated playlist of liked songs using Python from ' + previous_playlist_name)
                previous_playlist_id = this_playlist['id']
                sp_playlist.user_playlist_add_tracks(user=username, playlist_id=previous_playlist_id, tracks=[track_id])
                print("Created and added to playlist \"{}\": {} - {}".format(previous_playlist_name, item['track']['artists'][0]['name'], item['track']['name']))
                existing_track_ids.add(track_id)

    offset += result_limit
    results = sp.current_user_saved_tracks(limit=result_limit, offset=offset)


# Calculate the time until the next day
#now = datetime.datetime.now()
#next_day = now + datetime.timedelta(days=1)
#next_day_start = datetime.datetime(year=next_day.year, month=next_day.month, day=next_day.day, hour=0, minute=0, second=0)
#time_to_sleep = (next_day_start - now).total_seconds()

# Wait until the next day
#time.sleep(time_to_sleep)
