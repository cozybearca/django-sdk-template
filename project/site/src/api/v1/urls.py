import django_client_framework.api.urls
from django.urls import path

from . import views as v

app_name = "v1"

urlpatterns = [
    path("logout", v.Logout.as_view(), name="logout"),
    path("login/google_auth", v.GoogleSignInAPI.as_view(), name="login_with_google"),
] + django_client_framework.api.urls.urlpatterns
