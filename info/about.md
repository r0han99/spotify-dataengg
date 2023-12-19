## What is the topic/focus of your project?

The primary goal is to build a comprehensive data pipeline with Spotify's API with different utilities that synchornously communicate with each other to maintain and generate conditional/behavioural analytics specific to the user's interest on the Dashboard. The general emphasis of this project is to streamline the data-pipeline in an efficient way so that the analytics on the dashboard wouldn't have any descrepancies. For the conditional analytics, apart from the aggregate information; such as the top songs, number of streams and so on; we plan to personalise the experience by letting the user's integrate their playlists onto the application to get a quantified perspective of their taste of music. The attributes acousticness, danceability, liveness, instrumentalness and so on are extracted from the live API end-point for individual songs in the  playlist, transformed and analysed and visualised the user. Outside scope this project, we intend to expand this idea to be plugged into a prompt template and leverage a transformer model to create a descriptive-personification of this taste-profile. 

### What problem does it solve? Why is it useful?

The project aims to solve several problems related to user-engagment and giving the ability for the user to know intricate details  through the API data-pipeline about the music they listen to that are otherwise unseen in the conventional application. Here are the itemized macro-problems that are to be addressed with this project. 

**Diffulty in Accessing Intricate Data:** Spotify's API offers a vast amount of data regarding users' music preferences. However, effectively handling and analyzing this data can present difficulties. The project's main objective is to construct a thorough data pipeline in order to simplify the processes of collecting, processing, and storing data. This improved efficiency aids in minimizing the amount of resources required and guarantees a smooth user experience. Intricate variables like the referencing the aforementioned attributes are only available through the Spotify's API utilization of which is deemed difficult without having the basic fundamentals of how to use an API end-point to collect the data. Solution to provided through this application/dashboard interface where user's have the ability to conditionally pull and visualise these intricate variables.

**Personalized Music Insights:** The project extends its functionality beyond fundamental analytics by enabling users to incorporate their playlists. This functionality assists users in obtaining a more comprehensive comprehension of their music preferences by offering analytical insights on distinct characteristics such as acousticness, danceability, liveness, and instrumentalness for each song within their playlists. The customized approach improves the user's experience by providing individualized and specific information.

**Enhancing User Engagement:** The project improves user engagement with the Spotify platform by providing personalized analytics and the option to integrate playlists. Individuals have the opportunity to enhance their comprehension of their musical preferences and explore novel songs that align with their tastes. This feature not only maintains users' interest in the application but also motivates them to further explore and engage with their music collection.

### What data does it use?

This project leverages both on Live Streaming API endpoints for real-time access to user's playlists etc., and a pre-collected batch data of the aggregate information which will be updated to date with-in a database connected to the pipeline.

## What are the tools and technologies that you are planning to use? 



Data Pipeline -- Python - Programming Language Interface 

1. **Spotify API**: This remains the data source for collecting data from the Spotify API. And Kaggle for Pre-batched data which will be updated to date with the API. 

2. **PySpark ETL**: Introduce PySpark to perform ETL tasks. PySpark can help you process and transform data efficiently. You can use PySpark to read, clean, and transform the data as needed. For example, you can use the Spark DataFrame API to perform operations on your data.

3. **Kafka**: Continue using Kafka as the messaging system for real-time data streaming. Your PySpark ETL process can publish data to Kafka topics, similar to non-PySpark ETL.

4. **Docker Container**: You can containerize your PySpark ETL code to ensure it runs consistently in different environments.

5. **Airflow**: Use Apache Airflow to orchestrate and schedule your PySpark ETL jobs, just as you would for non-PySpark tasks.

6. **MongoDB**: Store processed data in MongoDB, as mentioned previously. 

   ​	**or** 

   **PostgreSQL**

7. **Kafka (Consumer)**: Continue to use Kafka consumers to read data from Kafka topics and store it in MongoDB, as needed.

8. **Streamlit**: Develop a Streamlit application that connects to MongoDB to visualize the data.

9. **AWS & AWS Sagemaker**: ***Optionally*** used for the Machine Learning models and also for data lakes.

Note: The pipeline described above is dynamic and will be changed/adjusted based on the requirements as we progress through the development. Addition of new utilities/tools or removal of the existing tools can happen based on the situational requirement. 

In an ideal case the simplest form the pipeline will be as follows,

1. **Spotify API**: This remains the data source for collecting real-time data from the Spotify API.
2. **Kaggle Data**: You can use Kaggle for pre-batched data, and the pipeline will automatically update it to date using the Spotify API.
3. **PySpark ETL**: PySpark to perform ETL tasks for both real-time and batch data. PySpark can help you process and transform data efficiently, whether it's coming from the Spotify API or Kaggle.
4. **Airflow**: Apache Airflow to orchestrate and schedule your PySpark ETL jobs for both real-time and batch data processing.
5. **MongoDB**: Store processed data in MongoDB, which acts as your primary data storage.
6. **Streamlit**: Develop a Streamlit application that connects to MongoDB to visualize and interact with the data.

##  What is the planned architecture?

























