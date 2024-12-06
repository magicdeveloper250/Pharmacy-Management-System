from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import *
from .models import User, PasswordResetToken
from django.db import IntegrityError
import base64


def auth_index(request):
    return render(request, "login.html")


def register_user(request):
    errors = {}
    if request.method == "POST":
        email = request.POST.get("email", "")
        username = request.POST.get("username", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        phone_number = request.POST.get("phone_number", "")
        role= request.POST.get("role")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        profile_picture = request.FILES.get("profile_picture", "")
        validation_results = [
            validate_first_name(first_name),
            validate_last_name(last_name),
            validate_email(email),
            validate_username(username),
            validate_phone_number(phone_number),
            validate_password(password),
            validate_confirm_password(password, confirm_password),
            validate_profile_picture(profile_picture),
        ]
        errors = filter_validation_errors(validation_results)

        if not errors:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    profile_picture=profile_picture,
                    phone_number=phone_number,
                    password=password,
                    role=role,
                )
                user.save()
                messages.success(request, "New user account created successfully")
                return redirect("login")
            except IntegrityError as e:
                error_message = str(e)
                if "authentication_user_email_key" in error_message:
                    errors["email"] = "Email already taken."
                elif "authentication_user_username_key" in error_message:
                    errors["username"] = "username already taken."
                elif "authentication_user_phone_number_key" in error_message:
                    errors["phone_number"] = "Phone number already taken."

            except Exception as e:
                messages.error(request, str(e))

    return render(request, "register.html", context={"errors": errors})


def login_user(request):
    if request.method == "POST":
        username = request.POST["identifier"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User logged successfully")
            return redirect("admin_dash")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "login.html")

@login_required
def logout_user(request):
    logout(request)
    return redirect("login")

def reset_password_email(request):
    if request.method=="POST":
        messages.success(request, "We've password reset instruction to the provided email address.")
        rst_token=None
        raw_token, hashed_token=generate_random_token()
        try:
            email= request.POST.get("email")
            user= User.objects.get(email= email)
            # chck if there are no current active and non expired token in database.
            rst_token=  PasswordResetToken.objects.get(user=user)
            if  rst_token.token_expired() or not rst_token.is_active:
                rst_token.delete()
                rst_token= PasswordResetToken.objects.create(user=user, token= hashed_token)
                rst_token.save()
        except User.DoesNotExist:
            return render(request, "reset_password_email.html")
        except PasswordResetToken.DoesNotExist:
            rst_token= PasswordResetToken.objects.create(user=user, token=hashed_token)
            rst_token.save()
        
        # encode token before sent
        token_bytes= raw_token.encode("utf-8")
        base64_bytes= base64.b64encode(token_bytes)
        base64_token=base64_bytes.decode("utf-8")

        # encode user email 
        email_bytes= user.email.encode("utf-8")
        email_base64_bytes= base64.b64encode(email_bytes)
        base64_email=email_base64_bytes.decode("utf-8")
        token = request.build_absolute_uri().replace(
        "reset_password", "reset_password_new_password/"
    ) + base64_token + f"/{base64_email}"
        send_email_in_thread(user.email,token )
           
    return render(request, "reset_password_email.html")


def reset_password(request, token, email):
    
    try:
        decoded_token= base64.b64decode(token).decode("utf-8")
        decoded_email= base64.b64decode(email).decode("utf-8")
        errors= {}
        user= User.objects.get(email= decoded_email)
        rst_token= PasswordResetToken.objects.get(user=user)
        if not verify_token(decoded_token, rst_token.token):
            messages.info(request, "Invalid token or token expired")
            return redirect("reset_password")
        if  rst_token.token_expired() or not rst_token.is_active:
            messages.info(request, "Invalid token or token expired")
            return redirect("reset_password")
        if request.method=="POST":
            new_password= request.POST.get("new_password")
            validation_errors=validate_password(new_password)
            if not validation_errors[0]:
                errors={"password":validation_errors[1]}
            if not errors:
                user= rst_token.user
                user.set_password(new_password)
                user.save()
                rst_token.is_active=False
                rst_token.save()
                messages.success(request, "Your password changed successfully")
                return redirect("login")
    except PasswordResetToken.DoesNotExist:
        messages.info(request, "Invalid token or token is expired")
    except User.DoesNotExist:
        messages.info(request, "Invalid token or token is expired")
    except Exception as e:
        messages.info(request, "Invalid token or token is expired")

    
    return render(request, "reset_password_new_password.html", context={"token":token,"email":email,  "errors":errors})

 
        
        
    
