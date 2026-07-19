"""Accounts views — Farmer registration/login, Admin login, Profile, Settings."""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import FarmerRegistrationForm, LoginForm, ProfileEditForm
from accounts.services.auth_service import AuthService, AuthServiceError
from core.utils.regex_validators import validate_phone, ValidationError as RegexValidationError


def farmer_register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:farmer_dashboard")

    if request.method == "POST":
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                validate_phone(data["phone"])
                service = AuthService()
                user = service.register_farmer(
                    full_name=data["full_name"],
                    username=data["username"],
                    email=data["email"],
                    phone=data["phone"],
                    farm_location=data["farm_location"],
                    password=data["password"],
                )
                login(request, user)
                messages.success(request, f"Welcome to AgroPrice, {data['full_name']}!")
                return redirect("dashboard:farmer_dashboard")
            except (AuthServiceError, RegexValidationError) as exc:
                messages.error(request, str(exc))
    else:
        form = FarmerRegistrationForm()

    return render(request, "accounts/farmer_register.html", {"form": form})


def farmer_login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:admin_dashboard" if request.user.is_staff else "dashboard:farmer_dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data["username"], password=form.cleaned_data["password"]
            )
            if user is not None and not user.is_staff:
                login(request, user)
                return redirect("dashboard:farmer_dashboard")
            elif user is not None and user.is_staff:
                messages.error(request, "Admins must log in via the Admin Login page.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/farmer_login.html", {"form": form})


def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard:admin_dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data["username"], password=form.cleaned_data["password"]
            )
            if user is not None and user.is_staff:
                login(request, user)
                return redirect("dashboard:admin_dashboard")
            else:
                messages.error(request, "Invalid admin credentials.")
    else:
        form = LoginForm()

    return render(request, "accounts/admin_login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out successfully.")
    return redirect("core:home")


@login_required
def profile_view(request):
    service = AuthService()
    mongo_profile = service.get_mongo_profile(request.user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            preferred = [c.strip() for c in data["preferred_crops"].split(",") if c.strip()]
            service.update_mongo_profile(request.user, {
                "full_name": data["full_name"],
                "phone": data["phone"],
                "farm_location": data["farm_location"],
                "preferred_crops": preferred,
            })
            request.user.first_name = data["full_name"]
            request.user.save(update_fields=["first_name"])
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileEditForm(initial={
            "full_name": mongo_profile.get("full_name", request.user.first_name),
            "phone": mongo_profile.get("phone", ""),
            "farm_location": mongo_profile.get("farm_location", ""),
            "preferred_crops": ", ".join(mongo_profile.get("preferred_crops", [])),
        })

    return render(request, "accounts/profile.html", {"form": form, "mongo_profile": mongo_profile})


@login_required
def settings_view(request):
    return render(request, "accounts/settings.html")
