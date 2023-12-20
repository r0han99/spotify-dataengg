import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from Scripts.pipline import extract_transform


default_args = {
    'owner': 'data-center-team-rohan-sid-jj-wyett',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='Spotify-ETL-DAG',
    default_args=default_args,
    start_date=datetime(2023, 12, 16, 2),
    description= 'Fetchs the Global Top 50 Songs Playlist from Spotify, Transforms it to Dataframe and Stores it in AWS S3.',
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='extract_transform',
        python_callable=extract_transform
    )
