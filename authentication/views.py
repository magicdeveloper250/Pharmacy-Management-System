from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .utils import *
from .models import Pharmacy, PasswordResetToken
from django.db import IntegrityError
import base64
from django.contrib.auth.decorators import login_not_required

@login_not_required
def auth_index(request):
    return render(request, "login.html")

@login_not_required
def register_pharmacy(request):
    errors = {}
    if request.method == "POST":
        email = request.POST.get("email", "")
        username = request.POST.get("username", "")
        pharmacy_name = request.POST.get("pharmacy_name", "")
        phone_number = request.POST.get("phone_number", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        profile_picture = request.FILES.get("profile_picture", None)

        validation_results = [
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
                pharmacy = Pharmacy.objects.create_user(
                    username=username,
                    email=email,
                    pharmacy_name=pharmacy_name,
                    profile_picture=profile_picture,
                    phone_number=phone_number,
                    password=password,
                )
                pharmacy.save()
                messages.success(request, "New pharmacy account created successfully")
                return redirect("login")
            except IntegrityError as e:
                error_message = str(e)
                if "authentication_pharmacy_email_key" in error_message:
                    errors["email"] = "Email already taken."
                elif "authentication_pharmacy_username_key" in error_message:
                    errors["username"] = "Username already taken."
                elif "authentication_pharmacy_phone_number_key" in error_message:
                    errors["phone_number"] = "Phone number already taken."
            except Exception as e:
                messages.error(request, str(e))

    return render(request, "register.html", context={"errors": errors})

@login_not_required
def login_pharmacy(request):
    next_page = request.GET.get('next', 'dashboard')   
    
    if request.method == "POST":
        username = request.POST.get("identifier")
        password = request.POST.get("password")
        pharmacy = authenticate(username=username, password=password)
        if pharmacy:
            login(request, pharmacy)
            messages.success(request, f"Welcome back, {pharmacy.username}!")
            return redirect(next_page)
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, "login.html", context={"next": next_page})

def logout_pharmacy(request):
    messages.info(request, f"{request.user.username} logged out")
    logout(request)
    return redirect('index')

@login_not_required
def reset_password_email(request):
    if request.method == "POST":
        messages.success(request, "We've sent password reset instructions to the provided email address.")
        raw_token, hashed_token = generate_random_token()
        try:
            email = request.POST.get("email")
            pharmacy = Pharmacy.objects.get(email=email)
            rst_token, created = PasswordResetToken.objects.get_or_create(user=pharmacy, defaults={"token": hashed_token})
            if not created and (rst_token.token_expired() or not rst_token.is_active):
                rst_token.token = hashed_token
                rst_token.save()

            # Encode token and email for URL
            base64_token = base64.b64encode(raw_token.encode("utf-8")).decode("utf-8")
            base64_email = base64.b64encode(pharmacy.email.encode("utf-8")).decode("utf-8")
            reset_url = request.build_absolute_uri().replace(
                "reset_password", f"reset_password_new_password/{base64_token}/{base64_email}"
            )
            send_email_in_thread(pharmacy.email, reset_url)
        except Pharmacy.DoesNotExist:
            pass

    return render(request, "reset_password_email.html")

@login_not_required
def reset_password(request, token, email):
    try:
        decoded_token = base64.b64decode(token).decode("utf-8")
        decoded_email = base64.b64decode(email).decode("utf-8")
        errors = {}
        pharmacy = Pharmacy.objects.get(email=decoded_email)
        rst_token = PasswordResetToken.objects.get(user=pharmacy)
        
        if not verify_token(decoded_token, rst_token.token) or rst_token.token_expired() or not rst_token.is_active:
            messages.info(request, "Invalid token or token expired")
            return redirect("reset_password")

        if request.method == "POST":
            new_password = request.POST.get("new_password")
            validation_errors = validate_password(new_password)
            if not validation_errors[0]:
                errors = {"password": validation_errors[1]}
            if not errors:
                pharmacy.set_password(new_password)
                pharmacy.save()
                rst_token.is_active = False
                rst_token.save()
                messages.success(request, "Your password was changed successfully")
                return redirect("login")
    except (PasswordResetToken.DoesNotExist, Pharmacy.DoesNotExist):
        messages.info(request, "Invalid token or token expired")
    except Exception as e:
        messages.error(request, "An unexpected error occurred")

    return render(request, "reset_password_new_password.html", context={"token": token, "email": email, "errors": errors})
