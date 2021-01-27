from django.shortcuts import render
from src.web.base.views import BaseView


class HomeView(BaseView):
    def get(self, request):
        return render(request, "home/home.html", self.template_context)
