from django.shortcuts import render
from authentication.models import Pharmacy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.contrib import messages
from ..decorators import (
    admin_required,
    superadmin_required,
    staff_required,
     pharmacy_permission_required,
)
@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@require_http_methods(["GET"])
def index(request):
    pharmacies = Pharmacy.objects.all()
    return render(request, "pharmacy.html", {"pharmacies": pharmacies})

@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@csrf_exempt
@require_http_methods(["POST"])
def add_pharmacy(request):
    try:
        data = json.loads(request.body)
        pharmacy = Pharmacy.objects.create(
            pharmacy_name=data.get('pharmacy_name'),
            address=data.get('address'),
            contact_email=data.get('contact_email'),
            contact_phone=data.get('contact_phone'),
            registration_number=data.get('registration_number'),
            license_number=data.get('license_number'),
            opening_hours=data.get('opening_hours')
        )
        return JsonResponse({'status': 'success', 'message': 'Pharmacy added successfully!', 'pharmacy': pharmacy.to_json()})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@csrf_exempt
@require_http_methods(["PUT"])
def update_pharmacy(request):
    try:
        data = json.loads(request.body)
        pharmacy = Pharmacy.objects.get(id=data.get('id'))
        pharmacy.pharmacy_name = data.get('pharmacy_name')
        pharmacy.address = data.get('address')
        pharmacy.contact_email = data.get('contact_email')
        pharmacy.contact_phone = data.get('contact_phone')
        pharmacy.registration_number = data.get('registration_number')
        pharmacy.license_number = data.get('license_number')
        pharmacy.opening_hours = data.get('opening_hours')
        pharmacy.save()
        messages.success(request, 'Pharmacy information updated successfully!')
        return JsonResponse({'status': 'success', 'message': 'Pharmacy updated successfully!', 'pharmacy': pharmacy.to_json()})
    except Pharmacy.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Pharmacy not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_pharmacy(request):
    try:
        data = json.loads(request.body)
        pharmacy_id = data.get('id')
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
        pharmacy.delete()
        return JsonResponse({'status': 'success', 'message': 'Pharmacy deleted successfully!'})
    except Pharmacy.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Pharmacy not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@require_http_methods(["GET"])
def get_pharmacies(request):
    pharmacies = Pharmacy.objects.all()
    pharmacies = [pharmacy.to_json() for pharmacy in pharmacies]
    return JsonResponse({'status': 'success', 'pharmacies': pharmacies})

@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@require_http_methods(["GET"])
def get_pharmacy(request):
    try:
        pharmacy = Pharmacy.objects.get(id=request.user.pharmacy.id)
        return JsonResponse({'status': 'success', 'data': pharmacy.to_json()})
    except Pharmacy.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Pharmacy not found.'})
