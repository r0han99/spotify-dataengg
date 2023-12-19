
# App Interface
import streamlit as st 
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os


def display_wrappped(top_tracks_info):

    # "Song Name":"Can You Hear The Music"
    # "Artist Name":"Ludwig Göransson"
    # "Artist Photo URL":"https://i.scdn.co/image/e7a97b420e09f4f125cd3e14fca5e7ea174e74e0"
    # "Album Name":"Oppenheimer (Original Motion Picture Soundtrack)"
    # "Popularity":77
    # "Explicit":false
    # "Album Art URL":"https://i.scdn.co/image/ab67616d0000b273af634982d9b15de3c77f7dd9"


    for top_track_dict in top_tracks_info:
        
            
        cols = st.columns(2)

        with cols[0]:

            st.markdown(f'''<span style="font-family:'poppins'; font-size:29px; font-weight:bold; color:#1DB954;">{top_track_dict['Song Name']}</span>''',unsafe_allow_html=True)
            st.image(top_track_dict["Album Art URL"], width=400, caption=f'{top_track_dict["Album Name"]}')

        with cols[1]:
            st.markdown(f'''<span style="font-family:'poppins'; font-size:25px; font-weight:bold;"> By {top_track_dict["Artist Name"]}</span>''',unsafe_allow_html=True)
            st.image(top_track_dict["Artist Photo URL"], width=300, caption=f'')
            st.markdown(f'''<span style="font-family:'poppins'; font-size:20px;">Song Popularity</span><span style="font-family:'poppins'; font-size:30px; font-weight:bold; color:#1DB954;">  {top_track_dict["Popularity"]}</span>''',unsafe_allow_html=True)
            
            # st.code(top_track_dict['Explicit'])
            if not top_track_dict['Explicit']:
                explicit = "No"
            else:
                explicit = "Yes"

            st.markdown(f'''<span style="font-family:'poppins'; font-size:20px;">Explicit?</span><span style="font-family:'poppins'; font-size:30px; font-weight:bold; color:#1DB954;">  {explicit}</span>''',unsafe_allow_html=True)
            






def spotipy_wrapped(sp):

    st.subheader("Wrapping Your Top Tracks This Year!", divider="rainbow")



    with st.status("Brewing your year-round songs!") as status:
        try:
            # Retrieve the user's top tracks
            time_range = 'long_term'  # Options: 'short_term', 'medium_term', 'long_term'
            top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=25)

            top_tracks_info = []

            for idx, track in enumerate(top_tracks['items'], 1):
                song_name = track['name']
                artist_name = ', '.join([artist['name'] for artist in track['artists']])
                album_name = track['album']['name']
                popularity = track['popularity']
                explicit = track['explicit']
                album_art_url = track['album']['images'][0]['url']

                # Retrieve the artist's photo (you can choose the desired image size)
                artist_id = track['artists'][0]['id']  # Assuming the first artist in the list
                artist_info = sp.artist(artist_id)
                artist_photo_url = artist_info['images'][0]['url'] if artist_info['images'] else None

                track_info = {
                    'Song Name': song_name,
                    'Artist Name': artist_name,
                    'Artist Photo URL': artist_photo_url,
                    'Album Name': album_name,
                    'Popularity': popularity,
                    'Explicit': explicit,
                    'Album Art URL': album_art_url
                }

                top_tracks_info.append(track_info)

            # Now, top_tracks_info is a list of dictionaries, each containing information about a top track.
            st.balloons()
            status.update(label="Your Spotify Wrapped is Complete! Click Me!", state="complete", expanded=False)
            st.markdown(
            """
            <style>
                section[data-testid="stSidebar"] {
                    width: 400px !important; # Set the width to your desired value
                }
            </style>
            """,
            unsafe_allow_html=True)


            
            display_wrappped(top_tracks_info)

        

        except Exception as e:
            st.error(f"Something went wrong: {e}")


        
