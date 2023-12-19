# App Interface
import streamlit as st 
from streamlit_extras.app_logo import add_logo
import time

# aws 
import boto3
import pandas as pd




def display_current_trends(aws_keys):

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
    st.dataframe(data)
