from django.urls import path

from . import home

app_name = "home"

urlpatterns = [
    path("", home.HomeView.as_view(), name="home"),
]
