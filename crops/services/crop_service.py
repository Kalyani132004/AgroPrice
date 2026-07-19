""" Handles crop-related business logic and manages crop operations. """
from crops.domain.crop import Crop
from core.utils.regex_validators import validate_crop_name, ValidationError
from db.base_repository import RepositoryError
from db.repositories.crop_repository import CropRepository


class CropService:
    def __init__(self):
        self.repo = CropRepository()

    def list_all(self) -> list:
        docs = self.repo.find({}, sort=[("name", 1)])
        return [Crop.from_dict(d) for d in docs]

    def get_by_id(self, crop_id: str) -> Crop | None:
        doc = self.repo.find_by_id(crop_id)
        return Crop.from_dict(doc) if doc else None

    def get_by_name(self, name: str) -> Crop | None:
        doc = self.repo.find_by_name(name)
        return Crop.from_dict(doc) if doc else None

    def search(self, query: str) -> list:
        docs = self.repo.search(query)
        return [Crop.from_dict(d) for d in docs]

    def add_crop(self, name: str, category: str, unit: str, quality_grades: list, description: str = "") -> str:
        try:
            clean_name = validate_crop_name(name)
        except ValidationError as exc:
            raise ValidationError(str(exc)) from exc

        if self.repo.find_by_name(clean_name):
            raise ValidationError(f"Crop '{clean_name}' already exists.")

        crop = Crop(name=clean_name, category=category, unit=unit, quality_grades=quality_grades, description=description)
        try:
            return self.repo.insert_one(crop.to_dict())
        except RepositoryError as exc:
            raise ValidationError(f"Could not save crop: {exc}") from exc

    def update_crop(self, crop_id: str, **updates) -> bool:
        if "name" in updates:
            updates["name"] = validate_crop_name(updates["name"])
        try:
            return self.repo.update_one(crop_id, updates)
        except RepositoryError as exc:
            raise ValidationError(str(exc)) from exc

    def delete_crop(self, crop_id: str) -> bool:
        try:
            return self.repo.delete_one(crop_id)
        except RepositoryError as exc:
            raise ValidationError(str(exc)) from exc

    def category_breakdown(self) -> list:
        return self.repo.category_counts()

    def total_count(self) -> int:
        return self.repo.count()
