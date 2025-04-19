# marketing/views.py
import os
import requests
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import InterestForm

def landing_page(request):
    form = InterestForm(request.POST or None)
    success = False
    brevo_status = None
    brevo_body = None

    if request.method == 'POST' and form.is_valid():
        # 1️⃣ Save to your database
        interest = form.save()

        # 2️⃣ Send your transactional emails
        send_mail(
            'New SprinkSync Interest',
            f"{interest.name or 'Someone'} signed up with {interest.email}.",
            settings.DEFAULT_FROM_EMAIL,
            ['your-team@company.com'],
        )
        send_mail(
            'Thanks for signing up!',
            'We’ll be in touch soon with early access details.',
            settings.DEFAULT_FROM_EMAIL,
            [interest.email],
        )

        # ─────────────── Add Brevo API call here ───────────────

        # 3️⃣ Define the payload using your actual Brevo attribute key
        payload = {
            'email': interest.email,
            'attributes': {
                'FIRSTNAME': interest.name or ''    # ← use the exact key from your Brevo Attributes settings
            },
            'listIds': [int(os.environ.get('BREVO_LIST_ID', 0))],
            'updateEnabled': True,
        }

        # 4️⃣ Fire the request to Brevo
        resp = requests.post(
            'https://api.brevo.com/v3/contacts',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'api-key': os.environ.get('BREVO_API_KEY', ''),
            },
            json=payload
        )

        # 5️⃣ Capture the response for debugging or display
        brevo_status = resp.status_code
        brevo_body   = resp.text

        success = True

    return render(request, 'marketing/landing.html', {
        'form': form,
        'success': success,
        'brevo_status': brevo_status,
        'brevo_body': brevo_body,
    })


def estimating_page(request):
    return render(request, 'marketing/estimating.html')

def design_page(request):
    return render(request, 'marketing/design.html')

def field_page(request):
    return render(request, 'marketing/field.html')

def project_page(request):
    return render(request, 'marketing/project.html')