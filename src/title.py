import streamlit as st

def maketitle():

    with open("./web/title.html", 'r') as f:
        html = f.read()

    st.markdown(html, unsafe_allow_html=True)