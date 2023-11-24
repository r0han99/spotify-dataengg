# App Interface
import streamlit as st 
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os


# Rendering 
from src.subtitle import makesubtitle
from src.title import maketitle
from src.font import setfonts



def load_keys():

    client_id = st.secrets['CLIENT_ID']
    client_secret = st.secrets['CLIENT_SECRET']
    
    keys = (client_id, client_secret)

    return keys




def get_token():


    client_id, client_secret = load_keys()

    # Instantiate Object
    SPOTIPY_CLIENT_ID = client_id
    SPOTIPY_CLIENT_SECRET = client_secret
    # SPOTIPY_REDIRECT_URI = 'https://inferential-spotify-dashboard.streamlit.app/'
    SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback' # for testing
    SCOPE= 'user-library-read user-library-modify playlist-read-private playlist-modify-private'

    #Initialize the Spotify client
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
        )
    )
    token_info = None

    

    try:
        token_info = st.session_state['token_info']
        
    except KeyError:
        pass

    if token_info and time.time() < token_info['expires_at']:
        print("Found cached token!")
        return token_info['access_token']

    sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE)
    url = sp_oauth.get_authorize_url()
    st.sidebar.link_button('Click Here to Authenticate!', url)

    if 'code' in st.experimental_get_query_params():
        code = st.experimental_get_query_params()['code'][0]
        token_info = sp_oauth.get_access_token(code)
        st.session_state['token_info'] = token_info
        return (token_info['access_token'], sp)
    
    return (None, sp)



def fetch_song_meta(sp):

    # Get the current user's username
    user_info = sp.current_user()
    user_id = user_info['id']
    # print(f"Logged in as {user_id}")

    # Search for a track
    track_name = st.text_input("Enter a Track Name", placeholder="Runaway",value="Runaway")
    search_results = sp.search(q=track_name, type='track', limit=1)

    if search_results and search_results['tracks']['items']:
        track = search_results['tracks']['items'][0]
        # Get album information
        st.write(track)
        album_info = sp.album(track['album']['id'])
        track_id = track['id']
        cols = st.columns(2)

        with cols[0]:
            makesubtitle(f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}", color='b',weight='bold')
            #st.code(f"Track: {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
            album_art_url = album_info['images'][0]['url']
            st.image(album_art_url, width=450)

        # Get album art URL
        with cols[1]:
            
            
            # Get audio features for the track
            audio_features = sp.audio_features([track['uri']])[0]
            st.code(f"Audio Features for {track['name']}:")
            st.code(f"Danceability: {audio_features['danceability']}")
            st.code(f"Energy: {audio_features['energy']}")
            st.code(f"Tempo: {audio_features['tempo']}")

        

        

        
    else:
        st.warning(f"No track found with the name '{track_name}'")


# main interface -- app starts here
def main_cs():


    setfonts()
    maketitle()
    


    token, sp = get_token()
    st.write(token)
    st.write(sp)
    st.sidebar.divider()

    with st.sidebar:
        makesubtitle("Control shelf ⏭️", weight='bold')

    st.divider()


    options = st.sidebar.selectbox("What do you want to know?", ["Select", "Current Trends", "Compare Playlists", "Playlist Variability Analysis",
                                                                 "Know the Artist", "Song Meta-Info", "Your Playlist Analysis"])


    st.sidebar.divider()

    


    if options == "Song Meta-Info":

        fetch_song_meta(sp)

   


if __name__ == '__main__':

    st.set_page_config(page_title="spotify dash", layout="wide", initial_sidebar_state="auto")

    main_cs()

    

