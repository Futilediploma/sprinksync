# marketing/urls.py
from django.urls import path
from . import views
from .views import landing_page, estimating_page, design_page, project_page, field_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('estimating/', views.estimating_page, name='estimating'),
    path('design/', views.design_page, name='design'),
    path('project/', views.project_page, name='project'),
    path('field/', views.field_page, name='field'),


]