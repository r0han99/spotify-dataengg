import streamlit as st 
from streamlit_extras.app_logo import add_logo
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os




def song_with_album_cover(sp, song_name, artist_name, mode="print"):


    # Search for the song by name and artist
    results = sp.search(q=f"track:{song_name} artist:{artist_name}", type='track', limit=1)

    # Check if any tracks were found
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        album_id = track['album']['id']

        # Get the album details
        album = sp.album(album_id)

        # Get the album cover URL (largest available size)
        cover_url = album['images'][0]['url']

        
    
        if mode == "print":
            st.markdown(f'''<img src="{cover_url}" alt="Image" width="80"/> <span style="font-family:poppins; font-size:18px; color: #1DB954; padding-left:10px;">  {song_name}</span>''', unsafe_allow_html=True)
    
        elif mode == "return":

            return f'''<img src="{cover_url}" alt="Image" width="80"/> <span style="font-family:poppins; font-size:18px; color: #1DB954; padding-left:10px;">   {song_name}</span>'''
