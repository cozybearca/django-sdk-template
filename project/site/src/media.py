from django.http.response import HttpResponse, HttpResponseNotFound
from django.views import View

from .common.db_file_storage import DatabaseFileStorage


class Media(View):
    def get(self, request, path, **kwargs):
        fs = DatabaseFileStorage()
        if fs.exists(path):
            with fs.open(path, "rb") as file:
                return HttpResponse(content=file.read())
        else:
            return HttpResponseNotFound()
