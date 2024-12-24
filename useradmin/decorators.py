from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
def pharmacy_permission_required(*permissions):
    """
    Decorator for views that checks whether a user has specific pharmacy permissions.
    Also verifies that users can only access their own pharmacy's data.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            if not all(request.user.has_perm(perm) for perm in permissions):
                if is_ajax:
                    return JsonResponse({
                        'status': 'error',
                        'message': "You don't have permission to access this page."
                    }, status=403)
                messages.error(request, "You don't have permission to access this page.")
                return redirect('forbidden')

            pharmacy_id = kwargs.get('pharmacy_id')
            if pharmacy_id and str(request.user.pharmacy.id) != str(pharmacy_id):
                messages.error(request, "You can only access your own pharmacy's data.")
                return redirect('admin_dash')

            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

def admin_required(view_func):
    """
    Decorator for views that checks if the user is a pharmacy admin.
    """
    def check_admin(user):
        return user.is_authenticated and user.is_admin
    
    return user_passes_test(check_admin, login_url='login')(view_func)

def superadmin_required(view_func):
    """
    Decorator for views that checks if the user is a superadmin.
    """
    def check_superadmin(user):
        return user.is_authenticated and user.is_superadmin
    
    return user_passes_test(check_superadmin, login_url='login')(view_func)

def staff_required(view_func):
    """
    Decorator for views that checks if the user is staff or higher.
    """
    def check_staff(user):
        return user.is_authenticated and (user.is_staff or user.is_admin or user.is_superadmin)
    
    return user_passes_test(check_staff, login_url='login')(view_func)