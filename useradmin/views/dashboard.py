from django.shortcuts import render
from ..models import *
from django.utils import timezone
from django.db.models import Sum
from ..decorators import (
    pharmacy_permission_required,
    admin_required,
    superadmin_required,
    staff_required
)
from django.db.models import Count

@staff_required
def index(request):
    tab = request.GET.get('tab', 'dash')  
    purchases = Purchase.objects.filter(purchase_date=timezone.now().date()).aggregate(Sum('total_price'))['total_price__sum']
    sales = Sales.objects.filter(sale_date=timezone.now().date()).aggregate(Sum('total_price'))['total_price__sum']
    customers= Customer.objects.annotate(customer_cout= Count("id"))
    customers_count= customers.count()
    medicines= Medicine.objects.annotate(medicine_count= Count("id"))
    medicines_count= medicines.count()
    suppliers=Supplier.objects.annotate(supplier_count= Count("id"))
    suppliers_count= suppliers.count()
    medicines_count = Medicine.objects.count()
    medicines_expiring_soon = Medicine.objects.filter(expiration_date__lte=timezone.now().date() + timezone.timedelta(days=30))
   
    total_quantity_in_stock = Medicine.objects.aggregate(Sum('quantity_in_stock'))['quantity_in_stock__sum'] or 0
    total_stock_value = Medicine.objects.aggregate(Sum('price'))['price__sum'] or 0

    return render(request, 'dashboard.html', {'active_tab': tab, 'customers':customers_count, 'medicines':medicines_count, 'suppliers':suppliers_count, 'purchases':purchases, 'sales':sales,'medicines_count': medicines_count,
        'expired_medicines': medicines_expiring_soon,
        'total_quantity_in_stock': total_quantity_in_stock,
        'total_stock_value': total_stock_value,})

