from django.urls import path
from .views import auth_index, register_pharmacy, login_pharmacy, logout_pharmacy, reset_password_email, reset_password

urlpatterns = [
    path("", auth_index, name="auth_index"),
    path("register/", register_pharmacy, name="register"),
    path("login/", login_pharmacy, name="login"),
    path("logout/", logout_pharmacy, name="logout"),
    path("reset_password", reset_password_email, name="reset_password"),
    path("reset_password_new_password/<str:token>/<str:email>", reset_password, name="new_password"),

]
