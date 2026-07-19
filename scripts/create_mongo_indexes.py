# """
# Creates MongoDB indexes for faster queries. Run once after initial setup:
#     python scripts/create_mongo_indexes.py
# """
# import os
# import sys

# import django

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agroprice.settings.development")
# django.setup()

# from db.connection import get_db  # noqa: E402


# def run():
#     db = get_db()

#     db["crops"].create_index("name", unique=True)
#     db["crops"].create_index("category")

#     db["pricehistory"].create_index([("crop_name", 1), ("date", -1)])
#     db["pricehistory"].create_index("market")

#     db["users"].create_index("auth_user_id", unique=True)

#     print("MongoDB indexes created successfully.")


# if __name__ == "__main__":
#     run()



"""
Create MongoDB indexes for AgroPrice.

Run:
    python scripts/create_mongo_indexes.py

This script is safe to run multiple times.
It checks whether indexes already exist before creating them.
"""

import os
import sys

import django
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import PyMongoError

# Django Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "agroprice.settings.development"
)

django.setup()

from db.connection import get_db  # noqa: E402


# Helper Function
def create_index_if_not_exists(collection, keys, **kwargs):
    """
    Create MongoDB index only if it does not already exist.
    """

    existing_indexes = collection.index_information()

    if isinstance(keys, str):
        index_name = f"{keys}_1"
        key_definition = [(keys, ASCENDING)]
    else:
        key_definition = keys
        index_name = "_".join(
            f"{field}_{direction}"
            for field, direction in keys
        )

    if index_name in existing_indexes:
        print(f"✓ Index already exists : {collection.name}.{index_name}")
        return

    collection.create_index(key_definition, **kwargs)

    print(f"✓ Created index : {collection.name}.{index_name}")


def run():

    db = get_db()

    print("\n========================================")
    print(" AgroPrice MongoDB Index Creation")
    print("========================================\n")

    try:
        # Crops Collection
        create_index_if_not_exists(
            db["crops"],
            "name",
            unique=True
        )

        create_index_if_not_exists(
            db["crops"],
            "category"
        )

        
        # Price History Collection

        create_index_if_not_exists(
            db["pricehistory"],
            [
                ("crop_name", ASCENDING),
                ("date", DESCENDING)
            ]
        )

        create_index_if_not_exists(
            db["pricehistory"],
            "market"
        )

    
        # Users Collection
        create_index_if_not_exists(
            db["users"],
            "auth_user_id",
            unique=True
        )

        print("\n✅ All MongoDB indexes are ready.")

    except PyMongoError as error:

        print("\n❌ MongoDB Index Creation Failed")
        print(error)


# Entry Point

if __name__ == "__main__":
    run()