
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os



def get_audio_features(song_name, artist_name, sp):
    

    # Search for the song by name
    
    
    query = f"{song_name} artist:{artist_name}"

    # Search for the song by name and artist
    results = sp.search(q=query, type='track', limit=1)

    # Check if any tracks were found
    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        
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
            
            return feature_values
        else:
            return None  # Audio features not found for the track
    else:
        return None  # Track not found


    
    

# print(SONG_DICTIONARY)