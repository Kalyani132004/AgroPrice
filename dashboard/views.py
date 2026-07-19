
from django.shortcuts import render, redirect
from accounts.models import Profile
from core.decorators import admin_required, farmer_required
from dashboard.services.dashboard_service import DashboardService
from db.repositories.contact_repository import ContactMessageRepository
from db.repositories.user_profile_repository import UserProfileRepository
from prices.services.price_service import PriceService


@farmer_required
def farmer_dashboard_view(request):
    service = DashboardService()
    data = service.farmer_dashboard_data(user=request.user)
    return render(request, "dashboard/farmer_dashboard.html", data)


@admin_required
def admin_dashboard_view(request):
    service = DashboardService()

    data = service.admin_dashboard_data()

    # MongoDB farmers data
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

@admin_required
def reports_view(request):
    price_service = PriceService()
    today_prices = price_service.today_prices()

    # MongoDB farmer count
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

# Mark Contact Message as Read
@admin_required
def mark_message_read(request, message_id):

    repo = ContactMessageRepository()

    repo.mark_as_read(message_id)

    return redirect("dashboard:contact_messages")


# Delete Contact Message

@admin_required
def delete_message(request, message_id):

    repo = ContactMessageRepository()

    repo.delete_one(message_id)

    return redirect("dashboard:contact_messages")