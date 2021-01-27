import uuid
from logging import getLogger

from django.contrib.auth import models as auth
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_client_framework import models as m
from django_client_framework.api import register_api_model
from rest_framework.authtoken.models import Token

LOGGER = getLogger(__name__)


@register_api_model
class User(m.Serializable, auth.AbstractUser):
    @classmethod
    def serializer_class(cls):
        from src.common.serializers import UserSerializer

        return UserSerializer

    @property
    def logged_in(self):
        return self.groups.filter(name="logged_in").exists()

    @cached_property
    def perma_token(self):
        token, _created = Token.objects.get_or_create(user=self)
        return token

    def set_perma_token(self, key):
        Token.objects.filter(user=self).delete()
        return Token.objects.create(user=self, key=key)
