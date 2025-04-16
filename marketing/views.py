# marketing/views.py
from django.shortcuts import render
from .forms import InterestForm


def landing_page(request):
    form = InterestForm(request.POST or None)
    success = False

    if request.method == 'POST' and form.is_valid():
        form.save()
        success = True

    return render(request, 'marketing/landing.html', {
        'form': form,
        'success': success,
    })