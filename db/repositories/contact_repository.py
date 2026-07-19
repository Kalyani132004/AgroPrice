"""ContactMessageRepository — MongoDB access for the `contact_messages` collection."""
from db.base_repository import BaseRepository


class ContactMessageRepository(BaseRepository):
    collection_name = "contact_messages"

    def recent(self, limit: int = 50) -> list:
        return self.find({}, sort=[("submitted_at", -1)], limit=limit)

    def unread_count(self) -> int:
        return self.count({"is_read": False})

    def mark_as_read(self, message_id: str) -> bool:
        return self.update_one(message_id, {"is_read": True})
