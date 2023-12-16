import streamlit as st 
from streamlit_extras.app_logo import add_logo
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os

# src
from src.display_song import song_with_album_cover

def analyse_playlist_variability(sp, username):
    # Get user's playlists
    playlists = sp.user_playlists(username)

    # Display user's playlists
    st.subheader(f"\n{username}'s playlists:", divider="rainbow")
    expander = st.expander("Playlists", expanded=True)
    for playlist in playlists['items']:
        
        playlist_cover = playlist["images"][0]["url"]
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        # st.write(f"- {playlist['name']} (id: {playlist['id']})")

        playlist_list_string = f'''<img src="{playlist_cover}" alt="Image" width="80"/> <span style="font-family:poppins; font-size:18px;  padding-left:10px;">   {playlist_name} - <span style="font-size:20px; color:orangered;">{playlist_id}</span></span>'''
        
        
        with expander:
            st.markdown(playlist_list_string, unsafe_allow_html=True)


    st.divider()
    # Get songs from a specific playlist
    playlist_id = st.text_input('\nEnter the playlist ID to get songs from: ')
    if playlist_id:
        
        results = sp.playlist_tracks(playlist_id)

    # Display songs from the playlist
    
    
    with st.status('Songs in the playlist:') as status:
        for track in results['items']:

            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            artwork_url = track['track']['album']['images'][0]['url']

            name_string = f'''<img src="{artwork_url}" alt="Image" width="80"/> <span style="font-family:poppins; font-size:18px; color: #1DB954; padding-left:10px;">   {track_name}</span>'''
            # name_string = song_with_album_cover(sp, song_name=track_name, artist_name=artist_name, mode="return")

            st.markdown(f''' <span>{name_string}</span> <span style="font-family:poppins; font-size:18px;">By {artist_name}</span>''', unsafe_allow_html=True)

        status.update(label="Song List Rendering - complete!", state="complete", expanded=True)