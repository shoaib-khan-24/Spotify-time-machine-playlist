import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://example.com/callback"


#---------------------------***** Getting top 100 songs *****-----------------------------

travel_time = input("Which time would you like to travel to? (YYYY-MM-DD): ")

billboard_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}
billboard_url = "https://www.billboard.com/charts/hot-100"
billboard_response = requests.get(url=f"{billboard_url}/{travel_time}", headers=billboard_header)
billboard_html = billboard_response.text

soup = BeautifulSoup(billboard_html , "html.parser")
top_100_song_titles_raw = soup.select(selector="li ul li h3")
top_100_song_titles = [each_song.getText().strip() for each_song in top_100_song_titles_raw]


#---------------------------***** Authenticating spotify *****--------------------------------

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-private",
    cache_path="token.txt",
    username="khanshoaib"
))
user_profile = sp.current_user()
user_id = user_profile["id"]

#-----------------------***** Creating playlist *****---------------------------

top_100_song_titles_uris = []
for song in top_100_song_titles:
    try:
        uri = sp.search(q=song , type="track", limit=1)["tracks"]["items"][0]['uri']
        top_100_song_titles_uris.append(uri)
    except IndexError:
        print(f"{song} is not available on spotify.")

playlist_name = f"{travel_time} Top 100 Billboard"

playlist = sp.user_playlist_create(user=user_id,name=playlist_name,public=False)
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id , top_100_song_titles_uris)
print(f"Playlist {travel_time} Top 100 Billboard created successfully.")
