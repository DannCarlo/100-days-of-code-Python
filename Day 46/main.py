import spotipy
import urllib
import datetime as dt
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from bs4 import BeautifulSoup

DAYS_OF_MONTH = [31, 28, 31, 30, 31, 30, 31, 30, 31, 31, 30, 31]

BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

def add_zero_to_date(number):
    if number < 10: return f"0{number}"
    else: return str(number)

def add_song_from_url_to_data_(url, data_dict, data_name):
    html_code = get_html(url)

    soup = BeautifulSoup(markup=html_code, features="html.parser")
    song_name = soup.select(selector=".o-chart-results-list-row-container .c-title")[0].string.strip()
    song_artist = soup.select(selector=".o-chart-results-list-row-container .c-title + .c-label")[0].string.strip()

    data_dict[data_name] = {
        "song_name" : song_name,
        "song_artist" : song_artist
    }

def get_html(url):
    website_request = urllib.request.Request(url)
    website_html = urllib.request.urlopen(website_request)

    return website_html

def add_song_info_from_spotify_to_data(data_dict):
    global spotify

    for date in data_dict:
        song_name = data_dict[date]["song_name"].lower()
        song_artist = data_dict[date]["song_artist"].lower()

        track_params = f"track:{song_name}"
        results = spotify.search(q=track_params, limit=5, type="track")

        for result in results["tracks"]["items"]:
            track_name = result["name"].lower()
            if song_name in track_name:
                track_artists = result["artists"]

                for track_artist in track_artists:
                    track_artist_name = track_artist["name"].lower()
                    if "é" in track_artist_name:
                        track_artist_name = track_artist_name.replace("é", "e")
                    if track_artist_name in song_artist:
                        track_result = result
                        break
        try:
            song_id = track_result["id"]
            song_uri = track_result["uri"]
        except:
            data_dict[date]["song_id"] = None
            data_dict[date]["song_uri"] = None
        else:
            data_dict[date]["song_id"] = song_id
            data_dict[date]["song_uri"] = song_uri

def create_spotify_playlist(title, data_dict):
    global spotify_user

    user_info = spotify_user.current_user()
    user_id = user_info["id"]

    playlist_id = spotify_user.user_playlist_create(user=user_id, name=title)["id"]

    song_ids_list = []
    for date in data_dict:
        song_uri = songs_data[date]["song_uri"]
        if song_uri not in song_ids_list and song_uri is not None: song_ids_list.append(song_uri)

    spotify_user.playlist_add_items(playlist_id, song_ids_list)

songs_data = dict()

datetime_today = dt.datetime.now()
month_now = datetime_today.month
day_now = datetime_today.day

# Ask month input
month_input = int(input(f"What month would you like to get all top 1 songs? input 1-{month_now} "))
days_of_month = DAYS_OF_MONTH[month_input - 1]
starting_day = 1

date_string = f"2024-{add_zero_to_date(month_input)}-{add_zero_to_date(starting_day)}"
date_url = BILLBOARD_URL + date_string

# Get top 1 song name with its artist for the month
while ((month_input==month_now and starting_day<=day_now and starting_day<=days_of_month)
       or (month_input!=month_now and starting_day<=days_of_month)):
    add_song_from_url_to_data_(date_url, songs_data, date_string)

    starting_day += 7
    date_string = f"2024-{add_zero_to_date(month_input)}-{add_zero_to_date(starting_day)}"
    date_url = BILLBOARD_URL + date_string

# Get song spotify uri from the gathered songs in the web
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
add_song_info_from_spotify_to_data(songs_data)

print(songs_data)

# Create playlist and add all the gathered songs via its song uri
spotify_user = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))
playlist_title = f"{date_string[:-3]} All Top 1 Tracks"
create_spotify_playlist(playlist_title, songs_data)
