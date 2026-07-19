"""
Profile model — a thin Django-side link between `auth_user` and the extended
MongoDB profile document. Only stores the `role` field relationally (so
Django's permission system / templates can check it fast without a Mongo
round-trip); everything else (farm location, phone, preferred crops) lives
in MongoDB via UserProfileRepository.
"""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = (
        ("farmer", "Farmer"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="farmer")
    mongo_profile_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
