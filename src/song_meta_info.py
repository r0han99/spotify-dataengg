# App Interface
import streamlit as st 
from streamlit_extras.app_logo import add_logo
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


def fetch_song_information(sp, song_name):
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

            return track_info, feature_names, feature_values