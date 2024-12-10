from django.shortcuts import render
from ..models import Purchase, Medicine, Supplier
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
def index(request):
    medicines= Medicine.objects.all()
    suppliers= Supplier.objects.all()
    return render(request, "purchase.html", {"suppliers":suppliers, "medicines":medicines})


@csrf_exempt
@require_http_methods(["POST"])
def add_purchase(request):
    try:
        data = json.loads(request.body)
        quantity = data.get('quantity')
        medicine = Medicine.objects.get(id=data.get('medicine'))
        supplier = Supplier.objects.get(id=data.get('supplier'))
        Purchase.objects.create(
            medicine=medicine,
            quantity=int(quantity),
            supplier=supplier,
        )
        medicine.quantity_in_stock+=int(quantity)
        medicine.save()
        purchases = list(Purchase.objects.all())
        purchases=[{
                'id': purchase.id,
                'medicine':purchase.medicine.to_json(),
                'quantity': purchase.quantity,
                'total_price': purchase.total_price,
                'purchase_date': purchase.purchase_date,
                'supplier':purchase.supplier.to_json()
            
        } for purchase in purchases]
        return JsonResponse({'status': 'success', 'message': 'Purchase added successfully!', 'purchases': purchases})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_purchase(request):
    try:
        data = json.loads(request.body)
        quantity = data.get('quantity')
        medicine = Medicine.objects.get(id=data.get('medicine'))
        supplier = Supplier.objects.get(id=data.get('supplier'))
        purchase = Purchase.objects.get(id=data.get('purchase_id'))
        qty_to_use= 0
        if purchase.quantity>int(float(quantity)):
            qty_to_use=-(purchase.quantity-int(float(quantity)))
        elif purchase.quantity<int(float(quantity)):
            qty_to_use=(int(float(quantity))-purchase.quantity)
        else:
            qty_to_use=0
        purchase.medicine = medicine
        purchase.quantity =  int(float(quantity))
        purchase.supplier = supplier
        purchase.save()
        medicine.quantity_in_stock=medicine.quantity_in_stock + (qty_to_use)
        medicine.save()
        purchases = list(Purchase.objects.all())
        purchases=[{
                'id': purchase.id,
                'medicine':purchase.medicine.to_json(),
                'quantity': purchase.quantity,
                'total_price': purchase.total_price,
                'purchase_date': purchase.purchase_date,
                'supplier':purchase.supplier.to_json()
            
        } for purchase in purchases]
        return JsonResponse({'status': 'success', 'message': 'Purchase updated successfully!', 'purchases': purchases}, status=201)
    except Purchase.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Purchase not found.'}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_purchase(request):
    try:
        data = json.loads(request.body)
        purchase_id = data.get('id')
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.delete()

        purchases = list(Purchase.objects.all())
        purchases=[{
                'id': purchase.id,
                'medicine':purchase.medicine.to_json(),
                'quantity': purchase.quantity,
                'total_price': purchase.total_price,
                'purchase_date': purchase.purchase_date,
                'supplier':purchase.supplier.to_json()
            
        } for purchase in purchases]
        return JsonResponse({'status': 'success', 'message': 'Purchase deleted successfully!', 'purchases': purchases})
    except Purchase.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Purchase not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def get_purchases(request):
    if request.method == 'GET':
        purchases = list(Purchase.objects.all())
        purchases=[{
                'id': purchase.id,
                'medicine':purchase.medicine.to_json(),
                'quantity': purchase.quantity,
                'total_price': purchase.total_price,
                'purchase_date': purchase.purchase_date,
                'supplier':purchase.supplier.to_json()
            
        } for purchase in purchases]

        return JsonResponse({'status': 'success', 'purchases': purchases})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def get_purchase(request):
    purchase_id = request.GET.get('id')
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        data = {
            'status': 'success',
            'purchase': {
                'id': purchase.id,
                'medicine': purchase.medicine.to_json(),
                'quantity': purchase.quantity,
                'total_price': purchase.total_price,
                'purchase_date': purchase.purchase_date,
                'supplier': purchase.supplier.to_json()
            }
        }
        return JsonResponse(data)
    except Purchase.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Purchase not found'})
