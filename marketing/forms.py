# marketing/forms.py
from django import forms
from .models import Interest

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ["name", "email"]
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
        }