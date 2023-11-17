# App Interface
import streamlit as st 


# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


# GLOBAL PARAMS
Green = "#1DB954"
Black = "#191414"


def maketitle():

    with open("./src/title.html", 'r') as f:
        html = f.read()

    st.markdown(html, unsafe_allow_html=True)

def makesubtitle(text, size="30px", color='g', weight='regular'):

    global Black
    global Green
    
    if color == 'g':
        
        color = Green
    elif 'b':
        color = Black
     # Defaulting 
    else: 
        
        color = Black

    
    
    st.markdown(f'''<span style="font-family: 'Circular Std'; font-size: {size}; color: {color}; font-weight: {weight}">{text}</span>''', unsafe_allow_html=True)



# main interface -- app starts here
def main_cs():


    maketitle()


    with st.sidebar:
        makesubtitle("Control shelf ⏭️", weight='bold')

    st.sidebar.divider()








if __name__ == '__main__':

    st.set_page_config(page_title="spotify dash", layout="wide", initial_sidebar_state="auto")

    main_cs()

    st.divider()

