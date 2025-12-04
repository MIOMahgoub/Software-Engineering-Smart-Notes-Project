from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect   # ← ADD THIS

urlpatterns = [
    # Redirect root URL "/" → login page
    path("", lambda request: redirect("login"), name="root"),   # ← ADD THIS

    path("admin/", admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("uploads/", include("uploads.urls")),
    path('accounts/', include('accounts.urls')),
    path("analytics/", include("analytics.urls")),
]
