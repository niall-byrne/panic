"""Security App Views"""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CSRFview(APIView):

  @method_decorator(ensure_csrf_cookie)
  def get(self, request):
    """Returns a 204, and set the CSRF Header."""
    return Response(status=status.HTTP_204_NO_CONTENT)
