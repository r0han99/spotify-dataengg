import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


import boto3
import os
from dotenv import load_dotenv



def extract_transform():

    load_dotenv()

    # AWS Credentials
    AWS_Service = os.getenv('AWS_SERVICE')
    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_Secret_Access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_USER = os.getenv('AWS_USER')
    AWS_FOLDER = os.getenv('AWS_FOLDER')

    # Spotify Credentials
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

    client_id = SPOTIPY_CLIENT_ID
    client_secret = SPOTIPY_CLIENT_SECRET
    redirect_uri = SPOTIPY_REDIRECT_URI


    # Bucket Details
    s3 = boto3.resource(
        service_name = AWS_Service,
        region_name = 'us-east-2',
        aws_access_key_id = 'AKIA2QMVGA2JUUHZXEAF',
        aws_secret_access_key = AWS_Secret_Access_key
    )



    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print("Extracting...")
        # Global Top 50 Playlist URI (this URI is subject to change)
    playlist_uri = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'

    # Fetch playlist
    results = sp.playlist_tracks(playlist_uri)

    songs_data = []
    for idx, item in enumerate(results['items']):
        track = item['track']
        song_info = {
            'title': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            # Spotify doesn't provide streaming numbers via Spotipy, placeholder added
            'popularity': track['popularity'], 
            'trending': 'N/A'
        }
        songs_data.append(song_info)

    
    # Uploading the file to s3. 
    pd.DataFrame(songs_data).to_csv('top_50_df.csv')
    s3.Bucket('dcsc-spotify').upload_file(Filename = "top_50_df.csv", Key = 'Extract/top_50_df.csv')

    

    # Formatted string
    formatted_string = "\nExtraction done... and Loaded to the Bucket"
    print(formatted_string)


#Get the top 50 songs and convert to DataFrame
top_50_df = extract_transform()




