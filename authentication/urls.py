from django.urls import path
from .views import auth_index, register_user, login_user, logout_user, reset_password_email, reset_password

urlpatterns = [
    path("", auth_index, name="auth_index"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("reset_password", reset_password_email, name="reset_password"),
    path("reset_password_new_password/<str:token>/<str:email>", reset_password, name="new_password"),

]
