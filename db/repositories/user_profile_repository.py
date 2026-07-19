"""UserProfileRepository — MongoDB access for the `users` (profile) collection.

Extended profile fields live here; core auth (username/password) stays in
Django's `auth_user` table. Linked via `auth_user_id`.
"""
from db.base_repository import BaseRepository


class UserProfileRepository(BaseRepository):
    collection_name = "users"

    def find_by_auth_id(self, auth_user_id: int) -> dict | None:
        return self.find_one({"auth_user_id": auth_user_id})

    def create_profile(self, auth_user_id: int, data: dict) -> str:
        document = {"auth_user_id": auth_user_id, **data}
        return self.insert_one(document)

    def update_by_auth_id(self, auth_user_id: int, updates: dict) -> bool:
        result = self.collection.update_one(
            {"auth_user_id": auth_user_id}, {"$set": updates}
        )
        return result.modified_count > 0

    def delete_by_auth_id(self, auth_user_id: int) -> bool:
        result = self.collection.delete_one({"auth_user_id": auth_user_id})
        return result.deleted_count > 0
