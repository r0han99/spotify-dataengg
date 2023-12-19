# App Interface
import streamlit as st 
from streamlit_extras.app_logo import add_logo
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth



# os dependencies
import sys
import os
import base64


# Rendering 
from src.subtitle import makesubtitle
from src.font import setfonts
from src.wrapped import spotipy_wrapped
from src.playlist_variability import analyse_playlist_variability
from src.current_trends import display_current_trends



# Convert the logo image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def load_keys():

    client_id = st.secrets['CLIENT_ID']
    client_secret = st.secrets['CLIENT_SECRET']
    
    keys = (client_id, client_secret)

    # AWS Keys

    AWS_Service = st.secrets['AWS_Service']
    AWS_S3_bucket_name = st.secrets['AWS_S3_bucket_name']
    AWS_Access_key = st.secrets['AWS_Access_key']
    AWS_Secret_Access_key = st.secrets['AWS_Secret_Access_key']
    AWS_User = st.secrets['AWS_User']
    AWS_FOLDER = st.secrets['AWS_FOLDER']
    BUCKET_NAME = st.secrets['BUCKET_NAME']

    aws_keys = [AWS_Service, AWS_S3_bucket_name, AWS_Access_key, AWS_Secret_Access_key, AWS_User, AWS_FOLDER, BUCKET_NAME]

    return keys, aws_keys



def instantiate_spotipy_object():

    keys, aws_keys = load_keys()

    client_id, client_secret = keys
    
    # Instantiate Object
    SPOTIPY_CLIENT_ID = client_id
    SPOTIPY_CLIENT_SECRET = client_secret
    SPOTIPY_REDIRECT_URI = 'https://inferential-spotify-dashboard.streamlit.app/'
    # SPOTIPY_REDIRECT_URI = 'http://localhost:8501/callback' # for testing
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
        st.markdown("")
        slot = st.empty()
        slot.link_button('Authenticate!', url, use_container_width=True)


    if 'code' in st.experimental_get_query_params():
        code = st.experimental_get_query_params()['code'][0]
        token_info = sp_oauth.get_access_token(code)
        st.session_state['token_info'] = token_info

        
        # Replacing button
        slot.success("Great! You are now authenticated!")

        
        st.session_state.token_state = "recieved"

        return token_info['access_token']
    
    return None





def fetch_song_meta(sp):

    audio_feature_descriptions = {
    'danceability': 'A measure of how suitable a track is for dancing. Higher values indicate tracks that are easier to dance to.',
    'energy': 'Represents the intensity and activity of a track. Higher values indicate more energetic tracks.',
    'key': 'The key of the track, represented as an integer from 0 to 11, where 0 represents C, 1 represents C#/Db, and so on.',
    'loudness': 'The overall loudness of the track in decibels (dB). Negative values indicate quieter tracks.',
    'mode': 'Indicates whether the track is in a major key (1) or a minor key (0).',
    'speechiness': 'Measures the presence of spoken words in the track. Higher values suggest more speech-like tracks.',
    'acousticness': 'Indicates the amount of acoustic sound in the track. A higher value means the track is more acoustic.',
    'instrumentalness': 'Measures the likelihood that the track contains no vocals. Values closer to 1 suggest instrumental tracks.',
    'liveness': 'Represents the presence of a live audience in the recording. Higher values suggest live recordings.',
    'valence': 'Describes the musical positivity of the track. Higher values indicate happier, more positive tracks.',
    'tempo': 'The tempo of the track in beats per minute (BPM). It indicates the speed or pace of the music.',
    'duration_ms': 'The duration of the track in milliseconds (ms). It represents the length of the track in time.'
    }


    
    st.subheader("Know about your favourite Song Features which are otherwise Unknown!", divider="rainbow" )

    # Streamlit UI
    song_name = st.text_input("Enter a Track Name", placeholder="Runaway", value="Runaway")

    st.divider()

    if song_name:
        # Search for the song by name
        query = f"{song_name}"

        # Search for the song by name only
        results = sp.search(q=query, type='track', limit=1)

        # Check if any tracks were found
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_id = track['id']

            # Get audio features for the track
            audio_features = sp.audio_features(track_id)

            if audio_features:
                # Extract the relevant audio features
                features = audio_features[0]
                feature_names = [
                    'danceability', 'energy', 'key', 'loudness', 'mode', 
                    'speechiness', 'acousticness', 'instrumentalness', 
                    'liveness', 'valence', 'tempo', 'duration_ms'
                ]

                # Create a list of audio feature values
                feature_values = [features[feature] for feature in feature_names]

                # Get additional track information
                artist_id = track['artists'][0]['id']
                artist_name = track['artists'][0]['name']  # Get the artist name
                album_name = track['album']['name']
                album_id = track['album']['id']
                popularity = track['popularity']
                explicit = track['explicit']
                album_cover_url = track['album']['images'][0]['url']

                # Get artist information
                artist = sp.artist(artist_id)
                artist_photo_url = artist['images'][0]['url']

                # Store all the information in a dictionary
                track_info = {
                    'song_name': song_name,
                    'artist_name': artist_name,
                    'album_name': album_name,
                    'feature_values': feature_values,
                    'popularity': popularity,
                    'explicit': explicit,
                    'album_cover_url': album_cover_url,
                    'artist_photo_url': artist_photo_url,
                }

                # st.write(track_info)


                cols = st.columns(2)

                with cols[0]:

                    st.markdown(f'''<span style="font-family:'poppins'; font-size:29px; font-weight:bold; color:#1DB954;">{track_info['song_name']}</span>''',unsafe_allow_html=True)
                    st.image(track_info["album_cover_url"], width=400, caption=f'{track_info["album_name"]}')

                with cols[1]:
                    st.markdown(f'''<span style="font-family:'poppins'; font-size:25px; font-weight:bold;"> By {track_info["artist_name"]}</span>''',unsafe_allow_html=True)
                    st.image(track_info["artist_photo_url"], width=300, caption=f'')
                    st.markdown(f'''<span style="font-family:'poppins'; font-size:20px;">Song Popularity</span><span style="font-family:'poppins'; font-size:30px; font-weight:bold; color:#1DB954;">  {track_info["popularity"]}</span>''',unsafe_allow_html=True)
                    
                    # st.code(top_track_dict['Explicit'])
                    if not track_info['explicit']:
                        explicit = "No"
                    else:
                        explicit = "Yes"

                    st.markdown(f'''<span style="font-family:'poppins'; font-size:20px;">Explicit?</span><span style="font-family:'poppins'; font-size:30px; font-weight:bold; color:#1DB954;">  {explicit}</span>''',unsafe_allow_html=True)
                    

                st.divider()
                st.subheader("Audio Features", divider="green")
                # Split the features into two columns
                cols = st.columns(2)

                with cols[0]:
                    # Display the first 6 features in the first column
                    for feature_name, feature_value in zip(feature_names[:6], feature_values[:6]):
                        st.markdown(f'''<span style="font-family: poppins; font-size:25px; font-weight:bold;">{feature_name.capitalize()} - </span><span style="font-family:'poppins'; font-size:35px; font-weight:bold; color:#1DB954;">{feature_value}</span>''', unsafe_allow_html=True)
                        expander = st.expander(f"{feature_name.capitalize()}")
                        expander.info(f'''{audio_feature_descriptions[feature_name]}''',icon="ℹ️")

                with cols[1]:
                    # Display the remaining 6 features in the second column
                    for feature_name, feature_value in zip(feature_names[6:], feature_values[6:]):
                        st.markdown(f'''<span style="font-family: poppins; font-size:25px; font-weight:bold;">{feature_name.capitalize()} - </span><span style="font-family:'poppins'; font-size:35px; font-weight:bold; color:#1DB954;">{feature_value}</span>''', unsafe_allow_html=True)
                        expander = st.expander(f"{feature_name.capitalize()}")
                        expander.info(f'''{audio_feature_descriptions[feature_name]}''',icon="ℹ️")



# main interface -- app starts here
def main_cs():

    # Initialize session state
    # add_logo("./assets/next.png", height=10)

    setfonts()
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
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

        


        options = st.sidebar.selectbox("What do you want to know?", ["What do you want to know?", "Current Trends", "Compare Playlists", "Playlist Variability Analysis", "Song Meta-Info", "Wrapped!"])


        st.sidebar.divider()

        if options == "What do you want to know?":
            st.balloons()
        
            st.markdown('''<center><span style="font-size:30px; font-family:'poppins';"> Explore Music through Numbers! Look what the app has to offer.</span></center>''', unsafe_allow_html=True)
            st.subheader("",divider="rainbow")

            # UPDATE THIS AREA WITH APP GALLERY
            st.code("This area will Show the APP GALLERY!")

        elif options == "Current Trends":
            _, aws_keys = load_keys()
    
            display_current_trends(aws_keys)

        

        elif options == "Song Meta-Info":

            fetch_song_meta(sp)

        elif options == "Wrapped!":
            spotipy_wrapped(sp)


        elif options == "Playlist Variability Analysis":


            
            username = st.text_input("Enter UserName: ", value="", placeholder="nocturnel99")
            
            expander = st.expander("Spotify Usernames are not what you think! See this!", expanded=False)
            
            with expander:
                st.error("This is not the Username!")
                st.image("./assets/spotify-wrong-username.png")
                st.success("This is your username!")
                st.image("./assets/spotify-right-username.png")


            if username != "":
                analyse_playlist_variability(sp, username)

            else:
                st.warning("Enter a username!")

                st.divider()

        elif options == "Compare Playlists":

            st.markdown(
            """
            <style>
                section[data-testid="stSidebar"] {
                    width: 300px !important; # Set the width to your desired value
                }
            </style>
            """,
            unsafe_allow_html=True)

            cols = st.columns(2)

            with cols[0]:
                username = st.text_input("Enter UserName: ", value="", placeholder="nocturnel99", key="user1")
                
                expander = st.expander("Spotify Usernames are not what you think! See this!", expanded=False)
                
                with expander:
                    st.error("This is not the Username!")
                    st.image("./assets/spotify-wrong-username.png")
                    st.success("This is your username!")
                    st.image("./assets/spotify-right-username.png")


                if username != "":
                    analyse_playlist_variability(sp, username)

                else:
                    st.warning("Enter a username-1!")

                    st.divider()

            with cols[1]:
                username = st.text_input("Enter UserName: ", value="", placeholder="nocturnel99", key="user2")
                
                expander = st.expander("Spotify Usernames are not what you think! See this!", expanded=False)
                
                with expander:
                    st.error("This is not the Username!")
                    st.image("./assets/spotify-wrong-username.png")
                    st.success("This is your username!")
                    st.image("./assets/spotify-right-username.png")


                if username != "":
                    analyse_playlist_variability(sp, username)

                else:
                    st.warning("Enter a username-2!")

                    st.divider()







    else:

        st.markdown('''<center><span style="font-size:30px;"> ← </span> <span style="font-family:'sans serif'; font-size:30px;">Please Authenticate to proceed!</span></center>''',unsafe_allow_html=True)
        st.divider()
        expander = st.expander("Why Authenticate? What happens when you click it.")
    
        with open("./info/auth_notes.md", "r") as f:
            content = f.read()
        expander.markdown(content)
        expander.markdown("Example")
        expander.markdown("App URL Pre-Authentication")
        expander.image("./info/image-1.png")
        expander.markdown("App URL Post-Authentication")
        expander.image("./info/image-2.png")


    




if __name__ == '__main__':

    logo_url = './assets/spotipy-logo.png'
    logo_base64 = image_to_base64(logo_url)

    st.set_page_config(page_title="Spotify Inference", layout="wide", initial_sidebar_state="auto", page_icon=logo_url)

    main_cs()

    st.sidebar.markdown(f'''
    <center>
        <img src="data:image/png;base64,{logo_base64}" alt="Your Logo" style="width: 54px; height: 54px; vertical-align: middle;">
        <span style="font-family: 'Circular Std'; font-size: 30px;">
            Spotify 
            <span style="font-family:'manrope';display: inline-block; width: 300px; height: 25px; line-height: 20px; background-color: #f0f0f0; border: 2px solid #000; text-align: center; border-radius: 10px; font-size: 15px;">A Different Perspective</span>
        </span>
    </center>
''', unsafe_allow_html=True)




    

    

    

