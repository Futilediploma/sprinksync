# marketing/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Interest

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ["name", "email", "company"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name (optional)",
                "class": "border rounded px-3 py-2 w-full"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "required": True,
                "class": "border rounded px-3 py-2 w-full"
            }),
            "company": forms.TextInput(attrs={
                "placeholder": "Company Name",
                "class": "border rounded px-3 py-2 w-full"
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Interest.objects.filter(email=email).exists():
            raise ValidationError("This email has already signed up.")
        return email
