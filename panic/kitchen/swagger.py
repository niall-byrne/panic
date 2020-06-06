"""Tools to support OpenApi Documentation"""

import functools


def openapi_ready(func):
  """Openapi generation needs to be able to call some methods on the viewset
  without a user on the request (or AnonymousUser being on it). drf_yasg sets
  the swagger_fake_view attr on the view when running these methods, so we can
  check for that and call the super method if it's present.
  """

  @functools.wraps(func)
  def wrapped(self, *args, **kwargs):
    if getattr(self, "swagger_fake_view", False):
      # Get this decorated method from the parent class and call it there
      return getattr(super(self.__class__, self), func.__name__)(*args,
                                                                 **kwargs)
    return func(self, *args, **kwargs)

  return wrapped
