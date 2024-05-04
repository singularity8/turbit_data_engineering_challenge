"""
Script to load example posts and users from 
JSONPlaceholder API and loads them into MongoDB

@Author: Paul
@Date: 2024-05-04
"""

import logging
import os

import requests
from dotenv import load_dotenv

from db_mongo import DBConnection

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

# Loading variables from .env file
load_dotenv()

# Load Mongo Credentials (from .env file)
mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_passwd = os.getenv("MONGO_INITDB_ROOT_PASSWORD")


def get_example_posts() -> list[dict]:
    """
    Gets Example Posts (+ comments) from JSONPlaceholder API

    Returns:
        collection of posts (list[dict])
    """

    logging.info("Getting Posts")

    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts = response.json()

    logging.info("Getting Post Ids")
    post_ids = [x["id"] for x in posts]
    n_post_ids = len(post_ids)

    logging.info(f"Got {n_post_ids} Post IDs to fetch comments for")

    logging.info("Create Dictionary of Posts")
    posts_collection = {x["id"]: x for x in posts}

    for cnt, post_id in enumerate(post_ids):
        if cnt % 10 == 0:
            logging.info(
                f"Currently at post {cnt} of {n_post_ids} ({cnt/n_post_ids:.0%})"
            )
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
        )
        posts_collection[post_id]["comments"] = response.json()

    logging.info(f"Got {len(posts_collection.values())} example posts")

    return list(posts_collection.values())


def get_example_users() -> list[dict]:
    """
    Gets Example Users from JSONPlaceholder API

    Returns:
        collection of users (list[dict])
    """

    logging.info("Getting Users")
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    users = response.json()

    logging.info(f"Got {len(users)} example users")

    return users


def run_data_loading() -> None:
    """
    Runs pipeline of loading data from JSONPlaceholder API and inserting them into MongoDB
    """

    posts_to_insert = get_example_posts()
    userts_to_insert = get_example_users()

    MongoDB = DBConnection(mongo_user, mongo_passwd)

    MongoDB.insert_into_mongodb("posts", posts_to_insert)
    MongoDB.insert_into_mongodb("users", userts_to_insert)


if __name__ == "__main__":

    run_data_loading()
