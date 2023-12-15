
# App Interface
import streamlit as st 
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os


def spotipy_wrapped(sp):

    username = st.text_input("Your Username?")
    

    if username != "":
        try:
            # Retrieve the user's top tracks
            time_range = 'long_term'  # Options: 'short_term', 'medium_term', 'long_term'
            top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=25)

            st.subheader("Your top tracks this year!")
            for idx, track in enumerate(top_tracks['items'], 1):
                st.code(f"{idx}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")


        except:
            st.error("something went wrong!")

    else:
        st.info("Enter Username!")
        st.code("test")


        
