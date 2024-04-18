# custom_backend.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the user exists with the given username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        # Check if the user is 'admin' and if the source IP is allowed
        if user.username == 'admin' and request.META.get('REMOTE_ADDR') != '0.0.0.0':
            raise PermissionDenied("Access denied")
        else:
            return super().authenticate(request, username=username, password=password, **kwargs)
