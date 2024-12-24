from django.shortcuts import render
from ..models import Medicine 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ..decorators import (
    pharmacy_permission_required,
    admin_required,
    superadmin_required,
    staff_required
)
 
@pharmacy_permission_required('authentication.view_medicines')
@require_http_methods(["GET"])
def index(request):
    return render(request, "medicine.html")

@pharmacy_permission_required('authentication.manage_medicines')
@csrf_exempt
@require_http_methods(["POST"])
def upload_medicine(request):
    data= json.loads(request.body)
    name = data.get('name')
    formulation = data.get('formulation')
    strength = data.get('strength')
    expiration_date = data.get('expiration_date')
    batch_number = data.get('batch_number')
    storage_conditions = data.get('storage_conditions')
    manufacturer = data.get('manufacturer')
    active_ingredients = data.get('active_ingredients')
    shelf_life = data.get('shelf_life')
    route_of_administration = data.get('route_of_administration')
    dosage_instructions = data.get('dosage_instructions')
    side_effects = data.get('side_effects')
    packaging_type = data.get('packaging_type')
    quantity_in_stock = data.get('quantity_in_stock')
    price = data.get('price')
    is_prescription_required = data.get('is_prescription_required')
    Medicine.objects.create(
        name=name,
        formulation=formulation,
        strength=strength,
        expiration_date=expiration_date,
        batch_number=batch_number,
        storage_conditions=storage_conditions,
        manufacturer=manufacturer,
        active_ingredients=active_ingredients,
        shelf_life=shelf_life,
        route_of_administration=route_of_administration,
        dosage_instructions=dosage_instructions,
        side_effects=side_effects,
        packaging_type=packaging_type,
        quantity_in_stock=quantity_in_stock,
        price=price,
        is_prescription_required=is_prescription_required
    )
    medicines = list(Medicine.objects.values())
    return JsonResponse({'status': 'success', 'message': 'Medicine added successfully!', 'medicines': medicines})
 


 
@pharmacy_permission_required('authentication.manage_medicines')
@csrf_exempt
@require_http_methods(["PUT"])  
def update_medicine(request):
    try:
        data = json.loads(request.body)
        medicine_id = data.get('medicine_id')
        name = data.get('name')
        formulation = data.get('formulation')
        strength = data.get('strength')
        expiration_date = data.get('expiration_date')
        batch_number = data.get('batch_number')
        storage_conditions = data.get('storage_conditions')
        manufacturer = data.get('manufacturer')
        active_ingredients = data.get('active_ingredients')
        shelf_life = data.get('shelf_life')
        route_of_administration = data.get('route_of_administration')
        dosage_instructions = data.get('dosage_instructions')
        side_effects = data.get('side_effects')
        packaging_type = data.get('packaging_type')
        quantity_in_stock = data.get('quantity_in_stock')
        price = data.get('price')
        is_prescription_required = data.get('is_prescription_required')

        medicine = Medicine.objects.get(id=medicine_id)
        medicine.name = name
        medicine.formulation = formulation
        medicine.strength = strength
        medicine.expiration_date = expiration_date
        medicine.batch_number = batch_number
        medicine.storage_conditions = storage_conditions
        medicine.manufacturer = manufacturer
        medicine.active_ingredients = active_ingredients
        medicine.shelf_life = shelf_life
        medicine.route_of_administration = route_of_administration
        medicine.dosage_instructions = dosage_instructions
        medicine.side_effects = side_effects
        medicine.packaging_type = packaging_type
        medicine.quantity_in_stock = quantity_in_stock
        medicine.price = price
        medicine.is_prescription_required = is_prescription_required
        medicine.save()
        medicines = list(Medicine.objects.values())
        return JsonResponse({'status': 'success', 'message': 'Medicine updated successfully!', 'medicines': medicines})

    except Medicine.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Medicine not found.'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@pharmacy_permission_required('authentication.manage_medicines')
@csrf_exempt
@require_http_methods(["DELETE"])  
def delete_medicine(request):
    try:
        data = json.loads(request.body)
        medicine_id = data.get('id')
        medicine = Medicine.objects.get(id=medicine_id)
        medicine.delete()
        medicines = list(Medicine.objects.values())
        return JsonResponse({'status': 'success', 'message': 'Medicine deleted successfully!', 'medicines': medicines})

    except Medicine.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Medicine not found.'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    

@pharmacy_permission_required('authentication.view_medicines')  
def get_medicines(request):
    if request.method == 'GET':
        medicines = list(Medicine.objects.values())
        return JsonResponse({'status': 'success', 'medicines': medicines})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
@pharmacy_permission_required('authentication.view_medicines')  
def get_medicine(request):
    medicine_id = request.GET.get('id')
    try:
        medicine = Medicine.objects.get(id=medicine_id)
        data = {
            'status': 'success',
            'medicine':  medicine.to_json()
        }
        return JsonResponse(data)
    except Medicine.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Medicine not found'})