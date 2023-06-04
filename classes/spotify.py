import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

# Settings of credentials
scope = "user-modify-playback-state user-read-playback-state"
client_id = "839e78754a4c487fb2e8d60cd2e8223d"
client_secret = "cab13022188848678f982ed37e5d40c4"
redirect_uri = "http://localhost:8080"

# Starts SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# Check the connected devices
devices = sp.devices()



# Select song
def selectSong(track_name):
    results = sp.search(q=track_name, type="track", limit=1) # Search for the song in spotify

    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"] # Get the url of the song
        sp.start_playback(uris=[track_uri])
        print(f"Reproduzindo a música: {track_name}")
    else:
        print("Nenhuma música encontrada com esse nome.")


# Next song
def next():
    try:
        sp.next_track()
        print("Pulou para a próxima música!")
    except spotipy.SpotifyException as e:
        print("Erro ao pular para a próxima música:", str(e))


# Pause song
def pause():
    sp.pause_playback()


# Play song
def play():
    sp.start_playback()


# Select a playlist
def selectPlaylist(playlist_name):
    try:
        # Search for the playlist in spotify
        results = sp.search(q=playlist_name, type="playlist")
        playlists = results["playlists"]["items"]
        
        if len(playlists) > 0:
            playlist_uri = playlists[0]["uri"]  # Get the url of the playlist
            sp.start_playback(context_uri=playlist_uri)
            print("Playlist em reprodução!")
        else:
            print("Nenhuma playlist encontrada com o nome especificado.")
    except spotipy.SpotifyException as e:
        print("Erro ao reproduzir a playlist:", str(e))