from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # ✅ root now shows dashboard
    path('register/', views.company_signup, name='company_signup'),
    path('add-user/', views.add_user, name='add_user'),
    path('project/', views.project_list, name='project_list'),
    path('project/new/', views.project_create, name='project_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
]
