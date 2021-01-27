from django.shortcuts import redirect, render

from .base_view import BaseView


class LoginView(BaseView):
    def get(self, request):
        if request.user.is_authenticated:
            url = request.GET.get("next", None)
            if url:
                return redirect(url)
            else:
                return redirect("/")
        return render(request, "base/views/login_view.html", self.template_context)
