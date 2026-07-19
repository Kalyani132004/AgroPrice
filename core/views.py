"""Core views — public marketing pages (Home, About, Contact) and 404 handler."""
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from core.forms import ContactForm
from db.repositories.contact_repository import ContactMessageRepository
from db.repositories.crop_repository import CropRepository
from db.repositories.price_repository import PriceRepository


def home_view(request):
    crop_repo = CropRepository()
    price_repo = PriceRepository()

    try:
        total_crops = crop_repo.count()
        high_low = price_repo.global_high_low()
        trending = price_repo.most_trending()
    except Exception:
        total_crops, high_low, trending = 0, {}, None

    context = {
        "total_crops": total_crops,
        "highest_price": high_low.get("max_price", 0) if high_low else 0,
        "lowest_price": high_low.get("min_price", 0) if high_low else 0,
        "trending_crop": trending.get("_id") if trending else "—",
    }
    return render(request, "core/home.html", context)


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                ContactMessageRepository().insert_one({
                    "name": data["name"],
                    "email": data["email"],
                    "subject": data["subject"],
                    "message": data["message"],
                    "submitted_at": timezone.now(),
                    "is_read": False,
                })
                messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
            except Exception:  # noqa: BLE001
                messages.error(request, "Something went wrong saving your message. Please try again.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


def error_404_view(request, exception=None):
    return render(request, "core/404.html", status=404)
