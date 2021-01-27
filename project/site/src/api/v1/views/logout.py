from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView


class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response(True)
