from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
class PharmacyManager(BaseUserManager):
    def create_user(self, email, username, pharmacy_name, phone_number, password=None,  profile_picture= None):
        if not email:
            raise ValueError("Pharmacy must have an email address")
        if not username:
            raise ValueError("Pharmacy must have a username")
        if not pharmacy_name:
            raise ValueError("Pharmacy must have a name")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            pharmacy_name=pharmacy_name,
            phone_number=phone_number,
            profile_picture=profile_picture
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, pharmacy_name, phone_number, password=None):
        user = self.create_user(
            email,
            username=username,
            pharmacy_name=pharmacy_name,
            phone_number=phone_number,
            password=password
        )
        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Pharmacy(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    pharmacy_name = models.CharField(max_length=100)
    profile_picture = models.FileField(upload_to="pharmacies/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "pharmacy_name", "phone_number"]

    objects = PharmacyManager()

    def __str__(self):
        return self.pharmacy_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
class PasswordResetToken(models.Model):
    user= models.ForeignKey(Pharmacy, on_delete=models.CASCADE, null=False)
    token= models.TextField(  null=False)
    is_active= models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def token_expired(self)->bool:
        expiration_time= self.date_created + timedelta(minutes=settings.RESET_TOKEN_TIMEOUT)
        return timezone.now()>expiration_time
    
    def __str__(self) -> str:
        return str(self.token)