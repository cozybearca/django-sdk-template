from django.conf import settings
from django.urls import include, path
from django.views.generic import RedirectView

app_name = "web"

urlpatterns = [
    path("", include("src.web.home.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=f"{settings.STATIC_URL}/favicon.ico"),
        name="favicon",
    ),
]
