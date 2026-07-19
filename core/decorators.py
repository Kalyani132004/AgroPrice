"""Custom decorators for role-based view protection (Farmer vs Admin)."""
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def admin_required(view_func):
    """Allows access only to staff/admin users; redirects farmers with a message."""
    @wraps(view_func)
    @login_required(login_url="accounts:admin_login")
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You need admin privileges to access that page.")
            return redirect("dashboard:farmer_dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper


def farmer_required(view_func):
    """Allows access only to authenticated non-staff (farmer) users."""
    @wraps(view_func)
    @login_required(login_url="accounts:farmer_login")
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("dashboard:admin_dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper
