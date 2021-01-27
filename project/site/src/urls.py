from django.conf import settings
from django.urls import include, path, re_path

from .media import Media

urlpatterns = [
    path("", include("src.web.urls")),
    path("api/", include("src.api.urls")),
    re_path(r"^media/(?P<path>.*)$", Media.as_view(), name="media"),
    # re_path(
    #     r"^static/(?P<path>.*)$",
    #     serve,
    #     {
    #         "document_root": settings.STATIC_ROOT,
    #     },
    #     "serve-collectstatic",
    # ),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.ENABLE_DJANGO_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
