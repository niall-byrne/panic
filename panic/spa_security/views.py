"""Security App Views"""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


class CSRFview(APIView):

  @method_decorator(ensure_csrf_cookie)
  def get(self, request):
    """Returns a 204, and sets the CSRF Cookie."""
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view([
    'CONNECT',
    'DELETE',
    'GET',
    'HEAD',
    'OPTIONS',
    'POST',
    'PATCH',
    'PUT',
    'TRACE',
])
def csrf_error(request, reason=""):  # pylint: disable=W0613
  """Returns a 403 with a custom error message."""
  return Response(
      {"error": "Refresh csrf and try again."},
      status=status.HTTP_403_FORBIDDEN,
  )
