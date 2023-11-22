# App Interface
import streamlit as st 

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os


# Rendering 
from src.subtitle import makesubtitle
from src.title import maketitle
from src.font import setfonts



def load_keys():

    client_id = os.environ('CLIENT_ID')
    client_secret = os.environ('CLIENT_SECRET')  

    st.write(client_id, client_secret)



# main interface -- app starts here
def main_cs():


    setfonts()
    maketitle()
    load_keys()


    with st.sidebar:
        makesubtitle("Control shelf ⏭️", weight='bold')

    st.divider()


    options = st.sidebar.selectbox("Whad do you want to know?", ["Select", "Current Trends", "Compare Playlists", "Playlist Variability Analysis",
                                                                 "Know the Artist", "Song Meta-Info", "Your Playlist Analysis"])


    st.sidebar.divider()

   






if __name__ == '__main__':

    st.set_page_config(page_title="spotify dash", layout="wide", initial_sidebar_state="auto")

    main_cs()

    

