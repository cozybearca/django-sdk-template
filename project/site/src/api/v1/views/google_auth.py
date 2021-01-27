from logging import getLogger

from django.contrib import auth
from django.utils.translation import gettext as _
from django_client_framework import exceptions as e
from django_client_framework import serializers as s
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from src import secrets
from src.common import models as m

LOGGER = getLogger(__name__)


class GoogleSignInAPI(APIView):
    permission_classes = [AllowAny]

    class Serializer(s.Serializer):
        id_token = s.CharField()

    def post(self, request):
        ser = self.Serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        id_token = ser.validated_data["id_token"]
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = verify_oauth2_token(
                id_token, requests.Request(), secrets.GOOGLE_SIGNIN_CLIENT_ID
            )

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise ValueError("Wrong issuer.")

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            LOGGER.debug(f"login as {idinfo=}")
            email_address = idinfo.get("email", None)
            email, _created_email = m.Email.objects.get_or_create(
                address=email_address,
            )
            user, _created = m.User.objects.update_or_create(
                email=email,
                defaults={
                    "first_name": idinfo.get("family_name", ""),
                    "last_name": idinfo.get("given_name", ""),
                },
            )
            if user.is_active:
                auth.login(request, user)
            else:
                raise e.ValidationError(
                    dict(
                        email_address=_(
                            f"The account {email.address} has been disabled."
                        )
                    )
                )
        except ValueError:
            return Response({"success": False})
        else:
            return Response(
                {"success": True, "user": s.UserSerializer(instance=user).data}
            )
