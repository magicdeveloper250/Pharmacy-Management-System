from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .utils import get_identifier_type

PharmacyUser = get_user_model()

class PharmacyAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            identifier_type = get_identifier_type(username)
            if identifier_type == "email":
                user = PharmacyUser.objects.get(email=username)
            elif identifier_type == "phone":
                user = PharmacyUser.objects.get(phone_number__iexact=username)
            elif identifier_type == "username":
                user = PharmacyUser.objects.get(username__iexact=username)
            else:
                return None
        except PharmacyUser.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return PharmacyUser.objects.get(pk=user_id)
        except PharmacyUser.DoesNotExist:
            return None
