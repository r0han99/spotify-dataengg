# Rendering 
from src.subtitle import makesubtitle
from src.font import setfonts
import streamlit as st

setfonts()


# title static
st.markdown('''<center><span style="font-size: 20px; color: #191414; font-weight: bold;">This is the,</span>
            <span style="font-size: 50px; color:#1DB954; font-weight:bold;">Inferential Spotify Dashboard</span></center>''',unsafe_allow_html=True)


st.divider()
makesubtitle("About", size="38px", color='b', weight='bold')


with open("./info/about.md", 'r') as f:

    contents = f.read()

st.markdown(contents)
st.image('./assets/updated_architecture.png')


rest_of_the_content = '''


Planned Architecture. It is subject to changes based on the situational requirements.

## What is the planned delivery format? (Website/App? Dashboard? )

The planned delivery format for this project is Dashboard and will be presented on Streamlit Inferface. Streamlit is a Python library that enables the rapid development of web applications with minimal coding requirements. This guide aims to provide an introduction to setting up a basic Streamlit dashboard. We will demonstrate the simplicity and flexibility of Streamlit for visualizing and analyzing data.

## What are the difficulties you're facing, if any?

During our work with the Spotify API, we encountered several unique challenges. Initially, the process of understanding and implementing authentication and authorization was found to be highly intricate. The careful attention required for this task included understanding the OAuth 2.0 flows, managing token security, and ensuring the appropriate authorization scopes.

We encountered an additional obstacle in the form of the stringent rate limiting policy enforced by Spotify. To effectively handle API requests and avoid exceeding usage limits, it is crucial to adopt a cautious approach, particularly when dealing with applications that have high levels of usage.

The data obtained from the Spotify API can be quite intricate because of its nested JSON structures. The extraction of the specific information we required necessitated significant manipulation and parsing of the data. Furthermore, certain data that could be accessed directly on the Spotify user interface was not accessible through the API, resulting in occasional limitations.

Efficiently managing token refresh, effectively handling errors, staying informed about API changes, and budgeting for potential API usage costs were all important factors that demanded our ongoing attention. 


'''

st.markdown(rest_of_the_content)

st.divider()