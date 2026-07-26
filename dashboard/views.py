from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from accounts.models import Profile
from core.decorators import admin_required, farmer_required
from dashboard.services.dashboard_service import DashboardService
from db.repositories.contact_repository import ContactMessageRepository
from db.repositories.user_profile_repository import UserProfileRepository
from prices.services.price_service import PriceService
from django.contrib import messages


@farmer_required
def farmer_dashboard_view(request):
    service = DashboardService()
    data = service.farmer_dashboard_data(user=request.user)
    return render(request, "dashboard/farmer_dashboard.html", data)


@admin_required
def admin_dashboard_view(request):
    service = DashboardService()

    data = service.admin_dashboard_data()

    user_repo = UserProfileRepository()
    farmers = user_repo.find({"role": "farmer"})

    data["farmers"] = [
        user_repo.serialize(farmer)
        for farmer in farmers
    ]

    data["total_farmers"] = len(farmers)

    return render(request, "dashboard/admin_dashboard.html", data)


@admin_required
def registered_farmers(request):

    user_repo = UserProfileRepository()

    farmers = user_repo.find({
        "role": "farmer"
    })

    farmers = [
        user_repo.serialize(farmer)
        for farmer in farmers
    ]

    return render(
        request,
        "dashboard/registered_farmers.html",
        {
            "farmers": farmers
        }
    )


# DELETE FARMER
@admin_required
def delete_farmer(request, auth_user_id):

    if request.method == "POST":

        user_repo = UserProfileRepository()

        # First check MongoDB profile
        farmer = user_repo.find_by_auth_id(auth_user_id)

        if not farmer:
            messages.error(request, "Farmer not found.")
            return redirect("dashboard:registered_farmers")


        # Safety check
        if farmer.get("role") != "farmer":
            messages.error(request, "Only farmers can be deleted.")
            return redirect("dashboard:registered_farmers")


        # Delete MongoDB profile
        user_repo.delete_by_auth_id(auth_user_id)


        # Delete Django user only if NOT admin
        user = User.objects.filter(
            id=auth_user_id,
            is_staff=False
        ).first()


        if user:
            user.delete()


        messages.success(
            request,
            "Farmer deleted successfully."
        )


    return redirect("dashboard:registered_farmers")

@admin_required
def reports_view(request):
    price_service = PriceService()
    today_prices = price_service.today_prices()

    user_repo = UserProfileRepository()
    total_farmers = user_repo.count({"role": "farmer"})

    return render(request, "dashboard/reports.html", {
        "today_prices": today_prices,
        "total_farmers": total_farmers,
        "total_records": len(today_prices),
    })


# Contact Messages

@admin_required
def contact_messages_view(request):

    repo = ContactMessageRepository()

    messages_list = repo.recent(limit=100)

    serialized = []

    for msg in messages_list:

        msg = repo.serialize(msg)

        if "submitted_at" in msg:
            try:
                from datetime import datetime

                dt = datetime.fromisoformat(msg["submitted_at"])

                msg["formatted_date"] = dt.strftime("%d %b %Y • %I:%M %p")

            except Exception:
                msg["formatted_date"] = msg["submitted_at"]

        serialized.append(msg)

    return render(
        request,
        "dashboard/contact_messages.html",
        {
            "contact_messages": serialized,
            "unread_count": repo.unread_count(),
        },
    )


@admin_required
def mark_message_read(request, message_id):

    repo = ContactMessageRepository()

    repo.mark_as_read(message_id)

    return redirect("dashboard:contact_messages")


@admin_required
def delete_message(request, message_id):

    repo = ContactMessageRepository()

    repo.delete_one(message_id)

    return redirect("dashboard:contact_messages")