"""
Seed script — populates MongoDB `crops` collection with sample Indian crops.
""" 

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agroprice.settings.development")
django.setup()

from crops.services.crop_service import CropService  # noqa: E402
from core.utils.regex_validators import ValidationError  # noqa: E402

SAMPLE_CROPS = [
    {"name": "Wheat", "category": "Cereal", "unit": "Quintal", "quality_grades": ["FAQ", "Grade-A"], "description": "Staple rabi cereal crop."},
    {"name": "Rice", "category": "Cereal", "unit": "Quintal", "quality_grades": ["FAQ", "Grade-A", "Premium"], "description": "Staple kharif cereal crop."},
    {"name": "Onion", "category": "Vegetable", "unit": "Quintal", "quality_grades": ["Grade-A", "Grade-B"], "description": "Widely traded vegetable crop."},
    {"name": "Tomato", "category": "Vegetable", "unit": "Quintal", "quality_grades": ["Grade-A", "Grade-B"], "description": "Perishable vegetable crop."},
    {"name": "Potato", "category": "Vegetable", "unit": "Quintal", "quality_grades": ["FAQ", "Grade-A"], "description": "Staple tuber crop."},
    {"name": "Soybean", "category": "Oilseed", "unit": "Quintal", "quality_grades": ["FAQ", "Grade-A"], "description": "Major oilseed crop."},
    {"name": "Cotton", "category": "Cash Crop", "unit": "Quintal", "quality_grades": ["Grade-A", "Premium"], "description": "Major cash/fiber crop."},
    {"name": "Sugarcane", "category": "Cash Crop", "unit": "Tonne", "quality_grades": ["FAQ"], "description": "Major cash crop for sugar production."},
    {"name": "Maize", "category": "Cereal", "unit": "Quintal", "quality_grades": ["FAQ", "Grade-A"], "description": "Versatile cereal/fodder crop."},
    {"name": "Groundnut", "category": "Oilseed", "unit": "Quintal", "quality_grades": ["FAQ", "Grade-A"], "description": "Major oilseed crop."},
]


def run():
    service = CropService()
    created, skipped = 0, 0
    for data in SAMPLE_CROPS:
        try:
            service.add_crop(**data)
            created += 1
            print(f"[+] Added crop: {data['name']}")
        except ValidationError as exc:
            skipped += 1
            print(f"[skip] {data['name']}: {exc}")
    print(f"\nDone. Created {created}, skipped {skipped}.")


if __name__ == "__main__":
    run()
