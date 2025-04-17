# marketing/views.py

import os, requests
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
        interest = form.save()

        # send your transactional emails as before...
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

        # Brevo API call
        api_url = 'https://api.brevo.com/v3/contacts'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api-key': os.environ.get('BREVO_API_KEY',''),
        }
        payload = {
            'email': interest.email,
            'attributes': {'FNAME': interest.name or ''},
            'listIds': [int(os.environ.get('BREVO_LIST_ID', 0))],
            'updateEnabled': True,
        }

        resp = requests.post(api_url, headers=headers, json=payload)
        brevo_status = resp.status_code
        brevo_body   = resp.text

        success = True

    return render(request, 'marketing/landing.html', {
        'form': form,
        'success': success,
        'brevo_status': brevo_status,
        'brevo_body': brevo_body,
    })
