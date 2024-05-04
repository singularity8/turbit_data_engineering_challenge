"""
Script to load turbine data from csv files (defined in .env) 
and loads them into MongoDB after minor transformations

@Author: Paul
@Date: 2024-05-04
"""

import json
import logging
import os
from datetime import datetime as dt

import pandas as pd
from dotenv import load_dotenv

from db_mongo import DBConnection

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

# Loading variables from .env file
load_dotenv()

# Load Mongo Credentials (from .env file)
mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_passwd = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
csv_urls = json.loads(os.getenv("TURBIT_CSV_URLS"))


def parse_turbine_data(csv_url: str) -> pd.DataFrame:
    """
    Loads csv data via provided URL and returns a parsed and transformed dataframe

    Args:
        csv_url (str)

    Returns:
        df_turbine (pd.DataFrame)
    """

    df_turbine = pd.read_csv(csv_url, delimiter=";", skiprows=range(1, 2), decimal=",")

    # Stripping whitespace from columns and lowercase
    df_turbine.columns = [
        x.strip().replace(" ", "_").lower() for x in df_turbine.columns
    ]

    # Convert dat/zeit column to datetime
    df_turbine["dat/zeit"] = df_turbine["dat/zeit"].apply(
        lambda r: dt.strptime(r, "%d.%m.%Y, %H:%M")
    )

    # Parse URL to get Turbine ID (assuming name of csv file is in format ..../Turbine{ID}.csv)
    turbine_id = csv_url.split(".csv")[0].split("/Turbine")[-1]

    # Add Turbine ID as column to beginning of df
    df_turbine.insert(0, "turbine_id", turbine_id)

    return df_turbine


def run_data_loading() -> None:
    """
    Runs pipeline of loading data from CSVs and inserting them into MongoDB
    """

    turbine_dfs = []

    for csv_url in csv_urls:
        logging.info(f"Loading data from: {csv_url}")

        turbine_dfs.append(parse_turbine_data(csv_url))

    df_turbine = pd.concat(turbine_dfs).reset_index(drop=True)

    MongoDB = DBConnection(mongo_user, mongo_passwd)

    MongoDB.insert_into_mongodb("turbine", df_turbine.to_dict("records"))


if __name__ == "__main__":

    run_data_loading()
