
import streamlit as st

def setfonts():

    with open( "./web/style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)