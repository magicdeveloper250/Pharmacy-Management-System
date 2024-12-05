from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .utils import get_identifier_type


User = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            identifier_type = get_identifier_type(username)
            if identifier_type == "email":
                user = User.objects.get(email=username)
            elif identifier_type == "phone":
                user = User.objects.get(phone_number__iexact=username)
            elif identifier_type == "username":
                user = User.objects.get(username__iexact=username)
            else:
                return None
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
