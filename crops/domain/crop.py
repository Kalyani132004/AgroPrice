""" crop and its basic information. """
from dataclasses import dataclass, field


@dataclass
class Crop:
    name: str
    category: str
    unit: str = "Quintal"      # Quintal, Kg, Tonne
    quality_grades: list = field(default_factory=lambda: ["FAQ", "Grade-A"])
    description: str = ""
    id: str = None

    def to_dict(self) -> dict:
        """Convert this Crop object into a MongoDB-ready dictionary."""
        return {
            "name": self.name,
            "category": self.category,
            "unit": self.unit,
            "quality_grades": self.quality_grades,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Crop":
        """Reconstruct a Crop object from a MongoDB document."""
        return cls(
            id=str(data.get("_id") or data.get("id") or ""),
            name=data.get("name", ""),
            category=data.get("category", ""),
            unit=data.get("unit", "Quintal"),
            quality_grades=data.get("quality_grades", []),
            description=data.get("description", ""),
        )

    def __str__(self):
        return f"{self.name} ({self.category}) — priced per {self.unit}"
