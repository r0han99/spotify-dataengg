import seaborn as sns
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go

import streamlit as st 
import pandas as pd
import time

# for spotify 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# os dependencies
import sys
import os

plt.rcParams['font.family'] = 'avenir'


def show_song_cover(sp, track_name, artist_name):
    # Create the search query with both track and artist name
    search_query = f"{track_name} artist:{artist_name}"
    
    search_results = sp.search(q=search_query, type='track', limit=1)

    if search_results and search_results['tracks']['items']:
        track = search_results['tracks']['items'][0]
        # Get album information
        album_info = sp.album(track['album']['id'])
        track_id = track['id']

        st.subheader(f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
        album_art_url = album_info['images'][0]['url']
        st.image(album_art_url, width=450)






def visualise(df,songs_artist_dict, p_name, cover, sp):


    
    song_dict = {song: artist for artist, song in songs_artist_dict}


    cols = st.columns(2)

    with cols[0]:
        st.image(cover, width=300)

    with cols[1]:
        st.markdown(f'''<span style="font-size:50px; font-family:'poppins;'; color:#1DB954; font-weight:bold;">{p_name}</span>''',unsafe_allow_html=True)
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        

        st.divider()

    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.subheader("Total Number of Songs in the playlist")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        

    with cols[1]:
        st.markdown(f'''<span style="font-size:90px; font-family:'poppins;'; color:#1DB954; font-weight:bold; text-align:right;">{df.shape[0]}</span>''',unsafe_allow_html=True)
        st.markdown("")
        st.markdown("")
        st.markdown("")



    st.divider()
    cols = st.columns(2)
       
    

    with cols[0]:
        st.subheader("How Alive is Your Playlist?")
        s = df[['Danceability', 'Energy', 'Liveness', 'Valence']].mean()
        df1 = s.to_frame().reset_index()
        df1.rename(columns={'index': 'theta', 0: 'r'}, inplace=True)

        # Create a polar plot with filled areas using go.Scatterpolar
        fig = go.Figure()

        color_with_opacity = "#1DB954"
        fill_opacity = 0.5
        fig.add_trace(go.Scatterpolar(
            r=df1['r'],
            theta=df1['theta'],
            fill='toself',
            fillcolor=f'rgba{tuple(int(color_with_opacity[i:i+2], 16) for i in (1, 3, 5)) + (fill_opacity,)}',
            name='Average Values'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True),
            ),
            showlegend=False,
            template='plotly_dark'  # Set the built-in theme here
        )


        st.plotly_chart(fig)

    with cols[1]:
        st.subheader("How Technical is your playlist?")
        # Calculate the mean values
        s = df[['Acousticness', 'Instrumentalness', 'Speechiness', 'Liveness']].mean()
        df1 = s.to_frame().reset_index()
        df1.rename(columns={'index': 'theta', 0: 'r'}, inplace=True)

        # Create a polar plot with filled areas using go.Scatterpolar
        fig = go.Figure()

        color_with_opacity = "#1DB954"
        fill_opacity = 0.5
        fig.add_trace(go.Scatterpolar(
            r=df1['r'],
            theta=df1['theta'],
            fill='toself',
            fillcolor=f'rgba{tuple(int(color_with_opacity[i:i+2], 16) for i in (1, 3, 5)) + (fill_opacity,)}',
            line=dict(color='#1DB954'),  # Line color
            name='Average Values'
        ))

        # Customize the polar layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True),
            ),
            showlegend=False,
            template='plotly_dark'  # Set the template/theme
        )

        st.plotly_chart(fig)


    st.subheader("Playlist Song Key's")
    sns.set(style="whitegrid")  # Set the style of the plot
    keys = df.Key.value_counts().sort_index(ascending = True)
    st.bar_chart(keys, color="#1DB954")


    


    count, bins = np.histogram(df['Tempo'], bins=50, density=True)
    bins = 0.5 * (bins[:-1] + bins[1:])  # Convert bin edges to centers

    # Create a DataFrame from the histogram data
    hist_data = pd.DataFrame({
        'Tempo': bins,
        'Density': count
    })

    # Plot the line chart using Streamlit's native charting
    st.subheader("Tempo Distribution of the Playlist")
    st.line_chart(hist_data.set_index('Tempo'), color="#1DB954")

    st.subheader("Duration Distribution of the songs in the Playlist")

    # Create a Chart object using Altair
    df['Duration (s)'] = df['Duration (ms)'] / 1000
    duration_chart = alt.Chart(df).mark_bar(color="#1DB954").encode(
        x=alt.X('Duration (s):Q', bin=alt.Bin(maxbins=20), title='Duration (s)'),
        y=alt.Y('count():Q', title='Count'),
    ).properties(
        width=600,
        title="Song Duration Distribution"
    )

    # Show the chart using st.altair_chart
    st.altair_chart(duration_chart, use_container_width=True)
    
    cols = st.columns(2)

    with cols[0]:
        st.subheader("Your Loudest Song", divider="green")
        song = df[df.Loudness ==df.Loudness.max()][['song', 'Loudness']]['song'].values[0]
        artist = song_dict[song]
        loudness = df[df.Loudness ==df.Loudness.max()][['song', 'Loudness']]['Loudness'].values[0]
        
        show_song_cover(sp, song, artist)
        st.code(f"Loudness = {loudness} dB")

    with cols[1]:
        st.subheader("Your Quietest Song", divider="green")
        song = df[df.Loudness ==df.Loudness.min()][['song', 'Loudness']]['song'].values[0]
        artist = song_dict[song]
        loudness = df[df.Loudness ==df.Loudness.min()][['song', 'Loudness']]['Loudness'].values[0]
        show_song_cover(sp, song, artist)
        st.code(f"Loudness = {loudness} dB")

