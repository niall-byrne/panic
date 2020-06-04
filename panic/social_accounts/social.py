"""Social Views for the Social Accounts App"""

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView


class FacebookLogin(SocialLoginView):
  authentication_classes = ()
  permission_classes = ()
  adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
  authentication_classes = ()
  permission_classes = ()
  adapter_class = GoogleOAuth2Adapter


class FacebookConnect(SocialConnectView):
  authentication_classes = ()
  permission_classes = ()
  adapter_class = FacebookOAuth2Adapter


class GoogleConnect(SocialConnectView):
  authentication_classes = ()
  permission_classes = ()
  adapter_class = GoogleOAuth2Adapter
