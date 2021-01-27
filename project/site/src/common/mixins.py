from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

# 在有任何非get的method的View中必须使用LoginAssert
# 不要使用LoginRedirect 因为redirect会使param丢失


class LoginAssert(LoginRequiredMixin):
    raise_exception = True


class LoginRedirect(LoginRequiredMixin):
    raise_exception = False
    redirect_field_name = "next"

    def get_login_url(self):
        return reverse("web:base:login_view")


class LoginRedirectHome(LoginRequiredMixin):
    def handle_no_permission(self, *args, **kwargs):
        return redirect("web:promotions:home")
