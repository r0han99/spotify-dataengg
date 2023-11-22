# Rendering 
from src.subtitle import makesubtitle
from src.title import maketitle
from src.font import setfonts
import streamlit as st

setfonts()


# title static
st.markdown('''<center><span style="font-size: 20px; color: #191414; font-weight: bold;">This is the,</span>
            <span style="font-size: 50px; color:#1DB954; font-weight:bold;">Inferential Spotify Dashboard</span></center>''',unsafe_allow_html=True)


st.divider()
makesubtitle("About - Need Changes", size="38px", color='b', weight='bold')


with open("./info/about.md", 'r') as f:

    contents = f.read()

st.markdown(contents.format('''st.image('./assets/architecture.png)'''))