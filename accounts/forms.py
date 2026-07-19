"""Forms for Farmer/Admin registration, login, and profile editing."""
from django import forms
from django.contrib.auth.models import User

INPUT_CLASS = "form-control"


class FarmerRegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Full Name"})
    )
    username = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Username"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "Email Address"})
    )
    phone = forms.CharField(
        max_length=15, widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Mobile Number"})
    )
    farm_location = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Farm Location (Village, District)"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Confirm Password"})
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") and cleaned.get("confirm_password"):
            if cleaned["password"] != cleaned["confirm_password"]:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Username", "autofocus": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, "placeholder": "Password"})
    )


class ProfileEditForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    farm_location = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    preferred_crops = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "e.g. Wheat, Rice, Onion"}),
    )
