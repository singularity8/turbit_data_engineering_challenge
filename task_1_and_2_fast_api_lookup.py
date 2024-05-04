"""
FastAPI implementation with two endpoints:
- /user_stats/{user_id} (GET)
- /turbine/{turbine_id} (GET)

@Author: Paul
@Date: 2024-05-04
"""

import logging
import os
from datetime import datetime as dt

from dotenv import load_dotenv
from fastapi import FastAPI

from db_mongo import DBConnection

# Loading variables from .env file
load_dotenv()

# Load Mongo Credentials (from .env file)
mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_passwd = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

app = FastAPI()

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


@app.get("/user_stats/{user_id}")
def get_user_stats(user_id: int, db_name="turbit") -> dict:
    """
    Gets User Stats for a given User ID (Task 1)

    Args:
        user_id (int)
        db_name (str, optional) Defaults to "turbit".

    Returns:
        user stats (dict)
    """

    logging.info("Connecting to MongoDB")

    MongoDB = DBConnection(mongo_user, mongo_passwd)

    query_results = MongoDB.find({"userId": user_id}, "posts", db_name)

    posts_user = 0
    comments_user = 0

    for res in query_results:
        posts_user += 1
        comments_user += len(res["comments"])

    return {"posts": posts_user, "comments": comments_user}


@app.get("/turbine/{turbine_id}")
def get_turbine_data(
    turbine_id: str, start_time: str, end_time: str, db_name="turbit"
) -> list[dict]:
    """
    Gets Turbine Data for given Turbine ID and start/end time (Task 2)

    Args:
        turbine_id (str)
        start_time (str in format %Y-%m-%dT%H:%M:%S) (greater than / >= filtering)
        end_time (str in format %Y-%m-%dT%H:%M:%S) (less than / < filtering)
        db_name (str, optional) Defaults to "turbit".

    Returns:
        turbine data (list[dict])
    """

    logging.info("Connecting to MongoDB")

    MongoDB = DBConnection(mongo_user, mongo_passwd)

    start = dt.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    end = dt.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

    query_definition = {
        "turbine_id": turbine_id,
        "dat/zeit": {"$gte": start, "$lt": end},
    }

    # Ignore _id field in return
    projection = {"_id": False}

    query_results = MongoDB.find(
        query=query_definition,
        collection="turbine",
        db_name=db_name,
        projection=projection,
    )

    query_results = list(query_results)

    return list(query_results)
