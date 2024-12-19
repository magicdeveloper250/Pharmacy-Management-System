from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ..models import Sales
from django.http import FileResponse, HttpResponse

@require_http_methods(["GET"])
def invoice(request,sale_id):
    try:
        sale= Sales.objects.get(id=sale_id)
        if sale.receipt and sale.receipt.storage.exists(sale.receipt.name):
            return FileResponse(sale.receipt.open('rb'), filename=f"invoice_{sale.id}.pdf")
        else:
        
            return HttpResponse("Invoice not", status=404)
    except Sales.DoesNotExist:

        return HttpResponse("Invoice not found", status=404)


 