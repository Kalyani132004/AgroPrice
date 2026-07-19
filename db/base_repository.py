""" common CRUD and database operations for all MongoDB repositories. """
from bson import ObjectId
from bson.errors import InvalidId

from db.connection import get_collection


class RepositoryError(Exception):
    """Raised when a repository operation fails"""


class BaseRepository:
    collection_name: str = None 

    def __init__(self):
        if not self.collection_name:
            raise NotImplementedError("Subclasses must set `collection_name`.")
        self.collection = get_collection(self.collection_name)

    # Create
    def insert_one(self, document: dict) -> str:
        try:
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as exc: 
            raise RepositoryError(f"Insert failed: {exc}") from exc

    def insert_many(self, documents: list) -> list:
        try:
            result = self.collection.insert_many(documents)
            return [str(_id) for _id in result.inserted_ids]
        except Exception as exc: 
            raise RepositoryError(f"Bulk insert failed: {exc}") from exc

    # Read
    def find_by_id(self, doc_id: str) -> dict | None:
        try:
            return self.collection.find_one({"_id": ObjectId(doc_id)})
        except (InvalidId, Exception) as exc: 
            raise RepositoryError(f"Invalid id or read failure: {exc}") from exc

    def find_one(self, query: dict) -> dict | None:
        return self.collection.find_one(query)

    def find(self, query: dict = None, limit: int = 0, sort: list = None) -> list:
        query = query or {}
        cursor = self.collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    def count(self, query: dict = None) -> int:
        return self.collection.count_documents(query or {})

    # Update
    def update_one(self, doc_id: str, updates: dict) -> bool:
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(doc_id)}, {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as exc: 
            raise RepositoryError(f"Update failed: {exc}") from exc

    # Delete
    def delete_one(self, doc_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as exc:
            raise RepositoryError(f"Delete failed: {exc}") from exc

    # Aggrigation
    def aggregate(self, pipeline: list) -> list:
        try:
            return list(self.collection.aggregate(pipeline))
        except Exception as exc:
            raise RepositoryError(f"Aggregation failed: {exc}") from exc

    @staticmethod
    def serialize(document: dict) -> dict:
        """Convert Mongo's ObjectId + datetime fields into JSON-safe values."""
        if not document:
            return document
        doc = dict(document)
        if "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        for key, value in doc.items():
            if hasattr(value, "isoformat"):
                doc[key] = value.isoformat()
        return doc
