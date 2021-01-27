from logging import getLogger

from django.conf import settings
from django.urls import resolve
from django.utils.functional import cached_property
from django.views import generic
from src.common import models as m

LOG = getLogger(__name__)


class BaseView(generic.View):
    @cached_property
    def template_context(self):
        context = {}
        request_path = resolve(self.request.path)
        request_path_namespaces = request_path.app_names[1:] + [request_path.url_name]
        context.update(
            {
                "app_js_url": (
                    "webpack/" + resolve(self.request.path).namespaces[1] + ".js"
                ),
                "request_path_namespaces": request_path_namespaces,
                "request_path_namespaces_css": " ".join(request_path_namespaces),
            }
        )
        return context
