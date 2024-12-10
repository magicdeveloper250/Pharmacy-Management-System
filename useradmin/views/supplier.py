from django.shortcuts import render
from django.http import JsonResponse
from ..models import Supplier
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
def index(request):
    return render(request, "supplier.html")

@csrf_exempt
@require_http_methods(["POST"])
def add_supplier(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        contact_name = data.get('contact_name')
        phone = data.get('contact_phone')
        email = data.get('contact_email')
        address = data.get('address')
        lead_time = data.get('lead_time')
        payment_terms= data.get("payment_terms")

        Supplier.objects.create(
            name=name,
            contact_name=contact_name,
            contact_phone=phone,
            contact_email=email,
            address=address,
            lead_time=lead_time,
            payment_terms=payment_terms
          
        )

        suppliers = list(Supplier.objects.values())
        return JsonResponse({'status': 'success', 'message': 'Supplier added successfully!', 'suppliers': suppliers})

    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_supplier(request):
    print(json.loads(request.body))
    try:
        data = json.loads(request.body)
        supplier_id = data.get('supplier_id')
        name = data.get('name')
        contact_name = data.get('contact_name')
        phone = data.get('contact_phone')
        email = data.get('contact_email')
        address = data.get('address')
        payment_terms = data.get('payment_terms')
        lead_time= data.get("lead_time")

        supplier = Supplier.objects.get(id=supplier_id)
        supplier.name = name
        supplier.contact_name = contact_name
        supplier.contact_phone = phone
        supplier.contact_email = email
        supplier.address = address
        supplier.payment_terms=payment_terms
        supplier.lead_time= lead_time
       
        supplier.save()

        suppliers = list(Supplier.objects.values())
        return JsonResponse({'status': 'success', 'message': 'Supplier updated successfully!', 'suppliers': suppliers})

    except Supplier.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Supplier not found.'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_supplier(request):
    try:
        data = json.loads(request.body)
        supplier_id = data.get('id')

        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()

        suppliers = list(Supplier.objects.values())
        return JsonResponse({'status': 'success', 'message': 'Supplier deleted successfully!', 'suppliers': suppliers})

    except Supplier.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Supplier not found.'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def get_suppliers(request):
    if request.method == 'GET':
        suppliers = list(Supplier.objects.values())
        return JsonResponse({'status': 'success', 'suppliers': suppliers})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def get_supplier(request):
    supplier_id = request.GET.get('id')
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        data = {
            'status': 'success',
            'supplier': supplier.to_json()
        }
        return JsonResponse(data)
    except Supplier.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Supplier not found'}, status=404)
