"""CSRF Token Validation"""

from rest_framework.authentication import CSRFCheck
from rest_framework.permissions import BasePermission


class ValidCSRF(BasePermission):
  """Enforces CSRF Checks."""
  message = "Illegal CSRF Token."

  def has_permission(self, request, view):
    return self.enforce_csrf(request)

  @staticmethod
  def enforce_csrf(request):
    """
    Enforce CSRF Validation.
    """
    check = CSRFCheck()
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
      return False
    return True
