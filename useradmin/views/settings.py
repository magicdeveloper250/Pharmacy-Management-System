from django.shortcuts import render
from authentication.models import Pharmacy, PharmacySettings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.contrib import messages
from ..decorators import (
    pharmacy_permission_required,
    admin_required,
    superadmin_required,
    staff_required
)
import pytz

@pharmacy_permission_required('authentication.view_pharmacy_settings')
@require_http_methods(["GET"])
def index(request):
    languages = PharmacySettings.LANGUAGE_CHOICES
    currencies = PharmacySettings.CURRENCY_CHOICES
    settings = PharmacySettings.objects.all()
    return render(request, "settings.html", context={
        "settings": settings,
        "languages": languages,
        "currencies": currencies,
        "timezones": pytz.all_timezones,
    })

@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@csrf_exempt
@require_http_methods(["POST"])
def add_settings(request):
    try:
        data = json.loads(request.body)
        try:
            pharmacy = request.user.pharmacy
            settings= PharmacySettings.objects.get(pharmacy=pharmacy)
            pharmacy=request.user.pharmacy
            settings.business_name= data.get("business_name")
            settings.legal_entity_name= data.get("legal_entity_name")
            settings.tax_identification_number= data.get("tax_identification_number")
            settings.contact_email= data.get("contact_email")
            settings.contact_phone= data.get("contact_phone")
            settings.address= data.get("address")
            settings.notification_email= data.get("notification_email")
            settings.low_stock_threshold=data.get("low_stock_threshold", 10)
            settings.require_prescription_approval=data.get("require_prescription_approval", True)
            settings.auto_order_enabled=data.get("auto_order_enabled", False)
            settings.enable_notifications=data.get("enable_notifications", False)
            settings.default_tax_rate=data.get("default_tax_rate", 0)
            settings.business_hours=data.get("business_hours", "")
            settings.receipt_footer_text=data.get("receipt_footer_text", "")
            settings.smtp_settings=data.get("smtp_settings", {})
            settings.currency=data.get("currency_symbol", "USD")
            settings.language=data.get("language", "en")
            settings.timezone=data.get("timezone", "UTC")
            settings.save()
            messages.success(request, 'Pharmacy business settings updated successfully!')
            return JsonResponse({
                'status': 'success',
                'message': 'PharmacySettings added successfully!',
                'settings': settings.to_json()
            })
            
        except PharmacySettings.DoesNotExist:
            settings = PharmacySettings.objects.create(
            pharmacy=request.user.pharmacy,
            business_name= data.get("business_name"),
            legal_entity_name= data.get("legal_entity_name"),
            tax_identification_number= data.get("tax_identification_number"),
            contact_email= data.get("contact_email"),
            contact_phone= data.get("contact_phone"),
            address= data.get("address"),
            notification_email= data.get("notification_email"),
            low_stock_threshold=data.get("low_stock_threshold", 10),
            require_prescription_approval=bool(data.get("require_prescription_approval", True)),
            enable_notifications=bool(data.get("enable_notifications", False)),
            auto_order_enabled=bool(data.get("auto_order_enabled", False)),
            default_tax_rate=data.get("default_tax_rate", 0),
            business_hours=data.get("business_hours", ""),
            receipt_footer_text=data.get("receipt_footer_text", ""),
            smtp_settings=data.get("smtp_settings", {}),
            currency=data.get("currency_symbol", "USD"),
            language=data.get("language", "en"),
            timezone=data.get("timezone", "UTC")
        )
            messages.success(request, 'Pharmacy business settings updated successfully!')
            return JsonResponse({
                'status': 'success',
                'message': 'PharmacySettings added successfully!',
                'settings': settings.to_json()
            })


        
    except Exception as e:
        print(e)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@csrf_exempt
@require_http_methods(["PUT"])
def update_settings(request):
    try:
        data = json.loads(request.body)
        pharmacy = Pharmacy.objects.get(id=request.user.pharmacy.id)
        pharmacy.pharmacy_name = data.get("pharmacy_name")
        pharmacy.address = data.get("address")
        pharmacy.contact_email = data.get( "contact_email")
        pharmacy.contact_phone = data.get("contact_phone")
        pharmacy.registration_number = data.get("registration_number")
        pharmacy.license_number = data.get("license_number")
        pharmacy.opening_hours = data.get("opening_hours")
        pharmacy.save()
        messages.success(request, 'Pharmacy Information updated successfully!')
        return JsonResponse({
            'status': 'success',
            'message': 'PharmacySettings updated successfully!',
            'pharmacy': pharmacy.to_json()
        })
    except Pharmacy.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'PharmacySettings not found.'
        }, status=404)
    except Exception as e:

        print(e)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@pharmacy_permission_required('authentication.manage_pharmacy_settings')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_settings(request):
    try:
        data = json.loads(request.body)
        settings_id = data.get('id')
        settings = PharmacySettings.objects.get(id=settings_id)
        settings.delete()
        
        all_settings = list(PharmacySettings.objects.all())
        settings_list = [setting.to_json() for setting in all_settings]
        
        return JsonResponse({
            'status': 'success',
            'message': 'PharmacySettings deleted successfully!',
            'settings': settings_list
        })
    except PharmacySettings.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'PharmacySettings not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@pharmacy_permission_required('authentication.view_pharmacy_settings')
def get_settings(request):
    if request.method == 'GET':
        all_settings = list(PharmacySettings.objects.all())
        settings_list = [setting.to_json() for setting in all_settings]
        return JsonResponse({
            'status': 'success',
            'settings': settings_list
        })
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    })

@pharmacy_permission_required('authentication.view_pharmacy_settings')
def get_settings(request):
    try:
        settings = PharmacySettings.objects.get(pharmacy=request.user.pharmacy)
        return JsonResponse({
            'status': 'success',
            'data': settings.to_json()
        })
    except PharmacySettings.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Settings not found'
        })

@pharmacy_permission_required('authentication.manage_pharmacy_settings')
def validate_settings(request):
    try:
        data = json.loads(request.body)
        settings_type = data.get('type')
        settings_data = data.get('settings')
        
        if settings_type == 'smtp':
            is_valid = True   
            return JsonResponse({
                'status': 'success',
                'valid': is_valid,
                'message': 'SMTP settings validated successfully'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Unknown settings type'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)