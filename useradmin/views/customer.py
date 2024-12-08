from django.shortcuts import render
from ..models import Customer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
 
@require_http_methods(["GET"])
def index(request):
    return render(request, "customer.html")


@csrf_exempt
@require_http_methods(["POST"])
def add_customer(request):
    data= json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob =  data.get('date_of_birth')
    email = data.get('email')
    phone_number = data.get('phone_number')
    address = data.get('address')
    allergies = data.get('allergies')

    Customer.objects.create(
       first_name=first_name,
       last_name=last_name,
       date_of_birth= dob,
       phone_number= phone_number,
       address=address,
       allergies=allergies,
       email=email

    )
    customers = list(Customer.objects.values())
    return JsonResponse({'status': 'success', 'message': 'Customer added successfully!', 'customers': customers})
 

@csrf_exempt
@require_http_methods(["PUT"])  
def update_customer(request):
  
    try:
        data= json.loads(request.body)
        customer_id= data.get("customer_id")
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        dob =  data.get('date_of_birth')
        email = data.get('email')
        phone_number = data.get('phone_number')
        address = data.get('address')
        allergies = data.get('allergies')

        customer = Customer.objects.get(id=customer_id)
        customer.first_name= first_name
        customer.last_name= last_name
        customer.date_of_birth= dob
        customer.address= address
        customer.allergies=allergies
        customer.email= email
        customer.phone_number= phone_number
        customer.save()
        customers = list(Customer.objects.values())
        return JsonResponse({'status': 'success', 'message': 'Medicine updated successfully!', 'customers': customers}, status=201)

    except Customer.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'customer not found.'
        }, status=404)
    
    except Exception as e:
        print(e)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)



@csrf_exempt
@require_http_methods(["DELETE"])  
def delete_customer(request):
    try:
        data = json.loads(request.body)
        customer_id = data.get('id')
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        customers = list(Customer.objects.values())
        return JsonResponse({'status': 'success', 'message': 'customer deleted successfully!', 'customers':customers})

    except Customer.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Customer not found.'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
def get_customers(request):
    if request.method == 'GET':
        customers = list(Customer.objects.values())
        return JsonResponse({'status': 'success', 'customers': customers})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
def get_customer(request):
    customer_id = request.GET.get('id')
    try:
        customer = Customer.objects.get(id=customer_id)
        data = {
            'status': 'success',
            'customer': {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone_number': customer.phone_number,
                "date_of_birth": customer.date_of_birth,
                "address":customer.address,
                "allergies":customer.allergies
            }
        }
        return JsonResponse(data)
    except Customer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Customer not found'})