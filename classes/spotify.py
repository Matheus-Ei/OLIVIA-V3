import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

# Configurar autenticação
scope = "user-modify-playback-state user-read-playback-state"
client_id = "839e78754a4c487fb2e8d60cd2e8223d"
client_secret = "cab13022188848678f982ed37e5d40c4"
redirect_uri = "http://localhost:8080"

# Criar instância do SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# Checa os dispositivos conectados
devices = sp.devices()



# Pesquisar música
def tocar_uma_musica(track_name):
    results = sp.search(q=track_name, type="track", limit=1)

    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])
        print(f"Reproduzindo a música: {track_name}")
    else:
        print("Nenhuma música encontrada com esse nome.")


# Pular para a próxima música
def pular():
    try:
        sp.next_track()
        print("Pulou para a próxima música!")
    except spotipy.SpotifyException as e:
        print("Erro ao pular para a próxima música:", str(e))


# Pausar reprodução
def pausar():
    sp.pause_playback()


# Retomar reprodução
def play():
    sp.start_playback()


# Tocar uma playlist por nome
def tocar_playlist(playlist_name):
    try:
        # Pesquisar a playlist pelo nome
        results = sp.search(q=playlist_name, type="playlist")
        playlists = results["playlists"]["items"]
        
        if len(playlists) > 0:
            playlist_uri = playlists[0]["uri"]  # Obter o URI da primeira playlist encontrada
            sp.start_playback(context_uri=playlist_uri)
            print("Playlist em reprodução!")
        else:
            print("Nenhuma playlist encontrada com o nome especificado.")
    except spotipy.SpotifyException as e:
        print("Erro ao reproduzir a playlist:", str(e))