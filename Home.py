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
from src.font import setfonts
from src.wrapped import spotipy_wrapped



def load_keys():

    client_id = st.secrets['CLIENT_ID']
    client_secret = st.secrets['CLIENT_SECRET']
    
    keys = (client_id, client_secret)

    return keys



def instantiate_spotipy_object():

    client_id, client_secret = load_keys()

    # Instantiate Object
    SPOTIPY_CLIENT_ID = client_id
    SPOTIPY_CLIENT_SECRET = client_secret
    SPOTIPY_REDIRECT_URI = 'https://inferential-spotify-dashboard.streamlit.app/'
    # SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback' # for testing
    SCOPE= 'user-library-read user-library-modify playlist-read-private playlist-modify-private user-top-read'

    #Initialize the Spotify client
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE,
        )
    )

    return sp, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE



def get_token(sp, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE):


    token_info = None

    try:
        token_info = st.session_state['token_info']
        
    except KeyError:
        pass

    if token_info and time.time() < token_info['expires_at']:
        print("Found cached token!")
       #token_info['access_token']

    sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE)
    url = sp_oauth.get_authorize_url()

    
    cols = st.columns([5,5])
    with cols[0]:
        st.subheader("Click Authenticate to Unlock Full Features!")


    with cols[1]:
        slot = st.empty()
        slot.link_button('Authenticate!', url, use_container_width=True)

    expander = st.expander("Why Authenticate? What happens when you click it.")
    
    with open("./info/auth_notes.md", "r") as f:
        content = f.read()
    expander.markdown(content)
    expander.markdown("Example")
    expander.markdown("App URL Pre-Authentication")
    expander.image("./info/image-1.png")
    expander.markdown("App URL Post-Authentication")
    expander.image("./info/image-2.png")


    if 'code' in st.experimental_get_query_params():
        code = st.experimental_get_query_params()['code'][0]
        token_info = sp_oauth.get_access_token(code)
        st.session_state['token_info'] = token_info

        
        # Replacing button
        slot.warning("Great!, You are now authenticated!")

        
        st.session_state.token_state = "recieved"

        return token_info['access_token']
    
    return None





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
        # st.write(track)
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

    # Initialize session state
    

    setfonts()
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    st.markdown('''<center><span style="font-family: 'Circular Std', 'Poppins';font-weight:bold;">This is the, <span style="font-size: 50px; color:#1DB954; font-weight:bold; font-family:'Circular Std', 'Poppins';">Inferential Spotify Dashboard<span></span></center>''',unsafe_allow_html=True)
    st.divider()

    sp, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE = instantiate_spotipy_object()
    

    with st.sidebar:

        if 'token_state' not in st.session_state:
            st.session_state.token_state = None
        

        if st.session_state.token_state == None:
            token = get_token(sp, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE)

        st.divider()
    
    if st.session_state.token_state == "recieved":
        
        with st.sidebar:
            makesubtitle("Control shelf ⏭️", weight='bold')

        


        options = st.sidebar.selectbox("What do you want to know?", ["What do you want to know?", "Current Trends", "Compare Playlists", "Playlist Variability Analysis",
                                                                    "Know the Artist", "Song Meta-Info", "Your Playlist Analysis", "Wrapped!"])


        st.sidebar.divider()

        if options == "What do you want to know?":
            st.balloons()
        
            st.markdown('''<center><span style="font-size:30px; font-family:'poppins';"> Explore Music through Numbers! Look what the app has to offer.</span></center>''', unsafe_allow_html=True)
            st.subheader("",divider="rainbow")

            # UPDATE THIS AREA WITH APP GALLERY
            st.code("This area will Show the APP GALLERY!")

        elif options == "Song Meta-Info":

            fetch_song_meta(sp)

        elif options == "Wrapped!":
            spotipy_wrapped(sp)


    else:

        st.subheader("← Please Authenticate to proceed! ", divider="rainbow")
   


if __name__ == '__main__':

    st.set_page_config(page_title="spotify dash", layout="wide", initial_sidebar_state="auto")

    main_cs()

    

