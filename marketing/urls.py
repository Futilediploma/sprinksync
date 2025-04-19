# marketing/urls.py
from django.urls import path
from . import views
from .views import landing_page, estimating_page, design_page, project_page, field_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('estimating/', views.estimating_page, name='estimating'),
    path('design/', views.design_page, name='design'),

]