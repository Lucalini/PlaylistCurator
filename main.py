
import requests
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from bs4 import BeautifulSoup

year = input("What year? Use format YYYY-MM-DD")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}/")
response.raise_for_status()
songspage= response.text

soup = BeautifulSoup(songspage, "html.parser")
songs = soup.select(selector="li h3")

artists = soup.find_all(name="span", class_="c-label")
artists_2 = []
for a in artists:

    try:
        int(a.getText())
    except:
        artists_2.append(a.getText())

artists_final = [artist.strip("\n\t\n") for artist in artists_2]

song_titles = [song.getText().strip("\n\n\t\n\t\n\t\t\n\t\t\t\t\t") for song in songs[:100]]
song_titles_final = []
for x in range (0,20):
    song_titles_final.append(song_titles[x])
artist_titles_final = []
for x in range (0,20):
    artist_titles_final.append(artists_final[x])
print(artist_titles_final)
print(song_titles_final)

for artist in artist_titles_final:
    if "Featuring" in artist:
        a_index = artist_titles_final.index(artist)
        a_split = artist.split(" ")
        artist_titles_final[a_index] = a_split[0]
print(artist_titles_final)
SPOTIPY_CLIENT_ID= "13b92f65a38b4b69b9d6838a838e588a"
SPOTIPY_SECRET_ID = "82f08825825342859f136c5a2138d9e9"
SPOTIPY_REDIRECT_URI = 'http://example.com'

scope = "playlist-modify-private"
sp= spotipy.Spotify\
    (auth_manager=SpotifyOAuth(
        scope=scope,
        client_id= SPOTIPY_CLIENT_ID,
        client_secret= SPOTIPY_SECRET_ID,
        username= "lucaverweyen",
        redirect_uri= SPOTIPY_REDIRECT_URI,
        show_dialog = True,
        cache_path="token.txt")
    )

pp=pprint.PrettyPrinter(indent=4)
pp.pprint(sp.search(q=f"{artist_titles_final[0]} {song_titles_final[0]}", limit=1 ))
song_uris = [sp.search(q=f"{artist_titles_final[x]} {song_titles_final[x]}", limit=1 )["tracks"]["items"][0]["uri"] for x in range (0,20)]
print(song_uris)
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
playlist_id = playlist["id"]
print(playlist)


results = sp.playlist_add_items(
    playlist_id= playlist_id,
    items = song_uris,
    position = None,
)

