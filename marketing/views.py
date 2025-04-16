# marketing/views.py
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import InterestForm


def landing_page(request):
    form = InterestForm(request.POST or None)
    success = False

    if request.method == 'POST' and form.is_valid():
        interest = form.save()
        # Notify admin
        send_mail(
            'New SprinkSync Interest',
            f"{interest.name or 'Someone'} signed up with {interest.email}.",
            DEFAULT_FROM_EMAIL,
            ['your-team@company.com'],
        )
        # Optional: Confirmation to user
        send_mail(
            'Thanks for signing up!',
            'We’ll be in touch soon with early access details.',
            DEFAULT_FROM_EMAIL,
            [interest.email],
        )
        success = True
    
    return render(request, 'marketing/landing.html', {'form': form, 'success': success})