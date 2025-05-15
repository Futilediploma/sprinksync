# marketing/views.py
import os
import requests
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import InterestForm
from django.views.generic import FormView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

def landing_page(request):
    form = InterestForm(request.POST or None)
    success = False
    brevo_status = None
    brevo_body = None

    if request.method == 'POST' and form.is_valid():
        # 1️⃣ Save to your database
        interest = form.save()

        # Debugging: Print environment variables related to email
        print("---- DEBUGGING SMTP SETTINGS ----")
        print(f"EMAIL_HOST: {os.getenv('EMAIL_HOST')}")
        print(f"EMAIL_PORT: {os.getenv('EMAIL_PORT')}")
        print(f"EMAIL_HOST_USER: {os.getenv('EMAIL_HOST_USER')}")
        print(f"EMAIL_HOST_PASSWORD: {os.getenv('EMAIL_HOST_PASSWORD')}")
        print(f"DEFAULT_FROM_EMAIL: {os.getenv('DEFAULT_FROM_EMAIL')}")
        print("---------------------------------")

        try:
            # 2️⃣ Send your transactional emails
            print("Sending transactional emails...")
            send_mail(
                'New SprinkSync Interest',
                f"{interest.name or 'Someone'} signed up with {interest.email}.",
                settings.DEFAULT_FROM_EMAIL,
                ['your-team@company.com'],
            )
            print("Notification email sent to team.")

            send_mail(
                'Thanks for signing up!',
                'We’ll be in touch soon with early access details.',
                settings.DEFAULT_FROM_EMAIL,
                [interest.email],
            )
            print("Confirmation email sent to user.")
        except Exception as e:
            print(f"Error sending email: {e}")

        # ─────────────── Add Brevo API call here ───────────────

        # 3️⃣ Define the payload using your actual Brevo attribute key
        payload = {
            'email': interest.email,
            'attributes': {
                'FIRSTNAME': interest.name or ''  # ← use the exact key from your Brevo Attributes settings
            },
            'listIds': [int(os.environ.get('BREVO_LIST_ID', 0))],
            'updateEnabled': True,
        }

        try:
            # 4️⃣ Fire the request to Brevo
            print("Sending data to Brevo...")
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
            brevo_body = resp.text
            print(f"Brevo Status Code: {brevo_status}")
            print(f"Brevo Response Body: {brevo_body}")

            if resp.status_code != 200:
                print(f"Error sending to Brevo: {brevo_body}")

        except Exception as e:
            print(f"Error during Brevo API call: {e}")

        success = True

    return render(request, 'marketing/landing.html', {
        'form': form,
        'success': success,
        'brevo_status': brevo_status,
        'brevo_body': brevo_body,
    })

class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login'

def estimating_page(request):
    return render(request, 'marketing/estimating.html')

def design_page(request):
    return render(request, 'marketing/design.html')

def field_page(request):
    return render(request, 'marketing/field.html')

def project_page(request):
    return render(request, 'marketing/project.html')
