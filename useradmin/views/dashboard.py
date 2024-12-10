from django.shortcuts import render
from ..models import *
from django.utils import timezone
from django.db.models import Sum

def index(request):
    tab = request.GET.get('tab', 'dash')  
    purchases = Purchase.objects.filter(purchase_date=timezone.now().date()).aggregate(Sum('total_price'))['total_price__sum']
    customers= Customer.objects.count()
    medicines= Medicine.objects.count()
    suppliers=Supplier.objects.count()

    return render(request, 'dashboard.html', {'active_tab': tab, 'customers':customers, 'medicines':medicines, 'suppliers':suppliers, 'purchases':purchases})

