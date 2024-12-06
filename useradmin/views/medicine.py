from django.shortcuts import render
from django.contrib import messages
from ..models import Medicine 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
 

def index(request):
    return render(request, "medicine.html")

@login_required
@csrf_exempt
def upload_medicine(request):
    if request.method == 'POST':
        # Get form data from the request
        name = request.POST.get('name')
        formulation = request.POST.get('formulation')
        strength = request.POST.get('strength')
        expiration_date = request.POST.get('expiration_date')
        batch_number = request.POST.get('batch_number')
        storage_conditions = request.POST.get('storage_conditions')
        manufacturer = request.POST.get('manufacturer')
        active_ingredients = request.POST.get('active_ingredients')
        shelf_life = request.POST.get('shelf_life')
        route_of_administration = request.POST.get('route_of_administration')
        dosage_instructions = request.POST.get('dosage_instructions')
        side_effects = request.POST.get('side_effects')
        packaging_type = request.POST.get('packaging_type')
        quantity_in_stock = request.POST.get('quantity_in_stock')
        price = request.POST.get('price')
        is_prescription_required = request.POST.get('is_prescription_required') == 'on'

        # Save the data to the database
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

        # Get all medicines as JSON
        medicines = list(Medicine.objects.values())
        return JsonResponse({'status': 'success', 'message': 'Medicine added successfully!', 'medicines': medicines})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})




@login_required
def get_medicines(request):
    if request.method == 'GET':
        medicines = list(Medicine.objects.values())
        return JsonResponse({'status': 'success', 'medicines': medicines})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
def get_medicine(request):
    medicine_id = request.GET.get('id')
    try:
        medicine = Medicine.objects.get(id=medicine_id)
        data = {
            'status': 'success',
            'medicine': {
                'id': medicine.id,
                'name': medicine.name,
                'formulation': medicine.formulation,
                'strength': medicine.strength,
                'expiration_date': medicine.expiration_date,
                'batch_number': medicine.batch_number,
                'storage_conditions': medicine.storage_conditions,
                'manufacturer': medicine.manufacturer,
                'active_ingredients': medicine.active_ingredients,
                'shelf_life': medicine.shelf_life,
                'route_of_administration': medicine.route_of_administration,
                'dosage_instructions': medicine.dosage_instructions,
                'side_effects': medicine.side_effects,
                'packaging_type': medicine.packaging_type,
                'quantity_in_stock': medicine.quantity_in_stock,
                'price': medicine.price,
                'is_prescription_required': medicine.is_prescription_required,
            }
        }
        return JsonResponse(data)
    except Medicine.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Medicine not found'})