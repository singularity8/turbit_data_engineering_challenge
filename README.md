# Turbit Data Engineering Challenge

This repository contains my solution to the data engineering challenge provided to me by Turbit. 

The solution for the following two tasks are contained within:
1. Develop a pipeline that involves setting up a MongoDB database using Docker Compose, retrieving and storing data from an external API, and exposing this data through FastAPI.
2. Load time series data from the CSV files above into a MongoDB collection and make the data accessible through the FastAPI.


## Technologies

- Docker
    - in order to easily create a MongoDB instance
- MongoDB
    - for storing example and turbine data
- Python (3.11)

## Python Setup

I used a virtual environment with Python 3.11 and the following modules:

- fastapi
    - for exposing an external API to example/turbine data
- pandas
    - dataframe handling module, used for loading/transforming csv files
- pymongo
    - helper package to interact with MongoDB
- python-dotenv
    - helper package for reading project wide credentials/settings from .env file
- requests
    - for running get requests to JSONPlaceholder API
- uvicorn
    - requirement for fastapi

## Preparation

First create a local MongoDB instance using the [docker-compose.yml](docker-compose.yml) file:
````
docker-compose up
````
The MongoDB credentials are taken from the [.env](.env) file and are currently using placeholder values. In a production setup these values should be changed and ideally stored in some form of secure key-value store.

*Note:* The Docker Compose definition also starts a Mongo Express Web Interface. This is not necessary for the pipeline to function but it allows for easier verification during development.

---

Now install the required packages [requirements.txt](requirements.txt) into your virtual environment / conda environment (depending on setup).

For instance using:
````
pip install -r requirements.txt
````

## Task 1

Then execute the [task_1_example_data_loading.py](task_1_example_data_loading.py) Python file. 
This script loads data from the following two JSONPlaceholder endpoints:
- users
- posts

For each post it queries the comments from the given post ID and ultimately stores them under the _comment_ attribute of each post.
Finally inserts the users and posts into two MongoDB collections with the same names.


## Task 2

For Task 2 execute the [task_2_load_csv_data.py](task_2_load_csv_data.py) Python file. 
This script loads data from the list of csv files in the environment variables ([.env](.env)) 
and after transformations (datetime parsing, column cleanup) inserts them into MongoDB

## FastAPI (Task 1 and 2)

Finally run the fastAPI server:
````
uvicorn task_1_and_2_fast_api_lookup:app --reload
````

You can now lookup stats (comments and posts) per User ID (range 1 to 10):
*http://localhost:8000/user_stats/{user_id}*

*Note*: the question of number of comments per user was a bit ambiguous to me as it could mean the number of comments a given user's post received or the number of comments a user wrote. I cross-checked the data to see if there is any overlap between the users who post (these ones have a user ID) and the ones who leave comments (these ones only have an email address) and could not find any overlap. As a result and for the sake of simplicity I decided to report the __number of comments a user's post received__ here.

___

As well as get data per Turbine and datetime range:
*http://localhost:8000/turbine/{turbine_id}?start_time={start_time}&end_time={end_time}*

*Note*: for the datetime filtering please use the ISO convention in the format of %Y-%m-%dT%H:%M:%S (for instance: 2016-01-01T00:10:00) and be aware that the start_time is inclusive and the end_time is exclusive

## Limitations and Future Improvements

The following limitations could be improved upon:

1. Proper credential management for MongoDB setup
2. Avoiding duplicate insertions of data into MongoDB
    - Running [task_2_load_csv_data.py](task_2_load_csv_data.py) multiple times results in duplicate entries into the MongoDB collection. This could be handled in various ways depending on implementation design and best practices (e.g. INSERT IGNORE, first deletion of data...)
3. Using Docker to set-up the Python Environment and/or FastAPI
    - Depending on how the various parts of the pipeline should be implemented and deployed, they could be combined into a single or multiple Docker Compose applications.
4. Loading data performance improvements
    - For the example data loading (task 1) I query the comments sequentially for each post. This will not scale well with an increase in posts and an implementation using asynchronous requests should be considered.