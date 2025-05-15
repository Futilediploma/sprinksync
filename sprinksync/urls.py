
from django.contrib import admin
from django.urls import path, include
from marketing.views import SignUpView, DashboardView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core marketing flows
    path('', include('marketing.urls')),

    # Authentication
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/',
         auth_views.LoginView.as_view(
           template_name='registration/login.html'
         ),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),

    # Protected dashboard
    path('dashboard/',
         DashboardView.as_view(),
         name='dashboard'),
]
