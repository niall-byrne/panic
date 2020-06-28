"""Views for the Appengine App."""

from django.http import HttpResponse
from django.views.generic import View


class WarmUp(View):
  """Handles Requests Related to App Engine's 'warm up' feature.

  `App Engine Warm Up Documentation
  <https://cloud.google.com/appengine/docs/standard/python3/
  configuring-warmup-requests>`__
  """

  def get(self, request, *args, **kwargs):  # pylint: disable=W0613
    """Processes an App Engine Warmup Request.

    :param request: A django request object
    :type request: :class:`django.http.HttpRequest`
    :returns: Status information for App Engine.
    :rtype: :class:`django.http.HttpResponse`
    """

    return HttpResponse('OK', status=200)
