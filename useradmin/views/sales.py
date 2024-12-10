from django.shortcuts import render
from ..models import  Medicine, Customer, Sales, Prescription
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
def index(request):
    medicines = Medicine.objects.all()
    customers = Customer.objects.all()
    return render(request, "sales.html", {"customers": customers, "medicines": medicines})

@csrf_exempt
@require_http_methods(["POST"])
def add_sale(request):
    try:
        data = json.loads(request.body)
        quantity = data.get('sale').get('quantity')
        medicine = Medicine.objects.get(id=data.get('sale').get('medicine'))
        customer = Customer.objects.get(id=data.get('sale').get("customer"))
        

        if medicine.quantity_in_stock < int(quantity):
            return JsonResponse({'status': 'error', 'message': 'Not enough stock available'}, status=400)
        if medicine.is_prescription_required and data.get("perscription"):
            perscription=Prescription.objects.create(
            customer= customer,
            medicine= medicine,
            doctor_name= data.get("perscription").get("doctor_name"),
            prescription_date=data.get("perscription").get("prescription_date"),
            dosage=data.get("perscription").get("prescription_date"),
            instructions=medicine.dosage_instructions
        )

        Sales.objects.create(
            medicine=medicine,
            quantity=int(quantity),
            customer=customer,
            total_price=medicine.price * int(quantity),
            prescription= perscription if medicine.is_prescription_required else None
        )
        medicine.quantity_in_stock -= int(quantity)
        medicine.save()

        sales = list(Sales.objects.all())
        sales = [ sale.to_json() for sale in sales]
        return JsonResponse({'status': 'success', 'message': 'Sales added successfully!', 'sales': sales})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_sale(request):
    try:
        data = json.loads(request.body)
        quantity = data.get('quantity')
        medicine = Medicine.objects.get(id=data.get('medicine'))
        customer = Customer.objects.get(id=data.get('customer'))
        sale = Sales.objects.get(id=data.get('sale_id'))

        qty_adjustment = int(quantity) - sale.quantity
        if qty_adjustment > 0 and medicine.quantity_in_stock < qty_adjustment:
            return JsonResponse({'status': 'error', 'message': 'Not enough stock available'}, status=400)

        sale.medicine = medicine
        sale.quantity = int(quantity)
        sale.customer = customer
        sale.total_price = medicine.price * int(quantity)
        sale.save()

        medicine.quantity_in_stock -= qty_adjustment
        medicine.save()

        sales = list(Sales.objects.all())
        sales = [ sale.to_json() for sale in sales]
        return JsonResponse({'status': 'success', 'message': 'Sales updated successfully!', 'sales': sales}, status=201)
    except Sales.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Sales not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_sale(request):
    try:
        data = json.loads(request.body)
        sale_id = data.get('id')
        sale = Sales.objects.get(id=sale_id)

        medicine = sale.medicine
        medicine.quantity_in_stock += sale.quantity
        medicine.save()

        sale.delete()

        sales = list(Sales.objects.all())
        sales = [ sale.to_json() for sale in sales]
        return JsonResponse({'status': 'success', 'message': 'Sales deleted successfully!', 'sales': sales})
    except Sales.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Sales not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def get_sales(request):
    if request.method == 'GET':
        sales = list(Sales.objects.all())
        sales = [ sale.to_json() for sale in sales]
        return JsonResponse({'status': 'success', 'sales': sales})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def get_sale(request):
    sale_id = request.GET.get('id')
    try:
        sale = Sales.objects.get(id=sale_id)
        data = {
            'status': 'success',
            'sale': sale.to_json()
        }
        return JsonResponse(data)
    except Sales.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Sales not found'})
