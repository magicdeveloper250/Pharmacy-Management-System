from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        username,
        password,
        email,
        phone_number,
        role=None,
        profile_picture=None,
    ):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            profile_picture=profile_picture,
        )
        if role == "buyer" or role==None:
            user.is_buyer = True
        elif role == "renter":
            user.is_renter = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        first_name,
        last_name,
        username,
        password,
        email,
        phone_number,
        profile_picture=None,
    ):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            profile_picture=profile_picture,
        )
        user.is_admin = True
        user.set_password(password)
        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=50, unique=True)
    profile_picture = models.FileField(upload_to="profiles/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_renter = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number"]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class PasswordResetToken(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    token= models.TextField(  null=False)
    is_active= models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def token_expired(self)->bool:
        expiration_time= self.date_created + timedelta(minutes=settings.RESET_TOKEN_TIMEOUT)
        return timezone.now()>expiration_time
    
    def __str__(self) -> str:
        return str(self.token)