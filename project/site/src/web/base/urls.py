from django.urls import path

from . import views as v

app_name = "base"


urlpatterns = [
    path("login", v.LoginView.as_view(), name="login_view"),
]
