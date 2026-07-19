from django.contrib.auth.models import User
from django.db import transaction

from accounts.models import Profile
from db.repositories.user_profile_repository import UserProfileRepository


class AuthServiceError(Exception):
    """Raised when registration fails at any stage."""


class AuthService:
    def __init__(self):
        self.profile_repo = UserProfileRepository()

    def register_farmer(self, *, full_name, username, email, phone, farm_location, password) -> User:
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username, email=email, password=password, first_name=full_name
                )
                Profile.objects.create(user=user, role="farmer")

                try:
                    mongo_id = self.profile_repo.create_profile(
                        auth_user_id=user.id,
                        data={
                            "full_name": full_name,
                            "phone": phone,
                            "farm_location": farm_location,
                            "preferred_crops": [],
                            "role": "farmer",
                        },
                    )
                    profile = Profile.objects.get(user=user)
                    profile.mongo_profile_id = mongo_id
                    profile.save(update_fields=["mongo_profile_id"])
                except Exception as mongo_exc:  # noqa: BLE001
                    # Roll back the whole transaction if the Mongo write fails
                    raise AuthServiceError(
                        f"Could not create extended profile in MongoDB: {mongo_exc}"
                    ) from mongo_exc

                return user
        except AuthServiceError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise AuthServiceError(f"Registration failed: {exc}") from exc

    def get_mongo_profile(self, user: User) -> dict:
        try:
            return self.profile_repo.find_by_auth_id(user.id) or {}
        except Exception:  # noqa: BLE001
            return {}

    def update_mongo_profile(self, user: User, updates: dict) -> bool:
        try:
            return self.profile_repo.update_by_auth_id(user.id, updates)
        except Exception:  # noqa: BLE001
            return False
