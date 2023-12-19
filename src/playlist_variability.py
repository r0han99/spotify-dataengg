import streamlit as st 
from streamlit_extras.app_logo import add_logo
import pandas as pd
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os

# src
from src.display_song import song_with_album_cover
from src.transform_audio_features import get_audio_features
from src.visualise_audio_features import visualise


@st.cache_data
def fetch_audio_features(songs_artist_dict, _sp):

    SONG_DICTIONARY = {}
    # Example usage
    attributes = ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 
                'Speechiness', 'Acousticness', 'Instrumentalness', 
                'Liveness', 'Valence', 'Tempo', 'Duration (ms)']
    

    for  artist_name, track_name in songs_artist_dict:
        audio_features_dictionary = {}
        
        audio_features = get_audio_features(track_name, artist_name, _sp)
        if audio_features:
            for feature, value in zip(attributes, audio_features):
                audio_features_dictionary[feature] = value
            
            SONG_DICTIONARY[track_name] = audio_features_dictionary
            
        else:
            print(f"UnAvailable")
            

        audio_features_df = pd.DataFrame(SONG_DICTIONARY).T.reset_index()
        cols = audio_features_df.columns 
        cols = list(cols)
        cols[0] = 'song'
        audio_features_df.columns = cols

    return audio_features_df



def analyse_playlist_variability(sp, username):
    # Get user's playlists
    playlists = sp.user_playlists(username)

    # Display user's playlists
    st.subheader(f"\n{username}'s playlists:", divider="rainbow")
    playlist_id_dict = {}
    expander = st.expander("Playlists", expanded=True)
    for playlist in playlists['items']:
        
        playlist_cover = playlist["images"][0]["url"]
        playlist_name = playlist['name']
        playlist_id = playlist['id']

        playlist_id_dict[playlist_id] = (playlist_name, playlist_cover)
        # st.write(f"- {playlist['name']} (id: {playlist['id']})")

        playlist_list_string = f'''<img src="{playlist_cover}" alt="Image" width="80"/> <span style="font-family:poppins; font-size:18px;  padding-left:10px;">   {playlist_name} - <span style="font-size:20px; color:orangered;">{playlist_id}</span></span>'''
        
        
        with expander:
            st.markdown(playlist_list_string, unsafe_allow_html=True)


    st.divider()
    # Get songs from a specific playlist

    

    playlist_id = st.text_input('\nEnter the playlist ID to get songs from: ')
    
    
    st.markdown("_Copy and paste the orange string associated to the playlist you want!_")
    st.divider()
    
    songs_artist_dict = []
    if playlist_id != "":
        
        results = sp.playlist_tracks(playlist_id)


        
        
        with st.status('Songs in the playlist:') as status:
            for track in results['items']:

                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']

                songs_artist_dict.append((artist_name, track_name))
                


                try:
                    artwork_url = track['track']['album']['images'][0]['url']
                    name_string = f'''<img src="{artwork_url}" alt="Image" width="80"/> <span style="font-family:poppins; font-size:18px; color: #1DB954; padding-left:10px;">   {track_name}</span>'''
                except:
                    name_string = song_with_album_cover(sp, song_name=track_name, artist_name=artist_name, mode="return")

                st.markdown(f''' <span>{name_string}</span> <span style="font-family:poppins; font-size:18px;">By {artist_name}</span>''', unsafe_allow_html=True)

            status.update(label="Song List Rendering - complete!", state="complete", expanded=False)


        
        
        

        
        audio_features_df = fetch_audio_features(songs_artist_dict, sp)
        
    

    
        
        st.subheader("Making Visualisations of your taste!", divider="rainbow")



        st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 300px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True)
    
        p_name, cover = playlist_id_dict[playlist_id]
        visualise(audio_features_df,songs_artist_dict, p_name, cover, sp)

        


        






        
            
            
            
