"""
Defines DBConnection class to connect to MongoDB.
Exposes two methods to the user:
- find (runs queries on given db and collection and returns results)
- insert_into_mongodb (inserts given set of data into given collection and db)

@Author: Paul
@Date: 2024-05-04
"""

import logging

from pymongo import MongoClient

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


class DBConnection:

    def __init__(self, db_user: str, db_passwd: str) -> None:

        self.db_user = db_user
        self.db_passwd = db_passwd

        self.conn = self.connect(db_user, db_passwd)

    def connect(self, db_user: str, db_passwd: str):
        return MongoClient(
            "localhost", username=db_user, password=db_passwd, port=27017
        )

    def find(
        self, query: dict, collection: str, db_name="turbit", projection=None
    ) -> list[dict]:
        """
        Executes query on MongoDB collection and db and returns results

        Args:
            Query definition (dict)
            Mongo DB collection name (str)
            Mongo DB database name (str) Defaults to "turbit"

        Returns:
            Query results (list[dict])
        """

        db_mongo = self.conn[db_name]
        collection_mongo = db_mongo[collection]

        query_results = collection_mongo.find(query, projection=projection)

        return list(query_results)

    def insert_into_mongodb(
        self, collection: str, data_to_insert: list[dict], db_name="turbit"
    ) -> None:
        """
        Inserts data into given MongoDB collection

        Args:
            Mongo DB collection name (str)
            Data to Insert (list[dict])
            Mongo DB database name (str) Defaults to "turbit"
        """

        db_mongo = self.conn[db_name]
        collection_mongo = db_mongo[collection]

        logging.info(
            f"Inserting {len(data_to_insert)} entries into DB: {db_name} and collection: {collection}"
        )

        object_ids = collection_mongo.insert_many(data_to_insert)

        # Making sure we inserted the same amount of entries as intended
        assert len(object_ids.inserted_ids) == len(data_to_insert)

        logging.info(f"Successfully inserted {len(object_ids.inserted_ids)} entries")
