from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json
from authentication.models import PharmacyUser, Pharmacy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Permission
from ..decorators import (
    pharmacy_permission_required,
    admin_required,
    superadmin_required,
    staff_required
)
@admin_required
@pharmacy_permission_required('authentication.manage_users') 
def users(request):
    permissions = [
        ("view_sales", "Can view pharmacy sales"),
        ("manage_sales", "Can manage pharmacy sales"),
        ("view_purchases", "Can view pharmacy purchases"),
        ("manage_purchases", "Can manage pharmacy purchases"),
        ("view_prescriptions", "Can view prescriptions"),
        ("manage_prescriptions", "Can manage prescriptions"),
        ("manage_users", "Can manage pharmacy staff"),
        ("view_customers", "Can view pharmacy customers"),
        ("manage_customers", "Can manage pharmacy customers"),
        ("view_reports", "Can view pharmacy reports"),
        ("view_suppliers", "Can view pharmacy suppliers"),
        ("manage_supplers", "Can manage pharmacy suplliers"),
        ("view_medicines", "Can view pharmacy medicines"),
        ("manage_medicines", "Can manage pharmacy medicines"),
        ("view_pharmacy_settings", "Can view pharmacy settings"),
        ("manage_pharmacy_settings", "Can manage pharmacy settings"),
    ]
    return render(request, "users.html",context={'permissions':permissions})

@pharmacy_permission_required('authentication.view_users')
@csrf_exempt
def user_list(request):
    try:
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)

        users = PharmacyUser.objects.select_related('pharmacy')

        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(pharmacy__pharmacy_name__icontains=search_query)
            )

        paginator = Paginator(users, per_page)
        page_obj = paginator.get_page(page_number)

        user_list = [{
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'pharmacy': user.pharmacy.pharmacy_name,
            'pharmacy_id': user.pharmacy.id,
            'phone_number': user.phone_number,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'is_active': user.is_active,
            'is_admin': user.is_admin,
            'is_verified': user.is_verified,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'permissions': [perm.codename for perm in user.user_permissions.all()]
        } for user in page_obj]

        return JsonResponse({
            'status': 'success',
            'data': user_list,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'total_records': paginator.count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
    
@admin_required
@pharmacy_permission_required('authentication.manage_users')
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_user(request):
    print(request.POST)
    try:
        data = json.loads(request.body)
        user = get_object_or_404(PharmacyUser, id=data.get("userId"))
        permissions = data.get('permissions', [])
        if 'email' in data and data['email'] != user.email:
            if PharmacyUser.objects.filter(email=data['email']).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email already exists'
                }, status=400)
            user.email = data['email']

        if 'username' in data and data['username'] != user.username:
            if PharmacyUser.objects.filter(username=data['username']).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username already exists'
                }, status=400)
            user.username = data['username']

        if 'pharmacy_id' in data:
            pharmacy = get_object_or_404(Pharmacy, id=data['pharmacy_id'])
            user.pharmacy = pharmacy

        if 'phone_number' in data:
            user.phone_number = data['phone_number']

        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'is_verified' in data:
            user.is_verified= data['is_verified']

        if 'is_admin' in data:
            user.is_admin = data['is_admin']

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        print(data)

        user.user_permissions.clear()
        if permissions:
            permission_objects = Permission.objects.filter(codename__in=permissions)
            user.user_permissions.set(permission_objects)

        user.save()

        return JsonResponse({
            'status': 'success',
            'message': 'User updated successfully',
            'data': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'pharmacy': user.pharmacy.pharmacy_name,
                'pharmacy_id': user.pharmacy.id,
                'phone_number': user.phone_number,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
                'is_active': user.is_active,
                'is_admin': user.is_admin,
                'is_verified': user.is_verified
            }
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    

@admin_required
@pharmacy_permission_required('authentication.manage_users')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("id")
        user = get_object_or_404(PharmacyUser, id=user_id)
        user.delete()

        return JsonResponse({
            'status': 'success',
            'message': 'User deleted successfully'
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
@admin_required
@pharmacy_permission_required('authentication.view_users')
@login_required
def get_user(request):
    try:
        user_id = request.GET.get('id')
        user = get_object_or_404(PharmacyUser, id=user_id)
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'pharmacy': user.pharmacy.pharmacy_name,
                'pharmacy_id': user.pharmacy.id,
                'phone_number': user.phone_number,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
                'is_active': user.is_active,
                'is_admin': user.is_admin,
                'is_verified': user.is_verified,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None,
                'permissions': [perm.codename for perm in user.user_permissions.all()]
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)