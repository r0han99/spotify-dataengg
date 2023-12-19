# App Interface
import streamlit as st 
from streamlit_extras.app_logo import add_logo
import time
from datetime import date

# aws 
import boto3
import pandas as pd



def get_album_art(sp, song_name, artist_name):
    # Formulate the query
    query = f"track:{song_name} artist:{artist_name}"

    # Search for the song
    results = sp.search(q=query, type='track', limit=1)

    # Check if any tracks were found
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        album_cover_url = track['album']['images'][0]['url']  # URL of the album art
        return album_cover_url
    else:
        return "./assets/spotipy-logo.png"





def display_current_trends(aws_keys, sp):

    AWS_Service, AWS_S3_bucket_name, AWS_Access_key, AWS_Secret_Access_key, AWS_User, AWS_FOLDER, BUCKET_NAME = aws_keys

    # Bucket Details
    s3 = boto3.resource(
        service_name = AWS_Service,
        region_name = 'us-east-2',
        aws_access_key_id = 'AKIA2QMVGA2JUUHZXEAF',
        aws_secret_access_key = AWS_Secret_Access_key
    )
    # Read file from s3 - Make sure to have all my creds.
    obj = s3.Bucket('dcsc-spotify').Object('Extract/top_50_df.csv').get()
    data = pd.read_csv(obj['Body'], index_col=0)
    # st.dataframe(data)


    # Get today's date
    today_date = date.today().strftime("%B %d %Y")

    # Add the subheader with today's date
    st.subheader(f"Global Top 50 Songs Now! Updated Daily! ~ {today_date}", divider="rainbow")

    expander = st.expander("Data is Powered By")

    with expander:
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Data Orchestration & Daily Updates by →")
            st.subheader("Date Warehouse and Storage by →")
            
        with cols[1]:
            st.image("./assets/airflow.png", width=200)
            st.image("./assets/aws-s3.webp", width=200)
    
    st.divider()
    

    songs = data['title'].to_list()
    artists = data['artist'].to_list()
    album = data['album'].to_list()
    popularity = data['popularity'].to_list()

    with st.status("Loading Top50 Global Songs as of Today!") as status:
        cols = st.columns(2)
        for song, artist, al, pop in zip(songs[:25], artists[:25], album[:25], popularity[:25]):
            url = get_album_art(sp, song, artist)
            with cols[0]:

                st.markdown(f'''<span style="font-family:'poppins'; font-size:29px; font-weight:bold; color:#1DB954;">{song}</span>''',unsafe_allow_html=True)
                st.image(url, width=400, caption=f'{al}')

                st.markdown(f'''<span style="font-family:'poppins'; font-size:25px; font-weight:bold;"> By {artist}</span>''',unsafe_allow_html=True)
                st.markdown(f'''<span style="font-family:'poppins'; font-size:20px;">Song Popularity</span><span style="font-family:'poppins'; font-size:30px; font-weight:bold; color:#1DB954;">  {pop}</span>''',unsafe_allow_html=True)
                
        for song, artist, al, pop in zip(songs[25:], artists[25:], album[25:], popularity[25:]):
            url = get_album_art(sp, song, artist)
            with cols[1]:

                st.markdown(f'''<span style="font-family:'poppins'; font-size:29px; font-weight:bold; color:#1DB954;">{song}</span>''',unsafe_allow_html=True)
                st.image(url, width=400, caption=f'{al}')

                st.markdown(f'''<span style="font-family:'poppins'; font-size:25px; font-weight:bold;"> By {artist}</span>''',unsafe_allow_html=True)
                st.markdown(f'''<span style="font-family:'poppins'; font-size:20px;">Song Popularity</span><span style="font-family:'poppins'; font-size:30px; font-weight:bold; color:#1DB954;">  {pop}</span>''',unsafe_allow_html=True)
                

        status.update(label="Completed!", state="complete", expanded=False)



    

    
